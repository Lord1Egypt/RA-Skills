#!/usr/bin/env python3
import hashlib, sys
data = open(sys.argv[1], 'rb').read() if sys.argv[1:] else sys.stdin.buffer.read()
print(hashlib.sha256(data).hexdigest())
