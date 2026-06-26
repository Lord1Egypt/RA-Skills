#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
START_SCRIPT="$TOOL_DIR/start_system_subtitle_overlay.sh"
ENV_FILE="$WORKSPACE_DIR/.env"

if [ ! -f "$START_SCRIPT" ]; then
  echo "SenseAudio floating audio assistant launcher not found: $START_SCRIPT" >&2
  exit 1
fi

if ! command -v swiftc >/dev/null 2>&1; then
  echo "swiftc not found. Install Xcode Command Line Tools before launching the native overlay." >&2
  exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
  echo "Warning: $ENV_FILE is missing. SenseAudio ASR/TTS/music features may not work until SENSEAUDIO_API_KEY is configured." >&2
fi

exec bash "$START_SCRIPT" "$@"
