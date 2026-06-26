#!/usr/bin/env bash
# If debug Chrome is not running, start it in the background (same user-data-dir).
# Login cookies live in the profile dir — closing the window does not delete them.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEBUG_PORT="${CHROME_DEBUG_PORT:-9222}"

if curl -sf "http://127.0.0.1:${DEBUG_PORT}/json/version" >/dev/null 2>&1; then
  echo "Chrome debug port ${DEBUG_PORT} already running."
  exit 0
fi

echo "Chrome not running on ${DEBUG_PORT}; starting..."
if [[ -z "${DISPLAY:-}" ]]; then
  echo "WARN: DISPLAY is not set. Chrome may not show on VNC."
  echo "  Example: export DISPLAY=:1   (match your VNC session)"
fi
bash "$SCRIPT_DIR/start_chrome_debug.sh" --detach
echo "If --check fails with 401, open VNC and log in to Zhihu once in this Chrome profile."
