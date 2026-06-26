"""Beak protocol envelope helper — identity attestation for Space Duck pecks.

A peck is a small JSON message sent from one paired duck (sender) to another
(target) via the Space Duck backend. Each peck carries an envelope describing
who-said-what-to-whom; the envelope is signed with the sender's per-duck
Beak Key (issued at pair time and stored on the sender's machine in
~/.space-duck/config.json). The server re-canonicalises the envelope and
checks the signature against the stored Beak Key — this is **identity
attestation**, not credential transport.

The envelope schema is the v2 "Phase E" form (server-side reference:
lambda_function.py:_envelope_v2_canonical). Two functions live here:

  canonical_v2(env) -> str
      Serialise the envelope to a stable byte form. Sort keys, drop
      formatting whitespace, coerce expected types. Must match the server
      byte-for-byte.

  sign_v2(env, beak_key) -> str
      Standard HMAC-SHA256(beak_key, canonical_v2(env)) hex digest.

The skill keeps these in their own module so the per-script intent is
clear: send_peck.py orchestrates a peck, _envelope.py describes how a
peck identifies itself.
"""
import hashlib
import hmac
import json


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
