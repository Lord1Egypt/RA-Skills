#!/usr/bin/env python3
"""v20.101: fetch_content.py - 通用文章抓取器
- 通用 curl 抓取 (5s 超时, 手机 UA)
- 失败 fallback 到 playwright (15s)
- 微信公众号走 weixin.sogou.com (移动 UA)
- 返回 {title, content, source, success}

策略:
1. 微信公众号 (mp.weixin.qq.com) → 用手机 UA + 短超时 (公众号页面 JS 渲染轻)
2. 普通网页 → 通用 UA + 5s 超时 (HTML 优先, 失败用 playwright)
3. 跳转链接 (sogou.com/link) → 检测后用 playwright 跟踪 redirect
"""
import sys
import re
import json
import time
import subprocess
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, Optional, List
from pathlib import Path

# 移动 UA (微信公众号页面最佳)
MOBILE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
DESKTOP_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/<server-ip> Safari/537.36'

# 内容提取 (HTML → 纯文本)
_SCRIPT_RE = re.compile(r'<script\b[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE)
_STYLE_RE = re.compile(r'<style\b[^>]*>.*?</style>', re.DOTALL | re.IGNORECASE)
_TAG_RE = re.compile(r'<[^>]+>')
_WS_RE = re.compile(r'\s+')

def _extract_text(html: str, max_len: int = 8000) -> str:
    """从 HTML 提取正文 (粗粒度, 不解析 DOM)
    v20.101: 简单但有效 - 删 script/style/HTML 标签, 保留段落结构
    """
    if not html:
        return ''
    # 删 script/style
    html = _SCRIPT_RE.sub('', html)
    html = _STYLE_RE.sub('', html)
    # 找正文区域 (article / main / body)
    body_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
    if not body_match:
        body_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL | re.IGNORECASE)
    if not body_match:
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    if body_match:
        html = body_match.group(1)
    # 删 HTML 标签
    text = _TAG_RE.sub(' ', html)
    # HTML entities (粗处理)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    # 合并空白
    text = _WS_RE.sub(' ', text).strip()
    if len(text) > max_len:
        text = text[:max_len] + '...'
    return text

def _extract_title(html: str) -> str:
    """从 HTML 提取 title"""
    m = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
    if m:
        title = m.group(1).strip()
        title = title.replace('&nbsp;', ' ').replace('&amp;', '&')
        return title[:200]
    return ''

def fetch_url_curl(url: str, timeout: int = 5, ua: str = MOBILE_UA) -> Dict:
    """通用 curl 抓取 (v20.101 默认)
    返回: {success, title, content, source, status, error}
    """
    result = {'url': url, 'success': False, 'title': '', 'content': '', 'source': 'curl', 'status': 0, 'error': ''}
    try:
        # 用 curl 因为它自动处理 gzip/charset/redirects
        r = subprocess.run(
            ['curl', '-s', '-L', '-A', ua, '--max-time', str(timeout),
             '-H', 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8',
             '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             '-o', '/tmp/_fetch_tmp.html',
             '-w', '%{http_code}|%{size_download}|%{url_effective}',
             url],
            capture_output=True, text=True, timeout=timeout + 3
        )
        if r.returncode != 0:
            result['error'] = f'curl failed: {r.returncode}'
            return result
        parts = r.stdout.split('|')
        status = int(parts[0]) if parts[0].isdigit() else 0
        size = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        result['status'] = status
        # 读文件
        try:
            with open('/tmp/_fetch_tmp.html', 'rb') as f:
                raw = f.read()
            # 简化的 charset 检测 (优先 utf-8, 退化 gb18030)
            for enc in ('utf-8', 'gb18030', 'gbk', 'latin-1'):
                try:
                    html = raw.decode(enc)
                    break
                except:
                    continue
            else:
                html = raw.decode('utf-8', errors='ignore')
        except Exception as e:
            result['error'] = f'read failed: {e}'
            return result
        # 200 但太小 = 可能是反爬空页面
        if status == 200 and size < 500:
            result['error'] = f'too_small:{size}'
            return result
        # 403/451 = 不可达
        if status in (403, 451, 404):
            result['error'] = f'status:{status}'
            return result
        # 提取
        result['title'] = _extract_title(html)
        result['content'] = _extract_text(html)
        # 内容太短 = 抓取失败 (只有导航栏)
        if len(result['content']) < 50:
            result['error'] = f'content_too_short:{len(result["content"])}'
            return result
        result['success'] = True
        return result
    except subprocess.TimeoutExpired:
        result['error'] = 'timeout'
        return result
    except Exception as e:
        result['error'] = f'exception:{type(e).__name__}:{e}'
        return result

def fetch_url_playwright(url: str, timeout: int = 15) -> Dict:
    """Playwright 兜底抓取 (v20.101 fallback)
    用于 curl 失败的页面 (JS 渲染重 / 反爬严)
    """
    result = {'url': url, 'success': False, 'title': '', 'content': '', 'source': 'playwright', 'status': 0, 'error': ''}
    try:
        import asyncio
        from playwright.async_api import async_playwright
        async def _go():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context(
                    user_agent=MOBILE_UA,
                    viewport={'width': 375, 'height': 812},
                    locale='zh-CN'
                )
                page = await ctx.new_page()
                try:
                    resp = await page.goto(url, wait_until='domcontentloaded', timeout=timeout*1000)
                    status = resp.status if resp else 0
                    await asyncio.sleep(0.5)  # 等 JS
                    html = await page.content()
                    title = await page.title()
                except Exception as e:
                    return {'error': f'goto:{e}', 'status': 0, 'html': '', 'title': ''}
                finally:
                    await browser.close()
                return {'status': status, 'html': html, 'title': title, 'error': ''}
        # 在已有 event loop 的环境 (如 FastAPI) 下用 nest_asyncio 兼容
        try:
            import nest_asyncio
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            data = loop.run_until_complete(_go())
        except (RuntimeError, ImportError):
            data = asyncio.run(_go())
        result['status'] = data['status']
        result['title'] = data['title'][:200]
        result['content'] = _extract_text(data['html'])
        if data['error']:
            result['error'] = data['error']
        elif len(result['content']) < 50:
            result['error'] = 'content_too_short'
        else:
            result['success'] = True
        return result
    except ImportError:
        result['error'] = 'playwright_not_installed'
        return result
    except Exception as e:
        result['error'] = f'pw_exception:{type(e).__name__}:{e}'
        return result

def fetch_url(url: str, use_playwright: bool = True) -> Dict:
    """v20.101 主入口: 智能抓取单个 URL
    1. 先 curl (5s)
    2. 失败 → playwright (15s)
    3. 微信公众号特殊处理
    """
    if not url or not url.startswith('http'):
        return {'url': url, 'success': False, 'error': 'invalid_url', 'title': '', 'content': '', 'source': '', 'status': 0}
    # 微信公众号: 优先 playwright (JS 渲染重)
    is_weixin = 'mp.weixin.qq.com' in url
    # 搜狗跳转链接: 直接 playwright (JS 解码 + redirect)
    is_sogou_link = 'sogou.com/link' in url or 'sogoucdn.com' in url
    if is_sogou_link:
        # 跳过 sogou 跳转, 直接 playwright 走完
        if use_playwright:
            return fetch_url_playwright(url, timeout=15)
        else:
            return fetch_url_curl(url, timeout=8, ua=MOBILE_UA)
    # 普通/微信公众号: curl 先试
    r = fetch_url_curl(url, timeout=5)
    if r['success']:
        return r
    # 微信公众号 curl 失败 → playwright
    if is_weixin and use_playwright:
        return fetch_url_playwright(url, timeout=15)
    # 其他: 如果启用 pw 兜底
    if use_playwright:
        return fetch_url_playwright(url, timeout=15)
    return r

def fetch_results(results: List[Dict], top_n: int = 3, use_playwright: bool = True) -> List[Dict]:
    """v20.101: 批量抓取搜索结果前 N 条
    输入: results = [{title, url, ...}, ...]
    输出: 同样的列表, 每条加了 content/success
    """
    out = []
    for i, r in enumerate(results[:top_n]):
        if not isinstance(r, dict):
            out.append(r)
            continue
        url = r.get('url', '')
        if not url:
            r['fetch_success'] = False
            r['fetch_error'] = 'no_url'
            out.append(r)
            continue
        print(f"  [{i+1}/{top_n}] {url[:60]}...", file=sys.stderr)
        t0 = time.time()
        fetch = fetch_url(url, use_playwright=use_playwright)
        elapsed = round(time.time() - t0, 1)
        r['fetch_success'] = fetch['success']
        r['fetch_error'] = fetch.get('error', '')
        r['fetch_source'] = fetch.get('source', '')
        r['fetch_elapsed'] = elapsed
        if fetch['success']:
            # 限制 content 长度避免爆 token
            r['content'] = fetch['content'][:5000]
            r['content_title'] = fetch.get('title', r.get('title', ''))
        out.append(r)
    # 剩余的也加标记
    for r in results[top_n:]:
        if isinstance(r, dict):
            r['fetch_success'] = False
            r['fetch_error'] = 'skipped'
            r['fetch_source'] = ''
            r['fetch_elapsed'] = 0
        out.append(r)
    return out

def main():
    import argparse
    p = argparse.ArgumentParser(description='v20.101: 文章抓取器')
    p.add_argument('url', nargs='?', help='单个 URL (省略则进入交互)')
    p.add_argument('--top', type=int, default=3, help='批量模式抓前 N 条 (从 stdin JSON 输入)')
    p.add_argument('--no-pw', action='store_true', help='禁用 playwright 兜底')
    p.add_argument('--json', action='store_true', help='输出 JSON')
    args = p.parse_args()
    use_pw = not args.no_pw
    if args.url:
        r = fetch_url(args.url, use_playwright=use_pw)
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print(f"URL: {r['url']}")
            print(f"Success: {r['success']} ({r['source']})")
            print(f"Status: {r['status']} | Error: {r['error']}")
            print(f"Title: {r['title']}")
            print(f"Content ({len(r['content'])} chars):")
            print(r['content'][:1000])
    elif not sys.stdin.isatty():
        # 批量模式: 从 stdin 读 JSON 数组
        data = json.load(sys.stdin)
        if isinstance(data, dict) and 'results' in data:
            data['results'] = fetch_results(data['results'], top_n=args.top, use_playwright=use_pw)
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif isinstance(data, list):
            data = fetch_results(data, top_n=args.top, use_playwright=use_pw)
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print("Invalid input: 需要 JSON list 或 {results: [...]}", file=sys.stderr)
            sys.exit(1)
    else:
        p.print_help()

if __name__ == '__main__':
    main()