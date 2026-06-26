#!/bin/bash

# Vibe Coding 技能本地安装脚本

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="$HOME/.openclaw/workspace/skills/vibe-coding"

echo "🎨 Vibe Coding 技能本地安装"
echo ""
echo "📁 源目录：$SKILL_DIR"
echo "📁 目标目录：$TARGET_DIR"
echo ""

# 检查目标目录
if [ -d "$TARGET_DIR" ]; then
  echo "⚠️  目标目录已存在，是否覆盖？(y/n)"
  read -r response
  if [[ "$response" != "y" ]]; then
    echo "❌ 取消安装"
    exit 1
  fi
  rm -rf "$TARGET_DIR"
fi

# 复制文件
echo "📦 复制文件..."
cp -r "$SKILL_DIR" "$TARGET_DIR"

# 设置执行权限
echo "🔧 设置执行权限..."
chmod +x "$TARGET_DIR/index.js"
chmod +x "$TARGET_DIR/scripts/publish.sh"

# 验证安装
echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  vibe-coding \"做一个个税计算器\""
echo ""
echo "或者:"
echo "  cd $TARGET_DIR"
echo "  node index.js \"做一个个税计算器\""
echo ""
