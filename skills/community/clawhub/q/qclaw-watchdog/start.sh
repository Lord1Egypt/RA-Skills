#!/bin/bash
# QClaw Watchdog 启动脚本 / Start script

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 加载 nvm (如果可用) / Load nvm (if available)
if [ -f "$HOME/.nvm/nvm.sh" ]; then
    source "$HOME/.nvm/nvm.sh"
fi

# 检查 Node.js / Check Node.js
if ! command -v node &> /dev/null; then
    echo "错误: Node.js 未安装"
    echo "Error: Node.js is not installed"
    exit 1
fi

# 设置 NODE_PATH 包含 QClaw 的 Lark SDK
# Set NODE_PATH to include QClaw's Lark SDK
export NODE_PATH="/Applications/QClaw.app/Contents/Resources/openclaw/node_modules:$NODE_PATH"

cd "$SCRIPT_DIR"

echo "启动 QClaw 看门狗..."
echo "Starting QClaw Watchdog..."
echo "Node: $(node --version)"
echo ""

# 运行看门狗 / Run watchdog
node watchdog.js "$@" 2>&1 | tee -a watchdog.log
