#!/bin/bash
# Requirement Checker 发布脚本 v1.0
# 用法：./scripts/publish.sh [版本号] [changelog]
# 自动更新所有文件的版本号，然后发布到 ClawHub
#
# 示例：
#   ./scripts/publish.sh                    # 使用 SKILL.md 中的版本发布
#   ./scripts/publish.sh 2.6.0 "文档优化"   # 指定版本发布

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 查找 clawhub 命令
if command -v clawhub &> /dev/null; then
    CLAWHUB_CMD="clawhub"
elif [ -f "$HOME/.nvm/versions/node/v22.22.0/bin/clawhub" ]; then
    CLAWHUB_CMD="$HOME/.nvm/versions/node/v22.22.0/bin/clawhub"
else
    echo "❌ clawhub 命令未找到"
    echo "💡 请确保已安装 clawhub"
    exit 1
fi

# 从 SKILL.md 读取当前版本
CURRENT_VERSION=$(grep "^version:" "$PROJECT_DIR/SKILL.md" | head -1 | sed "s/version: *\([0-9.]*\).*/\1/")

VERSION="${1:-$CURRENT_VERSION}"
CHANGELOG="${2:-基于 Claude Code 技巧优化文档结构}"

echo "════════════════════════════════════════════════════════"
echo "  Requirement Checker 发布脚本 v1.0"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📦 版本：${VERSION}"
echo "📝 Changelog: ${CHANGELOG}"
echo "📁 目录：${PROJECT_DIR}"
echo ""

# 确认发布
read -p "继续发布？(y/n) " -n 1 -re
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消"
    exit 1
fi

echo ""

# 更新版本号
echo "🔧 更新版本号和版本历史..."
if [ "$VERSION" != "$CURRENT_VERSION" ]; then
    python3 "${SCRIPT_DIR}/update_version.py" "${VERSION}" "${CHANGELOG}"
else
    echo "   版本号已是最新：${VERSION}"
fi

echo ""

# 验证技能文件
echo "🔍 验证技能文件..."
if [ ! -f "$PROJECT_DIR/SKILL.md" ]; then
    echo "❌ SKILL.md 不存在"
    exit 1
fi
if [ ! -f "$PROJECT_DIR/README.md" ]; then
    echo "❌ README.md 不存在"
    exit 1
fi
echo "   ✅ 技能文件验证通过"

echo ""

# 发布
echo "📦 发布到 ClawHub..."
cd "${PROJECT_DIR}"
$CLAWHUB_CMD publish . --version "${VERSION}" --changelog "v${VERSION}: ${CHANGELOG}" 2>&1

# 等待服务器处理
echo ""
echo "⏳ 等待服务器处理..."
sleep 3

# 验证远程状态
echo "🔍 验证发布状态..."
RESULT=$($CLAWHUB_CMD inspect requirement-checker --json 2>/dev/null | grep -o '"latest": "[^"]*"')

if echo "$RESULT" | grep -q "${VERSION}"; then
    echo ""
    echo "════════════════════════════════════════════════════════"
    echo "  ✅ 发布成功！"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo "   版本：${VERSION}"
    echo "   验证：$RESULT"
    echo ""
    echo "🔗 安装命令：clawhub install requirement-checker"
    echo ""
else
    echo ""
    echo "⚠️ 无法确认发布状态"
    echo "   期望版本：${VERSION}"
    echo "   远程状态：$RESULT"
    echo ""
    echo "💡 建议：稍后手动验证"
    echo "   $CLAWHUB_CMD inspect requirement-checker --json | grep latest"
    echo ""
fi

echo "════════════════════════════════════════════════════════"
echo "  发布完成"
echo "════════════════════════════════════════════════════════"
