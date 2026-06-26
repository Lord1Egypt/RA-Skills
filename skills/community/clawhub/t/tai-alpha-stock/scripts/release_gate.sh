#!/usr/bin/env bash
# Release gate: offline tests must pass; then live tests (optional skip on failure with artifact).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ -x "${ROOT}/.venv/bin/python" ]]; then
  PY="${ROOT}/.venv/bin/python"
else
  PY="${PYTHON:-python3}"
fi
echo "== Phase 0: repo structure (Markdown/SQL under /setup) =="
"${PY}" setup/tools/check_structure.py
echo "== Phase 1: offline (unit + integration) =="
"${PY}" -m pytest tests/unit tests/integration -v --tb=short
echo "== Phase 2: live data (yfinance) =="
"${PY}" -m pytest tests/live --live -v --tb=short || {
  echo "Live tests failed — inspect logs; blocking release." >&2
  exit 1
}
echo "Release gate OK."
