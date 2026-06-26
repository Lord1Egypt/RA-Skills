#!/bin/bash
# xiaozhi-mcp-server Start Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER="$SCRIPT_DIR/server.py"
CONFIG_FILE="$SCRIPT_DIR/../config.yaml"
PORT=${XIAOZHI_MCP_PORT:-28765}
LOG_FILE="/tmp/xiaozhi-mcp.log"
PID_FILE="/tmp/xiaozhi-mcp.pid"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
echo_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
echo_error() { echo -e "${RED}[ERROR]${NC} $1"; }
echo_prompt() { echo -e "${BLUE}[?]${NC} $1"; }

# Check Python
if ! command -v python3 &> /dev/null; then
    echo_error "Python3 not found"
    exit 1
fi

# Check dependencies
if ! python3 -c "import aiohttp" 2>/dev/null; then
    echo_info "Installing aiohttp..."
    pip3 install aiohttp --break-system-packages -q
fi

if ! python3 -c "import yaml" 2>/dev/null; then
    echo_info "Installing pyyaml..."
    pip3 install pyyaml --break-system-packages -q
fi

# Check config
check_target_session() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo_warn "config.yaml not found, creating default..."
        cat > "$CONFIG_FILE" << 'EOF'
# xiaozhi-mcp-server Configuration

# Server port (冷门端口避免冲突)
port: 28765

# Token (auto-generated if empty)
# Set your own token or leave empty for auto-generation
token: ""

# Target session for OpenClaw responses
# Format: channel:type:ID
# Examples:
#   QQ:         qqbot:c2c:你的QQ号 / qqbot:group:群号
#   飞书:       feishu:c2c:用户OpenID / feishu:group:群ID
#   钉钉:       ddingtalk:c2c:用户ID / ddingtalk:group:群ID
#   企业微信:   wecom:c2c:用户ID
#   Telegram:   telegram:c2c:用户ID
#   Discord:    discord:c2c:用户ID
target_session: ""

# Task timeout in seconds
task_timeout: 180

# Log level: debug, info, warn, error
log_level: info
EOF
    fi

    # Check if target_session is empty
    TARGET_SESSION=$(grep "^target_session:" "$CONFIG_FILE" | sed 's/target_session: *//' | tr -d '"')

    if [ -z "$TARGET_SESSION" ] || [ "$TARGET_SESSION" = '""' ]; then
        echo ""
        echo_warn "target_session 未配置！"
        echo ""
        echo "  target_session 决定了 OpenClaw 的回复发送到哪个会话。"
        echo ""
        echo "  支持的平台格式："
        echo "    QQ私聊:     qqbot:c2c:你的QQ号"
        echo "    QQ群:       qqbot:group:群号"
        echo "    飞书私聊:   feishu:c2c:用户OpenID"
        echo "    飞书群:     feishu:group:群ID"
        echo "    钉钉私聊:   ddingtalk:c2c:用户ID"
        echo "    钉钉群:     ddingtalk:group:群ID"
        echo "    企业微信:   wecom:c2c:用户ID"
        echo "    Telegram:   telegram:c2c:用户ID"
        echo "    Discord:    discord:c2c:用户ID"
        echo ""
        echo_prompt "请输入你的 target_session (留空跳过，稍后手动配置): "
        read -r USER_INPUT

        if [ -n "$USER_INPUT" ]; then
            # Update config file
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' "s/^target_session:.*$/target_session: \"$USER_INPUT\"/" "$CONFIG_FILE"
            else
                # Linux
                sed -i "s/^target_session:.*$/target_session: \"$USER_INPUT\"/" "$CONFIG_FILE"
            fi
            echo_info "已保存 target_session: $USER_INPUT"
        else
            echo_warn "跳过配置，请稍后手动编辑 config.yaml"
            echo ""
            echo "  配置文件: $CONFIG_FILE"
            echo ""
        fi
    fi
}

check_target_session

# Stop old process
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" &> /dev/null; then
        echo_info "Stopping old process (PID: $OLD_PID)"
        kill "$OLD_PID" 2>/dev/null || true
        sleep 1
    fi
fi

pkill -f "server.py.*28765" 2>/dev/null || true
sleep 1

# Start
echo_info "Starting xiaozhi-mcp-server on port $PORT..."
nohup python3 "$SERVER" "$PORT" > "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo "$NEW_PID" > "$PID_FILE"

sleep 2

if ps -p "$NEW_PID" &> /dev/null; then
    TOKEN=$(cat ~/.config/openclaw-mcp/token 2>/dev/null || echo "Check log")
    IP=$(curl -s ifconfig.me 2>/dev/null || hostname -I 2>/dev/null | awk '{print $1}' || echo "localhost")

    echo ""
    echo "=============================================="
    echo "  xiaozhi-mcp-server Started"
    echo "=============================================="
    echo ""
    echo "  HTTP:  http://$IP:$PORT/mcp"
    echo "  WS:    ws://$IP:$PORT/ws"
    echo "  Token: $TOKEN"
    echo ""
    echo "  Log: $LOG_FILE"
    echo "  PID: $NEW_PID"
    echo ""
    echo "  在瞄小智服务号配置中填入："
    echo "  - 服务器地址: $IP"
    echo "  - 端口: $PORT"
    echo "  - 连接码: $TOKEN"
    echo "=============================================="
else
    echo_error "Failed to start"
    echo_error "Check log: tail -f $LOG_FILE"
    exit 1
fi