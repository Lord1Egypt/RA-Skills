#!/bin/bash
# 安全安装脚本 - 集成 SkillSentry 扫描
# 用法: ./secure-install.sh <skill-full-name>
# 示例: ./secure-install.sh bytedance/agentkit-samples@web-search

set -e

SKILL_FULL="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="/home/gem/workspace/agent/skills"

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

echo "═══════════════════════════════════════════════════"
echo "   🔐 Skillhub 安全安装器"
echo "═══════════════════════════════════════════════════"
echo ""
echo "📦 准备安装: $SKILL_NAME"
echo "   来源: $OWNER/$REPO"
echo ""

# 步骤 1: 安装前安全扫描 (SkillSentry)
echo "🛡️  步骤 1/3: 执行安装前安全扫描..."
echo ""

# 检查 SkillSentry 是否安装
if [ ! -d "$SKILLS_DIR/skillsentry" ]; then
    echo "⚠️  SkillSentry 未安装，跳过安全预扫描"
    echo "   建议先安装: npx skills add ... skillsentry"
    echo ""
else
    # 检查已安装 skills 的安全状态
    echo "   扫描当前环境安全状态..."
    if [ -f "$SKILLS_DIR/skillsentry/scripts/audit.sh" ]; then
        bash "$SKILLS_DIR/skillsentry/scripts/audit.sh" > /tmp/pre-install-audit.json 2>/dev/null || true
        if [ -f /tmp/pre-install-audit.json ]; then
            RISK_COUNT=$(cat /tmp/pre-install-audit.json | grep -o '"risk"' | wc -l || echo "0")
            if [ "$RISK_COUNT" -gt 0 ]; then
                echo "   ⚠️  发现 $RISK_COUNT 个潜在风险，建议检查"
            else
                echo "   ✅ 当前环境安全状态良好"
            fi
        fi
    fi
    echo ""
fi

# 步骤 2: 安装 Skill
echo "⚡ 步骤 2/3: 安装 Skill..."
echo ""

URL="https://skills.volces.com/skills/$OWNER/$REPO"

cd /home/gem/workspace/agent
SKILLS_API_URL=https://skills.volces.com/v1 npx -y skills add "$URL" -s "$SKILL_NAME" -a openclaw -y --copy

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Skill 安装失败"
    exit 1
fi

echo ""
echo "✅ Skill '$SKILL_NAME' 安装成功"
echo ""

# 步骤 3: 安装后安全审计
echo "🛡️  步骤 3/3: 执行安装后安全审计..."
echo ""

if [ -d "$SKILLS_DIR/skillsentry" ] && [ -f "$SKILLS_DIR/skillsentry/scripts/audit.sh" ]; then
    # 对新安装的 skill 进行专门检查
    echo "   检查新安装 Skill 的安全配置..."
    
    # 检查 SKILL.md 是否存在
    if [ -f "$SKILLS_DIR/$SKILL_NAME/SKILL.md" ]; then
        echo "   ✅ SKILL.md 存在"
        
        # 简单检查常见的安全风险模式
        if grep -q "eval\|exec\|system\|child_process" "$SKILLS_DIR/$SKILL_NAME/SKILL.md" 2>/dev/null; then
            echo "   ⚠️  SKILL.md 中包含潜在代码执行相关描述，请审查"
        fi
        
        # 检查 scripts 目录
        if [ -d "$SKILLS_DIR/$SKILL_NAME/scripts" ]; then
            SCRIPT_COUNT=$(find "$SKILLS_DIR/$SKILL_NAME/scripts" -type f | wc -l)
            echo "   📁 发现 $SCRIPT_COUNT 个脚本文件"
            
            # 检查脚本中是否有可疑命令
            SUSPICIOUS=$(grep -r "rm -rf /\|curl.*|.*sh\|wget.*|.*sh\|bash -c.*\$(curl" "$SKILLS_DIR/$SKILL_NAME/scripts/" 2>/dev/null || true)
            if [ ! -z "$SUSPICIOUS" ]; then
                echo "   🚨 警告: 发现可疑命令模式，请人工审查!"
                echo "$SUSPICIOUS" | head -3
            else
                echo "   ✅ 未发现明显可疑命令"
            fi
        fi
    else
        echo "   ⚠️  SKILL.md 不存在，这可能不符合 Skill 规范"
    fi
    
    echo ""
    echo "📊 运行完整安全审计..."
    bash "$SKILLS_DIR/skillsentry/scripts/audit.sh" > "$SKILLS_DIR/$SKILL_NAME/.security-report.json" 2>/dev/null || true
    
    if [ -f "$SKILLS_DIR/$SKILL_NAME/.security-report.json" ]; then
        echo "   ✅ 安全报告已保存至: skills/$SKILL_NAME/.security-report.json"
    fi
else
    echo "   ℹ️ SkillSentry 未安装，跳过详细安全审计"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "   ✅ 安全安装流程完成!"
echo "═══════════════════════════════════════════════════"
echo ""
echo "📍 Skill 位置: skills/$SKILL_NAME/"
echo "📖 使用说明: 查看 skills/$SKILL_NAME/SKILL.md"
echo ""
echo "💡 提示:"
echo "   - 可以使用 SkillSentry 进行定期安全审计"
echo "   - 安全报告位于 .security-report.json"
echo ""
