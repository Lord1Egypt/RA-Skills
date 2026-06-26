#!/usr/bin/env bash
# OpenClaw entrypoint: Zhihu publish via attached Chrome (skill zhihu-publish-attach).
# By default, starts Chrome (debug mode) if port 9222 is down — unless --no-ensure-chrome.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=load_chromedriver_env.sh
source "$SCRIPT_DIR/load_chromedriver_env.sh"
load_chromedriver_env "$SCRIPT_DIR"

PY_SCRIPT="${ZHIHU_ATTACH_SCRIPT:-$SCRIPT_DIR/zhihu_attach_standalone.py}"

if [[ ! -f "$PY_SCRIPT" ]]; then
  echo "Missing $PY_SCRIPT" >&2
  exit 1
fi

AUTO_ENSURE=1
ARGS=()
for arg in "$@"; do
  case "$arg" in
    --no-ensure-chrome)
      AUTO_ENSURE=0
      ;;
    --ensure-chrome)
      # kept for compatibility; ensure is already default
      ;;
    *)
      ARGS+=("$arg")
      ;;
  esac
done

if [[ "$AUTO_ENSURE" -eq 1 ]]; then
  bash "$SCRIPT_DIR/ensure_chrome_debug.sh"
fi

exec python3 "$PY_SCRIPT" "${ARGS[@]}"
