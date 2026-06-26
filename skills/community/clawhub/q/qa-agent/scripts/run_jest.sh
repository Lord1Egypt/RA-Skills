#!/usr/bin/env bash
# run_jest.sh — Run Jest on a target path or test pattern.
# Usage: ./run_jest.sh [path/pattern] [extra jest args...]
# Defaults to all tests if no path is given.

set -euo pipefail

TARGET="${1:-}"
shift 2>/dev/null || true

echo "==> Jest: ${TARGET:-all tests}"
if [[ -n "${TARGET}" ]]; then
  jest --testPathPattern="${TARGET}" "$@"
else
  jest "$@"
fi
