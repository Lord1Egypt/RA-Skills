#!/bin/bash
# 图片压缩脚本
# 用法: image_compress.sh <input_image> [--output <output>] [--quality <1-100>] [--max-size <mb>]

set -e

# 默认参数
INPUT=""
OUTPUT=""
QUALITY=85
MAX_SIZE_MB=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --output|-o)
            OUTPUT="$2"
            shift 2
            ;;
        --quality|-q)
            QUALITY="$2"
            shift 2
            ;;
        --max-size|-s)
            MAX_SIZE_MB="$2"
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
    echo "❌ 错误: 请指定输入图片文件"
    echo "用法: $0 <input_image> [--output <output>] [--quality <1-100>]"
    exit 1
fi

if [[ ! -f "$INPUT" ]]; then
    echo "❌ 错误: 文件不存在: $INPUT"
    exit 1
fi

# 设置输出文件
if [[ -z "$OUTPUT" ]]; then
    BASENAME=$(basename "$INPUT" | sed 's/\.[^.]*$//')
    OUTPUT="/tmp/xiaodi-media/${BASENAME}_compressed.jpg"
fi

# 创建输出目录
mkdir -p "$(dirname "$OUTPUT")"

# 获取原始大小
ORIGINAL_SIZE=$(identify -format "%b" "$INPUT" 2>/dev/null || echo "unknown")
ORIGINAL_SIZE_KB=$(du -k "$INPUT" | cut -f1)

echo "🖼️ 图片压缩开始"
echo "   输入: $INPUT"
echo "   输出: $OUTPUT"
echo "   质量: ${QUALITY}%"
echo "   原始大小: ${ORIGINAL_SIZE}"

# 如果指定了最大大小，动态调整质量
CURRENT_QUALITY=$QUALITY
if [[ -n "$MAX_SIZE_MB" ]]; then
    MAX_SIZE_KB=$((MAX_SIZE_MB * 1024))
    
    # 先尝试指定质量
    convert "$INPUT" -quality $CURRENT_QUALITY "$OUTPUT" 2>/dev/null
    
    # 如果还是太大，逐步降低质量
    while [[ $(du -k "$OUTPUT" | cut -f1) -gt $MAX_SIZE_KB && $CURRENT_QUALITY -gt 10 ]]; do
        CURRENT_QUALITY=$((CURRENT_QUALITY - 10))
        convert "$INPUT" -quality $CURRENT_QUALITY "$OUTPUT" 2>/dev/null
    done
else
    convert "$INPUT" -quality $QUALITY "$OUTPUT" 2>/dev/null
fi

# 获取压缩后大小
COMPRESSED_SIZE_KB=$(du -k "$OUTPUT" | cut -f1)
COMPRESSION_RATIO=$(awk "BEGIN {printf \"%.1f\", $COMPRESSED_SIZE_KB * 100 / $ORIGINAL_SIZE_KB}")

echo ""
echo "✅ 压缩完成!"
echo "   压缩后大小: ${COMPRESSED_SIZE_KB}KB"
echo "   压缩比例: ${COMPRESSION_RATIO}%"
echo "   输出文件: $OUTPUT"