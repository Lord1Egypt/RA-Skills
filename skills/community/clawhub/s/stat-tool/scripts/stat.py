#!/usr/bin/env python3
import os, sys, datetime
path = sys.argv[1] if sys.argv[1:] else '.'
st = os.stat(path)
print(f"Size: {st.st_size}")
print(f"Modified: {datetime.datetime.fromtimestamp(st.st_mtime)}")
print(f"Mode: {oct(st.st_mode)}")
