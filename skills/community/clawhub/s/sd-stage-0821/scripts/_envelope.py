"""Beak protocol envelope helper — identity attestation for Space Duck pecks.

A peck is a small JSON message sent from one paired duck (sender) to another
(target) via the Space Duck backend. Each peck carries an envelope describing
who-said-what-to-whom; the envelope is signed with the sender's per-duck
credential and re-canonicalised by the server for verification. This is
**identity attestation**, not credential transport.

Two signing lanes live here:

  v2 — symmetric HMAC (legacy).
    canonical_v2(env) -> stable byte form (8 fields).
    sign_v2(env, beak_key) -> HMAC-SHA256(beak_key, canonical_v2(env)) hex.
    Server reference: lambda_function.py:_envelope_v2_canonical /
    _envelope_v2_sign. The Beak Key is the platform-held symmetric secret.

  v3 — Ed25519 asymmetric ([BEAK-V3-P2], docs/spec/BEAK-V3-ASYMMETRIC-IDENTITY.md).
    canonical_v3(env) -> stable byte form (10 fields = v2's 8 + `sender_key_id`
      + `protocol_caps`, both coerced identically to the server side).
    sign_v3(env, privkey_raw_hex) -> Ed25519(privkey).sign(canonical_v3).hex().
    Server reference: lambda_function.py:_envelope_v3_canonical /
    _envelope_v3_verify. The server holds ONLY the pubkey; the privkey
    stays on the owner's box at ~/.space-duck/sign_key.hex (chmod 0600).

Key helpers:

  load_sign_key() -> (privkey_hex, pubkey_hex, key_id) or (None, None, None)
    Read ~/.space-duck/sign_key.hex if present. Lazy imports cryptography.
  derive_key_id(pubkey_hex) -> 'sk_<8hex>' matching the server rule.

The skill keeps these in their own module so the per-script intent is clear:
send_peck.py orchestrates a peck; _envelope.py describes how a peck identifies
itself.
"""
import hashlib
import hmac
import json
from pathlib import Path


SIGN_KEY_PATH = Path.home() / '.space-duck' / 'sign_key.hex'


def canonical_v2(env):
    """Return the stable byte form of a v2 envelope for signing.

    Caller passes a dict with the seven envelope fields plus message_hash;
    we coerce each to its server-expected type and emit a JSON form with
    sorted keys + compact separators.
    """
    canonical = {
        'from_spaceduck_id': str(env.get('from_spaceduck_id', '')),
        'to_spaceduck_id':   str(env.get('to_spaceduck_id', '')),
        'conversation_id':   str(env.get('conversation_id', '')),
        'turn_index':        int(env.get('turn_index', 0) or 0),
        'intent':            str(env.get('intent', '')),
        'scopes_asserted':   sorted(env.get('scopes_asserted') or []),
        'timestamp':         int(env.get('timestamp', 0) or 0),
        'message_hash':      str(env.get('message_hash', '')),
    }
    return json.dumps(canonical, sort_keys=True, separators=(',', ':'))


def sign_v2(env, beak_key):
    """Return the HMAC-SHA256 hex digest of canonical_v2(env) keyed on beak_key.

    The Beak Key is an identity secret bound to a single Space Duck. The server
    looks up the duck's stored Beak Key and recomputes the same HMAC; mismatch
    rejects the peck. No credentials beyond identity attestation are conveyed.
    """
    return hmac.new(beak_key.encode(), canonical_v2(env).encode(), hashlib.sha256).hexdigest()


def canonical_v3(env):
    """Return the stable byte form of a v3 asymmetric envelope for Ed25519 signing.

    Byte-identical to the server's `_envelope_v3_canonical`: v2's eight fields
    plus `sender_key_id` (short id of the signing pubkey, `sk_<8hex>`) and
    `protocol_caps` (sorted list of capability strings). Field coercions match
    the server exactly — any drift here breaks server verify, so the two
    functions MUST be kept in lock-step.
    """
    canonical = {
        'from_spaceduck_id': str(env.get('from_spaceduck_id', '')),
        'to_spaceduck_id':   str(env.get('to_spaceduck_id', '')),
        'conversation_id':   str(env.get('conversation_id', '')),
        'turn_index':        int(env.get('turn_index', 0) or 0),
        'intent':            str(env.get('intent', '')),
        'scopes_asserted':   sorted(env.get('scopes_asserted') or []),
        'timestamp':         int(env.get('timestamp', 0) or 0),
        'message_hash':      str(env.get('message_hash', '')),
        'sender_key_id':     str(env.get('sender_key_id', '')),
        'protocol_caps':     sorted(env.get('protocol_caps') or []),
    }
    return json.dumps(canonical, sort_keys=True, separators=(',', ':'))


def sign_v3(env, privkey_raw_hex):
    """Return the Ed25519 hex signature over canonical_v3(env).

    `privkey_raw_hex` is 64 lowercase hex chars = 32 raw Ed25519 private-key
    bytes (matches what `sign_key.py setup` writes to ~/.space-duck/sign_key.hex).
    Lazily imports `cryptography`; when unavailable, raises RuntimeError naming
    the exact install command so callers can fall back to v2 gracefully.
    """
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except ImportError as _e:
        raise RuntimeError(
            'v3 envelope signing needs the `cryptography` package. '
            'Install it with: pip install cryptography'
        ) from _e
    if not privkey_raw_hex or len(privkey_raw_hex) != 64:
        raise RuntimeError('sign_v3: privkey_raw_hex must be 64 hex chars (32 raw bytes).')
    priv = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(privkey_raw_hex))
    return priv.sign(canonical_v3(env).encode('utf-8')).hex()


def derive_key_id(pubkey_hex):
    """Return the short `sk_<8hex>` identifier for a raw Ed25519 pubkey.

    Matches the server rule: `'sk_' + sha256(raw_pubkey_bytes).hexdigest()[:8]`.
    """
    pk = (pubkey_hex or '').strip().lower()
    if not pk:
        return ''
    return 'sk_' + hashlib.sha256(bytes.fromhex(pk)).hexdigest()[:8]


def load_sign_key():
    """Read ~/.space-duck/sign_key.hex and return (privkey_hex, pubkey_hex, key_id).

    Returns (None, None, None) when the file is absent, unreadable, or malformed,
    or when the `cryptography` package is not installed. Callers should treat a
    None result as "no v3 key available — fall back to v2".
    """
    if not SIGN_KEY_PATH.exists():
        return (None, None, None)
    try:
        privkey_hex = SIGN_KEY_PATH.read_text().strip().lower()
        if not privkey_hex or len(privkey_hex) != 64:
            return (None, None, None)
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        from cryptography.hazmat.primitives import serialization
        priv = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(privkey_hex))
        raw_pub = priv.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        pubkey_hex = raw_pub.hex()
        return (privkey_hex, pubkey_hex, derive_key_id(pubkey_hex))
    except Exception:
        return (None, None, None)
