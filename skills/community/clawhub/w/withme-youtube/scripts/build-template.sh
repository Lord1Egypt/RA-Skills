#!/bin/bash
# ============================================
# With me. — Lofi Ambient Video Build Template
# 复制此脚本到对应影片文件夹后修改参数
# ============================================
set -e

# === 可修改参数 ===
TOTAL_DURATION=7200        # 总时长（秒），2小时
SCENE_COUNT=5              # 场景数量
FADE_DURATION=3            # 场景间交叉淡入淡出（秒）
FPS=30
RES="3840x2160"            # 输出分辨率

# 音量（dB）— Ken 根据实际素材调整
VOL_MUSIC="-20dB"
VOL_AMBIENT="-16dB"
VOL_ATMOSPHERE="-22dB"

# 淡入淡出
FADE_IN=10                 # 开头淡入秒数
FADE_OUT=30                # 结尾淡出秒数

# === 路径（按实际修改） ===
IMG_DIR="images_4k"
MUSIC_FILES=("music1.wav" "music2.wav" "music3.wav")
AMBIENT="ambient.wav"      # 环境音循环
ATMOSPHERE="atmosphere.wav" # 氛围音循环
OUTPUT_NAME="output.mp4"

# === Ken Burns 效果参数 ===
# 每个场景的 zoompan 参数不同，创造视觉变化
# zoom 范围 1.0-1.15，移动方向：中心/上/左/右/对角
# 具体参数参考 jazz-cafe/build-jazz-4k.sh

# === 编码参数 ===
VIDEO_CODEC="libx264"
VIDEO_PRESET="medium"
VIDEO_CRF=18
AUDIO_CODEC="aac"
AUDIO_BITRATE="192k"

echo "============================================"
echo "With me. Video Builder"
echo "Duration: $((TOTAL_DURATION/3600))h | Scenes: $SCENE_COUNT | Res: $RES"
echo "============================================"
echo ""
echo "⚠️  这是模板脚本，请复制到影片文件夹后修改路径和参数再运行"
echo "    参考实际脚本: ~/Projects/withme-youtube/scripts/build-jazz-4k.sh"
