#!/usr/bin/env bash
# OpenClaw entrypoint: Xiaohongshu publish via attached Chrome (skill xiaohongshu-publish-attach).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=load_chromedriver_env.sh
source "$SCRIPT_DIR/load_chromedriver_env.sh"
load_chromedriver_env "$SCRIPT_DIR"

PY_SCRIPT="${XHS_ATTACH_SCRIPT:-$SCRIPT_DIR/xhs_attach_standalone.py}"

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
