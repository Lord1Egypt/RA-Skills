#!/usr/bin/env python3
"""
Space Duck — Review and respond to pending peck (connection) requests.

INTENT: List incoming peck requests; approve or deny one by peck_id.
CALLS:  POST <api>/beak/spaceducks       (list pending records)
        POST <api>/beak/peck/approve     (approve / reject by peck_id)
        Space Duck's own backend only — no third-party hosts.
AUTH:   Beak Key from ~/.space-duck/config.json, sent only to the Space
        Duck backend.

Usage: python3 check_pecks.py
       python3 check_pecks.py --approve <peck_id>
       python3 check_pecks.py --deny <peck_id>
"""
import json, sys, urllib.request, urllib.error
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'
API_BASE = 'https://beak.spaceduckling.com'

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())

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

if __name__ == '__main__':
    cfg = load_config()
    if '--approve' in sys.argv:
        pid = sys.argv[sys.argv.index('--approve') + 1]
        print(json.dumps(approve(cfg, pid), indent=2, default=str))
    elif '--deny' in sys.argv:
        pid = sys.argv[sys.argv.index('--deny') + 1]
        print(json.dumps(deny(cfg, pid), indent=2, default=str))
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
