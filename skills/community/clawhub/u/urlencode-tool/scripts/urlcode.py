#!/usr/bin/env python3
"""URL Encode Tool - URL encode/decode."""

import argparse
import sys
from urllib.parse import quote, unquote, quote_plus, unquote_plus


def main():
    parser = argparse.ArgumentParser(description='URL encode/decode')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--encode', '-e', help='Encode URL')
    group.add_argument('--decode', '-d', help='Decode URL')
    parser.add_argument('--component', action='store_true', help='Encode as component')
    parser.add_argument('--plus', '-p', action='store_true', help='Use plus for spaces')
    
    args = parser.parse_args()
    
    try:
        if args.encode:
            if args.component:
                result = quote(args.encode, safe='')
            elif args.plus:
                result = quote_plus(args.encode)
            else:
                result = quote(args.encode)
            print(result)
        elif args.decode:
            if args.plus:
                result = unquote_plus(args.decode)
            else:
                result = unquote(args.decode)
            print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
