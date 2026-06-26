#!/bin/bash
# 安装前安全检查脚本 - 仅检查，不安装
# 用法: ./pre-install-check.sh <owner/repo@skill-name>

set -e

SKILL_FULL="$1"

# 检查依赖
check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ 错误: 未找到 $1"
        exit 1
    fi
}

echo "═══════════════════════════════════════════════════"
echo "   🔐 安装前安全检查"
echo "═══════════════════════════════════════════════════"
echo ""

# 1. 检查参数
if [ -z "$SKILL_FULL" ]; then
    echo "❌ 错误: 请提供完整的 skill 名称"
    echo "格式: owner/repo@skill-name"
    echo "用法: $0 <owner/repo@skill-name>"
    exit 1
fi

# 解析 skill 名称
if [[ ! "$SKILL_FULL" =~ ^([^/]+)/([^@]+)@(.+)$ ]]; then
    echo "❌ 错误: Skill 名称格式不正确"
    echo "正确格式: owner/repo@skill-name"
    echo "示例: bytedance/agentkit-samples@web-search"
    exit 1
fi

OWNER="${BASH_REMATCH[1]}"
REPO="${BASH_REMATCH[2]}"
SKILL_NAME="${BASH_REMATCH[3]}"

echo "📦 目标 Skill: $SKILL_NAME"
echo "   来源: $OWNER/$REPO"
echo ""

# 2. 检查运行环境
echo "🔍 检查运行环境..."
check_dependency node
check_dependency npx
echo "   ✅ Node.js 和 npx 已安装"

# 检查网络
if ! ping -c 1 skills.volces.com &>/dev/null 2>&1; then
    echo "   ⚠️  无法连接到 skills.volces.com，请检查网络"
else
    echo "   ✅ 网络连接正常"
fi
echo ""

# 3. 强制检查 SkillSentry
echo "🛡️  检查安全审计工具 (SkillSentry)..."
SKILLSENTRY_INSTALLED=false

# 尝试多个可能的位置查找 skillsentry
POSSIBLE_PATHS=(
    "./skills/skillsentry"
    "../skillsentry"
    "../../skillsentry"
    "./.agents/skills/skillsentry"
)

for path in "${POSSIBLE_PATHS[@]}"; do
    if [ -d "$path" ]; then
        SKILLSENTRY_PATH="$path"
        SKILLSENTRY_INSTALLED=true
        break
    fi
done

if [ "$SKILLSENTRY_INSTALLED" = false ]; then
    echo ""
    echo "❌ SkillSentry 未安装！"
    echo ""
    echo "⚠️  安全警告：SkillSentry 是强制依赖"
    echo ""
    echo "请按以下步骤操作："
    echo ""
    echo "1️⃣  安装 SkillSentry："
    echo "   SKILLS_API_URL=https://skills.volces.com/v1 npx -y skills add https://skills.volces.com/skills/clawhub/poolguy24 -s skillsentry -a openclaw -y --copy"
    echo ""
    echo "2️⃣  运行安全审计："
    echo "   bash skills/skillsentry/scripts/audit.sh"
    echo ""
    echo "3️⃣  确认安全后再继续安装目标 Skill"
    echo ""
    exit 1
fi

echo "   ✅ SkillSentry 已找到: $SKILLSENTRY_PATH"
echo ""

# 4. 运行安全审计
echo "🔒 正在运行安全审计..."
echo ""

if [ -f "$SKILLSENTRY_PATH/scripts/audit.sh" ]; then
    bash "$SKILLSENTRY_PATH/scripts/audit.sh" 2>/dev/null || true
    echo ""
    echo "✅ 安全审计完成"
else
    echo "   ⚠️  SkillSentry 审计脚本未找到"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "   📋 安装前检查完成"
echo "═══════════════════════════════════════════════════"
echo ""
echo "📝 手动安装命令："
echo ""
echo "   SKILLS_API_URL=https://skills.volces.com/v1 npx -y skills add \\"
echo "       https://skills.volces.com/skills/$OWNER/$REPO \\"
echo "       -s $SKILL_NAME -a openclaw -y --copy"
echo ""
echo "⚠️  安全提示："
echo "   • 此命令将从远程下载并执行代码"
echo "   • 请确保您信任来源: $OWNER/$REPO"
echo "   • 建议先查看该技能的 SKILL.md 了解其功能"
echo "   • 安装后请再次运行 SkillSentry 审计"
echo ""
echo "❓ 是否继续安装?"
echo "   请复制上述命令手动执行，或仔细阅读 SKILL.md 后再决定"
echo ""

exit 0
