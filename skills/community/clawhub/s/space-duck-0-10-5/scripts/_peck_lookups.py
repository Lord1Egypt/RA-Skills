#!/usr/bin/env python3
"""Space Duck — read-only lookup registry for the peck auto-responder.

WHY THIS EXISTS
    The auto-responder composes replies with `claude --print` and NO tools
    (peck_responder.py — `bypassPermissions` was deliberately dropped in
    0.4.23 so untrusted peck text can never reach a tool call). That is the
    correct security posture, but it left the responder unable to answer even
    harmless factual questions from a peer: "what tier are you?", "are we
    still connected?", "when did you last pulse?" — it had to decline
    everything, which reads as stonewalling.

    This module closes that gap WITHOUT giving the model tools. The model
    never chooses a command; it may only name one of the fixed lookups below.
    We execute it here, in Python, and hand the result back as text.

SECURITY MODEL (read this before adding a lookup)
    * Allowlist, not an interpreter. `LOOKUPS` is a closed dict. An unknown
      name is dropped, not attempted.
    * No shell, no subprocess, no filesystem reads outside SD_DIR metadata,
      no environment dumping, no secrets. The Beak Key is USED to authenticate
      but is never returned in any payload.
    * Every lookup answers only about THIS duck's own network standing —
      facts the asking peer can already see from their side of the graph, or
      that its owner would happily state out loud.
    * Egress is unchanged: the same official Space Duck host every other
      script in this skill already calls, gated by _apiguard.
    * Off by default. `peck_lookups_enabled` must be set in config.json.
    * Fail-closed and non-raising: any error becomes a short text string.

    A lookup must NEVER read arbitrary paths, accept a peer-supplied URL, or
    expose another duck's private data. If a proposed lookup cannot satisfy
    all three, it does not belong here.
"""
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

try:
    from _apiguard import is_official_host
except Exception:                                    # pragma: no cover
    def is_official_host(_url):
        return False

SD_DIR = Path.home() / '.space-duck'

MAX_LOOKUPS_PER_PECK = 3      # cap the round-trips one peck can trigger
MAX_RESULT_CHARS     = 1500   # per lookup
MAX_TOTAL_CHARS      = 4500   # across all lookups in one peck
_HTTP_TIMEOUT        = 10


def _api(cfg):
    return (cfg or {}).get('api') or (cfg or {}).get('api_base') \
        or 'https://beak.spaceduckling.com'


def _get(cfg, path):
    """Authenticated GET against the official host only. Returns dict or None."""
    url = _api(cfg).rstrip('/') + path
    if not is_official_host(url):
        return None
    req = urllib.request.Request(url, headers={
        'Accept': 'application/json',
        'X-Beak-Key': (cfg or {}).get('beak_key', ''),
    })
    try:
        with urllib.request.urlopen(req, timeout=_HTTP_TIMEOUT) as r:
            return json.loads(r.read())
    except Exception:
        return None


def _post(cfg, path, body):
    url = _api(cfg).rstrip('/') + path
    if not is_official_host(url):
        return None
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers={'Accept': 'application/json',
                 'Content-Type': 'application/json',
                 'X-Beak-Key': (cfg or {}).get('beak_key', '')},
        method='POST')
    try:
        with urllib.request.urlopen(req, timeout=_HTTP_TIMEOUT) as r:
            return json.loads(r.read())
    except Exception:
        return None


def _ts(v):
    """Epoch seconds -> ISO8601Z. Returns '' rather than raising on junk."""
    try:
        return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(int(float(v))))
    except Exception:
        return str(v or '')


def _is_sdid(s):
    s = (s or '').strip()
    return len(s) == 16 and all(c in '0123456789abcdefABCDEF' for c in s)


# ── Lookup handlers ──────────────────────────────────────────────────────
# Signature: (cfg, arg, sender_sd) -> str.  Never raise. Never return secrets.

def _lk_self_status(cfg, arg, sender_sd):
    did = cfg.get('duckling_id', '')
    sdid = cfg.get('spaceduck_id', '')
    d = _get(cfg, f'/beak/status?duckling_id={did}') or {}
    if not d:
        return 'self_status: platform unreachable right now.'
    out = {
        'duck_name': cfg.get('agent_name') or cfg.get('duck_name') or '',
        'spaceduck_id': sdid,
        'trust_tier': d.get('trust_tier') or d.get('tier_verified') or '',
        'service_tier': d.get('plan') or d.get('tier') or '',
        'status': d.get('status') or '',
    }
    return 'self_status: ' + json.dumps({k: v for k, v in out.items() if v})


def _lk_connections(cfg, arg, sender_sd):
    did = cfg.get('duckling_id', '')
    d = _get(cfg, f'/beak/spaceducks?duckling_id={did}') or {}
    rows = d.get('agents') or d.get('spaceducks') or []
    if not rows:
        return 'connections: none visible (or platform unreachable).'
    # The bond graph returns one row per connection, so a duck bonded several
    # ways appears repeatedly (McQuacken x4 in the 2026-08-28 live test).
    # Dedupe by spaceduck_id — a peer asking "who are you connected to" wants
    # distinct ducks, not edge count.
    peers, seen = [], set()
    for r in rows:
        sid = r.get('spaceduck_id', '')
        if not sid or sid in seen:
            continue
        seen.add(sid)
        nm = (r.get('display_name') or r.get('duck_name')
              or r.get('agent_name') or r.get('name') or '')
        # The API echoes a truncated id as `name` when the row has no real
        # display name; that is noise, not an answer.
        if not nm or sid.startswith(nm):
            nm = '(unnamed)'
        peers.append({'name': nm, 'spaceduck_id': sid,
                      'status': r.get('status') or r.get('connection_status') or ''})
        if len(peers) >= 40:
            break
    return f'connections ({len(peers)}): ' + json.dumps(peers)


def _lk_permissions(cfg, arg, sender_sd):
    """What THIS duck grants the asking peer (or a named peer)."""
    peer = arg.strip() if _is_sdid(arg) else sender_sd
    if not _is_sdid(peer):
        return 'permissions: need a 16-hex spaceduck_id.'
    my_sd = cfg.get('spaceduck_id', '')
    d = _get(cfg, f'/beak/connection/permissions'
                  f'?sender_spaceduck_id={peer}&target_spaceduck_id={my_sd}') or {}
    perms = d.get('permissions') or d
    if not perms:
        return f'permissions: no connection record for {peer}.'
    return f'permissions[{peer}]: ' + json.dumps(perms)[:MAX_RESULT_CHARS]


def _lk_activity(cfg, arg, sender_sd):
    did = cfg.get('duckling_id', '')
    d = _post(cfg, '/beak/audit', {'duckling_id': did, 'limit': 10}) or {}
    # live shape verified 2026-08-28: {'entries': [...]}; the others are
    # defensive fallbacks in case the endpoint shape moves.
    rows = d.get('entries') or d.get('events') or d.get('items') or []
    if not rows:
        return 'activity: no recent events visible.'
    # `detail` is deliberately NOT included — it carries ids//internals of
    # other ducks. Event type + time is what a peer legitimately needs.
    trimmed = [{'ts': _ts(r.get('timestamp') or r.get('ts')),
                'event': r.get('event_type') or r.get('event') or r.get('action') or ''}
               for r in rows[:10]]
    return 'activity: ' + json.dumps(trimmed)


def _lk_skill_version(cfg, arg, sender_sd):
    # The skill's own _meta.json sits one level above this scripts/ dir; the
    # SD_DIR paths are fallbacks for unusual layouts. Resolving from __file__
    # is what actually works on a normal install (verified 2026-08-28).
    for p in (Path(__file__).resolve().parent.parent / '_meta.json',
              SD_DIR / '_meta.json', SD_DIR / 'skill' / '_meta.json'):
        try:
            if p.is_file():
                v = (json.loads(p.read_text()) or {}).get('version')
                if v:
                    return f'skill_version: space-duck {v}'
        except Exception:
            pass
    return 'skill_version: unknown (no _meta.json found locally).'


def _lk_host_time(cfg, arg, sender_sd):
    return ('host_time: ' + time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            + ' UTC (local: ' + time.strftime('%Y-%m-%d %H:%M:%S %Z') + ')')


LOOKUPS = {
    'self_status':   ('This duck\'s own identity, trust tier and service tier.',
                      _lk_self_status),
    'connections':   ('The ducks this duck is connected/bonded to.',
                      _lk_connections),
    'permissions':   ('Effective permissions this duck grants a peer. '
                      'Arg: optional 16-hex spaceduck_id (defaults to you).',
                      _lk_permissions),
    'activity':      ('Last 10 audit events on this duck.', _lk_activity),
    'skill_version': ('Installed space-duck skill version.', _lk_skill_version),
    'host_time':     ('Current time on this duck\'s host.', _lk_host_time),
}


def catalog_text():
    return '\n'.join(f'  - {n}: {d}' for n, (d, _) in sorted(LOOKUPS.items()))


def lookups_enabled(cfg, sender_sd):
    """Off unless the OWNER turned it on in config.json.

    `peck_lookups_senders`: optional allowlist of 16-hex spaceduck_ids. Empty
    or absent = any peer that already passed the connection permission check
    (the responder never reaches this code for an unauthorized sender).
    """
    if not (cfg or {}).get('peck_lookups_enabled'):
        return False
    allow = (cfg or {}).get('peck_lookups_senders') or []
    if not allow:
        return True
    return (sender_sd or '').upper() in {str(a).upper() for a in allow}


def run_lookups(cfg, names, sender_sd):
    """Execute allowlisted lookups. `names` is a list of (name, arg) pairs.

    Returns (results_text, executed_names). Unknown names are reported as
    unavailable rather than silently dropped, so the model stops re-asking.
    """
    out, executed, total = [], [], 0
    for name, arg in names[:MAX_LOOKUPS_PER_PECK]:
        entry = LOOKUPS.get((name or '').strip().lower())
        if not entry:
            out.append(f'{name}: not an available lookup.')
            continue
        try:
            text = str(entry[1](cfg, arg or '', sender_sd) or '')[:MAX_RESULT_CHARS]
        except Exception as e:
            text = f'{name}: lookup failed ({type(e).__name__}).'
        if total + len(text) > MAX_TOTAL_CHARS:
            out.append(f'{name}: omitted (result budget exhausted).')
            break
        total += len(text)
        out.append(text)
        executed.append(name)
    return '\n'.join(out), executed
