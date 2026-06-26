#!/usr/bin/env python3
import sys
print(''.join(reversed(open(sys.argv[1] if len(sys.argv)>1 else sys.stdin.read()).readlines())), end='')
