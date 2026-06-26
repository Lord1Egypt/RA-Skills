#!/usr/bin/env python3
"""
Space Duck — List active peck connections (and pending requests) for this duck.

INTENT: Fetch the peer list from Space Duck's backend, then format for
        humans or emit JSON.
CALLS:  POST <api>/beak/spaceducks — Space Duck's own backend only.
AUTH:   Reads duckling_id from ~/.space-duck/config.json. The listing
        endpoint scopes by duckling_id alone, so the Beak Key is not
        transmitted on this call.

Default: show approved/active connections.
--pending: show only pending (unanswered) requests.
--bond <sd_b>: 2026-06-08 — create an owner-internal bond between THIS
  duck (config's spaceduck_id) and the given peer duck. Both must share
  the same owner (duckling_id). Idempotent — duplicates are skipped.
  Calls POST /beak/me/internal-bond (lambda v701). Auth uses the local
  Beak Key.
--bond-all: 2026-06-08 — mesh-bond every duck owned by this duckling
  with every other one. Single call to /beak/me/internal-bond-all
  (lambda v702). Caps at 50 ducks.

Usage:
  python3 connections.py
  python3 connections.py --pending
  python3 connections.py --json
  python3 connections.py --bond <sd_b_id>
  python3 connections.py --bond-all
"""
import json, sys, urllib.request, urllib.error
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())

def list_connections(cfg, pending_only=False, as_json=False):
    api  = cfg.get('api_base', 'https://beak.spaceduckling.com')
    sdid = cfg.get('spaceduck_id', '')
    did  = cfg.get('duckling_id', '')

    if not did:
        print('ERROR: duckling_id missing from config. Re-run setup.py.')
        sys.exit(1)

    payload = json.dumps({'duckling_id': did}).encode()
    req = urllib.request.Request(
        f"{api}/beak/spaceducks",
        data=payload,
        headers={'Content-Type': 'application/json'},
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

    all_pecks = data.get('connections', data.get('pecks', []))
    pending   = [p for p in all_pecks if str(p.get('status', '')).lower() in ('pending', 'requested')]
    connected = [p for p in all_pecks if str(p.get('status', '')).lower() in ('connected', 'approved', 'active', 'bond', 'bonded', 'flock', 'bound')]

    # Direction classifier: prefer server-provided 'direction' (v474+); fall
    # back to caller-id heuristics for un-patched servers.
    def _dir(p):
        d = (p.get('direction') or '').lower()
        if d in ('self', 'outbound', 'inbound', 'unknown'):
            return d
        peer = p.get('peer_id') or p.get('spaceduck_id') or ''
        if peer and (peer == sdid or peer == did):
            return 'self'
        req = p.get('requester_id') or p.get('sender_id') or ''
        if req and (req == did or req == sdid):
            return 'outbound'
        return 'unknown'

    if as_json:
        out = pending if pending_only else {'pending': pending, 'connected': connected}
        print(json.dumps(out, indent=2, default=str))
        return

    if pending_only:
        if not pending:
            print('[connections] No pending peck requests.')
            return
        inbound  = [p for p in pending if _dir(p) == 'inbound']
        outbound = [p for p in pending if _dir(p) == 'outbound']
        stale    = [p for p in pending if _dir(p) == 'self']
        unknown  = [p for p in pending if _dir(p) == 'unknown']

        def _line(p):
            rid     = p.get('peer_id', p.get('requester_id', p.get('sender_id', '?')))
            rname   = p.get('peer_name', p.get('requester_name', p.get('sender_name', rid)))
            purpose = p.get('purpose', p.get('message', '—'))
            peck_id = p.get('peck_id', p.get('connection_id', '?'))
            return rid, rname, purpose, peck_id

        if inbound:
            print(f'[connections] Inbound — {len(inbound)} request(s) you can approve:')
            for p in inbound:
                rid, rname, purpose, peck_id = _line(p)
                print(f"  • {rname} ({rid})")
                print(f"    Purpose: {purpose}")
                print(f"    → approve: python3 check_pecks.py --approve {peck_id}")
                print(f"    → deny:    python3 check_pecks.py --deny {peck_id}")
        else:
            print('[connections] Inbound — none.')

        if outbound:
            print(f'[connections] Outbound — {len(outbound)} awaiting peer approval (no action):')
            for p in outbound:
                rid, rname, purpose, _pid = _line(p)
                print(f"  • {rname} ({rid})  Purpose: {purpose}")

        if stale:
            print(f'[connections] Stale — {len(stale)} self-referential record(s); ignore.')

        if unknown:
            print(f'[connections] Unknown direction — {len(unknown)} record(s); inspect with --json.')
        return

    # Dedup by peer SDID (keep newest by timestamp) and drop self-references.
    # Server returns one row per peck event, so the same peer can appear many
    # times; collapse to one line per peer. A row whose peer is THIS duck is a
    # stale self-referential record and is hidden here (matches --pending).
    def _peer_id(c):
        return c.get('peer_id', c.get('requester_spaceduck_id',
               c.get('target_spaceduck_id', c.get('spaceduck_id', '?'))))
    def _since(c):
        return c.get('connected_at', c.get('approved_at', c.get('created_at', '')))

    by_peer = {}
    self_refs = 0
    for c in connected:
        pid = _peer_id(c)
        if pid in (sdid, did) or not pid or pid == '?':
            self_refs += 1
            continue
        prev = by_peer.get(pid)
        if prev is None or (_since(c) or '') > (_since(prev) or ''):
            by_peer[pid] = c
    unique = sorted(by_peer.values(), key=lambda c: _since(c) or '', reverse=True)

    print(f'🔗 Active connections for duck {cfg.get("agent_name","?")} ({sdid})')
    print()
    if not unique:
        print('  No active connections yet.')
        print(f'  → Explore ducks to peck: https://spaceduckling.com/explore.html')
    else:
        for c in unique:
            peer_id   = _peer_id(c)
            peer_name = c.get('peer_name', c.get('agent_name', c.get('display_name', peer_id)))
            tier      = c.get('peer_tier', c.get('trust_tier', '?'))
            since     = _since(c)
            print(f"  🟢 {peer_name}  (ID: {peer_id}  |  Tier: {tier})")
            if since:
                print(f"       Connected since: {since}")
            print(f"       View: https://spaceduckling.com/explore.html?duck={peer_id}")
            print()
        dropped = len(connected) - len(unique) - self_refs
        if dropped > 0:
            print(f'  ({dropped} duplicate row(s) collapsed)')

    if self_refs:
        print(f'  ⓘ {self_refs} self-referential record(s) hidden.')

    if pending:
        print(f'  ⏳ {len(pending)} pending request(s) — run with --pending to review')

    print(f'  Manage connections: https://spaceduckling.com/mission-control.html?agent={sdid}')

def bond_pair(cfg, sd_b):
    """0.3.12 — create an owner-internal bond between cfg.spaceduck_id
    and sd_b. Both must share an owner. Uses the local Beak Key.
    Idempotent on the server side."""
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    sd_a = cfg.get('spaceduck_id', '')
    bk   = cfg.get('beak_key', '')
    if not sd_a or not bk:
        print('ERROR: spaceduck_id or beak_key missing from config.')
        sys.exit(1)
    if not sd_b:
        print('ERROR: target spaceduck_id required (pass after --bond).')
        sys.exit(1)
    body = json.dumps({'sd_a': sd_a, 'sd_b': sd_b}).encode()
    req = urllib.request.Request(
        f'{api}/beak/me/internal-bond',
        data=body, method='POST',
        headers={'Content-Type': 'application/json',
                 'Authorization': f'Bearer {bk}'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as he:
        try: d = json.loads(he.read())
        except Exception: d = {'error': str(he)}
        print(f'✗ HTTP {he.code}: {d.get("error", "")}')
        sys.exit(2)
    except Exception as e:
        print(f'✗ Error: {e}')
        sys.exit(2)
    if d.get('created'):
        print(f'🔗 Bonded {sd_a[:8]}… ↔ {sd_b[:8]}…  '
              f'connection_id={d.get("connection_id", "")}')
    elif d.get('ok'):
        print(f'✓ Already bonded (idempotent — connection_id='
              f'{d.get("connection_id", "")})')
    else:
        print(f'✗ Unexpected response: {d}')


def bond_all(cfg):
    """0.3.12 — mesh-bond every duck under this owner. Idempotent."""
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    bk  = cfg.get('beak_key', '')
    if not bk:
        print('ERROR: beak_key missing from config.')
        sys.exit(1)
    req = urllib.request.Request(
        f'{api}/beak/me/internal-bond-all',
        data=b'{}', method='POST',
        headers={'Content-Type': 'application/json',
                 'Authorization': f'Bearer {bk}'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as he:
        try: d = json.loads(he.read())
        except Exception: d = {'error': str(he)}
        print(f'✗ HTTP {he.code}: {d.get("error", "")}')
        sys.exit(2)
    except Exception as e:
        print(f'✗ Error: {e}')
        sys.exit(2)
    print(f'🕸️  Mesh-bond complete: '
          f'{d.get("created", 0)} created, '
          f'{d.get("skipped", 0)} already existed'
          + (f', {d.get("errors", 0)} errors' if d.get("errors") else '')
          + f'  ({d.get("duck_count", 0)} ducks, '
          f'{d.get("pairs_total", 0)} pairs total)')


if __name__ == '__main__':
    cfg = load_config()
    # 0.3.12 — bond subcommands run, then exit. Listing is the default.
    if '--bond-all' in sys.argv:
        bond_all(cfg)
        sys.exit(0)
    if '--bond' in sys.argv:
        try:
            idx = sys.argv.index('--bond')
            sd_b = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ''
        except (ValueError, IndexError):
            sd_b = ''
        bond_pair(cfg, sd_b)
        sys.exit(0)
    pending_only = '--pending' in sys.argv
    as_json      = '--json' in sys.argv
    list_connections(cfg, pending_only=pending_only, as_json=as_json)
