"""
RSS Agent 扫描器 - Feed 解析、自动发现、HTML 抓取、并发扫描。
"""

import html
import ipaddress
import re
import socket
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from typing import Callable, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

# 常量
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}
REQUEST_TIMEOUT = 30
MAX_RESPONSE_BYTES = 10 * 1024 * 1024  # 10 MB
MAX_RETRIES = 3
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
RETRY_BASE_DELAY = 1.0  # 秒

# SSRF 防护：屏蔽的 IP 范围
_BLOCKED_IP_RANGES = [
    ipaddress.ip_network('127.0.0.0/8'),       # 回环地址
    ipaddress.ip_network('10.0.0.0/8'),         # 私有网络 A
    ipaddress.ip_network('172.16.0.0/12'),      # 私有网络 B
    ipaddress.ip_network('192.168.0.0/16'),     # 私有网络 C
    ipaddress.ip_network('169.254.0.0/16'),     # Link-local / 云元数据
    ipaddress.ip_network('0.0.0.0/8'),          # 当前网络
    ipaddress.ip_network('100.64.0.0/10'),      # 共享地址空间
    ipaddress.ip_network('::1/128'),            # IPv6 回环
    ipaddress.ip_network('fc00::/7'),           # IPv6 私有
    ipaddress.ip_network('fe80::/10'),          # IPv6 Link-local
]
CONTENT_NS = '{http://purl.org/rss/1.0/modules/content/}'
ATOM_NS = '{http://www.w3.org/2005/Atom}'
RDF_NS = '{http://purl.org/rss/1.0/}'

FEED_LINK_TYPES = {
    'application/rss+xml',
    'application/atom+xml',
    'application/feed+json',
    'application/xml',
    'text/xml',
}

COMMON_FEED_PATHS = [
    '/feed', '/feed/', '/feed.xml',
    '/rss', '/rss/', '/rss.xml',
    '/atom.xml', '/index.xml',
    '/feed/rss', '/feed/atom',
    '/blog/feed', '/blog/rss', '/blog.rss',
]


# ---------------------------------------------------------------------------
# 安全 XML 解析（XXE 防护）
# ---------------------------------------------------------------------------

def safe_parse_xml_string(xml_bytes):
    """从字节解析 XML，禁用外部实体解析。"""
    if isinstance(xml_bytes, str):
        xml_bytes = xml_bytes.encode('utf-8', errors='replace')
    try:
        import defusedxml.ElementTree as DefusedET
        return DefusedET.fromstring(xml_bytes)
    except ImportError:
        # 标准库回退：移除 DOCTYPE 声明（含内部子集）以防止 XXE 攻击
        xml_text = xml_bytes.decode('utf-8', errors='replace')
        xml_text = re.sub(r'<!DOCTYPE\s[^[>]*(\[.*?\])?\s*>', '', xml_text,
                          count=1, flags=re.IGNORECASE | re.DOTALL)
        return ET.fromstring(xml_text)


def safe_parse_xml_file(filepath):
    """解析 XML 文件，带 XXE 防护。"""
    try:
        import defusedxml.ElementTree as DefusedET
        return DefusedET.parse(filepath).getroot()
    except ImportError:
        # 回退到 safe_parse_xml_string（已包含 DOCTYPE 移除）
        with open(filepath, 'rb') as f:
            return safe_parse_xml_string(f.read())


# ---------------------------------------------------------------------------
# HTML 标签清理
# ---------------------------------------------------------------------------

class _HTMLStripper(HTMLParser):
    """去除所有 HTML 标签，仅保留文本内容。
    危险标签（script, style, iframe, svg 等）的内容会被完全抑制。"""

    # 内容需要被完全抑制的标签
    _SUPPRESS_TAGS = {
        'script', 'style', 'head', 'iframe', 'object', 'embed',
        'applet', 'noscript', 'noembed', 'noframes', 'template',
        'svg', 'math', 'form', 'input', 'textarea', 'select', 'button',
    }

    _NEWLINE_TAGS = {
        'p', 'br', 'div', 'li', 'tr', 'dt', 'dd', 'blockquote', 'pre',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'article', 'section',
    }

    # 自闭合元素（永远没有结束标签）
    _VOID_TAGS = {
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr',
    }

    def __init__(self):
        super().__init__()
        self._parts = []
        self._suppress_stack = []  # stack of suppressed tag names

    def handle_starttag(self, tag, attrs):
        if tag in self._SUPPRESS_TAGS:
            # 自闭合标签只抑制不入栈（不期望有结束标签）
            if tag not in self._VOID_TAGS:
                self._suppress_stack.append(tag)
            # 自闭合标签如 <input>, <embed>, <img> — 直接跳过，不入栈
        elif not self._suppress_stack:
            if tag in self._NEWLINE_TAGS:
                self._parts.append('\n')

    def handle_endtag(self, tag):
        if tag in self._SUPPRESS_TAGS and self._suppress_stack:
            # 弹出最近匹配的标签
            for i in range(len(self._suppress_stack) - 1, -1, -1):
                if self._suppress_stack[i] == tag:
                    self._suppress_stack.pop(i)
                    break

    def handle_data(self, data):
        if not self._suppress_stack:
            self._parts.append(data)

    def get_text(self):
        return ''.join(self._parts).strip()


def strip_html(text):
    """安全地移除文本中的 HTML 标签。"""
    if not text:
        return ''
    text = html.unescape(text)
    stripper = _HTMLStripper()
    try:
        stripper.feed(text)
        return stripper.get_text()
    except Exception:
        text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', text, flags=re.DOTALL | re.IGNORECASE)
        return re.sub(r'<[^>]+>', '', text).strip()


# ---------------------------------------------------------------------------
# SSRF 防护
# ---------------------------------------------------------------------------

class SSRFError(Exception):
    """当 URL 指向被屏蔽的内网/私有地址时抛出。"""
    pass


DNS_RESOLVE_TIMEOUT = 5  # DNS 解析超时（秒）


def _validate_url_safe(url):
    """验证 URL 是否指向内网/私有网络。
    如果不安全则抛出 SSRFError。"""
    parsed = urlparse(url)

    # 仅允许 http 和 https 协议
    if parsed.scheme not in ('http', 'https'):
        raise SSRFError(f"Blocked scheme: {parsed.scheme} (only http/https allowed)")

    hostname = parsed.hostname
    if not hostname:
        raise SSRFError(f"No hostname in URL: {url}")

    # 将主机名解析为 IP 并检查是否在屏蔽范围内
    # 使用线程池限制 DNS 解析时间，防止卡死
    try:
        with ThreadPoolExecutor(max_workers=1) as dns_executor:
            future = dns_executor.submit(
                socket.getaddrinfo, hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM
            )
            addr_infos = future.result(timeout=DNS_RESOLVE_TIMEOUT)
    except (socket.gaierror, TimeoutError):
        # DNS 无法解析或超时 — 放行，让 HTTP 请求自然失败
        return

    for family, _, _, _, sockaddr in addr_infos:
        ip_str = sockaddr[0]
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            continue
        for blocked in _BLOCKED_IP_RANGES:
            if ip in blocked:
                raise SSRFError(
                    f"Blocked: {hostname} resolves to {ip} (private/internal network)"
                )


# ---------------------------------------------------------------------------
# HTTP 辅助
# ---------------------------------------------------------------------------

class ResponseTooLargeError(Exception):
    """当响应超过大小限制时抛出。"""
    pass


def _fetch_once(url, timeout):
    """单次请求，带 SSRF 安全的重定向跟随和大小限制。
    使用统一 deadline 机制，重定向和下载共享时间预算。"""
    import requests

    deadline = time.monotonic() + timeout

    _validate_url_safe(url)

    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError(f"Request timeout before connecting to {url}")

    resp = requests.get(
        url, timeout=min(timeout, remaining), headers=REQUEST_HEADERS,
        allow_redirects=False, stream=True,
    )

    # 手动处理重定向并进行验证
    max_redirects = 5
    for _ in range(max_redirects):
        if resp.status_code not in (301, 302, 303, 307, 308):
            break
        redirect_url = resp.headers.get('Location', '')
        if not redirect_url:
            break
        resp.close()

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"Request timeout during redirect to {redirect_url}")

        redirect_url = urljoin(url, redirect_url)
        _validate_url_safe(redirect_url)
        url = redirect_url
        resp = requests.get(
            url, timeout=min(timeout, remaining), headers=REQUEST_HEADERS,
            allow_redirects=False, stream=True,
        )

    # 强制响应大小限制
    content_length = resp.headers.get('Content-Length')
    if content_length:
        try:
            if int(content_length) > MAX_RESPONSE_BYTES:
                resp.close()
                raise ResponseTooLargeError(
                    f"Response too large: {content_length} bytes (limit {MAX_RESPONSE_BYTES})")
        except ValueError:
            pass  # 非数字的 Content-Length，跳过预检查

    # 分块读取内容并检查大小和时间预算
    chunks = []
    total = 0
    for chunk in resp.iter_content(chunk_size=65536):
        total += len(chunk)
        if total > MAX_RESPONSE_BYTES:
            resp.close()
            raise ResponseTooLargeError(
                f"Response exceeded {MAX_RESPONSE_BYTES} bytes during download")
        if time.monotonic() > deadline:
            resp.close()
            raise TimeoutError(f"Request timeout during download from {url}")
        chunks.append(chunk)

    # 构建简单的响应包装，避免依赖 requests 内部 API
    class _Response:
        def __init__(self, original, content):
            self.status_code = original.status_code
            self.headers = original.headers
            self.content = content
            self.encoding = original.encoding or 'utf-8'
        @property
        def text(self):
            return self.content.decode(self.encoding, errors='replace')

    return _Response(resp, b''.join(chunks))


def fetch_url(url, timeout=REQUEST_TIMEOUT, retries=MAX_RETRIES):
    """请求 URL，带 SSRF 防护、指数退避重试和响应大小限制。
    返回 Response。
    可能抛出 SSRFError、ResponseTooLargeError 或 requests 异常。"""
    import requests

    for attempt in range(retries):
        try:
            resp = _fetch_once(url, timeout=timeout)
            # 对临时性服务器错误进行重试
            if resp.status_code in RETRY_STATUS_CODES and attempt < retries - 1:
                # 遵循 429 的 Retry-After 头部
                retry_after = resp.headers.get('Retry-After')
                if retry_after:
                    try:
                        delay = min(float(retry_after), 30.0)
                    except ValueError:
                        delay = RETRY_BASE_DELAY * (2 ** attempt)
                else:
                    delay = RETRY_BASE_DELAY * (2 ** attempt)
                time.sleep(delay)
                continue
            return resp
        except (SSRFError, ResponseTooLargeError):
            raise  # 不可重试
        except (requests.ConnectionError, requests.Timeout):
            if attempt < retries - 1:
                time.sleep(RETRY_BASE_DELAY * (2 ** attempt))
                continue
            raise
        except requests.RequestException:
            raise  # 其他请求错误不可重试

    # 最后一次尝试返回了可重试的状态码 — 原样返回
    return resp


# ---------------------------------------------------------------------------
# Feed 解析
# ---------------------------------------------------------------------------

def _normalize_date(dt):
    """将 datetime 规范化为 naive UTC。"""
    if dt is None:
        return None
    if dt.tzinfo:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def _parse_rss_items(channel, limit=None, full_content=False, since=None):
    """解析 RSS 2.0 channel 条目。"""
    items = []
    for item in channel.findall('item'):
        title = item.findtext('title', 'No Title')
        link = item.findtext('link', '')
        pub_date_str = item.findtext('pubDate', '')
        desc = item.findtext('description', '')

        pub_date = None
        if pub_date_str:
            try:
                pub_date = _normalize_date(parsedate_to_datetime(pub_date_str))
            except Exception:
                pass

        if since and pub_date and pub_date < since:
            continue

        content = None
        if full_content:
            elem = item.find(f'{CONTENT_NS}encoded')
            if elem is not None and elem.text:
                content = strip_html(elem.text)

        summary = strip_html(desc) if desc else ''
        items.append({
            "title": title,
            "url": link,
            "link": link,
            "published_date": pub_date,
            "date_str": pub_date_str,
            "summary": summary[:300] + "..." if len(summary) > 300 else summary,
            "content": content,
        })

        if limit and len(items) >= limit:
            break

    return items


def _parse_atom_entries(root, limit=None, full_content=False, since=None):
    """解析 Atom Feed 条目。"""
    items = []
    for entry in root.findall(f'{ATOM_NS}entry'):
        title = entry.findtext(f'{ATOM_NS}title', 'No Title')
        # 优先使用 rel="alternate" 链接，回退到第一个链接
        link = ''
        link_nodes = entry.findall(f'{ATOM_NS}link')
        for ln in link_nodes:
            rel = ln.get('rel', 'alternate')
            if rel == 'alternate' and ln.get('href'):
                link = ln.get('href')
                break
        if not link and link_nodes:
            link = link_nodes[0].get('href', '')
        pub_date_str = entry.findtext(f'{ATOM_NS}updated', '') or entry.findtext(f'{ATOM_NS}published', '')

        pub_date = None
        if pub_date_str:
            try:
                dt_str = pub_date_str
                if dt_str.endswith('Z'):
                    dt_str = dt_str[:-1] + '+00:00'
                pub_date = _normalize_date(datetime.fromisoformat(dt_str))
            except Exception:
                pass

        if since and pub_date and pub_date < since:
            continue

        summary_text = entry.findtext(f'{ATOM_NS}summary', '')

        content = None
        if full_content:
            elem = entry.find(f'{ATOM_NS}content')
            if elem is not None and elem.text:
                content = strip_html(elem.text)

        summary = strip_html(summary_text) if summary_text else ''
        items.append({
            "title": title,
            "url": link,
            "link": link,
            "published_date": pub_date,
            "date_str": pub_date_str,
            "summary": summary[:300] + "..." if len(summary) > 300 else summary,
            "content": content,
        })

        if limit and len(items) >= limit:
            break

    return items


def parse_feed_xml(xml_bytes, limit=None, full_content=False, since=None):
    """从字节解析 RSS/Atom/RDF Feed，返回文章字典列表。"""
    root = safe_parse_xml_string(xml_bytes)

    # RSS 2.0
    channel = root.find('channel')
    if channel is not None:
        return _parse_rss_items(channel, limit=limit, full_content=full_content, since=since)

    # Atom
    if root.tag == f'{ATOM_NS}feed' or root.findall(f'{ATOM_NS}entry'):
        return _parse_atom_entries(root, limit=limit, full_content=full_content, since=since)

    # RSS 1.0 / RDF 回退
    rdf_items = root.findall(f'{RDF_NS}item')
    if rdf_items:
        channel_elem = ET.Element('channel')
        for ri in rdf_items:
            item_elem = ET.SubElement(channel_elem, 'item')
            for child in ri:
                tag = child.tag.replace(RDF_NS, '')
                sub = ET.SubElement(item_elem, tag)
                sub.text = child.text
        return _parse_rss_items(channel_elem, limit=limit, full_content=full_content, since=since)

    return []


# ---------------------------------------------------------------------------
# Feed 自动发现（参照 blogwatcher 模式）
# ---------------------------------------------------------------------------

def _extract_feed_links_from_html(html_text, base_url):
    """解析 HTML 查找 <link rel="alternate"> Feed URL。"""
    urls = []
    # 使用简单正则查找 link 标签（避免为此引入 bs4）
    pattern = re.compile(
        r'<link\s[^>]*?rel=["\']alternate["\'][^>]*?>',
        re.IGNORECASE | re.DOTALL
    )
    for match in pattern.finditer(html_text):
        tag = match.group(0)
        # 检查 type 属性
        type_match = re.search(r'type=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        href_match = re.search(r'href=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if type_match and href_match:
            link_type = type_match.group(1).lower().strip()
            href = href_match.group(1).strip()
            if link_type in FEED_LINK_TYPES and href:
                urls.append(urljoin(base_url, href))
    return urls


def _is_valid_feed(url, timeout=10):
    """检查 URL 是否返回有效的 RSS/Atom Feed。"""
    try:
        resp = fetch_url(url, timeout=timeout, retries=1)
        if resp.status_code != 200:
            return False
        content_type = resp.headers.get('Content-Type', '').lower()
        if 'xml' in content_type or 'rss' in content_type or 'atom' in content_type:
            return True
        text = resp.text[:500]
        return text.strip().startswith('<?xml') or '<rss' in text or '<feed' in text
    except Exception:
        return False


DISCOVER_TIMEOUT = 30  # discover_feed_url 总时间预算（秒）


def discover_feed_url(page_url, _timeout=DISCOVER_TIMEOUT):
    """给定博客主页 URL，尝试发现其 RSS/Atom Feed URL。
    返回 Feed URL 字符串，或 None。
    _timeout 控制整个发现过程的总时间预算。"""
    deadline = time.monotonic() + _timeout

    try:
        resp = fetch_url(page_url, timeout=min(10, _timeout))
        if resp.status_code != 200:
            return None
    except Exception:
        return None

    # 检查 URL 本身是否为 Feed
    content_type = resp.headers.get('Content-Type', '').lower()
    if 'xml' in content_type or 'rss' in content_type or 'atom' in content_type:
        return page_url

    text = resp.text[:1000]
    if text.strip().startswith('<?xml') or '<rss' in text or '<feed' in text:
        return page_url

    # 搜索 <link rel="alternate"> 标签
    candidates = _extract_feed_links_from_html(resp.text, page_url)
    for url in candidates:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return None  # 时间预算耗尽
        if _is_valid_feed(url, timeout=min(10, remaining)):
            return url

    # 尝试常见路径
    parsed = urlparse(page_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    for path in COMMON_FEED_PATHS:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return None  # 时间预算耗尽
        candidate = base + path
        if _is_valid_feed(candidate, timeout=min(10, remaining)):
            return candidate

    return None


# ---------------------------------------------------------------------------
# HTML 抓取回退（参照 blogwatcher 模式）
# ---------------------------------------------------------------------------

def scrape_articles_html(page_url, css_selector):
    """使用 CSS 选择器从 HTML 页面抓取文章。
    返回 {title, url} 字典列表。"""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return []

    try:
        resp = fetch_url(page_url)
        if resp.status_code != 200:
            return []
    except Exception:
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    elements = soup.select(css_selector)

    articles = []
    seen_urls = set()

    for elem in elements:
        # 查找链接
        link_tag = elem if elem.name == 'a' else elem.find('a')
        if not link_tag or not link_tag.get('href'):
            continue

        href = link_tag['href'].strip()
        if not href or href.startswith('#') or href.startswith('javascript:'):
            continue

        article_url = urljoin(page_url, href)
        if article_url in seen_urls:
            continue
        seen_urls.add(article_url)

        # 提取标题
        title = (
            link_tag.get_text(strip=True)
            or link_tag.get('title', '')
            or elem.get_text(strip=True)
            or 'Untitled'
        )

        articles.append({
            "title": title,
            "url": article_url,
            "summary": None,
            "content": None,
            "published_date": None,
        })

    return articles


# ---------------------------------------------------------------------------
# 扫描（参照 blogwatcher 模式）
# ---------------------------------------------------------------------------

class ScanResult:
    """单个博客的扫描结果。"""

    def __init__(self, blog_name, blog_id):
        self.blog_name = blog_name
        self.blog_id = blog_id
        self.new_articles = 0
        self.total_found = 0
        self.source = "none"  # "rss", "scraper", or "none"
        self.error = None
        self.discovered_feed_url = None  # 自动发现 Feed 时设置

    def __repr__(self):
        return (f"ScanResult({self.blog_name}: {self.new_articles} new / "
                f"{self.total_found} total, source={self.source})")


def scan_blog(blog, full_content=False):
    """扫描单个博客获取文章。
    blog: 包含 id, name, url, feed_url, scrape_selector 键的字典。
    返回 ScanResult。"""
    result = ScanResult(blog['name'], blog['id'])
    articles = []
    feed_url = blog.get('feed_url', '')

    # 第一步：尝试 RSS/Atom Feed
    if feed_url:
        try:
            resp = fetch_url(feed_url)
            if resp.status_code == 200:
                articles = parse_feed_xml(resp.content, full_content=full_content)
                if articles:
                    result.source = "rss"
                else:
                    result.error = "RSS feed returned no items"
            else:
                result.error = f"HTTP {resp.status_code} from {feed_url}"
        except Exception as e:
            result.error = f"RSS fetch failed: {str(e)[:80]}"

    # 第二步：如果没有 feed_url，尝试自动发现
    if not feed_url and blog.get('url'):
        discovered = discover_feed_url(blog['url'])
        if discovered:
            result.discovered_feed_url = discovered
            try:
                resp = fetch_url(discovered)
                if resp.status_code == 200:
                    articles = parse_feed_xml(resp.content, full_content=full_content)
                    if articles:
                        result.source = "rss"
                    else:
                        result.error = "Discovered feed returned no items"
                else:
                    result.error = f"HTTP {resp.status_code} from {discovered}"
            except Exception as e:
                result.error = f"Feed fetch failed: {str(e)[:80]}"

    # 第三步：回退到 HTML 抓取
    if not articles and blog.get('scrape_selector'):
        try:
            articles = scrape_articles_html(blog['url'], blog['scrape_selector'])
            if articles:
                result.source = "scraper"
                result.error = None  # 抓取成功，清除 RSS 错误
        except Exception as e:
            err = f"Scrape failed: {str(e)[:80]}"
            result.error = f"{result.error}; {err}" if result.error else err

    # 扫描内按 URL 去重
    seen = set()
    unique_articles = []
    for art in articles:
        url = art.get('url', '')
        if url and url not in seen:
            seen.add(url)
            unique_articles.append(art)

    result.total_found = len(unique_articles)
    return result, unique_articles


def scan_all(blogs, workers=5, full_content=False, on_progress=None):
    """并发扫描多个博客。
    返回按原始顺序排列的 (ScanResult, articles_list) 元组列表。"""
    if not blogs:
        return []

    results = [None] * len(blogs)

    def _scan_one(index, blog):
        result, articles = scan_blog(blog, full_content=full_content)
        if on_progress:
            on_progress(result)
        return index, result, articles

    max_workers = min(workers, len(blogs))
    total_timeout = min(90 * len(blogs), 300)

    if max_workers <= 1:
        for i, blog in enumerate(blogs):
            idx, result, articles = _scan_one(i, blog)
            results[idx] = (result, articles)
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(_scan_one, i, blog): i
                for i, blog in enumerate(blogs)
            }
            try:
                for future in as_completed(futures, timeout=total_timeout):
                    try:
                        idx, result, articles = future.result(timeout=5)
                        results[idx] = (result, articles)
                    except TimeoutError:
                        idx = futures[future]
                        blog = blogs[idx]
                        err_result = ScanResult(blog.get('name', '?'), blog.get('id', 0))
                        err_result.error = "扫描超时"
                        results[idx] = (err_result, [])
                    except Exception as e:
                        idx = futures[future]
                        blog = blogs[idx]
                        err_result = ScanResult(blog.get('name', '?'), blog.get('id', 0))
                        err_result.error = str(e)[:80]
                        results[idx] = (err_result, [])
            except TimeoutError:
                # as_completed 总超时：将所有未完成的 future 标记为超时
                for future, idx in futures.items():
                    if results[idx] is None:
                        blog = blogs[idx]
                        err_result = ScanResult(blog.get('name', '?'), blog.get('id', 0))
                        err_result.error = "扫描超时"
                        results[idx] = (err_result, [])
                        future.cancel()

    return results
