#!/bin/bash
set -e
set -u
set -o pipefail

# 一键初始化脚本
# 用途：检查依赖、创建目录、设置环境、运行测试

echo "🚀 alex-writing Skill 初始化"
echo "======================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查函数
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✅ $1 已安装${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 未安装${NC}"
        return 1
    fi
}

# 步骤 1：检查依赖
echo "📦 步骤 1/5: 检查依赖"
echo "--------------------------------------"

MISSING_DEPS=0

# 检查 Node.js
if check_command node; then
    NODE_VERSION=$(node --version)
    echo "   版本: $NODE_VERSION"
else
    echo -e "${YELLOW}   请安装 Node.js: https://nodejs.org/${NC}"
    MISSING_DEPS=1
fi

echo ""

# 检查 Git（可选）
if check_command git; then
    GIT_VERSION=$(git --version)
    echo "   版本: $GIT_VERSION"
else
    echo -e "${YELLOW}   Git 未安装（可选）${NC}"
fi

echo ""

# 检查 agent-reach（可选）
if check_command mcporter; then
    echo -e "${GREEN}✅ agent-reach 已安装${NC}"
    echo "   可使用多平台搜索功能"
else
    echo -e "${YELLOW}⚠️ agent-reach 未安装（可选）${NC}"
    echo "   将使用基础搜索工具"
fi

echo ""

if [ $MISSING_DEPS -eq 1 ]; then
    echo -e "${RED}❌ 缺少必需依赖，请先安装${NC}"
    exit 1
fi

# 步骤 2：创建目录结构
echo "📁 步骤 2/5: 创建目录结构"
echo "--------------------------------------"

DIRS=("_briefs" "_协作文档" "知识资料" "历史文章" "images")

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${YELLOW}⚠️ $dir 已存在${NC}"
    else
        mkdir -p "$dir"
        echo -e "${GREEN}✅ 创建 $dir${NC}"
    fi
done

echo ""

# 步骤 3：检查环境变量
echo "🔑 步骤 3/5: 检查环境变量"
echo "--------------------------------------"

if [ -n "${GOOGLE_API_KEY:-}" ]; then
    echo -e "${GREEN}✅ GOOGLE_API_KEY 已设置${NC}"
    echo "   可使用封面图生成功能"
else
    echo -e "${YELLOW}⚠️ GOOGLE_API_KEY 未设置${NC}"
    echo ""
    read -p "是否现在设置 GOOGLE_API_KEY? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "请输入 GOOGLE_API_KEY: " API_KEY
        if [ -n "$API_KEY" ]; then
            # 添加到 ~/.zshrc 或 ~/.bashrc
            if [ -f "$HOME/.zshrc" ]; then
                echo "export GOOGLE_API_KEY=\"$API_KEY\"" >> "$HOME/.zshrc"
                echo -e "${GREEN}✅ 已添加到 ~/.zshrc${NC}"
                echo "   请运行: source ~/.zshrc"
            elif [ -f "$HOME/.bashrc" ]; then
                echo "export GOOGLE_API_KEY=\"$API_KEY\"" >> "$HOME/.bashrc"
                echo -e "${GREEN}✅ 已添加到 ~/.bashrc${NC}"
                echo "   请运行: source ~/.bashrc"
            fi
            export GOOGLE_API_KEY="$API_KEY"
        fi
    fi
fi

echo ""

# 步骤 4：运行测试
echo "🧪 步骤 4/5: 运行测试"
echo "--------------------------------------"

# 测试脚本语法
echo "检查脚本语法..."
if bash -n scripts/保存文章.sh && bash -n scripts/创建项目结构.sh && bash -n scripts/生成封面图-批量.sh; then
    echo -e "${GREEN}✅ Shell 脚本语法正确${NC}"
else
    echo -e "${RED}❌ Shell 脚本语法错误${NC}"
fi

echo ""

# 测试 Node.js 脚本
echo "检查 Node.js 脚本..."
if node scripts/检查文章质量.js 2>&1 | grep -q "请提供文章文件路径"; then
    echo -e "${GREEN}✅ 检查文章质量.js 可用${NC}"
else
    echo -e "${RED}❌ 检查文章质量.js 不可用${NC}"
fi

if node scripts/检查选题重复.js 2>&1 | grep -q "请提供选题标题"; then
    echo -e "${GREEN}✅ 检查选题重复.js 可用${NC}"
else
    echo -e "${RED}❌ 检查选题重复.js 不可用${NC}"
fi

echo ""

# 步骤 5：显示快速开始指南
echo "📚 步骤 5/5: 快速开始指南"
echo "--------------------------------------"
echo ""
echo "🎉 初始化完成！"
echo ""
echo "📖 快速开始:"
echo ""
echo "1. 查看快速参考手册:"
echo "   cat QUICK_REFERENCE.md"
echo ""
echo "2. 创建新项目:"
echo "   ./scripts/创建项目结构.sh \"项目名称\""
echo ""
echo "3. 生成封面图:"
echo "   ./scripts/生成封面图-批量.sh prompts/cover.md"
echo ""
echo "4. 检查文章质量:"
echo "   node scripts/检查文章质量.js \"文章.md\""
echo ""
echo "5. 检查选题重复:"
echo "   node scripts/检查选题重复.js \"选题标题\""
echo ""
echo "📚 文档导航:"
echo "   - 主流程: SKILL.md"
echo "   - 快速参考: QUICK_REFERENCE.md"
echo "   - 故障排查: TROUBLESHOOTING.md"
echo "   - 工作流程: workflows/README.md"
echo "   - 参考文档: references/README.md"
echo ""
echo "💡 遇到问题？查看故障排查指南:"
echo "   cat TROUBLESHOOTING.md"
echo ""
