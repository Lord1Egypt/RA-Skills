#!/bin/bash
# 视频压缩脚本
# 用法: video_compress.sh <input_video> [--output <output>] [--size <target_mb>] [--crf <crf>]

set -e

# 默认参数
INPUT=""
OUTPUT=""
TARGET_SIZE_MB=""
CRF=23
PRESET="medium"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --output|-o)
            OUTPUT="$2"
            shift 2
            ;;
        --size|-s)
            TARGET_SIZE_MB="$2"
            shift 2
            ;;
        --crf|-c)
            CRF="$2"
            shift 2
            ;;
        --preset|-p)
            PRESET="$2"
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
    echo "用法: $0 <input_video> [--output <output>] [--size <target_mb>]"
    exit 1
fi

if [[ ! -f "$INPUT" ]]; then
    echo "❌ 错误: 文件不存在: $INPUT"
    exit 1
fi

# 设置输出文件
if [[ -z "$OUTPUT" ]]; then
    BASENAME=$(basename "$INPUT" | sed 's/\.[^.]*$//')
    OUTPUT="/tmp/xiaodi-media/${BASENAME}_compressed.mp4"
fi

# 创建输出目录
mkdir -p "$(dirname "$OUTPUT")"

# 获取视频信息
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT")
DURATION_INT=${DURATION%.*}
if [[ -z "$DURATION_INT" || "$DURATION_INT" -eq 0 ]]; then
    DURATION_INT=60
fi

# 如果指定了目标大小，计算 CRF
if [[ -n "$TARGET_SIZE_MB" ]]; then
    TARGET_KBPS=$((TARGET_SIZE_MB * 8192 / DURATION_INT))
    if [[ $TARGET_KBPS -lt 1000 ]]; then
        CRF=32
    elif [[ $TARGET_KBPS -lt 2000 ]]; then
        CRF=28
    elif [[ $TARGET_KBPS -lt 4000 ]]; then
        CRF=25
    else
        CRF=23
    fi
    echo "🎯 目标大小: ${TARGET_SIZE_MB}MB, 计算CRF: $CRF"
fi

# 获取原始文件大小
ORIGINAL_SIZE=$(du -m "$INPUT" | cut -f1)

echo "🎬 视频压缩开始"
echo "   输入: $INPUT"
echo "   输出: $OUTPUT"
echo "   时长: ${DURATION_INT}秒"
echo "   原始大小: ${ORIGINAL_SIZE}MB"
echo "   CRF: $CRF, Preset: $PRESET"

# 执行压缩
ffmpeg -y -i "$INPUT" \
    -c:v libx264 -crf $CRF -preset $PRESET \
    -c:a aac -b:a 128k \
    -movflags +faststart \
    "$OUTPUT" 2>&1 | tail -5

# 获取压缩后大小
COMPRESSED_SIZE=$(du -m "$OUTPUT" | cut -f1)
COMPRESSION_RATIO=$(awk "BEGIN {printf \"%.1f\", $COMPRESSED_SIZE * 100 / $ORIGINAL_SIZE}")

echo ""
echo "✅ 压缩完成!"
echo "   压缩后大小: ${COMPRESSED_SIZE}MB"
echo "   压缩比例: ${COMPRESSION_RATIO}%"
echo "   输出文件: $OUTPUT"