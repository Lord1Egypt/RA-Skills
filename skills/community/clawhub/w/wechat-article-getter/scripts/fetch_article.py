#!/usr/bin/env python3
"""
WeChat Article Reader — 微信公众号文章提取器

Usage:
    python3 fetch_article.py "https://mp.weixin.qq.com/s/xxx"
    python3 fetch_article.py "https://mp.weixin.qq.com/s/xxx" --output article.json
    python3 fetch_article.py "https://mp.weixin.qq.com/s/xxx" --format markdown

API:
    from fetch_article import fetch_wechat_article
    result = fetch_wechat_article(url)
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Optional

# ── 结果类型 ──

def _ok(title, author, publish_time, content, source, url):
    return {
        "success": True,
        "title": title,
        "author": author,
        "publish_time": publish_time,
        "content": content,
        "word_count": len(content),
        "source": source,
        "url": url,
        "error": None,
    }

def _err(url, error):
    return {
        "success": False,
        "title": "", "author": "", "publish_time": "",
        "content": "", "word_count": 0,
        "source": "", "url": url,
        "error": str(error),
    }


# ── Playwright 方式（主力） ──

_browser = None  # 复用浏览器实例

def _ensure_playwright_installed():
    """首次运行自动安装 playwright + chromium"""
    try:
        import playwright  # noqa: F401
    except ImportError:
        import subprocess
        print("📦 首次运行：安装 playwright + beautifulsoup4 ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "beautifulsoup4", "-q"])

    # 检查 chromium 是否已安装
    from pathlib import Path as _P
    cache = _P.home() / ".cache" / "ms-playwright"
    has_chromium = any(p.name.startswith("chromium") for p in cache.iterdir()) if cache.exists() else False
    if not has_chromium:
        import subprocess
        print("🌐 首次运行：安装 Chromium 浏览器（~110MB）...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ Chromium 安装完成")


def _get_browser():
    """懒加载 Playwright 浏览器（进程内复用）"""
    global _browser
    if _browser and _browser.is_connected():
        return _browser

    _ensure_playwright_installed()
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    _browser = pw.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ],
    )
    return _browser


def _fetch_via_playwright(url: str, timeout_ms: int = 30000) -> dict:
    """用 headless Chromium 渲染微信文章并提取正文"""
    from bs4 import BeautifulSoup

    browser = _get_browser()
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    )
    page = context.new_page()

    try:
        # 拦截图片/视频/字体加速加载
        page.route(
            re.compile(r"\.(png|jpg|jpeg|gif|svg|webp|mp4|mp3|woff2?|ttf|eot)(\?|$)", re.I),
            lambda route: route.abort(),
        )

        page.goto(url, wait_until="networkidle", timeout=timeout_ms)

        # 等待正文容器
        page.wait_for_selector("#js_content", timeout=10000)

        html = page.content()
    finally:
        page.close()
        context.close()

    # 解析
    soup = BeautifulSoup(html, "html.parser")

    # 标题
    title_el = soup.find("h1", {"id": "activity-name"})
    title = title_el.get_text(strip=True) if title_el else ""

    # 作者
    author_el = (
        soup.find("span", {"id": "js_author_name"})
        or soup.find("a", {"id": "js_name"})
    )
    author = author_el.get_text(strip=True) if author_el else ""

    # 发布时间
    time_el = soup.find("em", {"id": "publish_time"})
    publish_time = time_el.get_text(strip=True) if time_el else ""

    # 正文
    content_el = soup.find("div", {"id": "js_content"})
    if not content_el:
        return _err(url, "正文容器 #js_content 未找到（可能是登录墙或已删除）")

    # 清洗
    for tag in content_el.find_all(["script", "style", "iframe"]):
        tag.decompose()
    text = content_el.get_text(separator="\n", strip=True)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    text = text.strip()

    if len(text) < 50:
        return _err(url, f"正文过短（{len(text)} 字符），可能被反爬拦截")

    return _ok(title, author, publish_time, text, "playwright", url)


# ── 镜像站搜索（备用） ──

MIRROR_SITES = [
    ("53ai.com", "https://www.53ai.com/search?q={query}"),
    ("36kr.com", "https://36kr.com/search/articles/{query}"),
]

def _fetch_via_mirror(url: str, title_hint: str = "") -> dict:
    """在镜像站搜索文章（fallback）"""
    import httpx

    if not title_hint:
        return _err(url, "镜像搜索需要标题关键词")

    for site_name, search_tpl in MIRROR_SITES:
        try:
            search_url = search_tpl.format(query=title_hint[:30])
            resp = httpx.get(search_url, timeout=10, follow_redirects=True)
            if resp.status_code == 200 and len(resp.text) > 1000:
                # 简化：返回搜索提示
                return _err(url, f"镜像搜索 {site_name} 有结果，需手动提取（自动提取 TODO）")
        except Exception:
            continue

    return _err(url, "所有镜像站搜索失败")


# ── 统一入口 ──

def fetch_wechat_article(
    url: str,
    timeout_ms: int = 30000,
    fallback_mirror: bool = True,
) -> dict:
    """
    提取微信公众号文章正文。

    Args:
        url: mp.weixin.qq.com 文章链接
        timeout_ms: 页面加载超时（毫秒）
        fallback_mirror: Playwright 失败时是否尝试镜像站

    Returns:
        dict: {success, title, author, publish_time, content, word_count, source, url, error}
    """
    if "mp.weixin.qq.com" not in url:
        return _err(url, "不是微信公众号链接")

    # 尝试 Playwright
    try:
        result = _fetch_via_playwright(url, timeout_ms)
        if result["success"]:
            return result
        pw_error = result["error"]
    except ImportError:
        pw_error = "Playwright 未安装（运行 python3 scripts/setup.py）"
    except Exception as e:
        pw_error = str(e)[:200]

    # Playwright 失败 → 镜像
    if fallback_mirror:
        mirror_result = _fetch_via_mirror(url)
        if mirror_result["success"]:
            return mirror_result

    return _err(url, f"Playwright: {pw_error}")


# ── CLI ──

def main():
    import argparse

    parser = argparse.ArgumentParser(description="微信公众号文章提取器")
    parser.add_argument("url", help="微信文章链接 (mp.weixin.qq.com/s/xxx)")
    parser.add_argument("--output", "-o", help="输出文件路径（JSON）")
    parser.add_argument("--format", "-f", choices=["json", "markdown", "text"], default="json")
    parser.add_argument("--timeout", type=int, default=30000, help="超时（毫秒）")
    args = parser.parse_args()

    t0 = time.time()
    result = fetch_wechat_article(args.url, timeout_ms=args.timeout)
    elapsed = time.time() - t0

    if args.format == "json":
        out = json.dumps(result, ensure_ascii=False, indent=2)
    elif args.format == "markdown":
        if result["success"]:
            out = f"# {result['title']}\n\n"
            out += f"> 作者: {result['author']} | 发布: {result['publish_time']}\n\n"
            out += result["content"]
        else:
            out = f"❌ 提取失败: {result['error']}"
    else:  # text
        out = result.get("content", result.get("error", ""))

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"✅ 已保存到 {args.output} ({elapsed:.1f}s)")
    else:
        print(out)

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
