#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
STOP_SCRIPT="$TOOL_DIR/stop_system_subtitle_overlay.sh"

if [ ! -f "$STOP_SCRIPT" ]; then
  echo "SenseAudio floating audio assistant stop script not found: $STOP_SCRIPT" >&2
  exit 1
fi

exec bash "$STOP_SCRIPT" "$@"
