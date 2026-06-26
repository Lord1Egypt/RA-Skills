#!/bin/bash

# Skill Security Scanner - 扫描所有已安装的 skill
# 用法: ./scan-all.sh [skills目录]

SKILLS_DIR="${1:-$HOME/.openclaw/workspace/skills}"
SCAN_SCRIPT="$(dirname "$0")/scan.sh"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo "════════════════════════════════════════════════════"
echo "     🔒 Skill 全盘安全扫描"
echo "════════════════════════════════════════════════════"
echo ""
echo "📁 扫描目录: $SKILLS_DIR"
echo ""

# 检查目录
if [ ! -d "$SKILLS_DIR" ]; then
    echo "${RED}错误: 目录不存在: $SKILLS_DIR${NC}"
    exit 1
fi

# 统计
TOTAL=0; PASS=0; WARN=0; FAIL=0
RESULTS=()

# 扫描每个 skill
for skill_path in "$SKILLS_DIR"/*/; do
    [ -d "$skill_path" ] || continue
    
    skill_name=$(basename "$skill_path")
    TOTAL=$((TOTAL + 1))
    
    echo "────────────────────────────────────────────────────"
    echo "🔍 扫描: $skill_name"
    echo "────────────────────────────────────────────────────"
    
    # 运行单 skill 扫描
    result=$("$SCAN_SCRIPT" "$skill_path" 2>&1)
    
    # 提取结论（判断安全等级）
    if echo "$result" | grep -q "🚫"; then
        # 有危险标记
        if echo "$result" | grep -q "建议谨慎使用\|可疑\|不推荐\|禁止"; then
            status="🚫"
            FAIL=$((FAIL + 1))
        else
            status="⚠️"
            WARN=$((WARN + 1))
        fi
    else
        status="✅"
        PASS=$((PASS + 1))
    fi
    
    # 提取评分
    # 提取评分（去除 ANSI 转义序列，然后提取数字）
    score=$(echo "$result" | sed 's/\x1b\[[0-9;]*m//g' | sed -n 's/.*评分: *\([0-9]*\)\/100.*/\1/p' | grep -v '^$' | head -1)
    
    RESULTS+=("$status|$skill_name|$score")
    
    # 有风险的 skill 输出完整报告
    if [ "$status" = "🚫" ] || [ "$status" = "⚠️" ]; then
        echo "$result"
    fi
    echo ""
done

# 汇总报告
echo "════════════════════════════════════════════════════"
echo "                    📊 扫描汇总"
echo "════════════════════════════════════════════════════"
echo ""
echo "📦 扫描总数: $TOTAL"
echo ""
printf "│ %-30s │ %-8s │\n" "Skill" "评分"
echo "├───────────────────────────────────────────┼──────────┤"

for r in "${RESULTS[@]}"; do
    IFS='|' read -r status name score <<< "$r"
    printf "│ %-30s │ %-8s │\n" "$name" "${score:-N/A}"
done

echo "└───────────────────────────────────────────┴──────────┘"
echo ""
echo "✅ 通过: $PASS"
[ $WARN -gt 0 ] && echo "⚠️  建议审查: $WARN"
[ $FAIL -gt 0 ] && echo "🚫 禁止运行: $FAIL"
echo ""

# 高风险列表
if [ $FAIL -gt 0 ] || [ $WARN -gt 0 ]; then
    echo "⚠️  需要关注的 skill:"
    PROBLEM_SKILLS=""
    for r in "${RESULTS[@]}"; do
        IFS='|' read -r status name score <<< "$r"
        if [ "$status" = "🚫" ] || [ "$status" = "⚠️" ]; then
            echo "  - $name (评分: ${score:-N/A})"
            PROBLEM_SKILLS="$PROBLEM_SKILLS $name"
        fi
    done
    echo ""
    echo "💡 提示: 运行单个扫描可获取完整报告"
    echo "   ./scripts/scan.sh ~/.openclaw/workspace/skills/<skill-name>"
    echo ""
    echo "   示例:"
    for r in "${RESULTS[@]}"; do
        IFS='|' read -r status name score <<< "$r"
        if [ "$status" = "🚫" ] || [ "$status" = "⚠️" ]; then
            echo "   • ./scripts/scan.sh ~/.openclaw/workspace/skills/$name"
        fi
    done
fi

echo ""
