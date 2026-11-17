"""Shared daily update-nudge. 0.8.12 [NUDGE-0812].

Extracted from telegram_listener.py so peck-only boxes get the same nudge.
Before this, the check lived only in the telegram listener's pulse thread, so
a duck running just peck_listener.py (Josh's laptop is the reference case) had
no update path at all and would sit on an old version indefinitely.

One implementation, two callers. Never raises: both callers run it from a
long-lived loop that must not be able to die.
"""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

SKILL_VERSION_FALLBACK = '0.0.0'
_META_PATH = Path(__file__).resolve().parent.parent / '_meta.json'


def skill_version():
    """Installed (on-disk) skill version, read fresh from _meta.json.

    NOTE: this is disk truth, NOT the code currently executing. update.sh
    deliberately does not restart a running listener, so after an update the
    disk says 0.8.11 while 0.8.10 bytecode is still in memory. Callers that
    need the running version want RUNNING_SKILL_VERSION. Never raises.

    Returns '<fallback>-unknown' when _meta.json is missing or corrupt (dev
    checkouts and partial installs lack it) so a bogus read is visibly marked
    rather than silently masquerading as a real version.
    """
    try:
        v = (json.loads(_META_PATH.read_text()) or {}).get('version')
        if isinstance(v, str) and v.strip():
            return v.strip()
    except Exception:
        pass
    return SKILL_VERSION_FALLBACK + '-unknown'


# 0.8.11 [VER-0811] — callers snapshot skill_version() at import as
# RUNNING_SKILL_VERSION (see telegram_listener.py): that IS the version of the
# code in memory, while skill_version() re-reads disk, which diverges the
# moment update.sh runs without a restart. Reporting both lets Mission Control
# render an honest "update installed, restart pending" state instead of
# claiming the new version is live when the old bytecode is still serving.

VERSION_CHECK_INTERVAL = 86400          # once per day

# 0.8.11 [VER-0811] — nudge state PERSISTS to disk.
#
# 0.8.10 kept this in process memory only ([0] at import), so the check fired
# on the first loop iteration of every process start. Harmless while the nudge
# was DOA (see the contract fix below); the moment the nudge actually works, a
# crash-looping or supervisord-bounced listener would re-nudge the owner on
# every restart. The retired daemon got this right by persisting last-nudged
# version; the thread now does the same.
VERSION_STATE_FILE = Path.home() / '.space-duck' / 'version-check.json'


def _load_version_state():
    """{'last_check_ts': int, 'last_nudged': str}. Never raises."""
    try:
        d = json.loads(VERSION_STATE_FILE.read_text())
        if isinstance(d, dict):
            return d
    except Exception:
        pass
    return {}


def _save_version_state(state):
    try:
        VERSION_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        # 0.8.12 — write-then-rename. Two listeners on one box share this
        # file; a torn read costs an extra check (and possibly one extra
        # nudge), so make the swap atomic rather than rely on luck.
        tmp = VERSION_STATE_FILE.with_suffix('.json.tmp')
        with open(tmp, 'w') as f:
            json.dump(state, f)
        os.chmod(tmp, 0o600)
        os.replace(tmp, VERSION_STATE_FILE)
    except Exception:
        pass


# 0.8.13 [RUN-0813] — running-version marker.
#
# update.sh had no way to prove a restart actually took effect: it checked
# only that *a* listener process existed, which is also true when the bounce
# silently failed and the OLD process is still serving. Each listener now
# stamps the version it is EXECUTING at startup; update.sh reads the stamp
# back and refuses to report success unless running == installed.
RUNNING_VERSION_FILE = Path.home() / '.space-duck' / 'running-version.json'


def _atomic_write_json(path, data):
    """write-then-rename, 0600. Never raises."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + '.tmp')
        with open(tmp, 'w') as f:
            json.dump(data, f)
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    except Exception:
        pass


def record_running_version(component, version=None):
    """Stamp {component: {version, pid, started_at}} at listener startup.

    Keyed by component so telegram_listener and peck_listener on one box each
    keep their own entry instead of clobbering each other. Best-effort: a
    failed stamp must never stop a listener from starting.
    """
    try:
        cur = {}
        try:
            d = json.loads(RUNNING_VERSION_FILE.read_text())
            if isinstance(d, dict):
                cur = d
        except Exception:
            pass
        cur[str(component)] = {
            'version': str(version or skill_version()),
            'pid': os.getpid(),
            'started_at': int(time.time()),
        }
        _atomic_write_json(RUNNING_VERSION_FILE, cur)
    except Exception:
        pass


def _cmp_semver(a, b):
    """-1/0/1 for a<b / a==b / a>b. Non-numeric parts sort low, never raises."""
    def parts(v):
        return [int(c) if c.isdigit() else -1
                for c in str(v).split('-')[0].split('.')]
    pa, pb = parts(a), parts(b)
    n = max(len(pa), len(pb))
    pa += [0] * (n - len(pa)); pb += [0] * (n - len(pb))
    return (pa > pb) - (pa < pb)


def _version_check_once(beak_key, sd_id, api_base, verbose=False):
    """Nudge the owner if the installed skill is behind the published latest.

    Best-effort and NEVER raises: this runs inside the pulse thread and must
    not be able to kill it.

    Rate limiting is on DISK (VERSION_STATE_FILE), not process memory: at most
    one check per VERSION_CHECK_INTERVAL and at most one nudge per distinct
    published version, both surviving restarts.
    """
    try:
        state = _load_version_state()
        now = int(time.time())
        if now - int(state.get('last_check_ts') or 0) < VERSION_CHECK_INTERVAL:
            return
        state['last_check_ts'] = now
        _save_version_state(state)

        cur = skill_version()
        if cur.endswith('-unknown'):
            return                       # cannot compare against a fiction
        url = f'{api_base.rstrip("/")}/beak/skill/latest'
        with urllib.request.urlopen(urllib.request.Request(url), timeout=8) as r:
            latest = (json.loads(r.read()).get('skills') or {}).get('space-duck') or ''
        if not latest or _cmp_semver(cur, latest) >= 0:
            if verbose:
                print(f'[VERCHECK] installed={cur} latest={latest} — up to date',
                      file=sys.stderr)
            return
        if state.get('last_nudged') == latest:
            if verbose:
                print(f'[VERCHECK] already nudged for {latest} — silent',
                      file=sys.stderr)
            return

        # 0.8.11 [VER-0811] — CONTRACT FIX. 0.8.10 sent
        #   Authorization: Bearer <beak_key>  +  {"text": ...}
        # but /beak/tg/notify (lambda_function.py:14011-14017) reads ONLY the
        # X-Beak-Key header and requires {"spaceduck_id", "message"}. Every
        # nudge 401'd and the error was swallowed below, so the feature was
        # dead on arrival on every box. The retired daemon had it right.
        body = json.dumps({
            'spaceduck_id': sd_id,
            'message': (f'\u2b06\ufe0f space-duck update available: you are on '
                        f'{cur}, latest is {latest}.\n'
                        f'Run: clawhub update space-duck'),
        }).encode()
        req = urllib.request.Request(
            f'{api_base.rstrip("/")}/beak/tg/notify', data=body, method='POST',
            headers={'Content-Type': 'application/json',
                     'X-Beak-Key': beak_key,
                     'X-Spaceduck-ID': sd_id})
        with urllib.request.urlopen(req, timeout=8) as r:
            # 0.8.11 — HTTP 200 is NOT proof of delivery. The handler returns
            # 200 {"dispatched": false} when the owner's TG send fails (no
            # chat_id, dead token, Telegram reject). Suppressing on status
            # alone would mark the version nudged and go permanently silent
            # for an owner who never got the message. Require dispatched.
            ok = False
            if 200 <= r.status < 300:
                try:
                    ok = bool((json.loads(r.read()) or {}).get('dispatched'))
                except Exception:
                    ok = False
            if verbose:
                print(f'[VERCHECK] nudge ({cur} -> {latest}) HTTP {r.status} '
                      f'dispatched={ok}', file=sys.stderr)
        # Only suppress future nudges for this version if one actually landed.
        if ok:
            state['last_nudged'] = latest
            _save_version_state(state)
    except Exception as e:
        if verbose:
            print(f'[VERCHECK] skipped: {e}', file=sys.stderr)




def version_nudge_loop(beak_key, sd_id, api_base, verbose=False, interval=3600):
    """Long-lived caller for listeners without a pulse thread.

    The disk-persisted rate limit inside _version_check_once is what actually
    bounds network traffic to once a day; this wakes often enough that a box
    which is up for less than 24h at a stretch still gets its check in.
    """
    while True:
        try:
            _version_check_once(beak_key, sd_id, api_base, verbose)
        except Exception:
            pass
        time.sleep(interval)
