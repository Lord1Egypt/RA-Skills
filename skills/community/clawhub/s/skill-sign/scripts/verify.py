#!/usr/bin/env python3
"""
verify.py — verify a signed skill directory.

Usage:
    # Self-verify (defends against tampering after signing,
    #              but NOT against substitution by attacker with own keypair)
    python3 verify.py <skill-dir>

    # Trust-verify (defends against BOTH tampering AND substitution)
    python3 verify.py <skill-dir> --trust-key <pubkey-file>
    python3 verify.py <skill-dir> --trust-key-string ed25519:<base64>

Exit codes:
    0 = PASS (content unmodified + signature valid + [if --trust-key] trusted author)
    1 = FAIL (tampering detected OR signature invalid OR untrusted public key)
    2 = ERROR (malformed sign.key, missing file, etc.)
"""

import os
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _lib import (
    collect_files, compute_content_hash,
    ed25519_verify, decode_pubkey, decode_signature, encode_pubkey,
    read_sign_key,
)
# Import canonical payload builder from sign.py (single source of truth)
from sign import canonical_signed_payload


def load_trust_key(arg_file: str | None, arg_string: str | None) -> bytes | None:
    """Resolve trusted public key from either --trust-key file or --trust-key-string."""
    if arg_string:
        return decode_pubkey(arg_string)
    if arg_file:
        p = Path(arg_file).expanduser()
        if not p.exists():
            print(f"❌ Trust key file not found: {p}", file=sys.stderr)
            sys.exit(2)
        raw = p.read_bytes()
        # Accept either binary 32 bytes or text (ed25519:base64)
        if len(raw) == 32:
            return raw
        try:
            return decode_pubkey(raw.decode("utf-8", errors="replace"))
        except Exception as e:
            print(f"❌ Invalid trust key file: {e}", file=sys.stderr)
            sys.exit(2)
    return None


def main():
    ap = argparse.ArgumentParser(description="Verify a signed skill directory")
    ap.add_argument("skill_dir", help="Path to skill directory")
    ap.add_argument("--trust-key", help="Path to trusted public key file (binary 32B or ed25519:base64 text)")
    ap.add_argument("--trust-key-string", help="Trusted public key as 'ed25519:<base64>' string")
    ap.add_argument("--detail", action="store_true", help="Show full file list on failure")
    args = ap.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.is_dir():
        print(f"❌ Not a directory: {skill_dir}", file=sys.stderr)
        sys.exit(2)

    sk = read_sign_key(skill_dir)
    if not sk:
        print(f"❌ No sign.key found in {skill_dir}")
        print(f"   This skill has not been signed.")
        sys.exit(1)

    # Validate sign.key shape
    required = ["skill_name", "version", "signed_by", "signed_at",
                "algorithm", "public_key", "content_hash", "signature"]
    missing = [k for k in required if k not in sk]
    if missing:
        print(f"❌ sign.key is malformed (missing: {', '.join(missing)})", file=sys.stderr)
        sys.exit(2)

    if sk["algorithm"] != "ed25519":
        print(f"❌ Unsupported algorithm: {sk['algorithm']} (this tool only handles ed25519)",
              file=sys.stderr)
        sys.exit(2)

    # Resolve trust key (optional)
    trust_key = load_trust_key(args.trust_key, args.trust_key_string)

    # Header
    print(f"📋 Verifying: {sk['skill_name']}")
    print(f"   Signed by:    {sk['signed_by']}")
    print(f"   Signed at:    {sk['signed_at']}")
    print(f"   Version:      {sk.get('version') or '(none)'}")
    print(f"   Public key:   {sk['public_key']}")
    print()

    # Decode embedded public key & signature
    try:
        embedded_pub = decode_pubkey(sk["public_key"])
        sig_bytes = decode_signature(sk["signature"])
    except ValueError as e:
        print(f"❌ sign.key contains invalid key/signature: {e}", file=sys.stderr)
        sys.exit(2)

    # === Check 1: content_hash matches actual files ===
    files = collect_files(skill_dir)
    actual_hash = compute_content_hash(skill_dir, files)
    content_ok = (actual_hash == sk["content_hash"])

    # === Check 2: signature over canonical payload matches ===
    payload = canonical_signed_payload(
        sk["skill_name"], sk["version"], sk["signed_by"], sk["signed_at"],
        sk["algorithm"], sk["public_key"], sk["content_hash"],
    )
    sig_ok = ed25519_verify(embedded_pub, payload, sig_bytes)

    # === Check 3 (if --trust-key given): embedded pubkey matches trusted ===
    if trust_key is not None:
        trust_ok = (trust_key == embedded_pub)
    else:
        trust_ok = None  # skipped

    # ===== Report =====
    if content_ok and sig_ok and (trust_ok is not False):
        print(f"✅ PASS — Skill integrity verified.")
        print(f"   content_hash  : ✓ matches actual files")
        print(f"   signature     : ✓ valid for embedded public key")
        if trust_ok is True:
            print(f"   trusted author: ✓ public key matches --trust-key")
            print(f"")
            print(f"   This skill is unmodified AND verified as authored by the trusted key holder.")
        else:
            print(f"   trusted author: ⚠️  not checked (run with --trust-key to verify author)")
            print(f"")
            print(f"   ⚠️  This proves the skill is unmodified since signing, but NOT that")
            print(f"      it was signed by the person you think — anyone can self-sign.")
            print(f"      To verify author identity, run again with:")
            print(f"        --trust-key-string {sk['public_key']}")
            print(f"      (but only after you've obtained this key from a TRUSTED source,")
            print(f"       e.g. the author's official GitHub README.)")
        sys.exit(0)

    # FAIL path
    print(f"❌ FAIL — Verification failed.")
    print()
    if not content_ok:
        print(f"   content_hash  : ✗ MISMATCH")
        print(f"     expected : {sk['content_hash']}")
        print(f"     actual   : {actual_hash}")
        if args.detail:
            print(f"   Files currently in skill ({len(files)}):")
            for f in files:
                print(f"     {f}")
            print(f"   → Diff against signing time: not stored. Recompute requires re-signing.")
        else:
            print(f"     (re-run with --detail to list current files)")
    else:
        print(f"   content_hash  : ✓ ok")

    if not sig_ok:
        print(f"   signature     : ✗ INVALID")
        print(f"     The signature does not verify against the embedded public key.")
        print(f"     Either the sign.key was tampered with (metadata changed but not re-signed)")
        print(f"     or the signature itself was corrupted.")
    else:
        print(f"   signature     : ✓ ok")

    if trust_ok is False:
        print(f"   trusted author: ✗ MISMATCH")
        print(f"     Embedded public key in sign.key:")
        print(f"       {sk['public_key']}")
        print(f"     Your trusted key:")
        print(f"       {encode_pubkey(trust_key)}")
        print(f"     → This skill was signed by someone else (or with a different key).")
        print(f"       Do NOT trust this skill unless you also trust the embedded key.")

    print()
    print(f"💡 If you trust the current state and want to re-sign:")
    print(f"   python3 {os.path.dirname(__file__)}/sign.py {skill_dir}")
    sys.exit(1)


if __name__ == "__main__":
    main()
