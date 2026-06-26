#!/bin/bash
# STT Simple - One-Command Install / 一键安装
# Creates virtual environment, installs Whisper, downloads model
# 创建虚拟环境、安装 Whisper、下载模型

set -e

# Configuration / 配置
VENV_DIR="/root/.openclaw/venv/stt-simple"
OUTPUT_DIR="/root/.openclaw/workspace/stt_output"
MODEL_NAME="small"
SKILL_DIR="$(dirname "$0")"

# Colors / 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }
log_ok() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "========================================"
echo "  STT Simple - Local Speech-to-Text"
echo "  本地语音识别安装程序"
echo "  Installing Whisper + Dependencies"
echo "========================================"
echo ""

# Step 1: Check Python / 检查 Python
log_step "Checking Python... / 检查 Python..."
if ! command -v python3 &> /dev/null; then
    log_error "Python3 not found. Please install Python 3.8+ / 未找到 Python3，请安装 Python 3.8+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
log_ok "Python $PYTHON_VERSION found / 已找到 Python $PYTHON_VERSION"

# Step 2: Check/Create Virtual Environment / 检查/创建虚拟环境
log_step "Setting up virtual environment... / 设置虚拟环境..."
if [ -d "$VENV_DIR" ]; then
    log_warn "Virtual environment exists, recreating... / 虚拟环境已存在，重新创建..."
    rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR"
log_ok "Virtual environment created: $VENV_DIR / 虚拟环境已创建"

# Step 3: Install FFmpeg / 安装 FFmpeg
log_step "Checking FFmpeg... / 检查 FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    log_warn "FFmpeg not found, installing... / 未找到 FFmpeg，正在安装..."
    if command -v apt-get &> /dev/null; then
        apt-get update && apt-get install -y ffmpeg
    elif command -v yum &> /dev/null; then
        yum install -y ffmpeg
    elif command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        log_error "Cannot install FFmpeg automatically. Please install manually. / 无法自动安装 FFmpeg，请手动安装"
        exit 1
    fi
    log_ok "FFmpeg installed / FFmpeg 已安装"
else
    log_ok "FFmpeg already installed: $(ffmpeg -version | head -1) / FFmpeg 已安装"
fi

# Step 4: Install Whisper / 安装 Whisper
log_step "Installing OpenAI Whisper (this may take 2-5 minutes)... / 正在安装 OpenAI Whisper（可能需要 2-5 分钟）..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install openai-whisper
log_ok "Whisper installed / Whisper 已安装"

# Step 5: Download Model / 下载模型
log_step "Downloading Whisper '$MODEL_NAME' model (~244MB)... / 正在下载 Whisper '$MODEL_NAME' 模型（约 244MB）..."
# Model downloads on first use, trigger it / 模型在首次使用时下载，触发下载
"$VENV_DIR/bin/python" -c "import whisper; print('Loading model... / 正在加载模型...'); whisper.load_model('$MODEL_NAME'); print('Done / 完成')"
log_ok "Model downloaded to ~/.cache/whisper / 模型已下载到 ~/.cache/whisper"

# Step 6: Create Output Directory / 创建输出目录
log_step "Creating output directory... / 创建输出目录..."
mkdir -p "$OUTPUT_DIR"
log_ok "Output directory: $OUTPUT_DIR / 输出目录"

# Step 7: Verify Installation / 验证安装
echo ""
echo "========================================"
log_step "Verifying installation... / 验证安装..."
echo "========================================"

"$VENV_DIR/bin/whisper" --version
echo ""

# Test with a quick import / 快速导入测试
"$VENV_DIR/bin/python" -c "import whisper; print('Whisper version:', whisper.__version__)"

echo ""
echo "========================================"
echo "  ✅ Installation Complete! / 安装完成!"
echo "========================================"
echo ""
echo "Usage / 使用方法:"
echo "  # Transcribe audio file / 转录音频文件"
echo "  $VENV_DIR/bin/whisper audio.ogg --model small --language Chinese"
echo ""
echo "  # Or use Python script / 或使用 Python 脚本"
echo "  $VENV_DIR/bin/python $SKILL_DIR/stt_simple.py audio.ogg small zh"
echo ""
echo "Output directory / 输出目录: $OUTPUT_DIR"
echo ""
