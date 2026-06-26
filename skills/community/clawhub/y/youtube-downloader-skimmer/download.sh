#!/bin/bash
# YouTube 视频下载和剪辑工具 - 调用脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/youtube_downloader.py"

echo "🎬 YouTube Video Downloader & Skimmer v1.0.0"
echo "=========================="
echo ""
echo "用法："
echo "  $0 \"YouTube URL\" [选项]"
echo ""
echo "示例："
echo "  $0 \"https://www.youtube.com/watch?v=xxx\""
echo "  $0 \"https://www.youtube.com/watch?v=xxx\" --output-format mp3"
echo "  $0 \"https://www.youtube.com/watch?v=xxx\" --quality 720p"
echo ""

python3 "${PYTHON_SCRIPT}" "$@"
