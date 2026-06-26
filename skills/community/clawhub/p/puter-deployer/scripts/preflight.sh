#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-.}"
BUILD_DIR="${2:-dist}"

cd "$PROJECT_DIR"

echo "[1/5] checking puter CLI"
command -v puter >/dev/null || { echo "FAIL: puter CLI not found"; exit 2; }

echo "[2/5] checking puter auth"
if ! puter whoami >/dev/null 2>&1; then
  echo "FAIL: puter not authenticated. Run: puter login"
  exit 3
fi

echo "[3/5] checking build dir"
[ -d "$BUILD_DIR" ] || { echo "FAIL: build dir missing: $BUILD_DIR"; exit 4; }

echo "[4/5] checking build dir non-empty"
find "$BUILD_DIR" -mindepth 1 -print -quit | grep -q . || { echo "FAIL: build dir empty: $BUILD_DIR"; exit 5; }

echo "[5/5] checking index.html"
[ -f "$BUILD_DIR/index.html" ] || { echo "FAIL: missing $BUILD_DIR/index.html"; exit 6; }

echo "OK: preflight passed"
