#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEBUG_PORT="${CHROME_DEBUG_PORT:-9222}"
BASE="http://127.0.0.1:${DEBUG_PORT}"

port_up() {
  curl -sf "${BASE}/json/version" >/dev/null 2>&1
}

has_page() {
  curl -sf "${BASE}/json/list" 2>/dev/null | grep -q '"type": "page"'
}

ensure_page() {
  if has_page; then
    return 0
  fi
  curl -sf -X PUT "${BASE}/json/new?about:blank" >/dev/null 2>&1 || true
  sleep 0.5
}

wait_port() {
  local i
  for i in $(seq 1 20); do
    if port_up; then
      ensure_page
      return 0
    fi
    sleep 1
  done
  return 1
}

if port_up; then
  ensure_page
  echo "Chrome debug port ${DEBUG_PORT} already running."
  exit 0
fi

echo "Chrome not running on ${DEBUG_PORT}; starting..."
[[ -z "${DISPLAY:-}" ]] && echo "WARN: set DISPLAY=:1 for VNC"
bash "$SCRIPT_DIR/start_chrome_debug.sh" --detach

if wait_port; then
  echo "Chrome ready on ${DEBUG_PORT}."
  exit 0
fi

echo "Chrome failed to start on ${DEBUG_PORT}." >&2
exit 1
