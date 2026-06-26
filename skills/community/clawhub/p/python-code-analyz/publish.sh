#!/bin/bash
# ClawHub 发布脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
SKILL_NAME="Code Analyzer"
SKILL_SLUG="code-analyzer"
VERSION=$(grep -o '"version": "[^"]*"' package.json | cut -d'"' -f4)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ClawHub Skill 发布脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查 ClawHub CLI
echo -e "${YELLOW}▶ 检查 ClawHub CLI...${NC}"
if ! command -v clawhub &> /dev/null; then
    echo -e "${RED}✗ ClawHub CLI 未安装${NC}"
    echo "请运行: npm i -g clawhub"
    exit 1
fi
echo -e "${GREEN}✓ ClawHub CLI 已安装${NC}"

# 检查登录状态
echo -e "${YELLOW}▶ 检查登录状态...${NC}"
if ! clawhub whoami &> /dev/null; then
    echo -e "${RED}✗ 未登录 ClawHub${NC}"
    echo "请运行: clawhub login"
    exit 1
fi
echo -e "${GREEN}✓ 已登录 ClawHub${NC}"

# 显示发布信息
echo ""
echo -e "${YELLOW}▶ 发布信息:${NC}"
echo "  Skill 名称: $SKILL_NAME"
echo "  Skill Slug: $SKILL_SLUG"
echo "  版本: $VERSION"
echo ""

# 确认发布
read -p "确认发布? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo -e "${YELLOW}已取消发布${NC}"
    exit 0
fi

# 执行发布
echo ""
echo -e "${YELLOW}▶ 开始发布...${NC}"

clawhub publish . \
    --slug "$SKILL_SLUG" \
    --name "$SKILL_NAME" \
    --version "$VERSION" \
    --changelog "Initial release: Python code analysis and optimization tool with security scanning, performance optimization, and automatic refactoring"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✓ 发布成功!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "验证安装:"
echo "  clawhub search \"code analyzer\""
echo "  clawhub install code-analyzer"
