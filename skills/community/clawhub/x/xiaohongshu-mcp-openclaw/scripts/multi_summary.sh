#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KEYWORD="${1:-防晒}"
SEARCH_LIMIT="${2:-5}"
COMMENT_LIMIT="${3:-2}"
SERVER_NAME="${4:-xiaohongshu-mcp}"
TIMEOUT_MS="${5:-120000}"

OUT_FILE="${XHS_SUMMARY_OUT:-/tmp/xhs-multi-summary-$(date +%s).json}"

python3 "$BASE_DIR/scripts/xhs_mcp_client.py" \
  --server "$SERVER_NAME" \
  --timeout "$TIMEOUT_MS" \
  report \
  --keyword "$KEYWORD" \
  --search-limit "$SEARCH_LIMIT" \
  --comment-limit "$COMMENT_LIMIT" > "$OUT_FILE"

jq '{
  keyword,
  note_count: (.normalized | length),
  top_by_like: (
    (.normalized | sort_by(.like_count // 0) | reverse | .[0]) |
    {note_id, title, author, like_count, comment_count, url}
  ),
  items: (
    .normalized |
    map({
      note_id,
      title,
      author,
      like_count,
      comment_count,
      url,
      top_comment: (.top_comments[0].content // null)
    })
  )
}' "$OUT_FILE"

echo "[INFO] Raw full report saved: $OUT_FILE"
