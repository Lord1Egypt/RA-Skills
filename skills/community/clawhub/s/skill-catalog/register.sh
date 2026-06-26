#!/bin/bash
# Skill Registry - 自动扫描所有 SKILL.md 并生成 INDEX.md
# 用法: bash register.sh
# 输出: skills/INDEX.md

SKILLS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INDEX_FILE="$SKILLS_DIR/INDEX.md"
WORKSPACE_DIR="$(cd "$SKILLS_DIR/.." && pwd)"

echo "🔍 扫描 skills 目录..."
echo "   目录: $SKILLS_DIR"
echo "   输出: $INDEX_FILE"
echo ""

# 临时文件
TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

# 收集所有 SKILL.md 信息
declare -A skills
while IFS= read -r -d '' sk_file; do
    rel_path=$(realpath --relative-to="$SKILLS_DIR" "$sk_file")
    name=$(grep -oP 'name:\s*\K.*' "$sk_file" 2>/dev/null | head -1 | sed 's/^["'\'']//;s/["'\'']$//' | xargs)
    desc=$(grep -oP 'description:\s*"\K[^"]*' "$sk_file" 2>/dev/null | head -1)
    [ -z "$name" ] && name=$(basename "$(dirname "$sk_file")")
    [ -z "$desc" ] && desc=$(grep -oP 'description:\s*\K.*' "$sk_file" 2>/dev/null | head -1 | sed 's/^"//;s/"$//' | cut -c1-80)
    
    if [ -n "$name" ]; then
        echo "$rel_path|$name|$desc" >> "$TMPFILE"
    fi
done < <(find "$SKILLS_DIR" -name "SKILL.md" -type f -not -path "*/skill-index/*" -print0 | sort -z)

# 统计
TOTAL=$(wc -l < "$TMPFILE")
echo "   找到 $TOTAL 个 skill"
echo ""

# 分类逻辑（路径 + 描述 双重匹配）
categorize() {
    local path="$1"
    local desc="$2"
    local combined="$path $desc"
    
    # 1. 按目录结构优先
    case "$path" in
        scm-skill/*) echo "SCM 采购体系"; return ;;
        skynet-monitor/ai/*) echo "天网-AI 监控"; return ;;
        skynet-monitor/procurement/*) echo "天网-供应链监控"; return ;;
        skynet-monitor/weekly/*) echo "天网-周报"; return ;;
        skynet-monitor/common/*) echo "天网-通用"; return ;;
        skynet-monitor/*) echo "天网-其他"; return ;;
    esac
    
    # 2. 按描述关键词匹配
    case "$combined" in
        *内容创作*|*baoyu-*|*article*|*illustrator*|*comic*|*infographic*|*slide*|*xhs*|*cover*|*format-markdown*) echo "内容创作"; return ;;
        *视频*|*video*|*avatar*|*lipsync*|*talking*|*remotion*|*veo*|*seedance*) echo "媒体生成"; return ;;
        *图片*|*image*|*photo*|*compress*) echo "媒体生成"; return ;;
        *采购*|*supplier*|*寻源*|*p2p*|*替代料*|*降本*|*成本*|*质量*|*1688*|*sourcing*) echo "SCM 采购体系"; return ;;
        *github*|*coding-agent*|*browser*|*playwright*|*mcp*|*smart-explore*|*web-artifacts*|*web-design*) echo "开发工具"; return ;;
        *claude*|*claude-*) echo "Claude 生态"; return ;;
        *memory*|*mem-*|*diary*|*todo*|*shopping*|*daily*) echo "效率工具"; return ;;
        *搜索*|*search*|*extract*|*crawl*|*research*|*target*|*summarize*|*tavily*|*研究*) echo "研究搜索"; return ;;
        *飞书*|*feishu*|*公众号*|*wechat*|*微信*|*发布*) echo "内容发布"; return ;;
        *监控*|*monitor*|*weather*|*healthcheck*|*updater*|*cron*) echo "系统运维"; return ;;
        *英语*|*english*|*humanizer*|*scene-english*) echo "语言工具"; return ;;
        *AI*monitor*|*giants*|*资本*|*政策*|*人才*|*社会*|*Karpathy*|*博客*|*digest*) echo "行业监控"; return ;;
        *plan*|*do*|*make-plan*) echo "项目管理"; return ;;
        *agent*|*council*|*proactive*|*self-improving*) echo "AI Agent"; return ;;
        *专家*|*expert*) echo "专家系统"; return ;;
        *chip*|*半导体*|*半导*) echo "供应链"; return ;;
        *d3*|*visualization*) echo "可视化"; return ;;
        *skill*|*registry*|*index*|*vetter*|*creator*|*usage*) echo "Skill 管理"; return ;;
    esac
    
    # 3. 兜底
    echo "其他"
}

# 生成 INDEX.md
{
    echo "# Skills Index"
    echo ""
    echo "> 自动生成，勿手动编辑。运行 \`bash skills/skill-index/register.sh\` 更新。"
    echo "> 生成时间: $(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "> Skill 总数: $TOTAL"
    echo ""
    
    # 按分类分组
    current_cat=""
    while IFS='|' read -r path name desc; do
        cat=$(categorize "$path" "$desc")
        if [ "$cat" != "$current_cat" ]; then
            echo "## $cat"
            echo ""
            echo "| Skill | 路径 | 触发场景 |"
            echo "|-------|------|----------|"
            current_cat="$cat"
        fi
        # 截断描述
        short_desc=$(echo "$desc" | cut -c1-60)
        echo "| $name | $path | $short_desc |"
    done < "$TMPFILE"
    
    echo ""
    echo "---"
    echo ""
    echo "## 索引使用说明"
    echo ""
    echo "1. AI 启动时读取此文件，获得所有可用 skill 的路径和触发场景"
    echo "2. 路径为相对于 \`skills/\` 的路径，完整路径需拼上 \`\$WORKSPACE/skills/\`"
    echo "3. 新增/删除 skill 后，运行 \`bash skills/skill-index/register.sh\` 更新"
    echo "4. Git hooks 会在 commit/pull 时自动触发更新"
} > "$INDEX_FILE"

echo "✅ 索引已生成: $INDEX_FILE"
echo "   包含 $TOTAL 个 skill，按分类整理"
