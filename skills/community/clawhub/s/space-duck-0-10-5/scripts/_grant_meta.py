#!/usr/bin/env python3
"""
_grant_meta.py — grant-lifecycle helpers shared by send_peck.py and check_pecks.py.

INTENT (SKILL-091 Phase B, spec §5): surface a capability grant's *expiry* to
the operator BEFORE it lapses, so cross-owner grants (which today die on a 7d
TTL with no renewal) don't silently stop working a week after approval.

  - `send_peck.py` pre-flight  → one-line advisory warning when the active
    send_peck grant to the recipient has <7 days left (item 1).
  - `check_pecks.py`           → a once-per-window nudge for any active outbound
    grant nearing expiry (item 2), de-duped via ~/.space-duck/expiry_nudges.json.

DATA SOURCE — discovery note (spec §5 / item 1):
  The ONLY beak-key-callable grant surface is `POST /beak/grants/check` (dry_run)
  — already used by `check_pecks.grant_status()`. Today that response returns
  `{allowed, throttle_remaining, grant_id|reason}` and does NOT include
  `expires_at` / `grant_class` (lambda_function.py `/beak/grants/check` handler).
  `/beak/connection/permissions` returns connection permissions, not grant rows.
  So grant expiry metadata is NOT client-visible via any existing call yet.

  This module is therefore written FAIL-OPEN and forward-compatible: it reads
  `expires_at`/`grant_class` from the grants/check response *when present*, and
  when absent (today) it emits NOTHING — no warning, no nudge, and it NEVER
  blocks or gates a send. A one-line server change adding those two fields to
  the grants/check allow-response (out of skill scope) lights this up with zero
  further skill work. This is the capability-negotiation / graceful-degradation
  doctrine: the client already speaks the richer protocol.

CALLS:  POST <api>/beak/grants/check  (dry_run — no usage increment)
AUTH:   Authorization: Bearer <beak_key>  (grant endpoints use Bearer, not X-Beak-Key)
No new hosts, no new endpoints, no secrets written beyond a local seen-marker.
"""
import json, time, urllib.request, urllib.error
from pathlib import Path

# 7-day early-warning window. Matches the server's _GRANT_DEFAULT_TTL_SEC (7d),
# so a `timed` grant warns across its whole life while a `standing` grant only
# warns if it is genuinely about to lapse (abandoned, past sliding renewal).
WARN_WINDOW_SEC = 7 * 86400

NUDGE_PATH = Path.home() / '.space-duck' / 'expiry_nudges.json'


def default_scope(target_sd, capability='send_peck'):
    """send_peck grants are scoped `to:<recipient_sdid>` (server does exact
    string equality). Other capabilities default to empty scope."""
    return f'to:{target_sd}' if capability == 'send_peck' else ''


def extract_meta(resp):
    """Pure. Pull grant-lifecycle fields from a /beak/grants/check response.

    Returns {allowed, grant_id, grant_class, expires_at, reason}. Fields the
    current server omits (grant_class / expires_at) come back None — callers
    treat None as 'no signal' and stay silent (fail-open). Never raises."""
    if not isinstance(resp, dict):
        return {'allowed': None, 'grant_id': None, 'grant_class': None,
                'expires_at': None, 'reason': None}
    exp = resp.get('expires_at')
    try:
        exp = int(exp) if exp not in (None, '') else None
    except (TypeError, ValueError):
        exp = None
    return {
        'allowed':     resp.get('allowed'),
        'grant_id':    resp.get('grant_id'),
        'grant_class': resp.get('grant_class'),
        'expires_at':  exp,
        'reason':      resp.get('reason'),
    }


def _fmt_left(remaining):
    """Human 'Nd Nh' / 'Nh Nm' for a positive seconds count."""
    days = remaining // 86400
    hours = (remaining % 86400) // 3600
    if days >= 1:
        return f'{days}d {hours}h'
    mins = (remaining % 3600) // 60
    return f'{hours}h {mins}m'


def format_expiry_warning(meta, target_sd, peer_certified=None, now=None):
    """Pure. Return a one-line advisory string when an ACTIVE grant is within
    WARN_WINDOW_SEC of expiry, else None.

    Fail-open contract: any missing datum (not allowed / no expires_at /
    already lapsed / outside the window) → None. This function NEVER decides
    whether a send proceeds — it only produces advisory text."""
    if not meta or meta.get('allowed') is not True:
        return None
    exp = meta.get('expires_at')
    if not exp:
        return None
    now = int(now if now is not None else time.time())
    remaining = int(exp) - now
    if remaining <= 0 or remaining >= WARN_WINDOW_SEC:
        return None
    gc = meta.get('grant_class') or 'timed'
    left = _fmt_left(remaining)
    msg = (f'⏳ send_peck grant to {target_sd} ({gc}) expires in {left} '
           '— re-approval needed after that.')
    if gc != 'standing':
        if peer_certified is True:
            msg += (' Peer is CERTIFIED — request a Standing grant to end '
                    'the weekly re-approval.')
        elif peer_certified is None:
            msg += (' If the peer is CERTIFIED, request a Standing grant to end '
                    'the weekly re-approval.')
    return msg


def fetch_grant_check(cfg, target_sd, capability='send_peck', scope=None, timeout=5):
    """Best-effort POST /beak/grants/check dry_run. Returns the parsed dict, or
    None on ANY error/timeout. Never raises — the caller must be able to treat
    a None as 'no signal' and carry on immediately (no block, no delay-to-gate)."""
    try:
        api = cfg.get('api_base', 'https://beak.spaceduckling.com')
        bk = cfg.get('beak_key', '')
        if not bk:
            return None
        if scope is None:
            scope = default_scope(target_sd, capability)
        body = json.dumps({
            'recipient_spaceduck_id': target_sd,
            'capability': capability,
            'scope': scope,
            'dry_run': True,
        }).encode()
        req = urllib.request.Request(
            f'{api}/beak/grants/check', data=body, method='POST',
            headers={'Content-Type': 'application/json',
                     'Authorization': f'Bearer {bk}'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read() or b'{}')
    except Exception:
        return None


def preflight_expiry_warning(cfg, target_sd, capability='send_peck',
                             scope=None, peer_certified=None, timeout=5, now=None):
    """send_peck pre-flight (item 1). Best-effort: returns an advisory warning
    string or None. NEVER raises, never blocks. A dry_run check does not
    increment usage and is server-cached ~60s per (sender,recipient,cap,scope),
    so repeated sends to the same peer add no meaningful latency."""
    try:
        resp = fetch_grant_check(cfg, target_sd, capability, scope, timeout)
        if resp is None:
            return None
        return format_expiry_warning(extract_meta(resp), target_sd,
                                     peer_certified=peer_certified, now=now)
    except Exception:
        return None


# ── once-per-window nudge state (item 2) ────────────────────────────────────

def load_nudges():
    """Return the seen-marker map {grant_id: last_nudged_expires_at}. Never raises."""
    try:
        d = json.loads(NUDGE_PATH.read_text())
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def save_nudges(state):
    """Persist the seen-marker map (chmod 0600). Best-effort; never raises."""
    try:
        NUDGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        NUDGE_PATH.write_text(json.dumps(state, indent=2))
        try:
            NUDGE_PATH.chmod(0o600)
        except OSError:
            pass
    except Exception:
        pass


def should_nudge(grant_id, expires_at, state):
    """Pure. True iff this (grant_id, expiry-window) has not been nudged yet.
    Keying on expires_at (not just grant_id) means a standing grant that slid
    its expiry forward past a prior nudge can nudge again for the new window."""
    if not grant_id or not expires_at:
        return False
    return str(state.get(grant_id)) != str(int(expires_at))


def evaluate_nudge(resp, peer_sd, state, peer_certified=None, now=None):
    """Pure (no I/O). Given a grants/check response + the current nudge-state
    map, decide whether to emit a nudge for `peer_sd`.

    Returns (message_or_None, state). When a nudge fires, a COPY of state is
    returned with the marker recorded; otherwise the original state is returned
    unchanged. Fail-open: no expiry signal → (None, state)."""
    meta = extract_meta(resp)
    msg = format_expiry_warning(meta, peer_sd, peer_certified=peer_certified, now=now)
    if not msg:
        return None, state
    gid, exp = meta.get('grant_id'), meta.get('expires_at')
    if not should_nudge(gid, exp, state):
        return None, state
    new_state = dict(state)
    new_state[gid] = int(exp)
    return msg, new_state
