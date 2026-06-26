#!/usr/bin/env python3
import sys
start, end, step = 1, int(sys.argv[1]), 1
if len(sys.argv)>2: start, end = int(sys.argv[1]), int(sys.argv[2])
if len(sys.argv)>3: step = int(sys.argv[3])
for i in range(start, end+1, step): print(i)
