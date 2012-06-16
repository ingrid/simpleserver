#!/usr/bin/python
import os
import subprocess
import time
import socket
import sys
import mimetypes
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import utils, encoders

var = {}
port = 8000

def main():
    argv = sys.argv
    var['root'] = "."
    if len(argv) > 1:
        var['root'] = argv[1]
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((socket.gethostname(), port))
    print "Hostname:", socket.gethostbyname(socket.gethostname())
    print "Connected on port", port
    serversocket.listen(5)

    while 1: 
        client, address = serversocket.accept() 
        data = client.recv(1024) 
        if data:
            headers = data.split(' ')[1]
            file = headers
            print headers
            client.send(get_file(file)) 
            # Not sure how to use shut down appropriately.
            #client.shutdown(socket.SHUT_RDWR)
        client.close()

def get_file(file):
    ret = ""
    if file == "/":
        file = file + "index.html"
    file = var['root'] + file
    if not os.path.exists(file):
        ret = "404: Page Not Found"
    else:
        f = open(file)
        
        ret += 'HTTP/1.0 200 OK\r\n'
        if file.endswith('.html'):
            ret += "Content-Type: text/html\r\n\r\n"
        elif file.endswith('.css'):
            ret += "Content-Type: text/css\r\n\r\n"
        elif file.endswith('.png'):
            ret += "Content-Type: image/png\r\n\r\n"
        for line in iter(f.readlines()):
            ret += line
    return ret
if __name__ == "__main__":
    main()
