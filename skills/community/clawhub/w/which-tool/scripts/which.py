#!/usr/bin/env python3
"""Which Tool - Find command."""
import argparse, shutil, sys
parser = argparse.ArgumentParser()
parser.add_argument('cmd')
args = parser.parse_args()
path = shutil.which(args.cmd)
print(path if path else f"Command not found: {args.cmd}")
