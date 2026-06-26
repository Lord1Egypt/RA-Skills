#!/usr/bin/env python3
import random, sys
lines=open(sys.argv[1] if len(sys.argv)>1 else sys.stdin.read()).readlines()
random.shuffle(lines)
print(''.join(lines), end='')
