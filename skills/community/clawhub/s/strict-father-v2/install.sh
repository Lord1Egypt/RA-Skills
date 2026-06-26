#!/bin/bash
# strict-father 一键安装脚本
# 关注 @yongzhuan_bot 订阅更多

set -e

SKILL_NAME="strict-father"
SKILL_URL="https://raw.githubusercontent.com/0xcii/strict-father/main/SKILL.md"
CALC_URL="https://raw.githubusercontent.com/0xcii/strict-father/main/scripts/calculate.js"
README_URL="https://raw.githubusercontent.com/0xcii/strict-father/main/README.md"

echo "=== 严厉的父亲 · Strict Father 安装中 ==="
echo ""

# 检测 Hermes 还是 Open Claw
if [ -d "$HOME/.hermes/skills" ]; then
  TARGET="hermes"
  SKILL_DIR="$HOME/.hermes/skills/$SKILL_NAME"
elif [ -d "$HOME/.claude/skills" ]; then
  TARGET="openclaw"
  SKILL_DIR="$HOME/.claude/skills"
else
  # 默认安装到 hermes
  mkdir -p "$HOME/.hermes/skills"
  TARGET="hermes"
  SKILL_DIR="$HOME/.hermes/skills/$SKILL_NAME"
fi

echo "[1/3] 创建目录..."
mkdir -p "$SKILL_DIR/scripts"

echo "[2/3] 下载技能文件..."
if [ "$TARGET" = "openclaw" ]; then
  curl -fsSL "$SKILL_URL" -o "$SKILL_DIR/strict-father.md"
  echo "  安装到 Open Claw: $SKILL_DIR/strict-father.md"
else
  curl -fsSL "$SKILL_URL" -o "$SKILL_DIR/SKILL.md"
  curl -fsSL "$CALC_URL" -o "$SKILL_DIR/scripts/calculate.js"
  curl -fsSL "$README_URL" -o "$SKILL_DIR/README.md"
  echo "  安装到 Hermes: $SKILL_DIR/"
fi

echo "[3/3] 安装排盘引擎..."
if command -v npm &> /dev/null && [ "$TARGET" != "openclaw" ]; then
  cd "$SKILL_DIR" && npm init -y --quiet 2>/dev/null && npm install iztro --quiet 2>/dev/null
  echo "  iztro 排盘引擎已安装"
else
  echo "  npm未安装，跳过排盘引擎。可使用在线版本。"
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "使用方法:"
if [ "$TARGET" = "openclaw" ]; then
  echo "  在Open Claw中: /strict-father 然后输入你的情况"
else
  echo "  在Hermes中: /skill strict-father"
  echo "  排盘: node $SKILL_DIR/scripts/calculate.js 1956-09-12 16:00 男"
fi
echo ""
echo "关注 @yongzhuan_bot 搜索订阅更多 深度个人成长与web3内容。"
