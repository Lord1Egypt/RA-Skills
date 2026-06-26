#!/usr/bin/env python3
"""Uniq Tool - Unique lines."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='Unique lines')
    parser.add_argument('file', nargs='?', help='Input file')
    parser.add_argument('-c', '--count', action='store_true', help='Show counts')
    
    args = parser.parse_args()
    
    if args.file:
        try:
            lines = open(args.file).readlines()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        lines = sys.stdin.readlines()
    
    lines = [line.rstrip('\n') for line in lines]
    
    if args.count:
        from collections import Counter
        for line, count in Counter(lines).items():
            print(f"{count:4d} {line}")
    else:
        seen = set()
        for line in lines:
            if line not in seen:
                print(line)
                seen.add(line)


if __name__ == '__main__':
    main()
