#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)}"
PORT="${OVERLAY_PORT:-8787}"
LOG="$WORKSPACE/streaming-tests/http-server.log"

mkdir -p "$WORKSPACE/streaming-tests"

if ss -ltn | grep -q ":$PORT "; then
  echo "Overlay server already listening on :$PORT"
else
  nohup python3 -m http.server "$PORT" --directory "$WORKSPACE" > "$LOG" 2>&1 &
  sleep 1
  echo "Started overlay server on :$PORT"
fi

IP=$(hostname -I | awk '{print $1}')
echo "LAN base URL: http://$IP:$PORT"
