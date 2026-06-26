#!/usr/bin/env python3
"""Rm Tool - Remove files."""
import argparse, os, shutil, sys
parser = argparse.ArgumentParser()
parser.add_argument('paths', nargs='+')
parser.add_argument('--recursive', '-r', action='store_true')
parser.add_argument('--force', '-f', action='store_true')
args = parser.parse_args()
for p in args.paths:
    try:
        if os.path.isdir(p) and args.recursive:
            shutil.rmtree(p)
        elif os.path.isfile(p):
            os.remove(p)
        else:
            os.remove(p) if args.force else print(f"Use -r for dirs: {p}", file=sys.stderr)
        print(f"Removed: {p}")
    except Exception as e: print(f"Error: {e}", file=sys.stderr)
