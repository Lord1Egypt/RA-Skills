#!/bin/bash
# 分割音频脚本
# 用法：./split_audio.sh <音频文件> <输出目录> <分割时长（秒）>

AUDIO_FILE=$1
OUTPUT_DIR=$2
SEGMENT_DURATION=${3:-900}

if [ -z "$AUDIO_FILE" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "用法：./split_audio.sh <音频文件> <输出目录> [分割时长]"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# 获取音频时长
DURATION=$(ffprobe -i "$AUDIO_FILE" -show_entries format=duration -v quiet -of csv=p=0)

# 分割音频
SEGMENT_COUNT=0
START_TIME=0

while [ $(echo "$START_TIME < $DURATION" | bc) -eq 1 ]; do
    DURATION_MIN=$((SEGMENT_DURATION))
    REMAINING=$(echo "$DURATION - $START_TIME" | bc)
    
    if [ $(echo "$REMAINING < $SEGMENT_DURATION" | bc) -eq 1 ]; then
        DURATION_MIN=$REMAINING
    fi
    
    OUTPUT_FILE="${OUTPUT_DIR}/segment_${SEGMENT_COUNT:03d}.wav"
    
    ffmpeg -i "$AUDIO_FILE" \
        -ss "$START_TIME" \
        -t "$DURATION_MIN" \
        -vn \
        -acodec pcm_s16le \
        -ar 44100 \
        -ac 2 \
        "$OUTPUT_FILE" \
        -y
    
    SEGMENT_COUNT=$((SEGMENT_COUNT + 1))
    START_TIME=$(echo "$START_TIME + $SEGMENT_DURATION" | bc)
done

echo "✅ 音频已分割为 $SEGMENT_COUNT 段"
