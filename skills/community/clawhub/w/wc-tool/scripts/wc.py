#!/usr/bin/env python3
"""WC Tool - Word count."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='Word count')
    parser.add_argument('file', nargs='?', help='Input file')
    parser.add_argument('-l', '--lines', action='store_true', help='Count lines')
    parser.add_argument('-w', '--words', action='store_true', help='Count words')
    parser.add_argument('-c', '--chars', action='store_true', help='Count chars')
    
    args = parser.parse_args()
    
    if args.file:
        try:
            content = open(args.file).read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        content = sys.stdin.read()
    
    lines = content.count('\n')
    if not content.endswith('\n'):
        lines += 1
    words = len(content.split())
    chars = len(content)
    
    show_all = not (args.lines or args.words or args.chars)
    
    if show_all or args.lines:
        print(f"{lines:8}", end='')
    if show_all or args.words:
        print(f"{words:8}", end='')
    if show_all or args.chars:
        print(f"{chars:8}", end='')
    
    if args.file:
        print(f" {args.file}")
    else:
        print()


if __name__ == '__main__':
    main()
