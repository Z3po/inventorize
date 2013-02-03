#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Inenvorize information and push to inventorize server

from optparse import OptionParser
from ConfigParser import RawConfigParser
from sys import exit
from sys import path as sys_path

# Internals
active_modules = {}

parser = OptionParser() # {{{

parser.add_option("-f", "--file", dest="configfile",
                    help="configuration-file with inventory instructions", metavar="FILE")

options, args = parser.parse_args()
# }}}

def parseconfig(): # {{{
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

        if confparser.has_option('Main', 'checks_enabled'):
            configdict.update({ 'checks_enabled' : confparser.get('Main', 'checks_enabled').split() })
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

def load_module(module): # {{{
    if module == None:
        exit(0)
    else:
        try:
            return __import__(module)
        except:
            raise StandardError('you need to have the module in place')
# }}}

def add_module(check_name): # {{{
    global active_modules
    arguments = get_arguments(check_name)
    arguments.update({ 'name' : check_name })
    if arguments['module'] not in active_modules:
        module = load_module(arguments['module'])
        active_modules.update({ arguments['module'] :  getattr(module, module.__name__)() })
    active_modules[arguments['module']].add_arguments(arguments)
# }}}

def run_modules(): # {{{
    for module in active_modules:
        active_modules[module].run()
# }}}
 
def send_data(inventorize_server): # {{{
    for module in active_modules:
        result = active_modules[module].get_results()
        print str(result)
# }}}

if __name__ == '__main__':
    if not options.configfile:
        parser.error('We need to have the configfile')
    else:
        confparser = RawConfigParser()
        confparser.read(options.configfile)
        configdict = parseconfig()
        for check in configdict['checks_enabled']:
            add_module(check)
        run_modules()
        send_data(configdict['inventorize_server'])

# vim:filetype=python:foldmethod=marker:autoindent:expandtab:tabstop=4
