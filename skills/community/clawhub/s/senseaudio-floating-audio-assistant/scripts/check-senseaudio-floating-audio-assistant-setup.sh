#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
CHECK_SCRIPT="$TOOL_DIR/check_system_audio_setup.sh"
ENV_FILE="$WORKSPACE_DIR/.env"

echo "Checking SenseAudio floating audio assistant setup..."
echo

for bin in bash python3 swiftc; do
  if command -v "$bin" >/dev/null 2>&1; then
    echo "$bin: ok ($(command -v "$bin"))"
  else
    echo "$bin: missing"
  fi
done

if command -v SwitchAudioSource >/dev/null 2>&1; then
  echo "SwitchAudioSource: ok ($(command -v SwitchAudioSource))"
else
  echo "SwitchAudioSource: missing (install switchaudio-osx or put SwitchAudioSource in PATH)"
fi

if command -v audioclaw >/dev/null 2>&1; then
  echo "AudioClaw agent: CLI available ($(command -v audioclaw))"
else
  echo "AudioClaw agent: expected from host AudioClaw runtime; CLI is not on PATH"
fi

echo
if [ -f "$ENV_FILE" ]; then
  if grep -Eq '^(SENSEAUDIO_API_KEY|AUDIOCLAW_ASR_API_KEY)=' "$ENV_FILE"; then
    echo "SenseAudio key: configured in $ENV_FILE"
  else
    echo "SenseAudio key: missing in $ENV_FILE"
  fi
else
  echo "SenseAudio key: $ENV_FILE not found"
fi

echo
if [ -f "$CHECK_SCRIPT" ]; then
  bash "$CHECK_SCRIPT"
else
  echo "Audio setup checker not found: $CHECK_SCRIPT" >&2
  exit 1
fi
