#!/usr/bin/env python3
"""
知乎专栏文章抓取器
支持三级认证降级：Browser Profile → File Cookie → 高仿真请求头
"""
import argparse
import json
import os
import re
import sys
import time
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"依赖缺失: {e}. 请运行 pip install requests beautifulsoup4")
    sys.exit(1)

# 配置文件路径
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "cookie.json")
DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
)


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def build_cookie_string(cookie_dict):
    parts = []
    for k, v in cookie_dict.items():
        if k.startswith("_") or k in ("z_c0", "d_c0", "SESSIONID", "KMS"):
            if v:
                parts.append(f"{k}={v}")
    return "; ".join(parts)


def zhihu_url_to_api(url: str) -> str:
    """Convert zhuanlan.zhihu.com/p/xxx to internal API if possible."""
    parsed = urlparse(url)
    if "/p/" in parsed.path:
        match = re.search(r"/p/(\d+)", parsed.path)
        if match:
            article_id = match.group(1)
            return f"https://www.zhihu.com/api/v4/articles/{article_id}"
    return url


def fetch_with_browser_profile(url):
    """Use Playwright with headful Chromium and anti-detection to bypass Zhihu protection."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError("Playwright 未安装，请运行: pip install playwright && python -m playwright install chromium")

    with sync_playwright() as p:
        # headful mode is key to bypassing Zhihu's bot detection
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=DEFAULT_UA,
        )
        page = context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            delete navigator.__proto__.webdriver;
        """)
        page.goto(url, wait_until="domcontentloaded")
        # Give SPA time to hydrate
        page.wait_for_timeout(2500)
        html = page.content()
        browser.close()
        if len(html) < 1000 or "您当前请求存在异常" in html:
            raise RuntimeError("Playwright 抓取到的页面被拦截或为空")
        return html


def fetch_with_file_cookie(url, config):
    cookie = config.get("cookie", {})
    cookie_str = build_cookie_string(cookie)
    if not cookie_str:
        raise RuntimeError("未配置有效 Cookie")

    headers = {
        "User-Agent": DEFAULT_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.zhihu.com/",
        "Cookie": cookie_str,
    }
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}")
    return resp.text


def fetch_with_simulated_headers(url):
    """High-fidelity headers without any cookie."""
    headers = {
        "User-Agent": DEFAULT_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.zhihu.com/",
        "Origin": "https://www.zhihu.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}")
    return resp.text


def parse_zhihu_article(html: str, url: str):
    soup = BeautifulSoup(html, "html.parser")

    # 尝试多种标题选择器
    title = ""
    for selector in ["h1.Title", "h1", ".Post-Title", "title"]:
        tag = soup.select_one(selector)
        if tag:
            title = tag.get_text(strip=True)
            if title:
                break

    # 尝试提取正文
    content = ""
    content_el = soup.select_one("article.Post-RichTextContainer") or soup.select_one(".RichText") or soup.select_one(".Post-RichText")
    if content_el:
        # 清理脚本和样式
        for script in content_el.find_all(["script", "style", "noscript"]):
            script.decompose()
        paragraphs = []
        for p in content_el.find_all(["p", "h2", "h3", "li", "blockquote", "pre"]):
            text = p.get_text(strip=True)
            if text:
                paragraphs.append(text)
        content = "\n\n".join(paragraphs)
    else:
        # Fallback: 提取所有可见段落
        paragraphs = []
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if len(text) > 20:
                paragraphs.append(text)
        content = "\n\n".join(paragraphs[:50])

    if not content or len(content) < 100:
        raise RuntimeError("未能提取到正文内容，可能遇到反爬或页面结构变更")

    return {
        "title": title or "Unknown",
        "url": url,
        "content": content,
        "word_count": len(content),
    }


def fetch_article(url: str, config: dict):
    """Four-level auth fallback."""
    errors = []

    # 方法1: Playwright Browser (most reliable for Zhihu anti-bot)
    try:
        html = fetch_with_browser_profile(url)
        return {"html": html, "method": "playwright_browser"}
    except Exception as e:
        errors.append(f"playwright_browser: {e}")

    # 方法2: File Cookie
    try:
        time.sleep(1.5)
        html = fetch_with_file_cookie(url, config)
        return {"html": html, "method": "file_cookie"}
    except Exception as e:
        errors.append(f"file_cookie: {e}")

    # 方法3: Simulated headers (no cookie)
    try:
        time.sleep(2)
        html = fetch_with_simulated_headers(url)
        return {"html": html, "method": "simulated_headers"}
    except Exception as e:
        errors.append(f"simulated_headers: {e}")

    raise RuntimeError(f"所有抓取方式均失败: {'; '.join(errors)}")


def main():
    parser = argparse.ArgumentParser(description="知乎专栏文章抓取器")
    parser.add_argument("url", help="知乎专栏文章 URL，如 https://zhuanlan.zhihu.com/p/660571164")
    parser.add_argument("--output", "-o", default=None, help="输出 JSON 文件路径")
    args = parser.parse_args()

    url = args.url.strip()
    if "zhuanlan.zhihu.com" not in url:
        print("错误: 只支持 zhuanlan.zhihu.com 的专栏文章")
        sys.exit(1)

    config = load_config()

    try:
        result = fetch_article(url, config)
        article = parse_zhihu_article(result["html"], url)
        article["fetch_method"] = result["method"]

        output = {
            "meta": {
                "source": "zhihu-zhuanlan",
                "fetch_time": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "auth_method": result["method"],
                "url": url,
            },
            "data": article,
        }

        json_str = json.dumps(output, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_str)
            print(f"✅ 已保存到: {args.output}")
        else:
            print(json_str)

    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        print("\n💡 建议:")
        print("   1. 配置 Cookie: 编辑 config/cookie.json 填入浏览器中的知乎 Cookie")
        print("   2. 确保 URL 是有效的知乎专栏文章链接")
        sys.exit(1)


if __name__ == "__main__":
    main()
