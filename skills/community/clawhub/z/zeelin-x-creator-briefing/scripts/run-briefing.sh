#!/bin/bash
# ZeeLin X Creator Briefing - 兼容版执行脚本（不依赖 openclaw task）

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$SCRIPT_DIR/run_briefing.py" --days 10 --publish
