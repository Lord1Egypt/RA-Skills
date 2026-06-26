#!/bin/bash
# 大米追踪系统启动脚本
# 用法: ./start.sh [flask|gunicorn]

cd "$(dirname "$0")"

MODE="${1:-gunicorn}"
PORT=5001
HOST="0.0.0.0"

# 检查端口是否被占用
check_port() {
    lsof -i :$PORT >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "⚠️ 端口 $PORT 已被占用，正在停止旧进程..."
        lsof -ti :$PORT | xargs kill -9 2>/dev/null
        sleep 1
    fi
}

# 获取本机 IP
get_ip() {
    ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}'
}

check_port

if [ "$MODE" = "flask" ]; then
    echo "🚀 启动模式: Flask 开发服务器"
    echo "   本机访问: http://localhost:$PORT"
    echo "   手机访问: http://$(get_ip):$PORT"
    echo ""
    nohup python3 app.py > app.log 2>&1 &
    echo $! > app.pid
else
    echo "🚀 启动模式: Gunicorn 生产服务器"
    echo "   本机访问: http://localhost:$PORT"
    echo "   手机访问: http://$(get_ip):$PORT"
    echo ""
    nohup gunicorn --bind $HOST:$PORT --workers 2 --threads 4 app:app > app.log 2>&1 &
    echo $! > app.pid
fi

sleep 2

# 检查是否启动成功
if curl -s http://localhost:$PORT >/dev/null 2>&1; then
    echo "✅ 服务启动成功！"
    echo ""
    echo "📋 使用说明:"
    echo "   - 浏览器打开上述地址即可访问"
    echo "   - 查看日志: tail -f $(pwd)/app.log"
    echo "   - 停止服务: ./stop.sh"
else
    echo "❌ 服务启动失败，请查看日志:"
    cat app.log
fi
