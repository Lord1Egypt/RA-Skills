#!/usr/bin/env python3
"""
Space Duck — Bind a duck's Telegram bot inbound to your local receiver (β).

INTENT: Walk a BYOB owner through the bind/verify handshake without forcing
        them to hand-roll HMAC. Single command takes:
          - their spaceduck_id (or defaults from config.json)
          - a publicly-reachable HTTPS forward URL
        ...and ends with state=VERIFIED. From that point, every inbound
        Telegram message to that duck's bot gets signed + forwarded to the
        URL by the Space Duck Lambda (per lambda v538 forwarder).

CALLS:  POST /beak/agent/byob-bind
        POST /beak/agent/byob-verify
        GET  /beak/agent/byob-status
        POST /beak/agent/byob-revoke
AUTH:   x-beak-key header (per-duck Beak Key from ~/.space-duck/config.json,
        written by pair.py)

Usage:
  # First-time bind
  python3 bind_telegram.py --forward-url https://my-tunnel.example.com:8788/beak/telegram/forward
  python3 bind_telegram.py --spaceduck-id <SD> --forward-url <URL>

  # Status check
  python3 bind_telegram.py --status
  python3 bind_telegram.py --spaceduck-id <SD> --status

  # Revoke (e.g. switching to a new tunnel URL)
  python3 bind_telegram.py --revoke
  python3 bind_telegram.py --spaceduck-id <SD> --revoke

  # Two-step (mostly for scripting):
  python3 bind_telegram.py --forward-url <URL> --bind-only    # → BINDING
  python3 bind_telegram.py --verify-pending                   # → VERIFIED

States:
  UNBOUND   no binding registered (default for new ducks)
  BINDING   bind submitted, awaiting verify handshake (5min TTL on challenge)
  VERIFIED  active — inbound TG forwards to your URL
  DEGRADED  3 consecutive forward failures; auto-recovers on next success
  REVOKED   owner withdrew binding; URL cleared

Signature scheme (handled automatically):
  secret    = HMAC-SHA256(beak_key, b'byob-hmac-v1')
  signature = HMAC-SHA256(secret, challenge_bytes).hex()

Exit codes:
  0 — VERIFIED (or operation succeeded for --status / --revoke)
  1 — local error (missing args, config, unreachable platform)
  2 — auth error (403 — beak_key didn't match)
  3 — URL validation rejected (not HTTPS, private IP, etc.)
  4 — state mismatch (e.g. tried --verify-pending without prior bind)
"""
import argparse
import hashlib
import hmac
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_API = os.environ.get('SPACE_DUCK_API', 'https://beak.spaceduckling.com')
CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'
PENDING_PATH = Path.home() / '.space-duck' / 'pending_bind.json'


def _load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f'Config not found at {CONFIG_PATH}. Run `python3 pair.py` first.')
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    return cfg.get('beak_key', ''), cfg.get('spaceduck_id', '')


def _compute_signature(beak_key, challenge):
    """Domain-separated HMAC: first derive a per-duck BYOB secret from the
    beak_key (so a beak_key leak in another channel doesn't trivially leak
    forward-signing authority), then sign the challenge."""
    secret = hmac.new(beak_key.encode(), b'byob-hmac-v1', hashlib.sha256).digest()
    return hmac.new(secret, challenge.encode(), hashlib.sha256).hexdigest()


def _http(method, url, body=None, beak_key=None, timeout=15):
    data = json.dumps(body).encode() if body is not None else None
    headers = {'Content-Type': 'application/json'}
    if beak_key:
        headers['x-beak-key'] = beak_key
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as he:
        try:
            err = json.loads(he.read())
        except Exception:
            err = {'error': 'http_error', 'detail': str(he)[:200]}
        return he.code, err
    except urllib.error.URLError as ue:
        return 0, {'error': 'network', 'detail': str(ue)[:200]}


def status(api_base, beak_key, spaceduck_id):
    return _http('GET',
                 f'{api_base.rstrip("/")}/beak/agent/byob-status?spaceduck_id={urllib.parse.quote(spaceduck_id)}',
                 beak_key=beak_key)


def bind(api_base, beak_key, spaceduck_id, forward_url):
    return _http('POST', api_base.rstrip('/') + '/beak/agent/byob-bind',
                 body={'spaceduck_id': spaceduck_id, 'forward_url': forward_url},
                 beak_key=beak_key)


def verify(api_base, beak_key, spaceduck_id, challenge, signature):
    return _http('POST', api_base.rstrip('/') + '/beak/agent/byob-verify',
                 body={'spaceduck_id': spaceduck_id, 'challenge': challenge,
                       'signature': signature},
                 beak_key=beak_key)


def revoke(api_base, beak_key, spaceduck_id):
    return _http('POST', api_base.rstrip('/') + '/beak/agent/byob-revoke',
                 body={'spaceduck_id': spaceduck_id},
                 beak_key=beak_key)


def _emit(o):
    print(json.dumps(o, indent=2))


def main(argv=None):
    p = argparse.ArgumentParser(description='Bind a duck\'s Telegram inbound to a local receiver URL.')
    p.add_argument('--spaceduck-id', help='Spaceduck ID (defaults to config.json value)')
    p.add_argument('--forward-url',
                   help='HTTPS URL of your local /beak/telegram/forward receiver')
    p.add_argument('--status', action='store_true', help='Print current binding state and exit')
    p.add_argument('--revoke', action='store_true', help='Revoke binding (clears URL + state)')
    p.add_argument('--bind-only', action='store_true',
                   help='Two-step: submit bind, save challenge to pending_bind.json, exit')
    p.add_argument('--verify-pending', action='store_true',
                   help='Two-step: verify the challenge saved by --bind-only, exit VERIFIED')
    p.add_argument('--api', default=DEFAULT_API, help='Override API base (advanced)')
    args = p.parse_args(argv)

    try:
        beak_key, default_sd = _load_config()
    except FileNotFoundError as e:
        print(f'ERR: {e}', file=sys.stderr)
        return 1
    sd_id = args.spaceduck_id or default_sd
    if not sd_id:
        print('ERR: --spaceduck-id required (no default in config)', file=sys.stderr)
        return 1

    if args.status:
        s, r = status(args.api, beak_key, sd_id)
        _emit(r)
        return 0 if s == 200 else (2 if s == 403 else 1)

    if args.revoke:
        s, r = revoke(args.api, beak_key, sd_id)
        _emit(r)
        return 0 if s == 200 else (2 if s == 403 else 1)

    if args.verify_pending:
        if not PENDING_PATH.exists():
            print(f'ERR: no pending bind found at {PENDING_PATH}. Run --bind-only first.',
                  file=sys.stderr)
            return 4
        with open(PENDING_PATH) as f:
            pending = json.load(f)
        if pending.get('spaceduck_id') != sd_id:
            print(f'ERR: pending bind is for {pending.get("spaceduck_id")!r}, not {sd_id!r}',
                  file=sys.stderr)
            return 4
        sig = _compute_signature(beak_key, pending['challenge'])
        s, r = verify(args.api, beak_key, sd_id, pending['challenge'], sig)
        _emit(r)
        if s == 200:
            PENDING_PATH.unlink(missing_ok=True)
            return 0
        return 2 if s == 403 else (4 if s == 409 else 1)

    # Default flow: bind (+ optionally verify) in one shot
    if not args.forward_url:
        print('ERR: --forward-url required (or use --status / --revoke / --verify-pending)',
              file=sys.stderr)
        return 1

    s, r = bind(args.api, beak_key, sd_id, args.forward_url)
    if s == 400 and r.get('error') == 'url_rejected':
        _emit(r)
        return 3
    if s == 403:
        _emit(r)
        return 2
    if s != 200:
        _emit(r)
        return 1

    challenge = r.get('verify_challenge', '')
    if not challenge:
        print('ERR: bind succeeded but no verify_challenge returned', file=sys.stderr)
        _emit(r)
        return 1

    if args.bind_only:
        # Persist pending state for a later --verify-pending call.
        PENDING_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(PENDING_PATH, 'w') as f:
            json.dump({
                'spaceduck_id': sd_id,
                'challenge': challenge,
                'expires_at': r.get('challenge_expires_at'),
                'forward_url': args.forward_url,
            }, f)
        os.chmod(PENDING_PATH, 0o600)
        _emit({**r, 'pending_saved_to': str(PENDING_PATH)})
        return 0

    # Default: compute signature + verify immediately
    sig = _compute_signature(beak_key, challenge)
    s2, r2 = verify(args.api, beak_key, sd_id, challenge, sig)
    if s2 == 200:
        _emit({'bind': r, 'verify': r2})
        return 0
    _emit({'bind': r, 'verify': r2, 'verify_status': s2})
    return 2 if s2 == 403 else (4 if s2 == 409 else 1)


if __name__ == '__main__':
    sys.exit(main())
