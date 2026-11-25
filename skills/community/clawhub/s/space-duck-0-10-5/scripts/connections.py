#!/usr/bin/env python3
"""
Space Duck — List BONDED connections (and pending requests) for this duck.

INTENT: Show the ducks this duck is actually BONDED to — never a duck that
        merely appears alive in the Pond directory. A bond is what lets you
        peck; roster-liveness is not.
CALLS:  POST <api>/beak/spaceducks              — candidate rows (duckling-scoped)
        POST <api>/beak/connection/permissions  — authoritative per-target bond
                                                   verify (X-Beak-Key). 200 =>
                                                   real bond; 404 => not bonded.
AUTH:   Reads duckling_id from ~/.space-duck/config.json for the listing call
        (scoped by duckling_id alone). The bond-verify call sends the Beak Key
        (X-Beak-Key) — the SAME endpoint permissions.py uses, so what shows as
        🟢 here is exactly what the server treats as a bond.

WHY THIS IS TWO STEPS (SKILL-094, 2026-09-14):
  /beak/spaceducks returns rows from the connections table filtered by a WIDE
  ACTIVE_SET that admits status='PENDING' and status='BOND' and defaults each
  row's `relationship` to 'BOND'. The server's own bond resolver
  (_lookup_bilateral_connection / the /beak/connection/permissions matcher)
  only honours _CONNECTED_STATUSES = ACTIVE/approved/BONDED/CONNECTED/FLOCK/
  BOUND. That gap let a roster/pending/one-directional row render as a 🟢
  "connection" for a duck you were never bonded to (Larry→Wayne field report).
  Fix: classify candidates against the server's authoritative status set, then
  VERIFY each survivor with the per-target bond endpoint before calling it a
  connection. Unverified/404 rows are shown separately as "NOT bonded", never
  🟢, so an operator never thinks they can peck a duck they haven't bonded.

Default: show BONDED connections (verified) + a clearly-labelled
         "alive but NOT bonded" section for candidates that failed verify.
--no-verify: skip the per-target bond verify (faster; classifies by status
         only and labels every peer "unverified — bond not confirmed").
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
  python3 connections.py                 # bonded connections (verified) + roster
  python3 connections.py --no-verify     # status-only (no per-target bond probe)
  python3 connections.py --pending
  python3 connections.py --json
  python3 connections.py --bond <sd_b_id>
  python3 connections.py --bond-all
"""
import json, sys, urllib.request, urllib.error
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'

# Mirror of the server's authoritative _CONNECTED_STATUSES
# (coordination/lambda_function.py:4707), lowercased. A real bilateral bond
# carries one of these. Two deliberate exclusions vs the /beak/spaceducks
# ACTIVE_SET (lambda_function.py:28592) are what fix the roster-vs-bond
# conflation:
#   • 'pending' / 'requested' — an unanswered peck or POND_REQUEST is not a bond.
#   • 'bond' — /beak/spaceducks admits status='BOND', but the server's bond
#     resolver only honours 'BONDED'. Treating 'BOND' as connected is exactly
#     what rendered alive-but-unbonded ducks as 🟢.
BONDED_STATUSES = {'active', 'approved', 'bonded', 'connected', 'flock', 'bound'}

# Relationship values that are requests, never bonds. The server DEFAULTS a
# row's relationship to 'BOND' when the field is absent (lambda_function.py:28782),
# so relationship is used only to EXCLUDE obvious requests, never to include.
REQUEST_RELATIONSHIPS = {'POND_REQUEST', 'REQUEST', 'PENDING'}

# Cap on per-target bond-verify probes in one listing (bounds cost on a duck
# with a large candidate set; mirrors the 0.9.1 25-peer cap precedent).
MAX_VERIFY = 25

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    cfg = json.loads(CONFIG_PATH.read_text())
    from _apiguard import check_api_base  # [HARDEN-071]
    check_api_base(cfg)
    return cfg


def verify_bond(api, cfg, peer_id):
    """Authoritative per-target bond check — the SAME endpoint permissions.py
    uses (POST /beak/connection/permissions, X-Beak-Key). Beak-key-reachable,
    no JWT needed. Returns (verdict, detail):
      ('bonded', {connection_id, permissions, shared_files})  — 200, real bond
      ('not_bonded', {})                                      — 404, no bond
      ('unverified', {})                                      — other/error
    """
    sd = cfg.get('spaceduck_id', '')
    bk = cfg.get('beak_key', '')
    if not sd or not bk or not peer_id:
        return ('unverified', {})
    body = json.dumps({'spaceduck_id': sd, 'target_id': peer_id}).encode()
    req = urllib.request.Request(
        f'{api}/beak/connection/permissions', data=body, method='POST',
        headers={'Content-Type': 'application/json',
                 'X-Beak-Key': bk, 'X-Spaceduck-ID': sd})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return ('bonded', json.loads(r.read()))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return ('not_bonded', {})
        return ('unverified', {})
    except Exception:
        return ('unverified', {})


def fetch_bonded_bulk(api, cfg):
    """SKILL-095: one-call authoritative bond list via the beak-key endpoint
    GET /beak/connections/bonded. Replaces up to MAX_VERIFY per-target probes
    when the server supports it. Returns (status, rows):
      ('ok', [ {peer_id, connection_id, status, permissions, shared_files} ])
      ('unavailable', [])  — 404 (older server without the endpoint) or any
                             error → caller falls back to per-target verify
                             (capability negotiation: never break on an old
                             server).
    """
    sd = cfg.get('spaceduck_id', '')
    bk = cfg.get('beak_key', '')
    if not sd or not bk:
        return ('unavailable', [])
    req = urllib.request.Request(
        f'{api}/beak/connections/bonded', method='GET',
        headers={'X-Beak-Key': bk, 'X-Spaceduck-ID': sd})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        return ('ok', data.get('bonded', []) or [])
    except urllib.error.HTTPError:
        # 404 => endpoint not deployed on this server → graceful fallback.
        return ('unavailable', [])
    except Exception:
        return ('unavailable', [])


def _is_bond_candidate(row):
    """Status/relationship gate BEFORE network verify. True only if the row's
    status is in the server's authoritative connected set AND its relationship
    is not a request type. Pure — offline-testable."""
    status = str(row.get('status', '')).lower()
    rel    = str(row.get('relationship', '')).upper()
    if status not in BONDED_STATUSES:
        return False
    if rel in REQUEST_RELATIONSHIPS:
        return False
    return True

def list_connections(cfg, pending_only=False, as_json=False, verify=True):
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
    # "connected" here means CANDIDATE rows whose status passes the server's
    # authoritative connected-status gate. It is NOT proof of a bond — that
    # comes from verify_bond() below. NOTE this deliberately drops the old
    # 'bond' status (see BONDED_STATUSES) that leaked non-bonds through.
    connected = [p for p in all_pecks if _is_bond_candidate(p)]

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

    def _peer_id(c):
        return c.get('peer_id', c.get('requester_spaceduck_id',
               c.get('target_spaceduck_id', c.get('spaceduck_id', '?'))))
    def _since(c):
        return c.get('connected_at', c.get('approved_at', c.get('created_at', '')))

    # ── --pending short-circuits (output contract unchanged) ──
    if pending_only:
        if as_json:
            print(json.dumps(pending, indent=2, default=str))
            return
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

    # Dedup candidate rows by peer SDID (keep newest) and drop self-references.
    # Server returns one row per peck event, so the same peer can appear many
    # times; collapse to one line per peer. A row whose peer is THIS duck is a
    # stale self-referential record and is hidden here (matches --pending).
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
    dup_dropped = max(0, len(connected) - len(unique) - self_refs)

    # Peer name/tier/since lookup from the candidate rows (used to enrich the
    # authoritative bulk-bond list, which carries only ids + perms).
    name_by_peer, tier_by_peer, since_by_peer = {}, {}, {}
    for c in all_pecks:
        pid = _peer_id(c)
        if not pid or pid == '?':
            continue
        if pid not in since_by_peer or (_since(c) or '') >= (since_by_peer.get(pid) or ''):
            name_by_peer[pid]  = c.get('peer_name', c.get('agent_name', c.get('display_name', pid)))
            tier_by_peer[pid]  = c.get('peer_tier', c.get('trust_tier', '?'))
            since_by_peer[pid] = _since(c)

    # SKILL-095: prefer the ONE-CALL authoritative bond list. If the server
    # supports GET /beak/connections/bonded (200), the bonds come straight from
    # it — no per-target probing. On 404/error (older server) OR --no-verify,
    # fall back to the per-target verify path below unchanged.
    source = 'per-target'
    bulk_status, bulk_rows = ('skip', [])
    if verify:
        bulk_status, bulk_rows = fetch_bonded_bulk(api, cfg)

    if verify and bulk_status == 'ok':
        source = 'bulk'
        bonded, notb = [], []
        bonded_ids = set()
        for row in bulk_rows:
            pid = row.get('peer_id') or row.get('spaceduck_id') or ''
            # Boss patch (SKILL-095 review): dedup by PEER — the table holds
            # duplicate connection rows per peer (rotation/legacy dupes) and
            # the endpoint returns every row; show each peer once, first row
            # wins (matches per-target first-match behavior).
            if not pid or pid in bonded_ids:
                continue
            bonded_ids.add(pid)
            perms = row.get('permissions', {}) or {}
            bonded.append({
                'peer_id':       pid,
                'peer_name':     name_by_peer.get(pid, pid),
                'peer_tier':     tier_by_peer.get(pid, '?'),
                'status':        row.get('status', ''),
                'direction':     'unknown',
                'since':         since_by_peer.get(pid, ''),
                'verified':      True,
                'connection_id': row.get('connection_id', ''),
                'shared_files':  row.get('shared_files', []),
                'caps': {
                    'rate_per_hour': perms.get('rate_limit_per_hour'),
                    'daily_limit':   perms.get('daily_limit'),
                    'min_tier':      perms.get('block_below_tier'),
                },
                'reason': '',
            })
        # Roster: candidates alive in the directory but NOT in the
        # authoritative bond set → shown ⚪, never 🟢.
        for c in unique:
            pid = _peer_id(c)
            if pid in bonded_ids:
                continue
            notb.append({
                'peer_id':   pid,
                'peer_name': name_by_peer.get(pid, pid),
                'peer_tier': tier_by_peer.get(pid, '?'),
                'status':    c.get('status', ''),
                'direction': _dir(c),
                'since':     since_by_peer.get(pid, ''),
                'verified':  False,
                'reason':    'not bonded (authoritative bond list)',
            })
    else:
        # VERIFY each candidate against the authoritative per-target bond
        # endpoint. 200 => real bond (🟢); 404 => roster only, NOT bonded;
        # error => unverified. --no-verify skips the probe: every candidate is
        # then flagged unverified and NONE gets a 🟢 (we never assert a bond we
        # haven't confirmed). Probes are capped at MAX_VERIFY.
        results = []
        probed = 0
        for c in unique:
            pid = _peer_id(c)
            entry = {
                'peer_id':   pid,
                'peer_name': c.get('peer_name', c.get('agent_name', c.get('display_name', pid))),
                'peer_tier': c.get('peer_tier', c.get('trust_tier', '?')),
                'status':    c.get('status', ''),
                'direction': _dir(c),
                'since':     _since(c),
                'verified':  False,
                'reason':    '',
            }
            if not verify:
                entry['reason'] = 'unverified (--no-verify)'
            elif probed >= MAX_VERIFY:
                entry['reason'] = f'unverified (probe cap {MAX_VERIFY} reached)'
            else:
                verdict, detail = verify_bond(api, cfg, pid)
                probed += 1
                if verdict == 'bonded':
                    entry['verified'] = True
                    entry['connection_id'] = detail.get('connection_id', '')
                    perms = detail.get('permissions', {}) or {}
                    entry['caps'] = {
                        'rate_per_hour': perms.get('rate_limit_per_hour'),
                        'daily_limit':   perms.get('daily_limit'),
                        'min_tier':      perms.get('block_below_tier'),
                    }
                elif verdict == 'not_bonded':
                    entry['reason'] = 'not bonded (server 404 — roster/pending only)'
                else:
                    entry['reason'] = 'unverified (bond endpoint unreachable)'
            results.append(entry)

        bonded = [e for e in results if e['verified']]
        notb   = [e for e in results if not e['verified']]

    if as_json:
        print(json.dumps({
            'spaceduck_id':         sdid,
            'verified':             verify,
            'source':               source,   # 'bulk' (one-call) | 'per-target' | 'per-target' (no-verify)
            'bonded':               bonded,
            'not_bonded':           notb,
            'pending':              pending,
            'self_refs_hidden':     self_refs,
            'duplicates_collapsed': dup_dropped,
            'connected':            bonded,   # back-compat key (now = verified bonds only)
        }, indent=2, default=str))
        return

    # ── Human output ──
    print(f'🔗 Connections for duck {cfg.get("agent_name","?")} ({sdid})')
    print()

    if bonded:
        print(f'  Bonded connections — {len(bonded)} (verified against the bond endpoint):')
        for e in bonded:
            print(f"  🟢 {e['peer_name']}  (ID: {e['peer_id']}  |  Tier: {e['peer_tier']})")
            if e.get('connection_id'):
                print(f"       Connection: {e['connection_id']}")
            caps = e.get('caps') or {}
            if caps.get('rate_per_hour') is not None or caps.get('daily_limit') is not None:
                print(f"       Caps: {caps.get('rate_per_hour', '?')}/hr, "
                      f"{caps.get('daily_limit', '?')}/day, "
                      f"min tier {caps.get('min_tier', 'T0')}")
            if e.get('since'):
                print(f"       Since: {e['since']}")
            print(f"       View: https://spaceduckling.com/explore.html?duck={e['peer_id']}")
            print()
    else:
        print('  Bonded connections — none.')
        print(f'  → Explore ducks to peck: https://spaceduckling.com/explore.html')
        print()

    if notb:
        label = ('Pond roster — alive but NOT bonded' if verify
                 else 'Candidates — status-qualified, NOT verified (drop --no-verify to confirm)')
        print(f'  {label} — {len(notb)} '
              f'(NOT connections; you cannot peck these until a bond exists):')
        for e in notb:
            print(f"  ⚪ {e['peer_name']}  (ID: {e['peer_id']})  — {e['reason'] or 'not bonded'}")
        print(f'     → to bond, send a Pond connection request '
              f'(see references/CONNECTION-CEREMONY.md)')
        print()

    if dup_dropped:
        print(f'  ({dup_dropped} duplicate row(s) collapsed)')
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
    verify       = '--no-verify' not in sys.argv
    list_connections(cfg, pending_only=pending_only, as_json=as_json, verify=verify)
