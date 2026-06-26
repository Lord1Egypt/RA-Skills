#!/usr/bin/env python3
import sys, subprocess
lines = sys.stdin.read().strip().split('\n')
cmd = sys.argv[1:]
for line in lines:
    subprocess.run([c.replace('{}', line) for c in cmd])
