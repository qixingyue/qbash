import os

def q_cd(tokens):
    os.chdir(tokens[1])
    return 1

