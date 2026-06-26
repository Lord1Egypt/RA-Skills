#!/usr/bin/env python3
"""Zip Tool - Create ZIP archives."""
import argparse, zipfile, sys
parser = argparse.ArgumentParser()
parser.add_argument('output')
parser.add_argument('files', nargs='+')
args = parser.parse_args()
try:
    with zipfile.ZipFile(args.output, 'w') as z:
        for f in args.files:
            z.write(f, arcname=f)
    print(f"Created: {args.output}")
except Exception as e: print(f"Error: {e}", file=sys.stderr)
