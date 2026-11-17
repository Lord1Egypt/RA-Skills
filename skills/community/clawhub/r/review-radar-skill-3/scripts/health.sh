#!/usr/bin/env bash
# Review Radar 服务健康检查
set -euo pipefail
BASE="${RR_BASE_URL:-http://127.0.0.1:8787}"
curl -sf --max-time 5 "$BASE/health" || {
  echo "服务不在线。请先启动: cd <review-radar目录> && python cli.py serve" >&2
  exit 1
}
