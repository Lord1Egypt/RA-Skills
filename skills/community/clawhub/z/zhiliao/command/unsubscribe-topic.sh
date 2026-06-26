#!/bin/bash
# 取消订阅知了话题
# 用法: ./unsubscribe-topic TOPIC_ID

set -e

TOPIC_ID="$1"

if [ -z "$TOPIC_ID" ]; then
  echo "错误: 请提供话题 ID"
  echo "用法: $0 TOPIC_ID"
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
curl -s -X POST "$BASE_URL/api/topic/v1/out/topic/unsubscribe" \
  -H "Content-Type: application/json" \
  -H "Authorization: $ZHILIAO_API_KEY" \
  -d "{\"topic_id\": \"$TOPIC_ID\"}" \
  | iconv -c -t UTF-8 > "$TEMP_RESULT"

# 展示结果
cat "$TEMP_RESULT" | jq -r '
  if .code == 0 then
    "✅ \(.msg)"
  else
    "❌ 取消订阅失败: \(.msg)"
  end
'

# 从本地话题列表中移除
CODE=$(cat "$TEMP_RESULT" | jq -r '.code')
if [ "$CODE" = "0" ]; then
  TOPICS_FILE=~/.zhiliao/topics.json
  if [ -f "$TOPICS_FILE" ]; then
    cat "$TOPICS_FILE" | jq --arg id "$TOPIC_ID" \
      '[.[] | select(.topic_id == $id | not)]' \
      > /tmp/zhiliao_topics.json && mv /tmp/zhiliao_topics.json "$TOPICS_FILE"
    echo "已从本地移除（剩余 $(cat "$TOPICS_FILE" | jq 'length') 个话题）"
  fi
  # 清理文章缓存
  rm -f ~/.zhiliao/articles/${TOPIC_ID}.json
fi

rm -f "$TEMP_RESULT"
