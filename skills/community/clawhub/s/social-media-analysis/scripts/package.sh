#!/bin/bash
#
# Skill 打包脚本
# 将 social-media-analysis skill 打包为 zip 文件，方便分享
#

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${1:-.}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="social-media-analysis-skill-${TIMESTAMP}.zip"

echo "📦 打包 Skill: $SKILL_DIR"
echo "输出目录：$OUTPUT_DIR"
echo "文件名：$PACKAGE_NAME"
echo ""

# 进入 skill 目录
cd "$SKILL_DIR"

# 创建 zip 包（排除不必要的文件）
zip -r "$OUTPUT_DIR/$PACKAGE_NAME" \
  SKILL.md \
  scripts/ \
  -x "*.DS_Store" \
  -x "*.pyc" \
  -x "__pycache__/*" \
  -x ".git/*"

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ 打包完成！"
  echo "文件：$OUTPUT_DIR/$PACKAGE_NAME"
  echo ""
  echo "📋 包含内容："
  unzip -l "$OUTPUT_DIR/$PACKAGE_NAME" | tail -20
else
  echo "❌ 打包失败"
  exit 1
fi
