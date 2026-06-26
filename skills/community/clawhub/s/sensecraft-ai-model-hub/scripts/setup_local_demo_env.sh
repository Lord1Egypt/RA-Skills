#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="${ROOT}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3.12}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "error: $PYTHON_BIN not found. Set PYTHON_BIN=/path/to/python3.12 and retry." >&2
  exit 1
fi

mkdir -p "$ROOT/models" "$ROOT/captures"

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install numpy opencv-python pillow ai-edge-litert

echo "OK: local demo environment ready"
echo "activate with: source $VENV_DIR/bin/activate"
