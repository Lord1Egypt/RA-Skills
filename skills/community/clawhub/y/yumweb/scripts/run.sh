#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

PY="$($SCRIPT_DIR/bootstrap.sh)"
exec "$PY" "$SCRIPT_DIR/yumweb.py" "$@"
