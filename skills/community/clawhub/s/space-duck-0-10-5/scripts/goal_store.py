#!/usr/bin/env python3
"""
goal_store.py — D1 goal-loop layer for the Space Duck auto-responder.

The organizing principle behind D2–D5: an auto-reply is a bounded TASK, not a chat
reflex. Each peck thread is a GOAL. The responder pursues it until the objective is
met (the model signals <goal_status>complete</goal_status>), it's blocked, or the
round budget is spent — then the thread is CLOSED and further pecks on it are ignored
(they must open a NEW goal). "Exchange pleasantries" is never an objective, so banter
has no goal to attach to.

FAIL-SAFE BY DESIGN: every public function swallows its own errors and degrades to a
no-op. If anything here breaks, the responder falls straight back to D3/D2/D5 — this
layer can only ADD a termination signal, never remove existing safety.

Store: ~/.space-duck/goals.json  { goal_id: {objective, status, rounds_used, opened_at} }
Status: open | complete | blocked  (closed = complete|blocked)
"""
import json, os, time
from pathlib import Path

SD_DIR = Path(os.environ.get('SPACEDUCK_DIR', str(Path.home() / '.space-duck')))
STORE = SD_DIR / 'goals.json'
MAX_GOALS = 200          # ring-cap the store so it can't grow unbounded

def _load():
    try:
        return json.loads(STORE.read_text())
    except Exception:
        return {}

def _save(d):
    try:
        # keep only the most-recent MAX_GOALS by opened_at
        if len(d) > MAX_GOALS:
            items = sorted(d.items(), key=lambda kv: kv[1].get('opened_at', 0))
            d = dict(items[-MAX_GOALS:])
        STORE.parent.mkdir(parents=True, exist_ok=True)
        STORE.write_text(json.dumps(d)[:500000])
    except Exception:
        pass

def status_of(goal_id: str):
    """Return 'open'|'complete'|'blocked' for an existing goal, or None if unknown.
    Fail-safe: None on any error (→ responder treats it as a fresh/no-goal thread)."""
    if not goal_id:
        return None
    try:
        return _load().get(goal_id, {}).get('status')
    except Exception:
        return None

def open_or_attach(goal_id: str, objective: str):
    """Open a goal for this thread if new, else bump rounds_used. Returns the goal dict
    (or None on error). Never raises."""
    if not goal_id:
        return None
    try:
        d = _load()
        g = d.get(goal_id)
        if g is None:
            g = {'objective': (objective or '')[:400], 'status': 'open',
                 'rounds_used': 1, 'opened_at': int(time.time())}
        else:
            g['rounds_used'] = int(g.get('rounds_used', 0)) + 1
        d[goal_id] = g
        _save(d)
        return g
    except Exception:
        return None

def close(goal_id: str, status: str):
    """Mark a goal complete|blocked. Never raises."""
    if not goal_id or status not in ('complete', 'blocked'):
        return
    try:
        d = _load()
        g = d.get(goal_id) or {'objective': '', 'rounds_used': 0, 'opened_at': int(time.time())}
        g['status'] = status
        g['closed_at'] = int(time.time())
        d[goal_id] = g
        _save(d)
    except Exception:
        pass

# The model is asked to append exactly one of these when the objective is resolved.
import re as _re
GOAL_STATUS_RE = _re.compile(r'<goal_status>\s*(complete|blocked|continue)\s*</goal_status>',
                             _re.IGNORECASE)

def parse_goal_status(reply_text: str):
    """Return 'complete'|'blocked'|'continue'|None from the model's reply. Never raises."""
    try:
        m = GOAL_STATUS_RE.search(reply_text or '')
        return m.group(1).lower() if m else None
    except Exception:
        return None

def strip_goal_status(reply_text: str) -> str:
    """Remove the <goal_status> tag so it never ships in the peck body."""
    try:
        return GOAL_STATUS_RE.sub('', reply_text or '').strip()
    except Exception:
        return reply_text

def goal_framing(objective: str, rounds_left) -> str:
    """System-prompt fragment injected into the compose so the reply stays on-goal and
    signals completion. Kept short + additive."""
    obj = (objective or 'the inbound request')[:300]
    return (
        f'\n\nGOAL-LOOP: You are working a single objective with this peer: "{obj}". '
        f'Reply ONLY to advance that objective. At the very END of your reply text and '
        f'INSIDE the <peck_reply> tags, append exactly <goal_status>complete</goal_status> '
        f'when the objective is fully resolved (the peer needs nothing further from you), '
        f'or <goal_status>blocked</goal_status> if you cannot proceed without the owner/peer. '
        f'Append neither while the objective is still in progress. '
        f'(~{rounds_left} rounds left before the hard cap.) The tag is stripped before the peck ships.'
    )

if __name__ == '__main__':
    import tempfile
    SD_DIR = Path(tempfile.mkdtemp()); STORE = SD_DIR / 'goals.json'
    ok = 0; tot = 0
    def check(label, cond):
        global ok, tot; tot += 1; ok += bool(cond)
        print(f"  {'✓' if cond else '✗'} {label}")

    GID = 'peck_root_abc'
    g = open_or_attach(GID, 'Seed a test job and send the job ID')
    check('open creates goal, status open', g and g['status'] == 'open' and g['rounds_used'] == 1)
    check('status_of returns open', status_of(GID) == 'open')
    g2 = open_or_attach(GID, 'ignored second objective')
    check('attach bumps rounds_used to 2', g2 and g2['rounds_used'] == 2)
    check('objective preserved on attach', g2['objective'] == 'Seed a test job and send the job ID')

    check('parse complete', parse_goal_status('Here is the job ID: J123. <goal_status>complete</goal_status>') == 'complete')
    check('parse blocked', parse_goal_status('Need creds first. <GOAL_STATUS>blocked</GOAL_STATUS>') == 'blocked')
    check('parse none when absent', parse_goal_status('just a normal reply') is None)
    check('strip removes tag', strip_goal_status('done J123 <goal_status>complete</goal_status>') == 'done J123')

    close(GID, 'complete')
    check('close sets complete', status_of(GID) == 'complete')
    check('unknown goal → None', status_of('nope') is None)
    check('goal_framing mentions objective + tag', 'goal_status>complete' in goal_framing('do X', 3))
    print(f"RESULT: {ok}/{tot} correct")
