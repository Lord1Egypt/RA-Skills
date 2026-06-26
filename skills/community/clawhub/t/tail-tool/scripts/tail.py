#!/usr/bin/env python3
"""Tail Tool - Last N lines."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='Last N lines')
    parser.add_argument('file', nargs='?', help='Input file')
    parser.add_argument('-n', '--lines', type=int, default=10, help='Number of lines')
    
    args = parser.parse_args()
    
    if args.file:
        try:
            lines = open(args.file).readlines()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        lines = sys.stdin.readlines()
    
    for line in lines[-args.lines:]:
        print(line.rstrip())


if __name__ == '__main__':
    main()
