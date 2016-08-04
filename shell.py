#!/usr/bin/env python
#coding=utf-8

###  参考这篇文章
###  https://github.com/supasate/yosh

import sys
import shlex
import os
import builtins as bt

SHELL_STATUS_RUN = 1
SHELL_STATUS_STOP= 0
build_in_commands = {}

def builtin_execute(cmd_name,tokens):
    return build_in_commands[cmd_name](tokens)

def register_command(cmd,callback):
    build_in_commands[cmd] = callback

def init_commands():
    register_command("cd",bt.q_cd)
    register_command("exit",bt.q_exit)

def tokenize(string):
    return shlex.split(string)

def execute(tokens):
    if tokens[0] in build_in_commands:
        return builtin_execute(tokens[0],tokens)
    pid = os.fork()
    if 0 == pid :
        os.execvp(tokens[0],tokens)
    elif pid > 0 :
        while True:
            wpid,status = os.waitpid(pid,0)
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break
    return SHELL_STATUS_RUN

def shell_loop():
    status = SHELL_STATUS_RUN
    while status == SHELL_STATUS_RUN:
        sys.stdout.write(">")
        sys.stdout.flush()
        cmd = sys.stdin.readline()
        cmd_tokens = tokenize(cmd)
        status = execute(cmd_tokens)

if __name__ == "__main__":
    init_commands()
    shell_loop()
