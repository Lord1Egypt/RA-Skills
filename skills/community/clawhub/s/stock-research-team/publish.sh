#!/usr/bin/env bash
# ============================================================
# AI 投研团队 — 一键发布到 GitHub
# 用法：bash publish.sh
# ============================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

REPO_NAME="stock-research-team"
REPO_DESC="Multi-role AI stock research team skill for OpenClaw — Technical, Fundamental, Macro, Sentiment analysis with MCP Server"

cd "$(dirname "$0")"

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  📈 AI 投研团队 — 发布到 GitHub${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Step 1: 检查 gh CLI
if ! command -v gh &>/dev/null; then
    echo -e "${RED}[FAIL]${NC} GitHub CLI (gh) 未安装"
    echo "  安装方式: brew install gh"
    exit 1
fi

# Step 2: 检查认证状态
if ! gh auth status &>/dev/null 2>&1; then
    echo -e "${YELLOW}[INFO]${NC} 请先登录 GitHub..."
    gh auth login
fi

echo -e "${GREEN}[OK]${NC}   GitHub 已认证"

# Step 3: 初始化 Git（如果尚未初始化）
if [ ! -d ".git" ]; then
    git init
    echo -e "${GREEN}[OK]${NC}   Git 仓库已初始化"
fi

# Step 4: 添加所有文件
git add -A
git commit -m "feat: initial release — AI Stock Research Team skill v1.0.0

Multi-role AI stock research team for OpenClaw:
- 6 specialized analyst roles (Technical/Fundamental/Macro/Sentiment/Bull/Bear)
- MCP Server with 5 financial data tools (akshare + yfinance)
- A-share and US stock support with auto market detection
- Bull-bear debate, trading strategy, and risk review
- Composite scoring system (100-point scale)
- Automated setup with Python venv and MCP registration
- HTML report template for visual presentation"

echo -e "${GREEN}[OK]${NC}   代码已提交"

# Step 5: 创建 GitHub 仓库并推送
echo -e "${YELLOW}[INFO]${NC} 创建 GitHub 仓库..."

gh repo create "$REPO_NAME" \
    --public \
    --description "$REPO_DESC" \
    --source . \
    --push \
    --remote origin

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✅ 发布完成！${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "  GitHub:   https://github.com/charonling/$REPO_NAME"
echo ""
echo "  下一步（可选）— 发布到 ClawHub："
echo "    npm install -g clawhub"
echo "    clawhub login"
echo "    clawhub publish . --slug $REPO_NAME --name 'AI Stock Research Team' --version 1.0.0"
echo ""

# 清理自身（publish.sh 不需要保留在仓库中）
echo -e "${YELLOW}[INFO]${NC} 提示：publish.sh 仅用于首次发布，可删除后 git push"
echo ""
