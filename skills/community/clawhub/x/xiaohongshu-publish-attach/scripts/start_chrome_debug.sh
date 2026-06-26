#!/usr/bin/env bash
# Start Chrome with remote debugging (shared profile with zhihu-publish-attach).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

_check_hint() {
  echo "bash $SCRIPT_DIR/xhs_publish.sh --check --json"
}

DETACH=0
[[ "${1:-}" == "--detach" ]] && DETACH=1 && shift

DEBUG_PORT="${CHROME_DEBUG_PORT:-9222}"
USER_DATA_DIR="${CHROME_USER_DATA_DIR:-$HOME/.chrome-zhihu-automation}"

mkdir -p "$USER_DATA_DIR"

CHROME=""
for candidate in google-chrome-stable google-chrome chromium-browser chromium; do
  command -v "$candidate" >/dev/null 2>&1 && CHROME="$candidate" && break
done

if [[ -z "$CHROME" ]]; then
  echo "Chrome not found." >&2
  exit 1
fi

if curl -sf "http://127.0.0.1:${DEBUG_PORT}/json/version" >/dev/null 2>&1; then
  echo "Chrome debug port ${DEBUG_PORT} already listening."
  $(_check_hint)
  exit 0
fi

EXTRA_ARGS=()
[[ "$(id -u)" -eq 0 ]] && EXTRA_ARGS+=(--no-sandbox --disable-setuid-sandbox)
EXTRA_ARGS+=(--disable-dev-shm-usage)
# Reduce native permission bars (geolocation) stealing clicks during automation
EXTRA_ARGS+=(--disable-notifications)

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
  nohup "${CHROME_CMD[@]}" >/tmp/chrome-zhihu-automation.log 2>&1 &
  sleep 2
  if curl -sf "http://127.0.0.1:${DEBUG_PORT}/json/version" >/dev/null; then
    echo "OK: port ${DEBUG_PORT} up."
    if ! curl -sf "http://127.0.0.1:${DEBUG_PORT}/json/list" | grep -q '"type": "page"'; then
      curl -sf -X PUT "http://127.0.0.1:${DEBUG_PORT}/json/new?about:blank" >/dev/null || true
    fi
  fi
  exit 0
fi

echo "Log in to Zhihu AND Xiaohongshu in this window (same profile), then:"
$(_check_hint)
exec "${CHROME_CMD[@]}"
