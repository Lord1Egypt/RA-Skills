#!/usr/bin/env python3
import sys
print(open(sys.argv[1] if len(sys.argv)>1 else sys.stdin.read()).read().replace('        ', '\t'))
