#!/usr/bin/python
# -*- coding: utf-8 -*-
# (C) Copyright [2014] Avery Rozar

__author__ = 'Avery Rozar'

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from ConfigParser import SafeConfigParser
from time import strftime, localtime
from lib.enable_mode import ssh_enable_mode, telnet_enable_mode
from lib.send_cmd import send_command
from lib.cmds import SHOWRUN
import sys


def main():
  conf_parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter,
                               add_help=False)
  conf_parser.add_argument('--conf_file', help='Specify a conf file', metavar='FILE')
  conf_parser.add_argument('--host_file', dest='hosts', type=file, help='specify a target host file')
  args, remanaing_argv = conf_parser.parse_known_args()
  if args.conf_file:
    conf = SafeConfigParser()
    conf.read([args.conf_file])
    defaults = dict(conf.items('Defaults'))
  else:
      defaults = {'option': 'default'}
  parser = ArgumentParser(parents=[conf_parser])
  parser.set_defaults(**defaults)
  args = parser.parse_args()
  hosts = args.hosts
  user = args.user
  passwd = args.passwd
  en_passwd = args.en_passwd
  conf_path = args.conf_path
  use_telnet = args.use_telnet
  if hosts:
    for line in hosts:
      host = line.rstrip()
      if use_telnet == 'yes':  # Please don't
        telnet_child = telnet_enable_mode(host, passwd, en_passwd)
        if telnet_child:
          current_time = strftime('%m.%d.%y.%M.%S', localtime())
          output_name = conf_path+'/{0}_{1}.txt'.format(host, current_time)
          sys.stdout = open(output_name, 'w')
          send_command(telnet_child, SHOWRUN)
      else:
        ssh_child = ssh_enable_mode(user, host, passwd, en_passwd)
        if ssh_child:
          current_time = strftime('%m.%d.%y.%M.%S', localtime())
          output_name = conf_path+'/{0}_{1}.txt'.format(host, current_time)
          sys.stdout = open(output_name, 'w')
          send_command(ssh_child, SHOWRUN)
  else:
      print('I need hosts!!')


if __name__ == '__main__':
  try:
    main()
  except (IOError, SystemExit):
    raise
  except KeyboardInterrupt:
    print('Crtl+C Pressed. Shutting down.')
