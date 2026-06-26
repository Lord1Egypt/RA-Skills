#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$SKILL_DIR"
python scripts/wechat_article_assistant.py sync-all --interval-seconds 180 --json "$@"
