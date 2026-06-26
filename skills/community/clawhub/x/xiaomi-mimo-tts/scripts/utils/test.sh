#!/bin/bash
# MiMo TTS 测试脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== MiMo TTS 测试 ==="
echo ""

# 检查环境变量
if [ -z "${XIAOMI_API_KEY}" ] && [ -z "${MIMO_API_KEY}" ]; then
    echo "❌ MIMO_API_KEY 未设置"
    echo "   请运行: export MIMO_API_KEY=your-api-key"
    exit 1
fi
echo "✓ MIMO_API_KEY 已设置"

# 检查依赖
echo ""
echo "检查依赖..."
for cmd in curl python3 ffmpeg; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ $cmd 未安装"
        exit 1
    fi
    echo "✓ $cmd 已安装"
done

# 测试 API 连接
echo ""
echo "测试 API 连接..."
TEST_RESPONSE=$(curl -s -w "\n%{http_code}" "https://api.xiaomimimo.com/v1/models" \
    -H "Authorization: Bearer $MIMO_API_KEY")

HTTP_CODE=$(echo "$TEST_RESPONSE" | tail -n 1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ API 连接成功"
else
    echo "❌ API 连接失败 (HTTP $HTTP_CODE)"
    exit 1
fi

# 测试 TTS 生成
echo ""
echo "测试 TTS 生成..."
TEST_TEXT="测试语音合成"
OUTPUT_FILE="/tmp/mimo-tts-test-$(date +%s).ogg"

RESULT=$("$SCRIPT_DIR/../mimo-tts.sh" "$TEST_TEXT" "$OUTPUT_FILE" 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ] && [ -f "$OUTPUT_FILE" ]; then
    FILE_SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null || stat -c%s "$OUTPUT_FILE" 2>/dev/null)
    echo "✓ TTS 生成成功"
    echo "  文件: $OUTPUT_FILE"
    echo "  大小: $FILE_SIZE bytes"
    rm -f "$OUTPUT_FILE"
    echo ""
    echo "=== 所有测试通过 ==="
    exit 0
else
    echo "❌ TTS 生成失败"
    echo "$RESULT"
    exit 1
fi
