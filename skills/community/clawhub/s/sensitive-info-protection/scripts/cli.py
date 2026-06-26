#!/usr/bin/env python3
import argparse
import sys
from detector import SensitiveDetector


def main():
    parser = argparse.ArgumentParser(description='Sensitive Information Detection CLI')
    parser.add_argument('input', nargs='?', help='Input text or file to scan (use - for stdin)')
    parser.add_argument('--config', '-c', help='Path to custom rules configuration file')
    parser.add_argument('--desensitize', '-d', action='store_true', help='Output desensitized text')
    parser.add_argument('--replacement', '-r', default='***', help='Replacement text for desensitization')

    args = parser.parse_args()

    # Initialize detector
    detector = SensitiveDetector()

    # Load custom config if provided
    if args.config:
        detector.load_config(args.config)

    # Get input content
    if not args.input:
        print("No input provided. Reading from stdin...")
        content = sys.stdin.read()
    elif args.input == '-':
        content = sys.stdin.read()
    else:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            content = args.input

    # Scan
    result = detector.scan(content)

    if args.desensitize:
        if result.has_sensitive:
            desensitized = detector.desensitize(content, args.replacement)
            print(desensitized)
        else:
            print(content)
    else:
        print(result.to_markdown())

    if result.has_sensitive and not args.desensitize:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
