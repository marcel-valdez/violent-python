'''
  Simple vulnerable server for the violent python examples
'''

import socket
import sys
from thread import *

def send_greeting(connection, address):
  connection.send('FreeFloat FtpServer (Version 1.00)')
  connection.close()

HOST = ''
PORT = 1121

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# bind socket to local host and port
try:
  serverSocket.bind((HOST, PORT))
except socket.error as msg:
  print 'bind failed. Error Code: ' + str(msg[0]) + '. Message: ' + msg[1]
  sys.exit()

print 'Socket bind complete'

# Start listening on socket
serverSocket.listen(10)
print 'Socket now listening'

# Now keep talking with the client
while 1:
  # wait to accept a connection - blocking call
  connection, address = serverSocket.accept()
  print 'Connected with ' + address[0] + ':' + str(address[1])
  start_new_thread(send_greeting, (connection, address))

serverSocket.close()
