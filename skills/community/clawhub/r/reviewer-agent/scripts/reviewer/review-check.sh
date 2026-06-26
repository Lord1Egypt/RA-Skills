#!/bin/bash
# review-check.sh - 评审Agent专用检查脚本
# 在评审开始前，快速检查项目状态

WORKSPACE="/root/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills"
REVIEW_DIR="$WORKSPACE/.reviewer"
REVIEW_LOG="$REVIEW_DIR/reviews/$(date +%Y-%m-%d).md"
mkdir -p "$(dirname "$REVIEW_LOG")"

# 检查指定skill的状态
check_skill() {
    local skill_name=$1
    local skill_dir="$SKILL_DIR/$skill_name"
    
    echo "### $skill_name"
    
    if [ ! -d "$skill_dir" ]; then
        echo "- ❌ 目录不存在"
        return
    fi
    
    # SKILL.md版本
    local version="未知"
    if grep -q "^version:" "$skill_dir/SKILL.md" 2>/dev/null; then
        version=$(grep "^version:" "$skill_dir/SKILL.md" | head -1 | cut -d':' -f2 | tr -d ' ')
    fi
    echo "- 版本：$version"
    
    # 更新时间
    if [ -f "$skill_dir/SKILL.md" ]; then
        local mtime=$(stat -c %y "$skill_dir/SKILL.md" 2>/dev/null | cut -d' ' -f1)
        echo "- SKILL.md更新：$mtime"
    fi
    
    # check.sh存在
    local check_sh=$(find "$skill_dir/scripts" -name "*check.sh" 2>/dev/null | wc -l)
    if [ $check_sh -gt 0 ]; then
        echo "- ✅ check.sh存在"
    else
        echo "- ❌ 缺少check.sh"
    fi
    
    # 语法检查
    for sh in $(find "$skill_dir/scripts" -name "*.sh" 2>/dev/null); do
        bash -n "$sh" 2>&1 && echo "  ✅ $sh 语法OK" || echo "  ❌ $sh 语法错误"
    done
    
    echo ""
}

# 主函数
main() {
    local project=${1:-all}
    
    echo "# 评审检查报告 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "项目：$project"
    echo ""
    
    if [ "$project" = "all" ]; then
        for skill in "$SKILL_DIR"/apollo-*; do
            local name=$(basename "$skill")
            check_skill "$name"
        done
    else
        check_skill "$project"
    fi
}

main "$@"
