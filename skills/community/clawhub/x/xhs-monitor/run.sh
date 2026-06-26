#!/bin/bash
# 小红书竞品监控定时任务
# 
# 使用说明：
# 1. 设置环境变量：export CHROMIUM_PATH="你的Chrome路径"
# 2. 设置数据目录：export XHS_DATA_DIR="$HOME/xhs-monitor/data"
# 3. 添加定时任务

# 配置（可根据需要修改）
CHROMIUM_PATH=${CHROMIUM_PATH:-""}
XHS_DATA_DIR=${XHS_DATA_DIR:-"$HOME/xhs-monitor/data"}
DEBUG_PORT=${DEBUG_PORT:-9223}
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 查找 Chrome（Mac/Linux）
if [ -z "$CHROMIUM_PATH" ]; then
    if [ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
        CHROMIUM_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif [ -f "/usr/bin/google-chrome" ]; then
        CHROMIUM_PATH="/usr/bin/google-chrome"
    fi
fi

cd "$PROJECT_DIR/src"

# 确保数据目录存在
mkdir -p "$XHS_DATA_DIR"

# 确保浏览器在运行
if ! curl -s "http://localhost:$DEBUG_PORT/json/version" > /dev/null 2>&1; then
    if [ -n "$CHROMIUM_PATH" ] && [ -f "$CHROMIUM_PATH" ]; then
        echo "启动浏览器..."
        "$CHROMIUM_PATH" \
            --remote-debugging-port=$DEBUG_PORT \
            --user-data-dir="$XHS_DATA_DIR/browser" \
            --no-first-run \
            "https://www.xiaohongshu.com/" &
        sleep 5
    else
        echo "警告: 未找到Chrome，请设置 CHROMIUM_PATH 环境变量"
    fi
fi

# 运行主程序
node main.js >> ../logs/cron.log 2>&1
