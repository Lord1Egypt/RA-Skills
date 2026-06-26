#!/bin/bash
# 创建知了话题（两步式：预览 + 确认）
# 用法:
#   预览:   ./create-topic "话题描述" [SCOPE]
#   自动创建: ./create-topic "话题描述" [SCOPE] --auto-create
#   确认:   ./create-topic --confirm --session-id SESSION_ID --action ACTION [--topic-id TOPIC_ID]

set -e

# ============================================================
# 解析参数
# ============================================================
CONFIRM_MODE=false
AUTO_CREATE=false
PROMPT=""
SCOPE=""
SESSION_ID=""
ACTION=""
TOPIC_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --confirm)
      CONFIRM_MODE=true
      shift
      ;;
    --session-id)
      SESSION_ID="$2"
      shift 2
      ;;
    --action)
      ACTION="$2"
      shift 2
      ;;
    --topic-id)
      TOPIC_ID="$2"
      shift 2
      ;;
    --auto-create)
      AUTO_CREATE=true
      shift
      ;;
    *)
      if [ -z "$PROMPT" ]; then
        PROMPT="$1"
      elif [ -z "$SCOPE" ]; then
        SCOPE="$1"
      fi
      shift
      ;;
  esac
done

# ============================================================
# 加载配置
# ============================================================
ZHILIAO_API_KEY="${ZHILIAO_API_KEY:-$(cat ~/.zhiliao/config.json 2>/dev/null | jq -r '.apiKey // empty')}"
BASE_URL="${ZHILIAO_BASE_URL:-$(cat ~/.zhiliao/config.json 2>/dev/null | jq -r '.baseUrl // "http://api-public.zhiliao.news"')}"
BASE_URL="${BASE_URL:-http://api-public.zhiliao.news}"

if [ -z "$ZHILIAO_API_KEY" ]; then
  echo "错误: 未配置 API Key"
  echo "请设置环境变量: export ZHILIAO_API_KEY=\"your-key\""
  echo "或创建配置文件: ~/.zhiliao/config.json"
  exit 1
fi

# ============================================================
# 确认模式：调用 /confirm 接口
# ============================================================
if [ "$CONFIRM_MODE" = true ]; then
  if [ -z "$SESSION_ID" ]; then
    echo "错误: --confirm 模式需要 --session-id 参数"
    exit 1
  fi
  if [ -z "$ACTION" ]; then
    echo "错误: --confirm 模式需要 --action 参数 (create 或 subscribe)"
    exit 1
  fi
  if [ "$ACTION" = "subscribe" ] && [ -z "$TOPIC_ID" ]; then
    echo "错误: subscribe 操作需要 --topic-id 参数"
    exit 1
  fi

  # 构建请求体
  if [ "$ACTION" = "subscribe" ]; then
    BODY="{\"session_id\": \"$SESSION_ID\", \"action\": \"$ACTION\", \"topic_id\": \"$TOPIC_ID\"}"
  else
    BODY="{\"session_id\": \"$SESSION_ID\", \"action\": \"$ACTION\"}"
  fi

  TEMP_RESULT=$(mktemp)
  curl -s -X POST "$BASE_URL/api/topic/v1/out/topic/confirm" \
    -H "Content-Type: application/json" \
    -H "Authorization: $ZHILIAO_API_KEY" \
    -d "$BODY" \
    | iconv -c -t UTF-8 > "$TEMP_RESULT"

  # 展示结果
  cat "$TEMP_RESULT" | jq -r '
    if .code == 0 then
      "✅ 操作成功",
      "",
      "名称: \(.data.name)",
      "ID: \(.data.topic_id)",
      "描述: \(.data.description)",
      (if .data.surface_url then "封面: \(.data.surface_url)" else empty end)
    elif (.msg | test("余额不足")) then
      "❌ \(.msg)",
      "",
      "请前往充值页面充值: http://open.zhiliao.news/topic/api_key"
    else
      "❌ 操作失败: \(.msg)"
    end
  '

  # 保存话题（如果成功）
  CODE=$(cat "$TEMP_RESULT" | jq -r '.code')
  if [ "$CODE" = "0" ]; then
    mkdir -p ~/.zhiliao
    TOPICS_FILE=~/.zhiliao/topics.json
    [ ! -f "$TOPICS_FILE" ] && echo "[]" > "$TOPICS_FILE"

    NEW_TOPIC=$(cat "$TEMP_RESULT" | jq '.data + {"created_at": (now | strftime("%Y-%m-%dT%H:%M:%SZ"))}')
    cat "$TOPICS_FILE" | jq --argjson t "$NEW_TOPIC" \
      '[.[] | select(.topic_id == $t.topic_id | not)] + [$t]' \
      > /tmp/zhiliao_topics.json && mv /tmp/zhiliao_topics.json "$TOPICS_FILE"

    echo ""
    echo "已保存（共 $(cat "$TOPICS_FILE" | jq 'length') 个话题）"
  fi

  rm -f "$TEMP_RESULT"
  exit 0
fi

# ============================================================
# 预览模式：调用 /generate 接口
# ============================================================
if [ -z "$PROMPT" ]; then
  echo "错误: 请提供话题描述"
  echo "用法:"
  echo "  预览:   $0 \"话题描述\" [SCOPE]"
  echo "  自动创建: $0 \"话题描述\" [SCOPE] --auto-create"
  echo "  确认:   $0 --confirm --session-id SESSION_ID --action ACTION [--topic-id TOPIC_ID]"
  exit 1
fi

SCOPE="${SCOPE:-$(cat /dev/urandom | LC_ALL=C tr -dc 'a-z0-9' | head -c 6)}"

# 获取或创建 session_id
mkdir -p ~/.zhiliao/sessions
SESSION_FILE=~/.zhiliao/sessions/${SCOPE}.json
if [ -f "$SESSION_FILE" ]; then
  SESSION_ID=$(cat "$SESSION_FILE" | jq -r '.sessionId')
else
  SESSION_ID=$(uuidgen 2>/dev/null || openssl rand -hex 16)
  echo "{\"sessionId\":\"$SESSION_ID\"}" > "$SESSION_FILE"
fi

# 调用 /generate API（仅返回预览）
TEMP_RESULT=$(mktemp)
curl -s -X POST "$BASE_URL/api/topic/v1/out/topic/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: $ZHILIAO_API_KEY" \
  -H "X-Session-Id: $SESSION_ID" \
  -d "{\"prompt\": \"$PROMPT\"}" \
  | iconv -c -t UTF-8 > "$TEMP_RESULT"

CODE=$(cat "$TEMP_RESULT" | jq -r '.code')

if [ "$CODE" != "0" ]; then
  cat "$TEMP_RESULT" | jq -r '"❌ 预览失败: \(.msg)"'
  rm -f "$TEMP_RESULT"
  exit 1
fi

# 提取 session_id（从响应中获取，覆盖本地生成的）
RESP_SESSION_ID=$(cat "$TEMP_RESULT" | jq -r '.data.session_id // empty')
if [ -n "$RESP_SESSION_ID" ]; then
  SESSION_ID="$RESP_SESSION_ID"
fi

if [ "$AUTO_CREATE" = true ]; then
  # --auto-create 模式：展示预览后自动调用 /confirm
  cat "$TEMP_RESULT" | jq -r '
    "📋 话题预览:",
    "",
    "名称: \(.data.created_topic.name)",
    "描述: \(.data.created_topic.description)",
    (if .data.created_topic.surface_url then "封面: \(.data.created_topic.surface_url)" else empty end),
    "",
    "🔄 正在自动创建..."
  '

  # 调用 /confirm 创建
  CONFIRM_RESULT=$(mktemp)
  curl -s -X POST "$BASE_URL/api/topic/v1/out/topic/confirm" \
    -H "Content-Type: application/json" \
    -H "Authorization: $ZHILIAO_API_KEY" \
    -d "{\"session_id\": \"$SESSION_ID\", \"action\": \"create\"}" \
    | iconv -c -t UTF-8 > "$CONFIRM_RESULT"

  cat "$CONFIRM_RESULT" | jq -r '
    if .code == 0 then
      "✅ 话题创建成功",
      "",
      "名称: \(.data.name)",
      "ID: \(.data.topic_id)",
      "描述: \(.data.description)",
      (if .data.surface_url then "封面: \(.data.surface_url)" else empty end)
    elif (.msg | test("余额不足")) then
      "❌ \(.msg)",
      "",
      "请前往充值页面充值: http://open.zhiliao.news/topic/api_key"
    else
      "❌ 创建失败: \(.msg)"
    end
  '

  # 保存话题
  CONFIRM_CODE=$(cat "$CONFIRM_RESULT" | jq -r '.code')
  if [ "$CONFIRM_CODE" = "0" ]; then
    mkdir -p ~/.zhiliao
    TOPICS_FILE=~/.zhiliao/topics.json
    [ ! -f "$TOPICS_FILE" ] && echo "[]" > "$TOPICS_FILE"

    NEW_TOPIC=$(cat "$CONFIRM_RESULT" | jq '.data + {"created_at": (now | strftime("%Y-%m-%dT%H:%M:%SZ"))}')
    cat "$TOPICS_FILE" | jq --argjson t "$NEW_TOPIC" \
      '[.[] | select(.topic_id == $t.topic_id | not)] + [$t]' \
      > /tmp/zhiliao_topics.json && mv /tmp/zhiliao_topics.json "$TOPICS_FILE"

    rm -f "$SESSION_FILE"
    echo ""
    echo "已保存（共 $(cat "$TOPICS_FILE" | jq 'length') 个话题）"
  fi

  rm -f "$CONFIRM_RESULT"
else
  # 默认预览模式：输出 JSON 供 agent 解析
  cat "$TEMP_RESULT" | jq '{
    preview: true,
    session_id: .data.session_id,
    created_topic: .data.created_topic,
    related_topics: .data.related_topics
  }'

  echo ""
  echo "---"
  echo "提示: 使用以下命令确认操作:"
  echo "  创建新话题: $0 --confirm --session-id \"$SESSION_ID\" --action create"
  echo "  关注已有话题: $0 --confirm --session-id \"$SESSION_ID\" --action subscribe --topic-id TOPIC_ID"
fi

rm -f "$TEMP_RESULT"
