#!/bin/bash
# OpenVoice V2 引擎安装脚本 (MyShell AI)
# 使用: bash scripts/install_openvoice.sh

set -e
CDIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$CDIR"

echo "=== 安装 OpenVoice V2 引擎 ==="

# 1. 确保基础 venv 存在
if [ ! -d "venv" ]; then
    echo "[!] 未找到 venv，先执行基础安装..."
    bash scripts/auto_installer.sh
fi
source venv/bin/activate

# 2. 克隆 OpenVoice 源码
OPENVOICE_DIR="venv/OpenVoice"
if [ ! -d "$OPENVOICE_DIR" ]; then
    echo "[*] 正在克隆 OpenVoice 源码..."
    git clone --depth 1 https://github.com/myshell-ai/OpenVoice.git "$OPENVOICE_DIR"
fi

cd "$OPENVOICE_DIR"

# 3. 安装 OpenVoice 核心
echo "[*] 安装 OpenVoice 及其依赖..."
pip install -e .

cd "$CDIR"

# 4. 下载 V2 权重至全局模型目录
MODEL_DIR="$HOME/.openclaw/models/voice-clone/OpenVoice"
if [ ! -d "$MODEL_DIR/checkpoints_v2" ]; then
    echo "[*] 正在下载 OpenVoice V2 权重..."
    mkdir -p "$MODEL_DIR"
    pip install huggingface_hub
    python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='myshell-ai/OpenVoiceV2',
    local_dir='$MODEL_DIR/checkpoints_v2'
)
print('权重下载完毕！')
"
fi

echo ""
echo "=== OpenVoice V2 引擎安装完毕！==="
echo "模型权重: $MODEL_DIR/checkpoints_v2/"
echo "启动方式: TTS_BACKEND=openvoice python server/app.py"
