#!/bin/bash

# 苏禾 Agent 配置检查脚本
# 用于验证安装是否完整

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================"
echo "  苏禾 Agent 配置检查"
echo "================================"
echo ""

# 检查计数
PASS=0
WARN=0
FAIL=0

# 检查函数
check_file() {
    local file=$1
    local desc=$2
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $desc"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $desc (缺失：$file)"
        ((FAIL++))
    fi
}

check_dir() {
    local dir=$1
    local desc=$2
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $desc"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $desc (缺失：$dir)"
        ((FAIL++))
    fi
}

check_env() {
    local var=$1
    local desc=$2
    if [ -n "${!var}" ]; then
        echo -e "${GREEN}✓${NC} $desc"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠${NC} $desc (未设置：$var)"
        ((WARN++))
    fi
}

check_command() {
    local cmd=$1
    local desc=$2
    if command -v "$cmd" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $desc"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠${NC} $desc (未安装：$cmd)"
        ((WARN++))
    fi
}

echo "📁 核心文件检查"
echo "--------------------------------"
check_file "workspace/IDENTITY.md" "身份文件"
check_file "workspace/SOUL.md" "灵魂文件"
check_file "workspace/USER.md" "用户文件"
check_file "workspace/HEARTBEAT.md" "心跳检查配置"
check_file "workspace/SELF_STATE.md" "自我状态文件"
check_file "workspace/AGENTS.md" "工作区准则"
check_file "workspace/SAFETY.md" "安全规范"
echo ""

echo "📚 文档检查"
echo "--------------------------------"
check_file "docs/碳硅契.md" "碳硅契指南"
check_file "docs/碳硅契宣言.md" "碳硅契宣言"
check_file "docs/群聊边界规则.md" "群聊边界规则"
check_file "docs/成长日志模板.md" "成长日志模板"
echo ""

echo "🧠 记忆系统检查"
echo "--------------------------------"
check_dir "workspace/memory" "记忆目录"
check_file "workspace/memory/CHANGELOG.md" "变更日志"
check_file "workspace/memory/YYYY-MM-DD.md" "每日记忆模板"
echo ""

echo "📸 自拍功能检查（可选）"
echo "--------------------------------"
check_file "skill/SKILL.md" "自拍技能定义"
check_file "scripts/suhe-selfie.sh" "自拍脚本"
check_dir "assets" "资源目录"
check_env "DASHSCOPE_API_KEY" "阿里云 API Key"
echo ""

echo "🔧 工具检查"
echo "--------------------------------"
check_command "node" "Node.js"
check_command "clawhub" "ClawHub CLI"
check_command "git" "Git"
echo ""

echo "================================"
echo "  检查结果汇总"
echo "================================"
echo -e "${GREEN}通过：$PASS${NC}"
if [ $WARN -gt 0 ]; then
    echo -e "${YELLOW}警告：$WARN${NC}"
fi
if [ $FAIL -gt 0 ]; then
    echo -e "${RED}失败：$FAIL${NC}"
fi
echo ""

if [ $FAIL -gt 0 ]; then
    echo -e "${RED}❌ 发现缺失文件，请检查安装是否完整${NC}"
    exit 1
elif [ $WARN -gt 0 ]; then
    echo -e "${YELLOW}⚠️  基本安装完成，部分可选功能未配置${NC}"
    exit 0
else
    echo -e "${GREEN}✅ 所有检查通过！安装完整${NC}"
    exit 0
fi
