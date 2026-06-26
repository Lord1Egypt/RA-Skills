#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 TEXT_FILE [VOICE] [MAX_DIRECT_CHARS]" >&2
  exit 1
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${OPENCLAW_WORKSPACE:-$(pwd)}"
TEXT_FILE="$1"
VOICE="${2:-ru-RU-DmitryNeural}"
MAX_DIRECT_CHARS="${3:-280}"
CANONICAL="$WORKSPACE/tmp/voice-mode-latest.mp3"
STATE_DIR="$WORKSPACE/skills/text-to-voice-local/state"
LAST_FILE="$STATE_DIR/last-output.txt"
mkdir -p "$STATE_DIR" "$WORKSPACE/tmp"
"$SCRIPT_DIR/voice_reply.sh" "$TEXT_FILE" "$CANONICAL" "$VOICE" "$MAX_DIRECT_CHARS" >/dev/null
printf '%s\n' "$CANONICAL" > "$LAST_FILE"
printf '%s\n' "$CANONICAL"
