#!/usr/bin/env python3
import re, sys
pattern = sys.argv[1] if len(sys.argv) > 1 else ''
text = sys.stdin.read()
if pattern.startswith('s/'):
    parts = pattern[2:].split('/')
    if len(parts) >= 2:
        text = re.sub(parts[0], parts[1], text)
print(text, end='')
