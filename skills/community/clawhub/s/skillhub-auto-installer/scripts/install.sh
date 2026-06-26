#!/bin/bash
# Skillhub 安装脚本
# 用法: ./install.sh <skill-full-name>
# 示例: ./install.sh bytedance/agentkit-samples@web-search

SKILL_FULL="$1"

if [ -z "$SKILL_FULL" ]; then
    echo "❌ 错误: 请提供完整的 skill 名称"
    echo "格式: owner/repo@skill-name"
    echo "用法: $0 <owner/repo@skill-name>"
    exit 1
fi

# 解析 skill 名称
# 格式: owner/repo@skill-name
if [[ ! "$SKILL_FULL" =~ ^([^/]+)/([^@]+)@(.+)$ ]]; then
    echo "❌ 错误: Skill 名称格式不正确"
    echo "正确格式: owner/repo@skill-name"
    echo "示例: bytedance/agentkit-samples@web-search"
    exit 1
fi

OWNER="${BASH_REMATCH[1]}"
REPO="${BASH_REMATCH[2]}"
SKILL_NAME="${BASH_REMATCH[3]}"

echo "📦 正在安装 Skill: $SKILL_NAME"
echo "   来源: $OWNER/$REPO"
echo ""

# 构建 URL
URL="https://skills.volces.com/skills/$OWNER/$REPO"

echo "🔗 URL: $URL"
echo ""

# 执行安装
cd /home/gem/workspace/agent
SKILLS_API_URL=https://skills.volces.com/v1 npx -y skills add "$URL" -s "$SKILL_NAME" -a openclaw -y --copy

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Skill '$SKILL_NAME' 安装成功！"
    echo ""
    echo "📍 安装位置: skills/$SKILL_NAME/"
    echo "📝 使用方式: 查看 skills/$SKILL_NAME/SKILL.md 了解具体功能"
else
    echo ""
    echo "❌ Skill 安装失败，错误码: $EXIT_CODE"
    exit 1
fi
