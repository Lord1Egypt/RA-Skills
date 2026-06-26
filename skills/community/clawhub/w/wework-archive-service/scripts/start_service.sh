#!/bin/bash
# 企业微信存档服务启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_PY="$SCRIPT_DIR/wework_combined_service.py"
PID_FILE="$SCRIPT_DIR/../wework_service.pid"
LOG_FILE="$SCRIPT_DIR/../wework_service.log"
CONFIG_FILE="$SCRIPT_DIR/../config/wework_config.json"

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 配置文件不存在: $CONFIG_FILE"
    echo "请先创建配置文件，参考 config/wework_config_template.json"
    exit 1
fi

# 检查Python依赖
echo "检查Python依赖..."
python3 -c "import flask, Crypto, requests" 2>/dev/null || {
    echo "安装Python依赖..."
    pip3 install flask pycryptodome requests
}

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "服务已在运行 (PID: $PID)"
        exit 0
    else
        echo "发现旧的PID文件，清理..."
        rm -f "$PID_FILE"
    fi
fi

# 启动服务
echo "启动企业微信存档服务..."
cd "$SCRIPT_DIR/.."
nohup python3 "$SERVICE_PY" > "$LOG_FILE" 2>&1 &
SERVICE_PID=$!

# 保存PID
echo $SERVICE_PID > "$PID_FILE"
echo "服务已启动 (PID: $SERVICE_PID)"
echo "日志文件: $LOG_FILE"
echo "服务运行在: http://localhost:8400"

# 等待服务启动
sleep 2
if ps -p $SERVICE_PID > /dev/null 2>&1; then
    echo "服务启动成功!"
    echo "检查服务状态: curl http://localhost:8400/health"
else
    echo "警告: 服务可能启动失败，请检查日志: $LOG_FILE"
fi