#!/usr/bin/env python3
"""Tar Tool - TAR archives."""
import argparse, tarfile, sys
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('files', nargs='*')
parser.add_argument('-x', '--extract', action='store_true')
args = parser.parse_args()
if args.extract:
    with tarfile.open(args.file, 'r:*') as t:
        t.extractall()
    print(f"Extracted: {args.file}")
else:
    with tarfile.open(args.file, 'w') as t:
        for f in args.files or []:
            t.add(f)
    print(f"Created: {args.file}")
