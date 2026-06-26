#!/usr/bin/env python3
"""UUID Tool - Generate UUIDs."""

import argparse
import uuid as uuid_module
import sys


def generate_uuid(version: int = 4, count: int = 1, upper: bool = False, no_dashes: bool = False,
                  namespace: str = None, name: str = None) -> list:
    """Generate UUIDs."""
    results = []
    
    namespaces = {
        'default': uuid_module.NAMESPACE_DNS,
        'url': uuid_module.NAMESPACE_URL,
        'oid': uuid_module.NAMESPACE_OID,
        'x500': uuid_module.NAMESPACE_X500
    }
    
    for i in range(count):
        if version == 1:
            u = uuid_module.uuid1()
        elif version == 4:
            u = uuid_module.uuid4()
        elif version == 5:
            if not name:
                print("Error: --name is required for UUID v5", file=sys.stderr)
                return []
            ns = namespaces.get(namespace, uuid_module.NAMESPACE_DNS)
            u = uuid_module.uuid5(ns, name)
        else:
            print(f"Error: Unsupported UUID version: {version}", file=sys.stderr)
            return []
        
        result = str(u)
        
        if upper:
            result = result.upper()
        if no_dashes:
            result = result.replace('-', '')
        
        results.append(result)
    
    return results


def main():
    parser = argparse.ArgumentParser(description='UUID generation tool')
    
    parser.add_argument('--count', '-n', type=int, default=1, help='Number of UUIDs to generate')
    parser.add_argument('--version', type=int, choices=[1, 4, 5], default=4, help='UUID version')
    parser.add_argument('--namespace', default='default', 
                       choices=['default', 'url', 'oid', 'x500'],
                       help='Namespace for v5 UUID')
    parser.add_argument('--name', help='Name for v5 UUID')
    parser.add_argument('--upper', '-u', action='store_true', help='Output in uppercase')
    parser.add_argument('--no-dashes', action='store_true', help='Output without dashes')
    
    args = parser.parse_args()
    
    # Validate v5 requirements
    if args.version == 5 and not args.name:
        print("Error: --name is required for UUID v5", file=sys.stderr)
        sys.exit(1)
    
    results = generate_uuid(
        version=args.version,
        count=args.count,
        upper=args.upper,
        no_dashes=args.no_dashes,
        namespace=args.namespace,
        name=args.name
    )
    
    for result in results:
        print(result)


if __name__ == '__main__':
    main()
