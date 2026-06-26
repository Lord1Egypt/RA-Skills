#!/bin/bash

# Vibe Coding 技能发布脚本

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

echo "🎨 Vibe Coding 技能发布"
echo ""
echo "📁 目录：$SKILL_DIR"
echo ""

# 检查必要文件
echo "📋 检查必要文件..."
REQUIRED_FILES=("SKILL.md" "README.md" "index.js" "package.json" "clawhub.json")
for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ 缺少必要文件：$file"
    exit 1
  fi
  echo "  ✅ $file"
done
echo ""

# 检查目录结构
echo "📁 检查目录结构..."
REQUIRED_DIRS=("executors" "templates" "utils" "examples")
for dir in "${REQUIRED_DIRS[@]}"; do
  if [ ! -d "$dir" ]; then
    echo "❌ 缺少必要目录：$dir"
    exit 1
  fi
  echo "  ✅ $dir"
done
echo ""

# 版本号
VERSION=$(grep '"version"' clawhub.json | cut -d'"' -f4)
echo "📦 版本：v$VERSION"
echo ""

# 发布到 ClawHub
echo "🚀 发布到 ClawHub..."
echo ""
echo "请运行以下命令发布技能："
echo ""
echo "  cd $SKILL_DIR"
echo "  clawhub publish"
echo ""
echo "或者手动复制到技能目录："
echo ""
echo "  cp -r $SKILL_DIR ~/.openclaw/workspace/skills/vibe-coding"
echo ""

echo "✅ 发布准备完成！"
