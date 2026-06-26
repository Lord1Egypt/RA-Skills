#!/bin/bash
# 视频帧提取脚本
# 用法: video_frame.sh <input_video> [--time <timestamp>] [--output <output>]

set -e

# 默认参数
INPUT=""
TIME="00:00:00"
OUTPUT=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --time|-t)
            TIME="$2"
            shift 2
            ;;
        --output|-o)
            OUTPUT="$2"
            shift 2
            ;;
        -*)
            echo "未知参数: $1"
            exit 1
            ;;
        *)
            if [[ -z "$INPUT" ]]; then
                INPUT="$1"
            fi
            shift
            ;;
    esac
done

# 检查输入
if [[ -z "$INPUT" ]]; then
    echo "❌ 错误: 请指定输入视频文件"
    echo "用法: $0 <input_video> [--time <timestamp>] [--output <output>]"
    exit 1
fi

if [[ ! -f "$INPUT" ]]; then
    echo "❌ 错误: 文件不存在: $INPUT"
    exit 1
fi

# 设置输出文件
if [[ -z "$OUTPUT" ]]; then
    BASENAME=$(basename "$INPUT" | sed 's/\.[^.]*$//')
    TIME_STR=$(echo "$TIME" | tr ':' '_')
    OUTPUT="/tmp/xiaodi-media/${BASENAME}_frame_${TIME_STR}.jpg"
fi

# 创建输出目录
mkdir -p "$(dirname "$OUTPUT")"

echo "🎬 提取视频帧"
echo "   输入: $INPUT"
echo "   时间: $TIME"
echo "   输出: $OUTPUT"

# 提取帧
ffmpeg -y -ss "$TIME" -i "$INPUT" -vframes 1 -q:v 2 "$OUTPUT" 2>&1 | tail -3

# 检查输出
if [[ -f "$OUTPUT" ]]; then
    FILE_SIZE=$(du -h "$OUTPUT" | cut -f1)
    echo ""
    echo "✅ 帧提取完成!"
    echo "   文件大小: $FILE_SIZE"
    echo "   输出文件: $OUTPUT"
else
    echo "❌ 提取失败"
    exit 1
fi