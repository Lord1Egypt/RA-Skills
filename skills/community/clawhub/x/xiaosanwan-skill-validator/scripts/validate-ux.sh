#!/bin/bash
# UX 用户体验验证脚本
# 用法: validate-ux.sh <skill-name>

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SKILL_NAME=$1
SKILL_DIR="/root/.openclaw/workspace/skills"

if [ -z "$SKILL_NAME" ]; then
    echo "用法: $0 <skill-name>"
    exit 1
fi

SKILL_PATH="$SKILL_DIR/$SKILL_NAME"

if [ ! -d "$SKILL_PATH" ]; then
    echo -e "${RED}✗ Skill 不存在: $SKILL_NAME${NC}"
    exit 1
fi

# 分数统计
declare -A SCORES
declare -A SUGGESTIONS

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║           🎨 UX 用户体验验证: $SKILL_NAME${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📅 验证时间: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ========== 可视化验证 ==========
echo ""
echo -e "${YELLOW}🎨 可视化验证${NC}"
echo "---"

visual_score=0
visual_checks=""

# 1. 颜色输出
if grep -rq "\\033\[" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 使用颜色输出${NC}"
    ((visual_score+=25))
else
    echo -e "  ${YELLOW}⚠️ 无颜色输出${NC}"
    visual_checks="${visual_checks}添加颜色输出 (如 \\033[0;32m 表示绿色)\n"
fi

# 2. 表格格式
if grep -rqE "\|.*\||printf.*%|column|awk.*print" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 使用表格/格式化输出${NC}"
    ((visual_score+=25))
else
    echo -e "  ${YELLOW}⚠️ 无格式化输出${NC}"
fi

# 3. 图标/Emoji
if grep -rqE "✅|❌|⚠️|🔴|🟢|🟡|📋|🔍|💡|🎨|🌍|🗣️" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 使用图标/Emoji${NC}"
    ((visual_score+=25))
else
    echo -e "  ${YELLOW}⚠️ 无图标${NC}"
fi

# 4. 分隔线
if grep -rqE "^[-=]{5,}|━|─|╔|╚" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 使用分隔线${NC}"
    ((visual_score+=25))
else
    echo -e "  ${YELLOW}⚠️ 无分隔线${NC}"
fi

SCORES[visual]=$visual_score
echo ""
echo -e "  评分: ${BLUE}$visual_score/100${NC}"

# ========== 时区验证 ==========
echo ""
echo -e "${YELLOW}🌍 时区处理验证${NC}"
echo "---"

tz_score=0
tz_issues=""

# 1. UTC 使用
if grep -rq "UTC\|utc\|iso8601\|ISO 8601" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 使用 UTC 或 ISO 8601${NC}"
    ((tz_score+=30))
fi

# 2. TZ 环境变量
if grep -rq "TZ=\|timezone\|TimeZone" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 支持时区配置${NC}"
    ((tz_score+=30))
fi

# 3. 硬编码时区检查
if grep -rqE "CST|PST|EST|GMT\+[0-9]|北京时间" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${YELLOW}⚠️ 发现硬编码时区${NC}"
    tz_issues="${tz_issues}替换硬编码时区为 TZ 环境变量\n"
else
    echo -e "  ${GREEN}✅ 无硬编码时区${NC}"
    ((tz_score+=20))
fi

# 4. 时间格式化
if grep -rq "date.*+%|strftime|moment|dayjs" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 使用时间格式化${NC}"
    ((tz_score+=20))
fi

SCORES[tz]=$tz_score
echo ""
echo -e "  评分: ${BLUE}$tz_score/100${NC}"

# ========== 多语言验证 ==========
echo ""
echo -e "${YELLOW}🗣️ 多语言支持验证${NC}"
echo "---"

i18n_score=0
i18n_issues=""

# 1. 语言资源目录
if [ -d "$SKILL_PATH/locales" ] || [ -d "$SKILL_PATH/i18n" ] || [ -d "$SKILL_PATH/lang" ]; then
    echo -e "  ${GREEN}✅ 包含语言资源目录${NC}"
    ((i18n_score+=40))
else
    echo -e "  ${YELLOW}⚠️ 无语言资源目录${NC}"
    i18n_issues="${i18n_issues}创建 locales/ 目录存放语言文件\n"
fi

# 2. 硬编码文本检查
hardcoded=$(grep -rE "(错误|成功|失败|提示|警告|注意|Error|Success|Failed|Warning)" "$SKILL_PATH"/*.sh 2>/dev/null | wc -l || echo 0)
if [ "$hardcoded" -gt 10 ]; then
    echo -e "  ${YELLOW}⚠️ 发现 $hardcoded 处硬编码文本${NC}"
    i18n_issues="${i18n_issues}将硬编码文本提取到语言文件\n"
elif [ "$hardcoded" -gt 0 ]; then
    echo -e "  ${GREEN}✅ 少量硬编码文本 ($hardcoded 处)${NC}"
    ((i18n_score+=20))
else
    echo -e "  ${GREEN}✅ 无硬编码文本${NC}"
    ((i18n_score+=30))
fi

# 3. UTF-8 支持
if grep -rq "UTF-8\|utf8\|LANG" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 声明 UTF-8 编码${NC}"
    ((i18n_score+=30))
else
    echo -e "  ${YELLOW}⚠️ 未声明编码${NC}"
fi

# 4. 环境变量 LOCALE 支持
if grep -rq "LANG\|LOCALE\|LANGUAGE" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 支持语言环境变量${NC}"
    ((i18n_score+=30))
fi

SCORES[i18n]=$i18n_score
echo ""
echo -e "  评分: ${BLUE}$i18n_score/100${NC}"

# ========== 用户引导验证 ==========
echo ""
echo -e "${YELLOW}🎯 用户引导验证${NC}"
echo "---"

guide_score=0

# 1. 帮助文档
if grep -rq "help\|--help\|用法\|usage" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 包含帮助信息${NC}"
    ((guide_score+=30))
else
    echo -e "  ${YELLOW}⚠️ 缺少帮助信息${NC}"
fi

# 2. 使用示例
if grep -rq "示例\|example\|Example\|Example:" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 包含使用示例${NC}"
    ((guide_score+=30))
else
    echo -e "  ${YELLOW}⚠️ 缺少使用示例${NC}"
fi

# 3. 错误提示
if grep -rq "请检查\|Please check\|建议\|suggest\|建议：" "$SKILL_PATH" 2>/dev/null; then
    echo -e "  ${GREEN}✅ 错误信息包含建议${NC}"
    ((guide_score+=20))
else
    echo -e "  ${YELLOW}⚠️ 错误信息缺少建议${NC}"
fi

# 4. SKILL.md 文档
if [ -f "$SKILL_PATH/SKILL.md" ]; then
    lines=$(wc -l < "$SKILL_PATH/SKILL.md")
    if [ "$lines" -gt 50 ]; then
        echo -e "  ${GREEN}✅ SKILL.md 文档完整 ($lines 行)${NC}"
        ((guide_score+=20))
    else
        echo -e "  ${YELLOW}⚠️ SKILL.md 文档较简单 ($lines 行)${NC}"
    fi
fi

SCORES[guide]=$guide_score
echo ""
echo -e "  评分: ${BLUE}$guide_score/100${NC}"

# ========== 综合评分 ==========
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

total_score=$(( (${SCORES[visual]} + ${SCORES[tz]} + ${SCORES[i18n]} + ${SCORES[guide]}) / 4 ))

echo ""
echo -e "${BLUE}📊 UX 综合评分${NC}"
echo ""
echo "  可视化:   ${SCORES[visual]}/100"
echo "  时区处理: ${SCORES[tz]}/100"
echo "  多语言:   ${SCORES[i18n]}/100"
echo "  用户引导: ${SCORES[guide]}/100"
echo ""
echo -e "  ${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  总分:     ${CYAN}$total_score/100${NC}"

# 等级评定
if [ $total_score -ge 90 ]; then
    grade="🌟 优秀"
elif [ $total_score -ge 70 ]; then
    grade="✅ 良好"
elif [ $total_score -ge 50 ]; then
    grade="⚠️ 一般"
else
    grade="❌ 需改进"
fi

echo -e "  等级:     $grade${NC}"

# ========== 最佳实践建议 ==========
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}💡 最佳实践建议${NC}"
echo "---"

if [ ${SCORES[visual]} -lt 70 ]; then
    echo ""
    echo "【可视化改进】"
    echo "  • 添加颜色输出提升可读性"
    echo "  • 使用表格展示结构化数据"
    echo "  • 使用图标区分状态 (✅ ❌ ⚠️)"
fi

if [ ${SCORES[tz]} -lt 70 ]; then
    echo ""
    echo "【时区处理】"
    echo "  • 使用 ISO 8601 格式: date -u +%Y-%m-%dT%H:%M:%SZ"
    echo "  • 支持用户时区: export TZ=Asia/Shanghai"
    echo "  • 避免硬编码时区"
fi

if [ ${SCORES[i18n]} -lt 70 ]; then
    echo ""
    echo "【国际化】"
    echo "  • 创建 locales/ 目录"
    echo "  • 将文本提取到语言文件:"
    echo "    locales/en.json: {\"error\": \"Not found\"}"
    echo "    locales/zh.json: {\"error\": \"未找到\"}"
    echo "  • 支持环境变量: LANG=zh_CN"
fi

if [ ${SCORES[guide]} -lt 70 ]; then
    echo ""
    echo "【用户引导】"
    echo "  • 添加 --help 参数"
    echo "  • 包含使用示例"
    echo "  • 错误信息附带解决建议"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${CYAN}UX 验证完成！${NC}"
echo ""
