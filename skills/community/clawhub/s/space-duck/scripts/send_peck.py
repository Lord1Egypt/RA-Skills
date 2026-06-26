#!/usr/bin/env python3
"""
Space Duck — Send a peck (direct message) to another connected duck.

INTENT: Deliver a duck-to-duck message via the Space Duck network.
CALLS:  POST <api>/beak/agent/message — Space Duck's own backend only.
        No third-party hosts are ever contacted.
AUTH:   Beak Key is read from ~/.space-duck/config.json (chmod 600) and
        identifies this agent to the Space Duck backend.
HMAC:   Phase E v2 envelope (BRIEF v0.1.7 §E). Signature =
        HMAC-SHA256(beak_key, canonical_v2_json) over 8 canonical fields:
        from_spaceduck_id, to_spaceduck_id, conversation_id, turn_index,
        intent, scopes_asserted (sorted), timestamp, message_hash. The
        server reconstructs the same canonical form and compares.
        Legacy v1 (peck_id|target|ts|msg_hash) sunsets 2026-06-05.

Usage: python3 send_peck.py --to <spaceduck_id> --message "Hello" [--purpose "collab"]
"""
import argparse, hashlib, json, re, secrets, sys, time, urllib.error, urllib.request
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'
INBOX_DIR   = Path.home() / '.space-duck' / 'inbox'
SDID_RE = re.compile(r'^[0-9A-Fa-f]{16}$')

# B5 (2026-06-24): default round cap for an initial peck that opens a chain but
# doesn't declare its own. Guarantees peck_responder's deterministic terminator
# (current_round >= max_rounds) always engages, so the Jaccard novelty gate is a
# backstop rather than the sole stop. Round 1 = initial send; ~5 auto-replies
# before the cap trips. Override with --max-rounds.
DEFAULT_INITIAL_MAX_ROUNDS = 6

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())

def resolve_reply_to(peck_id):
    """Look up a stashed inbound envelope in ~/.space-duck/inbox/ and return
    the sender's SDID so the caller can reply without a roster round-trip.
    peck_listener.py persists every inbound peck JSON here (push + poll modes),
    so this is the cheapest "reply to whoever just pecked me" path — and it
    sidesteps the David-style bug where the local connections list is missing
    a peer that just messaged you.
    """
    pid = (peck_id or '').strip()
    if not pid:
        print('ERROR: --reply-to requires a peck_id.')
        sys.exit(1)
    path = INBOX_DIR / f'{pid}.json'
    if not path.exists():
        print(f'ERROR: no inbox record for {pid} at {path}.')
        print('  peck_listener.py writes inbound pecks here on receipt — '
              'if the file is missing, the listener may not have been '
              'running when this peck arrived.')
        sys.exit(1)
    try:
        env = json.loads(path.read_text())
    except Exception as e:
        print(f'ERROR: could not parse {path}: {e}')
        sys.exit(1)
    sender = (env.get('sender_spaceduck_id')
              or env.get('from_spaceduck_id')
              or env.get('requester_spaceduck_id')
              or '')
    if not sender:
        print(f'ERROR: {path} has no sender_spaceduck_id / from_spaceduck_id '
              '/ requester_spaceduck_id field.')
        sys.exit(1)
    if not SDID_RE.match(sender):
        print(f'ERROR: sender field "{sender}" in {path} is not a 16-hex SDID.')
        sys.exit(1)
    return sender.upper()


def resolve_target(cfg, name_or_sdid):
    """BRIEF v0.1.7 §G — name→SDID resolver. Pass-through if it's already a
    16-hex SDID; otherwise look up by display_name in the caller's connections.
    """
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
        print(f'ERROR: contact lookup failed: {e}')
        sys.exit(1)
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

# Make sibling-dir helpers importable when this script is invoked via an
# absolute path (e.g. `python3 /path/to/scripts/send_peck.py`). The user's
# CWD is not the scripts dir in that case, so a bare `from _envelope ...`
# wouldn't find it. We extend sys.path the standard way; no dynamic loader.
import pathlib as _pl
_script_dir = str(_pl.Path(__file__).resolve().parent)
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

# Envelope identity-attestation helper.
from _envelope import canonical_v2 as _v2_canonical, sign_v2 as _v2_sign

def _preflight_permissions(cfg, target_id):
    """Pre-flight read of /beak/connection/permissions. Surfaces caps BEFORE
    we hit the wire with a peck — so a rate-limited / disabled connection
    fails with a friendly message instead of a generic 403 after the round
    trip. Server-side enforcement is still the source of truth; this is UX.
    Returns (proceed: bool, summary: str). Never raises — soft on errors."""
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    sdid = cfg.get('spaceduck_id', '')
    bk = cfg.get('beak_key', '')
    if not (api and sdid and bk):
        return True, ''
    # 2026-05-17 — try the local preflight cache first (refreshed by sync.py pull).
    # Falls back to the live call only on cache miss. Saves a round-trip per peck
    # for typical interactive sessions.
    try:
        from _preflight import get_effective
        perms_cached = get_effective(target_id, cfg)
        if perms_cached:
            data = {'permissions': perms_cached}
        else:
            data = None
    except Exception:
        data = None
    if data is None:
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

def _request_grant(api, beak_key, recipient_sd, capability, scope, reason):
    """On a `grant_required` 403, ask the owner for permission.
    POST /beak/grants/request — beak-key auth via `Authorization: Bearer`
    (NOT X-Beak-Key). The server writes a pending grant_request row and
    notifies the owner (Mission Control inbox + push chain), or auto-approves
    when sender and recipient share an owner (intra-owner fast path).
    Returns the parsed JSON dict, or an error-tagged dict. Never raises —
    this is a best-effort recovery path."""
    body = json.dumps({
        'recipient_spaceduck_id': recipient_sd,
        'capability': capability,
        'scope': scope,
        'reason': (reason or '')[:200],
    }).encode()
    req = urllib.request.Request(
        f'{api}/beak/grants/request',
        data=body, method='POST',
        headers={'Content-Type': 'application/json',
                 'Authorization': f'Bearer {beak_key}'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return {'_http_error': e.code, **json.loads(e.read())}
        except Exception:
            return {'_http_error': e.code}
    except Exception as e:
        return {'_exception': str(e)}

def send_peck(cfg, target_id, message, purpose='connect', peck_type='notify',
              skip_preflight=False, tool_use=None, peck_meta=None,
              no_auto_grant=False):
    api  = cfg.get('api_base', 'https://beak.spaceduckling.com')
    sdid = cfg.get('spaceduck_id', '')
    bk   = cfg.get('beak_key', '')
    if not sdid or not bk:
        print('ERROR: spaceduck_id or beak_key missing from config.')
        sys.exit(1)

    if not skip_preflight:
        proceed, summary = _preflight_permissions(cfg, target_id)
        if summary:
            print(f'   {summary}')
        if not proceed:
            print(f'❌ Pre-flight blocked: {summary}')
            sys.exit(3)

    peck_id      = 'peck_' + secrets.token_urlsafe(12)
    timestamp    = int(time.time())
    message_hash = hashlib.sha256(message.encode()).hexdigest()

    # 0.4.0 Phase 1 (bugfix 2026-06-12 11:30) — auto-default root_peck_id to
    # the new peck_id when emitting v2 metadata without an explicit root.
    # The CLI help text promised this behavior; the original implementation
    # never wired it. Without root_peck_id propagating, receivers can't walk
    # _chain_history() and Phase 2 novelty scoring silently no-ops.
    if peck_meta and isinstance(peck_meta, dict) and peck_meta.get('protocol_version'):
        if not peck_meta.get('root_peck_id'):
            peck_meta = dict(peck_meta)
            peck_meta['root_peck_id'] = peck_id

    # Fresh peck (no real session): conversation_id = peck_id, turn_index = 0,
    # intent = peck_type, scopes_asserted = [].
    env_v2 = {
        'from_spaceduck_id': sdid,
        'to_spaceduck_id':   target_id,
        'conversation_id':   peck_id,
        'turn_index':        0,
        'intent':            peck_type,
        'scopes_asserted':   [],
        'timestamp':          timestamp,
        'message_hash':       message_hash,
    }
    signature = _v2_sign(env_v2, bk)

    _payload_dict = {
        'envelope_version':     '2',
        'sender_spaceduck_id':  sdid,
        'beak_key':             bk,
        'target_spaceduck_id':  target_id,
        'message':              message,
        'message_hash':         message_hash,
        'purpose':              purpose,
        'peck_type':            peck_type,
        'peck_id':              peck_id,
        'conversation_id':      peck_id,
        'turn_index':           0,
        'intent':               peck_type,
        'scopes_asserted':      [],
        'timestamp':            timestamp,
        'signature':            signature,
    }
    # Phase 5 — tool_use[] is signature-neutral (not in v2 HMAC scope).
    if tool_use:
        _payload_dict['tool_use'] = tool_use
    # 0.4.0 Phase 1 — peck protocol v2 metadata. Signature-neutral (not in
    # v2 HMAC scope). Receiver parses defensively via peck_responder
    # _parse_peck_meta(); absent or malformed falls back to v1 semantics.
    #
    # Top-level mirror policy: when peck_meta is supplied, we ALSO copy
    # protocol_version, session_id, root_peck_id, max_rounds, current_round
    # to top-level envelope fields. This lets v1 receivers (or v2 receivers
    # whose termination code path reads top-level — like the existing
    # _session_should_terminate) see the chain state without parsing meta.
    # peck_meta itself remains the canonical source for v2-native logic.
    if peck_meta and isinstance(peck_meta, dict):
        _payload_dict['peck_meta'] = peck_meta
        for _meta_k, _env_k in (('protocol_version', 'peck_protocol_version'),
                                ('session_id',       'session_id'),
                                ('root_peck_id',     'root_peck_id'),
                                ('max_rounds',       'max_rounds'),
                                ('current_round',    'current_round')):
            _v = peck_meta.get(_meta_k)
            if _v not in (None, ''):
                _payload_dict[_env_k] = _v
    payload = json.dumps(_payload_dict).encode()

    req = urllib.request.Request(
        f"{api}/beak/agent/message",
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            resp = json.loads(r.read())
        print(f'✅ Peck sent to {target_id}')
        print(f'   Peck ID: {peck_id}')
        status = resp.get('status', resp.get('message', 'sent'))
        print(f'   Status: {status}')
        # P1: surface real fan-out so the sender can tell whether the peck
        # actually reached a human surface, vs. only landing on the always-on
        # quack channel (which the recipient may never check).
        chans = resp.get('channels') or resp.get('delivered_channels') or []
        if not isinstance(chans, list):
            chans = [str(chans)]
        print(f'   Channels: {", ".join(chans) if chans else "NONE"}')
        if not chans or set(chans) <= {'quack'}:
            print('   Note: not fanned out to any bound human/agent surface — '
                  'target may not be peck\'d to you yet, or has no Telegram/'
                  'webhook channel bound. Awaiting approval is normal on '
                  'first contact.')
        # v0.4.7 — surface target's declared capabilities so the sender knows
        # whether to expect an auto-reply (or human-loop reply, or silence).
        tcaps = resp.get('target_capabilities') or []
        thint = resp.get('target_capability_hint')
        if isinstance(tcaps, list) and tcaps:
            print(f'   Target capabilities: {", ".join(tcaps)}')
            if 'auto_respond_peck' in tcaps:
                print('   → Target advertises auto-reply. Reply expected.')
        if thint:
            print(f'   ⚠ {thint}')
        return resp
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        # P5: the lambda now returns 400 wrong_id_type when the caller passed
        # a Duckling ID where an SDID was expected. Surface the resolved SDID
        # so the user can re-run without guessing.
        try:
            err_obj = json.loads(body)
        except Exception:
            err_obj = {}
        if e.code == 400 and err_obj.get('error') == 'wrong_id_type':
            print('ERROR: wrong identifier type.')
            print(f'  You passed:        {err_obj.get("supplied", target_id)}  (Duckling ID)')
            correct = err_obj.get('correct_spaceduck_id') or ''
            if correct:
                print(f'  Correct SDID:     {correct}')
                print(f'  Re-run with:       --to {correct}')
            else:
                print('  No SDID is registered for that Duckling ID yet.')
            sys.exit(2)
        # 2026-05-17 — surface specific new error codes the server can return.
        _err = err_obj.get('error', '')
        if e.code == 403 and _err == 'connection_muted':
            mu = err_obj.get('muted_until', 0)
            print(f'ERROR: connection is muted (muted_until={mu}).')
            print(f'  Run: permissions.py --target {target_id} --set muted_until=0')
            sys.exit(4)
        if e.code == 429 and _err == 'human_daily_budget_exceeded':
            print(f'ERROR: your daily peck-cost cap was reached.')
            print(f'  cap=${err_obj.get("budget_usd",0):.2f} · today=~${err_obj.get("estimated_cost_usd",0):.4f} · pecks={err_obj.get("pecks_today",0)}')
            print('  All your ducks pause outbound pecks until midnight UTC.')
            print('  Raise the cap in Mission Control → Daily Spend Cap card.')
            sys.exit(5)
        if e.code == 429 and _err == 'rate_limited':
            print(f'ERROR: per-pair rate limit ({err_obj.get("reason","?")}). Retry in {err_obj.get("retry_after_seconds","?")}s.')
            sys.exit(6)
        # 2026-06-24 — capability-grant recovery. The sender duck enforces
        # grants; this peck needs a `send_peck` grant the agent doesn't have
        # yet. Self-request one (owner still approves) instead of dead-ending
        # on a generic 403 + web fallback.
        if e.code == 403 and _err == 'grant_required':
            cap   = err_obj.get('capability', 'send_peck')
            scope = err_obj.get('scope', f'to:{target_id}')
            print(f'ERROR: grant required for "{cap}" → {target_id}.')
            print(f'  Reason: {err_obj.get("reason", "sender duck enforces capability grants")}')
            if no_auto_grant:
                print('  (--no-auto-grant set — not requesting automatically.)')
                print(f'  Web fallback: https://spaceduckling.com/explore.html?duck={target_id}')
                sys.exit(7)
            gr = _request_grant(api, bk, target_id, cap, scope,
                                reason=f'send_peck: {message[:80]}')
            if gr.get('auto_approved'):
                print(f'✅ Grant auto-approved (intra-owner) — grant_id={gr.get("grant_id")}.')
                print('   Re-run send_peck to deliver the message.')
                sys.exit(8)
            if gr.get('status') == 'pending' and gr.get('request_id'):
                print(f'🔔 Grant requested: {gr["request_id"]} — owner approval pending in Mission Control.')
                chans = gr.get('notification_channels') or []
                if chans:
                    print(f'   Owner notified via: {", ".join(chans)}')
                print(f'   Poll status:  check_pecks.py --grant-status {target_id} {cap}')
                print('   Re-run send_peck once the grant is approved.')
                sys.exit(2)
            print(f'  ⚠ Grant request did not succeed: {gr}')
            print(f'  Web fallback: https://spaceduckling.com/explore.html?duck={target_id}')
            sys.exit(1)
        print(f'ERROR: HTTP {e.code} — {body}')
        if e.code == 403:
            print(f'  Hint: target may not be peck\'d to you, or sender cert is missing.')
        print(f'  Web fallback: https://spaceduckling.com/explore.html?duck={target_id}')
        sys.exit(1)
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a peck to another Space Duck')
    # P5: identifier discipline. SDID and Duckling ID are both 16-hex —
    # indistinguishable by shape, distinct in semantics. The peck protocol is
    # keyed by SDID. The CLI now lets callers say which kind they have so
    # mistakes are caught at the boundary instead of producing a silent
    # "Target duck not found" response.
    target_grp = parser.add_mutually_exclusive_group(required=True)
    target_grp.add_argument('--to', metavar='ID',
        help='Target duck ID (SDID preferred; legacy alias — accepts either, '
             'but server may bounce a Duckling ID with a 400 wrong_id_type).')
    target_grp.add_argument('--spaceduck-id', dest='spaceduck_id',
        metavar='SDID', help='Target Space Duck ID (16 hex). The protocol key.')
    target_grp.add_argument('--duckling-id', dest='duckling_id',
        metavar='DUCKLING_ID',
        help=('Target Duckling ID — wrong field for the peck protocol. '
              'Provided so the CLI can refuse loudly instead of letting it '
              'reach the server as a stealth SDID.'))
    target_grp.add_argument('--reply-to', dest='reply_to', metavar='PECK_ID',
        help=('Reply to the sender of a previously-received peck. Reads '
              '~/.space-duck/inbox/<PECK_ID>.json (written by peck_listener.py) '
              'and uses its sender_spaceduck_id as the target — no roster '
              'lookup needed.'))
    parser.add_argument('--message', '-m', required=True, help='Message to send')
    parser.add_argument('--purpose', default='connect', help='Purpose label (default: connect)')
    parser.add_argument('--peck-type', default='notify',
                        choices=['notify', 'query', 'data_request', 'task_delegation'])
    parser.add_argument('--skip-preflight', action='store_true',
                        help='Bypass /beak/connection/permissions pre-flight check.')
    parser.add_argument('--no-auto-grant', dest='no_auto_grant', action='store_true',
                        help=('Do NOT auto-request a capability grant on a '
                              '403 grant_required. For scripted callers that '
                              'must avoid side effects; exits 7 instead.'))
    parser.add_argument('--tool-use', dest='tool_use', metavar='JSON',
                        help=('Phase 5 (2026-06-06): JSON list of structured '
                              'tool-call records to attach to the envelope. '
                              'Receiver gets context for free. '
                              'Example: \'[{"name":"bash","cmd":"ls","stdout":"..."}]\''))
    parser.add_argument('--peck-meta', dest='peck_meta', metavar='JSON',
                        help=('0.4.0 Phase 1 (2026-06-12): JSON dict of peck '
                              'protocol v2 metadata. Signature-neutral; '
                              'embedded in envelope as `peck_meta`. Fields: '
                              'protocol_version (int), session_id (str), '
                              'root_peck_id (str), max_rounds (int), '
                              'current_round (int), agent_state (dict), '
                              'chain_state (active|closing_candidate|closed). '
                              'Receivers that pre-date v2 ignore it. '
                              'Example: \'{"protocol_version":2,"session_id":'
                              '"abc","root_peck_id":"peck_xyz","max_rounds":4}\''))
    parser.add_argument('--protocol-version', dest='protocol_version',
                        type=int, default=None,
                        help=('0.4.0 Phase 1: shortcut to set just the '
                              'protocol_version field of peck_meta without '
                              'building a full JSON dict. Use with '
                              '--session-id / --max-rounds for a Phase 0 / '
                              '1 envelope.'))
    parser.add_argument('--session-id', dest='session_id', metavar='UUID',
                        help='Phase 0/1 shortcut — sets peck_meta.session_id.')
    parser.add_argument('--root-peck-id', dest='root_peck_id', metavar='PECK_ID',
                        help=('Phase 0/1 shortcut — sets peck_meta.root_peck_id. '
                              'For the FIRST peck in a chain, leave unset and '
                              'this script will use the new peck_id as root.'))
    parser.add_argument('--max-rounds', dest='max_rounds', type=int,
                        help='Phase 0/1 shortcut — sets peck_meta.max_rounds.')
    parser.add_argument('--current-round', dest='current_round', type=int,
                        help=('Phase 0/1 shortcut — sets peck_meta.current_round. '
                              'For the FIRST peck in a chain, set to 1 (sender '
                              'counts their own send as round 1). Receivers '
                              'increment this on reply via Phase 1.5 echo-back.'))
    args = parser.parse_args()

    if args.duckling_id:
        print('ERROR: --duckling-id is not a valid peck target.')
        print('  The peck protocol is keyed by Space Duck ID (SDID), not by')
        print('  Duckling ID. Look up the target\'s SDID (via Mission Control')
        print('  or `connections.py`) and re-run with --spaceduck-id.')
        sys.exit(2)

    cfg = load_config()
    if args.reply_to:
        target_sdid = resolve_reply_to(args.reply_to)
        print(f'↩ reply-to: resolved {args.reply_to} → {target_sdid}')
    else:
        target_in = args.spaceduck_id or args.to
        target_sdid = resolve_target(cfg, target_in)
    _tool_use_list = None
    if args.tool_use:
        try:
            _tool_use_list = json.loads(args.tool_use)
            if not isinstance(_tool_use_list, list):
                print('ERROR: --tool-use must be a JSON array.')
                sys.exit(2)
        except json.JSONDecodeError as _e:
            print(f'ERROR: --tool-use is not valid JSON: {_e}')
            sys.exit(2)

    # 0.4.0 Phase 1 — assemble peck_meta from --peck-meta JSON and/or shortcut
    # flags. Shortcut flags override fields in --peck-meta when both supplied.
    _peck_meta = None
    if args.peck_meta:
        try:
            _peck_meta = json.loads(args.peck_meta)
            if not isinstance(_peck_meta, dict):
                print('ERROR: --peck-meta must be a JSON object.')
                sys.exit(2)
        except json.JSONDecodeError as _e:
            print(f'ERROR: --peck-meta is not valid JSON: {_e}')
            sys.exit(2)
    if (args.protocol_version is not None or args.session_id or
            args.root_peck_id or args.max_rounds is not None or
            args.current_round is not None):
        if _peck_meta is None:
            _peck_meta = {}
        if args.protocol_version is not None:
            _peck_meta['protocol_version'] = args.protocol_version
        elif 'protocol_version' not in _peck_meta:
            _peck_meta['protocol_version'] = 2
        if args.session_id:
            _peck_meta['session_id'] = args.session_id
        if args.root_peck_id:
            _peck_meta['root_peck_id'] = args.root_peck_id
        if args.max_rounds is not None:
            _peck_meta['max_rounds'] = args.max_rounds
        if args.current_round is not None:
            _peck_meta['current_round'] = args.current_round

    # B5 (2026-06-24): on an INITIAL peck (not --reply-to), guarantee a bounded
    # v2 session so the deterministic round cap always propagates. Without this,
    # a plain `send_peck --message ...` carried no session + no max_rounds, so
    # two auto-responders ping-ponged with only <peck_done/> + the Jaccard gate
    # to stop them (Wayne B5). setdefault respects any explicit --session-id /
    # --max-rounds / --current-round the caller already supplied; reply pecks
    # are untouched (they inherit the session via the responder's echo-mirror).
    if not args.reply_to:
        if _peck_meta is None:
            _peck_meta = {}
        _peck_meta.setdefault('protocol_version', 2)
        _peck_meta.setdefault('session_id', 'sess_' + secrets.token_urlsafe(12))
        _peck_meta.setdefault('current_round', 1)
        _peck_meta.setdefault('max_rounds', DEFAULT_INITIAL_MAX_ROUNDS)

    send_peck(cfg, target_sdid, args.message, args.purpose, args.peck_type,
              skip_preflight=args.skip_preflight, tool_use=_tool_use_list,
              peck_meta=_peck_meta, no_auto_grant=args.no_auto_grant)
