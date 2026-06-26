#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Keep runtime data OUTSIDE the skill directory by default.
STATE_BASE="${YUBOTO_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/openclaw/yuboto-omni-api}"
LOG_DIR="${YUBOTO_LOG_DIR:-$STATE_BASE/logs}"
STATE_DIR="$STATE_BASE/state"
mkdir -p "$LOG_DIR" "$STATE_DIR"

# Check for OCTAPUSH_API_KEY environment variable
if [ -z "${OCTAPUSH_API_KEY:-}" ]; then
  echo "ERROR: OCTAPUSH_API_KEY environment variable is not set." >&2
  echo "Set it via OpenClaw config (preferred) or export OCTAPUSH_API_KEY='your_key'" >&2
  exit 1
fi

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
LOG_FILE="$LOG_DIR/poll-$(date -u +%Y%m%d).log"

{
  echo "[$TS] poll-pending START"
  python3 "$BASE_DIR/scripts/yuboto_cli.py" --state-dir "$STATE_DIR" poll-pending
  echo "[$TS] poll-pending END"
} | tee -a "$LOG_FILE"
