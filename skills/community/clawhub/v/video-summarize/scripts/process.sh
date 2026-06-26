#!/bin/bash
# 通用视频处理脚本：优先字幕下载，无字幕则 Whisper 转录
# 支持：B站、YouTube、抖音、Twitter、Instagram、TikTok 等多种平台
# 支持并发处理（每个视频使用独立目录，清理简单）
# YouTube 支持：需要 Chrome 浏览器已登录 YouTube

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$SKILL_DIR/.venv"
MODELS_DIR="$SKILL_DIR/whisper-models"
CACHE_DIR="$SKILL_DIR/cache"
RESULT_DIR="$SKILL_DIR/summarize_result"

# 检查环境
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ 环境未安装，请先运行: scripts/install_dependency.sh"
    exit 1
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 参数
VIDEO_URL="$1"

# 检测是否是 YouTube 链接（需要 cookies）
YTDLP_COOKIES=""
if [[ "$VIDEO_URL" =~ youtube\.com|youtu\.be ]]; then
    YTDLP_COOKIES="--cookies-from-browser chrome"
    echo "ℹ️ YouTube 链接，将使用 Chrome cookies"
fi

if [ -z "$VIDEO_URL" ]; then
    echo "用法: process.sh <视频链接>"
    echo ""
    echo "支持平台："
    echo "  B站: https://www.bilibili.com/video/BVxxx"
    echo "  YouTube: https://www.youtube.com/watch?v=xxx"
    echo "  抖音: https://www.douyin.com/video/xxx"
    echo "  Twitter/X: https://twitter.com/user/status/xxx"
    echo "  TikTok: https://www.tiktok.com/@user/video/xxx"
    echo "  Instagram: https://www.instagram.com/p/xxx"
    echo "  其他: yt-dlp 支持的任何平台"
    echo ""
    echo "注意：YouTube 视频需要 Chrome 浏览器已登录 YouTube"
    exit 1
fi

# 准备目录
mkdir -p "$CACHE_DIR"
mkdir -p "$RESULT_DIR"

# ===== 步骤 1：获取视频信息 =====
echo "[1/4] 获取视频信息..."

# 获取标题和视频 ID
VIDEO_TITLE=$(yt-dlp $YTDLP_COOKIES --get-title --no-playlist "$VIDEO_URL" 2>/dev/null || echo "未知标题")
VIDEO_ID=$(yt-dlp $YTDLP_COOKIES --get-id --no-playlist "$VIDEO_URL" 2>/dev/null || echo "unknown")

echo "标题: $VIDEO_TITLE"
echo "视频ID: $VIDEO_ID"

# 用 Python 处理标题 → 安全文件名
SAFE_TITLE=$(python3 "$SCRIPT_DIR/safe_filename.py" "$VIDEO_TITLE")
echo "文件名: $SAFE_TITLE"
echo ""

# 定义目录结构：所有中间文件放在 cache/{SAFE_TITLE}/ 下
WORK_DIR="$CACHE_DIR/$SAFE_TITLE"
mkdir -p "$WORK_DIR"

STATUS_FILE="$WORK_DIR/status.json"
SUBS_DIR="$WORK_DIR/subs"
AUDIO_FILE="$WORK_DIR/audio.m4a"
WAV_FILE="$WORK_DIR/audio.wav"
TRANSCRIPT_TXT="$WORK_DIR/transcript.txt"

# 最终输出文件
# transcript_raw.txt 放在 cache/{safe_title}/ 目录（保留，不清理）
CACHE_TRANSCRIPT="$WORK_DIR/transcript_raw.txt"
CACHE_MD="$RESULT_DIR/${SAFE_TITLE}.md"

# ===== 检查缓存 =====
if [ -f "$CACHE_TRANSCRIPT" ]; then
    echo "=== 已有缓存 ==="
    echo ""
    echo "标题: $VIDEO_TITLE"
    echo "视频ID: $VIDEO_ID"
    echo "链接: $VIDEO_URL"
    echo ""
    if [ -f "$CACHE_MD" ]; then
        echo "✅ 总结已完成: $CACHE_MD"
    else
        echo "✅ 转录已完成（等待总结）: $CACHE_TRANSCRIPT"
    fi
    echo ""
    echo "--- 转录预览 ---"
    head -c 500 "$CACHE_TRANSCRIPT"
    echo ""
    echo "---------------"
    exit 0
fi

# ===== 开始处理 =====
echo "=== 开始处理 ==="
echo ""
echo "标题: $VIDEO_TITLE"
echo "视频ID: $VIDEO_ID"
echo "链接: $VIDEO_URL"
echo ""

# 写入状态文件
cat > "$STATUS_FILE" << EOF
{
  "video_id": "$VIDEO_ID",
  "title": "$VIDEO_TITLE",
  "url": "$VIDEO_URL",
  "status": "processing",
  "start_time": "$(date -Iseconds)"
}
EOF
echo "✅ 状态已记录"

# ===== 步骤 2：尝试下载字幕 =====
echo ""
echo "[2/4] 检查字幕..."
mkdir -p "$SUBS_DIR"

# 尝试下载字幕（只下载优先级最高的：简体中文 > 英文）
yt-dlp \
    $YTDLP_COOKIES \
    --write-subs \
    --write-auto-subs \
    --sub-langs "zh-Hans,zh-CN,en" \
    --skip-download \
    --output "${SUBS_DIR}/${SAFE_TITLE}" \
    --no-playlist \
    --no-warning \
    "$VIDEO_URL" 2>&1 | grep -E "(Downloading|Writing|has no)" | tail -5 || true

# 查找字幕文件（优先 vtt/srt 格式）
SUB_FILE=$(find "$SUBS_DIR" -name "*.vtt" -o -name "*.srt" | head -1)

if [ -n "$SUB_FILE" ] && [ -f "$SUB_FILE" ]; then
    echo "✅ 找到字幕: $SUB_FILE"
    USE_SUBS=true
else
    echo "⚠️ 无字幕，将使用 Whisper 转录"
    USE_SUBS=false
fi

# ===== 分支处理 =====
if [ "$USE_SUBS" = true ]; then
    # ===== 字幕路径：直接提取文本 =====
    echo ""
    echo "[3/4] 提取字幕文本..."
    
    # 提取纯文本（去掉时间戳等格式）
    grep -vE "^[0-9]+$|^WEBVTT|^Kind:|^Language:|-->|^$" "$SUB_FILE" | \
        sed 's/<[^>]*>//g' | \
        tr -d '\r' | \
        awk 'NF' > "$CACHE_TRANSCRIPT"
    
    echo "✅ 字幕提取完成"
    
    METHOD="字幕下载"
else
    # ===== Whisper 转录路径 =====
    
    # 检查 Whisper 模型
    if [ ! -f "$MODELS_DIR/ggml-base.bin" ]; then
        rm -rf "$WORK_DIR"
        echo "❌ Whisper 模型未下载，请先运行: scripts/install_dependency.sh"
        exit 1
    fi
    
    echo ""
    echo "[3/4] 下载音频..."
    yt-dlp \
        $YTDLP_COOKIES \
        --format "bestaudio/best" \
        --extract-audio \
        --output "${AUDIO_FILE}" \
        --no-playlist \
        --no-warning \
        "$VIDEO_URL" 2>&1 | tail -5
    
    if [ ! -f "$AUDIO_FILE" ]; then
        rm -rf "$WORK_DIR"
        echo "❌ 音频下载失败"
        exit 1
    fi
    echo "✅ 音频下载完成"
    
    # 转换为 WAV
    echo ""
    echo "转换音频格式..."
    ffmpeg -i "$AUDIO_FILE" -ar 16000 -ac 1 -y "$WAV_FILE" -loglevel warning 2>&1 || true
    
    if [ ! -f "$WAV_FILE" ]; then
        rm -rf "$WORK_DIR"
        echo "❌ 格式转换失败"
        exit 1
    fi
    
    # Whisper 转录
    echo ""
    echo "Whisper 转录（可能需要1-5分钟）..."
    MODEL_PATH="$MODELS_DIR/ggml-base.bin"
    
    whisper-cli -m "$MODEL_PATH" -f "$WAV_FILE" -l auto -otxt -of "${WORK_DIR}/transcript" 2>&1 | grep -E "(processing|whisper_print|output_txt)" | tail -5 || true
    
    if [ ! -f "$TRANSCRIPT_TXT" ]; then
        rm -rf "$WORK_DIR"
        echo "❌ 转录失败"
        exit 1
    fi
    
    mv "$TRANSCRIPT_TXT" "$CACHE_TRANSCRIPT"
    
    METHOD="Whisper 转录"
fi

# ===== 步骤 4：清理临时文件 =====
echo ""
echo "[4/4] 清理临时文件..."

# 只清理中间文件，保留 transcript_raw.txt
rm -rf "$SUBS_DIR"
rm -f "$AUDIO_FILE" "$WAV_FILE" "$STATUS_FILE"
# 如果 whisper 生成了临时文件也清理
rm -f "$WORK_DIR/transcript.txt"
# 注意：transcript_raw.txt 保留不删除

echo ""
echo "=== 处理完成 ==="
echo ""
echo "标题: $VIDEO_TITLE"
echo "视频ID: $VIDEO_ID"
echo "链接: $VIDEO_URL"
echo "处理方式: $METHOD"
echo ""
echo "文件保存:"
echo "  转录: $CACHE_TRANSCRIPT"
echo "  总结: $CACHE_MD（待生成）"
echo ""
echo "--- 内容预览 ---"
head -c 100 "$CACHE_TRANSCRIPT"
echo ""
echo "---------------"
echo ""
echo "转录完成！请让大模型总结并保存到 md 文件"