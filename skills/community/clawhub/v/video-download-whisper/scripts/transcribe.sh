#!/bin/bash
# 音频转录脚本
# 用法: ./transcribe.sh <音频文件路径> [模型] [输出目录]

set -e

# 动态查找Whisper路径
if [ -x "/Users/yanghaohan/Library/Python/3.9/bin/whisper" ]; then
    WHISPER_BIN="/Users/yanghaohan/Library/Python/3.9/bin/whisper"
elif command -v whisper &>/dev/null; then
    WHISPER_BIN="whisper"
else
    echo "错误: 找不到 Whisper"
    echo "提示: pip3 install -U openai-whisper"
    exit 1
fi

# 参数解析
AUDIO_FILE="$1"
MODEL="${2:-medium}"
OUTPUT_DIR="${3:-/tmp}"

if [ ! -f "$AUDIO_FILE" ]; then
    echo "错误: 音频文件不存在: $AUDIO_FILE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "=== 转录开始 ==="
echo "音频: $AUDIO_FILE"
echo "模型: $MODEL"
echo "输出: $OUTPUT_DIR"

# 执行转录
$WHISPER_BIN "$AUDIO_FILE" \
    --model "$MODEL" \
    --output_format txt \
    --output_dir "$OUTPUT_DIR"

# 获取输出文件名
BASENAME=$(basename "$AUDIO_FILE" | cut -d. -f1)
TRANSCRIPT="$OUTPUT_DIR/${BASENAME}.txt"

if [ -f "$TRANSCRIPT" ]; then
    echo "=== 转录完成 ==="
    echo "文件: $TRANSCRIPT"
    echo ""
    echo "=== 预览（前1000字） ==="
    head -c 1000 "$TRANSCRIPT"
    echo ""
else
    echo "错误: 转录失败"
    exit 1
fi
