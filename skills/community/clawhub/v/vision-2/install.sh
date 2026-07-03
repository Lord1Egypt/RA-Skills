#!/bin/bash
# Vision 一键安装脚本

set -e

SKILL_DIR="$HOME/.claude/skills/vision"
SCRIPTS_DIR="$SKILL_DIR/scripts"

echo "=== 安装 Vision Skill ==="

# 创建目录
mkdir -p "$SCRIPTS_DIR"

# 检查参数
if [ -n "$1" ]; then
  # 从 GitHub 安装
  echo "从 GitHub 下载..."
  curl -fsSL "$1/SKILL.md" -o "$SKILL_DIR/SKILL.md"
  curl -fsSL "$1/scripts/vision.js" -o "$SCRIPTS_DIR/vision.js"
  curl -fsSL "$1/config.json" -o "$SKILL_DIR/config.json" 2>/dev/null || true
else
  # 本地安装
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  if [ -f "$SCRIPT_DIR/SKILL.md" ] && [ -f "$SCRIPT_DIR/scripts/vision.js" ]; then
    echo "从本地复制..."
    cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/"
    cp "$SCRIPT_DIR/scripts/vision.js" "$SCRIPTS_DIR/"
    cp "$SCRIPT_DIR/config.json" "$SKILL_DIR/" 2>/dev/null || true
  else
    echo "错误：请提供 GitHub URL 或在 skill 目录下运行此脚本"
    echo "用法：curl -fsSL https://.../install.sh | bash"
    exit 1
  fi
fi

# 设置执行权限
chmod +x "$SCRIPTS_DIR/vision.js"

echo ""
echo "✅ 安装完成！"
echo ""
echo "下一步：配置图片识别服务"
echo "  node $SCRIPTS_DIR/vision.js --setup"
echo ""
