#!/usr/bin/env python3
"""UUID/ULID/NanoID toolkit: generate, parse, validate, and convert identifiers.

No external dependencies — uses Python's built-in uuid module plus custom implementations.
"""

import argparse
import os
import sys
import time
import uuid
import base64
import struct
import string
import secrets


# --- ULID implementation (no external deps) ---

ULID_ENCODING = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"  # Crockford's Base32
ULID_DECODE = {c: i for i, c in enumerate(ULID_ENCODING)}


def ulid_generate():
    """Generate a ULID (Universally Unique Lexicographically Sortable Identifier)."""
    timestamp_ms = int(time.time() * 1000)
    # 6 bytes timestamp (48 bits)
    ts_bytes = struct.pack(">Q", timestamp_ms)[2:]  # take last 6 bytes
    # 10 bytes randomness (80 bits)
    rand_bytes = os.urandom(10)
    ulid_bytes = ts_bytes + rand_bytes

    # Encode to Crockford's Base32 (26 chars)
    result = []
    # Process as a 128-bit integer
    n = int.from_bytes(ulid_bytes, "big")
    for _ in range(26):
        result.append(ULID_ENCODING[n & 0x1F])
        n >>= 5
    return "".join(reversed(result))


def ulid_parse(ulid_str):
    """Parse a ULID string and extract timestamp."""
    ulid_str = ulid_str.upper()
    if len(ulid_str) != 26:
        return None
    try:
        n = 0
        for c in ulid_str:
            n = (n << 5) | ULID_DECODE[c]
    except KeyError:
        return None
    # Extract timestamp (top 48 bits)
    ts_ms = n >> 80
    ts = ts_ms / 1000.0
    from datetime import datetime, timezone
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return {
        "type": "ULID",
        "value": ulid_str,
        "timestamp_ms": ts_ms,
        "timestamp": dt.isoformat(),
        "random_bits": 80,
    }


# --- NanoID implementation ---

NANOID_ALPHABET = string.ascii_letters + string.digits + "_-"


def nanoid_generate(size=21, alphabet=None):
    """Generate a NanoID."""
    alpha = alphabet or NANOID_ALPHABET
    return "".join(secrets.choice(alpha) for _ in range(size))


# --- UUID helpers ---

def uuid_parse(value):
    """Parse a UUID string and return info."""
    try:
        u = uuid.UUID(value)
    except ValueError:
        return None
    info = {
        "type": "UUID",
        "value": str(u),
        "version": u.version,
        "variant": str(u.variant),
        "hex": u.hex,
        "int": u.int,
        "urn": u.urn,
        "bytes_le": u.bytes_le.hex(),
    }
    if u.version == 1:
        # Extract timestamp
        ts = (u.time - 0x01B21DD213814000) / 1e7
        from datetime import datetime, timezone
        try:
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            info["timestamp"] = dt.isoformat()
        except (OSError, OverflowError):
            info["timestamp"] = "out of range"
        info["clock_seq"] = u.clock_seq
        info["node"] = format(u.node, "012x")
        info["node_mac"] = ":".join(format(u.node, "012x")[i:i+2] for i in range(0, 12, 2))
    return info


def cmd_generate(args):
    """Generate identifiers."""
    id_type = args.type.lower()
    count = args.count or 1
    results = []

    for _ in range(count):
        if id_type == "uuid4" or id_type == "v4":
            results.append(str(uuid.uuid4()))
        elif id_type == "uuid1" or id_type == "v1":
            results.append(str(uuid.uuid1()))
        elif id_type in ("uuid3", "v3"):
            if not args.name:
                print("--name required for UUID v3/v5", file=sys.stderr)
                return 1
            ns = uuid.NAMESPACE_DNS
            if args.namespace:
                ns_map = {"dns": uuid.NAMESPACE_DNS, "url": uuid.NAMESPACE_URL,
                          "oid": uuid.NAMESPACE_OID, "x500": uuid.NAMESPACE_X500}
                ns = ns_map.get(args.namespace.lower(), uuid.NAMESPACE_DNS)
            results.append(str(uuid.uuid3(ns, args.name)))
        elif id_type in ("uuid5", "v5"):
            if not args.name:
                print("--name required for UUID v3/v5", file=sys.stderr)
                return 1
            ns = uuid.NAMESPACE_DNS
            if args.namespace:
                ns_map = {"dns": uuid.NAMESPACE_DNS, "url": uuid.NAMESPACE_URL,
                          "oid": uuid.NAMESPACE_OID, "x500": uuid.NAMESPACE_X500}
                ns = ns_map.get(args.namespace.lower(), uuid.NAMESPACE_DNS)
            results.append(str(uuid.uuid5(ns, args.name)))
        elif id_type == "ulid":
            results.append(ulid_generate())
        elif id_type == "nanoid":
            size = args.size or 21
            results.append(nanoid_generate(size=size))
        elif id_type == "nil":
            results.append(str(uuid.UUID(int=0)))
        else:
            print(f"Unknown type: '{id_type}'. Options: uuid4, uuid1, uuid3, uuid5, ulid, nanoid, nil", file=sys.stderr)
            return 1

    if args.upper:
        results = [r.upper() for r in results]

    for r in results:
        print(r)
    return 0


def cmd_parse(args):
    """Parse and display info about an identifier."""
    value = args.value.strip()

    # Try UUID
    info = uuid_parse(value)
    if info:
        print(f"Type:     UUID v{info['version']}")
        print(f"Value:    {info['value']}")
        print(f"Version:  {info['version']}")
        print(f"Variant:  {info['variant']}")
        print(f"Hex:      {info['hex']}")
        print(f"Integer:  {info['int']}")
        print(f"URN:      {info['urn']}")
        if "timestamp" in info:
            print(f"Time:     {info['timestamp']}")
            print(f"Clock:    {info['clock_seq']}")
            print(f"Node:     {info['node_mac']}")
        return 0

    # Try ULID
    info = ulid_parse(value)
    if info:
        print(f"Type:     ULID")
        print(f"Value:    {info['value']}")
        print(f"Time:     {info['timestamp']}")
        print(f"Time ms:  {info['timestamp_ms']}")
        print(f"Random:   {info['random_bits']} bits")
        return 0

    print(f"Cannot parse: '{value}'. Not a valid UUID or ULID.", file=sys.stderr)
    return 1


def cmd_validate(args):
    """Validate one or more identifiers."""
    values = args.values
    all_valid = True
    for v in values:
        v = v.strip()
        is_uuid = uuid_parse(v) is not None
        is_ulid = ulid_parse(v) is not None
        if is_uuid:
            u = uuid.UUID(v)
            print(f"✓ {v}  (UUID v{u.version})")
        elif is_ulid:
            print(f"✓ {v}  (ULID)")
        else:
            print(f"✗ {v}  (invalid)")
            all_valid = False
    return 0 if all_valid else 1


def cmd_convert(args):
    """Convert UUID between formats."""
    value = args.value.strip()
    try:
        u = uuid.UUID(value)
    except ValueError:
        print(f"Invalid UUID: '{value}'", file=sys.stderr)
        return 1

    print(f"Standard:   {str(u)}")
    print(f"Upper:      {str(u).upper()}")
    print(f"No dashes:  {u.hex}")
    print(f"URN:        {u.urn}")
    print(f"Integer:    {u.int}")
    print(f"Base64:     {base64.b64encode(u.bytes).decode()}")
    print(f"Bytes (LE): {u.bytes_le.hex()}")
    print(f"Braces:     {{{str(u)}}}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="UUID/ULID/NanoID toolkit: generate, parse, validate, convert",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s generate uuid4                     # Generate UUIDv4
  %(prog)s generate uuid4 --count 10          # Generate 10 UUIDv4s
  %(prog)s generate ulid                      # Generate ULID
  %(prog)s generate nanoid --size 16          # 16-char NanoID
  %(prog)s generate uuid5 --name example.com  # Deterministic UUID
  %(prog)s parse 550e8400-e29b-41d4-a716-446655440000
  %(prog)s validate 550e8400-e29b-41d4-a716-446655440000 invalid-id
  %(prog)s convert 550e8400-e29b-41d4-a716-446655440000
""",
    )

    sub = parser.add_subparsers(dest="command", help="Command to run")

    # generate
    p_gen = sub.add_parser("generate", help="Generate identifiers")
    p_gen.add_argument("type", help="Type: uuid4, uuid1, uuid3, uuid5, ulid, nanoid, nil")
    p_gen.add_argument("--count", "-c", type=int, help="Number to generate (default: 1)")
    p_gen.add_argument("--name", "-n", help="Name for UUID v3/v5")
    p_gen.add_argument("--namespace", help="Namespace for UUID v3/v5 (dns, url, oid, x500)")
    p_gen.add_argument("--size", "-s", type=int, help="Size for NanoID (default: 21)")
    p_gen.add_argument("--upper", "-u", action="store_true", help="Output in uppercase")

    # parse
    p_parse = sub.add_parser("parse", help="Parse and display info about an identifier")
    p_parse.add_argument("value", help="UUID or ULID to parse")

    # validate
    p_val = sub.add_parser("validate", help="Validate identifiers")
    p_val.add_argument("values", nargs="+", help="Values to validate")

    # convert
    p_conv = sub.add_parser("convert", help="Convert UUID between formats")
    p_conv.add_argument("value", help="UUID to convert")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    cmds = {
        "generate": cmd_generate,
        "parse": cmd_parse,
        "validate": cmd_validate,
        "convert": cmd_convert,
    }
    return cmds[args.command](args)


if __name__ == "__main__":
    sys.exit(main() or 0)
