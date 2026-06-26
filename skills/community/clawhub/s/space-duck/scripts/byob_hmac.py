#!/usr/bin/env python3
"""BYOB Workspace Bridge — HMAC reference implementation (Python).

Pinned to docs/spec/BYOB-WORKSPACE-BRIDGE.md rev 4 (findings B + B-revisit).

Canonical form (byte-exact):
  method            uppercase ASCII (GET, POST)
  path-no-trailing-slash, NFC-normalised filename, lowercase %2f
  unix_ts_as_decimal_string
  hex_lower_sha256_of_body OR EMPTY_SHA256 constant for empty

Symmetric with space-duck-html/static/byob-hmac.js — both implementations
MUST produce byte-identical signatures for the same canonical bytes. T19
in the Phase 4 test suite cross-validates with fixture vectors.

Usage:
  >>> from byob_hmac import byob_sign
  >>> byob_sign('bk_LIVE_...', 'GET', '/v1/files', 1780058400)
  '7e3f...'
  >>> byob_sign('bk_LIVE_...', 'POST', '/v1/file/AGENTS.md', 1780058400, b'{"content":"…"}')
  '9a12...'

CLI for fixture generation:
  $ byob_hmac.py GET /v1/files 1780058400 --key bk_LIVE_test
  7e3f...
"""
import argparse
import hashlib
import hmac
import sys
import unicodedata
import urllib.parse


EMPTY_SHA256 = ('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')


def byob_canonical(method, path, unix_ts, body_bytes=None):
    """Produce the canonical bytes the HMAC is computed over."""
    if path != '/' and path.endswith('/'):
        raise ValueError('trailing_slash_disallowed')
    if body_bytes is None or body_bytes == b'':
        body_hash = EMPTY_SHA256
    else:
        if isinstance(body_bytes, str):
            body_bytes = body_bytes.encode('utf-8')
        body_hash = hashlib.sha256(body_bytes).hexdigest()
    return '\n'.join([method.upper(), path, str(int(unix_ts)), body_hash])


def byob_sign(beak_key, method, path, unix_ts, body_bytes=None):
    """Return hex-lower HMAC-SHA256 over the canonical bytes."""
    canonical = byob_canonical(method, path, unix_ts, body_bytes)
    return hmac.new(beak_key.encode('utf-8'), canonical.encode('utf-8'),
                    hashlib.sha256).hexdigest()


def encode_filename(name):
    """NFC-normalise + percent-encode with lowercase hex (RFC-pinned)."""
    nfc = unicodedata.normalize('NFC', name)
    return urllib.parse.quote(nfc, safe='', encoding='utf-8').lower()


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('method', choices=['GET', 'POST'])
    p.add_argument('path')
    p.add_argument('unix_ts', type=int)
    p.add_argument('--key', required=True, help='beak_key')
    p.add_argument('--body', help='request body (string)')
    args = p.parse_args()
    body = args.body.encode('utf-8') if args.body else None
    print(byob_sign(args.key, args.method, args.path, args.unix_ts, body))
    return 0


if __name__ == '__main__':
    sys.exit(main())
