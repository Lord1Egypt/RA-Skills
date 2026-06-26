#!/usr/bin/env bash
# test-sidecar.sh — Wrapper that runs the Python test suite
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$SKILL_DIR/scripts/test-sidecar.py" "$@"
