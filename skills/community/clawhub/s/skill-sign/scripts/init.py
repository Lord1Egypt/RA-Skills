#!/usr/bin/env python3
"""
init.py — generate Ed25519 keypair for skill-sign.

Usage:
    python3 init.py                  # Interactive; refuses to overwrite existing
    python3 init.py --force          # Overwrite existing keypair (DANGEROUS)
    python3 init.py --seed-from-stdin  # Use 32 bytes from stdin (deterministic)

Output:
    ~/.config/skill-sign/private.key       (32-byte Ed25519 seed, chmod 600)
    ~/.config/skill-sign/public.key        (32-byte Ed25519 pubkey, chmod 644)
    ~/.config/skill-sign/public.key.txt    (base64 short form for copy-paste)

WARNING: If you lose private.key, all signatures become un-revocable.
         Back it up to a safe place (encrypted USB / password manager).
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from _lib import (
    private_key_path, public_key_path, public_key_txt_path,
    write_secret_file, write_public_file,
    ed25519_keygen, encode_pubkey,
)


def main():
    p = argparse.ArgumentParser(description="Generate Ed25519 keypair for skill-sign")
    p.add_argument("--force", action="store_true",
                   help="Overwrite existing private key (irreversible)")
    p.add_argument("--seed-from-stdin", action="store_true",
                   help="Read 32-byte seed from stdin instead of os.urandom (deterministic, for testing)")
    args = p.parse_args()

    priv_p = private_key_path()
    pub_p = public_key_path()
    pub_txt_p = public_key_txt_path()

    if priv_p.exists() and not args.force:
        print(f"❌ Private key already exists at: {priv_p}")
        print()
        print("   If you want to:")
        print(f"     - View current public key:   python3 {os.path.dirname(__file__)}/export_public.py")
        print(f"     - Replace (LOSE all old sigs): python3 {sys.argv[0]} --force")
        print(f"     - Rotate (planned for v1.1): not yet implemented")
        sys.exit(1)

    # Generate seed
    if args.seed_from_stdin:
        seed = sys.stdin.buffer.read(32)
        if len(seed) != 32:
            print(f"❌ stdin must provide exactly 32 bytes (got {len(seed)})", file=sys.stderr)
            sys.exit(1)
    else:
        seed = os.urandom(32)

    priv, pub = ed25519_keygen(seed)

    # Write files
    write_secret_file(priv_p, priv)
    write_public_file(pub_p, pub)

    pub_encoded = encode_pubkey(pub)
    write_public_file(pub_txt_p, (pub_encoded + "\n").encode("utf-8"))

    print(f"✅ Keypair generated.")
    print()
    print(f"   Private key (KEEP SECRET):  {priv_p}  (chmod 600)")
    print(f"   Public key  (binary):       {pub_p}")
    print(f"   Public key  (base64):       {pub_txt_p}")
    print()
    print(f"📋 Public key (copy this to SKILL.md / README / share with verifiers):")
    print()
    print(f"   {pub_encoded}")
    print()
    print(f"🛡️  IMPORTANT:")
    print(f"   1. Back up {priv_p} to a safe place (encrypted USB / password manager).")
    print(f"   2. NEVER commit private.key to git or share it.")
    print(f"   3. If lost, you cannot re-sign with the same identity.")
    print()
    print(f"Next: python3 {os.path.dirname(__file__)}/sign.py <skill-dir>")


if __name__ == "__main__":
    main()
