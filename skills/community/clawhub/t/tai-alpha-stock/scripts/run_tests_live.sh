#!/usr/bin/env bash
# Full suite including live yfinance tests. Nightly / pre-release.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ -x "${ROOT}/.venv/bin/python" ]]; then
  PY="${ROOT}/.venv/bin/python"
else
  PY="${PYTHON:-python3}"
fi
exec "${PY}" -m pytest tests --live -v --tb=short "$@"
