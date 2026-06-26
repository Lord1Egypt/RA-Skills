#!/usr/bin/env bash
# dashboard.sh — Start, stop, or check the spend-ledger dashboard server.
#
# Usage:
#   dashboard.sh start   — Start the dashboard server (background)
#   dashboard.sh stop    — Stop the dashboard server
#   dashboard.sh status  — Check if the dashboard is running
#   dashboard.sh url     — Print the dashboard URL

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/../server"
DATA_DIR="$SCRIPT_DIR/../data"
PID_FILE="$DATA_DIR/dashboard.pid"
PORT="${SPEND_LEDGER_PORT:-18920}"

mkdir -p "$DATA_DIR"

case "${1:-status}" in
  start)
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
      echo "Dashboard already running (PID $(cat "$PID_FILE"))"
      echo "http://127.0.0.1:${PORT}"
      exit 0
    fi
    node "$SERVER_DIR/server.js" &
    echo $! > "$PID_FILE"
    echo "Dashboard started (PID $!)"
    echo "http://127.0.0.1:${PORT}"
    ;;
  stop)
    if [ -f "$PID_FILE" ]; then
      PID=$(cat "$PID_FILE")
      if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        echo "Dashboard stopped (PID $PID)"
      else
        echo "Dashboard not running (stale PID file)"
      fi
      rm -f "$PID_FILE"
    else
      echo "Dashboard not running"
    fi
    ;;
  status)
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
      echo "Dashboard running (PID $(cat "$PID_FILE"))"
      echo "http://127.0.0.1:${PORT}"
    else
      echo "Dashboard not running"
      rm -f "$PID_FILE" 2>/dev/null
    fi
    ;;
  url)
    echo "http://127.0.0.1:${PORT}"
    ;;
  *)
    echo "Usage: dashboard.sh {start|stop|status|url}" >&2
    exit 1
    ;;
esac
