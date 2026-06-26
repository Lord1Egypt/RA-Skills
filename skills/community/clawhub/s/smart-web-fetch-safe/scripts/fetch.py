#!/usr/bin/env python3
"""
Smart Web Fetch Safe - 安全版网页内容获取
- 本地解析优先，隐私安全
- 可选远程清洗，Token 优化更强
"""

import sys
import os
import json
import re
import argparse
from urllib.parse import urlparse

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

import requests

# 默认配置
DEFAULT_MAX_CHARS = int(os.getenv("MAX_CHARS", "10000"))
DEFAULT_MODE = os.getenv("DEFAULT_MODE", "local")
ALLOWED_DOMAINS = os.getenv("ALLOWED_DOMAINS", "")

# 远程清洗服务
JINA_READER_URL = "https://r.jina.ai/http://{url}"
MARKDOWN_NEW_URL = "https://markdown.new/{url}"


def is_domain_allowed(url: str) -> bool:
    """检查域名是否在白名单中"""
    if not ALLOWED_DOMAINS:
        return True  # 未配置白名单，允许所有
    
    parsed = urlparse(url)
    allowed = [d.strip() for d in ALLOWED_DOMAINS.split(",")]
    return parsed.netloc in allowed or any(parsed.netloc.endswith("." + d) for d in allowed)


def clean_html_local(html: str, max_chars: int = DEFAULT_MAX_CHARS) -> str:
    """本地 HTML 解析清洗"""
    if not BS4_AVAILABLE:
        print("Warning: beautifulsoup4 not installed, using basic cleaning", file=sys.stderr)
        return basic_clean(html, max_chars)
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 移除脚本和样式
    for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']):
        tag.decompose()
    
    # 获取主要内容区域
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|article|post|entry')) or soup.body
    
    if main_content:
        text = main_content.get_text(separator='\n', strip=True)
    else:
        text = soup.get_text(separator='\n', strip=True)
    
    # 清理多余空白
    lines = [line.strip() for line in text.split('\n')]
    lines = [line for line in lines if line]
    text = '\n'.join(lines)
    
    # 截断
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n... [内容已截断]"
    
    return text


def basic_clean(html: str, max_chars: int = DEFAULT_MAX_CHARS) -> str:
    """基础 HTML 清洗（无 beautifulsoup4 时使用）"""
    # 移除脚本
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', '', html)
    
    # 解码 HTML 实体
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    
    # 清理空白
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()
    
    # 截断
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n... [内容已截断]"
    
    return text


def fetch_remote(url: str, max_chars: int = DEFAULT_MAX_CHARS) -> dict:
    """远程清洗模式（使用 Jina Reader）"""
    try:
        # 移除协议前缀
        clean_url = url.replace("https://", "").replace("http://", "")
        jina_url = JINA_READER_URL.format(url=clean_url)
        
        response = requests.get(jina_url, timeout=30)
        response.raise_for_status()
        
        content = response.text
        
        # 截断
        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n... [内容已截断]"
        
        return {
            "success": True,
            "url": url,
            "content": content,
            "source": "jina",
            "mode": "remote",
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "content": None,
            "source": "jina",
            "mode": "remote",
            "error": str(e)
        }


def fetch_local(url: str, max_chars: int = DEFAULT_MAX_CHARS) -> dict:
    """本地解析模式"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        content = clean_html_local(response.text, max_chars)
        
        return {
            "success": True,
            "url": url,
            "content": content,
            "source": "local",
            "mode": "local",
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "content": None,
            "source": "local",
            "mode": "local",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Smart Web Fetch Safe')
    parser.add_argument('url', help='URL to fetch')
    parser.add_argument('--remote', action='store_true', help='Use remote cleaning (Jina Reader)')
    parser.add_argument('--local', action='store_true', help='Use local parsing (default)')
    parser.add_argument('--max-chars', type=int, default=DEFAULT_MAX_CHARS, help='Max characters to return')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    parser.add_argument('--allow', type=str, help='Override allowed domains (comma-separated)')
    
    args = parser.parse_args()
    url = args.url
    
    # 域名检查
    global ALLOWED_DOMAINS
    if args.allow:
        ALLOWED_DOMAINS = args.allow
    
    if not is_domain_allowed(url):
        result = {
            "success": False,
            "url": url,
            "content": None,
            "error": f"Domain not allowed. Allowed: {ALLOWED_DOMAINS or 'all'}"
        }
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(result["error"], file=sys.stderr)
        sys.exit(1)
    
    # 选择模式
    use_remote = args.remote or (DEFAULT_MODE == "remote" and not args.local)
    
    if use_remote:
        result = fetch_remote(url, args.max_chars)
        # 如果远程失败，尝试降级到本地
        if not result["success"]:
            print(f"Remote fetch failed: {result['error']}, falling back to local...", file=sys.stderr)
            result = fetch_local(url, args.max_chars)
    else:
        result = fetch_local(url, args.max_chars)
    
    # 输出
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result["success"]:
            print(result["content"])
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
