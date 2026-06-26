#!/bin/bash
# Smart Search 发布脚本

set -e

echo "🚀 Smart Search 发布脚本 v2.0.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查登录状态
if ! clawhub whoami &>/dev/null; then
    echo "⚠️  未登录 ClawHub"
    echo ""
    echo "📝 请先登录："
    echo "   clawhub login"
    echo ""
    echo "🌐 或访问：https://clawhub.com"
    exit 1
fi

echo "✅ 已登录：$(clawhub whoami)"
echo ""

# 检查必要文件
echo "📋 检查必要文件..."
REQUIRED_FILES=("SKILL.md" "search.sh" "deploy-searx.sh" "_meta.json")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少必要文件：$file"
        exit 1
    fi
done
echo "✅ 所有必要文件存在"
echo ""

# 读取版本
VERSION=$(grep -o '"version": "[^"]*"' _meta.json | cut -d'"' -f4)
echo "📦 发布版本：v$VERSION"
echo ""

# 确认发布
read -p "是否确认发布 v$VERSION 到 ClawHub？(y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "❌ 发布已取消"
    exit 1
fi

echo ""
echo "🔄 发布中..."
echo ""

# 发布
clawhub publish . \
  --slug smart-search \
  --name "Smart Search" \
  --version "$VERSION" \
  --changelog "v$VERSION: SearX 1.1.0 + Tavily 双引擎架构，智能场景识别，一键部署"

echo ""
echo "🎉 发布成功！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 技能名称：smart-search"
echo "🏷️  版本号：v$VERSION"
echo "🌐 访问地址：https://clawhub.com/skills/smart-search"
echo ""
echo "📥 安装命令："
echo "   clawhub install smart-search"
echo ""
echo "📊 查看状态："
echo "   clawhub list"
echo ""
