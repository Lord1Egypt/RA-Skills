#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -n "${RUFF_BIN:-}" ]; then
  RUFF_CMD=("${RUFF_BIN}")
elif command -v ruff >/dev/null 2>&1; then
  RUFF_CMD=("ruff")
elif python3 -m ruff --version >/dev/null 2>&1; then
  RUFF_CMD=("python3" "-m" "ruff")
elif command -v uv >/dev/null 2>&1; then
  RUFF_CMD=("uvx" "--from" "ruff" "ruff")
else
  echo "ruff is not installed and uv is unavailable" >&2
  exit 127
fi

python3 -m compileall -q "${SCRIPT_DIR}"
"${RUFF_CMD[@]}" check "${SCRIPT_DIR}"
python3 "${SCRIPT_DIR}/check_research_mode_docs.py"
python3 "${SCRIPT_DIR}/release_smoke.py" >/dev/null

if command -v pyright >/dev/null 2>&1; then
  pyright --project "${SKILL_DIR}/pyrightconfig.json"
elif command -v uv >/dev/null 2>&1; then
  uvx --from pyright pyright --project "${SKILL_DIR}/pyrightconfig.json"
else
  echo "pyright is not installed and uv is unavailable; skipping typecheck" >&2
fi

python3 "${SCRIPT_DIR}/selftest_research_mode.py"

if python3 -m pytest --version >/dev/null 2>&1; then
  python3 -m pytest -q "${SCRIPT_DIR}/selftest"
elif command -v uv >/dev/null 2>&1; then
  uvx --from pytest pytest -q "${SCRIPT_DIR}/selftest"
else
  echo "pytest is not installed and uv is unavailable; skipping pytest compatibility check" >&2
fi
