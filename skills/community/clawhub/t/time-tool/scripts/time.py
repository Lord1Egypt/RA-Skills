#!/usr/bin/env python3
import time, subprocess, sys
if len(sys.argv) < 2: print("Usage: time.py <cmd>"); sys.exit(1)
start = time.time()
subprocess.run(sys.argv[1:])
print(f"Time: {time.time()-start:.2f}s")
