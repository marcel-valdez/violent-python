import zipfile
import optparse
from threading import Thread
import sys

def extractFile(zFile, password):
  zFile = zipfile.ZipFile(zFile)
  zFile.extractall(pwd = password)

def findPassword(zipfilename, dictionary):
  for line in open(dictionary).readlines():
    try:
      password = line.strip('\n')
      extractFile(zipfilename, password)
      return password
    except Exception, e:
      pass

  return None

def main():
  parser = optparse.OptionParser('usage%prog -f <zpfile> -d <dictionary>')
  parser.add_option('-f', dest = 'zname', type = 'string', help = 'specify zip file')
  parser.add_option('-d', dest = 'dname', type = 'string', help = 'specify dictionary file')
  (options, args) = parser.parse_args()

  dictionary = options.dname
  zipfilename = options.zname
  if (options.zname == None) | (options.dname == None):
    print parser.usage
    zipfilename = 'evil.zip'
    dictionary = 'dictionary.txt'
    # exit(0)

  password = findPassword(zipfilename, dictionary)
  if password != None:
    print '[+] Password is: ' + password
    sys.exit(0)
  else:
    print '[-] Password not found.'
    sys.exit(1)

if __name__ == '__main__':
  main()