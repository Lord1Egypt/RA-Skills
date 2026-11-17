#!/usr/bin/env bash
# 批量提交视频 URL（异步），输出 job_id 列表供后续轮询
set -euo pipefail
BASE="${RR_BASE_URL:-http://127.0.0.1:8787}"
[ $# -ge 1 ] || { echo "用法: batch.sh <URL1> [URL2 ...]" >&2; exit 1; }
URLS=$(printf '%s\n' "$@" | python3 -c "import sys,json;print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))")
curl -sf -X POST "$BASE/jobs/batch" -H 'Content-Type: application/json' -d "{\"urls\": $URLS}"
