#!/usr/bin/env python3
import urllib.request, sys, os
url, output = None, None
for i, a in enumerate(sys.argv[1:]):
    if a == '-O': output = sys.argv[i+3]
    elif not a.startswith('-'): url = a
if not url: print("Usage: wget.py <url> [-O output]"); sys.exit(1)
urllib.request.urlretrieve(url, output or os.path.basename(url))
print("Downloaded")
