#!/usr/bin/env python3
"""Sort Tool - Sort lines."""

import argparse
import sys


def sort_lines(lines: list, reverse: bool = False, numeric: bool = False, 
               unique: bool = False, ignore_case: bool = False):
    """Sort lines."""
    if ignore_case:
        lines = [(line.lower(), line) for line in lines]
        lines.sort(key=lambda x: x[0], reverse=reverse)
        lines = [line[1] for line in lines]
    elif numeric:
        try:
            lines.sort(key=lambda x: float(x), reverse=reverse)
        except ValueError:
            lines.sort(reverse=reverse)
    else:
        lines.sort(reverse=reverse)
    
    if unique:
        seen = set()
        result = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                result.append(line)
        lines = result
    
    return lines


def main():
    parser = argparse.ArgumentParser(description='Sort lines')
    parser.add_argument('file', nargs='?', help='File to sort')
    parser.add_argument('-r', '--reverse', action='store_true', help='Reverse sort')
    parser.add_argument('-n', '--numeric', action='store_true', help='Numeric sort')
    parser.add_argument('-u', '--unique', action='store_true', help='Remove duplicates')
    parser.add_argument('-f', '--ignore-case', action='store_true', help='Case insensitive')
    
    args = parser.parse_args()
    
    # Read input
    if args.file:
        try:
            with open(args.file, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        lines = sys.stdin.readlines()
    
    # Strip newlines for processing
    lines = [line.rstrip('\n') for line in lines]
    
    # Sort
    lines = sort_lines(lines, args.reverse, args.numeric, args.unique, args.ignore_case)
    
    # Output
    for line in lines:
        print(line)


if __name__ == '__main__':
    main()
