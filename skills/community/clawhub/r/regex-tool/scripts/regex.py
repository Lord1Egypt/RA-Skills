#!/usr/bin/env python3
"""Regex Tool - Test regular expressions."""

import argparse
import re
import sys


def test_regex(pattern: str, text: str, find_all: bool = False, 
               replace: str = None, ignore_case: bool = False, 
               multiline: bool = False, verbose: bool = False):
    """Test regex pattern."""
    flags = 0
    if ignore_case:
        flags |= re.IGNORECASE
    if multiline:
        flags |= re.MULTILINE
    
    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        print(f"Invalid pattern: {e}", file=sys.stderr)
        return False
    
    if replace:
        # Replacement mode
        if find_all:
            result = regex.sub(replace, text)
        else:
            result = regex.sub(replace, text, count=1)
        print(result)
    elif find_all:
        # Find all matches
        matches = regex.findall(text)
        if verbose:
            for i, match in enumerate(matches):
                print(f"{i+1}: {match}")
        else:
            for match in matches:
                print(match)
    else:
        # Single match
        match = regex.search(text)
        if match:
            print(f"Match found: {match.group()}")
            if match.groups():
                print(f"Groups: {match.groups()}")
            if match.span():
                print(f"Position: {match.span()}")
        else:
            print("No match")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Regex testing tool')
    parser.add_argument('pattern', help='Regex pattern')
    parser.add_argument('text', nargs='?', help='Text to match')
    parser.add_argument('-g', '--find-all', action='store_true', help='Find all matches')
    parser.add_argument('-r', '--replace', help='Replacement pattern')
    parser.add_argument('-i', '--ignore-case', action='store_true', help='Case insensitive')
    parser.add_argument('-m', '--multiline', action='store_true', help='Multiline mode')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if not args.text:
        # Interactive mode
        print(f"Pattern: {args.pattern}")
        print("Enter text to test (Ctrl+D to exit):")
        text = sys.stdin.read()
        test_regex(args.pattern, text, args.find_all, args.replace, 
                  args.ignore_case, args.multiline, args.verbose)
    else:
        test_regex(args.pattern, args.text, args.find_all, args.replace,
                  args.ignore_case, args.multiline, args.verbose)


if __name__ == '__main__':
    main()
