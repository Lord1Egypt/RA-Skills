#!/bin/bash
# 检查所有话题的文章更新
# 用法: ./check-articles

set -e

TOPICS_FILE=~/.zhiliao/topics.json

if [ ! -f "$TOPICS_FILE" ]; then
  echo "暂无话题，请先创建一个话题。"
  exit 0
fi

# 加载配置
ZHILIAO_API_KEY="${ZHILIAO_API_KEY:-$(cat ~/.zhiliao/config.json 2>/dev/null | jq -r '.apiKey // empty')}"
BASE_URL="${ZHILIAO_BASE_URL:-$(cat ~/.zhiliao/config.json 2>/dev/null | jq -r '.baseUrl // "http://api-public.zhiliao.news"')}"
BASE_URL="${BASE_URL:-http://api-public.zhiliao.news}"

if [ -z "$ZHILIAO_API_KEY" ]; then
  echo "错误: 未配置 API Key"
  exit 1
fi

echo "# 知了 - 话题资讯更新"
echo ""
echo "> 检查时间: $(date '+%Y-%m-%d %H:%M:%S') | 共 $(cat "$TOPICS_FILE" | jq 'length') 个话题"
echo ""

cat "$TOPICS_FILE" | jq -r '.[].topic_id' | while read -r TOPIC_ID; do
  TOPIC_NAME=$(cat "$TOPICS_FILE" | jq -r --arg id "$TOPIC_ID" '.[] | select(.topic_id == $id) | .name')

  # 调用 API 获取文章
  TEMP_RESULT=$(mktemp)
  curl -s -X POST "$BASE_URL/api/topic/v1/out/topic/article" \
    -H "Content-Type: application/json" \
    -H "Authorization: $ZHILIAO_API_KEY" \
    -d "{\"topic_id\": \"$TOPIC_ID\", \"limit\": 10, \"cursor\": \"\"}" \
    | iconv -c -t UTF-8 > "$TEMP_RESULT"

  # 展示结果
  echo "## $TOPIC_NAME"
  echo ""
  cat "$TEMP_RESULT" | jq -r '"> 话题 ID: `\(.data.feed_list[0].topic_id)` | 共 \(.data.article_num) 篇 | 最近1小时新增 \(.data.no_article_last_hour_count) 篇\n"'

  ARTICLE_COUNT=$(cat "$TEMP_RESULT" | jq '.data.feed_list | length')
  if [ "$ARTICLE_COUNT" = "0" ]; then
    echo "*暂无文章*"
  else
    cat "$TEMP_RESULT" | jq -r '
      .data.feed_list[] |
      "- [\(.title)](https://h5.zhiliao.news/article/\(.entry_id))",
      "  > \(.description // "暂无摘要" | .[0:120])",
      "  > \(.pub_time | strftime("%Y-%m-%d %H:%M"))\n"
    '
  fi

  # 缓存到本地
  mkdir -p ~/.zhiliao/articles
  cat "$TEMP_RESULT" | jq '{updated_at: (now | strftime("%Y-%m-%dT%H:%M:%SZ")), articles: .data.feed_list}' \
    > ~/.zhiliao/articles/${TOPIC_ID}.json

  rm -f "$TEMP_RESULT"
  echo "---"
  echo ""
done
