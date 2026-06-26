#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== Cleaning build artifacts ==="
find . -type d -name '__pycache__' -prune -exec rm -rf {} + 2>/dev/null || true
find . -type f -name '*.pyc' -delete 2>/dev/null || true
rm -rf reports/test-generated 2>/dev/null || true

echo "=== Running regression pack ==="
./tests/regression/run-all.sh

echo "=== Verifying strict release gate ==="
./validate-release.sh --strict

echo "=== Ready for super-memori packaging (current active line) ==="
