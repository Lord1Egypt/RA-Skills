#!/usr/bin/env bash
# 查询任务状态
set -euo pipefail
BASE="${RR_BASE_URL:-http://127.0.0.1:8787}"
curl -sf "$BASE/jobs/${1:?用法: status.sh <job_id>}" | python3 -m json.tool
