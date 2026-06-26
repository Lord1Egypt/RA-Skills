#!/usr/bin/env bash
# run_pytest.sh — Run pytest on a target path.
# Usage: ./run_pytest.sh [path] [extra pytest args...]
# Defaults to current directory if no path is given.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTEST="${SKILL_DIR}/venv/bin/pytest"

TARGET="${1:-.}"
shift 2>/dev/null || true

echo "==> pytest: ${TARGET}"
"${PYTEST}" "${TARGET}" -v "$@"
