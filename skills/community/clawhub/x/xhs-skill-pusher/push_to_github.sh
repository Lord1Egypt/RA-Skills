#!/bin/bash
# 推送到GitHub的脚本

set -e

REPO_NAME="xhs-skill-pusher"
REPO_DESC="小红书内容发布技能 - 规范化cookie管理 + xhs-kit自动化发布"
USERNAME="beizhi-tech"  # 替换为实际的GitHub用户名

echo "🚀 准备推送到GitHub..."

# 检查是否已设置远程仓库
if git remote | grep -q origin; then
    echo "✅ 远程仓库已设置"
else
    echo "❌ 未设置远程仓库"
    echo "请先创建GitHub仓库:"
    echo "1. 访问: https://github.com/new"
    echo "2. 仓库名称: $REPO_NAME"
    echo "3. 描述: $REPO_DESC"
    echo "4. 选择公开或私有"
    echo ""
    echo "创建后运行:"
    echo "  git remote add origin https://github.com/$USERNAME/$REPO_NAME.git"
    echo "  git push -u origin main"
    exit 1
fi

# 推送到GitHub
echo "推送代码到GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 推送成功！"
    echo ""
    echo "📦 项目信息:"
    echo "  名称: $REPO_NAME"
    echo "  描述: $REPO_DESC"
    echo "  版本: v1.0.0"
    echo ""
    echo "🚀 快速开始:"
    echo "  git clone https://github.com/$USERNAME/$REPO_NAME.git"
    echo "  cd $REPO_NAME"
    echo "  npm install"
    echo "  详细指南: docs/QUICK_START.md"
else
    echo "❌ 推送失败"
    echo "请检查:"
    echo "1. GitHub仓库是否存在"
    echo "2. 是否有推送权限"
    echo "3. 网络连接是否正常"
fi