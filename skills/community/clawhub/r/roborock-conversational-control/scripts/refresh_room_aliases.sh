#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="${JOJO_CONFIG_FILE:-$SKILL_DIR/jojo.env}"

if [[ -f "$CONFIG_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
fi

DEVICE_ID="${JOJO_DEVICE_ID:-}"
ROBOROCK_BIN="${ROBOROCK_BIN:-}"

if [[ -z "$ROBOROCK_BIN" ]]; then
  if command -v roborock >/dev/null 2>&1; then
    ROBOROCK_BIN="$(command -v roborock)"
  elif [[ -x "$HOME/.local/bin/roborock" ]]; then
    ROBOROCK_BIN="$HOME/.local/bin/roborock"
  else
    echo "Could not find roborock CLI." >&2
    exit 1
  fi
fi

if [[ -z "$DEVICE_ID" ]]; then
  echo "Missing JOJO_DEVICE_ID. Set it in $CONFIG_FILE or your shell." >&2
  exit 1
fi

"$ROBOROCK_BIN" rooms --device_id "$DEVICE_ID" | python3 -c '
import json, re, sys
data = json.load(sys.stdin)
rooms = data.get("rooms", [])
for room in rooms:
    raw_name = str(room.get("rawName", "")).strip()
    segment = room.get("segmentId")
    env_name = re.sub(r"[^A-Z0-9]+", "_", raw_name.upper()).strip("_")
    print(f"ROOM_{env_name}=\"{segment}\"")
'
