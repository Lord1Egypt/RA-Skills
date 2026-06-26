#!/bin/bash
# publish.sh - 一键发布 Threshold Trader 到 ClawHub 和 GitHub

set -e  # 遇到错误立即退出

echo "========================================"
echo "📦 Publishing Threshold Trader Skill"
echo "========================================"

# 检查是否在正确的目录
if [ ! -f "SKILL.md" ] || [ ! -f "clawhub.json" ]; then
    echo "❌ Error: Must run from threshold-trader directory"
    exit 1
fi

# 发布到 ClawHub
echo ""
echo "1️⃣ Publishing to ClawHub..."
echo "----------------------------------------"

# 询问版本号
echo "Enter version number (e.g., 1.0.0, 1.0.1, 1.1.0):"
echo "  - 1.0.0 = Initial release"
echo "  - 1.0.x = Bug fixes"
echo "  - 1.x.0 = New features"
echo "  - x.0.0 = Breaking changes"
read -p "Version [default: 1.0.0]: " VERSION

# 如果用户没输入，使用默认值
if [ -z "$VERSION" ]; then
    VERSION="1.0.0"
fi

echo "Publishing version $VERSION..."
npx clawhub@latest publish . --slug threshold-trader --version "$VERSION"

echo ""
echo "✅ Published to ClawHub successfully!"

# 如果有 git 仓库，同时推送
if [ -d .git ]; then
    echo ""
    echo "2️⃣ Pushing to GitHub..."
    echo "----------------------------------------"
    
    git add .
    TIMESTAMP=$(date +%Y-%m-%d_%H:%M:%S)
    git commit -m "Publish to ClawHub - $TIMESTAMP" || echo "No changes to commit"
    git push || echo "⚠️  Git push failed (maybe no remote configured)"
    
    echo "✅ Pushed to GitHub!"
else
    echo ""
    echo "ℹ️  No git repository found. Skipping GitHub push."
    echo "   To add GitHub tracking, run:"
    echo "   git init && git remote add origin <your-repo-url>"
fi

echo ""
echo "========================================"
echo "✅ All done!"
echo "========================================"
echo ""
echo "📊 Your skill will appear at:"
echo "   https://simmer.markets/skills"
echo "   (syncs within 6 hours)"
echo ""
echo "🧪 Test installation with:"
echo "   npx clawhub@latest install threshold-trader"
echo ""
