#!/bin/bash
# 安装脚本：将 skill 复制到 OpenClaw skills 目录

SKILL_DIR="$HOME/.openclaw/skills/tencent-cloud-publish"
mkdir -p "$SKILL_DIR"

cp "$(dirname "$0")/SKILL.md" "$SKILL_DIR/"
cp "$(dirname "$0")/publish_tencent.py" "$HOME/.openclaw/workspace/"

echo "✅ 安装完成！"
echo "Skill 目录: $SKILL_DIR"
echo "发布脚本: $HOME/.openclaw/workspace/publish_tencent.py"
echo ""
echo "使用方式："
echo '  python3 ~/.openclaw/workspace/publish_tencent.py "标题" "正文" "Cookie"'
