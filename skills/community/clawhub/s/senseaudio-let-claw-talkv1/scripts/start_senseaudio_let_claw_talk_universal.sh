#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MAC_DEFAULT_PYTHON="/Library/Developer/CommandLineTools/usr/bin/python3"
VOICECLAW_PYTHON_BIN="${VOICECLAW_PYTHON_BIN:-}"

if [[ -z "$VOICECLAW_PYTHON_BIN" ]]; then
  if [[ "$(uname -s 2>/dev/null || true)" == "Darwin" && -x "$MAC_DEFAULT_PYTHON" ]]; then
    VOICECLAW_PYTHON_BIN="$MAC_DEFAULT_PYTHON"
  elif command -v python3 >/dev/null 2>&1; then
    VOICECLAW_PYTHON_BIN="$(command -v python3)"
  elif command -v python >/dev/null 2>&1; then
    VOICECLAW_PYTHON_BIN="$(command -v python)"
  else
    echo "python3 not found" >&2
    exit 1
  fi
fi

export VOICECLAW_TTS_MODE="${VOICECLAW_TTS_MODE:-senseaudio}"
export VOICECLAW_CAPTURE_BACKEND="${VOICECLAW_CAPTURE_BACKEND:-auto}"
export VOICECLAW_VOICE_ID="${VOICECLAW_VOICE_ID:-male_0004_a}"
export VOICECLAW_EMOTION="${VOICECLAW_EMOTION:-calm}"
export VOICECLAW_TTS_SPEED="${VOICECLAW_TTS_SPEED:-1.25}"
export VOICECLAW_SENSEAUDIO_STREAMING_TTS="${VOICECLAW_SENSEAUDIO_STREAMING_TTS:-0}"
export VOICECLAW_SENSEAUDIO_STREAMING_BACKEND="${VOICECLAW_SENSEAUDIO_STREAMING_BACKEND:-auto}"
export VOICECLAW_WAKE_PHRASE="${VOICECLAW_WAKE_PHRASE:-贾维斯}"
export VOICECLAW_SLEEP_PHRASE="${VOICECLAW_SLEEP_PHRASE:-贾维斯休息}"
export VOICECLAW_STATUS_SOUNDS="${VOICECLAW_STATUS_SOUNDS:-0}"
export VOICECLAW_SPEAKER_BACKEND="${VOICECLAW_SPEAKER_BACKEND:-none}"
export VOICECLAW_WESPEAKER_THRESHOLD="${VOICECLAW_WESPEAKER_THRESHOLD:-0.72}"
export VOICECLAW_WESPEAKER_PORT="${VOICECLAW_WESPEAKER_PORT:-18567}"
export VOICECLAW_WESPEAKER_PYTHON="${VOICECLAW_WESPEAKER_PYTHON:-$HOME/.audioclaw/workspace/tools/wespeaker/.venv/bin/python}"
export VOICECLAW_EXTRA_ARGS="${VOICECLAW_EXTRA_ARGS:-}"
export VOICECLAW_PYTHON_BIN

cmd=(
  "$VOICECLAW_PYTHON_BIN"
  "$SCRIPT_DIR/run_continuous_voice_assistant.py"
  --tts-mode "$VOICECLAW_TTS_MODE"
  --capture-backend "$VOICECLAW_CAPTURE_BACKEND"
  --voice-id "$VOICECLAW_VOICE_ID"
  --emotion "$VOICECLAW_EMOTION"
  --tts-speed "$VOICECLAW_TTS_SPEED"
  --speaker-verification-backend "$VOICECLAW_SPEAKER_BACKEND"
  --wespeaker-threshold "$VOICECLAW_WESPEAKER_THRESHOLD"
  --wespeaker-port "$VOICECLAW_WESPEAKER_PORT"
  --wespeaker-python "$VOICECLAW_WESPEAKER_PYTHON"
)

case "${VOICECLAW_STATUS_SOUNDS:-0}" in
  1|true|TRUE|True|yes|YES|Yes|on|ON|On)
    cmd+=(--status-sounds)
    ;;
  *)
    cmd+=(--no-status-sounds)
    ;;
esac

if [[ $# -gt 0 ]]; then
  cmd+=("$@")
fi

if [[ -n "$VOICECLAW_EXTRA_ARGS" ]]; then
  read -r -a extra_args <<<"$VOICECLAW_EXTRA_ARGS"
  cmd+=("${extra_args[@]}")
fi

exec "${cmd[@]}"
