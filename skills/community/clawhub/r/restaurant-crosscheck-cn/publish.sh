#!/bin/bash
# Quick publish script for ClawHub

echo "=========================================="
echo "📤 发布到 ClawHub"
echo "=========================================="
echo ""

SKILL_DIR="$(dirname "$(readlink -f "$0")")"
cd "$SKILL_DIR"

echo "📁 Skill 目录: $SKILL_DIR"
echo ""

# Check if SKILL.md exists
if [ ! -f "SKILL.md" ]; then
    echo "❌ 错误: 找不到 SKILL.md"
    exit 1
fi

echo "✅ 找到 SKILL.md"
echo ""

# Check if clawhub is installed
if ! command -v clawhub &> /dev/null; then
    echo "❌ ClawHub CLI 未安装"
    echo ""
    echo "请先安装:"
    echo "  npm install -g clawhub"
    echo ""
    echo "然后登录:"
    echo "  clawhub login"
    exit 1
fi

echo "✅ ClawHub CLI 已安装"
echo ""

# Check if logged in
if ! clawhub whoami &> /dev/null; then
    echo "⚠️ 未登录 ClawHub"
    echo ""
    echo "请先登录:"
    echo "  clawhub login"
    echo ""
    echo "或在有浏览器的设备上:"
    echo "  1. 访问 https://clawhub.ai"
    echo "  2. 登录并获取 API token"
    echo "  3. 使用: clawhub login --token YOUR_TOKEN"
    echo ""
    exit 1
fi

echo "✅ 已登录 ClawHub"
echo ""

echo "=========================================="
echo "准备发布"
echo "=========================================="
echo ""

# Display skill info
echo "Skill 信息:"
echo "  Slug: restaurant-crosscheck"
echo "  Name: 餐厅推荐交叉验证"
echo "  Version: 1.0.0"
echo ""

# Confirm publish
read -p "确认发布？(y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消"
    exit 0
fi

echo ""
echo "📤 正在发布..."
echo ""

# Publish
clawhub publish . \
  --slug restaurant-crosscheck \
  --name "餐厅推荐交叉验证" \
  --description "Cross-reference restaurant recommendations from Xiaohongshu and Dianping to validate restaurant quality and consistency." \
  --version 1.0.0 \
  --changelog "Initial release:

Features:
- Cross-platform validation (Dianping + Xiaohongshu)
- Location-based search by city/district
- Cuisine type filtering
- Consistency analysis between platforms
- Recommendation scoring (0-10)
- Server-friendly command-line tool
- Full documentation (Chinese + English)

Usage:
- Command line: restaurant-crosscheck 'location' 'cuisine'
- Dialogue integration: '查询深圳南山区推荐餐厅'
- Server version with mock data
- Full version with real scraping (requires browser)

Files:
- SKILL.md (skill definition)
- README.md (full documentation)
- QUICKSTART.md (quick start guide)
- SERVER_GUIDE.md (server usage)
- IMPLEMENTATION.md (technical details)
- restaurant-crosscheck (CLI tool)
- scripts/crosscheck_simple.py (server version)
- scripts/config.py (configuration)
" \
  --tags "restaurant,food,recommendation,dianping,xiaohongshu,chinese,china"

echo ""
echo "=========================================="
echo "✅ 发布完成！"
echo "=========================================="
echo ""

echo "验证发布:"
echo "  clawhub search restaurant-crosscheck"
echo ""
echo "查看详情:"
echo "  clawhub inspect restaurant-crosscheck"
echo ""
