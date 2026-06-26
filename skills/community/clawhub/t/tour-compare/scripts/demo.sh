#!/bin/bash

# tour-compare 功能演示脚本
# 运行此脚本展示所有核心功能

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "🦐 tour-compare 功能演示"
echo "========================================"
echo ""

# 测试 1: JSON 对比
echo "📊 测试 1: JSON 商品对比（带老人参数）"
echo "----------------------------------------"
node src/index.js compare \
  '{"platform":"携程","title":"云南昆明大理丽江 6 日游","price":3299,"rating":4.8,"shoppingStops":0,"hotelStars":4,"days":6}' \
  '{"platform":"飞猪","title":"云南经典 6 日游","price":2899,"rating":4.6,"shoppingStops":4,"hotelStars":3,"days":6}' \
  --group 老人

echo ""
echo "✅ 测试 1 完成"
echo ""
read -p "按回车继续..." </dev/tty

# 测试 2: 智能推荐
echo "🎯 测试 2: 智能推荐（云南，老人，5000 预算）"
echo "----------------------------------------"
node src/index.js recommend \
  --destination 云南 \
  --budget 5000 \
  --group 老人 \
  --days 6

echo ""
echo "✅ 测试 2 完成"
echo ""
read -p "按回车继续..." </dev/tty

# 测试 3: 深度分析
echo "🔍 测试 3: 深度分析单个商品"
echo "----------------------------------------"
node src/index.js analyze \
  '{"platform":"携程","title":"云南 6 日游纯玩团","price":3299,"rating":4.8,"shoppingStops":0,"hotelStars":4,"hotelStandard":"4 钻","selfPaidItems":[{"name":"索道","price":180},{"name":"电瓶车","price":50}],"days":6}' \
  --deep

echo ""
echo "✅ 测试 3 完成"
echo ""

# 测试 4: 帮助信息
echo "📖 测试 4: 查看帮助信息"
echo "----------------------------------------"
node src/index.js --help

echo ""
echo "========================================"
echo "✅ 所有测试完成！"
echo "========================================"
echo ""
echo "💡 提示:"
echo "  - 链接抓取功能需要安装：npm install puppeteer cheerio"
echo "  - 图片导出功能需要安装：npm install canvas"
echo "  - 更多示例见：examples/usage.md"
echo ""
