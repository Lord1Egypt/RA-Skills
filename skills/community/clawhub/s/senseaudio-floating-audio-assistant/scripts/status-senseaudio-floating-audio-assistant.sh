#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
RUNS_DIR="$STATE_DIR/runs"
ENV_FILE="$WORKSPACE_DIR/.env"

echo "SenseAudio Floating Audio Assistant"
echo

if pgrep -fl "subtitle_overlay_app|AudioClawOverlay|runner.py|mic_pcm_stream" >/dev/null 2>&1; then
  echo "Process: running"
  pgrep -fl "subtitle_overlay_app|AudioClawOverlay|runner.py|mic_pcm_stream" | sed 's/^/  /'
else
  echo "Process: not running"
fi

echo
if [ -f "$ENV_FILE" ]; then
  if grep -Eq '^(SENSEAUDIO_API_KEY|AUDIOCLAW_ASR_API_KEY)=' "$ENV_FILE"; then
    echo "SenseAudio key: configured"
  else
    echo "SenseAudio key: .env exists, but no SENSEAUDIO_API_KEY/AUDIOCLAW_ASR_API_KEY entry was found"
  fi
else
  echo "SenseAudio key: workspace .env missing"
fi

echo
if [ -d "$RUNS_DIR" ]; then
  run_count="$(find "$RUNS_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')"
  latest_run="$(find "$RUNS_DIR" -mindepth 1 -maxdepth 1 -type d -print 2>/dev/null | sort | tail -n 1)"
  echo "Runs: $run_count"
  if [ -n "${latest_run:-}" ]; then
    echo "Latest: $latest_run"
  fi
else
  echo "Runs: none yet"
fi

echo
if [ -d "$TOOL_DIR" ]; then
  echo "Tool dir: $TOOL_DIR"
else
  echo "Tool dir missing: $TOOL_DIR"
fi
