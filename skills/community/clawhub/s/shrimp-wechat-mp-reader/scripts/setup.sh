#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_DIR"

if [[ ! -f package.json ]]; then
  echo "missing package.json" >&2
  exit 1
fi

npm install
npx playwright install chromium

echo "[wechat-mp-reader] setup done"