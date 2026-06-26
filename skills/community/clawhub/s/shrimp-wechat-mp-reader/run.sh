#!/usr/bin/env bash
set -euo pipefail

URL="${1:-}"
if [[ -z "$URL" ]]; then
  echo "usage: $0 <mp.weixin.qq.com url>" >&2
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SKILL_DIR"

if [[ ! -d node_modules/playwright ]]; then
  npm install >/dev/null 2>&1
fi

PLAYWRIGHT_BROWSERS_PATH="$HOME/.cache/ms-playwright"
export PLAYWRIGHT_BROWSERS_PATH

if [[ ! -x "$PLAYWRIGHT_BROWSERS_PATH/chromium-1217/chrome-linux64/chrome" ]]; then
  npx playwright install chromium >/dev/null 2>&1
fi

node scripts/extract.js "$URL"
