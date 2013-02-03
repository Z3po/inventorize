# -*- coding: utf-8 -*-
#
'''HTTP Module

This Module is Handling HTTP requests.
When initializing class HTTP you need to pass the argument dictionary holding the configuration and the result_name.
Parameters:
            - name   : The name the resultdict should hold (like "ACCESS_WEBSITE_XYZ" so you can identify your results later on)
            - action : The action to trigger. Any of "connect_HTTP,"
            - url    : The URL we are trying to access
            - expect : What is expected to come back

import HTTP

http_module = HTTP.HTTP()
http_module.add_arguments( { 'name' : 'check_http_google', 'action' : 'connect_HTTP', 'url' : 'http://www.google.de', 'expect' : None } )
http_module.run()
results = http_module.get_results()
'''

import urllib
from re import search as re_search

class HTTP(object): # {{{
    resultdict = {}
    argumentlist = []

    def add_arguments(self, argumentdict): # {{{
        self.argumentlist.append(argumentdict)
    # }}}

    def append_results(self, result, arguments): # {{{
        self.resultdict.update({ arguments['name'] : 
                            { 'result' : result,
                                'url' : arguments['url'],
                                'expect' : arguments['expect']
                            }
                        })
    # }}}

    def get_results(self): # {{{
        return self.resultdict
    # }}}

    def connect_HTTP(self, arguments): # {{{
        if arguments['expect'] == 'None':
            expect = ''
        else:
            expect = arguments['expect']
        try:
            urlhandle = urllib.urlopen(arguments['url'])
            for line in urlhandle.readlines():
                if re_search(expect, line.strip()):
                    return True
        except:
            return False

        return False
    # }}}

    def run(self): # {{{
        for argumentdict in self.argumentlist:
            result = getattr(self, argumentdict['action'])(argumentdict)
            self.append_results(result, argumentdict)
    # }}}

# }}}

# vim:filetype=python:foldmethod=marker:autoindent:expandtab:tabstop=4
