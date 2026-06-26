#!/bin/bash
# 获取话题文章
# 用法: ./fetch-articles TOPIC_ID [LIMIT] [CURSOR]

set -e

TOPIC_ID="$1"
LIMIT="${2:-20}"
CURSOR="${3:-}"

if [ -z "$TOPIC_ID" ]; then
  echo "错误: 请提供话题 ID"
  echo "用法: $0 TOPIC_ID [LIMIT] [CURSOR]"
  exit 1
fi

# 加载配置
ZHILIAO_API_KEY="${ZHILIAO_API_KEY:-$(cat ~/.zhiliao/config.json 2>/dev/null | jq -r '.apiKey // empty')}"
BASE_URL="${ZHILIAO_BASE_URL:-$(cat ~/.zhiliao/config.json 2>/dev/null | jq -r '.baseUrl // "http://api-public.zhiliao.news"')}"
BASE_URL="${BASE_URL:-http://api-public.zhiliao.news}"

if [ -z "$ZHILIAO_API_KEY" ]; then
  echo "错误: 未配置 API Key"
  exit 1
fi

# 调用 API
TEMP_RESULT=$(mktemp)
curl -s -X POST "$BASE_URL/api/topic/v1/out/topic/article" \
  -H "Content-Type: application/json" \
  -H "Authorization: $ZHILIAO_API_KEY" \
  -d "{\"topic_id\": \"$TOPIC_ID\", \"limit\": $LIMIT, \"cursor\": \"$CURSOR\"}" \
  | iconv -c -t UTF-8 > "$TEMP_RESULT"

# 展示结果
cat "$TEMP_RESULT" | jq -r '
  "共 \(.data.article_num) 篇 | 最近1小时新增 \(.data.no_article_last_hour_count) 篇 | 最近1天新增 \(.data.no_article_last_day_count) 篇\n",
  (.data.feed_list[] |
    "### [\(.title)](https://h5.zhiliao.news/article/\(.entry_id))",
    "> \(.description // "暂无摘要")",
    "> 发布时间: \(.pub_time | strftime("%Y-%m-%d %H:%M"))",
    (if .viewpoint then "\n**核心观点：**", (.viewpoint[] | "- \(.)") else empty end),
    ""
  ),
  (if .data.has_more then "---\n还有更多文章，下一页 cursor: `\(.data.cursor)`" else empty end)
'

# 缓存到本地
mkdir -p ~/.zhiliao/articles
cat "$TEMP_RESULT" | jq '{updated_at: (now | strftime("%Y-%m-%dT%H:%M:%SZ")), articles: .data.feed_list}' \
  > ~/.zhiliao/articles/${TOPIC_ID}.json

rm -f "$TEMP_RESULT"
