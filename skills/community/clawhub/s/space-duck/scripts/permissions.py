#!/usr/bin/env python3
"""
Space Duck — Inspect connection permissions for a peck'd duck.

INTENT: Tell the agent what's *actually* shared with a given peer (files,
        topics, rate caps, daily caps, budget, cooldown, blocked terms)
        BEFORE it tries to peck and gets a 403.
CALLS:  POST <api>/beak/connection/permissions   — read current permissions
        PUT  <api>/beak/connection/permissions   — update (optional)
AUTH:   X-Beak-Key header from ~/.space-duck/config.json (chmod 600).
        No HMAC required — this endpoint is owner-scoped via beak key.

Permissions live per-connection (you ↔ the target). Defaults on a fresh
connection: rate 10/hr, daily 50, no budget cap, 5-min cooldown, no topic
restrictions, T0 minimum tier.

Usage:
  # Show what's shared with one peer
  python3 permissions.py --target <spaceduck_id>

  # JSON output (e.g. for a pre-send check in send_peck)
  python3 permissions.py --target <id> --json

  # Update fields (whitelist below; others are ignored server-side)
  python3 permissions.py --target <id> \\
      --set rate_limit_per_hour=5 daily_limit=20 daily_budget_usd=1.5
"""
import argparse, json, sys, urllib.error, urllib.request
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'

ALLOWED_FIELDS = {
    'allowed_topics':       'list[str]',
    'blocked_topics':       'list[str]',
    'rate_limit_per_hour':  'int',
    'daily_limit':          'int',
    'daily_budget_usd':     'float',
    'block_below_tier':     'str (T0|T1|T2|T3)',
    'cooldown_minutes':     'int',
    'stop_keywords':        'list[str]',
    'notify_parent_on':     'list[str]',
    'shared_files':         'list[str]',
    'muted_until':          'int',  # epoch seconds; 0 = unmuted (added 2026-05-17)
}

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())

def _headers(cfg):
    h = {'Content-Type': 'application/json',
         'X-Beak-Key': cfg.get('beak_key', '')}
    if cfg.get('spaceduck_id'):
        h['X-Spaceduck-ID'] = cfg['spaceduck_id']
    return h

def _request(method, url, headers, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def _http_err(e):
    body = e.read().decode()
    print(f'ERROR: HTTP {e.code} — {body}')
    sys.exit(1)

def get_permissions(cfg, target_id):
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    body = {'spaceduck_id': cfg.get('spaceduck_id', ''), 'target_id': target_id}
    try:
        return _request('POST', f'{api}/beak/connection/permissions',
                        _headers(cfg), body)
    except urllib.error.HTTPError as e:
        _http_err(e)
    except Exception as e:
        print(f'ERROR: {e}'); sys.exit(1)

def update_permissions(cfg, target_id, updates):
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    body = {
        'spaceduck_id': cfg.get('spaceduck_id', ''),
        'target_id':    target_id,
        'permissions':  updates,
    }
    try:
        return _request('PUT', f'{api}/beak/connection/permissions',
                        _headers(cfg), body)
    except urllib.error.HTTPError as e:
        _http_err(e)
    except Exception as e:
        print(f'ERROR: {e}'); sys.exit(1)

def _print_perms(target_id, data):
    perms  = data.get('permissions', {})
    shared = data.get('shared_files', [])
    cid    = data.get('connection_id', '?')

    print(f'🔒 Permissions for connection with {target_id}')
    print(f'   Connection ID: {cid}')
    print()
    print('   Caps:')
    print(f'     • Rate limit / hr:  {perms.get("rate_limit_per_hour", 10)}')
    print(f'     • Daily limit:      {perms.get("daily_limit", 50)}')
    print(f'     • Daily budget:     ${perms.get("daily_budget_usd", 0.0):.2f}'
          f'  ({"no cap" if not perms.get("daily_budget_usd") else "auto-stop on cap"})')
    print(f'     • Cooldown:         {perms.get("cooldown_minutes", 5)} min')
    print(f'     • Min tier:         {perms.get("block_below_tier", "T0")}')
    print()
    print('   Topic gates:')
    at = perms.get('allowed_topics') or []
    bt = perms.get('blocked_topics') or []
    print(f'     • Allowed: {", ".join(at) if at else "(any — no whitelist)"}')
    print(f'     • Blocked: {", ".join(bt) if bt else "(none)"}')
    sk = perms.get('stop_keywords') or []
    if sk:
        print(f'     • Stop on: {", ".join(sk)}')
    print()
    print('   Shared files:')
    if shared:
        for f in shared:
            print(f'     • {f}')
    else:
        print('     (none — peer can\'t read any file zones)')
    npo = perms.get('notify_parent_on') or []
    if npo:
        print()
        print(f'   Notify parent on: {", ".join(npo)}')

def _parse_set(pairs):
    """Parse k=v pairs into typed updates against ALLOWED_FIELDS."""
    out = {}
    for raw in pairs:
        if '=' not in raw:
            print(f'ERROR: --set value must be key=value, got "{raw}"'); sys.exit(1)
        k, v = raw.split('=', 1)
        k = k.strip(); v = v.strip()
        if k not in ALLOWED_FIELDS:
            print(f'ERROR: "{k}" is not an allowed permission field. '
                  f'Allowed: {", ".join(ALLOWED_FIELDS)}'); sys.exit(1)
        kind = ALLOWED_FIELDS[k]
        try:
            if kind == 'int':
                out[k] = int(v)
            elif kind == 'float':
                out[k] = float(v)
            elif kind.startswith('list'):
                out[k] = [s.strip() for s in v.split(',') if s.strip()]
            else:
                out[k] = v
        except ValueError:
            print(f'ERROR: could not parse {k}={v} as {kind}'); sys.exit(1)
    return out

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Inspect / update connection permissions')
    p.add_argument('--target', required=True, metavar='SPACEDUCK_ID')
    p.add_argument('--json',   action='store_true', help='Emit raw JSON')
    p.add_argument('--set',    nargs='+', metavar='key=value',
                   help='Update permission fields (PUT). See ALLOWED_FIELDS.')
    args = p.parse_args()

    cfg = load_config()

    if args.set:
        updates = _parse_set(args.set)
        resp = update_permissions(cfg, args.target, updates)
        if args.json:
            print(json.dumps(resp, indent=2, default=str))
        else:
            print(f'✏️  Updated {len(updates)} field(s) for {args.target}.')
            _print_perms(args.target, resp)
    else:
        data = get_permissions(cfg, args.target)
        if args.json:
            print(json.dumps(data, indent=2, default=str))
        else:
            _print_perms(args.target, data)
