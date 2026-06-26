#!/usr/bin/env bash
# Tech Trending Monitor - Get tech signal clusters & market data
# Usage: ./trending.sh
#        ./trending.sh --category signalClusters
set -euo pipefail
API_BASE="https://1341839497-kvq7g9wk8p.ap-guangzhou.tencentscf.com"
CATEGORY="${1:-}"
[[ "$CATEGORY" == "--category" ]] && CATEGORY="${2:-}"
if [[ -z "$CATEGORY" ]]; then
  echo "📊 技术趋势信号监控"
  echo "━━━━━━━━━━━━━━━━━━━━━━"
  RESPONSE=$(curl -s "${API_BASE}/trending" --connect-timeout 10 --max-time 15)
  echo "$RESPONSE" | jq -r '.data.signalClusters | to_entries[] |
    "🔍 \(.key): \(.value.status) | \(.value.platforms)平台 | \(.value.marketSize)\n   机会: \(.value.opportunity)\n   关键词: \(.value.keywords | join(", "))\n"'
  echo "━━━━━━━━━━━━━━━━━━━━━━"
  echo "$RESPONSE" | jq -r '.data.methodology | "📋 方法论: \(.name)\n   规则: " + (.rules | join(" → ")) + "\n   启动标准: \(.startupCriteria)"'
else
  curl -s "${API_BASE}/trending?category=$CATEGORY" | jq -r '.data | to_entries[0] | .value | if type == "array" then map("• \(.name): \(.focus)") | join("\n") elif type == "object" then keys[] else . end'
fi
