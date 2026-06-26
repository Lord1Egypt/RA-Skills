#!/usr/bin/env bash
# run_eslint.sh — Run ESLint on a target path.
# Usage: ./run_eslint.sh [path] [extra eslint args...]
# Defaults to current directory if no path is given.

set -euo pipefail

TARGET="${1:-.}"
shift 2>/dev/null || true

echo "==> ESLint: ${TARGET}"
eslint "${TARGET}" "$@"
