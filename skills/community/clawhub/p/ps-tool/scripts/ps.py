#!/usr/bin/env python3
"""Ps Tool - List processes."""
import os, sys
for p in os.listdir('/proc'):
    if p.isdigit():
        try:
            with open(f'/proc/{p}/cmdline', 'r') as f:
                cmd = f.read().replace('\x00', ' ').strip() or '[kernel]'
            print(f"{p:6} {cmd[:60]}")
        except: pass
