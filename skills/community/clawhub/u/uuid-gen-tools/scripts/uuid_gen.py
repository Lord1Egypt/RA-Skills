#!/usr/bin/env python3
"""UUID Generator - Generate UUID v1, v4, v5 in various formats"""
import uuid, sys

def generate_v4(count=1, fmt='standard'):
    uuids = [uuid.uuid4() for _ in range(count)]
    return format_uuids(uuids, fmt)

def generate_v1(count=1, fmt='standard'):
    uuids = [uuid.uuid1() for _ in range(count)]
    return format_uuids(uuids, fmt)

def generate_v5(namespace, name, count=1, fmt='standard'):
    ns_map = {'url': uuid.UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8'),
              'dns': uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8'),
              'oid': uuid.UUID('6ba7b812-9dad-11d1-80b4-00c04fd430c8'),
              'x500': uuid.UUID('6ba7b814-9dad-11d1-80b4-00c04fd430c8')}
    ns = ns_map.get(namespace.lower(), uuid.UUID(namespace))
    uuids = [uuid.uuid5(ns, name) for _ in range(count)]
    return format_uuids(uuids, fmt)

def format_uuids(uuids, fmt):
    results = []
    for u in uuids:
        s = str(u)
        if fmt == 'uppercase':
            s = s.upper()
        elif fmt == 'nodashes':
            s = s.replace('-', '')
        elif fmt == 'urlsafe':
            s = u.urlsafe().decode() if hasattr(u, 'urlsafe') else s.replace('-', '')
        results.append(s)
    return '\n'.join(results)

def main():
    args = sys.argv[1:]
    version = 'v4'
    count = 1
    fmt = 'standard'
    namespace = None
    name = None
    
    i = 0
    while i < len(args):
        if args[i] == 'v1' or args[i] == 'v4' or args[i] == 'v5':
            version = args[i]
        elif args[i] == '--count' and i + 1 < len(args):
            count = int(args[i+1]); i += 1
        elif args[i] == '--format' and i + 1 < len(args):
            fmt = args[i+1]; i += 1
        elif args[i] == 'ns:url' or args[i] == 'ns:dns' or args[i].startswith('ns:'):
            namespace = args[i][3:]
        elif i > 0 and args[i-1].startswith('ns:'):
            name = args[i]
        i += 1
    
    # Find name in args
    for arg in args:
        if not arg.startswith('-') and not arg.startswith('v') and arg not in ['url', 'dns', 'oid', 'x500']:
            if namespace and not name:
                name = arg
    
    try:
        if version == 'v4':
            print(generate_v4(count, fmt))
        elif version == 'v1':
            print(generate_v1(count, fmt))
        elif version == 'v5':
            if not namespace or not name:
                print("UUID v5 requires namespace and name", file=sys.stderr)
                sys.exit(1)
            print(generate_v5(namespace, name, count, fmt))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
