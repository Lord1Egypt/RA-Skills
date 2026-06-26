#!/usr/bin/env bash
# ─────────────────────────────────────────────
# WeChat Work 通知 Skill - 一键安装脚本
# ─────────────────────────────────────────────

set -e

echo "🚀 WeChat Work 通知 Skill 安装"

# 检查 requests 库
if ! python3 -c "import requests" 2>/dev/null; then
    echo "📦 安装 requests..."
    pip install requests
fi

echo "✅ 安装完成！"
echo ""
echo "下一步："
echo "1. 获取企业微信群机器人 Webhook URL"
echo "2. 设置环境变量："
echo "   export WECHAT_WEBHOOK_URL='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=XXX'"
echo ""
echo "测试发送："
echo "   python -m skills.wechat_notify --text 'Hello WeChat!'"
