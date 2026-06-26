#!/usr/bin/env python3
"""Unzip Tool - Extract ZIP archives."""
import argparse, zipfile, sys
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-d', '--dir', default='.')
args = parser.parse_args()
try:
    with zipfile.ZipFile(args.file, 'r') as z:
        z.extractall(args.dir)
    print(f"Extracted to: {args.dir}")
except Exception as e: print(f"Error: {e}", file=sys.stderr)
