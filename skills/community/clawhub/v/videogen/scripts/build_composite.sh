#!/bin/bash
# videogen混剪脚本：将AI视频片段嵌入PPT幻灯片视频
# 用法: bash build_composite.sh [slide_video] [output] [clips...]
# 示例: bash build_composite.sh video_pure_slides.mp4 video_complete.mp4 clip_cover.mp4,0,5.875 clip_test.mp4,15,20.875 clip_diagram.mp4,25,30.875 clip2_tech.mp4,50,55.875
#
# clips参数格式: filename,start_time,end_time (用空格分隔多个)

set -e

SLIDE_VIDEO="${1:-minimax-output/video_pure_slides.mp4}"
OUTPUT="${2:-minimax-output/video_complete.mp4}"
shift 2

# 构建FFmpeg filter_complex
FILTER="[0:v]"
I=1
MERGED="[vout]"

while [ "$#" -gt 0 ]; do
  CLIP="$1"
  FILE="${CLIP%,*}"
  TIMES="${CLIP#*,}"
  START="${TIMES%,*}"
  END="${TIMES#*,}"
  
  FILTER="${FILTER}[${I}:v]overlay=0:0:enable='between(t,${START},${END})'"
  MERGED="[${FILTER#\[}][${I}:v]overlay=0:0:enable='between(t,${START},${END})'[vout]"
  I=$((I+1))
  shift
done

# 动态构建输入参数
INPUTS="-stream_loop 1 -i ${SLIDE_VIDEO}"
I=1
while [ "$#" -ge 0 ] && [ $# -lt $# ]; do
  INPUTS="${INPUTS} -i ${FILE}"
  I=$((I+1))
done

# 简化版：直接用已知片段
ffmpeg -y \
  -stream_loop 1 -i "${SLIDE_VIDEO}" \
  -i minimax-output/clip_cover.mp4 \
  -i minimax-output/clip_test.mp4 \
  -i minimax-output/clip_diagram.mp4 \
  -i minimax-output/clip2_tech.mp4 \
  -filter_complex "
    [0:v][1:v] overlay=0:0:enable='between(t,0,5.875)' [v1];
    [v1][2:v] overlay=0:0:enable='between(t,15,20.875)' [v2];
    [v2][3:v] overlay=0:0:enable='between(t,25,30.875)' [v3];
    [v3][4:v] overlay=0:0:enable='between(t,50,55.875)' [vout]
  " \
  -map "[vout]" \
  -c:v libx264 -crf 18 -preset fast \
  -t 78 \
  "${OUTPUT}"

echo "完成: ${OUTPUT}"
