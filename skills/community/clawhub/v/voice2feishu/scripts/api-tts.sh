#!/bin/bash
# API TTS 模式
# 使用第三方 API 生成语音并发送到飞书

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 默认配置
TTS_API_URL="${TTS_API_URL:-https://open.bigmodel.cn/api/paas/v4/audio/speech}"
TTS_API_KEY="${TTS_API_KEY:-}"
DEFAULT_VOICE="${TTS_DEFAULT_VOICE:-alloy}"
VOICE="$DEFAULT_VOICE"
RECEIVE_ID_TYPE="open_id"

# 解析参数
TEXT=""
RECEIVER=""

while [ $# -gt 0 ]; do
  case "$1" in
    --voice)
      VOICE="$2"
      shift 2
      ;;
    --chat)
      RECEIVE_ID_TYPE="chat_id"
      shift
      ;;
    -h|--help)
      cat << EOF
用法: voice2feishu api <文字> <接收者> [选项]

选项:
  --voice <名称>   指定音色（默认: $DEFAULT_VOICE）
  --chat           接收者是群聊

支持的音色（取决于 API）:
  alloy, echo, fable, onyx, nova, shimmer

示例:
  voice2feishu api "你好" ou_xxx
  voice2feishu api "大家好" oc_xxx --chat --voice nova
EOF
      exit 0
      ;;
    *)
      if [ -z "$TEXT" ]; then
        TEXT="$1"
      elif [ -z "$RECEIVER" ]; then
        RECEIVER="$1"
      fi
      shift
      ;;
  esac
done

# 参数检查
if [ -z "$TEXT" ]; then
  echo "❌ 错误：缺少文字内容"
  exit 1
fi

if [ -z "$RECEIVER" ]; then
  echo "❌ 错误：缺少接收者 ID"
  exit 1
fi

if [ -z "$TTS_API_KEY" ]; then
  echo "❌ 错误：未设置 TTS_API_KEY 环境变量"
  echo ""
  echo "请设置:"
  echo "  export TTS_API_KEY='your_api_key'"
  exit 1
fi

echo "🎙️  API TTS 模式"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 文字: $TEXT"
echo "🎤 音色: $VOICE"
echo "👤 接收者: $RECEIVER"
echo ""

# 1. 调用 TTS API 生成语音
echo "🔊 生成语音..."
OUTPUT_FILE="/tmp/voice2feishu-api-$(date +%s).mp3"

HTTP_CODE=$(curl -s -w "%{http_code}" -o "$OUTPUT_FILE" \
  -X POST "$TTS_API_URL" \
  -H "Authorization: Bearer $TTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"tts-1\",
    \"input\": \"$TEXT\",
    \"voice\": \"$VOICE\"
  }")

if [ "$HTTP_CODE" != "200" ]; then
  echo "❌ TTS API 调用失败 (HTTP $HTTP_CODE)"
  if [ -f "$OUTPUT_FILE" ]; then
    cat "$OUTPUT_FILE"
    rm -f "$OUTPUT_FILE"
  fi
  exit 1
fi

if [ ! -s "$OUTPUT_FILE" ]; then
  echo "❌ 生成的音频文件为空"
  rm -f "$OUTPUT_FILE"
  exit 1
fi

FILE_SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
echo "✅ 语音生成成功 ($FILE_SIZE)"

# 2. 上传到飞书
echo ""
bash "$SCRIPT_DIR/upload-feishu.sh" "$OUTPUT_FILE" "$RECEIVER" "$RECEIVE_ID_TYPE"

# 3. 清理
rm -f "$OUTPUT_FILE"
