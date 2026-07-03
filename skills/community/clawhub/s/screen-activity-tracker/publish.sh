#!/bin/bash
# ClawHub 发布命令生成脚本
# 使用方法：bash publish.sh

SKILL_NAME="screen-activity-tracker"
SKILL_DIR="/Users/zeject/ai/skills/mySkills/screen-activity-tracker"
GITHUB_USER="zeject"
GITHUB_REPO="screen-activity-tracker"

echo "==================================="
echo "Screen Activity Tracker - 发布指南"
echo "==================================="
echo ""

# 1. 检查 ClawHub CLI
echo "1. 检查 ClawHub CLI..."
if ! command -v clawhub &> /dev/null; then
    echo "   ❌ ClawHub CLI 未安装"
    echo "   安装命令: npm install -g clawhub"
    exit 1
else
    echo "   ✓ ClawHub CLI 已安装"
fi
echo ""

# 2. 登录 ClawHub
echo "2. 登录 ClawHub..."
echo "   执行命令: clawhub login"
echo "   或者: clawhub login --token <YOUR_TOKEN>"
echo ""

# 3. 检查 GitHub 仓库
echo "3. 创建 GitHub 仓库（如果还没有）..."
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit: Screen Activity Tracker v1.0.0'"
echo "   gh repo create $GITHUB_USER/$GITHUB_REPO --public"
echo "   git remote add origin https://github.com/$GITHUB_USER/$GITHUB_REPO.git"
echo "   git push -u origin main"
echo ""

# 4. 发布到 ClawHub
echo "4. 发布到 ClawHub..."
echo "   命令选项 A - 从本地发布:"
echo "   clawhub publish $SKILL_DIR \\"
echo "     --slug $SKILL_NAME \\"
echo "     --name \"Screen Activity Tracker\" \\"
echo "     --version 1.0.0 \\"
echo "     --changelog \"Initial release with screenshot tracking, AI analysis, and dual backend support\" \\"
echo "     --tags \"screenshot,productivity,vision,siyuan,tracking\""
echo ""
echo "   命令选项 B - 从 GitHub 导入（推荐）:"
echo "   1. 访问 https://clawhub.ai"
echo "   2. 登录后点击 'Publish'"
echo "   3. 选择 'Import from GitHub'"
echo "   4. 输入: https://github.com/$GITHUB_USER/$GITHUB_REPO"
echo "   5. 填写信息并发布"
echo ""

# 5. 更新版本
echo "5. 后续更新版本..."
echo "   修改 SKILL.md 中的 version 字段"
echo "   git commit -m 'Bump version to 1.0.1'"
echo "   git push"
echo "   clawhub publish $SKILL_DIR \\"
echo "     --slug $SKILL_NAME \\"
echo "     --version 1.0.1 \\"
echo "     --changelog 'Bug fixes and improvements'"
echo ""

# 6. 安装测试
echo "6. 测试安装..."
echo "   clawhub search $SKILL_NAME"
echo "   clawhub install $SKILL_NAME"
echo ""

echo "==================================="
echo "完整发布流程已生成"
echo "==================================="
