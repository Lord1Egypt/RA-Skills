#!/usr/bin/env python3
import hashlib, sys
h = hashlib.sha256()
h.update(open(sys.argv[1] if len(sys.argv) > 1 else "a.txt", "rb").read())
print(h.hexdigest())
