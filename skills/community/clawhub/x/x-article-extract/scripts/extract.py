#!/usr/bin/env python3
"""
X Article 内容提取 — 独立 CLI 工具

支持三种场景：
  1. 普通推文 → xreach tweet
  2. X Article → Playwright + xreach cookie
  3. 推文含 t.co 外部链接 → 解析 + Firecrawl

用法:
    # 提取单条
    python3 extract.py --url "https://x.com/user/status/123"

    # 提取并入库
    python3 extract.py --url "https://x.com/user/status/123" --ingest

    # 批量
    python3 extract.py --url "https://x.com/a/status/111" --url "https://x.com/b/status/222"

    # 仅解析 t.co
    python3 extract.py --resolve "https://t.co/abc123"
"""

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger("x-article-extract")

# ── 工具函数 ─────────────────────────────────────────────────────

def get_proxy() -> str | None:
    """获取代理 URL。"""
    return os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or None


def parse_playwright_proxy(proxy_url: str | None) -> dict | None:
    """将带认证信息的代理 URL 转成 Playwright 需要的 proxy 配置。"""
    if not proxy_url:
        return None

    from urllib.parse import urlparse, unquote

    parsed = urlparse(proxy_url)
    if not parsed.scheme or not parsed.hostname or not parsed.port:
        return {"server": proxy_url}

    proxy = {"server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"}
    if parsed.username:
        proxy["username"] = unquote(parsed.username)
    if parsed.password:
        proxy["password"] = unquote(parsed.password)
    return proxy


def resolve_tco(tco_url: str, proxy: str | None = None) -> str | None:
    """解析 t.co 短链到真实 URL。"""
    try:
        cmd = ["curl", "-Ls", "-o", "/dev/null", "-w", "%{url_effective}",
               "--max-time", "10", tco_url]
        if proxy:
            cmd.extend(["--proxy", proxy])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        url = result.stdout.strip()
        return url if url and url != tco_url else None
    except Exception as e:
        logger.warning("t.co 解析失败: %s", e)
        return None


def has_cjk(text: str) -> bool:
    """检测文本是否包含 CJK 字符。"""
    return any(0x4E00 <= ord(ch) <= 0x9FFF for ch in text)


def parse_x_url(url: str) -> str | None:
    """从 X/Twitter URL 中提取 tweet ID。"""
    m = re.search(r"(?:x\.com|twitter\.com)/[^/]+/status/(\d+)", url)
    return m.group(1) if m else None


# ── 提取函数 ─────────────────────────────────────────────────────

def extract_tweet(tweet_id: str, proxy: str | None = None) -> dict:
    """用 xreach 提取推文数据。"""
    xreach = shutil.which("xreach")
    if not xreach:
        return {"error": "xreach 未安装"}

    cmd = [xreach, "tweet", tweet_id, "--json"]
    if proxy:
        cmd.extend(["--proxy", proxy])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {"error": f"xreach 失败: {result.stderr.strip()[:200]}"}
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return {"error": "xreach 超时"}
    except json.JSONDecodeError:
        return {"error": "xreach 输出解析失败"}


def scrape_x_article(article_url: str, proxy: str | None = None) -> str:
    """用 Playwright + xreach cookie 抓取 X Article 完整正文。"""
    session_path = Path.home() / ".config" / "xfetch" / "session.json"
    if not session_path.exists():
        logger.info("xreach session 不存在")
        return ""

    try:
        with open(session_path) as f:
            session = json.load(f)
        auth_token = session.get("authToken", "")
        ct0 = session.get("ct0", "")
        if not auth_token or not ct0:
            return ""
    except Exception:
        return ""

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.info("playwright 未安装")
        return ""

    try:
        with sync_playwright() as p:
            launch_opts = {"headless": True}
            pw_proxy = parse_playwright_proxy(proxy)
            if pw_proxy:
                launch_opts["proxy"] = pw_proxy

            browser = p.chromium.launch(**launch_opts)
            context = browser.new_context()
            context.add_cookies([
                {"name": "auth_token", "value": auth_token,
                 "domain": ".x.com", "path": "/"},
                {"name": "ct0", "value": ct0,
                 "domain": ".x.com", "path": "/"},
            ])

            page = context.new_page()
            # X Article 在代理环境下经常迟迟到不了 domcontentloaded，
            # 先拿到首包(commit)再多等一段时间，成功率更高。
            page.goto(article_url, timeout=120000, wait_until="commit")
            page.wait_for_timeout(12000)

            content = ""
            for selector in ["main", "article", "[role='article']"]:
                el = page.query_selector(selector)
                if el:
                    text = el.inner_text()
                    if len(text) > 200:
                        content = text
                        break

            browser.close()
            return content[:8000] if len(content) > 200 else ""
    except Exception as e:
        logger.warning("Playwright 异常: %s", e)
        return ""


def get_thread_context(tweet_id: str, screen_name: str,
                       proxy: str | None = None) -> str:
    """用 xreach thread 获取讨论上下文。"""
    xreach = shutil.which("xreach")
    if not xreach:
        return ""

    try:
        cmd = [xreach, "thread", tweet_id, "--json"]
        if proxy:
            cmd.extend(["--proxy", proxy])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return ""

        data = json.loads(result.stdout)
        items = data if isinstance(data, list) else data.get("items", [])

        parts = []
        for t in items:
            text = t.get("text", "").strip()
            user = t.get("user", {}).get("screenName", "")
            stripped = re.sub(r'https?://\S+', '', text).strip()
            if len(stripped) > 20:
                prefix = f"@{user}" if user != screen_name else "作者补充"
                parts.append(f"[{prefix}] {text}")

        return "\n\n".join(parts[:10]) if parts else ""
    except Exception:
        return ""


def fetch_external_page(url: str) -> dict | None:
    """用 Firecrawl 抓取外部网页。"""
    import urllib.request

    api_key = os.environ.get("FIRECRAWL_API_KEY", "")
    if not api_key:
        return None

    try:
        payload = json.dumps({"url": url, "formats": ["markdown"]}).encode()
        req = urllib.request.Request(
            "https://api.firecrawl.dev/v1/scrape",
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())

        if not data.get("success"):
            return None

        page = data.get("data", {})
        markdown = page.get("markdown", "")
        title = page.get("metadata", {}).get("title", "")
        return {"title": title, "content": markdown} if len(markdown) > 100 else None
    except Exception:
        return None


# ── 主逻辑 ───────────────────────────────────────────────────────

def extract_x_url(url: str, proxy: str | None = None) -> dict:
    """
    提取一条 X/Twitter URL 的完整内容。

    返回:
        {
            "url": str,
            "title": str,
            "author": str,
            "description": str,
            "content_type": "tweet" | "x_article" | "external_page",
            "engagement": {...},
            "word_count": int,
            "language": str,
        }
    """
    tweet_id = parse_x_url(url)
    if not tweet_id:
        return {"url": url, "error": "无法解析 X/Twitter URL"}

    # 获取推文
    tweet = extract_tweet(tweet_id, proxy)
    if "error" in tweet:
        return {"url": url, **tweet}

    text = tweet.get("text", "")
    user = tweet.get("user", {})
    author = user.get("name", "") or user.get("screenName", "Unknown")
    screen_name = user.get("screenName", "")
    created_at = tweet.get("createdAt", "")

    engagement = {
        "views": tweet.get("viewCount", 0),
        "likes": tweet.get("likeCount", 0),
        "retweets": tweet.get("retweetCount", 0),
        "bookmarks": tweet.get("bookmarkCount", 0),
        "replies": tweet.get("replyCount", 0),
        "quotes": tweet.get("quoteCount", 0),
    }
    engagement_text = (
        f"{engagement['views']} 浏览 · {engagement['likes']} 赞 · "
        f"{engagement['retweets']} 转发 · {engagement['bookmarks']} 收藏"
    )

    # 检测薄内容（正文只有 t.co 链接）
    text_stripped = re.sub(r'https?://t\.co/\S+', '', text).strip()
    tco_urls = re.findall(r'https?://t\.co/\S+', text)

    if len(text_stripped) < 30 and tco_urls:
        # 解析 t.co
        resolved = None
        for tco in tco_urls:
            resolved = resolve_tco(tco, proxy)
            if resolved:
                logger.info("t.co → %s", resolved)
                break

        if resolved and ("x.com/i/article" in resolved or "twitter.com/i/article" in resolved):
            # X Article
            article_text = scrape_x_article(resolved, proxy)
            if not article_text:
                article_text = get_thread_context(tweet_id, screen_name, proxy)
                content_type = "x_article_thread"
            else:
                content_type = "x_article"

            first_line = article_text.split("\n")[0].strip() if article_text else ""
            title = f"@{screen_name}: {first_line[:80]}" if first_line else f"@{screen_name} 的 X Article"

            description = (
                f"X Article by @{screen_name}\n"
                f"Article URL: {resolved}\n"
                f"互动: {engagement_text}\n\n"
                f"{article_text}"
            )

            return {
                "url": url,
                "title": title,
                "author": author,
                "screen_name": screen_name,
                "description": description,
                "content_type": content_type,
                "article_url": resolved,
                "engagement": engagement,
                "word_count": len(description),
                "language": "zh" if has_cjk(description) else "en",
                "publish_date": created_at[:10] if created_at else "",
            }

        elif resolved:
            # 外部网页
            page = fetch_external_page(resolved)
            if page:
                title = page["title"] or f"@{screen_name} 分享"
                description = (
                    f"@{screen_name} 分享: {resolved}\n"
                    f"互动: {engagement_text}\n\n"
                    f"{page['content'][:6000]}"
                )
                return {
                    "url": url,
                    "title": title,
                    "author": author,
                    "screen_name": screen_name,
                    "description": description,
                    "content_type": "external_page",
                    "target_url": resolved,
                    "engagement": engagement,
                    "word_count": len(description),
                    "language": "zh" if has_cjk(description) else "en",
                    "publish_date": created_at[:10] if created_at else "",
                }

    # 普通推文
    title = f"@{screen_name}: {text[:80]}" if screen_name else text[:80]
    return {
        "url": url,
        "title": title,
        "author": author,
        "screen_name": screen_name,
        "description": text,
        "content_type": "tweet",
        "engagement": engagement,
        "word_count": len(text),
        "language": "zh" if has_cjk(text) else "en",
        "publish_date": created_at[:10] if created_at else "",
    }


# ── 入库 ─────────────────────────────────────────────────────────

def ingest_to_content_factory(result: dict) -> str | None:
    """将提取结果写入内容工厂素材库（通过 bitable_ops.py）。"""
    bitable_script = Path.home() / ".openclaw/workspace/skills/content-factory/scripts/bitable_ops.py"
    if not bitable_script.exists():
        logger.warning("内容工厂 bitable_ops.py 不存在")
        return None

    import json, subprocess

    fields = {
        "title": result.get("title", "")[:50],
        "source_platform": "video_x",
        "source_type": "link",
        "source_url": result.get("url", ""),
        "raw_content": result.get("description", ""),
        "author": result.get("author", ""),
        "status": "待处理",
    }

    try:
        proc = subprocess.run(
            ["python3", str(bitable_script), "create",
             "--table", "MaterialInbox",
             "--fields", json.dumps(fields, ensure_ascii=False)],
            capture_output=True, text=True, timeout=30,
        )
        if proc.returncode != 0:
            logger.warning("入库失败: %s", proc.stderr.strip())
            return None

        logger.info("已入库: %s", proc.stdout.strip())
        return proc.stdout.strip()
    except Exception as e:
        logger.warning("入库失败: %s", e)
        return None


# ── CLI ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="X/Twitter 内容提取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--url", action="append", default=[],
                        help="X/Twitter URL（可多个）")
    parser.add_argument("--resolve", default="",
                        help="仅解析 t.co 短链")
    parser.add_argument("--ingest", action="store_true",
                        help="提取后入库到内容工厂")
    parser.add_argument("--json", action="store_true", dest="output_json",
                        help="输出原始 JSON")
    parser.add_argument("--proxy", default="",
                        help="代理地址（默认从环境变量读取）")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(message)s")

    proxy = args.proxy or get_proxy()

    # 仅解析 t.co
    if args.resolve:
        resolved = resolve_tco(args.resolve, proxy)
        if resolved:
            print(f"{args.resolve} → {resolved}")
        else:
            print(f"解析失败: {args.resolve}")
        return

    if not args.url:
        parser.print_help()
        sys.exit(1)

    results = []
    for url in args.url:
        result = extract_x_url(url, proxy)
        results.append(result)

        if args.ingest and "error" not in result:
            record_id = ingest_to_content_factory(result)
            if record_id:
                result["record_id"] = record_id

    # 输出
    if args.output_json:
        output = results if len(results) > 1 else results[0]
        json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        for r in results:
            print(f"\n{'═' * 60}")
            if "error" in r:
                print(f"  ERROR: {r['error']}")
                print(f"  URL: {r['url']}")
                continue

            print(f"  {r.get('content_type', '?').upper()}")
            print(f"  标题: {r.get('title', '')}")
            print(f"  作者: {r.get('author', '')}")
            e = r.get("engagement", {})
            print(f"  互动: {e.get('views', 0)} 浏览 · {e.get('likes', 0)} 赞 · "
                  f"{e.get('bookmarks', 0)} 收藏")
            print(f"  字数: {r.get('word_count', 0)}")

            if r.get("record_id"):
                print(f"  入库: {r['record_id']}")

            desc = r.get("description", "")
            if desc:
                print(f"\n  --- 内容预览（前 500 字）---")
                print(f"  {desc[:500]}")
            print(f"{'═' * 60}")


if __name__ == "__main__":
    main()
