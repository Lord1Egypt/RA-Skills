#!/usr/bin/env python3
"""
web-search-local: 本地网络搜索脚本
基于必应搜索，无需 API Key

用法:
    python3 search.py --query "关键词" [--limit 10] [--engine bing|ddg|auto] [--verbose]
"""

import argparse
import hashlib
import json
import logging
import os
import random
import sys
import time
from urllib.parse import quote_plus

try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import xml.etree.ElementTree as ET
except ImportError:
    print("Error: xml.etree.ElementTree not available", file=sys.stderr)
    sys.exit(1)

# ── 常量 ──────────────────────────────────────────────

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]

BING_RSS_URL = "https://www.bing.com/search"
BING_CN_RSS_URL = "https://cn.bing.com/search"
DDG_HTML_URL = "https://html.duckduckgo.com/html/"  # 备用：可能被 SSL 封锁
YANDEX_SEARCH_URL = "https://yandex.com/search/"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

REQUEST_TIMEOUT = 10  # seconds (default, overridable via --timeout)
PROXY = None  # proxy URL (placeholder for future use)
NO_REDIRECT = False  # disable HTTP redirect following (placeholder for --no-redirect)

# 元信息计时器（每次搜索重置）
_search_timings = {}

def set_timeout(timeout):
    """修改全局请求超时时间"""
    global REQUEST_TIMEOUT
    REQUEST_TIMEOUT = timeout

def set_proxy(proxy_url):
    """Set proxy for all HTTP requests (HTTP and SOCKS5 supported)."""
    global PROXY
    if proxy_url:
        PROXY = proxy_url
        logger.info(f"Proxy configured: {PROXY}")


def _get_proxies():
    """Return proxies dict for requests, or None if no proxy configured."""
    if PROXY:
        return {"http": PROXY, "https": PROXY}
    return None

def set_no_redirect(enabled):
    """启用或禁用 HTTP 重定向跟随"""
    global NO_REDIRECT
    NO_REDIRECT = enabled
    if enabled:
        logger.info("No-redirect mode enabled")

MIN_DELAY = 2  # seconds
MAX_DELAY = 5  # seconds
MAX_RETRIES = 4

# CAPTCHA 检测关键词
CAPTCHA_KEYWORDS = ["captcha", "verify", "robot", "unusual traffic", "human verification"]

# 缓存配置
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "web-search-local")
CACHE_TTL = 3600  # 默认 1 小时过期

logger = logging.getLogger("web-search-local")


# ── 缓存函数 ──────────────────────────────────────────

def _cache_key(query, engine):
    """生成缓存键：query + engine 的 MD5"""
    raw = f"{engine}:{query}".lower().strip()
    return hashlib.md5(raw.encode()).hexdigest()


def cache_get(query, engine, ttl=None, verbose=False):
    """从缓存读取搜索结果，过期返回 None"""
    if ttl is None:
        ttl = CACHE_TTL
    key = _cache_key(query, engine)
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    if not os.path.exists(cache_file):
        logger.debug(f"[Cache] 未命中: {query}")
        return None
    try:
        mtime = os.path.getmtime(cache_file)
        age = time.time() - mtime
        if age > ttl:
            logger.debug(f"[Cache] 已过期: {query} (age={age:.0f}s, ttl={ttl})")
            return None
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"[Cache] 命中: {query} (age={age:.0f}s)")
        return data
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"[Cache] 读取失败: {e}")
        return None


def cache_set(query, engine, results, verbose=False):
    """写入搜索结果到缓存"""
    key = _cache_key(query, engine)
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)
        logger.debug(f"[Cache] 已写入: {query}")
    except OSError as e:
        logger.warning(f"[Cache] 写入失败: {e}")


# ── 工具函数 ──────────────────────────────────────────

def get_random_ua():
    """返回随机 User-Agent"""
    return random.choice(USER_AGENTS)


def random_delay():
    """随机延迟 2-5 秒"""
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    logger.debug(f"延迟 {delay:.1f}s")
    time.sleep(delay)


def build_headers():
    """构建完整浏览器请求头"""
    headers = HEADERS.copy()
    headers["User-Agent"] = get_random_ua()
    return headers


def is_captcha_page(text):
    """检测是否命中 CAPTCHA 页面"""
    text_lower = text.lower()
    return any(kw in text_lower for kw in CAPTCHA_KEYWORDS)


def exponential_backoff(attempt):
    """指数退避：1s, 2s, 4s, 8s"""
    delay = 2 ** attempt
    logger.warning(f"退避重试，等待 {delay}s (attempt {attempt + 1})")
    time.sleep(delay)


# ── Cookie 获取 ────────────────────────────────────────

def get_bing_cookies():
    """先访问必应首页获取 Cookie"""
    session = requests.Session()
    headers = build_headers()
    try:
        resp = session.get("https://www.bing.com", headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=not NO_REDIRECT, proxies=_get_proxies())
        # 安全地获取 cookie dict（处理重名 cookie）
        cookie_dict = {}
        for cookie in session.cookies:
            cookie_dict[cookie.name] = cookie.value
        logger.debug(f"首页响应: {resp.status_code}, cookies: {len(cookie_dict)} 个")
        return cookie_dict
    except requests.RequestException as e:
        logger.warning(f"获取 Cookie 失败: {e}")
        return {}


# ── Bing RSS 搜索 ─────────────────────────────────────

def search_bing_rss(query, limit=10, verbose=False, fast=False, lang=None):
    """
    使用 Bing RSS 格式搜索
    fast=True 时跳过 Cookie 获取，减少延迟
    lang: 搜索语言（如 "en", "zh-Hans"），影响 Bing 的 setlang 参数
    返回: [{title, url, snippet}]
    """
    global _search_timings
    _search_timings = {}

    # Cookie 获取
    t_cookie_start = time.time()
    cookies = {} if fast else get_bing_cookies()
    _search_timings["cookie"] = round(time.time() - t_cookie_start, 3)
    if not fast:
        random_delay()

    params = {"q": query, "format": "rss", "count": min(limit, 50)}
    if lang:
        params["setlang"] = lang
    headers = build_headers()

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"[RSS] 搜索: {query} (attempt {attempt + 1})")
            t_search_start = time.time()
            resp = requests.get(
                BING_RSS_URL,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=not NO_REDIRECT,
                proxies=_get_proxies(),
            )
            _search_timings["search"] = round(time.time() - t_search_start, 3)

            if resp.status_code == 429 or resp.status_code == 503:
                logger.warning(f"[RSS] HTTP {resp.status_code}")
                exponential_backoff(attempt)
                continue

            if resp.status_code == 403:
                logger.warning("[RSS] 被拒绝 (403)，尝试中国版")
                resp = requests.get(
                    BING_CN_RSS_URL,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    timeout=REQUEST_TIMEOUT,
                    allow_redirects=not NO_REDIRECT,
                    proxies=_get_proxies(),
                )

            resp.raise_for_status()

            if is_captcha_page(resp.text):
                logger.warning("[RSS] 命中 CAPTCHA")
                exponential_backoff(attempt)
                continue

            t_parse_start = time.time()
            results = parse_rss_results(resp.text, limit)
            _search_timings["parse"] = round(time.time() - t_parse_start, 3)
            return results

        except requests.Timeout:
            logger.warning("[RSS] 请求超时")
            exponential_backoff(attempt)
        except requests.RequestException as e:
            logger.error(f"[RSS] 请求失败: {e}")
            exponential_backoff(attempt)

    logger.error("[RSS] 所有重试均失败")
    return []


def parse_rss_results(xml_text, limit):
    """解析 Bing RSS XML 为结果列表"""
    results = []
    try:
        root = ET.fromstring(xml_text)
        # RSS namespace handling
        ns = {"": ""}
        items = root.findall(".//item")

        for item in items[:limit]:
            title = item.findtext("title", "").strip()
            url = item.findtext("link", "").strip()
            desc = item.findtext("description", "").strip()
            pub_date = item.findtext("pubDate", "").strip()

            if url:
                result = {
                    "title": title,
                    "url": url,
                    "snippet": desc,
                }
                if pub_date:
                    result["date"] = pub_date
                results.append(result)

        logger.info(f"[RSS] 解析到 {len(results)} 条结果")
    except ET.ParseError as e:
        logger.error(f"[RSS] XML 解析失败: {e}")

    return results


# ── Bing HTML 搜索 ────────────────────────────────────

def search_bing_html(query, limit=10, verbose=False, fast=False, lang=None):
    """
    使用 Bing HTML 页面解析搜索结果（RSS 备用方案）
    fast=True 时跳过 Cookie 获取，减少延迟
    lang: 搜索语言（如 "en", "zh-Hans"），影响 Bing 的 setlang 参数
    返回: [{title, url, snippet}]
    """
    global _search_timings
    if not _search_timings:
        _search_timings = {}

    # Cookie 获取
    t_cookie_start = time.time()
    cookies = {} if fast else get_bing_cookies()
    _search_timings["cookie"] = round(time.time() - t_cookie_start, 3)
    if not fast:
        random_delay()

    params = {"q": query}
    if lang:
        params["setlang"] = lang
    headers = build_headers()

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"[HTML] 搜索: {query} (attempt {attempt + 1})")
            t_search_start = time.time()
            resp = requests.get(
                BING_RSS_URL,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=not NO_REDIRECT,
                proxies=_get_proxies(),
            )
            _search_timings["search"] = round(time.time() - t_search_start, 3)

            if resp.status_code == 429 or resp.status_code == 503:
                logger.warning(f"[HTML] HTTP {resp.status_code}")
                exponential_backoff(attempt)
                continue

            if resp.status_code == 403:
                logger.warning("[HTML] 被拒绝 (403)，尝试中国版")
                resp = requests.get(
                    BING_CN_RSS_URL,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    timeout=REQUEST_TIMEOUT,
                    allow_redirects=not NO_REDIRECT,
                    proxies=_get_proxies(),
                )

            resp.raise_for_status()

            if is_captcha_page(resp.text):
                logger.warning("[HTML] 命中 CAPTCHA")
                exponential_backoff(attempt)
                continue

            t_parse_start = time.time()
            results = parse_html_results(resp.text, limit)
            _search_timings["parse"] = round(time.time() - t_parse_start, 3)
            return results

        except requests.Timeout:
            logger.warning("[HTML] 请求超时")
            exponential_backoff(attempt)
        except requests.RequestException as e:
            logger.error(f"[HTML] 请求失败: {e}")
            exponential_backoff(attempt)

    logger.error("[HTML] 所有重试均失败")
    return []


def parse_html_results(html_text, limit):
    """
    解析 Bing HTML 搜索结果页面
    从 class="b_algo" 区块中提取标题、URL、摘要
    """
    results = []

    try:
        from html.parser import HTMLParser
    except ImportError:
        logger.error("[HTML] html.parser 不可用")
        return results

    class BingHTMLParser(HTMLParser):
        """解析 Bing 搜索结果 HTML"""

        def __init__(self):
            super().__init__()
            self.results = []
            self._in_b_algo = False
            self._in_h2 = False
            self._in_link = False
            self._in_caption = False
            self._in_snippet = False
            self._depth = 0
            self._algo_depth = 0
            self._current = {}
            self._link_href = ""
            self._snippet_text = ""

        def handle_starttag(self, tag, attrs):
            attrs_dict = dict(attrs)
            cls = attrs_dict.get("class", "")
            tag_id = attrs_dict.get("id", "")

            # 检测搜索结果区块
            if tag == "li" and "b_algo" in cls:
                self._in_b_algo = True
                self._algo_depth = self._depth
                self._current = {"title": "", "url": "", "snippet": ""}

            if self._in_b_algo:
                if tag == "h2":
                    self._in_h2 = True
                if self._in_h2 and tag == "a":
                    self._in_link = True
                    href = attrs_dict.get("href", "")
                    if href and href.startswith("http"):
                        self._current["url"] = href
                        self._link_href = href
                if tag == "div" and "b_caption" in cls:
                    self._in_caption = True
                if self._in_caption and tag == "p":
                    self._in_snippet = True
                    self._snippet_text = ""

            self._depth += 1

        def handle_endtag(self, tag):
            self._depth -= 1

            if tag == "a" and self._in_link:
                self._in_link = False
            if tag == "h2" and self._in_h2:
                self._in_h2 = False
            if tag == "p" and self._in_snippet:
                self._current["snippet"] = self._snippet_text.strip()
                self._in_snippet = False
            if tag == "div" and self._in_caption:
                self._in_caption = False
            if tag == "li" and self._in_b_algo and self._depth <= self._algo_depth:
                # 收集完一个结果
                if self._current.get("url"):
                    self.results.append(self._current)
                self._in_b_algo = False
                self._current = {}

        def handle_data(self, data):
            if self._in_link and self._in_h2 and not self._current.get("title"):
                self._current["title"] = data.strip()
            if self._in_snippet:
                self._snippet_text += data

    try:
        parser = BingHTMLParser()
        parser.feed(html_text)
        results = parser.results[:limit]
        logger.info(f"[HTML] 解析到 {len(results)} 条结果")
    except Exception as e:
        logger.error(f"[HTML] 解析失败: {e}")

    return results


# ── DuckDuckGo 搜索 ──────────────────────────────────

def search_ddg(query, limit=10, verbose=False):
    """
    使用 DuckDuckGo HTML 版搜索（可能被 SSL 封锁）
    返回: [{title, url, snippet}]
    """
    global _search_timings
    _search_timings = {"cookie": 0.0}

    random_delay()
    headers = build_headers()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = {"q": query, "b": "", "kl": ""}

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"[DDG] 搜索: {query} (attempt {attempt + 1})")
            t_search_start = time.time()
            resp = requests.post(
                DDG_HTML_URL,
                data=data,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
                proxies=_get_proxies(),
            )
            _search_timings["search"] = round(time.time() - t_search_start, 3)

            if resp.status_code == 429 or resp.status_code == 503:
                logger.warning(f"[DDG] HTTP {resp.status_code}")
                exponential_backoff(attempt)
                continue

            resp.raise_for_status()

            if is_captcha_page(resp.text):
                logger.warning("[DDG] 命中 CAPTCHA")
                exponential_backoff(attempt)
                continue

            t_parse_start = time.time()
            results = parse_ddg_results(resp.text, limit)
            _search_timings["parse"] = round(time.time() - t_parse_start, 3)
            return results

        except requests.Timeout:
            logger.warning("[DDG] 请求超时")
            exponential_backoff(attempt)
        except requests.RequestException as e:
            logger.error(f"[DDG] 请求失败: {e}")
            exponential_backoff(attempt)

    logger.error("[DDG] 所有重试均失败")
    return []


def parse_ddg_results(html_text, limit):
    """
    解析 DuckDuckGo HTML 搜索结果
    """
    results = []
    try:
        from html.parser import HTMLParser
    except ImportError:
        logger.error("[DDG] html.parser 不可用")
        return results

    class DDGHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.results = []
            self._in_result = False
            self._in_title_link = False
            self._in_snippet = False
            self._current = {}
            self._snippet_text = ""

        def handle_starttag(self, tag, attrs):
            attrs_dict = dict(attrs)
            cls = attrs_dict.get("class", "")
            if tag == "div" and "result" in cls and "result--" not in cls:
                self._in_result = True
                self._current = {"title": "", "url": "", "snippet": ""}
            if self._in_result and tag == "a" and "result__a" in cls:
                self._in_title_link = True
                href = attrs_dict.get("href", "")
                if href:
                    real_url = extract_ddg_url(href)
                    if real_url:
                        self._current["url"] = real_url
            if self._in_result and tag in ("a", "td") and "result__snippet" in cls:
                self._in_snippet = True
                self._snippet_text = ""

        def handle_endtag(self, tag):
            if tag == "a" and self._in_title_link:
                self._in_title_link = False
            if tag in ("a", "td") and self._in_snippet:
                self._current["snippet"] = self._snippet_text.strip()
                self._in_snippet = False
            if tag == "div" and self._in_result:
                if self._current.get("url"):
                    self.results.append(self._current)
                self._in_result = False
                self._current = {}

        def handle_data(self, data):
            if self._in_title_link and not self._current.get("title"):
                self._current["title"] = data.strip()
            if self._in_snippet:
                self._snippet_text += data

    try:
        parser = DDGHTMLParser()
        parser.feed(html_text)
        results = parser.results[:limit]
        logger.info(f"[DDG] 解析到 {len(results)} 条结果")
    except Exception as e:
        logger.error(f"[DDG] 解析失败: {e}")
    return results


def extract_ddg_url(href):
    """从 DDG 重定向链接中提取真实 URL"""
    from urllib.parse import unquote, urlparse, parse_qs
    try:
        if "uddg=" in href:
            parsed = urlparse(href if href.startswith("http") else "https:" + href)
            qs = parse_qs(parsed.query)
            if "uddg" in qs:
                return unquote(qs["uddg"][0])
        if href.startswith("http"):
            return href
        return None
    except Exception:
        return None


# ── Yandex 搜索 ──────────────────────────────────────

def search_yandex(query, limit=10, verbose=False):
    """
    使用 Yandex 搜索（备选引擎）
    返回: [{title, url, snippet}]
    """
    global _search_timings
    _search_timings = {"cookie": 0.0}

    random_delay()
    headers = build_headers()
    params = {"text": query}

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"[Yandex] 搜索: {query} (attempt {attempt + 1})")
            t_search_start = time.time()
            resp = requests.get(
                YANDEX_SEARCH_URL,
                params=params,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
                proxies=_get_proxies(),
            )
            _search_timings["search"] = round(time.time() - t_search_start, 3)

            if resp.status_code == 429 or resp.status_code == 503:
                logger.warning(f"[Yandex] HTTP {resp.status_code}")
                exponential_backoff(attempt)
                continue

            resp.raise_for_status()

            if is_captcha_page(resp.text):
                logger.warning("[Yandex] 命中 CAPTCHA")
                exponential_backoff(attempt)
                continue

            t_parse_start = time.time()
            results = parse_yandex_results(resp.text, limit)
            _search_timings["parse"] = round(time.time() - t_parse_start, 3)
            return results

        except requests.Timeout:
            logger.warning("[Yandex] 请求超时")
            exponential_backoff(attempt)
        except requests.RequestException as e:
            logger.error(f"[Yandex] 请求失败: {e}")
            exponential_backoff(attempt)

    logger.error("[Yandex] 所有重试均失败")
    return []


def parse_yandex_results(html_text, limit):
    """
    解析 Yandex 搜索结果 HTML
    Yandex 结果在 <li class="serp-item"> 中，使用 regex 提取标题/URL/摘要
    """
    results = []
    import re

    # Extract title + URL from OrganicTitle-Link or similar patterns
    title_pattern = re.compile(
        r'<a[^>]*class="[^"]*(?:OrganicTitle-Link|Link)[^"]*"[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>',
        re.DOTALL
    )
    # Extract snippet from OrganicText
    snippet_pattern = re.compile(
        r'<div[^>]*class="[^"]*OrganicText[^"]*"[^>]*>(.*?)</div>',
        re.DOTALL
    )

    titles_urls = title_pattern.findall(html_text)
    snippets = snippet_pattern.findall(html_text)

    # Clean HTML tags from snippets
    clean_re = re.compile(r'<[^>]+>')

    for i, (url, raw_title) in enumerate(titles_urls[:limit]):
        title = clean_re.sub('', raw_title).strip()
        snippet = clean_re.sub('', snippets[i]).strip() if i < len(snippets) else ""
        if title and url:
            results.append({
                "title": title,
                "url": url,
                "snippet": snippet,
            })

    logger.info(f"[Yandex] 解析到 {len(results)} 条结果")
    return results


def search_auto(query, limit=10, verbose=False, fast=False, lang=None):
    """
    自动搜索：优先 Bing → Yandex → DuckDuckGo
    lang: 搜索语言（仅影响 Bing 引擎）
    返回去重后的结果（按优先级保留）
    """
    engine_attempts = []  # 记录引擎尝试历史

    # 1. Bing RSS
    logger.info("[Auto] 尝试引擎 1/5: Bing RSS")
    results = search_bing_rss(query, limit, verbose, fast=fast, lang=lang)
    engine_attempts.append(("bing_rss", len(results)))
    if results:
        logger.info(f"[Auto] ✓ Bing RSS 成功，获得 {len(results)} 条结果")
        # 如果结果不足，补充其他引擎（保持优先顺序）
        if len(results) < limit:
            logger.info(f"[Auto] 结果不足 {limit} 条，尝试补充...")
            # 优先级: Bing HTML → Yandex → DDG → WebFetch
            if len(results) < limit:
                logger.info("[Auto] 补充来源: Bing HTML")
                extra = search_bing_html(query, limit - len(results), verbose, fast=fast, lang=lang)
                seen_urls = {r["url"] for r in results}
                for r in extra:
                    if r["url"] not in seen_urls:
                        results.append(r)
                        seen_urls.add(r["url"])
            if len(results) < limit:
                logger.info("[Auto] 补充来源: Yandex")
                extra = search_yandex(query, limit - len(results), verbose)
                seen_urls = {r["url"] for r in results}
                for r in extra:
                    if r["url"] not in seen_urls:
                        results.append(r)
                        seen_urls.add(r["url"])
            if len(results) < limit:
                logger.info("[Auto] 补充来源: DuckDuckGo")
                extra = search_ddg(query, limit - len(results), verbose)
                seen_urls = {r["url"] for r in results}
                for r in extra:
                    if r["url"] not in seen_urls:
                        results.append(r)
                        seen_urls.add(r["url"])
            if len(results) < limit:
                logger.info("[Auto] 补充来源: WebFetch")
                extra = search_web_fetch(query, limit - len(results), verbose)
                seen_urls = {r["url"] for r in results}
                for r in extra:
                    if r["url"] not in seen_urls:
                        results.append(r)
                        seen_urls.add(r["url"])
        return results[:limit]
    else:
        logger.info("[Auto] ✗ Bing RSS 无结果")

    # 2. Bing HTML
    logger.info("[Auto] 尝试引擎 2/5: Bing HTML")
    results = search_bing_html(query, limit, verbose, fast=fast, lang=lang)
    engine_attempts.append(("bing_html", len(results)))
    if results:
        logger.info(f"[Auto] ✓ Bing HTML 成功，获得 {len(results)} 条结果")
        if len(results) < limit:
            logger.info(f"[Auto] 结果不足 {limit} 条，尝试补充 Yandex...")
            extra = search_yandex(query, limit - len(results), verbose)
            seen_urls = {r["url"] for r in results}
            for r in extra:
                if r["url"] not in seen_urls:
                    results.append(r)
                    seen_urls.add(r["url"])
        return results[:limit]
    else:
        logger.info("[Auto] ✗ Bing HTML 无结果")

    # 3. Yandex
    logger.info("[Auto] 尝试引擎 3/5: Yandex")
    results = search_yandex(query, limit, verbose)
    engine_attempts.append(("yandex", len(results)))
    if results:
        logger.info(f"[Auto] ✓ Yandex 成功，获得 {len(results)} 条结果")
        if len(results) < limit:
            logger.info(f"[Auto] 结果不足 {limit} 条，尝试补充 DuckDuckGo...")
            extra = search_ddg(query, limit - len(results), verbose)
            seen_urls = {r["url"] for r in results}
            for r in extra:
                if r["url"] not in seen_urls:
                    results.append(r)
                    seen_urls.add(r["url"])
        if len(results) < limit:
            logger.info("[Auto] 补充来源: WebFetch")
            extra = search_web_fetch(query, limit - len(results), verbose)
            seen_urls = {r["url"] for r in results}
            for r in extra:
                if r["url"] not in seen_urls:
                    results.append(r)
                    seen_urls.add(r["url"])
        return results[:limit]
    else:
        logger.info("[Auto] ✗ Yandex 无结果")

    # 4. DuckDuckGo
    logger.info("[Auto] 尝试引擎 4/5: DuckDuckGo")
    results = search_ddg(query, limit, verbose)
    engine_attempts.append(("ddg", len(results)))
    if results:
        logger.info(f"[Auto] ✓ DuckDuckGo 成功，获得 {len(results)} 条结果")
        if len(results) < limit:
            logger.info("[Auto] 补充来源: WebFetch")
            extra = search_web_fetch(query, limit - len(results), verbose)
            seen_urls = {r["url"] for r in results}
            for r in extra:
                if r["url"] not in seen_urls:
                    results.append(r)
                    seen_urls.add(r["url"])
        return results[:limit]
    else:
        logger.info("[Auto] ✗ DuckDuckGo 无结果")

    # 5. WebFetch (urllib 备用)
    logger.info("[Auto] 尝试引擎 5/5: WebFetch (urllib)")
    results = search_web_fetch(query, limit, verbose)
    engine_attempts.append(("webfetch", len(results)))
    if results:
        logger.info(f"[Auto] ✓ WebFetch 成功，获得 {len(results)} 条结果")
        return results[:limit]
    else:
        logger.info("[Auto] ✗ WebFetch 无结果")

    # 所有引擎均失败
    logger.warning(f"[Auto] 所有引擎均失败，尝试历史: {engine_attempts}")
    return []


# ── Web Fetch 引擎 (urllib 备用) ──────────────────────

def search_web_fetch(query, limit=10, verbose=False):
    """
    使用标准库 urllib 的搜索（不依赖 requests 包）
    作为 requests 不可用时的备用引擎
    返回: [{title, url, snippet}]
    """
    global _search_timings
    _search_timings = {"cookie": 0.0}

    import urllib.request
    import urllib.error
    import urllib.parse
    import gzip
    import io

    ua = get_random_ua()
    encoded_q = urllib.parse.quote_plus(query)
    url = f"https://cn.bing.com/search?q={encoded_q}"

    req = urllib.request.Request(url)
    req.add_header("User-Agent", ua)
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    req.add_header("Accept-Language", "zh-CN,zh;q=0.9,en;q=0.8")
    req.add_header("Accept-Encoding", "gzip, deflate")

    random_delay()

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"[WebFetch] 搜索: {query} (attempt {attempt + 1})")
            t_search_start = time.time()
            resp = urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT)

            raw_data = resp.read()
            # 处理 gzip 压缩
            if resp.headers.get("Content-Encoding") == "gzip":
                raw_data = gzip.GzipFile(fileobj=io.BytesIO(raw_data)).read()

            html_text = raw_data.decode("utf-8", errors="replace")
            _search_timings["search"] = round(time.time() - t_search_start, 3)

            if is_captcha_page(html_text):
                logger.warning("[WebFetch] 命中 CAPTCHA")
                exponential_backoff(attempt)
                continue

            t_parse_start = time.time()
            results = parse_html_results(html_text, limit)
            _search_timings["parse"] = round(time.time() - t_parse_start, 3)
            return results

        except urllib.error.HTTPError as e:
            logger.warning(f"[WebFetch] HTTP {e.code}: {e.reason}")
            if e.code in (429, 503):
                exponential_backoff(attempt)
                continue
            return []
        except urllib.error.URLError as e:
            logger.warning(f"[WebFetch] URL 错误: {e.reason}")
            exponential_backoff(attempt)
        except Exception as e:
            logger.error(f"[WebFetch] 失败: {e}")
            exponential_backoff(attempt)

    logger.error("[WebFetch] 所有重试均失败")
    return []


USE_COLOR = True  # ANSI color support, overridable via --no-color


def sort_results_by_date(results, reverse=True):
    """Sort results by date field (newest first by default). Items without date go to end."""
    from email.utils import parsedate_to_datetime
    import re

    def _parse_date(raw):
        """Parse RFC 2822 date string, with fallback for Chinese day names and month names."""
        if not raw:
            return None
        # Try standard parsing first
        try:
            return parsedate_to_datetime(raw).timestamp()
        except Exception:
            pass
        # Fallback: strip Chinese day names (周一, 周二, etc.) and retry
        cleaned = re.sub(r'^周[一二三四五六日天],?\s*', '', raw)
        try:
            return parsedate_to_datetime(cleaned).timestamp()
        except Exception:
            pass
        # Fallback: Chinese date format "16 3月 2026 23:38:00 GMT"
        zh_months = {'1月': 'Jan', '2月': 'Feb', '3月': 'Mar', '4月': 'Apr', '5月': 'May', '6月': 'Jun',
                     '7月': 'Jul', '8月': 'Aug', '9月': 'Sep', '10月': 'Oct', '11月': 'Nov', '12月': 'Dec'}
        m = re.search(r'(\d{1,2})\s+(\d{1,2}月)\s+(\d{4})\s+(\d{2}:\d{2}:\d{2})', cleaned)
        if m and m.group(2) in zh_months:
            try:
                from datetime import datetime
                english_month = zh_months[m.group(2)]
                dt_str = f"{m.group(1)} {english_month} {m.group(3)} {m.group(4)}"
                dt = datetime.strptime(dt_str, "%d %b %Y %H:%M:%S")
                return dt.timestamp()
            except Exception:
                pass
        # Fallback: extract English month pattern "12 Mar 2026"
        m = re.search(r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})', cleaned, re.IGNORECASE)
        if m:
            try:
                from datetime import datetime
                dt = datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%d %b %Y")
                return dt.timestamp()
            except Exception:
                pass
        return None

    def date_key(r):
        ts = _parse_date(r.get("date", ""))
        if ts is None:
            return (1, 0)  # no date → end
        return (0, -ts if reverse else ts)

    return sorted(results, key=date_key)

def set_color(enabled):
    """启用或禁用 ANSI 颜色输出"""
    global USE_COLOR
    USE_COLOR = enabled


def format_text_output(output, elapsed=None, color=None):
    """将搜索结果格式化为人类可读的文本"""
    if color is None:
        color = USE_COLOR

    # ANSI color codes
    RESET = "\033[0m" if color else ""
    BOLD = "\033[1m" if color else ""
    CYAN = "\033[36m" if color else ""
    GREEN = "\033[32m" if color else ""
    YELLOW = "\033[33m" if color else ""
    DIM = "\033[2m" if color else ""

    lines = []
    lines.append(f"{BOLD}搜索:{RESET} {output['query']}")
    lines.append(f"{BOLD}引擎:{RESET} {CYAN}{output['engine']}{RESET}")
    lines.append(f"{BOLD}结果数:{RESET} {output['count']}")
    lines.append(DIM + "─" * 60 + RESET if color else "=" * 60)

    for i, r in enumerate(output["results"], 1):
        lines.append(f"\n{GREEN}{i}.{RESET} {BOLD}{r['title']}{RESET}" if color else f"\n{i}. {r['title']}")
        lines.append(f"   {CYAN}{r['url']}{RESET}" if color else f"   {r['url']}")
        if r.get("snippet"):
            lines.append(f"   {r['snippet']}")

    if not output["results"]:
        lines.append("\n(无搜索结果)")

    if elapsed is not None:
        lines.append("")
        lines.append(f"{YELLOW}搜索耗时:{RESET} {elapsed:.2f}s" if color else f"搜索耗时: {elapsed:.2f}s")

    # 元信息计时
    metadata = output.get("metadata", {})
    if metadata:
        parts = []
        if metadata.get("cookie_seconds", 0) > 0:
            parts.append(f"cookie {metadata['cookie_seconds']}s")
        if metadata.get("search_seconds", 0) > 0:
            parts.append(f"search {metadata['search_seconds']}s")
        if metadata.get("parse_seconds", 0) > 0:
            parts.append(f"parse {metadata['parse_seconds']}s")
        if metadata.get("cache_hit"):
            parts.append("cache ✓")
        if parts:
            lines.append(f"{DIM}  [{', '.join(parts)}]{RESET}" if color else f"  [{', '.join(parts)}]")

    return "\n".join(lines)


def write_output(text, filepath=None):
    """输出到文件或 stdout"""
    if filepath:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text + "\n")
            logger.info(f"结果已写入: {filepath}")
        except OSError as e:
            logger.error(f"写入文件失败: {e}")
            print(text)
    else:
        print(text)


def cache_clear():
    """清空所有缓存文件"""
    import glob
    if not os.path.isdir(CACHE_DIR):
        return 0
    files = glob.glob(os.path.join(CACHE_DIR, "*.json"))
    count = 0
    for f in files:
        try:
            os.remove(f)
            count += 1
        except OSError:
            pass
    return count


def cache_stats():
    """返回缓存统计信息"""
    import glob
    if not os.path.isdir(CACHE_DIR):
        return {"total": 0, "valid": 0, "expired": 0, "total_size_kb": 0}
    files = glob.glob(os.path.join(CACHE_DIR, "*.json"))
    total = len(files)
    valid = 0
    expired = 0
    total_size = 0
    now = time.time()
    for f in files:
        try:
            stat = os.stat(f)
            total_size += stat.st_size
            age = now - stat.st_mtime
            if age < CACHE_TTL:
                valid += 1
            else:
                expired += 1
        except OSError:
            pass
    return {
        "total": total,
        "valid": valid,
        "expired": expired,
        "total_size_kb": round(total_size / 1024, 1),
        "cache_dir": CACHE_DIR,
    }


# ── 参数解析 ──────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="本地网络搜索 (基于必应)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--query", "-q", help="搜索关键词")
    parser.add_argument("--limit", "-l", "--count", type=int, default=10, help="返回结果数量 (默认: 10)")
    parser.add_argument(
        "--engine", "-e",
        choices=["bing", "ddg", "yandex", "webfetch", "auto"],
        default="bing",
        help="搜索引擎 (默认: bing)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="显示调试信息")
    parser.add_argument("--no-cache", action="store_true", help="跳过缓存")
    parser.add_argument("--cache-ttl", type=int, default=None, help="缓存过期时间（秒，默认 3600）")
    parser.add_argument("--cache-clear", action="store_true", help="清空所有缓存")
    parser.add_argument("--cache-stats", action="store_true", help="显示缓存统计")
    parser.add_argument("--output", "-o", help="输出到文件（如 -o results.json）")
    parser.add_argument(
        "--format", "-f",
        choices=["json", "text"],
        default="json",
        dest="fmt",
        help="输出格式：json（默认）或 text（人类可读）",
    )
    parser.add_argument("--fast", action="store_true", help="快速模式：跳过 Cookie 获取，减少延迟")
    parser.add_argument("--lang", help="搜索语言（如 en, zh-Hans），影响 Bing 的 setlang 参数")
    parser.add_argument("--timeout", "-t", type=int, default=10, help="请求超时时间（秒，默认 10）")
    parser.add_argument("--no-color", action="store_true", help="text 格式输出时禁用 ANSI 颜色码")
    parser.add_argument("--proxy", help="代理地址（如 socks5://127.0.0.1:1080 或 http://host:port）")
    parser.add_argument("--no-redirect", action="store_true", help="禁止 HTTP 重定向跟随，用于检测搜索引擎跳转链接")
    parser.add_argument(
        "--sort",
        choices=["relevance", "date"],
        default="relevance",
        help="结果排序方式：relevance（默认，相关性）或 date（日期，newest first，需 RSS 源支持）",
    )
    return parser.parse_args()


# ── 主函数 ────────────────────────────────────────────

def main():
    args = parse_args()

    # 配置日志
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    # 应用 --timeout 参数
    set_timeout(args.timeout)

    # 应用 --no-color 参数
    set_color(not args.no_color)

    # 应用 --proxy 参数（预留接口）
    if args.proxy:
        set_proxy(args.proxy)

    # 应用 --no-redirect 参数
    if args.no_redirect:
        set_no_redirect(True)

    # 缓存管理命令
    if args.cache_clear:
        count = cache_clear()
        print(json.dumps({"action": "clear", "removed": count}, ensure_ascii=False))
        return

    if args.cache_stats:
        stats = cache_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return

    # 搜索模式需要 --query
    if not args.query:
        print("Error: --query/-q is required for search", file=sys.stderr)
        sys.exit(1)

    logger.info(f"搜索: {args.query} (engine={args.engine}, limit={args.limit})")

    results = []
    engine_used = args.engine

    # 缓存 TTL
    cache_ttl = args.cache_ttl if args.cache_ttl is not None else CACHE_TTL

    # fast 模式：跳过 Cookie 和延迟
    fast = args.fast

    # language 参数
    lang = args.lang

    # 计时
    t_start = time.time()

    # 尝试缓存读取（除非 --no-cache）
    if not args.no_cache:
        cached = cache_get(args.query, args.engine, ttl=cache_ttl, verbose=args.verbose)
        if cached is not None:
            elapsed = time.time() - t_start
            cached["elapsed_seconds"] = round(elapsed, 2)
            if "metadata" not in cached:
                cached["metadata"] = {"cookie_seconds": 0.0, "search_seconds": 0.0, "parse_seconds": 0.0, "cache_hit": True}
            else:
                cached["metadata"]["cache_hit"] = True
            if args.fmt == "text":
                write_output(format_text_output(cached, elapsed=elapsed), args.output)
            else:
                write_output(json.dumps(cached, ensure_ascii=False, indent=2), args.output)
            return

    if args.engine == "bing":
        results = search_bing_rss(args.query, args.limit, args.verbose, fast=fast, lang=lang)
        if not results:
            logger.info("RSS 搜索无结果，尝试 HTML 解析")
            results = search_bing_html(args.query, args.limit, args.verbose, fast=fast, lang=lang)
    elif args.engine == "ddg":
        results = search_ddg(args.query, args.limit, args.verbose)
    elif args.engine == "yandex":
        results = search_yandex(args.query, args.limit, args.verbose)
    elif args.engine == "webfetch":
        results = search_web_fetch(args.query, args.limit, args.verbose)
    elif args.engine == "auto":
        results = search_auto(args.query, args.limit, args.verbose, fast=fast, lang=lang)
        # auto 模式下记录实际使用的引擎（取第一个成功的结果来源）
        if results:
            engine_used = "auto(bing→yandex→ddg)"

    # --sort date: 按日期排序（RSS 有 pubDate 时生效）
    if args.sort == "date" and results:
        results = sort_results_by_date(results)
        logger.info("结果已按日期排序 (newest first)")

    # 输出 JSON
    elapsed = time.time() - t_start
    metadata = {
        "cookie_seconds": _search_timings.get("cookie", 0.0),
        "search_seconds": _search_timings.get("search", 0.0),
        "parse_seconds": _search_timings.get("parse", 0.0),
    }
    output = {
        "query": args.query,
        "engine": engine_used,
        "count": len(results),
        "results": results,
        "elapsed_seconds": round(elapsed, 2),
        "metadata": metadata,
    }

    # 写入缓存
    if results and not args.no_cache:
        cache_set(args.query, args.engine, output, args.verbose)

    # 输出
    if args.fmt == "text":
        write_output(format_text_output(output, elapsed=elapsed), args.output)
    else:
        write_output(json.dumps(output, ensure_ascii=False, indent=2), args.output)

    # verbose 模式下额外输出总结日志
    if args.verbose:
        logger.info("=" * 60)
        logger.info("搜索完成总结:")
        logger.info(f"  查询: {output['query']}")
        logger.info(f"  引擎: {output['engine']}")
        logger.info(f"  结果数: {output['count']}")
        logger.info(f"  总耗时: {output['elapsed_seconds']}s")
        if "metadata" in output:
            md = output["metadata"]
            logger.info(f"  分段耗时: cookie={md.get('cookie_seconds', 0)}s, search={md.get('search_seconds', 0)}s, parse={md.get('parse_seconds', 0)}s")
            if md.get("cache_hit"):
                logger.info("  缓存状态: ✓ HIT")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
