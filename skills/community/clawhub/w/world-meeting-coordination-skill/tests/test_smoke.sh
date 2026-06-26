#!/usr/bin/env bash
set -euo pipefail
python3 "$(dirname "$0")/../scripts/meeting_windows.py" \
  --date 2026-03-06 \
  --anchor America/Chicago \
  --zones "Chicago=America/Chicago,London=Europe/London,Tel Aviv=Asia/Jerusalem" \
  | rg -q "✅ \*\*Optimal\*\*"
echo "ok"
