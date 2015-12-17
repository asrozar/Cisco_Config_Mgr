#!/usr/bin/python
# -*- coding: utf-8 -*-
# (C) Copyright [2014] Avery Rozar

__author__ = 'Avery Rozar'


from os import system
try:
  import pexpect

except ImportError:
  print('Installing pexpect..')
  try:
    system('sudo easy_install pexpect')
    import pexpect
  except:
    print('You will need to run this as sudo the first time to install pexpect')
    exit()

from lib.prompts import PRIV_EXEC_MODE
from lib.cmds import IOSTERMLEN0, SHOWVER, QOUTMORE, ASATERMPAGER0


def ssh_enable_mode(user, host, passwd, en_passwd):
    ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
    constr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(constr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:', '.Connection refused.'])

    if ret == 0:
        print '[-] Error Connecting to ' + host
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT])
        if ret == 0:
            print '[-] Could not accept new key from ' + host
            return
    if ret == 3:
        print '[-] Could not connect to ' + host
        return
    child.sendline(passwd)
    auth = child.expect(['[P|p]assword:', '.>', '.#'])
    if auth == 0:
        print 'User password is incorrect'
        return
    if auth == 1:
        child.sendline('enable')
        child.sendline(en_passwd)
        enable = child.expect([pexpect.TIMEOUT, '.#'])
        if enable == 0:
            print 'enable password for ' + host + ' is incorrect'
            return
        if enable == 1:
            child.sendline(SHOWVER)  # find out what Cisco OS we are working with
            what_os = child.expect([pexpect.TIMEOUT, '.IOS.', '.Adaptive.', '.Nexus.'])
            if what_os == 0:
                print 'show ver' + ' time out' + ' for ' + host
                return
            if what_os == 1:  # IOS
                child.sendcontrol('c')
                child.expect(PRIV_EXEC_MODE)
                child.sendline(IOSTERMLEN0)
                child.expect(PRIV_EXEC_MODE)
                return child
            if what_os == 2:  # ASAOS
                child.send(QOUTMORE)
                child.expect(PRIV_EXEC_MODE)
                child.sendline(ASATERMPAGER0)
                child.expect(PRIV_EXEC_MODE)
                return child
            if what_os == 3:  # NX-OS
                child.sendcontrol('c')
                child.expect(PRIV_EXEC_MODE)
                child.sendline(IOSTERMLEN0)
                child.expect(PRIV_EXEC_MODE)
                return child

    if auth == 2:
        child.sendline(SHOWVER)  # find out what Cisco OS we are working with
        what_os = child.expect([pexpect.TIMEOUT,  '.IOS.', '.Adaptive.', '.Nexus.'])
        if what_os == 0:
            print 'show ver' + ' time out' + 'for ' + host
            return
        if what_os == 1:  # IOS
            child.sendcontrol('c')
            child.expect(PRIV_EXEC_MODE)
            child.sendline(IOSTERMLEN0)
            child.expect(PRIV_EXEC_MODE)
            return child
        if what_os == 2:  # ASAOS
            child.send(QOUTMORE)
            child.expect(PRIV_EXEC_MODE)
            child.sendline(ASATERMPAGER0)
            child.expect(PRIV_EXEC_MODE)
            return child
        if what_os == 3:  # NX-OS
            child.sendcontrol('c')
            child.expect(PRIV_EXEC_MODE)
            child.sendline(IOSTERMLEN0)
            child.expect(PRIV_EXEC_MODE)
            return child

    else:
        print 'Failed to log in to ' + host


def telnet_enable_mode(host, passwd, en_passwd):
    constr = 'telnet ' + host
    child = pexpect.spawn(constr)
    ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])

    if ret == 0:
        print '[-] Error Connecting to ' + host
        return
    if ret == 1:
        child.sendline(passwd)

    auth = child.expect(['[P|p]assword:', '.>', '.#'])
    if auth == 0:
        print 'Password is incorrect'
        return
    if auth == 1:
        child.sendline('enable')
        child.sendline(en_passwd)
        enable = child.expect([pexpect.TIMEOUT, '.#'])
        if enable == 0:
            print 'enable password for ' + host + ' is incorrect'
            return
        if enable == 1:
            child.sendline(SHOWVER)  # find out what Cisco OS we are working with
            what_os = child.expect([pexpect.TIMEOUT, '.IOS.', '.Adaptive.'])
            if what_os == 0:
                print 'show ver' + ' time out' + 'for ' + host
                return
            if what_os == 1:  # IOS
                child.sendcontrol('c')
                child.expect(PRIV_EXEC_MODE)
                child.sendline(IOSTERMLEN0)
                child.expect(PRIV_EXEC_MODE)
                return child
            if what_os == 2:  # ASAOS
                child.sendline(QOUTMORE)
                child.expect(PRIV_EXEC_MODE)
                child.sendline(ASATERMPAGER0)
                child.expect(PRIV_EXEC_MODE)
                return child
    if auth == 2:
        child.sendline(SHOWVER)  # find out what Cisco OS we are working with
        what_os = child.expect([pexpect.TIMEOUT,  '.IOS.', '.Adaptive.'])
        if what_os == 0:
            print 'show ver' + ' time out' + 'for ' + host
            return
        if what_os == 1:  # IOS
            child.sendcontrol('c')
            child.expect(PRIV_EXEC_MODE)
            child.sendline(IOSTERMLEN0)
            child.expect(PRIV_EXEC_MODE)
            return child
        if what_os == 2:  # ASAOS
            child.sendline(QOUTMORE)
            child.expect(PRIV_EXEC_MODE)
            child.sendline(ASATERMPAGER0)
            child.expect(PRIV_EXEC_MODE)
            return child

    else:
        print 'Failed to log in to ' + host
