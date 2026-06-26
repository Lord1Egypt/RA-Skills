#!/usr/bin/env python3
import sys
lines = sys.stdin.readlines()
for line in reversed(lines):
    print(line, end='')
