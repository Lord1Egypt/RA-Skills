#!/usr/bin/env bash
# run_ruff.sh — Run Ruff Python linter on a target path.
# Usage: ./run_ruff.sh [path] [extra ruff args...]
# Defaults to current directory if no path is given.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUFF="${SKILL_DIR}/venv/bin/ruff"

TARGET="${1:-.}"
shift 2>/dev/null || true

echo "==> Ruff lint: ${TARGET}"
"${RUFF}" check "${TARGET}" "$@"
