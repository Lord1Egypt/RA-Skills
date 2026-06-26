#!/usr/bin/env python3
"""Top Tool - System monitor."""
import os, time
print("PID    CMD                      MEM%   CPU%")
for p in os.listdir('/proc'):
    if p.isdigit():
        try:
            with open(f'/proc/{p}/stat', 'r') as f:
                stat = f.read().split()
                with open(f'/proc/{p}/cmdline', 'r') as f:
                    cmd = f.read().replace('\x00', ' ').strip()[:20] or '[kernel]'
            print(f"{p:6} {cmd:24}")
        except: pass
