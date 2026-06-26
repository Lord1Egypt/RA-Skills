#!/usr/bin/env python3
"""Tree Tool - Directory tree."""
import argparse, os
parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default='.')
parser.add_argument('-d', '--depth', type=int, default=3)
args = parser.parse_args()

def tree(p, prefix='', depth=0):
    if depth > args.depth: return
    try:
        items = sorted(os.listdir(p))
    except: return
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        print(prefix + ('└── ' if is_last else '├── ') + item)
        if os.path.isdir(os.path.join(p, item)):
            tree(os.path.join(p, item), prefix + ('    ' if is_last else '│   '), depth+1)
tree(args.path)
