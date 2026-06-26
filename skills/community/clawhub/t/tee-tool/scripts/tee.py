#!/usr/bin/env python3
import sys
text=sys.stdin.read()
with open(sys.argv[1] if len(sys.argv)>1 else 'out.txt','w') as f: f.write(text)
print(text, end='')
