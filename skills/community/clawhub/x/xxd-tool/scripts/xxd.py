#!/usr/bin/env python3
import sys
data = open(sys.argv[1],'rb').read() if len(sys.argv)>1 else sys.stdin.buffer.read()
for i in range(0,len(data),16):
    hexed=' '.join(f'{b:02x}' for b in data[i:i+16])
    ascii_=''.join(chr(b) if 32<=b<127 else '.' for b in data[i:i+16])
    print(f'{i:08x}  {hexed:<48}  |{ascii_}|')
