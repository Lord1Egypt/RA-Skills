#!/bin/bash
# 查看话题列表（通过 API 获取）
# 用法: ./list-topics [TOPIC_ID]

set -e

TOPIC_ID="$1"

# 加载配置
ZHILIAO_API_KEY="${ZHILIAO_API_KEY:-$(cat ~/.zhiliao/config.json 2>/dev/null | jq -r '.apiKey // empty')}"
BASE_URL="${ZHILIAO_BASE_URL:-$(cat ~/.zhiliao/config.json 2>/dev/null | jq -r '.baseUrl // "http://api-public.zhiliao.news"')}"
BASE_URL="${BASE_URL:-http://api-public.zhiliao.news}"

if [ -z "$ZHILIAO_API_KEY" ]; then
  echo "错误: 未配置 API Key"
  echo "请设置环境变量: export ZHILIAO_API_KEY=\"your-key\""
  echo "或创建配置文件: ~/.zhiliao/config.json"
  exit 1
fi

# 调用 API
TEMP_RESULT=$(mktemp)
curl -s -X POST "$BASE_URL/api/topic/v1/user_sub_topic/get" \
  -H "Content-Type: application/json" \
  -H "Authorization: $ZHILIAO_API_KEY" \
  -d '{}' \
  | iconv -c -t UTF-8 > "$TEMP_RESULT"

CODE=$(cat "$TEMP_RESULT" | jq -r '.code')
if [ "$CODE" != "0" ]; then
  cat "$TEMP_RESULT" | jq -r '"❌ 获取话题列表失败: \(.msg)"'
  rm -f "$TEMP_RESULT"
  exit 1
fi

if [ -n "$TOPIC_ID" ]; then
  # 查看单个话题详情
  cat "$TEMP_RESULT" | jq -r --arg id "$TOPIC_ID" '
    .data.user_subscribes[] | select(.topic_id == $id) |
    "# \(.name)\n",
    "| 字段 | 值 |",
    "|------|------|",
    "| ID | `\(.topic_id)` |",
    "| 描述 | \(.description) |",
    "| 封面 | \(.surface_url // "无") |",
    "| 创建时间 | \(.create_at // 0 | todate) |"
  '
else
  # 列出所有话题
  SUB_NUM=$(cat "$TEMP_RESULT" | jq -r '.data.user_sub_topic_num')
  if [ "$SUB_NUM" = "0" ]; then
    echo "暂无话题，请先创建一个话题。"
    rm -f "$TEMP_RESULT"
    exit 0
  fi

  cat "$TEMP_RESULT" | jq -r '
    "# 我的话题（共 \(.data.user_sub_topic_num) 个）\n",
    (.data.user_subscribes[] |
      "## \(.name)\n",
      "| 字段 | 值 |",
      "|------|------|",
      "| ID | `\(.topic_id)` |",
      "| 描述 | \(.description) |",
      "| 创建时间 | \(.create_at // 0 | todate) |",
      ""
    )
  '
fi

rm -f "$TEMP_RESULT"
