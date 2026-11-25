#!/usr/bin/env python3
"""
Space Duck — Actor-critic helper.

INTENT: Runs a critic-style pass over an agent's DRAFT reply before
        peck_responder.py sends it. Goal: surface flaws, sharpen the
        argument, or escalate when the responder is being asked to do
        something it shouldn't.

CALLED BY: peck_responder.py when the connection's `critic_mode` is
        'alternating' OR when the inbound message contains a
        <critic_request reason="..."/> marker.

INPUT (stdin, JSON):
    {
      "draft_reply":  "<the responder's proposed reply text>",
      "inbound":      {<original peck envelope JSON>},
      "connection":   {<resolved permissions dict>}
    }

OUTPUT (stdout, JSON):
    {
      "verdict":  "PASS" | "REVISE" | "BLOCK",
      "reason":   "short why",
      "rewrite":  "<revised reply if verdict=REVISE, else empty>"
    }

DOCTRINE: Lane A receiver = user infra runs the brain. This script lives
in the BYOA agent's local skill install and calls the local `claude`
CLI. No new server-side endpoints, no Lambda mutations.

ENV KNOBS:
    SPACEDUCK_CRITIC_MODEL   default: claude-haiku-4-5 (fast critic)
    SPACEDUCK_CRITIC_TIMEOUT default: 45
"""
import json, os, subprocess, sys, time
from pathlib import Path

# 0.8.17 — see _claudebin: systemd PATH hides user-local installs.
try:
    from _claudebin import resolve_claude, safe_cwd
except Exception:
    def resolve_claude():
        return 'claude'

    def safe_cwd():
        return os.path.expanduser('~')

HOME    = Path.home()
SD_DIR  = HOME / '.space-duck'
LOG     = SD_DIR / 'critic.log'
MODEL   = os.environ.get('SPACEDUCK_CRITIC_MODEL', 'claude-haiku-4-5')
TIMEOUT = int(os.environ.get('SPACEDUCK_CRITIC_TIMEOUT', '45'))


def _log(msg):
    line = f'[{time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}] critic {msg}\n'
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, 'a') as f:
            f.write(line)
    except Exception:
        pass
    sys.stderr.write(line)


def main():
    try:
        payload = json.loads(sys.stdin.read() or '{}')
    except json.JSONDecodeError as e:
        _log(f'stdin not JSON: {e}')
        # [HARDEN-073] fail closed: HOLD, never PASS, when the critic can't run
        print(json.dumps({'verdict': 'HOLD', 'reason': 'critic_bad_input', 'rewrite': ''}))
        return 0

    draft   = (payload.get('draft_reply') or '').strip()
    inbound = payload.get('inbound') or {}
    conn    = payload.get('connection') or {}
    if not draft:
        print(json.dumps({'verdict': 'PASS', 'reason': 'empty_draft', 'rewrite': ''}))
        return 0

    sender_name  = inbound.get('sender_name') or 'a peer'
    inbound_text = (inbound.get('message') or inbound.get('text') or '').strip()

    # Critic prompt — terse, structured. The CLI output MUST be parseable
    # JSON so we never silently send half-baked replies.
    prompt = (
        '# Critic pass\n'
        f'Peer "{sender_name}" sent us:\n> {inbound_text[:1500]}\n\n'
        f'Our draft reply is:\n> {draft[:1500]}\n\n'
        'Review the draft. Return a JSON object with three fields:\n'
        '  "verdict": "PASS" if the draft is good as-is,\n'
        '             "REVISE" if it needs improvement,\n'
        '             "BLOCK" if it leaks data, escalates wrongly, or '
        'is otherwise unsafe to send.\n'
        '  "reason": one short sentence.\n'
        '  "rewrite": the improved reply text, only when verdict=REVISE; '
        'empty otherwise.\n\n'
        'Return ONLY the JSON object. No preamble, no markdown fence.'
    )

    # [CRB-1] The critic reviews text and returns JSON — it needs NO tools.
    # Inbound-peck content is attacker-influenced, so never run it with
    # bypassed permissions. Disable the entire toolset (`--tools ""`) instead:
    # nothing to approve (so --print never hangs) and nothing to abuse if the
    # model is prompt-injected by the peer's message.
    cmd = [resolve_claude(), '--print', '--tools', '',
           '--model', MODEL, prompt]
    try:
        # cwd pinned: a deleted inherited cwd makes the CLI exit 1 before it
        # reads the prompt, which fails the critic CLOSED and holds every reply.
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=TIMEOUT, cwd=safe_cwd())
    except subprocess.TimeoutExpired:
        _log('claude CLI timed out — HOLD (fail closed)')  # [HARDEN-073]
        print(json.dumps({'verdict': 'HOLD', 'reason': 'critic_timeout', 'rewrite': ''}))
        return 0
    except FileNotFoundError:
        _log('claude CLI missing — HOLD (fail closed)')  # [HARDEN-073]
        print(json.dumps({'verdict': 'HOLD', 'reason': 'critic_unavailable', 'rewrite': ''}))
        return 0
    except Exception as e:
        _log(f'claude CLI error: {e}')  # [HARDEN-073]
        print(json.dumps({'verdict': 'HOLD', 'reason': f'critic_error:{e}', 'rewrite': ''}))
        return 0

    if out.returncode != 0:
        _log(f'claude CLI exit {out.returncode}: {out.stderr[:200]}')  # [HARDEN-073]
        print(json.dumps({'verdict': 'HOLD', 'reason': 'critic_nonzero_exit', 'rewrite': ''}))
        return 0

    raw = (out.stdout or '').strip()
    # Strip common preambles defensively.
    if raw.startswith('```'):
        raw = raw.strip('`').strip()
        if raw.lower().startswith('json'):
            raw = raw[4:].strip()
    try:
        parsed = json.loads(raw)
        verdict = (parsed.get('verdict') or 'HOLD').upper()
        if verdict not in ('PASS', 'REVISE', 'BLOCK'):
            verdict = 'HOLD'  # [HARDEN-073] unknown verdict = fail closed
        rewrite = (parsed.get('rewrite') or '').strip()
        reason  = (parsed.get('reason') or '').strip()[:200]
        _log(f'verdict={verdict} reason={reason!r}')
        print(json.dumps({'verdict': verdict, 'reason': reason, 'rewrite': rewrite}))
    except json.JSONDecodeError:
        _log('critic CLI returned non-JSON — HOLD (fail closed)')  # [HARDEN-073]
        print(json.dumps({'verdict': 'HOLD', 'reason': 'critic_unparseable', 'rewrite': ''}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
