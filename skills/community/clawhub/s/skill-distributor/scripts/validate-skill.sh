#!/bin/bash
# validate-skill.sh - Pre-publish validation for skill-distributor
# Usage: ./scripts/validate-skill.sh <skill-directory> [platform]
# Example: ./scripts/validate-skill.sh ./ai-usage-collector clawhub

set -e

SKILL_DIR="${1:-.}"
PLATFORM="${2:-all}"
SKILL_MD="${SKILL_DIR}/SKILL.md"

echo "🔍 技能发布前校验"
echo "目录: ${SKILL_DIR}"
echo "平台: ${PLATFORM}"
echo "---"

# 1. 检查 SKILL.md 是否存在
if [ ! -f "$SKILL_MD" ]; then
    echo "❌ 错误: ${SKILL_MD} 不存在"
    exit 1
fi
echo "✅ SKILL.md 存在"

# 2. 提取 frontmatter 字段（兼容 bash 3.x）
get_field() {
    local key="$1"
    local file="$2"
    # 提取 key: value 格式的字段，去除引号
    grep -E "^${key}:" "$file" 2>/dev/null | sed "s/^${key}:[[:space:]]*//" | sed 's/^"//;s/"$//' | head -1
}

NAME=$(get_field "name" "$SKILL_MD")
DESC=$(get_field "description" "$SKILL_MD")
VERSION=$(get_field "version" "$SKILL_MD")
AUTHOR=$(get_field "author" "$SKILL_MD")
ALLOWED_TOOLS=$(get_field "allowed-tools" "$SKILL_MD")

ERRORS=0

# 3. 校验必填字段
echo ""
echo "📋 校验必填字段..."

if [ -z "$NAME" ]; then
    echo "❌ 缺失必填字段: name"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ name: $NAME"
fi

if [ -z "$DESC" ]; then
    echo "❌ 缺失必填字段: description"
    ERRORS=$((ERRORS + 1))
else
    # 显示前50字符
    SHORT_DESC=$(echo "$DESC" | cut -c1-50)
    echo "✅ description: ${SHORT_DESC}..."
fi

if [ -z "$VERSION" ]; then
    echo "⚠️  缺失字段: version（将使用默认值 1.0.0）"
else
    # 检查 version 是否为合法 semver
    if echo "$VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
        echo "✅ version: $VERSION"
    else
        echo "⚠️  version 格式可能不正确: $VERSION（应为 semver 如 1.0.0）"
    fi
fi

if [ -z "$AUTHOR" ]; then
    echo "⚠️  缺失字段: author（可选但建议填写）"
else
    echo "✅ author: $AUTHOR"
fi

# 4. 平台特定校验
if [ "$PLATFORM" = "clawhub" ] || [ "$PLATFORM" = "all" ]; then
    echo ""
    echo "🚀 ClawHub 平台校验..."
    
    # 检查 allowed-tools 字段（ClawHub 不支持）
    if [ -n "$ALLOWED_TOOLS" ]; then
        echo "❌ ClawHub 不支持 allowed-tools 字段，请移除"
        ERRORS=$((ERRORS + 1))
    else
        echo "✅ 无 ClawHub 不支持的字段"
    fi
    
    # 检查 clawhub CLI
    if command -v npx >/dev/null 2>&1; then
        echo "✅ npx 可用（clawhub CLI）"
    else
        echo "⚠️  npx 不可用，请安装 Node.js"
    fi
    
    # 检查登录状态
    if npx clawhub whoami >/dev/null 2>&1; then
        echo "✅ ClawHub 已登录"
    else
        echo "⚠️  ClawHub 未登录，请运行: clawhub login"
    fi
fi

if [ "$PLATFORM" = "workbuddy" ] || [ "$PLATFORM" = "all" ]; then
    echo ""
    echo "🤖 WorkBuddy 平台校验..."
    
    if [ -n "$ALLOWED_TOOLS" ]; then
        echo "✅ allowed-tools: $ALLOWED_TOOLS"
    else
        echo "ℹ️  未设置 allowed-tools（可选）"
    fi
fi

# 5. 总结
echo ""
echo "---"
if [ $ERRORS -eq 0 ]; then
    echo "✅ 校验通过！可以发布到 ${PLATFORM}"
    exit 0
else
    echo "❌ 发现 ${ERRORS} 个错误，请修正后再发布"
    exit 1
fi
