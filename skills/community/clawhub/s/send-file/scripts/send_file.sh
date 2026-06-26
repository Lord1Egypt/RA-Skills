#!/bin/bash
# send_file.sh - 文件发送辅助脚本
# 用法: ./send_file.sh <file_path> [platform] [target]

set -e

FILE_PATH="$1"
PLATFORM="${2:-feishu}"
TARGET="$3"

if [[ -z "$FILE_PATH" ]]; then
    echo "用法: $0 <file_path> [platform] [target]"
    echo ""
    echo "参数:"
    echo "  file_path - 要发送的文件路径"
    echo "  platform  - 目标平台 (feishu/telegram/discord/signal)，默认 feishu"
    echo "  target    - 目标用户或群组ID，留空则发送到当前对话"
    echo ""
    echo "示例:"
    echo "  $0 /path/to/file.pdf"
    echo "  $0 /path/to/file.pdf feishu user:ou_xxx"
    exit 1
fi

if [[ ! -f "$FILE_PATH" ]]; then
    echo "❌ 错误: 文件不存在: $FILE_PATH"
    exit 1
fi

FILENAME=$(basename "$FILE_PATH")
FILESIZE=$(stat -f%z "$FILE_PATH" 2>/dev/null || stat -c%s "$FILE_PATH" 2>/dev/null)

# 格式化文件大小
format_size() {
    local size=$1
    if [[ $size -ge 1048576 ]]; then
        echo "$(echo "scale=1; $size / 1048576" | bc)MB"
    elif [[ $size -ge 1024 ]]; then
        echo "$(echo "scale=1; $size / 1024" | bc)KB"
    else
        echo "${size}B"
    fi
}

SIZE_STR=$(format_size $FILESIZE)

echo "📤 准备发送文件:"
echo "   路径: $FILE_PATH"
echo "   文件名: $FILENAME"
echo "   大小: $SIZE_STR"
echo "   平台: $PLATFORM"
echo "   目标: ${TARGET:-当前对话}"
echo ""

# 检查文件大小限制
case "$PLATFORM" in
    feishu)
        MAX_SIZE=31457280  # 30MB
        if [[ $FILESIZE -gt $MAX_SIZE ]]; then
            echo "⚠️  警告: 文件超过飞书限制 (30MB)，可能发送失败"
        fi
        ;;
    telegram)
        MAX_SIZE=52428800  # 50MB
        if [[ $FILESIZE -gt $MAX_SIZE ]]; then
            echo "⚠️  警告: 文件超过 Telegram 限制 (50MB)，可能发送失败"
        fi
        ;;
    discord)
        MAX_SIZE=26214400  # 25MB (普通用户)
        if [[ $FILESIZE -gt $MAX_SIZE ]]; then
            echo "⚠️  警告: 文件超过 Discord 限制 (25MB)，可能发送失败"
        fi
        ;;
esac

echo "✅ 文件检查通过，可以发送"