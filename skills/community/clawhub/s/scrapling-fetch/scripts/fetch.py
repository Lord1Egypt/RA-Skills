#!/usr/bin/env python3
"""
Scrapling Fetch - 智能网页内容抓取工具
支持绕过反爬机制（微信、Medium、Cloudflare等）
"""
import sys
import json
import argparse
from urllib.parse import urlparse

VENV_PYTHON = "/Users/gaolei/.openclaw/workspace/.venv/bin/python3"

def is_wechat_url(url: str) -> bool:
    """检测是否为微信公众号链接"""
    return "mp.weixin.qq.com" in url

def is_antibot_site(url: str) -> bool:
    """检测是否为已知反爬网站"""
    antibot_domains = [
        "medium.com",
        "substack.com",
        "zhihu.com",
        "cloudflare.com"
    ]
    domain = urlparse(url).netloc.lower()
    return any(d in domain for d in antibot_domains)

def fetch_with_scrapling(url: str, max_chars: int = 50000) -> dict:
    """使用 Scrapling 抓取（绕过反爬）"""
    import subprocess
    
    code = f"""
from scrapling.fetchers import StealthyFetcher
import json

url = "{url}"
page = StealthyFetcher.fetch(url, headless=True, network_idle=True)

# 提取标题
title = page.css('h1::text').get()
if not title:
    title = page.css('meta[property="og:title"]::attr(content)').get()
if not title:
    title = page.css('title::text').get()

# 提取作者
author = page.css('meta[name="author"]::attr(content)').get()
if not author:
    author = page.css('[rel="author"]::text').get()

# 提取正文（兼容多种网站结构）
content_selectors = [
    'div.rich_media_content',  # 微信
    'article',  # 通用博客
    'div.post-content',  # Substack
    'main',  # 语义化标签
    'body'  # 最后兜底
]

content = None
for selector in content_selectors:
    elem = page.css(selector)
    if elem:
        # 获取所有段落
        paragraphs = elem.css('p, section, div')
        texts = []
        for p in paragraphs:
            text = p.css('::text').get()
            if text and text.strip():
                texts.append(text.strip())
        if texts:
            content = '\\n\\n'.join(texts)
            break

# 如果都没找到，获取全页文本
if not content:
    content = page.css('body::text').get()

result = {{
    'title': title.strip() if title else '未找到标题',
    'author': author.strip() if author else '未知作者',
    'content': content[:50000] if content else '',
    'word_count': len(content) if content else 0,
    'fetcher': 'scrapling',
    'url': url
}}

print(json.dumps(result, ensure_ascii=False))
"""
    
    result = subprocess.run(
        [VENV_PYTHON, "-c", code],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode != 0:
        return {
            "error": result.stderr,
            "fetcher": "scrapling",
            "url": url
        }
    
    return json.loads(result.stdout)

def fetch_with_jina(url: str, max_chars: int = 50000) -> dict:
    """使用 Jina Reader 快速抓取（适合普通网页）"""
    import urllib.request
    import urllib.error
    
    jina_url = f"https://r.jina.ai/{url}"
    
    try:
        req = urllib.request.Request(
            jina_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            
        # Jina 返回 Markdown，尝试提取标题
        lines = content.split('\n')
        title = '未知标题'
        for line in lines[:10]:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        return {
            'title': title,
            'author': '未知',
            'content': content[:max_chars],
            'word_count': len(content),
            'fetcher': 'jina',
            'url': url
        }
    except Exception as e:
        return {
            "error": str(e),
            "fetcher": "jina",
            "url": url
        }

def main():
    parser = argparse.ArgumentParser(description='智能网页内容抓取')
    parser.add_argument('url', help='目标网址')
    parser.add_argument('--fast', action='store_true', help='使用 Jina Reader（速度快）')
    parser.add_argument('--text', action='store_true', help='只输出纯文本')
    parser.add_argument('--max-chars', type=int, default=50000, help='最大字符数')
    
    args = parser.parse_args()
    
    # 选择抓取方式
    if args.fast:
        result = fetch_with_jina(args.url, args.max_chars)
    elif is_wechat_url(args.url) or is_antibot_site(args.url):
        # 反爬网站用 Scrapling
        result = fetch_with_scrapling(args.url, args.max_chars)
    else:
        # 普通网站先尝试 Jina（快）
        result = fetch_with_jina(args.url, args.max_chars)
        if 'error' in result:
            # Jina 失败，切换 Scrapling
            result = fetch_with_scrapling(args.url, args.max_chars)
    
    # 输出
    if args.text:
        print(result.get('content', result.get('error', '未知错误')))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
