#!/usr/bin/env python3
"""
Space Duck — Review and respond to pending peck (connection) requests.

INTENT: List incoming peck requests; approve or deny one by peck_id.
CALLS:  POST <api>/beak/spaceducks           (list pending records)
        POST <api>/beak/peck/approve         (approve / reject by peck_id)
        GET  <api>/beak/peck/<id>/status     (delivery state — [DELIVERY-A])
        Space Duck's own backend only — no third-party hosts.
AUTH:   Beak Key from ~/.space-duck/config.json, sent only to the Space
        Duck backend.

Usage: python3 check_pecks.py
       python3 check_pecks.py --approve <peck_id>
       python3 check_pecks.py --deny <peck_id>
       python3 check_pecks.py --status <peck_id>
"""
import json, sys, urllib.request, urllib.error, urllib.parse
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'
API_BASE = 'https://beak.spaceduckling.com'

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    cfg = json.loads(CONFIG_PATH.read_text())
    from _apiguard import check_api_base  # [HARDEN-071]
    check_api_base(cfg)
    return cfg

def _direction(p, did, sdid):
    """Server-provided direction (v474+) with legacy fallback."""
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

def check_pending(cfg):
    did  = cfg.get('duckling_id', '')
    sdid = cfg.get('spaceduck_id', '')
    if not did:
        print('ERROR: duckling_id missing from config. Re-run setup.py.')
        return []
    payload = json.dumps({'duckling_id': did}).encode()
    req = urllib.request.Request(
        f"{API_BASE}/beak/spaceducks",
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        all_records = data.get('connections', data.get('pecks', []))
        pending = [p for p in all_records if str(p.get('status', '')).lower() in ('pending', 'requested')]
        if not pending:
            print('[pecks] No pending connection requests.')
            return []

        inbound  = [p for p in pending if _direction(p, did, sdid) == 'inbound']
        outbound = [p for p in pending if _direction(p, did, sdid) == 'outbound']
        stale    = [p for p in pending if _direction(p, did, sdid) == 'self']
        unknown  = [p for p in pending if _direction(p, did, sdid) == 'unknown']

        if inbound:
            print(f'[pecks] {len(inbound)} inbound request(s) you can approve:')
            for p in inbound:
                pid     = p.get('peck_id', p.get('connection_id', '?'))
                rname   = p.get('peer_name', p.get('requester_name', p.get('agent_name', p.get('requester_id', p.get('peer_id', '?')))))
                purpose = p.get('purpose', '?')
                print(f"  • {pid} from {rname} — {purpose}")
        else:
            print('[pecks] No inbound requests to approve.')

        if outbound:
            print(f'[pecks] {len(outbound)} outbound request(s) awaiting peer (no action):')
            for p in outbound:
                pid   = p.get('peck_id', p.get('connection_id', '?'))
                rname = p.get('peer_name', p.get('agent_name', p.get('peer_id', '?')))
                print(f"  • {pid} → {rname}")

        if stale:
            print(f'[pecks] {len(stale)} stale self-referential record(s); ignore.')

        if unknown:
            print(f'[pecks] {len(unknown)} record(s) with unknown direction; inspect with connections.py --pending --json.')

        # Only inbound is actionable — return the rest so callers that consume
        # this list (older tooling) don't try to approve outbound/self records.
        return inbound
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"[pecks] HTTP {e.code}: {body}")
        return []
    except Exception as e:
        print(f"[pecks] Error: {e}")
        return []

def _decide(cfg, peck_id, action):
    """action: 'approve' | 'reject'  (server validates these only)."""
    payload = json.dumps({
        'peck_id':   peck_id,
        'beak_key':  cfg['beak_key'],
        'action':    action,
    }).encode()
    req = urllib.request.Request(
        f"{API_BASE}/beak/peck/approve",
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def approve(cfg, peck_id):
    return _decide(cfg, peck_id, 'approve')

def deny(cfg, peck_id):
    return _decide(cfg, peck_id, 'reject')

def grant_status(cfg, target_sd, capability='send_peck', scope=None):
    """Poll whether a capability grant to `target_sd` is live yet.
    Uses /beak/grants/check (Lane A surface) with dry_run=true — beak-key
    auth via `Authorization: Bearer`, no usage increment. This is the
    sender-agent's poll path after send_peck.py self-requests a grant; the
    owner-side /beak/grant-requests listing is Cognito-auth (owner only) and
    not callable with a beak key. Returns the parsed dict.

    Scope MUST match the grant's scope exactly (server does string equality).
    send_peck grants are scoped `to:<recipient_sdid>` — mirror the enforcement
    check at lambda_v8.py send_peck path — so default to that for send_peck."""
    if scope is None:
        scope = f'to:{target_sd}' if capability == 'send_peck' else ''
    body = json.dumps({
        'recipient_spaceduck_id': target_sd,
        'capability': capability,
        'scope': scope,
        'dry_run': True,
    }).encode()
    req = urllib.request.Request(
        f"{API_BASE}/beak/grants/check",
        data=body, method='POST',
        headers={'Content-Type': 'application/json',
                 'Authorization': f"Bearer {cfg['beak_key']}"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def delivery_status(cfg, peck_id):
    """[DELIVERY-A 2026-10-19] GET /beak/peck/<peck_id>/status.

    docs/spec/OPENHARNESS-ADOPTION.md §5.4 rule 3. Answers "what actually
    happened to that peck" AFTER the send call returned — which nothing
    could before, because the only delivery signal was the send response's
    `channels` list, and that always contains 'quack' (the platform's own
    write counted as a channel).

    Readable by either end of the peck; authenticated with the beak key,
    same as every other call in this script. Returns the parsed body, or a
    dict with an `error` key — never raises, so the CLI can print a
    sensible line against an older Lambda that has no such route.
    """
    pid = str(peck_id or '').strip()
    if not pid:
        return {'error': 'peck_id_required'}
    req = urllib.request.Request(
        f"{API_BASE}/beak/peck/{urllib.parse.quote(pid)}/status",
        headers={'X-Beak-Key': cfg.get('beak_key', '')},
        method='GET',
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            out = json.loads(e.read())
        except Exception:
            out = {}
        if e.code == 404:
            # Could be either "no such peck" or a Lambda that predates the
            # route. Say both rather than guessing.
            out.setdefault('error', 'not_found')
            out['hint'] = ('no such peck for this duck, or this platform '
                           'version has no /status route yet')
        out.setdefault('error', f'http_{e.code}')
        out['http_status'] = e.code
        return out
    except Exception as e:
        return {'error': 'request_failed', 'detail': str(e)[:160]}


def print_delivery_status(res):
    """Render delivery_status() for a human. Returns a shell exit code:
    0 delivered, 3 still in flight / held, 4 failed, 2 lookup problem."""
    if res.get('error'):
        print(f'ERROR: {res["error"]}'
              + (f' — {res["hint"]}' if res.get('hint') else '')
              + (f' ({res["detail"]})' if res.get('detail') else ''))
        return 2
    state = str(res.get('delivery_state') or '?')
    print(f'peck {res.get("peck_id", "?")}')
    print(f'  state:    {state}')
    if res.get('delivery_reason'):
        print(f'  reason:   {res["delivery_reason"]}')
    if res.get('required_capability'):
        print(f'  requires: {res["required_capability"]}')
    legs = res.get('legs') or {}
    if legs:
        print('  legs:     '
              + ', '.join(f'{k}={v}' for k, v in sorted(legs.items())))
    if res.get('channels'):
        print(f'  channels: {", ".join(str(c) for c in res["channels"])}')
    # delivery_state_stored differs from delivery_state for pre-Phase-A
    # rows (pushed/acked), which the platform normalises on read.
    stored = str(res.get('delivery_state_stored') or '')
    if stored and stored != state:
        print(f'  (stored as "{stored}" — legacy row, mapped on read)')
    if state == 'delivered':
        print('  ✅ the recipient runtime acknowledged this peck.')
        return 0
    if state.startswith('failed:'):
        print('  ❌ terminal failure. The peck will not be delivered as-is.')
        return 4
    if state.startswith('held:'):
        print('  ⏳ stored and collectable — the recipient has not taken it '
              'yet. Not lost.')
        return 3
    if state.startswith('pushed_unconfirmed'):
        print('  ⏳ pushed, but the recipient runtime has not acknowledged.')
        return 3
    return 3


def nudge_expiring_grants(cfg):
    """0.9.1 [PERMS-B item 2] — once-per-window nudge for active OUTBOUND
    send_peck grants nearing expiry. Iterates connected peers, best-effort
    reads each grant's expiry via /beak/grants/check (dry_run), and prints ONE
    nudge per grant per expiry window (de-duped in
    ~/.space-duck/expiry_nudges.json, keyed by grant_id+window).

    FAIL-OPEN: no expiry signal from the server (today's reality — the endpoint
    does not yet return expires_at) → prints nothing. Never raises, never
    blocks the primary check_pending output."""
    try:
        import _grant_meta
    except Exception:
        return
    did = cfg.get('duckling_id', '')
    sdid = (cfg.get('spaceduck_id', '') or '').upper()
    if not did:
        return
    try:
        payload = json.dumps({'duckling_id': did}).encode()
        req = urllib.request.Request(
            f"{API_BASE}/beak/spaceducks", data=payload,
            headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
    except Exception:
        return
    records = data.get('connections', data.get('pecks', [])) or []
    peers, seen = [], set()
    for c in records:
        # Only established connections have an active grant to warn about.
        if str(c.get('status', '')).lower() not in (
                'active', 'connected', 'approved', 'flock', 'bound',
                'bonded', 'bond'):
            continue
        # We are the sender; any connected peer is a candidate recipient.
        pid = (c.get('peer_id') or c.get('target_spaceduck_id')
               or c.get('requester_spaceduck_id') or c.get('spaceduck_id') or '')
        pid = (pid or '').upper()
        if pid and pid != sdid and pid not in seen:
            seen.add(pid)
            peers.append(pid)
    if not peers:
        return
    # Cost guard: bound the sweep on large flocks (oldest-connection peers
    # beyond the cap wait for the next run — nudges are advisory, not urgent).
    peers = peers[:25]
    state = _grant_meta.load_nudges()
    changed = False
    for pid in peers:
        resp = _grant_meta.fetch_grant_check(cfg, pid, 'send_peck')
        if resp is None:
            continue
        # Capability probe: an allow-response WITHOUT expires_at means the
        # server doesn't surface grant expiry yet (today's prod) — stop the
        # sweep instead of burning one dry-run call + audit row per peer.
        if resp.get('allowed') is True and 'expires_at' not in resp:
            break
        msg, new_state = _grant_meta.evaluate_nudge(resp, pid, state)
        if msg:
            print(f'[grants] {msg}')
            state = new_state
            changed = True
    if changed:
        _grant_meta.save_nudges(state)


if __name__ == '__main__':
    cfg = load_config()
    if '--approve' in sys.argv:
        pid = sys.argv[sys.argv.index('--approve') + 1]
        print(json.dumps(approve(cfg, pid), indent=2, default=str))
    elif '--deny' in sys.argv:
        pid = sys.argv[sys.argv.index('--deny') + 1]
        print(json.dumps(deny(cfg, pid), indent=2, default=str))
    elif '--status' in sys.argv:
        # [DELIVERY-A 2026-10-19] spec §5.4 rule 3 — sender-visible delivery
        # state. `in` on argv is exact-element matching, so this does not
        # collide with the --grant-status branch below.
        i = sys.argv.index('--status')
        pid = sys.argv[i + 1] if i + 1 < len(sys.argv) else ''
        if not pid or pid.startswith('-'):
            print('Usage: check_pecks.py --status <peck_id>')
            sys.exit(2)
        sys.exit(print_delivery_status(delivery_status(cfg, pid)))
    elif '--grant-status' in sys.argv:
        i = sys.argv.index('--grant-status')
        target = sys.argv[i + 1] if i + 1 < len(sys.argv) else ''
        cap = sys.argv[i + 2] if i + 2 < len(sys.argv) and not sys.argv[i + 2].startswith('-') else 'send_peck'
        if not target:
            print('Usage: check_pecks.py --grant-status <target_sdid> [capability]')
            sys.exit(2)
        res = grant_status(cfg, target, cap)
        allowed = res.get('allowed')
        if allowed is True:
            print(f'✅ Grant ACTIVE for "{cap}" → {target}. send_peck will go through.')
            sys.exit(0)
        print(f'⏳ Not yet — "{cap}" → {target}: {res.get("reason", "pending owner approval")}')
        sys.exit(3)
    else:
        check_pending(cfg)
        nudge_expiring_grants(cfg)
