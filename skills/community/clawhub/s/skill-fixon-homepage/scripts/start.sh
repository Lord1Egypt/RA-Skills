#!/bin/bash
# 启动 OpenClaw 主页插件服务

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.openclaw/homepage"
PID_FILE="$CONFIG_DIR/server.pid"
LOG_FILE="$CONFIG_DIR/server.log"

# 检查配置文件
if [ ! -f "$CONFIG_DIR/config.yaml" ]; then
    echo "❌ 配置文件不存在，请先运行: bash $BASE_DIR/init.sh"
    exit 1
fi

# 检查是否已运行
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "❌ 服务已在运行中 (PID: $PID)"
        exit 1
    fi
    rm -f "$PID_FILE"
fi

# 读取配置中的端口
PORT=$(grep "^[[:space:]]*port:" "$CONFIG_DIR/config.yaml" | awk '{print $2}' || echo "8080")

echo "🚀 启动 OpenClaw 主页插件服务..."
echo "   端口: $PORT"
echo "   日志: $LOG_FILE"

# 启动服务
cd "$BASE_DIR"
nohup python3 main.py > "$LOG_FILE" 2>&1 &
PID=$!
echo $PID > "$PID_FILE"

sleep 2

# 检查是否启动成功
if ps -p $PID > /dev/null 2>&1; then
    echo "✅ 服务已启动 (PID: $PID)"
    echo "   健康检查: http://localhost:$PORT/homepage/health"
    echo "   聊天接口: http://localhost:$PORT/homepage/chat"
else
    echo "❌ 服务启动失败，请查看日志: $LOG_FILE"
    exit 1
fi
