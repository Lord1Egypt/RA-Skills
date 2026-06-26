#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
STATE_FILE="$WORKSPACE_DIR/state/realtime_interpreter/audio_route_state.sh"
SKIP_OVERLAY_KILL=0

if [ "${1:-}" = "--skip-overlay-kill" ]; then
  SKIP_OVERLAY_KILL=1
fi

if ! command -v SwitchAudioSource >/dev/null 2>&1; then
  echo "SwitchAudioSource not found. If Homebrew is installed, run: brew install switchaudio-osx" >&2
  exit 1
fi

device_exists() {
  local device="$1"
  [ -n "$device" ] && SwitchAudioSource -a | grep -Fxq "$device"
}

if [ "$SKIP_OVERLAY_KILL" -ne 1 ]; then
  pkill -f "$SCRIPT_DIR/subtitle_overlay_app" >/dev/null 2>&1 || true
  pkill -f "$SCRIPT_DIR/AudioClawOverlay.app/Contents/MacOS/subtitle_overlay_app" >/dev/null 2>&1 || true
  sleep 1
  pkill -9 -f "$SCRIPT_DIR/subtitle_overlay_app" >/dev/null 2>&1 || true
  pkill -9 -f "$SCRIPT_DIR/AudioClawOverlay.app/Contents/MacOS/subtitle_overlay_app" >/dev/null 2>&1 || true
fi

pkill -f "$SCRIPT_DIR/runner.py" >/dev/null 2>&1 || true
pkill -f "$SCRIPT_DIR/mic_pcm_stream" >/dev/null 2>&1 || true
sleep 1
pkill -9 -f "$SCRIPT_DIR/runner.py" >/dev/null 2>&1 || true
pkill -9 -f "$SCRIPT_DIR/mic_pcm_stream" >/dev/null 2>&1 || true

if [ -f "$STATE_FILE" ]; then
  # shellcheck disable=SC1090
  source "$STATE_FILE"

  if device_exists "${PREV_OUTPUT_DEVICE:-}"; then
    SwitchAudioSource -t output -s "$PREV_OUTPUT_DEVICE" >/dev/null || true
  fi
  if device_exists "${PREV_SYSTEM_DEVICE:-}"; then
    SwitchAudioSource -t system -s "$PREV_SYSTEM_DEVICE" >/dev/null || true
  fi

  if [[ "${PREV_OUTPUT_VOLUME:-}" =~ ^[0-9]+$ ]]; then
    osascript -e "set volume output volume ${PREV_OUTPUT_VOLUME}" >/dev/null 2>&1 || true
  fi

  rm -f "$STATE_FILE"
fi

echo "Subtitle mode disabled."
echo "Current output device: $(SwitchAudioSource -t output -c 2>/dev/null || echo unknown)"
