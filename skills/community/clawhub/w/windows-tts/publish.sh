#!/bin/bash

# Windows TTS ClawHub Publish Script
# 快速发布脚本

set -e

SKILL_DIR="/home/cmos/skills/windows-tts"
SKILL_NAME="windows-tts"
VERSION="1.0.0"

echo "🚀 Windows TTS - ClawHub 发布脚本"
echo "================================"
echo ""

# 检查是否已登录
echo "📝 检查登录状态..."
if ! clawhub whoami > /dev/null 2>&1; then
    echo "❌ 未登录 ClawHub"
    echo ""
    echo "请先登录："
    echo "  clawhub login"
    echo ""
    exit 1
fi

clawhub whoami
echo ""

# 进入技能目录
cd "$SKILL_DIR"

# 检查必需文件
echo "📦 检查必需文件..."
REQUIRED_FILES=("SKILL.md" "package.json" "dist/")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -e "$file" ]; then
        echo "❌ 缺少必需文件：$file"
        exit 1
    fi
    echo "  ✓ $file"
done
echo ""

# 编译检查
echo "🔨 编译检查..."
npm run build
echo ""

# 发布
echo "📤 发布到 ClawHub..."
echo ""
echo "技能信息："
echo "  名称：$SKILL_NAME"
echo "  版本：$VERSION"
echo "  路径：$SKILL_DIR"
echo ""

read -p "确认发布？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 取消发布"
    exit 1
fi

# 执行发布
cd /home/cmos/skills
clawhub publish "$SKILL_NAME" \
  --slug "$SKILL_NAME" \
  --name "Windows TTS Notification" \
  --version "$VERSION" \
  --tags "latest,tts,notification,windows,azure,broadcast,reminder" \
  --changelog "Initial release: Cross-device TTS broadcast for family reminders"

echo ""
echo "✅ 发布成功！"
echo ""
echo "🌐 技能页面："
echo "  https://clawhub.ai/skills/$SKILL_NAME"
echo ""
echo "📥 安装命令："
echo "  clawhub install $SKILL_NAME"
echo ""

