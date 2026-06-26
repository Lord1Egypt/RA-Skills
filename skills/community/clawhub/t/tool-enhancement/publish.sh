#!/bin/bash
# 发布脚本：一键推送到 GitHub 和 ClawHub

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "📦 开始发布..."

# 读取当前版本（从 SKILL.md 的 metadata 中）
CURRENT=$(grep -A1 '"version":' SKILL.md | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
if [ -z "$CURRENT" ]; then
    CURRENT="1.0.0"
fi

echo "  当前版本: $CURRENT"

# 递增版本号
MAJOR=$(echo $CURRENT | cut -d. -f1)
MINOR=$(echo $CURRENT | cut -d. -f2)
PATCH=$(echo $CURRENT | cut -d. -f3)
NEW_VERSION="${MAJOR}.${MINOR}.$((PATCH + 1))"

echo "  新版本: $NEW_VERSION"

# Git 提交并推送
echo "  📤 推送到 GitHub..."
git add -A
git commit -m "release: v$NEW_VERSION" 2>/dev/null || echo "  (无新变更)"
git push

# ClawHub 发布 (必须用完整路径 + DEBUG=*)
echo "  ☁️  发布到 ClawHub..."
DEBUG=* clawhub publish "$SCRIPT_DIR" \
    --slug tool-enhancement \
    --name "Tool Enhancement" \
    --version "$NEW_VERSION" \
    --changelog "版本更新" 2>&1 | tail -3

echo ""
echo "✅ 发布完成!"
echo "  GitHub: https://github.com/ntaffffff/openclaw-tool-enhancement"
echo "  ClawHub: https://clawhub.ai/skill/tool-enhancement"
echo "  版本: v$NEW_VERSION"