#!/bin/bash
# xiaozhi-mcp-server Start Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER="$SCRIPT_DIR/server.py"
PORT=${XIAOZHI_MCP_PORT:-9000}
LOG_FILE="/tmp/xiaozhi-mcp.log"
PID_FILE="/tmp/xiaozhi-mcp.pid"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
echo_error() { echo -e "${RED}[ERROR]${NC} $1"; }

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

# Stop old process
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" &> /dev/null; then
        echo_info "Stopping old process (PID: $OLD_PID)"
        kill "$OLD_PID" 2>/dev/null || true
        sleep 1
    fi
fi

pkill -f "xiaozhi-mcp-server" 2>/dev/null || true

# Start
echo_info "Starting xiaozhi-mcp-server on port $PORT..."
nohup python3 "$SERVER" http "$PORT" > "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo "$NEW_PID" > "$PID_FILE"

sleep 2

if ps -p "$NEW_PID" &> /dev/null; then
    TOKEN=$(cat ~/.config/openclaw-mcp/token 2>/dev/null || echo "Check log")
    IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "localhost")

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
    echo "=============================================="
else
    echo_error "Failed to start"
    echo_error "Check log: tail -f $LOG_FILE"
    exit 1
fi