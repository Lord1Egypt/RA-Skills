#!/usr/bin/env bash
# init-slidev.sh — 初始化 Slidev 项目并生成 PPT
# 用法: bash init-slidev.sh <slides.md路径> [项目目录]

set -e

SLIDES_FILE="${1:-slides.md}"
PROJECT_DIR="${2:-.}"

cd "$PROJECT_DIR"

# 检查是否已有 package.json
if [ ! -f "package.json" ]; then
  echo "📦 初始化项目..."
  npm init -y > /dev/null 2>&1
fi

# 检查 slidev 是否已安装
if ! npm ls @slidev/cli > /dev/null 2>&1; then
  echo "📥 安装 Slidev..."
  npm install @slidev/cli > /dev/null 2>&1
fi

echo "✅ 就绪！运行以下命令启动："
echo "   npx @slidev/cli \"$SLIDES_FILE\""
