#!/bin/bash
# quick-publish.sh - 简化版发布脚本（直接发布，不交互）

set -e

echo "========================================="
echo "🚀 快速发布 Threshold Trader 到 ClawHub"
echo "========================================="
echo ""

# 默认版本
VERSION="${1:-1.0.0}"

echo "📌 发布信息："
echo "   Slug: threshold-trader"
echo "   Version: $VERSION"
echo "   Account: $(npx clawhub@latest whoami 2>/dev/null || echo '未登录')"
echo ""

read -p "确认发布? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ 取消发布"
    exit 0
fi

echo ""
echo "🔄 正在发布..."
npx clawhub@latest publish . --slug threshold-trader --version "$VERSION"

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✅ 发布成功！"
    echo "========================================="
    echo ""
    echo "📊 验证安装："
    echo "   npx clawhub@latest install threshold-trader"
    echo ""
    echo "🌐 查看技能："
    echo "   https://clawhub.ai/skills/threshold-trader"
    echo ""
    echo "⏰ Simmer 同步："
    echo "   6小时后出现在 https://simmer.markets/skills"
    echo ""
else
    echo ""
    echo "========================================="
    echo "❌ 发布失败"
    echo "========================================="
    echo ""
    echo "🔧 可能的原因："
    echo "   1. GitHub API 限制（等待几小时后重试）"
    echo "   2. 网络问题（检查连接）"
    echo "   3. 账户权限（确认已登录）"
    echo ""
    echo "💡 解决方案："
    echo "   1. 等待 1-2 小时后重新运行："
    echo "      ./quick-publish.sh $VERSION"
    echo ""
    echo "   2. 检查 ClawHub 状态："
    echo "      https://clawhub.ai"
    echo ""
    echo "   3. 联系支持："
    echo "      ClawHub Discord/Telegram"
    echo ""
    exit 1
fi
