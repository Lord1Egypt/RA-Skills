#!/usr/bin/env python3
"""Touch Tool - Create files."""
import argparse, os, sys
parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
args = parser.parse_args()
for f in args.files:
    try:
        open(f, 'a').close()
        print(f"Created: {f}")
    except Exception as e: print(f"Error: {e}", file=sys.stderr)
