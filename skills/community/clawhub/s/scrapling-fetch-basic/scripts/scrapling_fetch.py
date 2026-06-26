#!/usr/bin/env python3
"""
Scrapling Fetch Basic - 基础网页抓取工具 v1.0.0

用法:
    python3 scrapling_fetch.py <url> [max_chars] [--mode basic|stealth] [--json] [--debug]

示例:
    python3 scrapling_fetch.py "https://example.com/article"
    python3 scrapling_fetch.py "https://example.com" 10000
    python3 scrapling_fetch.py "https://protected.com" --mode stealth
"""

import argparse
import json
import re
import sys
from typing import Tuple

# 基础版正文选择器优先级（11个）
CONTENT_SELECTORS = [
    "article",
    "main",
    ".post-content",
    ".article-content",
    ".entry-content",
    ".post-body",
    "[class*='body']",
    "[class*='content']",
    "#content",
    "#main",
    "body",
]


def fetch_basic(url: str, debug: bool = False) -> Tuple[str, str]:
    """
    基础 HTTP 抓取模式
    
    Returns:
        Tuple[html, selector]: 页面内容、命中的选择器
    """
    from scrapling.fetchers import Fetcher
    
    if debug:
        print(f"[DEBUG] 使用 Fetcher.get() 抓取: {url}", file=sys.stderr)
    
    page = Fetcher.get(url)
    html = page.html_content
    
    # 尝试选择器
    for selector in CONTENT_SELECTORS:
        try:
            elements = page.css(selector)
            if elements and len(elements) > 0:
                elem = elements[0]
                content = elem.get() if hasattr(elem, 'get') else str(elem)
                if content and len(content) > 500:
                    if debug:
                        print(f"[DEBUG] 命中选择器: {selector} (长度: {len(content)})", file=sys.stderr)
                    return content, selector
        except Exception as e:
            if debug:
                print(f"[DEBUG] 选择器 {selector} 失败: {e}", file=sys.stderr)
            continue
    
    if debug:
        print(f"[DEBUG] 未命中选择器，使用完整页面", file=sys.stderr)
    return html, "full_page"


def fetch_stealth(url: str, debug: bool = False) -> Tuple[str, str]:
    """
    隐身浏览器抓取模式（绕过反爬）
    
    Returns:
        Tuple[html, selector]: 页面内容、命中的选择器
    """
    from scrapling.fetchers import StealthyFetcher
    
    if debug:
        print(f"[DEBUG] 使用 StealthyFetcher 抓取: {url}", file=sys.stderr)
    
    try:
        page = StealthyFetcher.fetch(
            url,
            headless=True,
            network_idle=True,
            wait=3,
        )
    except Exception as e:
        if debug:
            print(f"[DEBUG] StealthyFetcher 失败: {e}，回退到 Fetcher", file=sys.stderr)
        return fetch_basic(url, debug)
    
    html = page.html_content
    
    # 尝试选择器
    for selector in CONTENT_SELECTORS:
        try:
            elements = page.css(selector)
            if elements and len(elements) > 0:
                elem = elements[0]
                content = elem.get() if hasattr(elem, 'get') else str(elem)
                if content and len(content) > 500:
                    if debug:
                        print(f"[DEBUG] 命中选择器: {selector} (长度: {len(content)})", file=sys.stderr)
                    return content, selector
        except Exception as e:
            if debug:
                print(f"[DEBUG] 选择器 {selector} 失败: {e}", file=sys.stderr)
            continue
    
    if debug:
        print(f"[DEBUG] 未命中有效选择器，使用完整页面", file=sys.stderr)
    return html, "full_page"


def html_to_markdown(html: str, base_url: str = "") -> str:
    """将 HTML 转换为 Markdown"""
    from html2text import HTML2Text
    
    h = HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0
    h.unicode_snob = True
    h.skip_internal_links = False
    
    if base_url:
        h.baseurl = base_url
    
    return h.handle(html)


def clean_content(text: str) -> str:
    """清理内容中的多余空行"""
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_title(html: str) -> str:
    """从 HTML 中提取标题"""
    from scrapling.fetchers import Fetcher
    
    try:
        page = Fetcher.parse(html)
        
        # 标准 title 标签
        title = page.css("title::text").get()
        if title:
            return title.strip()
        
        # h1 标签
        h1 = page.css("h1::text").get()
        if h1:
            return h1.strip()
    except:
        pass
    
    return ""


def main():
    parser = argparse.ArgumentParser(
        description="Scrapling Fetch Basic v1.0.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url", help="目标网页 URL")
    parser.add_argument("max_chars", nargs="?", type=int, default=30000,
                        help="最大输出字符数（默认: 30000）")
    parser.add_argument("--mode", choices=["basic", "stealth"], default="basic",
                        help="抓取模式: basic（快速）/ stealth（隐身，绕过反爬）")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--debug", action="store_true", help="显示调试信息")
    
    args = parser.parse_args()
    
    try:
        # 抓取页面
        if args.mode == "stealth":
            html, selector = fetch_stealth(args.url, args.debug)
        else:
            html, selector = fetch_basic(args.url, args.debug)
        
        # 提取标题
        title = extract_title(html)
        
        # 转换为 Markdown
        markdown = html_to_markdown(html, args.url)
        
        # 清理内容
        markdown = clean_content(markdown)
        
        # 截断
        original_len = len(markdown)
        truncated = len(markdown) > args.max_chars
        if truncated:
            markdown = markdown[:args.max_chars] + "\n\n... [内容已截断]"
        
        # 输出
        if args.json:
            result = {
                "url": args.url,
                "title": title,
                "content": markdown,
                "selector": selector,
                "length": original_len,
                "truncated": truncated,
                "mode": args.mode,
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if title:
                print(f"# {title}\n")
            print(markdown)
            
            if args.debug:
                print(f"\n---", file=sys.stderr)
                print(f"[DEBUG] 选择器: {selector}", file=sys.stderr)
                print(f"[DEBUG] 原始长度: {original_len}", file=sys.stderr)
                print(f"[DEBUG] 截断: {truncated}", file=sys.stderr)
    
    except Exception as e:
        if args.json:
            print(json.dumps({
                "error": str(e),
                "url": args.url,
            }, ensure_ascii=False))
        else:
            print(f"[error] fetch failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
