#!/usr/bin/env bash
# 算量回归比对入口（不需要图形界面，纯 JSON 对账）
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${CAD_PYTHON:-}"
if [ -z "$PY" ]; then
  if command -v python3 >/dev/null 2>&1; then
    PY=python3
  else
    for cand in "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3; do
      if [ -x "$cand" ]; then PY="$cand"; break; fi
    done
  fi
fi
[ -n "$PY" ] || { echo "找不到 python3，可设 CAD_PYTHON" >&2; exit 3; }
exec "$PY" "$SCRIPT_DIR/cad_quantity_regression.py" "$@"
