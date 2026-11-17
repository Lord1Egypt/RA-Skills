#!/usr/bin/env bash
# 报告库检索：list_reports.sh [产品型号关键词]
set -euo pipefail
BASE="${RR_BASE_URL:-http://127.0.0.1:8787}"
if [ $# -ge 1 ]; then
  curl -sf "$BASE/reports?model=$1" | python3 -m json.tool
else
  curl -sf "$BASE/reports" | python3 -m json.tool
fi
