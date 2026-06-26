#!/bin/bash
# telegram-signin.sh - Telegram 机器人自动签到脚本
# 用法: ./telegram-signin.sh [session-name] [bot-name]
# 默认 session-name: telegram-web
# 默认 bot-name: OkEmbyBot

SESSION_NAME="${1:-telegram-web}"
BOT_NAME="${2:-OkEmbyBot}"
CHECKIN_REF=""

echo "=== Telegram 自动签到 ==="
echo "Session: $SESSION_NAME"
echo "Bot: $BOT_NAME"
echo ""

# 打开 Telegram Web
echo "[1/6] 打开 Telegram Web..."
agent-browser --session-name "$SESSION_NAME" open https://web.telegram.org
sleep 4

# 打开机器人命令键盘
echo "[2/6] 打开命令键盘..."
agent-browser --session-name "$SESSION_NAME" snapshot -i > /dev/null 2>&1
agent-browser --session-name "$SESSION_NAME" click e35 2>/dev/null
sleep 1

# 发送 /start 命令
echo "[3/6] 发送 /start 命令..."
agent-browser --session-name "$SESSION_NAME" fill e90 "/start" 2>/dev/null
agent-browser --session-name "$SESSION_NAME" press Enter 2>/dev/null
sleep 3

# 找到签到按钮
echo "[4/6] 查找签到按钮..."
CHECKIN_REF=$(agent-browser --session-name "$SESSION_NAME" snapshot -i 2>&1 | grep "签到" | tail -1 | grep -o 'ref=e[0-9]*' | tail -1 | cut -d'=' -f2)

if [ -z "$CHECKIN_REF" ]; then
    echo "错误：找不到签到按钮"
    agent-browser --session-name "$SESSION_NAME" screenshot /tmp/checkin-error.png
    echo "截图已保存到 /tmp/checkin-error.png"
    exit 1
fi

echo "找到签到按钮: e$CHECKIN_REF"

# 点击签到按钮
echo "[5/6] 点击签到按钮 (e$CHECKIN_REF)..."
agent-browser --session-name "$SESSION_NAME" click "e$CHECKIN_REF"
sleep 5

# 截图验证
echo "[6/6] 截图验证..."
agent-browser --session-name "$SESSION_NAME" screenshot /tmp/checkin-result.png

echo ""
echo "=== 完成 ==="
echo "截图已保存到 /tmp/checkin-result.png"
echo "请查看截图确认签到结果。"