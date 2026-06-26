#!/bin/bash
# Session Compactor - GitHub 一键部署脚本
# 在本地电脑执行（需已安装 git 并配置 GitHub 认证）

set -e

echo "🚀 Session Compactor 部署到 GitHub"
echo "=================================="

# 配置变量
GITHUB_USERNAME="fangbb-coder"
REPO_NAME="session-compactor"
TOKEN=""
REMOTE_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

# 检查是否在正确的目录
if [ ! -f "SKILL.md" ]; then
  echo "❌ 请在 session-compactor 目录下运行此脚本"
  exit 1
fi

# 1. 初始化 git (如果还没做)
if [ ! -d ".git" ]; then
  echo "📦 初始化 git 仓库..."
  git init
  git add -A
  git commit -m "feat: initial implementation of session-compactor skill"
else
  echo "📦 Git 仓库已存在，添加文件..."
  git add -A
  git commit -m "update: prepare for GitHub deployment" || echo "⚠️  无新更改提交"
fi

# 2. 设置远程仓库
echo "🔧 配置远程仓库: ${REMOTE_URL}"
git remote remove origin 2>/dev/null || true
git remote add origin "${REMOTE_URL}"

# 3. 设置主分支
git branch -M main

# 4. 推送到 GitHub
echo "📤 正在推送到 GitHub..."
git push -u origin main

echo "✅ 推送成功！"
echo "🔗 仓库地址: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo ""
echo "📝 后续步骤:"
echo "1. 在 OpenClaw 中启用技能: openclaw skills register ."
echo "2. 测试压缩: node scripts/compact_session.js"
