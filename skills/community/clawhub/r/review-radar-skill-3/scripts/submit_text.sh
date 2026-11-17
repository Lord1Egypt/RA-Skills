#!/usr/bin/env bash
# 手动文本兜底：submit_text.sh <文本文件> [标题]
set -euo pipefail
BASE="${RR_BASE_URL:-http://127.0.0.1:8787}"
FILE="${1:?用法: submit_text.sh <文本文件路径> [标题]}"
TITLE="${2:-手动文本任务}"
PAYLOAD=$(python3 -c "
import json,sys
text = open('$FILE', encoding='utf-8').read()
print(json.dumps({'manual_text': text, 'title': '$TITLE', 'run_async': False}))
")
JOB=$(curl -sf -X POST "$BASE/jobs" -H 'Content-Type: application/json' -d "$PAYLOAD")
JOB_ID=$(echo "$JOB" | python3 -c "import sys,json;print(json.load(sys.stdin)['job_id'])")
curl -sf "$BASE/reports/$JOB_ID?format=md"
