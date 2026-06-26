#!/bin/bash
# 音频提取脚本
# 用法: audio_extract.sh <input_video> [--output <output>] [--format <mp3|wav|aac>]

set -e

# 默认参数
INPUT=""
OUTPUT=""
FORMAT="mp3"
BITRATE="192k"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --output|-o)
            OUTPUT="$2"
            shift 2
            ;;
        --format|-f)
            FORMAT="$2"
            shift 2
            ;;
        --bitrate|-b)
            BITRATE="$2"
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
    echo "用法: $0 <input_video> [--output <output>] [--format <mp3|wav|aac>]"
    exit 1
fi

if [[ ! -f "$INPUT" ]]; then
    echo "❌ 错误: 文件不存在: $INPUT"
    exit 1
fi

# 设置输出文件
if [[ -z "$OUTPUT" ]]; then
    BASENAME=$(basename "$INPUT" | sed 's/\.[^.]*$//')
    OUTPUT="/tmp/xiaodi-media/${BASENAME}.${FORMAT}"
fi

# 创建输出目录
mkdir -p "$(dirname "$OUTPUT")"

# 获取视频时长
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT" 2>/dev/null || echo "未知")

echo "🎵 音频提取开始"
echo "   输入: $INPUT"
echo "   输出: $OUTPUT"
echo "   格式: $FORMAT"
echo "   比特率: $BITRATE"
echo "   时长: ${DURATION}秒"

# 根据格式选择编码器
case $FORMAT in
    mp3)
        CODEC="libmp3lame"
        ;;
    wav)
        CODEC="pcm_s16le"
        BITRATE=""
        ;;
    aac)
        CODEC="aac"
        ;;
    *)
        echo "❌ 不支持的格式: $FORMAT"
        exit 1
        ;;
esac

# 提取音频
if [[ -n "$BITRATE" ]]; then
    ffmpeg -y -i "$INPUT" -vn -c:a $CODEC -b:a $BITRATE "$OUTPUT" 2>&1 | tail -5
else
    ffmpeg -y -i "$INPUT" -vn -c:a $CODEC "$OUTPUT" 2>&1 | tail -5
fi

# 获取输出大小
OUTPUT_SIZE=$(du -h "$OUTPUT" | cut -f1)

echo ""
echo "✅ 音频提取完成!"
echo "   文件大小: $OUTPUT_SIZE"
echo "   输出文件: $OUTPUT"