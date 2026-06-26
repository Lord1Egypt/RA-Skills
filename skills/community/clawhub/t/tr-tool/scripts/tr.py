#!/usr/bin/env python3
import sys, string
if len(sys.argv)<3: print("Usage: tr.py from to"); sys.exit(1)
trans = str.maketrans(sys.argv[1], sys.argv[2])
print(sys.stdin.read().translate(trans))
