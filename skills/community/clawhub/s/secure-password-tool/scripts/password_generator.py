#!/usr/bin/env python3
"""
Secure Password Generator - Generate cryptographically secure random passwords
Uses secrets module for cryptographic security (not random)
"""
import secrets
import string
import sys
import json
import argparse

def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True, exclude_similar=False):
    """Generate a cryptographically secure random password
    
    Args:
        length: Password length (default 16)
        use_upper: Include uppercase letters (default True)
        use_lower: Include lowercase letters (default True)
        use_digits: Include digits (default True)
        use_special: Include special symbols (default True)
        exclude_similar: Exclude similar characters 0O1lI (default False)
    
    Returns:
        str: Generated password
    """
    chars = ''
    
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    if exclude_similar:
        similar = '0O1lI'
        chars = ''.join(c for c in chars if c not in similar)
    
    if not chars:
        chars = string.ascii_letters + string.digits
    
    # Use secrets.choice for cryptographic security
    return ''.join(secrets.choice(chars) for _ in range(length))

def main():
    parser = argparse.ArgumentParser(
        description='Generate cryptographically secure random passwords',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 password_generator.py
  python3 password_generator.py 20
  python3 password_generator.py 24 10
  python3 password_generator.py 16 --exclude-similar
  python3 password_generator.py 16 --no-special
        """
    )
    
    parser.add_argument('length', type=int, nargs='?', default=16, help='Password length (default: 16)')
    parser.add_argument('count', type=int, nargs='?', default=1, help='Number of passwords (default: 1)')
    parser.add_argument('--no-upper', action='store_true', help='Exclude uppercase letters')
    parser.add_argument('--no-lower', action='store_true', help='Exclude lowercase letters')
    parser.add_argument('--no-digits', action='store_true', help='Exclude digits')
    parser.add_argument('--no-special', action='store_true', help='Exclude special symbols')
    parser.add_argument('--exclude-similar', action='store_true', help='Exclude similar characters (0O1lI)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Generate passwords
    passwords = [
        generate_password(
            args.length,
            use_upper=not args.no_upper,
            use_lower=not args.no_lower,
            use_digits=not args.no_digits,
            use_special=not args.no_special,
            exclude_similar=args.exclude_similar
        )
        for _ in range(args.count)
    ]
    
    result = {
        'count': args.count,
        'length': args.length,
        'passwords': passwords,
        'options': {
            'uppercase': not args.no_upper,
            'lowercase': not args.no_lower,
            'digits': not args.no_digits,
            'special': not args.no_special,
            'exclude_similar': args.exclude_similar
        }
    }
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if args.count == 1:
            print(f"🔐 Generated password ({args.length} chars):")
            print(f"   {passwords[0]}")
        else:
            print(f"🔐 Generated {args.count} passwords ({args.length} chars each):")
            for i, pwd in enumerate(passwords, 1):
                print(f"   {i}. {pwd}")

if __name__ == '__main__':
    main()
