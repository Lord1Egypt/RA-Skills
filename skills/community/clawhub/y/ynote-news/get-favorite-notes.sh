#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# get-favorite-notes.sh — 获取最近收藏笔记（内容自动截断）
#
# mcporter 输出落盘，jq 从文件解析并截断，避免大体积进 bash 变量。
# 截断策略：每条笔记保留 title 全文 + content 前 N 字（默认 500）
#
# 用法：
#   bash get-favorite-notes.sh              # 默认 limit=30, 每条 500 字
#   bash get-favorite-notes.sh 15            # limit=15
#   bash get-favorite-notes.sh 30 800       # limit=30, 每条 800 字
# ─────────────────────────────────────────────

LIMIT="${1:-30}"
MAX_CHARS="${2:-500}"
TMPFILE="${TMPDIR:-/tmp}/ynote-fav-notes-$$.json"

cleanup() { rm -f "$TMPFILE"; }
trap cleanup EXIT

# 主路径：落盘后 jq 解析，避免大输出进变量
if ! mcporter call youdaonote.getRecentFavoriteNotes --args "{\"limit\":$LIMIT}" --output json > "$TMPFILE" 2>/dev/null; then
  echo '{"error":"getRecentFavoriteNotes 调用失败"}' >&2
  exit 1
fi

if [ ! -s "$TMPFILE" ]; then
  echo '{"error":"getRecentFavoriteNotes 未返回数据"}' >&2
  exit 1
fi

jq -e --argjson max "$MAX_CHARS" '
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
' < "$TMPFILE"
