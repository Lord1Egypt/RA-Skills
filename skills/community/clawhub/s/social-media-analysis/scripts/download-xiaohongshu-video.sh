#!/bin/bash
#
# 小红书视频下载脚本
# 功能：使用 yt-dlp 下载小红书视频并抽帧
#
# 用法：
#   ./download-xiaohongshu-video.sh <URL> <输出目录> [--cookie <COOKIE_STRING>]
#
# 示例：
#   ./download-xiaohongshu-video.sh "https://www.xiaohongshu.com/explore/69b8f9360000000021039d96" ./output
#   ./download-xiaohongshu-video.sh "URL" ./output --cookie "unread=xxx; id_token=xxx"
#

set -e

URL="$1"
OUTPUT_DIR="$2"
COOKIE=""

# 解析参数
shift 2
while [[ $# -gt 0 ]]; do
  case $1 in
    --cookie)
      COOKIE="$2"
      shift 2
      ;;
    *)
      echo "未知参数：$1"
      exit 1
      ;;
  esac
done

if [ -z "$URL" ] || [ -z "$OUTPUT_DIR" ]; then
  echo "用法：./download-xiaohongshu-video.sh <URL> <输出目录> [--cookie <COOKIE_STRING>]"
  echo "示例：./download-xiaohongshu-video.sh \"https://www.xiaohongshu.com/explore/xxx\" ./output"
  exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "开始下载小红书视频：$URL"
echo "输出目录：$OUTPUT_DIR"
echo "---"

# 准备 Cookie 文件
COOKIE_FILE="/tmp/xhs_cookies_$$"
COOKIE_ARG=""

if [ -n "$COOKIE" ]; then
  # 将 Cookie 字符串转换为 Netscape 格式
  echo "# Netscape HTTP Cookie File" > "$COOKIE_FILE"
  
  echo "$COOKIE" | tr ';' '\n' | while read -r cookie; do
    cookie=$(echo "$cookie" | xargs)  # 去除首尾空格
    if [ -n "$cookie" ]; then
      key=$(echo "$cookie" | cut -d'=' -f1)
      value=$(echo "$cookie" | cut -d'=' -f2-)
      if [ -n "$key" ] && [ -n "$value" ]; then
        echo -e ".xiaohongshu.com\tTRUE\t/\tTRUE\t0\t${key}\t${value}" >> "$COOKIE_FILE"
      fi
    fi
  done
  
  COOKIE_ARG="--cookies $COOKIE_FILE"
  echo "✅ Cookie 文件已创建：$COOKIE_FILE"
fi

# 检查 yt-dlp 是否安装
if ! command -v yt-dlp &> /dev/null; then
  echo "❌ yt-dlp 未安装，请先安装：brew install yt-dlp"
  exit 1
fi

# 下载视频
echo ""
echo "正在下载视频..."
VIDEO_PATH="$OUTPUT_DIR/video.mp4"

if [ -n "$COOKIE_ARG" ]; then
  yt-dlp $COOKIE_ARG -f best -o "$VIDEO_PATH" "$URL"
else
  yt-dlp -f best -o "$VIDEO_PATH" "$URL"
fi

# 检查下载结果
if [ -f "$VIDEO_PATH" ]; then
  SIZE=$(ls -lh "$VIDEO_PATH" | awk '{print $5}')
  echo ""
  echo "---"
  echo "✅ 视频已下载：video.mp4 ($SIZE)"
  echo "输出目录：$OUTPUT_DIR"
  
  # 询问是否抽帧
  echo ""
  read -p "是否需要视频抽帧？（每 5 秒一帧，输入 y 确认）: " -n 1 -r
  echo
  
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "正在抽帧..."
    cd "$OUTPUT_DIR"
    ffmpeg -i video.mp4 -vf "fps=1/5" -q:v 2 frame_%03d.jpg 2>&1 | tail -5
    
    FRAME_COUNT=$(ls -1 frame_*.jpg 2>/dev/null | wc -l | xargs)
    echo ""
    echo "✅ 抽帧完成！共 ${FRAME_COUNT} 帧"
    echo "输出文件：frame_001.jpg, frame_002.jpg..."
  fi
  
else
  echo "❌ 视频下载失败，文件不存在"
  exit 1
fi

# 清理临时 Cookie 文件
if [ -n "$COOKIE_ARG" ] && [ -f "$COOKIE_FILE" ]; then
  rm -f "$COOKIE_FILE"
fi
