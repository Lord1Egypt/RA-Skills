#!/usr/bin/env bash
# 提交单个视频 URL，同步等待并输出 Markdown 情报卡
set -euo pipefail
BASE="${RR_BASE_URL:-http://127.0.0.1:8787}"
URL="${1:?用法: submit.sh <视频URL>}"
JOB=$(curl -sf -X POST "$BASE/jobs" -H 'Content-Type: application/json' \
  -d "{\"url\": \"$URL\", \"run_async\": false}")
JOB_ID=$(echo "$JOB" | python3 -c "import sys,json;print(json.load(sys.stdin)['job_id'])")
curl -sf "$BASE/reports/$JOB_ID?format=md"
