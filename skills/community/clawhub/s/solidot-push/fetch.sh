#!/bin/bash
#
# Solidot 资讯推送脚本
# 抓取热门文章和最新文章，推送到飞书文档
#

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${WORKSPACE:-$(cd "$SKILL_DIR/../.." && pwd)}"

# 环境变量
FEISHU_APP_ID="${FEISHU_APP_ID:-}"
FEISHU_APP_SECRET="${FEISHU_APP_SECRET:-}"
FEISHU_DOC_TOKEN="${FEISHU_DOC_TOKEN:-}"

echo "🕐 $(date '+%Y-%m-%d %H:%M:%S') - 开始抓取 Solidot 资讯"

# 检查浏览器是否运行
BROWSER_STATUS=$(openclaw browser status 2>&1 | grep -c "running: true" || echo "0")
if [ "$BROWSER_STATUS" = "0" ]; then
    echo "📱 启动浏览器..."
    openclaw browser start
    sleep 3
fi

# 导航到 solidot
echo "📥 导航到 solidot.org..."
openclaw browser navigate "https://www.solidot.org/" > /dev/null 2>&1
sleep 5

# 获取文章列表
echo "📰 获取文章列表..."
ARTICLES_JSON=$(openclaw browser evaluate --fn "() => {
  const articles = [];
  const links = document.querySelectorAll('a[href^=\"/story?sid=\"]');
  const seen = new Set();
  links.forEach((link) => {
    const title = link.textContent.trim();
    const href = link.getAttribute('href');
    // 跳过评论链接和重复
    if (title && !href.includes('#comment') && !seen.has(title)) {
      seen.add(title);
      articles.push({
        title: title,
        url: 'https://www.solidot.org' + href
      });
    }
  });
  return articles.slice(0, 15);
}" 2>/dev/null)

if [ -z "$ARTICLES_JSON" ] || [ "$ARTICLES_JSON" = "null" ]; then
    echo "❌ 无法获取文章列表"
    exit 1
fi

echo "✅ 获取到文章列表"

# 提取文章标题
ARTICLES=$(echo "$ARTICLES_JSON" | grep -oP '"title":\s*"\K[^"]+' | head -15)

# 生成飞书文档内容
NOW=$(date '+%Y-%m-%d %H:%M')
CONTENT="# Solidot 资讯推送 ($NOW)\n\n"
CONTENT+="## 🔥 热门/最新文章\n\n"

count=1
while IFS= read -r title; do
    if [ -n "$title" ]; then
        url=$(echo "$ARTICLES_JSON" | grep -A1 "\"title\": \"$title\"" | grep -oP '"url":\s*"\K[^"]+')
        CONTENT+="$count. [$title]($url)\n"
        count=$((count + 1))
    fi
done <<< "$ARTICLES"

CONTENT+="\n---\n"
CONTENT+="来源: [Solidot](https://www.solidot.org/)\n"

echo "📤 推送内容已准备好"

# 推送到飞书
if [ -n "$FEISHU_DOC_TOKEN" ]; then
    # 写入飞书文档
    echo "$CONTENT" | feishu_doc write --doc_token "$FEISHU_DOC_TOKEN" --content "$(echo "$CONTENT")" 2>/dev/null || true
    echo "✅ 已推送到飞书文档"
else
    # 没有配置飞书时，保存到本地
    echo "$CONTENT" > "$WORKSPACE/solidot-push.md"
    echo "📄 已保存到 $WORKSPACE/solidot-push.md"
    echo ""
    echo "=== 推送内容预览 ==="
    cat "$WORKSPACE/solidot-push.md"
fi

echo "✅ 完成!"
