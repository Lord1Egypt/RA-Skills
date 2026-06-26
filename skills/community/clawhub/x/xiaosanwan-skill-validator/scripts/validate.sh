#!/bin/bash
# Skill 功能验证主脚本
# 用法: validate.sh <skill-name>

# 不使用 set -e，允许部分失败
# set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SKILL_NAME=$1
SKILL_DIR="/root/.openclaw/workspace/skills"

# 检查参数
if [ -z "$SKILL_NAME" ]; then
    echo "用法: $0 <skill-name>"
    echo ""
    echo "已安装的技能:"
    ls -1 "$SKILL_DIR" 2>/dev/null | head -20
    exit 1
fi

SKILL_PATH="$SKILL_DIR/$SKILL_NAME"

# 初始化计数器
PASS=0
WARN=0
FAIL=0
SKIP=0
TOTAL=0

# 结果记录
RESULTS=""

# 验证函数
check_pass() {
    ((PASS++))
    ((TOTAL++))
    RESULTS="${RESULTS}  ✓ $1\n"
}

check_warn() {
    ((WARN++))
    ((TOTAL++))
    RESULTS="${RESULTS}  ⚠ $1\n"
}

check_fail() {
    ((FAIL++))
    ((TOTAL++))
    RESULTS="${RESULTS}  ✗ $1\n"
}

check_skip() {
    ((SKIP++))
    ((TOTAL++))
    RESULTS="${RESULTS}  ⊘ $1\n"
}

# 开始验证
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         🧪 Skill 验证: $SKILL_NAME                    ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📅 验证时间: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ========== 第一阶段：基础验证（举例法）==========
echo ""
echo -e "${YELLOW}📦 第一阶段：基础验证${NC}"
echo "---"

# 1. 检查目录存在
if [ -d "$SKILL_PATH" ]; then
    check_pass "技能目录存在"
else
    check_fail "技能目录不存在: $SKILL_PATH"
    echo ""
    echo -e "${RED}❌ Skill 未安装: $SKILL_NAME${NC}"
    echo "安装命令: clawhub install $SKILL_NAME"
    exit 1
fi

# 2. 检查 SKILL.md
if [ -f "$SKILL_PATH/SKILL.md" ]; then
    check_pass "SKILL.md 文件存在"
    
    # 检查必要字段
    if grep -q "^name:" "$SKILL_PATH/SKILL.md"; then
        check_pass "SKILL.md 包含 name 字段"
    else
        check_warn "SKILL.md 缺少 name 字段"
    fi
    
    if grep -q "^description:" "$SKILL_PATH/SKILL.md"; then
        check_pass "SKILL.md 包含 description 字段"
    else
        check_warn "SKILL.md 缺少 description 字段"
    fi
else
    check_fail "SKILL.md 文件缺失"
fi

# 3. 检查 scripts 目录
if [ -d "$SKILL_PATH/scripts" ]; then
    check_pass "scripts/ 目录存在"
    
    # 检查脚本文件
    script_count=$(ls -1 "$SKILL_PATH/scripts"/*.sh 2>/dev/null | wc -l)
    if [ $script_count -gt 0 ]; then
        check_pass "包含 $script_count 个脚本文件"
    else
        check_warn "scripts/ 目录为空"
    fi
else
    check_warn "scripts/ 目录不存在"
fi

# 4. 检查依赖（从 SKILL.md 提取）
echo ""
echo -e "${BLUE}🔍 检查依赖...${NC}"

# 提取 bins 依赖
bins=$(grep -oP 'bins.*?\[.*?\]' "$SKILL_PATH/SKILL.md" 2>/dev/null | grep -oP '\[.*?\]' | tr -d '[]"' | tr ',' '\n' | tr -d ' ')
if [ -n "$bins" ]; then
    for bin in $bins; do
        if command -v "$bin" >/dev/null 2>&1; then
            check_pass "依赖 $bin 可用"
        else
            check_fail "依赖 $bin 不可用"
        fi
    done
fi

# 提取 env 依赖
envs=$(grep -oP 'env.*?\[.*?\]' "$SKILL_PATH/SKILL.md" 2>/dev/null | grep -oP '\[.*?\]' | tr -d '[]"' | tr ',' '\n' | tr -d ' ' | tr -d "'")
if [ -n "$envs" ]; then
    for env in $envs; do
        # 跳过空值
        [ -z "$env" ] && continue
        if [ -n "${!env}" ]; then
            check_pass "环境变量 $env 已设置"
        else
            check_warn "环境变量 $env 未设置"
        fi
    done
fi

# ========== 第二阶段：异常验证（反证法）==========
echo ""
echo -e "${YELLOW}🧪 第二阶段：异常验证${NC}"
echo "---"

# 测试空参数
first_script=$(ls "$SKILL_PATH/scripts"/*.sh 2>/dev/null | head -1)
if [ -n "$first_script" ] && [ -f "$first_script" ]; then
    # 空参数测试
    output=$($first_script 2>&1) && result=0 || result=$?
    if [ $result -eq 0 ] || echo "$output" | grep -qi "usage\|用法\|参数\|help"; then
        check_pass "空参数测试：有正确提示"
    else
        check_warn "空参数测试：无明确提示"
    fi
else
    check_skip "异常验证：无可执行脚本"
fi

# ========== 第三阶段：功能测试 ==========
echo ""
echo -e "${YELLOW}⚡ 第三阶段：功能测试${NC}"
echo "---"

# 根据技能类型进行特定测试
case "$SKILL_NAME" in
    *email*)
        # 邮件技能测试
        echo "检测到邮件类技能..."
        if [ -n "$EMAIL_ADDRESS" ] && [ -n "$EMAIL_PASSWORD" ]; then
            check_pass "邮件配置完整"
        else
            check_warn "邮件配置不完整"
        fi
        ;;
    *diagnose*)
        # 诊断技能测试
        echo "检测到诊断类技能..."
        if [ -f "$SKILL_PATH/scripts/diagnose.sh" ]; then
            output=$(bash "$SKILL_PATH/scripts/diagnose.sh" 2>&1 | head -5)
            if [ -n "$output" ]; then
                check_pass "诊断脚本可执行"
            else
                check_fail "诊断脚本执行失败"
            fi
        fi
        ;;
    *)
        # 通用测试
        echo "执行通用功能测试..."
        if [ -f "$SKILL_PATH/scripts"/*.sh ]; then
            check_pass "存在可执行脚本"
        else
            check_skip "无可执行脚本"
        fi
        ;;
esac

# ========== 第四阶段：UX 验证 ==========
echo ""
echo -e "${YELLOW}🎨 第四阶段：UX 验证${NC}"
echo "---"

# 可视化检查
if grep -rq "\\033\[" "$SKILL_PATH" 2>/dev/null; then
    check_pass "可视化：使用颜色输出"
else
    check_warn "可视化：建议添加颜色输出"
fi

# 时区检查
if grep -rq "UTC\|iso8601" "$SKILL_PATH" 2>/dev/null; then
    check_pass "时区：使用 UTC 时间"
elif grep -rqE "CST|PST|EST|GMT\+[0-9]" "$SKILL_PATH" 2>/dev/null; then
    check_warn "时区：发现硬编码时区"
else
    check_skip "时区：未使用时间"
fi

# 多语言检查
if [ -d "$SKILL_PATH/locales" ] || [ -d "$SKILL_PATH/i18n" ]; then
    check_pass "国际化：包含语言资源"
else
    check_warn "国际化：建议添加多语言支持"
fi

# 用户引导检查
if grep -rq "help\|--help\|用法" "$SKILL_PATH" 2>/dev/null; then
    check_pass "用户引导：包含帮助信息"
else
    check_warn "用户引导：建议添加帮助信息"
fi

# ========== 生成报告 ==========
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}📊 验证结果${NC}"
echo "---"
echo -e "$RESULTS"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}📈 统计${NC}"
echo "  通过: $PASS"
echo "  警告: $WARN"
echo "  失败: $FAIL"
echo "  跳过: $SKIP"
echo ""

# 计算分数
SCORE=$((PASS * 100 / TOTAL))
if [ $SCORE -ge 90 ]; then
    GRADE="🌟 优秀"
elif [ $SCORE -ge 70 ]; then
    GRADE="✅ 良好"
elif [ $SCORE -ge 50 ]; then
    GRADE="⚠️ 可用"
else
    GRADE="❌ 不可用"
fi

echo -e "${BLUE}📋 评分${NC}"
echo "  分数: $SCORE/100"
echo "  等级: $GRADE"

# ========== 生成建议 ==========
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}💡 完善建议${NC}"
echo "---"

if [ $FAIL -gt 0 ]; then
    echo ""
    echo "【必须修复】"
    [ ! -f "$SKILL_PATH/SKILL.md" ] && echo "  1. 创建 SKILL.md 文件，包含 name 和 description"
    echo ""
fi

if [ $WARN -gt 0 ]; then
    echo "【建议完善】"
    
    # 检查环境变量
    if echo "$RESULTS" | grep -q "环境变量.*未设置"; then
        echo "  1. 设置必要的环境变量"
        echo "     export 变量名='值'"
    fi
    
    # 检查脚本
    if [ ! -d "$SKILL_PATH/scripts" ]; then
        echo "  2. 创建 scripts/ 目录并添加脚本"
    fi
    
    # 检查文档
    if grep -q "SKILL.md 缺少" <<< "$RESULTS"; then
        echo "  3. 完善 SKILL.md 文档"
    fi
    
    echo ""
fi

# 优化建议
echo "【优化建议】"
echo "  1. 添加使用示例到 SKILL.md"
echo "  2. 添加错误处理和提示"
echo "  3. 编写测试用例"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${CYAN}验证完成！${NC}"
echo ""
