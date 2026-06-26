#!/bin/bash
# 视频关键帧提取脚本
# 使用方法：bash extract_frames.sh <视频文件路径> [输出目录] [帧间隔秒数]

# 参数检查
if [ -z "$1" ]; then
    echo "使用方法: bash extract_frames.sh <视频文件> [输出目录] [间隔秒数]"
    echo "示例: bash extract_frames.sh video.mp4 ./frames 6"
    exit 1
fi

VIDEO_FILE="$1"
OUTPUT_DIR="${2:-./frames}"
INTERVAL="${3:-6}"

# 检查视频文件
if [ ! -f "$VIDEO_FILE" ]; then
    echo "错误：视频文件不存在: $VIDEO_FILE"
    exit 1
fi

# 检查 ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "错误：未安装 ffmpeg，请先安装"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 获取视频时长
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_FILE")
echo "视频时长: ${DURATION}秒"

# 计算预期帧数
EXPECTED_FRAMES=$(echo "scale=0; $DURATION / $INTERVAL" | bc)
echo "预计提取帧数: ${EXPECTED_FRAMES}张"

# 提取关键帧
echo "正在提取关键帧..."
ffmpeg -i "$VIDEO_FILE" -vf "fps=1/$INTERVAL" -q:v 2 "$OUTPUT_DIR/frame_%02d.jpg" -y 2>&1 | tail -3

# 统计结果
FRAME_COUNT=$(ls -1 "$OUTPUT_DIR"/frame_*.jpg 2>/dev/null | wc -l)
echo "完成！共提取 ${FRAME_COUNT} 张截图到 ${OUTPUT_DIR}"

# 列出文件
echo ""
echo "截图文件列表："
ls -lh "$OUTPUT_DIR"/frame_*.jpg 2>/dev/null | awk '{print $NF, $5}'
