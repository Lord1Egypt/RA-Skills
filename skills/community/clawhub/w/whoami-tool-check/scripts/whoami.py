#!/usr/bin/env python3
import os, pwd
try: print(pwd.getpwuid(os.getuid())[0])
except: print(os.getenv('USER', 'unknown'))
