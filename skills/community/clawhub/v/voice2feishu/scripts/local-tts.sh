#!/bin/bash
# 本地 ChatTTS 模式
# 使用本地 ChatTTS 服务生成语音并发送到飞书

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 默认配置
CHATTTS_URL="${CHATTTS_URL:-http://localhost:8080}"
DEFAULT_SEED="${CHATTTS_DEFAULT_SEED:-500}"
SEED="$DEFAULT_SEED"
RECEIVE_ID_TYPE="open_id"

# 解析参数
TEXT=""
RECEIVER=""

while [ $# -gt 0 ]; do
  case "$1" in
    --seed)
      SEED="$2"
      shift 2
      ;;
    --chat)
      RECEIVE_ID_TYPE="chat_id"
      shift
      ;;
    -h|--help)
      cat << EOF
用法: voice2feishu local <文字> <接收者> [选项]

选项:
  --seed <数字>    指定音色种子（默认: $DEFAULT_SEED）
  --chat           接收者是群聊

示例:
  voice2feishu local "你好" ou_xxx
  voice2feishu local "大家好" oc_xxx --chat --seed 100
  voice2feishu local "测试" ou_xxx --seed 500

提示:
  - 不同 seed 产生不同音色
  - 建议测试几个 seed，找到喜欢的音色
  - 设置默认 seed: export CHATTTS_DEFAULT_SEED=500
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

echo "🎙️  本地 ChatTTS 模式"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 文字: $TEXT"
echo "🎲 种子: $SEED"
echo "👤 接收者: $RECEIVER"
echo ""

# 1. 检查 ChatTTS 服务
echo "🔍 检查 ChatTTS 服务..."
if ! curl -s --connect-timeout 3 "$CHATTTS_URL/health" > /dev/null 2>&1; then
  echo "❌ ChatTTS 服务未启动"
  echo ""
  echo "请先启动服务:"
  echo "  voice2feishu start-chattts"
  echo ""
  echo "或检查 CHATTTS_URL 环境变量（当前: $CHATTTS_URL）"
  exit 1
fi
echo "✅ ChatTTS 服务正常"

# 2. 调用 ChatTTS 生成语音
echo ""
echo "🔊 生成语音..."
OUTPUT_FILE="/tmp/voice2feishu-local-$(date +%s).wav"

HTTP_CODE=$(curl -s -w "%{http_code}" -o "$OUTPUT_FILE" \
  -X POST "$CHATTTS_URL/tts" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"$TEXT\",
    \"seed\": $SEED
  }")

if [ "$HTTP_CODE" != "200" ]; then
  echo "❌ ChatTTS 调用失败 (HTTP $HTTP_CODE)"
  if [ -f "$OUTPUT_FILE" ]; then
    cat "$OUTPUT_FILE" 2>/dev/null || true
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

# 3. 上传到飞书
echo ""
bash "$SCRIPT_DIR/upload-feishu.sh" "$OUTPUT_FILE" "$RECEIVER" "$RECEIVE_ID_TYPE"

# 4. 清理
rm -f "$OUTPUT_FILE"
