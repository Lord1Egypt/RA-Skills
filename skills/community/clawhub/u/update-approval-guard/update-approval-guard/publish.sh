#!/bin/bash

# Update Approval Guard 技能一键发布脚本
# 使用方法: ./publish.sh

set -e

echo "🦞 Update Approval Guard 技能发布脚本"
echo "=================================="
echo ""

# 检查是否在技能目录
if [ ! -f "SKILL.md" ]; then
    echo "❌ 错误: 请在 update-approval-guard 目录中运行此脚本"
    exit 1
fi

# 1. 检查 git 配置
echo "📝 步骤 1/6: 检查 Git 配置"
if ! git config user.email >/dev/null 2>&1; then
    echo "请输入你的邮箱:"
    read -r email
    git config --global user.email "$email"
fi

if ! git config user.name >/dev/null 2>&1; then
    echo "请输入你的名字:"
    read -r name
    git config --global user.name "$name"
fi

echo "✅ Git 配置完成"
echo ""

# 2. 初始化 Git 仓库
echo "📦 步骤 2/6: 初始化 Git 仓库"
if [ ! -d .git ]; then
    git init
    echo "✅ Git 仓库初始化完成"
else
    echo "ℹ️  Git 仓库已存在"
fi
echo ""

# 3. 创建提交
echo "💾 步骤 3/6: 创建 Git 提交"
git add .
git commit -m "Initial commit: Update Approval Guard skill for OpenClaw" || echo "ℹ️  没有新更改"
echo ""

# 4. GitHub 仓库
echo "🐙 步骤 4/6: 创建 GitHub 仓库"
echo "请选择创建方式:"
echo "  1) 自动创建（需要 gh CLI 认证）"
echo "  2) 手动创建（打开浏览器）"
echo "  3) 已创建（输入仓库 URL）"
read -p "选择 (1/2/3): " choice

case $choice in
    1)
        echo "自动创建 GitHub 仓库..."
        gh repo create update-approval-guard --public \
          --description="Daily update checker for OpenClaw and installed skills with approval workflow" \
          --source=. --push
        REPO_URL="https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)"
        ;;
    2)
        echo "请在浏览器中创建仓库:"
        echo "https://github.com/new"
        echo ""
        echo "创建完成后，输入仓库 URL（例如: https://github.com/your-username/update-approval-guard）:"
        read -r REPO_URL
        git remote add origin "$REPO_URL"
        git branch -M main
        git push -u origin main
        ;;
    3)
        echo "输入仓库 URL（例如: https://github.com/your-username/update-approval-guard）:"
        read -r REPO_URL
        git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"
        git branch -M main
        git push -u origin main
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo "✅ GitHub 仓库创建完成: $REPO_URL"
echo ""

# 5. 登录 ClawHub
echo "🦞 步骤 5/6: 登录 ClawHub"
if ! clawhub whoami >/dev/null 2>&1; then
    echo "需要登录 ClawHub..."
    clawhub login
else
    echo "ℹ️  已登录 ClawHub"
fi
echo ""

# 6. 发布到 ClawHub
echo "🚀 步骤 6/6: 发布到 ClawHub"
clawhub publish . \
  --slug update-approval-guard \
  --name "Update Approval Guard" \
  --version 1.0.0 \
  --changelog "Initial release: Daily update checker with approval workflow for OpenClaw"

echo ""
echo "✅ 发布完成！"
echo ""
echo "🔗 链接:"
echo "  - GitHub: $REPO_URL"
echo "  - ClawHub: https://clawhub.com/skills/update-approval-guard"
echo ""
echo "验证安装:"
echo "  clawhub search update-approval-guard"
echo "  clawhub install update-approval-guard"
