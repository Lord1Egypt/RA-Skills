#!/bin/bash
# 已合并到 run_social_ops_v5（主题）或 run_social_publish.sh（标题+共用正文）
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"
if [ "$#" -eq 1 ]; then
  exec "$D/run_social_ops_v5.sh" "$1"
fi
if [ "$#" -eq 2 ]; then
  exec "$D/run_social_publish.sh" "$1" "$2"
fi
echo "Usage: $0 \"主题\""
echo "   or: $0 \"标题\" \"共用正文\"（旧模式）"
exit 1
