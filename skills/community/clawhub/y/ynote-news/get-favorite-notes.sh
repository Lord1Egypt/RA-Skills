#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# get-favorite-notes.sh — 获取最近收藏笔记（内容自动截断）
#
# 调用 mcp-call.sh getRecentFavoriteNotes 后，用 jq 截断每条笔记的 content，
# 确保总输出量可控，避免撑爆 Agent 的 context window。
#
# 截断策略：每条笔记保留 title 全文 + content 前 N 字（默认 500）
#
# 依赖：curl, jq（同 mcp-call.sh）
# 用法：
#   bash get-favorite-notes.sh              # 默认 limit=30, 每条 500 字
#   bash get-favorite-notes.sh 15           # limit=15
#   bash get-favorite-notes.sh 30 800       # limit=30, 每条 800 字
# ─────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

LIMIT="${1:-30}"
MAX_CHARS="${2:-500}"

# mcp-call.sh 后台 SSE 进程被 kill 时可能返回非零退出码（如 143），属正常行为
RAW=$(bash "$SCRIPT_DIR/mcp-call.sh" getRecentFavoriteNotes "{\"limit\":$LIMIT}" 2>/dev/null) || true

if [ -z "$RAW" ]; then
  echo '{"error":"getRecentFavoriteNotes 未返回数据"}' >&2
  exit 1
fi

echo "$RAW" | jq --argjson max "$MAX_CHARS" '
  if type == "array" then
    [ .[] | {
      fileId,
      title,
      content: (
        (.content // "") as $c |
        if ($c | length) > $max
        then ($c[0:$max] + "…（已截断，原文 " + ($c | length | tostring) + " 字）")
        else $c
        end
      ),
      collectTime
    }]
  else .
  end
'
