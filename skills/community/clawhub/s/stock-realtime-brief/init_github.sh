#!/usr/bin/env bash
# 一键初始化 GitHub 仓库脚本
# 用法: ./init_github.sh <your-github-username>

set -e

GITHUB_USER="${1:-Michaelliugh}"
REPO_NAME="stock-realtime-brief"

echo "🚀 初始化 GitHub 仓库: ${GITHUB_USER}/${REPO_NAME}"
echo ""

# 1. 替换 README 和 SKILL.md 中的占位符
echo "📝 替换占位符..."
find . -name "*.md" -o -name "*.toml" -o -name "*.yml" | xargs sed -i "s/Michaelliugh/${GITHUB_USER}/g" 2>/dev/null || true
find . -name "*.md" -o -name "*.toml" | xargs sed -i "s/Michaelliugh/${GITHUB_USER}/g" 2>/dev/null || true

# 2. Git init
if [ ! -d ".git" ]; then
    echo "📦 git init..."
    git init -b main
fi

# 3. 提交
echo "📝 git add + commit..."
git add .
git commit -m "feat: initial release v2.2.0 — three-mode A-share analyzer with stop-loss discipline" || true

# 4. 创建 GitHub 仓库
echo ""
echo "✅ 本地准备完成！"
echo ""
echo "下一步（手动执行）:"
echo ""
echo "  方式 A：使用 gh cli"
echo "    gh repo create ${REPO_NAME} --public --description 'A-share real-time analysis with three modes (portfolio/single/multi)' --homepage 'https://github.com/${GITHUB_USER}/${REPO_NAME}'"
echo "    git remote add origin git@github.com:${GITHUB_USER}/${REPO_NAME}.git"
echo "    git push -u origin main"
echo ""
echo "  方式 B：在 GitHub 网页创建后"
echo "    git remote add origin https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
echo "    git push -u origin main"
echo ""
echo "  发布版本:"
echo "    git tag -a v2.2.0 -m 'v2.2.0 release'"
echo "    git push --tags"
echo ""
echo "📖 推荐 topics:"
echo "    a-share, stock-analysis, technical-analysis, openclaw, hermes-skill, trading, china-stock, tushare-alternative"
