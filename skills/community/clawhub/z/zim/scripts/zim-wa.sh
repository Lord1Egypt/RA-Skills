#!/usr/bin/env bash
# zim-wa.sh — OpenClaw-friendly wrapper for Zim WhatsApp agent
# Usage: bash zim-wa.sh "Find flights DXB to CPH May 1" [user_id]
#
# Outputs JSON: {"response": "...", "success": true/false}

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ZIM_ROOT="$(dirname "$SCRIPT_DIR")"
VENV="$ZIM_ROOT/.venv/bin/python3"

MESSAGE="${1:?Usage: zim-wa.sh MESSAGE [USER_ID]}"
USER_ID="${2:-whatsapp:+971544042230}"

# Required: set these in your environment before running
if [ -z "${TRAVELPAYOUTS_TOKEN:-}" ]; then
  echo '{"error": "TRAVELPAYOUTS_TOKEN not set", "success": false}'
  exit 1
fi
export TRAVELPAYOUTS_TOKEN
export TRAVELPAYOUTS_MARKER="${TRAVELPAYOUTS_MARKER:-}"

exec "$VENV" "$SCRIPT_DIR/zim-whatsapp-handler.py" \
  --message "$MESSAGE" \
  --user-id "$USER_ID" \
  --json
