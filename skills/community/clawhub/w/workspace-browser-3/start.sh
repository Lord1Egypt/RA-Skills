#!/bin/bash
cd "$(dirname "$0")"
pkill -f "python3.*app.py" 2>/dev/null
sleep 2
# 启动应用（数据库初始化在app.py中自动执行）
python3 app.py > app.log 2>&1 &
echo "Workspace浏览器3.0 已启动"
echo "访问地址: http://175.178.154.173:5001"
echo "日志文件: app.log"