#!/usr/bin/env python3
"""
Scrapling Fetch - 高质量网页抓取工具 v1.1

用法:
    python3 scrapling_fetch.py <url> [max_chars] [--mode basic|stealth|auto] [--json] [--debug]

示例:
    python3 scrapling_fetch.py "https://example.com/article"
    python3 scrapling_fetch.py "https://example.com" 10000
    python3 scrapling_fetch.py "https://mp.weixin.qq.com/xxx" --mode auto
    python3 scrapling_fetch.py "https://protected.com" --mode stealth
"""

import argparse
import json
import re
import sys
from typing import Tuple, List

# 正文选择器优先级
CONTENT_SELECTORS = [
    "#js_content",           # 微信公众号正文
    ".rich_media_content",   # 微信公众号备选
    "article",
    "main",
    ".post-content",
    ".article-content",
    ".entry-content",
    ".post-body",
    ".content-body",
    "[class*='body']",
    "[class*='content']",
    "[class*='article']",
    "#content",
    "#main",
    ".content",
    "body",
]

# 微信公众号噪音选择器（需要移除的内容）
WECHAT_NOISE_SELECTORS = [
    "#js_a_preview_popular",
    "#js_a_bottom_ad",
    ".rich_media_tool",
    ".rich_media_area_extra",
    ".rich_media_areas",
    "#js_name",
    ".rich_media_meta_nickname",
    "#js_cpc_area",
    ".js_understand_content",
]

# 需要使用 stealth 模式的域名
STEALTH_DOMAINS = [
    "mp.weixin.qq.com",
    "cloudflare.com",
]


def is_wechat_url(url: str) -> bool:
    """检测是否为微信文章"""
    return "mp.weixin.qq.com" in url


def needs_stealth_mode(url: str) -> bool:
    """检测是否需要使用 stealth 模式"""
    for domain in STEALTH_DOMAINS:
        if domain in url:
            return True
    return False


def clean_wechat_noise(html: str) -> str:
    """清理微信公众号噪音内容"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        
        # 移除噪音元素
        for selector in WECHAT_NOISE_SELECTORS:
            for element in soup.select(selector):
                element.decompose()
        
        return str(soup)
    except Exception:
        return html


def clean_content(text: str) -> str:
    """清理内容中的噪音"""
    # 移除多余的空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 移除微信相关的噪音文字
    noise_patterns = [
        r'继续滑动看下一个',
        r'轻触阅读原文',
        r'扫描二维码关注',
        r'微信扫一扫可打开此内容',
        r'使用完整服务',
        r'预览时标签不可点',
    ]
    for pattern in noise_patterns:
        text = re.sub(pattern, '', text)
    return text.strip()


def fetch_basic(url: str, debug: bool = False) -> Tuple[str, str, bool]:
    """
    基础 HTTP 抓取模式
    
    Returns:
        Tuple[html, selector, is_wechat]: 页面 HTML、命中的选择器、是否微信文章
    """
    from scrapling.fetchers import Fetcher
    
    if debug:
        print(f"[DEBUG] 使用 Fetcher.get() 抓取: {url}", file=sys.stderr)
    
    page = Fetcher.get(url)
    html = page.html_content
    is_wechat = is_wechat_url(url)
    
    # 微信文章特殊处理
    if is_wechat:
        html = clean_wechat_noise(html)
    
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
                    return content, selector, is_wechat
        except Exception as e:
            if debug:
                print(f"[DEBUG] 选择器 {selector} 失败: {e}", file=sys.stderr)
            continue
    
    if debug:
        print(f"[DEBUG] 未命中选择器，使用完整页面", file=sys.stderr)
    return html, "full_page", is_wechat


def fetch_stealth(url: str, debug: bool = False) -> Tuple[str, str, bool]:
    """
    隐身浏览器抓取模式（绕过反爬）
    
    Returns:
        Tuple[html, selector, is_wechat]: 页面 HTML、命中的选择器、是否微信文章
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
    is_wechat = is_wechat_url(url)
    
    # 微信文章特殊处理
    if is_wechat:
        html = clean_wechat_noise(html)
    
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
                    return content, selector, is_wechat
        except Exception as e:
            if debug:
                print(f"[DEBUG] 选择器 {selector} 失败: {e}", file=sys.stderr)
            continue
    
    if debug:
        print(f"[DEBUG] 未命中有效选择器，使用完整页面", file=sys.stderr)
    return html, "full_page", is_wechat


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


def extract_title(html: str) -> str:
    """从 HTML 中提取标题"""
    from scrapling.fetchers import Fetcher
    
    try:
        page = Fetcher.parse(html)
        
        # 微信公众号标题
        title = page.css("#activity-name::text").get()
        if title:
            return title.strip()
        
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
        description="高质量网页抓取工具 v1.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url", help="目标网页 URL")
    parser.add_argument("max_chars", nargs="?", type=int, default=30000,
                        help="最大输出字符数（默认: 30000）")
    parser.add_argument("--mode", choices=["basic", "stealth", "auto"], default="auto",
                        help="抓取模式: basic（快速）/ stealth（隐身）/ auto（自动检测）")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--debug", action="store_true", help="显示调试信息")
    
    args = parser.parse_args()
    
    # 确定抓取模式
    if args.mode == "auto":
        mode = "stealth" if needs_stealth_mode(args.url) else "basic"
        if args.debug:
            print(f"[DEBUG] 自动选择模式: {mode}", file=sys.stderr)
    else:
        mode = args.mode
    
    try:
        # 抓取页面
        if mode == "stealth":
            html, selector, is_wechat = fetch_stealth(args.url, args.debug)
        else:
            html, selector, is_wechat = fetch_basic(args.url, args.debug)
        
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
                "mode": mode,
                "is_wechat": is_wechat,
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
                print(f"[DEBUG] 微信文章: {is_wechat}", file=sys.stderr)
    
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
