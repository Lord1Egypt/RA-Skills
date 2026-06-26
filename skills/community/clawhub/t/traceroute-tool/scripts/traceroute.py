#!/usr/bin/env python3
"""Traceroute Tool - Trace route."""
import subprocess, sys
host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
subprocess.run(['traceroute', host])
