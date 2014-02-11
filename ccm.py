#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
(C) Copyright [2014] InfoSec Consulting, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 
http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

         ...
    .:::|#:#|::::.
 .:::::|##|##|::::::.
 .::::|##|:|##|:::::.
  ::::|#|:::|#|:::::
  ::::|#|:::|#|:::::
  ::::|##|:|##|:::::
  ::::.|#|:|#|.:::::
  ::|####|::|####|::
  :|###|:|##|:|###|:
  |###|::|##|::|###|
  |#|::|##||##|::|#|
  |#|:|##|::|##|:|#|
  |#|##|::::::|##|#|
   |#|::::::::::|#|
    ::::::::::::::
      ::::::::::
       ::::::::
        ::::::
          ::
"""
__author__ = 'Avery Rozar'

import argparse
import ConfigParser
import sys
from modules.enable_mode import *
from modules.send_cmd import *
from modules.cmds import *

def main(argv=None):
    if argv is None:
        argv = sys.argv
    conf_parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
                                          add_help=False)
    conf_parser.add_argument('--conf_file', help='Specify a conf file', metavar='FILE')
    conf_parser.add_argument('--host_file', dest='hosts', type=file, help='specify a target host file')
    args, remanaing_argv = conf_parser.parse_known_args()

    if args.conf_file:
        conf = ConfigParser.SafeConfigParser()
        conf.read([args.conf_file])
        defaults = dict(conf.items('Defaults'))
    else:
        defaults = {'option': 'default'}
    parser = argparse.ArgumentParser(parents=[conf_parser])
    parser.set_defaults(**defaults)
    parser.add_argument('--option')

    args = parser.parse_args()
    hosts = args.hosts
    user = args.user
    passwd = args.passwd
    en_passwd = args.en_passwd

    if hosts:
        for line in hosts:
            host = line.rstrip()
            child = enable_mode(user, host, passwd, en_passwd)

            if child:
                send_command(child, SHOWRUN)
    else:
        print('I need hosts!!')
if __name__ == '__main__':
    main()