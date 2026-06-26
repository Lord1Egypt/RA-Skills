#!/bin/bash
# vsum - 视频字幕获取脚本

set -e

# 用法
usage() {
    echo "用法: vsum.sh <视频链接> [语言]"
    echo ""
    echo "示例:"
    echo "  vsum.sh \"https://www.youtube.com/watch?v=xxx\""
    echo "  vsum.sh \"https://www.bilibili.com/video/BVxxx\""
    exit 1
}

# 检查参数
if [ $# -lt 1 ]; then
    usage
fi

URL="$1"
LANG="${2:-en}"
OUTPUT_DIR="${HOME}/Downloads"

# 检测平台
detect_platform() {
    if echo "$URL" | grep -q "bilibili.com"; then
        echo "bilibili"
    elif echo "$URL" | grep -q "youtube.com\|youtu.be"; then
        echo "youtube"
    else
        echo "unknown"
    fi
}

PLATFORM=$(detect_platform)

if [ "$PLATFORM" = "unknown" ]; then
    echo "错误: 无法识别的视频平台"
    exit 1
fi

echo "检测到平台: $PLATFORM"

cd "$OUTPUT_DIR"

# 获取字幕
if [ "$PLATFORM" = "youtube" ]; then
    echo "获取 YouTube 字幕..."
    yt-dlp --write-auto-subs --sub-lang "$LANG" --skip-download "$URL"
elif [ "$PLATFORM" = "bilibili" ]; then
    echo "获取 Bilibili 字幕（需要登录）..."
    yt-dlp --cookies-from-browser chrome --write-subs --sub-lang ai-zh,zh-CN,"$LANG" --skip-download "$URL"
fi

echo "字幕已保存到: $OUTPUT_DIR"
echo ""
echo "下一步: 将字幕内容发送给 AI 进行总结"
