#!/usr/bin/env bash
# Start Chrome on Linux + VNC with remote debugging for OpenClaw / zhihu_attach.py.
#
# Usage (inside the VNC desktop terminal):
#   bash scripts/start_chrome_debug.sh
# Then log in to Zhihu in that Chrome window.
#
# On the same machine:
#   python zhihu_attach.py --check
#
# Restart after closing the window (same profile, login usually kept):
#   bash scripts/start_chrome_debug.sh
# Or auto-start if not running:
#   bash scripts/ensure_chrome_debug.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

_check_cmd_hint() {
  if [[ -f "$SCRIPT_DIR/zhihu_publish.sh" ]]; then
    echo "bash $SCRIPT_DIR/zhihu_publish.sh --check --json"
  elif [[ -f "$SCRIPT_DIR/zhihu_attach_standalone.py" ]]; then
    echo "python3 $SCRIPT_DIR/zhihu_attach_standalone.py --check --json"
  else
    echo "python3 $(dirname "$SCRIPT_DIR")/zhihu_attach_standalone.py --check"
  fi
}

DETACH=0
if [[ "${1:-}" == "--detach" ]]; then
  DETACH=1
  shift
fi

DEBUG_PORT="${CHROME_DEBUG_PORT:-9222}"
# Dedicated profile dir, isolated from the system default Chrome profile
USER_DATA_DIR="${CHROME_USER_DATA_DIR:-$HOME/.chrome-zhihu-automation}"

mkdir -p "$USER_DATA_DIR"

CHROME=""
for candidate in \
  google-chrome-stable \
  google-chrome \
  chromium-browser \
  chromium; do
  if command -v "$candidate" >/dev/null 2>&1; then
    CHROME="$candidate"
    break
  fi
done

if [[ -z "$CHROME" ]]; then
  echo "Chrome/Chromium not found. Install google-chrome or chromium." >&2
  exit 1
fi

if curl -sf "http://127.0.0.1:${DEBUG_PORT}/json/version" >/dev/null 2>&1; then
  echo "Chrome debug port ${DEBUG_PORT} is already listening; skip relaunch."
  echo "Run: $(_check_cmd_hint)"
  exit 0
fi

# Chrome refuses to start as root unless --no-sandbox is set (crbug.com/638180)
EXTRA_ARGS=()
if [[ "$(id -u)" -eq 0 ]]; then
  EXTRA_ARGS+=(--no-sandbox --disable-setuid-sandbox)
  echo "Note: running as root; adding --no-sandbox (required by Chrome)."
fi
# Common on Linux VPS / small /dev/shm (avoids crashes or blank tabs)
EXTRA_ARGS+=(--disable-dev-shm-usage)

echo "Launching: $CHROME"
echo "  Debug port: $DEBUG_PORT"
echo "  Profile dir: $USER_DATA_DIR"
if ((${#EXTRA_ARGS[@]})); then
  echo "  Extra flags: ${EXTRA_ARGS[*]}"
fi
echo ""
CHROME_CMD=(
  "$CHROME"
  --remote-debugging-port="$DEBUG_PORT"
  --user-data-dir="$USER_DATA_DIR"
  --no-first-run
  --no-default-browser-check
  "${EXTRA_ARGS[@]}"
  "$@"
)

if [[ "$DETACH" -eq 1 ]]; then
  echo "Starting Chrome in background (profile keeps login cookies)..."
  nohup "${CHROME_CMD[@]}" >/tmp/chrome-zhihu-automation.log 2>&1 &
  echo "PID: $!"
  sleep 2
  if curl -sf "http://127.0.0.1:${DEBUG_PORT}/json/version" >/dev/null 2>&1; then
    echo "OK: debug port ${DEBUG_PORT} is up."
    echo "If Zhihu asks to log in again, use VNC once — then future restarts reuse this profile."
  else
    echo "WARN: port not ready yet. Check /tmp/chrome-zhihu-automation.log" >&2
    exit 1
  fi
  exit 0
fi

echo "Log in to Zhihu in this window, then run:"
echo "  $(_check_cmd_hint)"

exec "${CHROME_CMD[@]}"
