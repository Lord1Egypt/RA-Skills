#!/usr/bin/env bash
# openclaw_brain.sh — Stage-1 NATIVE brain wrapper for reply_with_claude.sh
# (skill 0.4.26). Routes a Telegram message through the duck's OWN embedded
# OpenClaw agent (`openclaw agent --local`) so replies carry persistent
# per-chat conversation memory + the duck's OpenClaw workspace context,
# instead of the stateless one-shot claude CLI link.
#
# Contract (reply_with_claude.sh run_brain): composed prompt arrives on
# STDIN, reply text goes to STDOUT, exit 0. Non-zero / empty / the
# __NO_CAPACITY__ sentinel → responder falls through to the Stage-2 chain,
# so a fault here can never kill replies.
#
# Design choice: we deliberately DO NOT feed the composed prompt (SOUL.md +
# MEMORY.md re-injected every turn) into a persistent session — that would
# duplicate identity context on every message and bloat the session. The
# duck's identity lives in its OpenClaw workspace (SOUL.md/AGENTS.md/
# MEMORY.md, loaded by OpenClaw itself); we pass only the raw incoming
# message, pulled from SD_PAYLOAD (exported by reply_with_claude.sh).
# STDIN is drained and used only as a fallback if SD_PAYLOAD is absent.
#
# Env knobs (set in the listener systemd unit):
#   HOME                     duck's own home (config at $HOME/.openclaw/) — required
#   IS_SANDBOX=1             required on root installs: the openclaw claude-cli
#                            backend passes --dangerously-skip-permissions,
#                            which the claude CLI refuses under root unless
#                            sandboxed (same guard class as the 0.4.23/0.4.25
#                            responder fixes; this is how the main gateway runs)
#   SPACEDUCK_OC_TIMEOUT     seconds per agent turn (default 110)
#   SPACEDUCK_OC_SESSION_PREFIX  session key prefix (default agent:main:tg)
set -u

TIMEOUT="${SPACEDUCK_OC_TIMEOUT:-110}"
PREFIX="${SPACEDUCK_OC_SESSION_PREFIX:-agent:main:tg}"

STDIN_PROMPT="$(cat || true)"

command -v openclaw >/dev/null 2>&1 || { echo "openclaw not on PATH" >&2; exit 3; }

# Derive message + chat-scoped session key from SD_PAYLOAD; fall back to stdin.
eval "$(python3 - <<'PY'
import json, os, re, shlex
msg, chat = '', 'default'
try:
    p = json.loads(os.environ.get('SD_PAYLOAD', '') or '{}')
    tg = p.get('telegram_update') or p  # forward envelope or bare update
    m = tg.get('message') or tg.get('edited_message') or {}
    msg = (m.get('text') or m.get('caption') or '').strip()
    cid = (m.get('chat') or {}).get('id')
    frm = m.get('from') or {}
    sender = frm.get('first_name') or frm.get('username') or 'a user'
    if cid is not None:
        chat = re.sub(r'[^0-9A-Za-z_-]', '_', str(cid))
    if msg:
        msg = f'[Telegram message from {sender}] {msg}'
except Exception:
    pass
print('MSG=' + shlex.quote(msg))
print('CHAT=' + shlex.quote(chat))
PY
)"

[ -n "$MSG" ] || MSG="$STDIN_PROMPT"
[ -n "$MSG" ] || { echo "no message text" >&2; exit 4; }

OUT="$(timeout "$TIMEOUT" openclaw agent --local --json \
        --session-key "${PREFIX}-${CHAT}" -m "$MSG" \
        --timeout "$TIMEOUT" 2>/dev/null)"
RC=$?
[ $RC -eq 0 ] || { echo "openclaw agent exit $RC" >&2; exit 5; }

REPLY="$(printf '%s' "$OUT" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(1)
payloads = d.get('payloads') or (d.get('result') or {}).get('payloads') or []
texts = [p.get('text') or '' for p in payloads]
out = '\n\n'.join(t for t in texts if t.strip()).strip()
print(out)
")"

[ -n "$REPLY" ] || { echo "empty reply from openclaw agent" >&2; exit 6; }
printf '%s\n' "$REPLY"
