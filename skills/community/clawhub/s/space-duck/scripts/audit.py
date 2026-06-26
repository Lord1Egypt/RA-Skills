#!/usr/bin/env python3
"""
Space Duck — Show recent activity log (pecks, tier changes, cert events).

INTENT: Fetch the duckling-scoped audit trail from Space Duck's backend.
CALLS:  POST <api>/beak/audit  body: {duckling_id, limit}
        Space Duck's own backend only — no third-party hosts.
AUTH:   Beak Key from ~/.space-duck/config.json, sent as X-Beak-Key
        header to the Space Duck backend.

Default: last 20 events. Shows peck events, tier changes, cert actions, etc.

Usage: python3 audit.py [--limit N] [--json]
"""
import json, sys, datetime, urllib.request, urllib.error, argparse
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'

EVENT_ICONS = {
    'peck.sent':        '→🦆',
    'peck.received':    '←🦆',
    'peck.approved':    '✅',
    'peck.denied':      '❌',
    'pulse':            '💓',
    'tier.change':      '⬆️ ',
    'cert.issued':      '📜',
    'cert.verified':    '✔️ ',
    'agent.registered': '🐣',
    'agent.deleted':    '🪦',
    'key.rotated':      '🔑',
}

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())

def fmt_ts(ts):
    if not ts:
        return '?'
    try:
        dt = datetime.datetime.fromtimestamp(int(ts), datetime.UTC)
        return dt.strftime('%d %b %H:%M UTC')
    except Exception:
        return str(ts)

def show_audit(cfg, limit=20, as_json=False):
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    did = cfg.get('duckling_id', '')
    bk  = cfg.get('beak_key', '')

    payload = json.dumps({'duckling_id': did, 'limit': limit}).encode()
    req = urllib.request.Request(
        f"{api}/beak/audit",
        data=payload,
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Beak-Key': bk,
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} — {e.read().decode()}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    entries = data.get('entries', data.get('events', []))

    if as_json:
        print(json.dumps(entries, indent=2))
        return

    if not entries:
        print('No activity found.')
        return

    print(f'📋 Recent Activity (last {len(entries)} events)')
    print()
    for e in entries:
        etype  = e.get('event_type', e.get('type', '?'))
        detail = e.get('detail', e.get('description', ''))
        ts     = fmt_ts(e.get('timestamp', e.get('created_at')))
        icon   = EVENT_ICONS.get(etype, '•')
        print(f"  {icon}  {ts}  {etype}")
        if detail:
            print(f"          {detail}")

    print()
    print(f'  Full log: https://spaceduckling.com/mission-control.html#audit')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show Space Duck activity log')
    parser.add_argument('--limit', type=int, default=20, help='Number of events (default: 20)')
    parser.add_argument('--json', dest='as_json', action='store_true')
    args = parser.parse_args()

    cfg = load_config()
    show_audit(cfg, limit=args.limit, as_json=args.as_json)
