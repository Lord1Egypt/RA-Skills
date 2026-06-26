#!/bin/bash
# 微信公众号文章阅读脚本
# 用法: ./read_article.sh "<文章URL>" <输出目录>

set -e

URL="$1"
OUTPUT_DIR="${2:-./wechat-article}"

if [ -z "$URL" ]; then
    echo "用法: $0 \"<文章URL>\" [输出目录]"
    exit 1
fi

echo "=== 微信公众号文章阅读器 ==="
echo "URL: $URL"
echo "输出: $OUTPUT_DIR"
echo ""

# 创建输出目录
mkdir -p "$OUTPUT_DIR/images"

# 1. 打开文章
echo "[1/5] 打开文章..."
agent-browser open "$URL" --timeout 30000

# 2. 滚动加载
echo "[2/5] 滚动加载所有内容..."
for i in {1..8}; do
    agent-browser scroll down 800 2>/dev/null || true
    sleep 1
done

# 3. 提取文章内容
echo "[3/5] 提取文章内容..."
agent-browser eval "
const title = document.querySelector('#activity-name')?.innerText || '未找到标题';
const author = document.querySelector('#js_name')?.innerText || '';
const content = document.querySelector('#js_content')?.innerText || '';
JSON.stringify({title, author, content, contentLength: content.length});
" 2>&1 | tail -1 > "$OUTPUT_DIR/article.json"

# 4. 提取图片URL
echo "[4/5] 提取图片URL..."
agent-browser eval "
const imgs = document.querySelectorAll('img');
const urls = [];
imgs.forEach((img) => {
  const dataSrc = img.getAttribute('data-src');
  const w = img.width;
  const h = img.height;
  if (dataSrc && dataSrc.startsWith('http') && (w > 200 || h > 200)) {
    urls.push(dataSrc.split('#')[0]);
  }
});
urls.join('\\n');
" 2>&1 | tail -1 > "$OUTPUT_DIR/image_urls.txt"

# 5. 下载图片
echo "[5/5] 下载内容图片..."
count=0
while IFS= read -r url; do
    if [ -n "$url" ] && [[ "$url" == http* ]]; then
        count=$((count + 1))
        ext="jpg"
        if [[ "$url" == *wx_fmt=png* ]]; then ext="png"; fi
        if [[ "$url" == *wx_fmt=gif* ]]; then ext="gif"; fi
        if [[ "$url" == *wx_fmt=webp* ]]; then ext="webp"; fi
        
        filename=$(printf "img-%02d.%s" $count $ext)
        echo "  下载: $filename"
        curl -s -o "$OUTPUT_DIR/images/$filename" "$url" || true
    fi
done < "$OUTPUT_DIR/image_urls.txt"

# 完成
echo ""
echo "=== 完成 ==="
echo "文章内容: $OUTPUT_DIR/article.json"
echo "图片目录: $OUTPUT_DIR/images/"
echo "图片数量: $(ls -1 "$OUTPUT_DIR/images/" 2>/dev/null | wc -l)"