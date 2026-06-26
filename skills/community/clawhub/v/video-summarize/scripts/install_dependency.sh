#!/bin/bash
# 通用视频总结 - 环境安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$SKILL_DIR/.venv"
MODELS_DIR="$SKILL_DIR/whisper-models"

echo "=== 通用视频总结 Skill 环境安装 ==="
echo ""
echo "支持平台：B站、YouTube、抖音、Twitter、Instagram、TikTok 等"
echo ""

# ===== 步骤 1: 检测 Homebrew =====
echo "[1/7] 检测 Homebrew..."
if command -v brew &> /dev/null; then
    echo "✅ Homebrew 已安装"
else
    echo "❌ Homebrew 未安装"
    echo "正在安装 Homebrew（可能需要几分钟）..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # 添加 brew 到 PATH（Apple Silicon Mac）
    if [[ -d "/opt/homebrew/bin" ]] && ! grep -q "/opt/homebrew/bin" ~/.zshrc 2>/dev/null; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    echo "✅ Homebrew 安装完成"
fi

# ===== 步骤 2: 检测 Python =====
echo ""
echo "[2/7] 检测 Python..."
if command -v python3 &> /dev/null && python3 --version &>/dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✅ Python 已安装: $PYTHON_VERSION"
else
    echo "❌ Python 未安装"
    echo "正在通过 Homebrew 安装 Python..."
    brew install python3
    echo "✅ Python 安装完成"
fi

# ===== 步骤 3: 创建虚拟环境 =====
echo ""
echo "[3/7] 创建 Python 虚拟环境..."
if [ -d "$VENV_DIR" ]; then
    echo "✅ 虚拟环境已存在: $VENV_DIR"
else
    python3 -m venv "$VENV_DIR"
    echo "✅ 虚拟环境创建完成"
fi

# ===== 步骤 4: 安装 yt-dlp =====
echo ""
echo "[4/7] 安装 yt-dlp..."
source "$VENV_DIR/bin/activate"

if pip show yt-dlp &>/dev/null; then
    YTDLP_VERSION=$(pip show yt-dlp | grep Version | cut -d' ' -f2)
    echo "✅ yt-dlp 已安装: $YTDLP_VERSION"
else
    pip install --upgrade pip -q
    pip install yt-dlp -q
    echo "✅ yt-dlp 安装完成"
fi

# ===== 步骤 5: 安装 whisper.cpp =====
echo ""
echo "[5/7] 安装 whisper.cpp..."
if command -v whisper-cli &> /dev/null; then
    echo "✅ whisper.cpp 已安装"
else
    brew install whisper-cpp
    echo "✅ whisper.cpp 安装完成"
fi

# ===== 步骤 6: 下载 Whisper 模型 =====
echo ""
echo "[6/7] 下载 Whisper base 模型..."
mkdir -p "$MODELS_DIR"
MODEL_FILE="$MODELS_DIR/ggml-base.bin"

if [ -f "$MODEL_FILE" ]; then
    echo "✅ 模型已存在: $MODEL_FILE"
else
    echo "下载 ggml-base.bin (约 148MB)..."
    curl -L -o "$MODEL_FILE" \
        "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin"
    echo "✅ 模型下载完成"
fi

# ===== 步骤 7: 安装 ffmpeg =====
echo ""
echo "[7/7] 安装 ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg 已安装"
else
    brew install ffmpeg
    echo "✅ ffmpeg 安装完成"
fi

# ===== 完成 =====
echo ""
echo "=== 安装完成 ==="
echo "使用方法:"
echo "  ~/.agents/skills/video-summarize/scripts/process.sh '视频链接'"
echo ""
echo "支持链接格式:"
echo "  B站:       https://www.bilibili.com/video/BVxxx"
echo "  YouTube:   https://www.youtube.com/watch?v=xxx"
echo "  抖音:      https://www.douyin.com/video/xxx"
echo "  Twitter/X: https://twitter.com/user/status/xxx"
echo "  TikTok:    https://www.tiktok.com/@user/video/xxx"
echo "  其他:      yt-dlp 支持的任何平台"