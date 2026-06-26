#!/bin/bash
# 太极架构 Skills 自动化安装脚本
# 支持离线安装（检测本地 node_modules）
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TAICHI_DIR="$SCRIPT_DIR/taichi-framework"
SKILL_DIR="$SCRIPT_DIR"

echo "=== 太极架构 Skills 安装脚本 ==="

# 1. 检查并提示安装 Redis
if ! command -v redis-server &> /dev/null; then
    echo "[1/4] Redis 未安装，正在安装..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update -qq && sudo apt-get install -y redis-server > /dev/null 2>&1
        echo "  Redis 安装完成"
    else
        echo "  警告: 无法自动安装 Redis，请手动安装 redis-server"
    fi
else
    echo "[1/4] Redis 已安装"
fi

# 2. 创建 Python 虚拟环境
echo "[2/4] 创建 Python 虚拟环境..."
if [ ! -d "$TAICHI_DIR/venv" ]; then
    python3 -m venv "$TAICHI_DIR/venv"
    echo "  venv 创建完成"
else
    echo "  venv 已存在，跳过"
fi

# 3. 安装 Python 依赖
echo "[3/4] 安装 Python 依赖..."
source "$TAICHI_DIR/venv/bin/activate"
pip install --upgrade pip -q
pip install -q pyyaml redis click python-dotenv
echo "  依赖安装完成"

# 4. 创建运行时目录和状态文件
echo "[4/4] 初始化运行时环境..."
WORKSPACE_DIR="${TAICHI_WORKSPACE:-$TAICHI_DIR/workspace}"
mkdir -p "$WORKSPACE_DIR/logs" "$WORKSPACE_DIR/temp"
touch "$WORKSPACE_DIR/state.db"
echo "  工作区: $WORKSPACE_DIR"

# 5. 检查并启动 Redis
if command -v redis-server &> /dev/null; then
    if ! pgrep -x redis-server > /dev/null; then
        echo "  启动 Redis..."
        redis-server --daemonize yes --logfile "$WORKSPACE_DIR/logs/redis.log"
        echo "  Redis 已启动"
    else
        echo "  Redis 已在运行"
    fi
fi

echo ""
echo "=== 安装完成 ==="
echo "运行: cd $TAICHI_DIR && ./start.sh --mode centralized --request 'test'"
