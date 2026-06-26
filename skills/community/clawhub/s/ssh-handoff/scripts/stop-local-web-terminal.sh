#!/usr/bin/env bash
set -euo pipefail

PID="${1:-}"
SESSION_NAME="${2:-}"

if [[ -n "$PID" ]]; then
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    echo "Stopped PID $PID"
  else
    echo "PID $PID not running"
  fi
fi

if [[ -n "$SESSION_NAME" ]]; then
  echo "tmux session preserved: $SESSION_NAME"
fi

echo "Cleanup done"
