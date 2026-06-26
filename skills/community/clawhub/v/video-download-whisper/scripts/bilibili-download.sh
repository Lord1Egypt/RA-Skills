#!/bin/bash
# B站视频下载脚本
# 用法: ./bilibili-download.sh <短链接或BV号> [输出目录]

set -e

# 配置
OUTPUT_DIR="${2:-/tmp}"
mkdir -p "$OUTPUT_DIR"

# 解析输入
INPUT="$1"
if [[ "$INPUT" =~ ^BV[a-zA-Z0-9]+$ ]]; then
    # 直接是BV号
    BV="$INPUT"
else
    # 短链接，解析为BV号
    BV=$(curl -sI "$INPUT" 2>/dev/null | grep -i location | grep -oE 'BV[a-zA-Z0-9]+' | head -1)
fi

if [ -z "$BV" ]; then
    echo "错误: 无法解析BV号"
    exit 1
fi

echo "=== 下载视频: $BV ==="

# 下载视频
VIDEO_PATH="$OUTPUT_DIR/video_${BV}.mp4"
yt-dlp -o "$VIDEO_PATH" "https://www.bilibili.com/video/$BV"

# 提取音频
AUDIO_PATH="$OUTPUT_DIR/audio_${BV}.wav"
echo "=== 提取音频 ==="
ffmpeg -i "$VIDEO_PATH" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$AUDIO_PATH" -y

echo "=== 完成 ==="
echo "视频: $VIDEO_PATH"
echo "音频: $AUDIO_PATH"
