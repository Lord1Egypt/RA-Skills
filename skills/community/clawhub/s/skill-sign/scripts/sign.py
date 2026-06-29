#!/usr/bin/env python3
"""
sign.py — sign a skill directory with your Ed25519 private key.

Usage:
    python3 sign.py <skill-dir> [--version X.Y.Z] [--signed-by NAME]

Reads private key from: ~/.config/skill-sign/private.key
Writes signature to:    <skill-dir>/sign.key

Re-running on an already-signed skill UPDATES the signature (same author only).
"""

import os
import sys
import json
import argparse
import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _lib import (
    private_key_path, public_key_path,
    check_private_key_permissions,
    collect_files, compute_content_hash,
    ed25519_keygen, ed25519_sign,
    encode_pubkey, encode_signature,
    read_sign_key, write_sign_key,
)


def load_keypair():
    """Load private seed + derive public key. Exits if private.key missing."""
    priv_p = private_key_path()
    if not priv_p.exists():
        print(f"❌ No private key found at: {priv_p}")
        print(f"   Run: python3 {os.path.dirname(__file__)}/init.py")
        sys.exit(1)

    warn = check_private_key_permissions(priv_p)
    if warn:
        print(warn, file=sys.stderr)

    with open(priv_p, "rb") as f:
        seed = f.read()
    if len(seed) != 32:
        print(f"❌ Private key at {priv_p} is corrupt (got {len(seed)} bytes, expected 32).",
              file=sys.stderr)
        sys.exit(2)

    priv, pub = ed25519_keygen(seed)
    return priv, pub


def canonical_signed_payload(skill_name: str, version: str, signed_by: str,
                             signed_at: str, algorithm: str, public_key_str: str,
                             content_hash: str) -> bytes:
    """
    The exact bytes that get signed. Use sorted JSON for stability across
    Python versions / re-signs.
    """
    payload = {
        "algorithm": algorithm,
        "content_hash": content_hash,
        "public_key": public_key_str,
        "signed_at": signed_at,
        "signed_by": signed_by,
        "skill_name": skill_name,
        "version": version,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def main():
    ap = argparse.ArgumentParser(description="Sign a skill directory with Ed25519")
    ap.add_argument("skill_dir", help="Path to skill directory")
    ap.add_argument("--version", default="", help="Optional version string for the sign.key")
    ap.add_argument("--signed-by", default="",
                    help="Author name embedded in sign.key (default: $USER or 'unknown')")
    ap.add_argument("--rotate-key", action="store_true",
                    help="[v1.0 not implemented] Rotate signing key + re-sign all skills")
    args = ap.parse_args()

    if args.rotate_key:
        print("❌ --rotate-key is reserved for a future version (v1.1+).", file=sys.stderr)
        print("   For now, to use a new key: back up your old skills' sign.key,", file=sys.stderr)
        print("   run init.py --force, then re-sign each skill manually.", file=sys.stderr)
        sys.exit(3)

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.is_dir():
        print(f"❌ Not a directory: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    # Load keypair
    priv, pub = load_keypair()
    pub_encoded = encode_pubkey(pub)

    # Refuse to overwrite another author's signature
    existing = read_sign_key(skill_dir)
    if existing:
        existing_pub = existing.get("public_key", "")
        if existing_pub and existing_pub != pub_encoded:
            print(f"❌ This skill is already signed with a DIFFERENT public key:")
            print(f"   Existing: {existing_pub}")
            print(f"   Yours:    {pub_encoded}")
            print(f"   Refusing to overwrite. Move/delete sign.key manually if intentional.")
            sys.exit(1)

    # Resolve metadata
    skill_name = skill_dir.name
    signed_by = args.signed_by or os.environ.get("USER", "") or os.environ.get("USERNAME", "") or "unknown"
    version = args.version or existing.get("version", "")

    # Timestamp — use real local timezone, not hardcoded +08:00
    signed_at = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

    # Collect files + hash
    print(f"📂 Scanning skill files...")
    files = collect_files(skill_dir)
    print(f"   ({len(files)} files included)")
    content_hash = compute_content_hash(skill_dir, files)
    print(f"   content_hash = {content_hash[:24]}...")

    # Sign canonical payload
    payload = canonical_signed_payload(
        skill_name, version, signed_by, signed_at,
        "ed25519", pub_encoded, content_hash,
    )
    sig = ed25519_sign(priv, pub, payload)
    sig_encoded = encode_signature(sig)

    # Build sign.key
    sign_key_data = {
        "skill_name": skill_name,
        "version": version,
        "signed_by": signed_by,
        "signed_at": signed_at,
        "algorithm": "ed25519",
        "public_key": pub_encoded,
        "content_hash": content_hash,
        "signature": sig_encoded,
    }
    out_path = write_sign_key(skill_dir, sign_key_data)

    print(f"")
    print(f"✅ Signed: {skill_name}")
    print(f"   Signer:       {signed_by}")
    print(f"   Version:      {version or '(none)'}")
    print(f"   Signed at:    {signed_at}")
    print(f"   sign.key:     {out_path}")
    print(f"")
    print(f"📋 Share this public key so others can verify:")
    print(f"   {pub_encoded}")
    print(f"")
    print(f"Recipients can verify with:")
    print(f"   python3 verify.py {skill_dir.name} --trust-key-string {pub_encoded}")


if __name__ == "__main__":
    main()
