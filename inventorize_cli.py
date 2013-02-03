#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Inenvorize information and push to inventorize server

from optparse import OptionParser
from ConfigParser import RawConfigParser
from sys import exit
from sys import path as sys_path

parser = OptionParser() # {{{

parser.add_option("-f", "--file", dest="configfile",
                    help="configuration-file with inventory instructions", metavar="FILE")

options, args = parser.parse_args()
# }}}

def parsedata(): # {{{
    configdict = {}
    if not confparser.has_section('Main'):
        raise StandardError('No Main Section found in configfile...')
    else:
        if confparser.has_option('Main', 'modulepath'):
            sys_path.append(confparser.get('Main', 'modulepath'))
        else:
            print 'Please give a valid modulepath in configfiles Main Section'
            exit(255)

        if confparser.has_option('Main', 'inventorize_server'):
            configdict.update({ 'inventorize_server' : confparser.get('Main', 'inventorize_server') })
        else:
            print 'Please give a valid inventorize Server'
            exit(255)

        if confparser.has_option('Main', 'modules_enabled'):
            configdict.update({ 'modules_enabled' : confparser.get('Main', 'modules_enabled').split() })
    return configdict
# }}}

def get_arguments(configsection): # {{{
    argumentdict = {}
    if confparser.has_section(configsection):
        for option in confparser.options(configsection):
            argumentdict.update({ option : confparser.get(configsection, option) })
    else:
        print 'activated module has no options'
        exit(255)
    return argumentdict
# }}}

def load_modules(modules): # {{{
    if modules == None:
        exit(0)
    else:
        try:
            return __import__(module)
        except:
            raise StandardError('you need to have the module in place')
# }}}
 
def send_data(inventorize_server, result): # {{{
    pass
# }}}

if __name__ == '__main__':
    if not options.configfile:
        parser.error('We need to have the configfile')
    else:
        confparser = RawConfigParser()
        confparser.read(options.configfile)
        configdict = parsedata()
        for module in configdict['modules_enabled']:
            arguments = get_arguments(module)
            active_module = load_modules(module)
            result = active_module.run(arguments)
            send_data(configdict['inventorize_server'], result)
