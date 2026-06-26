#!/bin/bash
# 上传音频到飞书
# 用法: upload-feishu.sh <音频文件> <接收者ID> [接收者类型]

set -e

# 配置
APP_ID="${FEISHU_APP_ID}"
APP_SECRET="${FEISHU_APP_SECRET}"

# 参数
AUDIO_FILE="$1"
RECEIVER="$2"
RECEIVE_ID_TYPE="${3:-open_id}"

# 参数检查
if [ -z "$AUDIO_FILE" ] || [ -z "$RECEIVER" ]; then
  echo "❌ 错误：缺少参数"
  echo "用法: $0 <音频文件> <接收者ID> [open_id|chat_id]"
  exit 1
fi

if [ ! -f "$AUDIO_FILE" ]; then
  echo "❌ 错误：文件不存在: $AUDIO_FILE"
  exit 1
fi

if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ]; then
  echo "❌ 错误：未设置飞书环境变量"
  echo ""
  echo "请设置:"
  echo "  export FEISHU_APP_ID='cli_xxx'"
  echo "  export FEISHU_APP_SECRET='xxx'"
  exit 1
fi

echo "📤 上传到飞书"

# 1. 获取飞书 token
TOKEN_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$APP_ID\", \"app_secret\": \"$APP_SECRET\"}")

TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.tenant_access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
  echo "❌ 获取 token 失败"
  echo "$TOKEN_RESPONSE" | jq .
  exit 1
fi

# 2. 转换为 opus 格式（如果需要）
FILE_EXT="${AUDIO_FILE##*.}"
FILE_EXT_LOWER=$(echo "$FILE_EXT" | tr '[:upper:]' '[:lower:]')

if [ "$FILE_EXT_LOWER" = "opus" ] || [ "$FILE_EXT_LOWER" = "ogg" ]; then
  OPUS_FILE="$AUDIO_FILE"
else
  OPUS_FILE="/tmp/feishu-upload-$(date +%s).opus"
  ffmpeg -y -i "$AUDIO_FILE" \
    -c:a libopus \
    -b:a 24k \
    -ar 24000 \
    -ac 1 \
    "$OPUS_FILE" > /dev/null 2>&1
  
  if [ ! -f "$OPUS_FILE" ]; then
    echo "❌ 格式转换失败"
    exit 1
  fi
fi

# 3. 读取音频时长（毫秒）
EXACT_DURATION=$(ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 "$OPUS_FILE")

if [ -z "$EXACT_DURATION" ]; then
  echo "❌ 无法读取时长"
  exit 1
fi

DURATION_MS=$(awk "BEGIN {printf \"%.0f\", $EXACT_DURATION * 1000}")
DUR_SEC=$(awk "BEGIN {printf \"%.1f\", $DURATION_MS / 1000}")

# 4. 上传文件到飞书
UPLOAD_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$OPUS_FILE" \
  -F "file_type=opus" \
  -F "file_name=voice.opus" \
  -F "duration=$DURATION_MS")

UPLOAD_CODE=$(echo "$UPLOAD_RESPONSE" | jq -r '.code')
if [ "$UPLOAD_CODE" != "0" ]; then
  echo "❌ 上传失败"
  echo "$UPLOAD_RESPONSE" | jq .
  exit 1
fi

FILE_KEY=$(echo "$UPLOAD_RESPONSE" | jq -r '.data.file_key')

# 5. 发送音频消息
SEND_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=$RECEIVE_ID_TYPE" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"$RECEIVER\",
    \"msg_type\": \"audio\",
    \"content\": \"{\\\"file_key\\\": \\\"$FILE_KEY\\\", \\\"duration\\\": $DURATION_MS}\"
  }")

SEND_CODE=$(echo "$SEND_RESPONSE" | jq -r '.code')
if [ "$SEND_CODE" != "0" ]; then
  echo "❌ 发送失败"
  echo "$SEND_RESPONSE" | jq .
  exit 1
fi

# 6. 清理临时文件
if [ "$OPUS_FILE" != "$AUDIO_FILE" ]; then
  rm -f "$OPUS_FILE"
fi

# 7. 完成
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 语音消息发送成功！"
echo ""
echo "📊 统计："
echo "   • 时长: ${DUR_SEC} 秒"
echo "   • 接收者: $RECEIVER"
echo ""
