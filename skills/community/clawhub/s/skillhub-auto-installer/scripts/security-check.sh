#!/bin/bash
# 安全检查脚本 - 检查已安装技能的安全性
# 用法: ./security-check.sh [skill-name]

SKILL_NAME="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 动态查找 skills 目录
find_skills_dir() {
    # 尝试多个可能的位置
    POSSIBLE_PATHS=(
        "$(dirname "$SCRIPT_DIR")"           # 当前目录的父目录
        "$(dirname "$SCRIPT_DIR")/../.."     # 再往上两级
        "${OPENCLAW_STATE_DIR:-}"            # 环境变量
        "."
        ".."
    )
    
    for path in "${POSSIBLE_PATHS[@]}"; do
        if [ -d "$path/skills" ] && [ -f "$path/openclaw.json" 2>/dev/null ]; then
            echo "$path/skills"
            return 0
        fi
    done
    
    # 如果都找不到，使用相对路径
    echo "./skills"
    return 1
}

SKILLS_DIR="$(find_skills_dir)"

echo "═══════════════════════════════════════════════════"
echo "   🔐 Skill 安全检查"
echo "═══════════════════════════════════════════════════"
echo ""
echo "📁 检测到 Skills 目录: $SKILLS_DIR"
echo ""

# 检查 SkillSentry 是否可用
SKILLSENTRY_FOUND=false
SKILLSENTRY_PATH=""

for path in "$SKILLS_DIR/skillsentry" "$SKILLS_DIR/../skillsentry" "./skillsentry"; do
    if [ -d "$path" ]; then
        SKILLSENTRY_FOUND=true
        SKILLSENTRY_PATH="$path"
        break
    fi
done

if [ "$SKILLSENTRY_FOUND" = false ]; then
    echo "❌ SkillSentry 未安装"
    echo ""
    echo "安装方式:"
    echo "  SKILLS_API_URL=https://skills.volces.com/v1 npx -y skills add \\"
    echo "      https://skills.volces.com/skills/clawhub/poolguy24 \\"
    echo "      -s skillsentry -a openclaw -y --copy"
    exit 1
fi

echo "✅ SkillSentry 已找到: $SKILLSENTRY_PATH"
echo ""

# 如果指定了 skill，对该 skill 进行检查
if [ ! -z "$SKILL_NAME" ]; then
    TARGET_SKILL_DIR="$SKILLS_DIR/$SKILL_NAME"
    
    if [ ! -d "$TARGET_SKILL_DIR" ]; then
        echo "❌ Skill '$SKILL_NAME' 不存在于 $SKILLS_DIR"
        echo ""
        echo "已安装的 Skills:"
        ls -1 "$SKILLS_DIR" 2>/dev/null || echo "   (无法列出)"
        exit 1
    fi
    
    echo "📦 检查 Skill: $SKILL_NAME"
    echo "   路径: $TARGET_SKILL_DIR"
    echo ""
    
    # 基础检查
    echo "📋 基础检查:"
    
    # 1. SKILL.md 检查
    if [ -f "$TARGET_SKILL_DIR/SKILL.md" ]; then
        echo "   ✅ SKILL.md 存在"
        
        # 检查元数据
        if head -20 "$TARGET_SKILL_DIR/SKILL.md" | grep -q "^---"; then
            echo "   ✅ Frontmatter 存在"
        fi
        
        # 检查 name 字段
        if grep -q "^name:" "$TARGET_SKILL_DIR/SKILL.md"; then
            SKILL_DECLARED_NAME=$(grep "^name:" "$TARGET_SKILL_DIR/SKILL.md" | head -1 | sed 's/name:[[:space:]]*//' | tr -d '"' | tr -d "'")
            echo "   ✅ name 字段: $SKILL_DECLARED_NAME"
        fi
    else
        echo "   ❌ SKILL.md 不存在"
        echo "   ⚠️  不符合 Skill 规范"
    fi
    
    # 2. Scripts 检查
    if [ -d "$TARGET_SKILL_DIR/scripts" ]; then
        echo ""
        echo "📁 脚本检查:"
        
        SCRIPTS=$(find "$TARGET_SKILL_DIR/scripts" -type f 2>/dev/null | wc -l)
        echo "   发现 $SCRIPTS 个文件"
        
        SHELL_SCRIPTS=$(find "$TARGET_SKILL_DIR/scripts" -name "*.sh" -type f 2>/dev/null)
        if [ ! -z "$SHELL_SCRIPTS" ]; then
            SCRIPT_COUNT=$(echo "$SHELL_SCRIPTS" | wc -l)
            echo "   其中 $SCRIPT_COUNT 个 shell 脚本"
            
            # 检查高危命令
            echo ""
            echo "🔍 安全检查:"
            
            DANGEROUS=$(grep -rE "(rm -rf /|rm -rf \*|> /etc/|chmod 777 /|curl.*\|.*sh|wget.*\|.*sh)" "$TARGET_SKILL_DIR/scripts/" 2>/dev/null | grep -v "^#" || true)
            if [ ! -z "$DANGEROUS" ]; then
                echo "   🚨 发现高危命令模式:"
                echo "$DANGEROUS" | head -5 | sed 's/^/      /'
            else
                echo "   ✅ 未发现明显高危命令"
            fi
            
            # 检查网络请求
            NETWORK=$(grep -rE "(curl|wget|fetch)" "$TARGET_SKILL_DIR/scripts/" 2>/dev/null | grep -v "^#" || true)
            if [ ! -z "$NETWORK" ]; then
                echo "   ⚠️  发现网络请求调用 (请审查):"
                echo "$NETWORK" | head -3 | sed 's/^/      /'
            fi
            
            # 检查动态执行
            DYNAMIC_EXEC=$(grep -rE "(eval\s|exec\s|system\(|child_process)" "$TARGET_SKILL_DIR/scripts/" 2>/dev/null | grep -v "^#" || true)
            if [ ! -z "$DYNAMIC_EXEC" ]; then
                echo "   ⚠️  发现动态代码执行 (请审查):"
                echo "$DYNAMIC_EXEC" | head -3 | sed 's/^/      /'
            fi
        fi
    fi
    
    echo ""
fi

# 运行 SkillSentry 完整审计
echo "🛡️ 运行 SkillSentry 完整安全审计..."
echo ""

if [ -f "$SKILLSENTRY_PATH/scripts/audit.sh" ]; then
    bash "$SKILLSENTRY_PATH/scripts/audit.sh" 2>/dev/null || {
        echo "   ⚠️  审计脚本执行遇到问题"
    }
    echo ""
    echo "📊 审计完成"
else
    echo "❌ SkillSentry 审计脚本未找到"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "   ✅ 安全检查完成"
echo "═══════════════════════════════════════════════════"
echo ""

if [ ! -z "$SKILL_NAME" ]; then
    echo "💡 如需移除该 Skill，可删除目录:"
    echo "   rm -rf $TARGET_SKILL_DIR"
    echo ""
fi
