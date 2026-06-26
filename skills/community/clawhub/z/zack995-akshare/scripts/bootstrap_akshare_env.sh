#!/usr/bin/env bash
set -euo pipefail

VENV="${AKSHARE_VENV:-$HOME/.openclaw/.venvs/akshare}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

mkdir -p "$(dirname "$VENV")"
"$PYTHON_BIN" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip setuptools wheel
"$VENV/bin/pip" install --upgrade akshare

echo "AKShare ready: $VENV/bin/python"
