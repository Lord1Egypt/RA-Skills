#!/usr/bin/env bash
set -euo pipefail
# ─────────────────────────────────────────────
# websearch-call.sh — 通过 mcporter 调用 open-websearch MCP Server 的 search 工具
#
# 前置：用户需在 mcporter 中注册 open-websearch server（见安装指南 Step 4）。
# 降级策略：按 engines 顺序依次尝试，某一引擎失败则换下一个。
#
# 依赖：mcporter（已注册 open-websearch server）
# 用法：bash websearch-call.sh search '{"query":"关键词","limit":10}'
# ─────────────────────────────────────────────

if [ -n "${2+set}" ]; then
  TOOL_ARGS="$2"
else
  TOOL_ARGS="${1:-{}}"
fi

QUERY=$(node -e "const p=JSON.parse(process.argv[1]);console.log((p.query||'').trim())" "$TOOL_ARGS" 2>/dev/null || echo "")
if [ -z "$QUERY" ]; then
  echo '参数必须包含非空字符串 query' >&2
  exit 1
fi

LIMIT=$(node -e "const p=JSON.parse(process.argv[1]);console.log(typeof p.limit==='number'?p.limit:10)" "$TOOL_ARGS" 2>/dev/null || echo "10")
ENGINES=$(node -e "const p=JSON.parse(process.argv[1]);const e=Array.isArray(p.engines)&&p.engines.length>0?p.engines:['duckduckgo','bing','baidu'];console.log(e.join(' '))" "$TOOL_ARGS" 2>/dev/null || echo "duckduckgo bing baidu")
RECENCY=$(node -e "const p=JSON.parse(process.argv[1]);console.log(p.recency!==false&&p.recency!=='none'?'day':'')" "$TOOL_ARGS" 2>/dev/null || echo "day")

SEARCH_QUERY="$QUERY"
if [ "$RECENCY" = "day" ]; then
  SEARCH_QUERY="$QUERY 最新"
fi

TMPFILE="${TMPDIR:-/tmp}/websearch-result-$$.json"
cleanup() { rm -f "$TMPFILE"; }
trap cleanup EXIT

for ENGINE in $ENGINES; do
  MCPORTER_ARGS="{\"query\":\"$SEARCH_QUERY\",\"limit\":$LIMIT,\"engines\":[\"$ENGINE\"]}"

  if mcporter call open-websearch.search --args "$MCPORTER_ARGS" --output json > "$TMPFILE" 2>/dev/null; then
    if [ -s "$TMPFILE" ]; then
      cat "$TMPFILE"
      exit 0
    fi
  fi

  echo "引擎 $ENGINE 失败，尝试下一个..." >&2
  sleep 0.5
done

echo "所有引擎均失败" >&2
exit 1
