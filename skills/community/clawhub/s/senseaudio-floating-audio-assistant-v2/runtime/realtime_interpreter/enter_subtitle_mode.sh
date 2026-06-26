#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
STATE_DIR="$WORKSPACE_DIR/state/realtime_interpreter"
STATE_FILE="$STATE_DIR/audio_route_state.sh"

if ! command -v SwitchAudioSource >/dev/null 2>&1; then
  echo "SwitchAudioSource not found. If Homebrew is installed, run: brew install switchaudio-osx" >&2
  exit 1
fi

pick_route_device() {
  local device
  for device in "多输出设备" "Multi-Output Device"; do
    if SwitchAudioSource -a | grep -Fxq "$device"; then
      printf '%s\n' "$device"
      return 0
    fi
  done
  return 1
}

device_exists() {
  local device="$1"
  [ -n "$device" ] && SwitchAudioSource -a | grep -Fxq "$device"
}

quote_for_shell() {
  printf "%s" "$1" | sed "s/'/'\\\\''/g"
}

route_device="$(pick_route_device || true)"
if [ -z "$route_device" ]; then
  echo "No Multi-Output Device found. Please create one in Audio MIDI Setup first." >&2
  exit 1
fi

mkdir -p "$STATE_DIR"

current_output="$(SwitchAudioSource -t output -c 2>/dev/null || true)"
current_system="$(SwitchAudioSource -t system -c 2>/dev/null || true)"
current_volume="$(osascript -e 'output volume of (get volume settings)' 2>/dev/null || true)"

saved_output="$current_output"
saved_system="$current_system"
saved_volume="$current_volume"

if [ -f "$STATE_FILE" ]; then
  # shellcheck disable=SC1090
  source "$STATE_FILE"
  if [ "${ACTIVE:-0}" = "1" ]; then
    saved_output="${PREV_OUTPUT_DEVICE:-$saved_output}"
    saved_system="${PREV_SYSTEM_DEVICE:-$saved_system}"
    saved_volume="${PREV_OUTPUT_VOLUME:-$saved_volume}"
  fi
fi

{
  printf 'ACTIVE=1\n'
  printf "PREV_OUTPUT_DEVICE='%s'\n" "$(quote_for_shell "$saved_output")"
  printf "PREV_SYSTEM_DEVICE='%s'\n" "$(quote_for_shell "$saved_system")"
  printf "PREV_OUTPUT_VOLUME='%s'\n" "$(quote_for_shell "$saved_volume")"
  printf "ROUTE_DEVICE='%s'\n" "$(quote_for_shell "$route_device")"
} > "$STATE_FILE"

if [ "$current_output" != "$route_device" ] && device_exists "$route_device"; then
  SwitchAudioSource -t output -s "$route_device" >/dev/null
fi
if [ "$current_system" != "$route_device" ] && device_exists "$route_device"; then
  SwitchAudioSource -t system -s "$route_device" >/dev/null
fi

echo "Subtitle mode enabled."
echo "Audio route device: $route_device"
echo "Previous output device: ${saved_output:-unknown}"
