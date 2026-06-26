#!/bin/bash
# QQ 官方机器人后台运行脚本

cd "$(dirname "$0")"

LOG_FILE="$HOME/.openclaw/workspace/qq_bot.log"
PID_FILE="$HOME/.openclaw/workspace/qq_bot.pid"

case "${1:-start}" in
    start)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "🤖 QQ Bot 已在运行 (PID: $(cat $PID_FILE))"
            exit 0
        fi
        
        echo "🚀 启动 QQ 官方机器人 (后台运行)..."
        echo "📄 日志文件: $LOG_FILE"
        
        nohup python3 -u qq_official_bot.py > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        
        sleep 2
        
        if kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "✅ 启动成功 (PID: $(cat $PID_FILE))"
            echo ""
            echo "📋 常用命令:"
            echo "  查看日志: tail -f $LOG_FILE"
            echo "  停止: $0 stop"
            echo "  重启: $0 restart"
        else
            echo "❌ 启动失败，查看日志: $LOG_FILE"
            rm -f "$PID_FILE"
        fi
        ;;
    
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "🛑 停止 QQ Bot (PID: $PID)..."
                kill "$PID"
                rm -f "$PID_FILE"
                echo "✅ 已停止"
            else
                echo "⚠️ 进程不存在"
                rm -f "$PID_FILE"
            fi
        else
            echo "⚠️ 未找到 PID 文件，机器人可能未运行"
        fi
        ;;
    
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    
    status)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "🤖 QQ Bot 运行中 (PID: $(cat $PID_FILE))"
            echo "📄 日志: $LOG_FILE"
            echo ""
            echo "📊 最近日志:"
            tail -20 "$LOG_FILE"
        else
            echo "⚠️ QQ Bot 未运行"
            [ -f "$PID_FILE" ] && rm -f "$PID_FILE"
        fi
        ;;
    
    log)
        echo "📄 查看日志 (按 Ctrl+C 退出)..."
        tail -f "$LOG_FILE"
        ;;
    
    *)
        echo "用法: $0 {start|stop|restart|status|log}"
        echo ""
        echo "命令:"
        echo "  start   - 启动机器人 (后台运行)"
        echo "  stop    - 停止机器人"
        echo "  restart - 重启机器人"
        echo "  status  - 查看运行状态"
        echo "  log     - 查看实时日志"
        exit 1
        ;;
esac
