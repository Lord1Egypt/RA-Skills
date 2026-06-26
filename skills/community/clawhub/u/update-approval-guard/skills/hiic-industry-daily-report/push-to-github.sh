#!/bin/bash

# HIIC产业日报技能 - GitHub推送脚本
# 使用方法：./push-to-github.sh

set -e

echo "🚀 准备推送HIIC产业日报技能到GitHub..."
echo ""

# 配置
REPO_NAME="hiic-industry-daily-report"
REPO_URL="https://github.com/Waytobetter619/${REPO_NAME}.git"
COMMIT_MSG="v1.2.0: 简体中文统一、摘要优化、翻译功能"

# 检查是否已初始化Git
if [ ! -d ".git" ]; then
    echo "📦 初始化Git仓库..."
    git init
    git branch -M main
fi

# 检查是否有远程仓库
if ! git remote | grep -q "origin"; then
    echo "🔗 添加远程仓库..."
    git remote add origin ${REPO_URL}
fi

# 添加所有文件
echo "➕ 添加所有文件..."
git add .

# 提交
echo "💾 提交更改..."
git commit -m "${COMMIT_MSG}" || echo "没有需要提交的更改"

# 推送
echo "📤 推送到GitHub..."
git push -u origin main

echo ""
echo "✅ 推送完成！"
echo "🔗 仓库地址: ${REPO_URL}"
