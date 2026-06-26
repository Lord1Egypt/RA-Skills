#!/usr/bin/env python3
"""
UUID Toolkit - Generate, validate, and parse UUIDs
Supports: v1 (time-based), v4 (random), v5 (namespace-based)
"""
import uuid
import argparse
import sys

def generate_uuid_v1():
    """Generate UUID v1 (time-based)"""
    return str(uuid.uuid1())

def generate_uuid_v4():
    """Generate UUID v4 (random)"""
    return str(uuid.uuid4())

def generate_uuid_v5(namespace, name):
    """Generate UUID v5 (namespace-based)"""
    # Default to DNS namespace if not specified
    ns = uuid.NAMESPACE_DNS
    if namespace == 'url':
        ns = uuid.NAMESPACE_URL
    elif namespace == 'oid':
        ns = uuid.NAMESPACE_OID
    elif namespace == 'x500':
        ns = uuid.NAMESPACE_X500
    return str(uuid.uuid5(ns, name))

def validate_uuid(uuid_str):
    """Validate UUID format"""
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False

def parse_uuid(uuid_str):
    """Parse UUID and return components"""
    try:
        u = uuid.UUID(uuid_str)
        return {
            'valid': True,
            'version': u.version,
            'variant': str(u.variant),
            'hex': u.hex,
            'bytes': u.bytes.hex(),
            'int': u.int,
            'urn': u.urn
        }
    except ValueError:
        return {'valid': False}

def main():
    parser = argparse.ArgumentParser(
        description='UUID Toolkit - Generate, validate, and parse UUIDs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 uuid_toolkit.py
  python3 uuid_toolkit.py --v1
  python3 uuid_toolkit.py --count 10
  python3 uuid_toolkit.py --validate "550e8400-e29b-41d4-a716-446655440000"
        """
    )
    
    parser.add_argument('--v1', action='store_true', help='Generate UUID v1 (time-based)')
    parser.add_argument('--v4', action='store_true', help='Generate UUID v4 (random, default)')
    parser.add_argument('--v5', nargs=2, metavar=('NAMESPACE', 'NAME'), help='Generate UUID v5')
    parser.add_argument('--count', type=int, default=1, help='Number of UUIDs to generate')
    parser.add_argument('--validate', metavar='UUID', help='Validate UUID format')
    parser.add_argument('--parse', metavar='UUID', help='Parse UUID components')
    parser.add_argument('--no-hyphens', action='store_true', help='Output without hyphens')
    parser.add_argument('--upper', action='store_true', help='Output uppercase')
    
    args = parser.parse_args()
    
    # Validate mode
    if args.validate:
        is_valid = validate_uuid(args.validate)
        if is_valid:
            print(f"✅ Valid UUID: {args.validate}")
        else:
            print(f"❌ Invalid UUID: {args.validate}")
        return
    
    # Parse mode
    if args.parse:
        result = parse_uuid(args.parse)
        if result['valid']:
            print(f"✅ UUID: {args.parse}")
            print(f"   Version: {result['version']}")
            print(f"   Hex: {result['hex']}")
            print(f"   URN: {result['urn']}")
        else:
            print(f"❌ Invalid UUID: {args.parse}")
        return
    
    # UUID v5 mode
    if args.v5:
        namespace, name = args.v5
        result = generate_uuid_v5(namespace, name)
        if args.no_hyphens:
            result = result.replace('-', '')
        if args.upper:
            result = result.upper()
        print(result)
        return
    
    # Generate UUIDs
    generate_func = generate_uuid_v1 if args.v1 else generate_uuid_v4
    
    for _ in range(args.count):
        u = generate_func()
        if args.no_hyphens:
            u = u.replace('-', '')
        if args.upper:
            u = u.upper()
        print(u)

if __name__ == '__main__':
    main()
