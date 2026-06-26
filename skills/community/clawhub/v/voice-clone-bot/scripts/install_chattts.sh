#!/bin/bash
# ChatTTS 引擎安装脚本 (2noise)
# 使用: bash scripts/install_chattts.sh

set -e
CDIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$CDIR"

echo "=== 安装 ChatTTS 引擎 ==="

# 1. 确保基础 venv 存在
if [ ! -d "venv" ]; then
    echo "[!] 未找到 venv，先执行基础安装..."
    bash scripts/auto_installer.sh
fi
source venv/bin/activate

# 2. 克隆 ChatTTS 源码
CHATTTS_DIR="venv/ChatTTS"
if [ ! -d "$CHATTTS_DIR" ]; then
    echo "[*] 正在克隆 ChatTTS 源码..."
    git clone --depth 1 https://github.com/2noise/ChatTTS.git "$CHATTTS_DIR"
fi

cd "$CHATTTS_DIR"

# 3. 安装依赖
echo "[*] 安装 ChatTTS 及其依赖..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
pip install -e .

cd "$CDIR"

echo ""
echo "=== ChatTTS 引擎安装完毕！==="
echo "注意：ChatTTS 使用随机种子生成不同音色，不支持零样本克隆。"
echo "启动方式: TTS_BACKEND=chattts python server/app.py"
