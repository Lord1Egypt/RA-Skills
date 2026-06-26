#!/usr/bin/env python3
"""读取微信公众号文章，输出结构化文本。

用法：
    python3 read_wechat.py <url> [--json]

参数：
    url     微信公众号文章链接（mp.weixin.qq.com/s/xxx）
    --json  输出 JSON 格式（默认输出可读文本）
"""

import sys
import re
import json
import html as htmlmod
import datetime
import urllib.request

def fetch_article(url: str) -> dict:
    """抓取并解析微信公众号文章，返回结构化数据。"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        page = resp.read().decode("utf-8", errors="replace")

    result = {"url": url, "title": None, "author": None, "pub_time": None, "content": None}

    # 标题：尝试多种匹配
    for pattern in [
        r"var msg_title = '([^']+)'",
        r'var msg_title = "([^"]+)"',
        r'<h1[^>]*class="rich_media_title"[^>]*>(.*?)</h1>',
        r'<meta property="og:title" content="(.*?)"',
    ]:
        m = re.search(pattern, page, re.DOTALL)
        if m:
            title_raw = m.group(1).strip()
            # 清理可能混入的 JS 代码
            title_raw = re.split(r"['\"];\s*var ", title_raw)[0]
            result["title"] = htmlmod.unescape(re.sub(r"<[^>]+>", "", title_raw).strip())
            break

    # 公众号名称
    for pattern in [
        r"var nickname = '([^']+)'",
        r'var nickname = "([^"]+)"',
        r'<a[^>]*id="js_name"[^>]*>(.*?)</a>',
    ]:
        m = re.search(pattern, page, re.DOTALL)
        if m:
            result["author"] = htmlmod.unescape(re.sub(r"<[^>]+>", "", m.group(1)).strip())
            break

    # 发布时间
    m = re.search(r'var ct = "(\d+)"', page)
    if m:
        ts = int(m.group(1))
        dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone(datetime.timedelta(hours=8)))
        result["pub_time"] = dt.strftime("%Y-%m-%d %H:%M")

    # 正文
    content_match = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*<script', page, re.DOTALL)
    if not content_match:
        content_match = re.search(r'id="js_content"[^>]*>(.*?)<!--\s*end\s*-->', page, re.DOTALL)
    if not content_match:
        content_match = re.search(r'id="js_content"[^>]*>(.*?)$', page, re.DOTALL)

    if content_match:
        text = content_match.group(1)
        # 转换常见 HTML 为换行
        text = re.sub(r"<br\s*/?>", "\n", text)
        text = re.sub(r"<p[^>]*>", "\n", text)
        text = re.sub(r"</p>", "", text)
        text = re.sub(r"<h[1-6][^>]*>", "\n\n## ", text)
        text = re.sub(r"</h[1-6]>", "\n", text)
        text = re.sub(r"<li[^>]*>", "\n- ", text)
        # 提取图片 alt/src
        text = re.sub(r'<img[^>]*data-src="([^"]*)"[^>]*/?>',
                       lambda m: f'\n[图片: {m.group(1)}]\n', text)
        # 去除剩余标签
        text = re.sub(r"<[^>]+>", "", text)
        text = htmlmod.unescape(text)
        # 清理空白
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        result["content"] = text.strip()

    return result


def format_text(article: dict) -> str:
    """格式化为可读文本。"""
    lines = []
    if article["title"]:
        lines.append(f"📄 {article['title']}")
    if article["author"]:
        lines.append(f"📝 公众号：{article['author']}")
    if article["pub_time"]:
        lines.append(f"🕐 发布时间：{article['pub_time']}")
    lines.append(f"🔗 {article['url']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    if article["content"]:
        lines.append(article["content"])
    else:
        lines.append("⚠️ 未能提取正文内容（可能需要JS渲染或文章已被删除）")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 read_wechat.py <url> [--json]")
        sys.exit(1)

    url = sys.argv[1]
    use_json = "--json" in sys.argv

    if "mp.weixin.qq.com" not in url:
        print("⚠️ 不是微信公众号文章链接，请提供 mp.weixin.qq.com/s/xxx 格式的链接")
        sys.exit(1)

    try:
        article = fetch_article(url)
        if use_json:
            print(json.dumps(article, ensure_ascii=False, indent=2))
        else:
            print(format_text(article))
    except Exception as e:
        print(f"❌ 读取失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
