#!/bin/bash
# 测试 RSS to WeChat Skill

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== RSS to WeChat Skill 测试 ==="
echo ""

# 1. 检查依赖
echo "1. 检查依赖..."
echo -n "  blogwatcher: "
if command -v blogwatcher &> /dev/null; then
  echo "✅"
else
  echo "❌ 未安装"
fi

echo -n "  curl: "
if command -v curl &> /dev/null; then
  echo "✅"
else
  echo "❌ 未安装"
fi

echo -n "  jq: "
if command -v jq &> /dev/null; then
  echo "✅"
else
  echo "❌ 未安装"
fi

echo -n "  pandoc: "
if command -v pandoc &> /dev/null; then
  echo "✅"
else
  echo "❌ 未安装"
fi

echo ""

# 2. 检查配置文件
echo "2. 检查配置文件..."
if [ -f "$SCRIPT_DIR/config.sh" ]; then
  echo "  ✅ config.sh"
else
  echo "  ❌ config.sh 不存在"
fi

echo ""

# 3. 检查脚本文件
echo "3. 检查脚本文件..."
for script in fetch-rss.sh parse-article.sh format-wechat.sh publish-article.sh daily-featured.sh; do
  if [ -f "$SCRIPT_DIR/$script" ] && [ -x "$SCRIPT_DIR/$script" ]; then
    echo "  ✅ $script"
  else
    echo "  ❌ $script (不存在或无执行权限)"
  fi
done

echo ""

# 4. 检查依赖 skills
echo "4. 检查依赖 skills..."
echo -n "  wechat-cover: "
if [ -f "$HOME/clawd/skills/wechat-cover/generate-cover.sh" ]; then
  echo "✅"
else
  echo "❌"
fi

echo -n "  wechat-publish: "
if [ -f "$HOME/clawd/scripts/wechat-publish.sh" ]; then
  echo "✅"
else
  echo "❌"
fi

echo ""

# 5. 测试示例
echo "5. 测试示例..."
echo ""
echo "获取新文章:"
echo "  bash $SCRIPT_DIR/fetch-rss.sh"
echo ""
echo "发布文章:"
echo "  bash $SCRIPT_DIR/publish-article.sh 'https://simonwillison.net/...'"
echo ""
echo "每日精选:"
echo "  bash $SCRIPT_DIR/daily-featured.sh"
echo ""

echo "=== 测试完成 ==="
