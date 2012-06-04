#!/usr/bin/python
import os
import subprocess
import time
import sys

def listen(root=None):
    nc = subprocess.Popen(['nc', '-l', '8000'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    for line in iter(nc.stdout.readline,''):
        line = line.rstrip()
        if line.startswith("GET"):
            if root is None:
                nc.stdin.write("Hello world!")
            else:
                file = line.split(" ")[1]
                if file == "/":
                    file = file + "index.html"
                try:
                    f = open(root + file)
                    for line in iter(f.readlines()):
                        nc.stdin.write(line)
                except IOError:
                    nc.stdin.write("404: Page Not Found")
            nc.terminate()


def main():
    argv = sys.argv
    root = None
    if len(argv) > 1:
        root = argv[1]
    while 1:
        cont = listen(root=root)

if __name__ == "__main__":
    main()
