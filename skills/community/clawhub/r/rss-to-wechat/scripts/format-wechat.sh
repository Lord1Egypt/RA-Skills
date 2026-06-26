#!/bin/bash
# 格式化为微信公众号 HTML（内联样式，无外层标签）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# 使用方法
usage() {
  cat << EOF
用法: $0 <文章JSON> <输出文件>

参数:
  <文章JSON>   parse-article.sh 输出的 JSON 文件
  <输出文件>   输出的 HTML 文件路径

示例:
  $0 article.json output.html
EOF
  exit 1
}

if [ $# -lt 2 ]; then
  usage
fi

ARTICLE_JSON="$1"
OUTPUT_HTML="$2"

if [ ! -f "$ARTICLE_JSON" ]; then
  error "文章 JSON 文件不存在: $ARTICLE_JSON"
  exit 1
fi

log "格式化为公众号 HTML..."

# 读取文章数据
TITLE=$(jq -r '.title' "$ARTICLE_JSON")
AUTHOR=$(jq -r '.author' "$ARTICLE_JSON")
PUBLISHED=$(jq -r '.published' "$ARTICLE_JSON")
CONTENT=$(jq -r '.content' "$ARTICLE_JSON")
URL=$(jq -r '.url' "$ARTICLE_JSON")

# 转换 Markdown 为 HTML
CONTENT_HTML=$(echo "$CONTENT" | pandoc -f markdown -t html)

# 获取当前日期和星期
CURRENT_DATE=$(TZ=Asia/Shanghai date "+%Y年%m月%d日 星期%u" | sed 's/星期1/星期一/;s/星期2/星期二/;s/星期3/星期三/;s/星期4/星期四/;s/星期5/星期五/;s/星期6/星期六/;s/星期7/星期日/')

# 生成微信公众号兼容的 HTML（纯 section 标签 + 内联样式）
cat > "$OUTPUT_HTML" << EOF
<section style="background:#f5f5f0;padding:20px 15px;">

<!-- 头部品牌 Logo -->
<section style="background:#c41e3a;padding:20px 25px;margin-bottom:15px;border-radius:10px;text-align:center;">
<p style="display:flex;align-items:center;justify-content:center;gap:15px;margin-bottom:8px;">
<svg width="50" height="50" viewBox="0 0 140 140" style="display:inline-block;">
<circle cx="70" cy="70" r="70" fill="rgba(255,255,255,0.15)"/>
<path d="M40 110 L70 20 L100 110 M48 85 L92 85" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="70" cy="25" r="6" fill="#fff"/>
<line x1="70" y1="40" x2="70" y2="110" stroke="#fff" stroke-width="8" stroke-linecap="round"/>
</svg>
<span style="font-size:32px;font-weight:900;color:#fff;letter-spacing:4px;">AI晚知道</span>
</p>
<p style="font-size:13px;color:rgba(255,255,255,0.85);font-style:italic;font-family:Georgia,serif;">"All the AI News That's Fit to Read"</p>
</section>

<!-- 日期栏 -->
<section style="background:#fff;padding:15px 20px;margin-bottom:15px;box-shadow:0 1px 3px rgba(0,0,0,0.1);text-align:center;">
<p style="font-size:14px;color:#666;border-bottom:1px solid #eee;padding-bottom:10px;">$CURRENT_DATE</p>
<p style="font-size:12px;color:#999;margin-top:8px;">精选</p>
</section>

<!-- 标题 -->
<section style="background:#fff;padding:25px 20px;margin-bottom:15px;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
<p style="font-size:24px;font-weight:bold;color:#c41e3a;line-height:1.4;margin-bottom:12px;">$TITLE</p>
<p style="font-size:13px;color:#999;">来源：$AUTHOR | 发布时间：$PUBLISHED</p>
</section>

<!-- 文章内容 -->
<section style="background:#fff;padding:20px;margin-bottom:15px;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
EOF

# 将 Markdown HTML 转换为内联样式，并移除不兼容的元素
echo "$CONTENT_HTML" | sed \
  -e 's|<h1[^>]*>|<p style="font-size:22px;font-weight:bold;color:#1a1a1a;margin:20px 0 12px 0;">|g' \
  -e 's|</h1>|</p>|g' \
  -e 's|<h2[^>]*>|<p style="font-size:20px;font-weight:bold;color:#c41e3a;margin:18px 0 10px 0;">|g' \
  -e 's|</h2>|</p>|g' \
  -e 's|<h3[^>]*>|<p style="font-size:18px;font-weight:bold;color:#555;margin:16px 0 8px 0;">|g' \
  -e 's|</h3>|</p>|g' \
  -e 's|<p[^>]*>|<p style="font-size:14px;color:#444;line-height:1.8;margin-bottom:12px;">|g' \
  -e 's|<blockquote>|<section style="border-left:3px solid #c41e3a;padding-left:12px;margin:15px 0;color:#666;font-style:italic;">|g' \
  -e 's|</blockquote>|</section>|g' \
  -e 's|<code>|<span style="background:#f5f5f5;padding:2px 6px;border-radius:3px;font-family:monospace;font-size:13px;">|g' \
  -e 's|</code>|</span>|g' \
  -e 's|<pre>|<section style="background:#f5f5f5;padding:12px;border-radius:4px;overflow-x:auto;margin:12px 0;">|g' \
  -e 's|</pre>|</section>|g' \
  -e 's|<ul>|<section style="margin:10px 0;padding-left:20px;">|g' \
  -e 's|</ul>|</section>|g' \
  -e 's|<ol>|<section style="margin:10px 0;padding-left:20px;">|g' \
  -e 's|</ol>|</section>|g' \
  -e 's|<li>|<p style="font-size:14px;color:#444;line-height:1.8;margin-bottom:8px;">• |g' \
  -e 's|</li>|</p>|g' \
  -e 's|<strong>|<span style="font-weight:bold;color:#1a1a1a;">|g' \
  -e 's|</strong>|</span>|g' \
  -e 's|<em>|<span style="font-style:italic;color:#666;">|g' \
  -e 's|</em>|</span>|g' \
  -e 's|<a href="[^"]*">||g' \
  -e 's|</a>||g' \
  -e 's|<div[^>]*>||g' \
  -e 's|</div>||g' \
  >> "$OUTPUT_HTML"

cat >> "$OUTPUT_HTML" << EOF
</section>

<!-- 原文链接 -->
<section style="background:#fff;padding:15px 20px;margin-bottom:15px;box-shadow:0 1px 3px rgba(0,0,0,0.1);text-align:center;">
<p style="font-size:12px;color:#999;">原文链接</p>
<p style="font-size:11px;color:#1a5fb4;word-break:break-all;margin-top:5px;">$URL</p>
</section>

</section>
EOF

log "HTML 生成完成: $OUTPUT_HTML"
