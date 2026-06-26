#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_DIR="$SKILL_DIR/.runtime"
PY_DIR="$RUNTIME_DIR/ytvenv"
NODE_DIR="$RUNTIME_DIR/gemini"

mkdir -p "$RUNTIME_DIR"

if [[ ! -x "$PY_DIR/bin/python" ]]; then
  python3 -m venv "$PY_DIR"
fi
"$PY_DIR/bin/pip" install -q --upgrade pip yt-dlp

mkdir -p "$NODE_DIR"
if [[ ! -f "$NODE_DIR/package.json" ]]; then
  (cd "$NODE_DIR" && npm init -y >/dev/null 2>&1)
fi
(cd "$NODE_DIR" && npm install --silent puppeteer-core@24)

echo "SOCIAL_VIDEO_DISTILL_RUNTIME_OK"
echo "YT_DLP=$PY_DIR/bin/yt-dlp"
echo "PUPPETEER_CORE=$NODE_DIR/node_modules/puppeteer-core"
