#!/usr/bin/env python3
"""Random Tool - Generate random data."""

import argparse
import random
import string
import sys
import uuid


def random_int(min_val: int, max_val: int) -> int:
    """Generate random integer."""
    return random.randint(min_val, max_val)


def random_float(min_val: float, max_val: float) -> float:
    """Generate random float."""
    return random.uniform(min_val, max_val)


def random_string(length: int, charset: str = None) -> str:
    """Generate random string."""
    if charset is None:
        charset = string.ascii_letters + string.digits
    return ''.join(random.choice(charset) for _ in range(length))


def random_password(length: int) -> str:
    """Generate secure password."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    return ''.join(random.choice(chars) for _ in range(length))


def pick_choice(choices: list) -> str:
    """Pick random from choices."""
    return random.choice(choices)


def shuffle_lines(text: str) -> str:
    """Shuffle lines."""
    lines = text.strip().split('\n')
    random.shuffle(lines)
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Random data generator')
    parser.add_argument('--int', '-i', nargs=2, type=int, metavar=('MIN', 'MAX'), help='Random integer')
    parser.add_argument('--float', nargs=2, type=float, metavar=('MIN', 'MAX'), help='Random float')
    parser.add_argument('--string', '-s', type=int, help='Random string length')
    parser.add_argument('--choice', '-c', nargs='+', help='Pick random from choices')
    parser.add_argument('--shuffle', action='store_true', help='Shuffle lines')
    parser.add_argument('--password', type=int, metavar='LENGTH', help='Generate password')
    parser.add_argument('--uuid', action='store_true', help='Generate UUID')
    
    args = parser.parse_args()
    
    # Check stdin for shuffle
    if args.shuffle:
        text = sys.stdin.read()
        print(shuffle_lines(text))
        return
    
    if args.int:
        print(random_int(args.int[0], args.int[1]))
    elif args.float:
        print(round(random_float(args.float[0], args.float[1]), 6))
    elif args.string:
        print(random_string(args.string))
    elif args.password:
        print(random_password(args.password))
    elif args.uuid:
        print(uuid.uuid4())
    elif args.choice:
        print(pick_choice(args.choice))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
