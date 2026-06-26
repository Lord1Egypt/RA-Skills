#!/usr/bin/env bash
# Deterministic tests (unit + integration, no network). Use in PR CI.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ -x "${ROOT}/.venv/bin/python" ]]; then
  PY="${ROOT}/.venv/bin/python"
else
  PY="${PYTHON:-python3}"
fi
"${PY}" setup/tools/check_structure.py
exec "${PY}" -m pytest tests/unit tests/integration -v "$@"
