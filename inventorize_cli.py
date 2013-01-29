#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Inenvorize information and push to inventorize server

from optparse import OptionParser
from ConfigParser import RawConfigParser
from sys import exit

# Main Variables
modulepath = None
inventorize_server = None
modules_enabled = None

parser = OptionParser() # {{{

parser.add_option("-f", "--file", dest="configfile",
                    help="configuration-file with inventory instructions", metavar="FILE")

options, args = parser.parse_args()
# }}}

def parsedata(): # {{{
    global inventorize_server, modulepath, modules_enabled
    if not confparser.has_section('Main'):
        raise StandardError('No Main Section found in configfile...')
    else:
        if confparser.has_option('Main', 'modulepath'):
            modulepath = confparser.get('Main', 'modulepath')
        else:
            print 'Please give a valid modulepath in configfiles Main Section'
            exit(255)

        if confparser.has_option('Main', 'inventorize_server'):
            inventorize_server = confparser.get('Main', 'inventorize_server')
        else:
            print 'Please give a valid inventorize Server'
            exit(255)

        if confparser.has_option('Main', 'modules_enabled'):
            modules_enabled = confparser.get('Main', 'modules_enabled').split()
# }}}

def get_arguments(configsection): # {{{
    if confparser.has_section(configsection):
        pass
    else:
        print 'activated module is not available'
        exit(255)
# }}}

def load_modules(modules):
    if modules == None:
        exit(0)
    else:
        for module in modules:
            arguments = get_arguments(module)
            try:
                active_module = __import__(modulepath + '/' + module)
            except:
                raise StandardError('you need to have the module in place')
 

if __name__ == '__main__':
    if not options.configfile:
        parser.error('We need to have the configfile')
    else:
        confparser = RawConfigParser()
        confparser.read(options.configfile)
        parsedata()
        load_modules(modules_enabled)
