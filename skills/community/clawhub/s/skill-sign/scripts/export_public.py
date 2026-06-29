#!/usr/bin/env python3
"""
export_public.py — print your public key (for sharing with verifiers).

Usage:
    python3 export_public.py              # print short-form ed25519:<base64>
    python3 export_public.py --raw        # print binary public.key to stdout
    python3 export_public.py --skill-md   # print as a SKILL.md / README line
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from _lib import public_key_path, public_key_txt_path, encode_pubkey


def main():
    ap = argparse.ArgumentParser(description="Print your skill-sign public key")
    ap.add_argument("--raw", action="store_true", help="Print raw 32-byte binary to stdout")
    ap.add_argument("--skill-md", action="store_true",
                    help="Print as a SKILL.md / README markdown line")
    args = ap.parse_args()

    pub_p = public_key_path()
    if not pub_p.exists():
        print(f"❌ No public key at: {pub_p}", file=sys.stderr)
        print(f"   Run: python3 {os.path.dirname(__file__)}/init.py", file=sys.stderr)
        sys.exit(1)

    pub = pub_p.read_bytes()
    if len(pub) != 32:
        print(f"❌ Public key is corrupt ({len(pub)} bytes, expected 32)", file=sys.stderr)
        sys.exit(2)

    encoded = encode_pubkey(pub)

    if args.raw:
        sys.stdout.buffer.write(pub)
        return

    if args.skill_md:
        print(f"- **Signing Public Key**: `{encoded}`")
        print(f"  (Verify any skill with: `python3 verify.py <skill-dir> --trust-key-string {encoded}`)")
        return

    # Default: just the short form
    print(encoded)


if __name__ == "__main__":
    main()
