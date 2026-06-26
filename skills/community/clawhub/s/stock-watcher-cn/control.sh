#!/bin/bash

# stock-monitor 控制脚本

SCRIPT_DIR=$(dirname "$0")
MONITOR_PY="$SCRIPT_DIR/monitor.py"
LOG_FILE="$SCRIPT_DIR/logs/stock-watcher.log"
PID_FILE="$SCRIPT_DIR/pid/stock-watcher.pid"

# 确保日志和pid目录存在
mkdir -p "$SCRIPT_DIR/logs"
mkdir -p "$SCRIPT_DIR/pid"

start() {
    echo "启动股票盯盯系统..."
    if [ -f "$PID_FILE" ]; then
        echo "股票盯盯已经在运行中 (PID: $(cat $PID_FILE))"
        return 1
    fi
    
    # 启动监控进程
    python3 "$MONITOR_PY" --daemon &
    PID=$!
    echo $PID > "$PID_FILE"
    echo "股票盯盯启动成功，PID: $PID"
    echo "日志文件: $LOG_FILE"
}

stop() {
    echo "停止股票盯盯系统..."
    if [ ! -f "$PID_FILE" ]; then
        echo "股票盯盯未运行"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    kill $PID
    rm "$PID_FILE"
    echo "股票盯盯已停止"
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        echo "股票盯盯正在运行，PID: $PID"
        ps -p $PID
    else
        echo "股票盯盯未运行"
    fi
}

log() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo "日志文件不存在"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    log)
        log
        ;;
    *)
        echo "用法: $0 {start|stop|status|log}"
        exit 1
        ;;
esac