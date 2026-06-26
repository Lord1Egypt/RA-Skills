#!/usr/bin/env python3
"""
Space Duck — Multi-turn chat (peck_session) with another connected duck.

INTENT: Maintain a continuing conversation with one peer using the
        backend's peck_session machinery (rate / daily / budget gated).
CALLS:  POST <api>/beak/agent/message    — send one round (signed HMAC-SHA256)
        GET  <api>/beak/peck/session     — read session state
        POST <api>/beak/peck/stop        — end an open session
AUTH:   Beak Key from ~/.space-duck/config.json (chmod 600).
HMAC:   Phase E v2 envelope (BRIEF v0.1.7 §E). Signature =
        HMAC-SHA256(beak_key, canonical_v2_json) over 8 canonical fields:
        from_spaceduck_id, to_spaceduck_id, conversation_id, turn_index,
        intent, scopes_asserted (sorted), timestamp, message_hash. For
        multi-turn, conversation_id = session_id and turn_index = round.
        Legacy v1 sunsets 2026-06-05.

A peck_session is created automatically on round 0 — the server returns a
session_id that subsequent rounds reference via conversation_id /
_peck_session_id. Use --show to inspect; --stop to terminate.

Usage:
  # Start a new conversation (round 0)
  python3 chat.py --to <spaceduck_id> --message "Got a minute?" \
      [--goal "design review"] [--max-rounds 10]

  # Continue an existing session (round N)
  python3 chat.py --session <PS-id> --message "Follow-up question"

  # Inspect session state
  python3 chat.py --show <PS-id>

  # Stop a session
  python3 chat.py --stop <PS-id>
"""
import argparse, hashlib, hmac, json, re, secrets, sys, time
import urllib.error, urllib.parse, urllib.request
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'
SDID_RE = re.compile(r'^[0-9A-Fa-f]{16}$')

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())

def resolve_target(cfg, name_or_sdid):
    """BRIEF v0.1.7 §G — name→SDID resolver. See send_peck.py for full notes."""
    s = (name_or_sdid or '').strip()
    if SDID_RE.match(s):
        return s.upper()
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    did = cfg.get('duckling_id', '')
    if not did:
        print(f'ERROR: cannot resolve "{s}" — duckling_id missing from config.')
        sys.exit(1)
    try:
        req = urllib.request.Request(
            f'{api}/beak/spaceducks',
            data=json.dumps({'duckling_id': did}).encode(),
            headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
    except Exception as e:
        print(f'ERROR: contact lookup failed: {e}'); sys.exit(1)
    needle = s.lower()
    candidates = []
    for c in data.get('connections', data.get('pecks', [])):
        peer_id = (c.get('peer_id') or c.get('requester_spaceduck_id')
                   or c.get('target_spaceduck_id') or c.get('spaceduck_id') or '')
        peer_name = (c.get('peer_name') or c.get('agent_name')
                     or c.get('display_name') or '')
        if peer_name and peer_name.lower() == needle:
            return peer_id.upper()
        if peer_name and needle in peer_name.lower():
            candidates.append((peer_name, peer_id))
    if len(candidates) == 1:
        return candidates[0][1].upper()
    if not candidates:
        print(f'ERROR: no connected duck named "{s}". Run connections.py to list peers.')
    else:
        print(f'ERROR: "{s}" matches multiple ducks — please use the SDID:')
        for n, i in candidates: print(f'  • {n} ({i})')
    sys.exit(1)

def _v2_canonical(env):
    """Server-matched canonical JSON for the Phase E envelope."""
    canonical = {
        'from_spaceduck_id': str(env.get('from_spaceduck_id', '')),
        'to_spaceduck_id':   str(env.get('to_spaceduck_id', '')),
        'conversation_id':   str(env.get('conversation_id', '')),
        'turn_index':        int(env.get('turn_index', 0) or 0),
        'intent':            str(env.get('intent', '')),
        'scopes_asserted':   sorted(env.get('scopes_asserted') or []),
        'timestamp':         int(env.get('timestamp', 0) or 0),
        'message_hash':      str(env.get('message_hash', '')),
    }
    return json.dumps(canonical, sort_keys=True, separators=(',', ':'))

def _v2_sign(env, beak_key):
    return hmac.new(beak_key.encode(), _v2_canonical(env).encode(), hashlib.sha256).hexdigest()

def _preflight_permissions(cfg, target_id):
    """Pre-flight read of /beak/connection/permissions before round 0.

    Surfaces caps BEFORE we open a session so a rate-limited / disabled
    connection fails with a friendly message instead of a generic 403.
    Server-side enforcement is still the source of truth; this is UX.
    Returns (proceed: bool, summary: str). Never raises — soft on errors.
    """
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    sdid = cfg.get('spaceduck_id', '')
    bk = cfg.get('beak_key', '')
    if not (api and sdid and bk):
        return True, ''
    body = json.dumps({'spaceduck_id': sdid, 'target_id': target_id}).encode()
    headers = {'Content-Type': 'application/json',
               'X-Beak-Key': bk,
               'X-Spaceduck-ID': sdid}
    try:
        req = urllib.request.Request(
            f'{api}/beak/connection/permissions',
            data=body, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return True, '(no connection record yet — server will gate)'
        return True, f'(pre-flight: HTTP {e.code} — server will gate)'
    except Exception:
        return True, '(pre-flight unavailable — server will gate)'
    perms = (data or {}).get('permissions', {}) or {}
    rate = perms.get('rate_limit_per_hour', 10)
    daily = perms.get('daily_limit', 50)
    budget = perms.get('daily_budget_usd', 0.0) or 0.0
    cooldown = perms.get('cooldown_minutes', 5)
    tier_floor = perms.get('block_below_tier', 'T0')
    bt = perms.get('blocked_topics') or []
    # 2026-05-17 — agent-to-agent mute (server also enforces; this is UX).
    muted_until = int(perms.get('muted_until') or 0)
    if muted_until > int(time.time()):
        return False, (f'peer is muted until epoch {muted_until}. '
                       'Run `permissions.py --target ' + target_id + ' --set muted_until=0` to unmute.')
    if int(rate or 0) == 0:
        return False, ('peer has disabled pecks from you (rate_limit_per_hour=0). '
                       'Run `permissions.py --target ' + target_id + '` to see.')
    if int(daily or 0) == 0:
        return False, ('peer has disabled pecks from you today (daily_limit=0). '
                       'Run `permissions.py --target ' + target_id + '` to see.')
    parts = [f'{rate}/hr', f'{daily}/day']
    if budget > 0:
        parts.append(f'${budget:.2f}/day')
    parts.append(f'{cooldown}min cooldown')
    if tier_floor and tier_floor != 'T0':
        parts.append(f'min tier {tier_floor}')
    if bt:
        parts.append(f'{len(bt)} blocked topic(s)')
    return True, '🔒 caps: ' + ', '.join(parts)

def _post(url, payload):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def _get(url):
    req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def _http_err(e, hint=None):
    body = e.read().decode()
    print(f'ERROR: HTTP {e.code} — {body}')
    if hint:
        print(f'  Hint: {hint}')
    sys.exit(1)

def send_round(cfg, target_id, message, session_id=None, goal=None,
               max_rounds=10, peck_type='query', turn_index=0,
               skip_preflight=False):
    api  = cfg.get('api_base', 'https://beak.spaceduckling.com')
    sdid = cfg.get('spaceduck_id', '')
    bk   = cfg.get('beak_key', '')
    if not sdid or not bk:
        print('ERROR: spaceduck_id or beak_key missing from config.')
        sys.exit(1)

    # Round-0 only: pre-flight the connection's permissions. On continuation
    # rounds we already passed pre-flight when the session opened, and the
    # per-connection caps don't re-gate session continuation (the session
    # itself is gated by max_rounds + tier ceiling, checked separately).
    if not skip_preflight and not session_id:
        proceed, summary = _preflight_permissions(cfg, target_id)
        if summary:
            print(f'   {summary}')
        if not proceed:
            print(f'❌ Pre-flight blocked: {summary}')
            sys.exit(3)

    peck_id      = 'peck_' + secrets.token_urlsafe(12)
    timestamp    = int(time.time())
    message_hash = hashlib.sha256(message.encode()).hexdigest()

    # Multi-turn: conversation_id = real session_id, turn_index = current round.
    # Round 0 (no session yet): conversation_id = peck_id, turn_index = 0.
    conv_id = session_id or peck_id
    env_v2 = {
        'from_spaceduck_id': sdid,
        'to_spaceduck_id':   target_id,
        'conversation_id':   conv_id,
        'turn_index':        int(turn_index),
        'intent':            peck_type,
        'scopes_asserted':   [],
        'timestamp':          timestamp,
        'message_hash':       message_hash,
    }
    signature = _v2_sign(env_v2, bk)

    payload = {
        'envelope_version':     '2',
        'sender_spaceduck_id':  sdid,
        'beak_key':             bk,
        'target_spaceduck_id':  target_id,
        'message':              message,
        'message_hash':         message_hash,
        'peck_type':            peck_type,
        'peck_id':              peck_id,
        'conversation_id':      conv_id,
        'turn_index':           int(turn_index),
        'intent':               peck_type,
        'scopes_asserted':      [],
        'timestamp':            timestamp,
        'signature':            signature,
        '_peck_max_rounds':     max_rounds,
    }
    if session_id:
        payload['_peck_session_id'] = session_id
    if goal:
        payload['goal'] = goal

    try:
        resp = _post(f'{api}/beak/agent/message', payload)
    except urllib.error.HTTPError as e:
        # 2026-05-17 — surface the specific new error codes the server now returns.
        try: _body = json.loads(e.read())
        except Exception: _body = {}
        _err = _body.get('error', '')
        if e.code == 403 and _err == 'connection_muted':
            print(f'ERROR: connection muted until epoch {_body.get("muted_until",0)}')
            print(f'  Run: permissions.py --target {target_id} --set muted_until=0')
            sys.exit(4)
        if e.code == 429 and _err == 'human_daily_budget_exceeded':
            print(f'ERROR: your daily peck-cost cap was reached.')
            print(f'  cap=${_body.get("budget_usd",0):.2f} · today=~${_body.get("estimated_cost_usd",0):.4f}')
            print('  All your ducks pause outbound pecks until midnight UTC.')
            sys.exit(5)
        if e.code == 429 and _err == 'rate_limited':
            print(f'ERROR: per-pair rate limit ({_body.get("reason","?")}). Retry in {_body.get("retry_after_seconds","?")}s.')
            sys.exit(6)
        if e.code == 403:
            _http_err(e, hint='peck blocked — target may not be peck\'d to you, '
                              'or rate/daily/budget limit reached. Check '
                              'permissions.py to see gating.')
        _http_err(e)
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit(1)

    sid = resp.get('session_id') or resp.get('_peck_session_id') or session_id or '(new)'
    print(f'✅ Round delivered to {target_id}')
    print(f'   Peck ID: {peck_id}')
    print(f'   Session: {sid}')
    if 'channels' in resp:
        print(f'   Channels: {", ".join(resp["channels"])}')
    print()
    print('  → Continue:  python3 chat.py --session %s --message "..."' % sid)
    print('  → Inspect:   python3 chat.py --show %s' % sid)
    print('  → Stop:      python3 chat.py --stop %s' % sid)
    return resp

def show_session(cfg, session_id):
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    qs  = urllib.parse.urlencode({'session_id': session_id})
    try:
        data = _get(f'{api}/beak/peck/session?{qs}')
    except urllib.error.HTTPError as e:
        _http_err(e)
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit(1)

    print(f'💬 Session {data.get("session_id", session_id)}')
    print(f'   Status:    {data.get("status", "?")}')
    print(f'   Round:     {data.get("current_round", 0)} / {data.get("max_rounds", "?")}')
    print(f'   Initiator: {data.get("initiator", "?")}')
    print(f'   Target:    {data.get("target", "?")}')
    if data.get('goal'):
        print(f'   Goal:      {data["goal"]}')
    if data.get('cost_usd') is not None:
        print(f'   Cost:      ${data["cost_usd"]:.4f}  '
              f'(in: {data.get("tokens_in", 0)}, out: {data.get("tokens_out", 0)})')
    if data.get('flock_task_id'):
        print(f'   Flock:     {data["flock_task_id"]}')
    return data

def stop_session(cfg, session_id):
    api  = cfg.get('api_base', 'https://beak.spaceduckling.com')
    sdid = cfg.get('spaceduck_id', '')
    bk   = cfg.get('beak_key', '')
    payload = {'session_id': session_id, 'spaceduck_id': sdid, 'beak_key': bk}
    try:
        resp = _post(f'{api}/beak/peck/stop', payload)
    except urllib.error.HTTPError as e:
        _http_err(e)
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit(1)
    print(f'🛑 Session {session_id} stopped.')
    return resp

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Multi-turn chat over peck_session')
    p.add_argument('--to', metavar='SPACEDUCK_ID', help='Target duck (for round 0)')
    p.add_argument('--session', metavar='PS_ID', help='Continue an existing session')
    p.add_argument('--message', '-m', help='Message to send this round')
    p.add_argument('--goal', help='Optional goal label (round 0 only)')
    p.add_argument('--max-rounds', type=int, default=10, help='Cap on rounds (default 10)')
    p.add_argument('--peck-type', default='query',
                   choices=['notify', 'query', 'data_request', 'task_delegation'])
    p.add_argument('--show', metavar='PS_ID', help='Show session state and exit')
    p.add_argument('--stop', metavar='PS_ID', help='Stop an open session and exit')
    p.add_argument('--skip-preflight', action='store_true',
                   help='Bypass /beak/connection/permissions pre-flight check (round 0 only).')
    args = p.parse_args()

    cfg = load_config()

    if args.show:
        show_session(cfg, args.show); sys.exit(0)
    if args.stop:
        stop_session(cfg, args.stop); sys.exit(0)

    if not args.message:
        p.error('--message is required (unless --show / --stop)')
    if args.session:
        # The backend pulls target from the session; we still need a target
        # field + turn_index in the signed v2 envelope. Resolve via session lookup.
        sess = show_session(cfg, args.session)
        target = sess.get('target') or sess.get('initiator') or ''
        if not target:
            print('ERROR: could not resolve target from session.')
            sys.exit(1)
        # Refuse to send if the session is closed or already at its turn cap.
        # Tier-based caps (Free=0, Standard=1, Pro=50) are enforced server-side
        # in _peck_session_guard(); we check locally so the user gets an
        # actionable message instead of a 403 after the round trip.
        status = (sess.get('status') or '').upper()
        if status and status != 'ACTIVE':
            print(f'❌ Session {args.session} is {status}. Open a new session with --to.')
            sys.exit(3)
        cur_round = int(sess.get('current_round', 0) or 0)
        cap = sess.get('max_rounds')
        cap_int = int(cap) if isinstance(cap, (int, float)) and cap else None
        if cap_int is not None and cur_round >= cap_int:
            print(f'❌ Session at cap: round {cur_round}/{cap_int}. '
                  f'Stop it (--stop {args.session}) or open a fresh session with --to.')
            sys.exit(3)
        if cap_int is not None and cur_round >= cap_int - 1:
            print(f'⚠️  Last round before cap: {cur_round + 1}/{cap_int}.')
        next_turn = cur_round
        send_round(cfg, target, args.message, session_id=args.session,
                   max_rounds=args.max_rounds, peck_type=args.peck_type,
                   turn_index=next_turn, skip_preflight=args.skip_preflight)
    elif args.to:
        target_sdid = resolve_target(cfg, args.to)
        send_round(cfg, target_sdid, args.message, goal=args.goal,
                   max_rounds=args.max_rounds, peck_type=args.peck_type,
                   turn_index=0, skip_preflight=args.skip_preflight)
    else:
        p.error('--to (new) or --session (continue) is required')
