#!/bin/bash
# SDD 开发工作流 - 环境检查脚本
# 检查所有必要的依赖是否已安装

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 计数器
PASS=0
FAIL=0
WARN=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    echo -e "  ${YELLOW}→${NC} $2"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    echo -e "  ${YELLOW}→${NC} $2"
    ((WARN++))
}

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  SDD 开发工作流 - 环境检查${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# 检查 Python 3.11+
echo -e "${BLUE}[Python]${NC}"
if command -v python3.11 &> /dev/null; then
    PY_VER=$(python3.11 --version 2>&1)
    check_pass "Python 3.11+ 已安装: $PY_VER"
elif command -v python3.12 &> /dev/null; then
    PY_VER=$(python3.12 --version 2>&1)
    check_pass "Python 3.12+ 已安装: $PY_VER"
elif command -v python3 &> /dev/null; then
    PY_VER=$(python3 --version 2>&1)
    PY_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
    PY_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 11 ]; then
        check_pass "Python 版本符合要求: $PY_VER"
    else
        check_fail "Python 版本过低: $PY_VER (需要 3.11+)" "sudo apt-get install python3.11"
    fi
else
    check_fail "Python 未安装" "sudo apt-get install python3.11"
fi

# 检查 Git
echo ""
echo -e "${BLUE}[Git]${NC}"
if command -v git &> /dev/null; then
    GIT_VER=$(git --version)
    check_pass "Git 已安装: $GIT_VER"
else
    check_fail "Git 未安装" "sudo apt-get install git"
fi

# 检查 UV
echo ""
echo -e "${BLUE}[UV 包管理器]${NC}"
if command -v uv &> /dev/null; then
    UV_VER=$(uv --version 2>&1)
    check_pass "UV 已安装: $UV_VER"
else
    check_fail "UV 未安装" "curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

# 检查 specify-cli
echo ""
echo -e "${BLUE}[Speckit]${NC}"
if command -v specify &> /dev/null; then
    check_pass "specify-cli 已安装"
else
    check_fail "specify-cli 未安装" "uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"
fi

# 检查 Claude Code
echo ""
echo -e "${BLUE}[Claude Code]${NC}"
if command -v claude &> /dev/null; then
    CLAUDE_VER=$(claude --version 2>&1 || echo "已安装")
    check_pass "Claude Code 已安装: $CLAUDE_VER"
else
    check_fail "Claude Code 未安装" "npm install -g @anthropic-ai/claude-code"
fi

# 检查 Claude Code 配置
echo ""
echo -e "${BLUE}[Claude Code 配置]${NC}"
if [ -f ~/.claude/settings.json ]; then
    if grep -q "glm-5" ~/.claude/settings.json 2>/dev/null; then
        check_pass "GLM-5 模型已配置"
    else
        check_warn "GLM-5 模型未配置" "编辑 ~/.claude/settings.json 添加 ANTHROPIC_DEFAULT_*_MODEL"
    fi
    if grep -q "bigmodel.cn" ~/.claude/settings.json 2>/dev/null; then
        check_pass "智谱 API 已配置"
    else
        check_warn "智谱 API 未配置" "运行 coding-helper auth glm_coding_plan_china <API_KEY>"
    fi
else
    check_warn "Claude Code 配置文件不存在" "运行 coding-helper auth reload claude"
fi

# 检查 tmux
echo ""
echo -e "${BLUE}[tmux]${NC}"
if command -v tmux &> /dev/null; then
    TMUX_VER=$(tmux -V)
    check_pass "tmux 已安装: $TMUX_VER"
else
    check_fail "tmux 未安装" "sudo apt-get install tmux"
fi

# 检查 coding-helper（可选）
echo ""
echo -e "${BLUE}[Coding Helper]${NC}"
if command -v coding-helper &> /dev/null || command -v chelper &> /dev/null; then
    check_pass "coding-helper 已安装"
else
    check_warn "coding-helper 未安装（可选）" "npm install -g @z_ai/coding-helper"
fi

# 检查网络
echo ""
echo -e "${BLUE}[网络]${NC}"
if curl -s -o /dev/null -w "%{http_code}" https://api.github.com 2>/dev/null | grep -q "200"; then
    check_pass "GitHub API 可访问"
else
    check_warn "GitHub API 访问受限" "可能需要配置代理或 GitHub Token"
fi

# 总结
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "  ${GREEN}通过: $PASS${NC}  ${RED}失败: $FAIL${NC}  ${YELLOW}警告: $WARN${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

if [ $FAIL -gt 0 ]; then
    echo -e "${RED}环境检查未通过，请先安装缺失的依赖。${NC}"
    exit 1
elif [ $WARN -gt 0 ]; then
    echo -e "${YELLOW}环境检查通过，但有警告项，建议处理。${NC}"
    exit 0
else
    echo -e "${GREEN}环境检查通过！可以开始开发。${NC}"
    exit 0
fi
