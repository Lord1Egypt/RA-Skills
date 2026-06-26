#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python runtime not found: $PYTHON_BIN" >&2
  exit 1
fi

if [ ! -f "$SCRIPT_DIR/dist/index.html" ]; then
  echo "Missing built frontend. Run: npm run build" >&2
  exit 1
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/overlay_host.py" "$@"
