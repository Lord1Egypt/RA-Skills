#!/usr/bin/env python3
"""
微信公众号文章读取工具
用于解析和提取微信公众号链接的内容
"""

import argparse
import json
import re
import sys
from pathlib import Path

# 尝试导入可选依赖
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


def parse_wechat_url(url: str) -> dict:
    """
    解析微信 URL，提取关键信息

    Args:
        url: 微信公众号文章链接

    Returns:
        包含 URL 信息的字典
    """
    # 微信文章 URL 模式
    patterns = [
        r'https?://mp\.weixin\.qq\.com/s/([a-zA-Z0-9_-]+)',  # 直接文章 ID
        r'https?://mp\.weixin\.qq\.com/s\?([a-zA-Z0-9&=_-]+)',  # 带参数的 URL
        r'https?://mp\.weixin\.qq\.com/profile/([a-zA-Z0-9_-]+)',  # 公众号主页
    ]

    result = {
        "original_url": url,
        "type": "unknown",
        "article_id": None,
        "params": {}
    }

    # 提取文章 ID
    match = re.search(r'/s/([a-zA-Z0-9_-]+)', url)
    if match:
        result["type"] = "article"
        result["article_id"] = match.group(1)

    # 提取 URL 参数
    if '?' in url:
        query_string = url.split('?')[1]
        params = {}
        for param in query_string.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                params[key] = value
        result["params"] = params

    return result


def fetch_article_with_playwright(url: str) -> dict:
    """
    使用 Playwright 浏览器模拟访问微信文章

    Args:
        url: 微信公众号文章链接

    Returns:
        包含文章内容的字典
    """
    if not PLAYWRIGHT_AVAILABLE:
        return {
            "success": False,
            "error": "Playwright not installed. Run: pip install playwright && playwright install chromium"
        }

    result = {
        "success": False,
        "url": url,
        "title": None,
        "content": None,
        "author": None,
        "publish_date": None,
        "source": None,
        "error": None
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 设置更真实的浏览器环境
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })

            page.goto(url, wait_until="networkidle", timeout=30000)

            # 等待页面加载完成
            page.wait_for_timeout(3000)

            # 提取标题
            title_element = page.query_selector('#activity-name, .article_title, h1')
            if title_element:
                result["title"] = title_element.inner_text().strip()

            # 提取公众号来源 (作者和来源在同一区域)
            meta_elements = page.query_selector_all('.rich_media_meta')
            for el in meta_elements:
                text = el.inner_text().strip()
                if text:
                    # 判断是日期还是来源
                    if '年' in text and '月' in text:
                        result["publish_date"] = text
                    elif not result["source"]:
                        result["source"] = text

            # 提取作者（有时单独显示）
            author_element = page.query_selector('#js_author, .author_name, .author')
            if author_element:
                result["author"] = author_element.inner_text().strip()
            # 如果没有作者，用来源作为作者
            if not result["author"] and result["source"]:
                result["author"] = result["source"]

            # 提取发布时间（备选方案）
            if not result["publish_date"]:
                date_element = page.query_selector('#js_publish_time, .publish_time, .date')
                if date_element:
                    result["publish_date"] = date_element.inner_text().strip()

            # 提取文章内容
            content_element = page.query_selector('#js_content, .article_content, .content')
            if content_element:
                result["content"] = content_element.inner_text().strip()

            if result["title"] or result["content"]:
                result["success"] = True

            browser.close()

    except Exception as e:
        result["error"] = str(e)

    return result


def fetch_article_with_requests(url: str) -> dict:
    """
    使用 requests 直接请求微信文章（可能受防盗链限制）

    Args:
        url: 微信公众号文章链接

    Returns:
        包含文章内容的字典
    """
    if not REQUESTS_AVAILABLE:
        return {
            "success": False,
            "error": "requests not installed. Run: pip install requests"
        }

    result = {
        "success": False,
        "url": url,
        "title": None,
        "content": None,
        "error": None
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://mp.weixin.qq.com/",
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            html = response.text

            # 提取标题
            title_match = re.search(r'<h2[^>]*id=["\']?activity-name["\']?[^>]*>([^<]+)</h2>', html)
            if not title_match:
                title_match = re.search(r'<title>([^<]+)</title>', html)
            if title_match:
                result["title"] = title_match.group(1).strip()

            # 提取文章内容
            content_match = re.search(r'<div[^>]*id=["\']?js_content["\']?[^>]*>([\s\S]*?)</div>', html)
            if content_match:
                # 清理 HTML 标签
                content_html = content_match.group(1)
                content_text = re.sub(r'<[^>]+>', '', content_html)
                content_text = re.sub(r'\s+', ' ', content_text).strip()
                result["content"] = content_text
                result["success"] = True
        else:
            result["error"] = f"HTTP {response.status_code}"

    except Exception as e:
        result["error"] = str(e)

    return result


def fetch_article(url: str, use_browser: bool = True) -> dict:
    """
    获取微信文章内容

    Args:
        url: 微信公众号文章链接
        use_browser: 是否使用浏览器模式（更稳定但更慢）

    Returns:
        包含文章内容的字典
    """
    # 先解析 URL
    url_info = parse_wechat_url(url)
    print(f"解析 URL: {json.dumps(url_info, ensure_ascii=False, indent=2)}", file=sys.stderr)

    if use_browser and PLAYWRIGHT_AVAILABLE:
        return fetch_article_with_playwright(url)
    else:
        return fetch_article_with_requests(url)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="微信公众号文章读取工具")
    parser.add_argument("url", help="微信公众号文章链接")
    parser.add_argument("--no-browser", action="store_true", help="不使用浏览器，直接用 HTTP 请求")
    parser.add_argument("--output", "-o", help="输出文件路径 (JSON 格式)")

    args = parser.parse_args()

    # 获取文章
    result = fetch_article(args.url, use_browser=not args.no_browser)

    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {args.output}", file=sys.stderr)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    # 返回状态码
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()