#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT/storage/logs"
mkdir -p "$LOG_DIR"

if [ -f "$LOG_DIR/api.pid" ] && kill -0 "$(cat "$LOG_DIR/api.pid")" 2>/dev/null; then
  echo "API already running: $(cat "$LOG_DIR/api.pid")"
else
  cd "$ROOT"
  nohup python3 -m uvicorn services.api.app.main:app --host 127.0.0.1 --port 8000 >"$LOG_DIR/api.log" 2>&1 &
  echo $! > "$LOG_DIR/api.pid"
  echo "API started on http://127.0.0.1:8000"
fi

if [ -f "$LOG_DIR/web.pid" ] && kill -0 "$(cat "$LOG_DIR/web.pid")" 2>/dev/null; then
  echo "Web already running: $(cat "$LOG_DIR/web.pid")"
else
  cd "$ROOT/apps/web"
  nohup npm run dev -- --host 127.0.0.1 --port 5173 >"$LOG_DIR/web.log" 2>&1 &
  echo $! > "$LOG_DIR/web.pid"
  echo "Web started on http://127.0.0.1:5173"
fi

echo "Open http://127.0.0.1:5173"
