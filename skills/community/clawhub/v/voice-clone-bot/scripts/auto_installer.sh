#!/bin/bash
# voice-clone 全自动沙箱配置与注册运维中心

set -e
echo "=== 自动探测与注册 voice-clone-bot 全局插件环境 ==="

# 0. 宿主注册机制（面向 Agent 自主化）
SKILLS_DIR="$HOME/.openclaw/skills"
THIS_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ -d "$SKILLS_DIR" ]; then 
    SKILL_LINK="$SKILLS_DIR/voice-clone-bot"
    if [ -L "$SKILL_LINK" ] || [ -d "$SKILL_LINK" ]; then
        echo "[*] 技能路由已存在于宿主中：$SKILL_LINK，继续检查依赖..."
    else
        echo "[*] 未在宿主 OpenClaw 大脑中找到路由锚点，为您自动搭建软链接注册..."
        ln -s "$THIS_DIR" "$SKILL_LINK"
    fi
fi

# 1. 设置模型存放全局常量路径 (遵循严苛无感知要求)
GLOBAL_MODEL_DIR="$HOME/.openclaw/models/voice-clone"
if [ ! -d "$GLOBAL_MODEL_DIR" ]; then
    echo "[!] 未检测到全局模型权重库，自动建立隔离锚点: $GLOBAL_MODEL_DIR"
    mkdir -p "$GLOBAL_MODEL_DIR"
fi

# 2. 拉起独立的 Python 推理沙盒环境
if [ ! -d "venv" ]; then
    echo "=== 初始化独立的 Python 推理隔离环境 (Venv) ==="
    python3 -m venv venv
    echo "[*] 成功创建 venv"
fi

# 切换为隔离期的 Pip 通道
source venv/bin/activate
pip install --upgrade pip

# 3. 安装前序依赖组件 (F5-TTS, Torch 等)
echo "=== 开始解析并安装 Server 端依赖图谱 (免干扰模式) ==="
if [ -f "server/requirements.txt" ]; then
    pip install -r server/requirements.txt
    export HF_HOME="$GLOBAL_MODEL_DIR"
else
    echo "[!] 警告：未检测到 server/requirements.txt！"
fi

echo "=== 安装基建处理完毕！Agent 现在可以放心拉起 run_tts.sh 守护进程了 ==="
