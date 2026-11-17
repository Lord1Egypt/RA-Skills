#!/usr/bin/env bash
# Launcher for screener-docs: runs the script in an isolated Python env,
# never the system Python's site-packages.
#
# Resolution order:
#   1. SCREENER_DOCS_PYTHON  - explicit interpreter (e.g. an existing venv's bin/python)
#   2. uv                    - `uv run --script` with inline deps (cached, isolated)
#   3. managed venv          - auto-created at $SCREENER_DOCS_VENV
#                              (default: ~/.openclaw/tools/screener-docs/venv)
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$SKILL_DIR/scripts/screener_docs.py"
REQS="$SKILL_DIR/requirements.txt"
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
VENV="${SCREENER_DOCS_VENV:-$STATE_DIR/tools/screener-docs/venv}"

# 1. Explicit interpreter
if [[ -n "${SCREENER_DOCS_PYTHON:-}" ]]; then
  if ! "$SCREENER_DOCS_PYTHON" -c "import requests, bs4" 2>/dev/null; then
    echo "[screener-docs] installing deps into $SCREENER_DOCS_PYTHON env" >&2
    "$SCREENER_DOCS_PYTHON" -m pip install --quiet -r "$REQS"
  fi
  exec "$SCREENER_DOCS_PYTHON" "$SCRIPT" "$@"
fi

# 2. uv (unless disabled with SCREENER_DOCS_USE_UV=0)
if [[ "${SCREENER_DOCS_USE_UV:-1}" != "0" ]] && command -v uv >/dev/null 2>&1; then
  exec uv run --quiet --script "$SCRIPT" "$@"
fi

# 3. Managed venv
if [[ ! -x "$VENV/bin/python" ]]; then
  PY="$(command -v python3 || true)"
  [[ -z "$PY" ]] && { echo "[screener-docs] python3 not found; install python3 or uv" >&2; exit 2; }
  echo "[screener-docs] creating venv at $VENV (one-time)" >&2
  mkdir -p "$(dirname "$VENV")"
  "$PY" -m venv "$VENV"
  "$VENV/bin/python" -m pip install --quiet --upgrade pip
  "$VENV/bin/python" -m pip install --quiet -r "$REQS"
elif ! "$VENV/bin/python" -c "import requests, bs4" 2>/dev/null; then
  "$VENV/bin/python" -m pip install --quiet -r "$REQS"
fi
exec "$VENV/bin/python" "$SCRIPT" "$@"
