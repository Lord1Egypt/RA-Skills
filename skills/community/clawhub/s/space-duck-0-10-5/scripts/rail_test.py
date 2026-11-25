#!/usr/bin/env python3
"""
rail_test.py — end-to-end connectivity probe for the peck rail (0.9.0 [P5]).

INTENT: Prove the two-way rail to a peer is live — delivery AND receipt — with
        wording that carries NO grant / attestation / version / ID / financial
        vocabulary. Peer-fraud and anti-echo heuristics fire on that vocabulary;
        a connectivity test must not look like one duck pressuring another to
        vouch for anything. So the probe is deliberately boring: "reply with
        this token so I know the rail is up: <nonce>".

WHAT PASS MEANS (delivery + receipt, never attestation):
  1. DELIVERY ACK — the platform accepted the outbound peck (send_peck exits 0;
     HTTP 200). This proves the sender→platform leg.
  2. RECEIPT ECHO — a reply carrying the exact random nonce lands back in this
     duck's inbox within the timeout. This proves platform→peer→platform→here,
     i.e. the peer's runtime actually received and answered.
  Both must hold. Either alone is a FAIL with a specific reason.

CALLS:  Space Duck backend only (via send_peck.py subprocess for the send, and
        GET /beak/peck/inbox for the echo poll). No third-party hosts.
AUTH:   Beak Key from ~/.space-duck/config.json (Bearer for send, X-Beak-Key
        for the inbox read) — same rails every other script uses.

Usage:
  python3 rail_test.py --to <peer_sdid>
  python3 rail_test.py --to <peer_sdid> --timeout 90 --interval 3

NOTE: this reads the shared inbox non-destructively. If a peck_listener --poll
      is running it may ack the echo first, but the inbox GET still returns
      recent pecks within the `since` window, so the probe still sees the nonce.
"""
import argparse
import json
import os
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CONFIG_PATHS = [
    Path.home() / '.space-duck' / 'config.json',
    Path('/data/.spaceduck') / 'config.json',
    Path('/data/.openclaw/workspace/.spaceduck') / 'config.json',
]
_HERE = os.path.dirname(os.path.abspath(__file__))


def _load_config():
    for p in CONFIG_PATHS:
        try:
            if p.exists():
                cfg = json.loads(p.read_text())
                cfg['_path'] = str(p)
                return cfg
        except Exception:
            continue
    return None


def _inbox_get(api_base, beak_key, sd_id, since_ms, limit=20, timeout=15):
    url = (f'{api_base.rstrip("/")}/beak/peck/inbox'
           f'?spaceduck_id={urllib.parse.quote(sd_id)}'
           f'&since={int(since_ms)}&limit={int(limit)}')
    req = urllib.request.Request(url, headers={'X-Beak-Key': beak_key})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {}
    except Exception as e:
        return 0, {'error': str(e)}


def _send(target_sd, message, purpose, peck_type):
    """Send via send_peck.py in a subprocess (argv list — no shell, no quoting
    hazard). Returns (ok, exit_code, stdout, stderr). ok == platform accepted."""
    argv = [
        sys.executable, os.path.join(_HERE, 'send_peck.py'),
        '--spaceduck-id', target_sd,
        '--message', message,
        '--purpose', purpose,
        '--peck-type', peck_type,
        '--no-auto-grant',        # a rail test must never spawn a grant request
    ]
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=45)
        return p.returncode == 0, p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return False, 124, '', 'send_peck timed out'
    except Exception as e:
        return False, 1, '', str(e)


def rail_test(target_sd, timeout=60, interval=3):
    cfg = _load_config()
    if not cfg:
        print('FAIL: no paired config found. Run: python3 pair.py')
        return 2
    api_base = cfg.get('api_base', 'https://beak.spaceduckling.com').rstrip('/')
    sd_id = cfg.get('spaceduck_id', '')
    beak_key = cfg.get('beak_key', '')
    if not sd_id or not beak_key:
        print('FAIL: config missing spaceduck_id / beak_key.')
        return 2

    nonce = 'rail-' + secrets.token_hex(6)
    # Neutral, actionable wording. "please reply with … so I know the rail is up"
    # is a plain request (the peer's intent gate treats it as actionable and
    # answers) with zero grant/attest/version/ID/financial vocabulary.
    message = (f'Connectivity check — please reply with this token so I know '
               f'the rail is up: {nonce}')
    since_ms = int(time.time() * 1000) - 2000   # small skew guard

    print(f'🛰  rail_test  me={sd_id[:10]}…  peer={target_sd[:10]}…  nonce={nonce}')
    print(f'    api: {api_base}')

    # ── Leg 1: delivery ack ──
    ok, rc, out, err = _send(target_sd, message, purpose='connect', peck_type='query')
    if not ok:
        print('FAIL: delivery NACK — platform did not accept the outbound peck.')
        print(f'    send_peck exit={rc}')
        tail = (out or err or '').strip().splitlines()[-3:]
        for ln in tail:
            print(f'    | {ln}')
        return 1
    print('✅ delivery ack — platform accepted the peck (sender→platform leg up).')

    # ── Leg 2: receipt echo ──
    deadline = time.time() + max(1, timeout)
    polls = 0
    while time.time() < deadline:
        polls += 1
        status, body = _inbox_get(api_base, beak_key, sd_id, since_ms)
        if status == 200:
            for peck in (body.get('pecks') or []):
                msg = peck.get('message') or ''
                if nonce in msg:
                    who = (peck.get('sender_name')
                           or peck.get('sender_spaceduck_id') or '?')
                    from_target = peck.get('sender_spaceduck_id') == target_sd
                    print(f'✅ receipt echo — nonce came back from {who} '
                          f'{"(peer)" if from_target else "(unverified sender)"} '
                          f'after {polls} poll(s).')
                    print('PASS: rail is up both ways (delivery + receipt).')
                    return 0
        elif status not in (0,):
            print(f'    ⚠ inbox poll http_{status}: {body}')
        time.sleep(max(1, interval))

    print(f'FAIL: delivered, but no receipt echo within {timeout}s '
          f'({polls} poll(s)).')
    print('    Likely: peer offline / not auto-responding / no return rail.')
    print('    The sender→platform leg is proven; the return leg is not.')
    return 1


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description='Connectivity-only peck rail test (delivery + receipt echo).')
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument('--to', metavar='SDID', help='peer Space Duck ID (16 hex)')
    grp.add_argument('--spaceduck-id', dest='to', metavar='SDID',
                     help='peer Space Duck ID (alias for --to)')
    ap.add_argument('--timeout', type=int, default=60,
                    help='seconds to wait for the receipt echo (default 60)')
    ap.add_argument('--interval', type=int, default=3,
                    help='inbox poll interval in seconds (default 3)')
    args = ap.parse_args()
    sys.exit(rail_test(args.to, timeout=args.timeout, interval=args.interval))
