"""_pending_sends.py — durable queue for pecks blocked on a pending capability grant.

0.9.0 [F4-CLIENT]. The client half of the F4 grant-approval loop.

WHY: `send_peck.py` on a `403 grant_required` self-requests an owner grant
(`_request_grant`) and then exits, telling the human to "re-run once approved".
Nobody re-runs it. This queue persists the unsent peck so the approval can
resend it automatically — either driven by the platform's grant-approved
system-notice (peck_listener, push) or a gentle status poll (peck_listener
fallback, pull). Both consumers share one idempotency gate here so the peck is
resent EXACTLY once.

JOIN KEY: entries are keyed by the grant REQUEST id. That is the only join key
that exists at block time — the grant itself is minted later, on approval — and
the platform's `_notify_grant_approved` (lambda_function.py) echoes both
`request_id` and `grant_id` on the system-notice row, so `request_id` matches
the queued entry and `grant_id` is recorded when the entry is consumed.

STORAGE: a single local JSON file, `~/.space-duck/pending_sends.json`, 0600.
No network. No secrets — only the recipient SDID, the message, and peck
metadata needed to reconstruct the send. TTL-bounded (default 72h).
"""
import json
import os
import secrets
import threading
import time
from pathlib import Path

PENDING_FILE = Path.home() / '.space-duck' / 'pending_sends.json'
# The notice handler and the poll-fallback sweep run as threads in the SAME
# peck_listener process; claim() is load-modify-save, so without a lock both
# could read the file before either writes and each win the in-flight slot.
# One process-wide lock serializes every queue mutation. (Cross-process races
# don't arise: only peck_listener consumes this queue.)
_LOCK = threading.RLock()
DEFAULT_TTL_S = 72 * 3600           # 72h — an unapproved grant is stale by then
MAX_ATTEMPTS = 5                    # bounded resend attempts before giving up
_RETRY_BASE_S = 60                  # backoff base; capped at _RETRY_CAP_S
_RETRY_CAP_S = 3600
# While an attempt is in flight, hold the slot this long so a second consumer
# (the poll fallback racing the push notice) does not double-send. Short enough
# that a crashed resend still gets retried within a reasonable window.
_INFLIGHT_LOCK_S = 120


def _locked(fn):
    import functools

    @functools.wraps(fn)
    def wrapper(*a, **kw):
        with _LOCK:
            return fn(*a, **kw)
    return wrapper


def _now():
    return int(time.time())


def _load():
    """Return {request_id: entry}. Never raises."""
    try:
        d = json.loads(PENDING_FILE.read_text())
        if isinstance(d, dict):
            return d
    except Exception:
        pass
    return {}


def _save(d):
    """Atomic write-then-rename, 0600. Never raises."""
    try:
        PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = PENDING_FILE.with_suffix('.json.tmp')
        with open(tmp, 'w') as f:
            json.dump(d, f, indent=2)
        os.chmod(tmp, 0o600)
        os.replace(tmp, PENDING_FILE)
    except Exception:
        pass


def _backoff(attempts):
    return min(_RETRY_CAP_S, _RETRY_BASE_S * (2 ** max(0, attempts - 1)))


@_locked
def enqueue(request_id, *, target_spaceduck_id, message, purpose='connect',
            peck_type='notify', capability='send_peck', scope='',
            peck_meta=None, tool_use=None, ttl_s=DEFAULT_TTL_S):
    """Persist an unsent peck blocked on grant `request_id`.

    Idempotent on request_id: re-queuing the same request_id keeps the existing
    idempotency key and consumed/attempt state (a re-run of the same blocked
    send must not reset a resend already in progress). Returns the stored entry.
    """
    if not request_id:
        return None
    d = _load()
    now = _now()
    existing = d.get(request_id)
    if existing and not existing.get('done'):
        # Refresh the payload (message/meta may have changed on re-run) but keep
        # the idempotency key + attempt bookkeeping so we never double-send.
        existing.update({
            'target_spaceduck_id': target_spaceduck_id,
            'message': message,
            'purpose': purpose,
            'peck_type': peck_type,
            'capability': capability,
            'scope': scope,
            'peck_meta': peck_meta,
            'tool_use': tool_use,
        })
        _save(d)
        return existing
    entry = {
        'request_id': request_id,
        'idempotency_key': 'psend_' + secrets.token_urlsafe(12),
        'target_spaceduck_id': target_spaceduck_id,
        'message': message,
        'purpose': purpose,
        'peck_type': peck_type,
        'capability': capability,
        'scope': scope,
        'peck_meta': peck_meta,
        'tool_use': tool_use,
        'grant_id': '',
        'created_at': now,
        'expires_at': now + int(ttl_s or DEFAULT_TTL_S),
        'attempts': 0,
        'last_attempt_at': 0,
        'next_retry_at': 0,
        'inflight_until': 0,
        'done': False,
        'failed': False,
        'last_error': '',
    }
    d[request_id] = entry
    _save(d)
    return entry


@_locked
def prune_expired(now=None):
    """Drop expired / long-done entries. Returns count removed. Never raises."""
    now = now or _now()
    d = _load()
    drop = [rid for rid, e in d.items()
            if int(e.get('expires_at') or 0) and now > int(e['expires_at'])]
    for rid in drop:
        del d[rid]
    if drop:
        _save(d)
    return len(drop)


@_locked
def active(now=None):
    """Entries eligible for a (re)send attempt right now: not done, not expired,
    past any retry backoff, and not currently locked by an in-flight attempt.
    Returns a list of entry dicts (copies from disk)."""
    now = now or _now()
    out = []
    for e in _load().values():
        if e.get('done'):
            continue
        if int(e.get('expires_at') or 0) and now > int(e['expires_at']):
            continue
        if now < int(e.get('next_retry_at') or 0):
            continue
        if now < int(e.get('inflight_until') or 0):
            continue
        out.append(e)
    return out


@_locked
def claim(request_id, now=None):
    """Atomically mark `request_id` in-flight before a resend attempt.

    This is the shared idempotency gate: the push (notice) path and the poll
    fallback both call claim() first, and only one wins the slot. Returns the
    entry to send, or None if it is missing / done / expired / already claimed
    (in-flight) / out of attempts.
    """
    now = now or _now()
    d = _load()
    e = d.get(request_id)
    if not e:
        return None
    if e.get('done'):
        return None
    if int(e.get('expires_at') or 0) and now > int(e['expires_at']):
        del d[request_id]
        _save(d)
        return None
    if now < int(e.get('inflight_until') or 0):
        return None                      # another consumer holds the slot
    if now < int(e.get('next_retry_at') or 0):
        return None                      # still in backoff
    if int(e.get('attempts') or 0) >= MAX_ATTEMPTS:
        e['done'] = True
        e['failed'] = True
        e['last_error'] = 'max_attempts_exhausted'
        _save(d)
        return None
    e['attempts'] = int(e.get('attempts') or 0) + 1
    e['last_attempt_at'] = now
    e['inflight_until'] = now + _INFLIGHT_LOCK_S
    _save(d)
    return dict(e)


@_locked
def mark_done(request_id, grant_id='', now=None):
    """Record a successful resend. Removes the entry from the queue."""
    now = now or _now()
    d = _load()
    if request_id in d:
        del d[request_id]
        _save(d)
        return True
    return False


@_locked
def mark_failed(request_id, error='', now=None):
    """Record a failed resend attempt. Schedules a bounded backoff retry, or
    marks the entry dead once MAX_ATTEMPTS is reached."""
    now = now or _now()
    d = _load()
    e = d.get(request_id)
    if not e:
        return False
    e['last_error'] = str(error)[:200]
    e['inflight_until'] = 0              # release the in-flight lock
    if int(e.get('attempts') or 0) >= MAX_ATTEMPTS:
        e['done'] = True
        e['failed'] = True
    else:
        e['next_retry_at'] = now + _backoff(int(e.get('attempts') or 1))
    _save(d)
    return True


@_locked
def record_grant_id(request_id, grant_id):
    """Best-effort: stamp the grant_id learned from the approval notice onto the
    queued entry (audit trail; not required for the join)."""
    if not request_id or not grant_id:
        return
    d = _load()
    e = d.get(request_id)
    if e and not e.get('grant_id'):
        e['grant_id'] = grant_id
        _save(d)


if __name__ == '__main__':
    # Local self-test — no network, uses a temp HOME so the real queue is never
    # touched. Proves enqueue → claim (idempotency) → done, and the retry path.
    import tempfile
    tmp = tempfile.mkdtemp(prefix='pendtest_')
    PENDING_FILE = Path(tmp) / 'pending_sends.json'   # noqa: F811 (test override)
    ok = 0
    total = 0

    def check(label, cond):
        global ok, total
        total += 1
        if cond:
            ok += 1
        print(f'  [{"✓" if cond else "✗"}] {label}')

    # 1) enqueue
    e = enqueue('req_1', target_spaceduck_id='DEADBEEF', message='hi',
                capability='send_peck', scope='to:DEADBEEF')
    check('enqueue returns entry with idempotency key', bool(e and e['idempotency_key']))
    check('one active entry', len(active()) == 1)

    # 2) idempotent re-enqueue keeps the same idempotency key
    k0 = e['idempotency_key']
    e2 = enqueue('req_1', target_spaceduck_id='DEADBEEF', message='hi (again)',
                 capability='send_peck', scope='to:DEADBEEF')
    check('re-enqueue keeps idempotency key', e2['idempotency_key'] == k0)
    check('re-enqueue refreshes message', e2['message'] == 'hi (again)')
    check('still one active entry', len(active()) == 1)

    # 3) claim wins once; a second claim returns None (in-flight lock)
    c1 = claim('req_1')
    check('first claim returns entry', c1 is not None)
    c2 = claim('req_1')
    check('second claim blocked (in-flight lock = no double send)', c2 is None)
    check('claimed entry not active while in-flight', len(active()) == 0)

    # 4) success removes it
    mark_done('req_1', grant_id='grant_xyz')
    check('mark_done removes entry', 'req_1' not in _load())
    check('claim after done returns None', claim('req_1') is None)

    # 5) failure path → backoff → dead after MAX_ATTEMPTS
    enqueue('req_2', target_spaceduck_id='CAFE', message='retry me',
            capability='send_peck', scope='to:CAFE')
    for i in range(MAX_ATTEMPTS):
        got = claim('req_2', now=_now() + i * (_RETRY_CAP_S + 1))
        check(f'attempt {i + 1} claim ok', got is not None)
        mark_failed('req_2', error=f'boom{i}', now=_now() + i * (_RETRY_CAP_S + 1))
    dead = claim('req_2', now=_now() + MAX_ATTEMPTS * (_RETRY_CAP_S + 1))
    check('dead after MAX_ATTEMPTS (no infinite resend)', dead is None)
    check('dead entry marked failed+done', _load()['req_2']['failed'] is True)

    # 6) expiry prune
    enqueue('req_3', target_spaceduck_id='BEEF', message='old', ttl_s=1)
    d = _load(); d['req_3']['expires_at'] = _now() - 10; _save(d)
    check('prune removes expired', prune_expired() == 1)

    print(f'RESULT: {ok}/{total} checks passed')
    import shutil as _sh
    _sh.rmtree(tmp, ignore_errors=True)
    raise SystemExit(0 if ok == total else 1)
