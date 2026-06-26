#!/usr/bin/env python3
"""SCP Tool - Secure copy."""
import argparse, subprocess
parser = argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('dst')
args = parser.parse_args()
subprocess.run(['scp', args.src, args.dst])
