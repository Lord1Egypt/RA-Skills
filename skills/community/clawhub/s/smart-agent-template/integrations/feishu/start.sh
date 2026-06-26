#!/bin/bash
# 飞书 Bot 启动脚本（自动加载 .env）

set -e

cd "$(dirname "$0")"

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "❌ 未找到 .env 文件"
    echo "请复制 .env.example 并填入配置："
    echo "  cp .env.example .env"
    echo "  vim .env"
    exit 1
fi

# 加载环境变量
export $(grep -v '^#' .env | xargs)

# 检查必需配置
if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ]; then
    echo "❌ 缺少必需配置：FEISHU_APP_ID 或 FEISHU_APP_SECRET"
    exit 1
fi

if [ -z "$AI_ENGINE" ]; then
    echo "❌ 缺少 AI_ENGINE 配置"
    exit 1
fi

# 启动 Bot
echo "🚀 启动飞书 Bot..."
python3 bot.py
