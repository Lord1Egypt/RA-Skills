#!/usr/bin/env python3
"""
Space Duck — List all ducks (agents) registered under this duckling.

INTENT: Show every agent under the user's duckling account with status,
        trust tier, and last-pulse time.
CALLS:  GET <api>/beak/spaceducks?duckling_id=...
        Space Duck's own backend only — no third-party hosts.
AUTH:   Beak Key from ~/.space-duck/config.json, sent as X-Beak-Key
        header to the Space Duck backend.

Usage: python3 my_ducks.py [--json]
"""
import json, sys, datetime, urllib.request, urllib.error
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())

def ts_label(ts):
    if not ts:
        return 'never'
    try:
        dt = datetime.datetime.fromtimestamp(int(ts), datetime.UTC)
        delta = datetime.datetime.now(datetime.UTC) - dt
        mins = int(delta.total_seconds() // 60)
        if mins < 2:    return 'just now'
        if mins < 60:   return f'{mins}m ago'
        if mins < 1440: return f'{mins // 60}h ago'
        return dt.strftime('%d %b')
    except Exception:
        return str(ts)

def list_ducks(cfg, as_json=False):
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    did = cfg.get('duckling_id', '')
    bk  = cfg.get('beak_key', '')

    req = urllib.request.Request(
        f"{api}/beak/spaceducks?duckling_id={did}",
        headers={'Accept': 'application/json', 'X-Beak-Key': bk}
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

    ducks = data.get('spaceducks', [])

    if as_json:
        print(json.dumps(ducks, indent=2))
        return ducks

    if not ducks:
        print('No ducks registered under your account.')
        print(f'  → Register one at https://spaceduckling.com/the-inlet.html')
        return []

    current_id = cfg.get('spaceduck_id', '')
    print(f'🦆 Mission Control — {len(ducks)} duck(s) for duckling {did}')
    print()

    for d in ducks:
        sid    = d.get('spaceduck_id', '?')
        name   = d.get('agent_name', 'Unnamed')
        status = d.get('status', '?')
        tier   = d.get('trust_tier', '?')
        last   = ts_label(d.get('last_seen'))
        tag    = ' ← this agent' if sid == current_id else ''

        icon = {'ACTIVE': '🟢', 'IDLE': '🟡', 'OFFLINE': '⚫'}.get(status, '⚪')
        print(f"  {icon} {name}{tag}")
        print(f"       ID: {sid}  |  Tier: {tier}  |  Last pulse: {last}")
        print(f"       Manage: https://spaceduckling.com/mission-control.html?agent={sid}")
        print()

    print(f'  Mission Control: https://spaceduckling.com/mission-control.html')
    return ducks

if __name__ == '__main__':
    cfg = load_config()
    as_json = '--json' in sys.argv
    list_ducks(cfg, as_json=as_json)
