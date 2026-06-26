#!/usr/bin/env bash
set -euo pipefail

# Subagent watchdog:
# Wait until a deadline, then check for a completion marker file.
# If missing: emit a message, and optionally notify via OpenClaw messaging.

LABEL="${1:-}"
WAIT_SECONDS="${2:-}"

if [[ -z "$LABEL" ]]; then
  echo "usage: watch.sh <label> [wait_seconds]" >&2
  exit 2
fi

# Default: read from OpenClaw config and add +1 second
if [[ -z "${WAIT_SECONDS}" ]]; then
  WAIT_SECONDS="$(python3 - <<'PY'
import json, os
p=os.environ.get('OPENCLAW_CONFIG_PATH') or os.path.expanduser('~/.openclaw/openclaw.json')
obj=json.load(open(p))
secs=int(obj.get('caliban',{}).get('subagentWatchdog',{}).get('maxRuntimeSeconds',600))
print(secs+1)
PY
  )"
fi

STATE_DIR="${STATE_DIR:-$(pwd)/state}"
MARKER="$STATE_DIR/${LABEL}.done"

mkdir -p "$STATE_DIR"

sleep "$WAIT_SECONDS"

if [[ -f "$MARKER" ]]; then
  exit 0
fi

MSG="Subagent watchdog: no completion marker for '$LABEL' after ${WAIT_SECONDS}s."
echo "$MSG" >&2

# Optional notify via OpenClaw
OPENCLAW_BIN="${OPENCLAW_BIN:-/opt/homebrew/bin/openclaw}"
WATCHDOG_CHAT_ID="${WATCHDOG_CHAT_ID:-}"
WATCHDOG_CHANNEL="${WATCHDOG_CHANNEL:-telegram}"

if [[ -n "$WATCHDOG_CHAT_ID" ]] && [[ -x "$OPENCLAW_BIN" ]]; then
  "$OPENCLAW_BIN" message send --channel "$WATCHDOG_CHANNEL" --target "$WATCHDOG_CHAT_ID" --message "$MSG" --silent >/dev/null 2>&1 || true
fi

exit 1
