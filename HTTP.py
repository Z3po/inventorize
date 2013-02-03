# -*- coding: utf-8 -*-
#
'''HTTP Module

This Module is Handling HTTP requests.'''

from sys import exit
import urllib
from re import search as re_search

def connect_HTTP(url, expect):
    print 'connect_HTTP'
    if expect == 'None':
        expect = ''
    urlhandle = urllib.urlopen(url)
    for line in urlhandle.read():
        print str(line)
        if re_search(expect, line):
            return True

    return False

def run(argumentdict): # {{{
    functions = globals()
    count = 1
    while 'action' + str(count) in argumentdict:
        print str(functions)
        functions.get('action' + str(count))('test')
        if getattr(argumentdict['action' + str(count)], argumentdict['url' + str(count)], argumentdict['expect' + str(count)]):
            print 'YES'
        count += 1


# }}}
