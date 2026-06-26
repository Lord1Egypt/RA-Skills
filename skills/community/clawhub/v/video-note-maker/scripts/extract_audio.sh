#!/bin/bash
# 提取视频音频脚本
# 用法：./extract_audio.sh <视频文件> <输出音频文件>

VIDEO_FILE=$1
OUTPUT_FILE=$2

if [ -z "$VIDEO_FILE" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "用法：./extract_audio.sh <视频文件> <输出音频文件>"
    exit 1
fi

ffmpeg -i "$VIDEO_FILE" \
    -vn \
    -acodec pcm_s16le \
    -ar 44100 \
    -ac 2 \
    "$OUTPUT_FILE"

echo "✅ 音频已提取：$OUTPUT_FILE"
