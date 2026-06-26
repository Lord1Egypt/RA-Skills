#!/bin/bash
# Token Burn Monitor - Service management

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="/tmp/token-burn-monitor.pid"
LOG_FILE="/tmp/token-burn-monitor.log"
PORT="${PORT:-3847}"

start() {
    if is_running; then
        echo "Token Burn Monitor already running (PID: $(cat $PID_FILE))"
        return 0
    fi
    
    cd "$SCRIPT_DIR"
    nohup node server.js > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "🔥 Token Burn Monitor started (PID: $!)"
    echo "   URL: http://localhost:$PORT"
}

stop() {
    if [ -f "$PID_FILE" ]; then
        kill $(cat "$PID_FILE") 2>/dev/null
        rm -f "$PID_FILE"
        echo "Token Burn Monitor stopped"
    else
        echo "Token Burn Monitor not running"
    fi
}

is_running() {
    if [ -f "$PID_FILE" ]; then
        if kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            return 0
        else
            rm -f "$PID_FILE"
        fi
    fi
    return 1
}

status() {
    if is_running; then
        echo "Token Burn Monitor running (PID: $(cat $PID_FILE))"
        echo "URL: http://localhost:$PORT"
    else
        echo "Token Burn Monitor not running"
    fi
}

ensure() {
    if ! is_running; then
        start > /dev/null 2>&1
    fi
}

case "${1:-start}" in
    start)   start ;;
    stop)    stop ;;
    restart) stop; sleep 1; start ;;
    status)  status ;;
    ensure)  ensure ;;
    *)       echo "Usage: $0 {start|stop|restart|status|ensure}" ;;
esac
