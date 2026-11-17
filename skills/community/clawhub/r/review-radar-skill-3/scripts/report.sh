#!/usr/bin/env bash
# 取回报告（默认 Markdown，加 json 参数输出结构化 JSON）
set -euo pipefail
BASE="${RR_BASE_URL:-http://127.0.0.1:8787}"
FMT="${2:-md}"
curl -sf "$BASE/reports/${1:?用法: report.sh <job_id> [md|json]}?format=$FMT"
