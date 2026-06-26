#!/bin/bash
# CosyVoice 引擎安装脚本 (阿里通义实验室)
# 使用: bash scripts/install_cosyvoice.sh

set -e
CDIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$CDIR"

echo "=== 安装 CosyVoice2 引擎 ==="

# 1. 确保基础 venv 存在
if [ ! -d "venv" ]; then
    echo "[!] 未找到 venv，先执行基础安装..."
    bash scripts/auto_installer.sh
fi
source venv/bin/activate

# 2. 克隆 CosyVoice 源码到 venv 内部（不污染项目根目录）
COSYVOICE_DIR="venv/CosyVoice"
if [ ! -d "$COSYVOICE_DIR" ]; then
    echo "[*] 正在克隆 CosyVoice 源码..."
    git clone --depth 1 https://github.com/FunAudioLLM/CosyVoice.git "$COSYVOICE_DIR"
fi

cd "$COSYVOICE_DIR"

# 3. 安装 CosyVoice 本体依赖
echo "[*] 安装 CosyVoice 及其依赖..."
pip install -e .

# 4. 安装 Matcha-TTS 子依赖
if [ -d "third_party/Matcha-TTS" ]; then
    cd third_party/Matcha-TTS
    pip install -e .
    cd ../..
fi

cd "$CDIR"

# 5. 模型权重将在首次推理时自动从 ModelScope 下载至 ~/.openclaw/models/voice-clone/
# 可以通过设置 MODELSCOPE_CACHE 环境变量来控制下载路径（install.sh 中已设置）

echo ""
echo "=== CosyVoice 引擎安装完毕！==="
echo "启动方式: TTS_BACKEND=cosyvoice python server/app.py"
echo "或永久配置: 在 .env 文件中添加 TTS_BACKEND=cosyvoice"
