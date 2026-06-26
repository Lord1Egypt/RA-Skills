#!/usr/bin/env python3
"""
save_article.py — Fetch article content and save to Readwise Reader.

Outputs JSON to stdout for the agent to consume. Does NOT handle tagging —
that is delegated to the agent via llm-task.

Usage:
    python3 save_article.py "https://mp.weixin.qq.com/s/XXXXX"
    python3 save_article.py "https://example.com/post" --tag openclaw

Environment:
    READWISE_TOKEN — Required.

Output (JSON to stdout):
    On success:
    {
      "status": "ok",
      "title": "...",
      "author": "...",
      "domain": "...",
      "text_preview": "first ~8000 chars of body text",
      "is_wechat": true,
      "fetch_method": "server_fetch",
      "readwise_status": 201
    }

    On failure:
    {
      "status": "error",
      "error": "description",
      "fallback_saved": false
    }
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

READWISE_API_URL = "https://readwise.io/api/v3/save/"
TEXT_PREVIEW_MAX_CHARS = 8000

WECHAT_UI_FRAGMENTS = [
    "轻点两下取消赞",
    "轻点两下取消在看",
    "小程序 赞",
    "视频 小程序",
    "喜欢此内容的人还喜欢",
    "微信扫一扫关注该公众号",
    "前往看一看",
    '朋友会在"发现-看一看"看到你',
    "Scan with WeChat",
]


def output(data):
    """Print JSON to stdout and exit."""
    print(json.dumps(data, ensure_ascii=False))
    sys.exit(0 if data.get("status") == "ok" else 1)


def http_get(url, headers, timeout=15):
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            enc = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(enc, errors="replace")
    except (urllib.error.URLError, OSError, ValueError):
        return None


def http_post_json(url, headers, payload, timeout=30):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8", errors="replace"))
            return resp.status, body
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8", errors="replace"))
        except Exception:
            body = {"error": str(e)}
        return e.code, body
    except (urllib.error.URLError, OSError, ValueError) as e:
        return 0, {"error": str(e)}


def validate_wechat_html(html):
    if not html or len(html) < 5000:
        return False
    if sum(1 for f in WECHAT_UI_FRAGMENTS if f in html) >= 3:
        return False
    m = re.search(r'id="js_content"[^>]*>(.*?)</div>', html, re.DOTALL)
    if m:
        inner = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if len(inner) < 50:
            return False
    else:
        return False
    return True


def extract_title(html):
    og = re.search(r'property="og:title"\s+content="([^"]+)"', html)
    if og:
        return og.group(1)
    t = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    return t.group(1).strip() if t else None


def extract_author(html):
    a = re.search(r'name="author"\s+content="([^"]+)"', html)
    if a:
        return a.group(1)
    a = re.search(r'class="profile_nickname"[^>]*>([^<]+)<', html)
    if a:
        return a.group(1).strip()
    a = re.search(r'property="og:site_name"\s+content="([^"]+)"', html)
    return a.group(1) if a else None


def extract_text(html, max_chars=TEXT_PREVIEW_MAX_CHARS):
    """Extract readable text, preferring WeChat js_content div."""
    source = html
    js = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*<div', html, re.DOTALL)
    if not js:
        js = re.search(r'id="js_content"[^>]*>([\s\S]{100,}?)</div>', html, re.DOTALL)
    if js:
        source = js.group(1)
    text = re.sub(r"<script[^>]*>.*?</script>", "", source, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars] if len(text) > max_chars else text


def extract_domain(url):
    m = re.search(r"https?://([^/]+)", url)
    return m.group(1) if m else ""


def fetch_article(url, is_wechat=False):
    if is_wechat:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Mobile/15E148 MicroMessenger/8.0.44"
            ),
            "Referer": "https://mp.weixin.qq.com/",
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
    else:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        }
    return http_get(url, headers)


def save_to_readwise(token, url, html=None, title=None, tags=None):
    headers = {"Authorization": f"Token {token}"}
    payload = {"url": url, "tags": tags or ["openclaw"]}
    if html:
        payload["html"] = html
    if title:
        payload["title"] = title
    return http_post_json(READWISE_API_URL, headers, payload)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--tag", default="openclaw")
    args = parser.parse_args()

    token = os.environ.get("READWISE_TOKEN", "")
    if not token:
        output({"status": "error", "error": "READWISE_TOKEN not set", "fallback_saved": False})

    url = args.url.strip()
    if not url.startswith(("http://", "https://")):
        output({"status": "error", "error": f"Invalid URL: {url}", "fallback_saved": False})

    is_wechat = "mp.weixin.qq.com" in url
    domain = extract_domain(url)

    if is_wechat:
        html = fetch_article(url, is_wechat=True)

        if html and validate_wechat_html(html):
            title = extract_title(html) or "WeChat Article"
            author = extract_author(html)
            text = extract_text(html)
            status, body = save_to_readwise(token, url, html=html, title=title, tags=[args.tag])
            if status in (200, 201):
                output({
                    "status": "ok",
                    "title": title,
                    "author": author or "",
                    "domain": domain,
                    "text_preview": text,
                    "is_wechat": True,
                    "fetch_method": "server_fetch",
                    "readwise_status": status,
                })

        # Fallback: URL-only
        status, body = save_to_readwise(token, url, tags=[args.tag])
        if status in (200, 201):
            output({
                "status": "error",
                "error": "Server-side fetch failed; URL saved but content may be garbled",
                "fallback_saved": True,
            })

        err = body.get("detail", body.get("error", str(body)))
        output({"status": "error", "error": f"Readwise API {status}: {err}", "fallback_saved": False})

    else:
        html = fetch_article(url, is_wechat=False)
        title = None
        author = None
        text = ""

        if html and len(html) > 1000:
            title = extract_title(html)
            author = extract_author(html)
            text = extract_text(html)

        status, body = save_to_readwise(token, url, title=title, tags=[args.tag])
        if status in (200, 201):
            output({
                "status": "ok",
                "title": title or "",
                "author": author or "",
                "domain": domain,
                "text_preview": text,
                "is_wechat": False,
                "fetch_method": "readwise_direct" if not text else "server_prefetch",
                "readwise_status": status,
            })

        # Fallback: save with HTML
        if html and len(html) > 1000:
            status2, body2 = save_to_readwise(token, url, html=html, title=title, tags=[args.tag])
            if status2 in (200, 201):
                output({
                    "status": "ok",
                    "title": title or "",
                    "author": author or "",
                    "domain": domain,
                    "text_preview": text,
                    "is_wechat": False,
                    "fetch_method": "server_fetch_fallback",
                    "readwise_status": status2,
                })

        err = body.get("detail", body.get("error", str(body)))
        output({"status": "error", "error": f"Readwise API {status}: {err}", "fallback_saved": False})


if __name__ == "__main__":
    main()
