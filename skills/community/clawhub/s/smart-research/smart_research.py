"""
smart-research 核心脚本
统一入口：research / search / fetch / deep_search

多引擎搜索 → 多级降级抓取 → 结构化融合
"""

import time
import re
import logging
import asyncio
from typing import Any, Dict, List, Optional, Literal
from urllib.parse import urlparse
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

# ===========================
# 日志配置
# ===========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("smart_research")

# ===========================
# 枚举定义
# ===========================
class SearchEngine(Enum):
    BAIDU = "baidu"
    DUCKDUCKGO = "duckduckgo"
    BING = "bing"


class FetcherName(Enum):
    CRAWL4AI = "crawl4ai"
    JINA = "jina"
    MARKDOWN_NEW = "markdown_new"
    DEFUDDLE = "defuddle"
    PLAYWRIGHT = "playwright"


class TrustLevel(Enum):
    TRUSTED = "trusted"
    NORMAL = "normal"
    LOW_QUALITY = "low"


# ===========================
# 数据类型
# ===========================
@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    engine: str
    rank: int = 0
    score: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    is_trusted: bool = False
    favicon: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "engine": self.engine,
            "rank": self.rank,
            "score": self.score,
            "timestamp": self.timestamp.isoformat(),
            "is_trusted": self.is_trusted,
            "favicon": self.favicon,
            "metadata": self.metadata,
        }


@dataclass
class FetchResult:
    url: str
    success: bool
    content: Optional[str] = None
    html: Optional[str] = None
    title: Optional[str] = None
    favicon: Optional[str] = None
    error: Optional[str] = None
    fetcher_name: str = ""
    fetch_time_ms: int = 0
    status_code: int = 0
    redirect_count: int = 0

    @property
    def is_success(self) -> bool:
        return self.success and self.content is not None


@dataclass
class ResearchResult:
    query: str
    results: List[SearchResult] = field(default_factory=list)
    fetched_contents: Dict[str, str] = field(default_factory=dict)
    fusion_metadata: dict = field(default_factory=dict)
    total_results: int = 0
    engines_used: List[str] = field(default_factory=list)
    execution_time_ms: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "total_results": self.total_results,
            "engines_used": self.engines_used,
            "execution_time_ms": self.execution_time_ms,
            "timestamp": self.timestamp.isoformat(),
            "results": [r.to_dict() for r in self.results],
            "fetched_contents": self.fetched_contents,
            "fusion_metadata": self.fusion_metadata,
            "errors": self.errors,
        }


# ===========================
# 异常体系
# ===========================
class SmartResearchError(Exception):
    """基础异常"""
    pass


class SearchError(SmartResearchError):
    """搜索失败"""
    pass


class FetchError(SmartResearchError):
    """抓取失败"""
    pass


# ===========================
# 配置
# ===========================
DEFAULT_CONFIG = {
    "search_engines": ["baidu", "duckduckgo", "bing"],
    "search_timeout": 10,
    "max_results_per_engine": 10,
    "fetch_timeouts": {
        "crawl4ai": 15,
        "jina": 10,
        "markdown_new": 8,
        "defuddle": 8,
        "playwright": 30,
    },
    "fetcher_fallback_order": [
        "crawl4ai", "jina", "markdown_new", "defuddle", "playwright"
    ],
    "top_k": 20,
    "default_output_format": "dict",
}

# 引擎权威性权重
ENGINE_AUTHORITY = {
    "baidu": 0.8,
    "bing": 0.85,
    "duckduckgo": 0.9,
}

# 可信域名白名单
TRUSTED_DOMAINS = [
    r"github\.com",
    r"wikipedia\.org",
    r"zhihu\.com",
    r"stackoverflow\.com",
    r"docs\.python\.org",
    r"developer\.mozilla\.org",
    r"cnblogs\.com",
    r"csdn\.net",
    r"aliyun\.com",
    r"tencent\.com",
    r"baidu\.com",
    r"juejin\.cn",
    r"toutiao\.com",
]

# 低质量域名黑名单
LOW_QUALITY_DOMAINS = [
    r"\.click$",
    r"\.xyz$",
    r"\.top$",
    r"\.work\.tw$",
]

# ===========================
# 搜索层实现
# ===========================

def _make_result(
    engine: str,
    title: str,
    url: str,
    snippet: str,
    rank: int = 0,
) -> SearchResult:
    return SearchResult(
        title=title,
        url=url,
        snippet=snippet,
        engine=engine,
        rank=rank,
    )


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def _check_trusted(url: str) -> bool:
    domain = urlparse(url).netloc
    for pattern in TRUSTED_DOMAINS:
        if re.search(pattern, domain):
            return True
    return False


# ---- 百度搜索 ----
def search_baidu(query: str, num_results: int = 10) -> List[SearchResult]:
    """百度搜索（三层降级：baidusearch → Playwright → requests）"""
    results: List[SearchResult] = []

    # 第一层：baidusearch
    try:
        from baidusearch.baidusearch import search as baidu_search
        raw = baidu_search(query, num_results=num_results)
        results = [
            _make_result(
                "baidu",
                r.get("title", ""),
                r.get("url", ""),
                r.get("abstract", r.get("description", "")),
                i,
            )
            for i, r in enumerate(raw)
            if r.get("url")
        ]
        logger.info(f"[baidu] baidusearch 成功，返回 {len(results)} 条")
        return results
    except ImportError:
        logger.warning("[baidu] baidusearch 未安装，降级到 requests")
    except Exception as e:
        logger.warning(f"[baidu] baidusearch 失败: {e}，降级到 requests")

    # 第二层：requests（正则解析）
    try:
        import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        resp = requests.get(
            f"https://www.baidu.com/s?wd={query}&rn={num_results}",
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        resp.encoding = "utf-8"

        pattern = re.compile(
            r'<h3 class="t">.*?<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>.*?'
            r'<p class="c-abstract">(.*?)</p>',
            re.DOTALL,
        )
        for i, m in enumerate(pattern.finditer(resp.text)):
            if i >= num_results:
                break
            url = m.group(1).strip()
            title = _strip_html(m.group(2))
            snippet = _strip_html(m.group(3))
            if url:
                results.append(_make_result("baidu", title, url, snippet, i))

        logger.info(f"[baidu] requests 成功，返回 {len(results)} 条")
        return results
    except Exception as e:
        logger.warning(f"[baidu] requests 失败: {e}，降级到 Playwright")

    # 第三层：Playwright
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(
                f"https://www.baidu.com/s?wd={query}&rn={num_results}",
                timeout=15000,
                wait_until="networkidle",
            )
            time.sleep(1)
            items = page.query_selector_all("h3.t > a")
            for i, item in enumerate(items[:num_results]):
                title = item.inner_text()
                url = item.get_attribute("href")
                if url:
                    results.append(_make_result("baidu", title, url, "", i))
            browser.close()

        logger.info(f"[baidu] Playwright 成功，返回 {len(results)} 条")
        return results
    except Exception as e:
        logger.warning(f"[baidu] Playwright 失败: {e}")
        raise SearchError(f"百度搜索全部失败: {e}")


# ---- DuckDuckGo 搜索 ----
def search_duckduckgo(query: str, num_results: int = 10) -> List[SearchResult]:
    """DuckDuckGo 搜索"""
    try:
        import requests

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html",
        }
        resp = requests.get(
            "https://lite.duckduckgo.com/lite/",
            params={"q": query},
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()

        results: List[SearchResult] = []
        # 解析搜索结果
        link_pattern = re.compile(r'<a class="result-link"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL)
        snippet_pattern = re.compile(r'<a class="result-snippet"[^>]*>(.*?)</a>', re.DOTALL)

        links = list(link_pattern.finditer(resp.text))
        snippets = list(snippet_pattern.finditer(resp.text))

        for i in range(min(len(links), num_results)):
            url = links[i].group(1).strip()
            if not url or url.startswith("/"):
                continue
            title = _strip_html(links[i].group(2))
            snippet = ""
            if i < len(snippets):
                snippet = _strip_html(snippets[i].group(1))
            results.append(_make_result("duckduckgo", title, url, snippet, i))

        logger.info(f"[duckduckgo] 成功，返回 {len(results)} 条")
        return results
    except Exception as e:
        logger.warning(f"[duckduckgo] 失败: {e}")
        raise SearchError(f"DuckDuckGo 搜索失败: {e}")


# ---- Bing 搜索 ----
def search_bing(query: str, num_results: int = 10) -> List[SearchResult]:
    """Bing 搜索"""
    try:
        import requests

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html",
        }
        resp = requests.get(
            "https://www.bing.com/search",
            params={"q": query, "count": num_results},
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()

        results: List[SearchResult] = []
        pattern = re.compile(
            r'<li class="b_algo".*?<h2><a href="([^"]+)"[^>]*>(.*?)</a></h2>.*?'
            r'<p>(.*?)</p>',
            re.DOTALL,
        )
        for i, m in enumerate(pattern.finditer(resp.text)):
            if i >= num_results:
                break
            url = m.group(1).strip()
            title = _strip_html(m.group(2))
            snippet = _strip_html(m.group(3))
            if url:
                results.append(_make_result("bing", title, url, snippet, i))

        logger.info(f"[bing] 成功，返回 {len(results)} 条")
        return results
    except Exception as e:
        logger.warning(f"[bing] 失败: {e}")
        raise SearchError(f"Bing 搜索失败: {e}")


# ---- 多引擎搜索 ----
def search_all(
    query: str,
    engines: Optional[List[str]] = None,
    num_results: int = 10,
) -> Dict[str, List[SearchResult]]:
    """并发调用所有引擎，返回 {engine: results}"""
    engines = engines or ["baidu", "duckduckgo", "bing"]
    results_by_engine: Dict[str, List[SearchResult]] = {}

    for engine in engines:
        try:
            if engine == "baidu":
                results_by_engine[engine] = search_baidu(query, num_results)
            elif engine == "duckduckgo":
                results_by_engine[engine] = search_duckduckgo(query, num_results)
            elif engine == "bing":
                results_by_engine[engine] = search_bing(query, num_results)
        except SearchError as e:
            logger.warning(f"搜索引擎 {engine} 失败: {e}")
            results_by_engine[engine] = []

    return results_by_engine


# ===========================
# 抓取层实现
# ===========================

# ---- Crawl4AI 抓取 ----
def fetch_crawl4ai(url: str, timeout: int = 15) -> FetchResult:
    """Crawl4AI 抓取（首选，15s超时）"""
    start = time.time()
    try:
        import asyncio
        from crawl4ai import AsyncWebCrawler

        async def _fetch():
            async with AsyncWebCrawler(verbose=False) as crawler:
                return await crawler.arun(url=url)

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(_fetch())
        fetch_time_ms = int((time.time() - start) * 1000)

        if result.success:
            return FetchResult(
                url=url,
                success=True,
                content=result.markdown,
                html=result.html,
                title=result.metadata.get("title") if result.metadata else None,
                fetcher_name="crawl4ai",
                status_code=200,
                fetch_time_ms=fetch_time_ms,
            )
        else:
            return FetchResult(
                url=url,
                success=False,
                error=result.error_message or "Crawl4AI failed",
                fetcher_name="crawl4ai",
                fetch_time_ms=fetch_time_ms,
            )
    except ImportError:
        return FetchResult(
            url=url,
            success=False,
            error="crawl4ai 未安装",
            fetcher_name="crawl4ai",
            fetch_time_ms=int((time.time() - start) * 1000),
        )
    except Exception as e:
        return FetchResult(
            url=url,
            success=False,
            error=str(e),
            fetcher_name="crawl4ai",
            fetch_time_ms=int((time.time() - start) * 1000),
        )


# ---- Jina Reader 抓取 ----
def fetch_jina(url: str, timeout: int = 10) -> FetchResult:
    """Jina Reader 抓取（降级1，10s超时）"""
    start = time.time()
    try:
        import requests

        headers = {
            "Accept": "text/plain",
            "X-Return-Format": "markdown",
        }
        resp = requests.get(
            f"https://r.jina.ai/{url}",
            headers=headers,
            timeout=timeout,
        )
        fetch_time_ms = int((time.time() - start) * 1000)

        if resp.status_code == 200:
            content = resp.text
            title = None
            if content.startswith("#"):
                first_newline = content.find("\n")
                if first_newline > 0:
                    title = content[1:first_newline].strip()
                    content = content[first_newline + 1:].strip()
            return FetchResult(
                url=url,
                success=True,
                content=content,
                title=title,
                fetcher_name="jina",
                status_code=200,
                fetch_time_ms=fetch_time_ms,
            )
        else:
            return FetchResult(
                url=url,
                success=False,
                error=f"Jina 返回状态码 {resp.status_code}",
                fetcher_name="jina",
                status_code=resp.status_code,
                fetch_time_ms=fetch_time_ms,
            )
    except Exception as e:
        return FetchResult(
            url=url,
            success=False,
            error=str(e),
            fetcher_name="jina",
            fetch_time_ms=int((time.time() - start) * 1000),
        )


# ---- markdown.new 抓取 ----
def fetch_markdown_new(url: str, timeout: int = 8) -> FetchResult:
    """markdown.new 抓取（降级2，8s超时）"""
    start = time.time()
    try:
        import requests

        resp = requests.get(
            f"https://markdown.new/{url}",
            headers={
                "Accept": "text/markdown",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            },
            timeout=timeout,
        )
        fetch_time_ms = int((time.time() - start) * 1000)

        if resp.status_code == 200 and len(resp.text) > 100:
            return FetchResult(
                url=url,
                success=True,
                content=resp.text,
                fetcher_name="markdown_new",
                status_code=200,
                fetch_time_ms=fetch_time_ms,
            )
        else:
            return FetchResult(
                url=url,
                success=False,
                error=f"markdown.new 返回状态码 {resp.status_code} 或内容过短",
                fetcher_name="markdown_new",
                status_code=resp.status_code,
                fetch_time_ms=fetch_time_ms,
            )
    except Exception as e:
        return FetchResult(
            url=url,
            success=False,
            error=str(e),
            fetcher_name="markdown_new",
            fetch_time_ms=int((time.time() - start) * 1000),
        )


# ---- Defuddle 抓取 ----
def fetch_defuddle(url: str, timeout: int = 8) -> FetchResult:
    """Defuddle 抓取（降级3，8s超时）"""
    start = time.time()
    try:
        import requests

        resp = requests.get(
            f"https://defuddle.md/{url}",
            headers={
                "Accept": "text/markdown",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            },
            timeout=timeout,
        )
        fetch_time_ms = int((time.time() - start) * 1000)

        if resp.status_code == 200 and len(resp.text) > 100:
            data = resp.json()
            return FetchResult(
                url=url,
                success=True,
                content=resp.text,
                fetcher_name="defuddle",
                status_code=200,
                fetch_time_ms=fetch_time_ms,
            )
        else:
            return FetchResult(
                url=url,
                success=False,
                error=f"Defuddle 返回状态码 {resp.status_code}",
                fetcher_name="defuddle",
                status_code=resp.status_code,
                fetch_time_ms=fetch_time_ms,
            )
    except Exception as e:
        return FetchResult(
            url=url,
            success=False,
            error=str(e),
            fetcher_name="defuddle",
            fetch_time_ms=int((time.time() - start) * 1000),
        )


# ---- Playwright 抓取 ----
def fetch_playwright(url: str, timeout: int = 30) -> FetchResult:
    """Playwright 动态渲染抓取（兜底，30s超时）"""
    start = time.time()
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            executable = "/Users/xudequan/Library/Caches/ms-playwright/chromium-1208/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
            browser = p.chromium.launch(
                headless=True,
                executable_path=executable,
            )
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
            )
            page = context.new_page()
            response = page.goto(url, timeout=timeout * 1000, wait_until="networkidle")
            page.wait_for_load_state("domcontentloaded", timeout=15000)
            time.sleep(1)

            fetch_time_ms = int((time.time() - start) * 1000)
            status_code = response.status if response else 0
            content = page.content()
            title = page.title()

            browser.close()

            return FetchResult(
                url=url,
                success=True,
                content=content,
                html=content,
                title=title,
                fetcher_name="playwright",
                status_code=status_code,
                fetch_time_ms=fetch_time_ms,
            )
    except ImportError:
        return FetchResult(
            url=url,
            success=False,
            error="playwright 未安装",
            fetcher_name="playwright",
            fetch_time_ms=int((time.time() - start) * 1000),
        )
    except Exception as e:
        return FetchResult(
            url=url,
            success=False,
            error=str(e),
            fetcher_name="playwright",
            fetch_time_ms=int((time.time() - start) * 1000),
        )


# ---- 降级链主函数 ----
def fetch_with_fallback(url: str) -> FetchResult:
    """
    多级降级抓取
    降级顺序：crawl4ai → jina → markdown_new → defuddle → playwright
    """
    fetchers = [
        ("crawl4ai", fetch_crawl4ai, 15),
        ("jina", fetch_jina, 10),
        ("markdown_new", fetch_markdown_new, 8),
        ("defuddle", fetch_defuddle, 8),
        ("playwright", fetch_playwright, 30),
    ]

    last_error = None
    for name, fn, timeout in fetchers:
        logger.debug(f"[{name}] 尝试抓取: {url}")
        result = fn(url, timeout)
        if result.is_success:
            logger.info(f"[{name}] 成功抓取: {url} ({result.fetch_time_ms}ms)")
            return result
        last_error = result.error
        logger.debug(f"[{name}] 失败，降级: {last_error}")

    return FetchResult(
        url=url,
        success=False,
        error=last_error or "所有抓取方式均失败",
        fetcher_name="none",
    )


# ===========================
# 融合层实现
# ===========================

def normalize_url(url: str) -> str:
    """URL 归一化：去除追踪参数、协议、尾部斜杠"""
    try:
        parsed = urlparse(url)
        tracking_params = {
            "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
            "fbclid", "gclid", "ref", "source",
        }
        query_params = []
        for param in parsed.query.split("&"):
            if param:
                key = param.split("=")[0].lower()
                if key not in tracking_params:
                    query_params.append(param)
        query = "&".join(query_params)
        path = parsed.path.rstrip("/") or "/"
        return f"{parsed.netloc}{path}?{query}".rstrip("?")
    except Exception:
        return url


def url_similarity(url1: str, url2: str) -> float:
    """计算两个 URL 的相似度（0~1）"""
    n1 = normalize_url(url1)
    n2 = normalize_url(url2)
    if n1 == n2:
        return 1.0
    parsed1, parsed2 = urlparse(url1), urlparse(url2)
    score = 0.0
    if parsed1.netloc == parsed2.netloc:
        score += 0.7
        path1_parts = [p for p in parsed1.path.split("/") if p]
        path2_parts = [p for p in parsed2.path.split("/") if p]
        common = 0
        for p1, p2 in zip(path1_parts, path2_parts):
            if p1 == p2:
                common += 1
            else:
                break
        score += min(0.3, common * 0.15)
    return score


def get_trust_level(url: str) -> TrustLevel:
    """判断 URL 的信任级别"""
    domain = urlparse(url).netloc
    for pattern in TRUSTED_DOMAINS:
        if re.search(pattern, domain):
            return TrustLevel.TRUSTED
    for pattern in LOW_QUALITY_DOMAINS:
        if re.search(pattern, domain):
            return TrustLevel.LOW_QUALITY
    return TrustLevel.NORMAL


def merge_results(results_by_engine: Dict[str, List[SearchResult]]) -> List[SearchResult]:
    """多引擎结果去重合并"""
    all_pairs: List[tuple[SearchResult, str]] = []
    for engine, results in results_by_engine.items():
        for r in results:
            all_pairs.append((r, engine))

    merged: List[SearchResult] = []
    used_indices: set[int] = set()

    for i, (r1, _) in enumerate(all_pairs):
        if i in used_indices:
            continue
        group = [r1]
        used_indices.add(i)

        for j, (r2, _) in enumerate(all_pairs[i + 1:], start=i + 1):
            if j in used_indices:
                continue
            if url_similarity(r1.url, r2.url) > 0.85:
                group.append(r2)
                used_indices.add(j)

        merged.append(group[0])

    return merged


def score_result(result: SearchResult) -> float:
    """计算单条结果的综合评分"""
    base = 50.0
    rank_bonus = max(0, 20 - result.rank * 2)
    engine_authority = ENGINE_AUTHORITY.get(result.engine, 0.7) * 10
    trust = get_trust_level(result.url)
    trust_bonus = {TrustLevel.TRUSTED: 15, TrustLevel.NORMAL: 0, TrustLevel.LOW_QUALITY: -10}[trust]
    snippet_bonus = min(5, len(result.snippet) / 50) if result.snippet else 0

    total = base + rank_bonus + engine_authority + trust_bonus + snippet_bonus
    return round(min(100, max(0, total)), 2)


def score_and_sort(results: List[SearchResult]) -> List[SearchResult]:
    """对结果列表打分并按分数降序排序"""
    for r in results:
        r.score = score_result(r)
        r.is_trusted = _check_trusted(r.url)
    return sorted(results, key=lambda x: x.score, reverse=True)


def format_markdown(
    results: List[SearchResult],
    query: str,
    fusion_metadata: Optional[dict] = None,
) -> str:
    """结构化 Markdown 输出"""
    lines = [
        f"# 搜索结果：{query}",
        f"\n> 共找到 **{len(results)}** 条相关结果",
        "",
    ]

    if fusion_metadata:
        engines = fusion_metadata.get("engines_used", [])
        lines.append(f"> 搜索覆盖：{', '.join(engines)}")
        lines.append("")

    lines.append("---")

    for i, r in enumerate(results, 1):
        trust_tag = ""
        if r.is_trusted:
            trust_tag = " ✅"
        elif r.score < 40:
            trust_tag = " ⚠️"

        lines.append(f"### {i}. {r.title}{trust_tag}")
        lines.append(f"- **链接**：[{r.url}]({r.url})")
        lines.append(f"- **来源**：{r.engine}（排名 #{r.rank + 1}，评分 {r.score}）")
        lines.append(f"- **摘要**：{r.snippet}")
        lines.append("")

    lines.append(f"\n*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    return "\n".join(lines)


def format_json(
    results: List[SearchResult],
    query: str,
    fusion_metadata: Optional[dict] = None,
) -> dict:
    """结构化 JSON 输出"""
    return {
        "query": query,
        "total": len(results),
        "results": [r.to_dict() for r in results],
        "fusion_metadata": fusion_metadata or {},
        "generated_at": datetime.now().isoformat(),
    }


# ===========================
# research 主流程
# ===========================

def research(
    query: str,
    num_results: int = 5,
    crawl_depth: int = 3,
    engines: Optional[List[str]] = None,
    output_format: Literal["dict", "markdown", "json"] = "dict",
) -> ResearchResult | str | dict:
    """
    一键完成搜索 + 抓取 + 融合

    Args:
        query: 搜索关键词
        num_results: 每个引擎返回的结果数量
        crawl_depth: 抓取前 crawl_depth 个 URL（0=不抓取）
        engines: 使用的引擎列表，默认全部
        output_format: 输出格式，"dict" | "markdown" | "json"

    Returns:
        ResearchResult / Markdown 字符串 / JSON dict
    """
    start_time = time.time()
    errors: List[str] = []

    # 1. 多引擎搜索
    results_by_engine = search_all(query, engines=engines, num_results=num_results)
    for eng, res in results_by_engine.items():
        if not res:
            errors.append(f"引擎 {eng} 无结果")

    # 2. 合并去重
    merged = merge_results(results_by_engine)

    # 3. 打分排序
    scored = score_and_sort(merged)

    # 截取 Top K（默认20）
    top_k = DEFAULT_CONFIG.get("top_k", 20)
    final_results = scored[:top_k]

    # 4. 抓取页面内容（crawl_depth 个 URL）
    # 使用 r.url 作为 key，确保与 r.url 一致（SearchResult.url 可能被截断显示但存储的是完整URL）
    fetched_contents: Dict[str, str] = {}
    if crawl_depth > 0:
        urls_to_fetch = [(r.url, r.url) for r in final_results[:crawl_depth]]
        for orig_url, fetch_url in urls_to_fetch:
            fetch_result = fetch_with_fallback(fetch_url)
            if fetch_result.is_success and fetch_result.content:
                # 清理 HTML 标签
                content = fetch_result.content
                if not content.startswith("#") and "<" in content[:100]:
                    content = _strip_html(content)
                fetched_contents[orig_url] = content

    execution_time_ms = int((time.time() - start_time) * 1000)

    research_result = ResearchResult(
        query=query,
        results=final_results,
        fetched_contents=fetched_contents,
        fusion_metadata={
            "engines_used": list(results_by_engine.keys()),
            "total_raw": sum(len(v) for v in results_by_engine.values()),
            "after_dedup": len(merged),
        },
        total_results=len(final_results),
        engines_used=list(results_by_engine.keys()),
        execution_time_ms=execution_time_ms,
        errors=errors,
    )

    # 5. 格式化输出
    if output_format == "markdown":
        return format_markdown(final_results, query, research_result.fusion_metadata)
    elif output_format == "json":
        return format_json(final_results, query, research_result.fusion_metadata)
    else:
        return research_result


# ===========================
# 便捷单函数
# ===========================

def smart_search(query: str, engine: str = "baidu", num_results: int = 10) -> List[SearchResult]:
    """单引擎搜索便捷函数"""
    try:
        if engine == "baidu":
            return search_baidu(query, num_results)
        elif engine == "duckduckgo":
            return search_duckduckgo(query, num_results)
        elif engine == "bing":
            return search_bing(query, num_results)
        else:
            raise ValueError(f"未知引擎: {engine}")
    except SearchError as e:
        logger.error(f"[{engine}] 搜索失败: {e}")
        return []


def fetch_url(url: str) -> FetchResult:
    """抓取单个 URL，便捷函数"""
    return fetch_with_fallback(url)


def deep_search(
    query: str,
    num_results: int = 10,
    crawl_depth: int = 3,
) -> ResearchResult:
    """deep_search = research（保留别名）"""
    return research(query, num_results=num_results, crawl_depth=crawl_depth, output_format="dict")


# ===========================
# 统一入口
# ===========================

def main(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    统一入口，支持 actions: research / search / fetch / deep_search

    Args:
        input_data: {
            "action": "research" | "search" | "fetch" | "deep_search",
            "query": str,
            "num_results": int,
            "crawl_depth": int,
            "engine": str,         # 仅 search action
            "engines": list,       # 仅 research/deep_search
            "output_format": str,
            "url": str,            # 仅 fetch action
        }

    Returns:
        结构化结果 dict
    """
    action = input_data.get("action", "research")
    query = input_data.get("query", "")
    output_format = input_data.get("output_format", "dict")

    if not query and action != "fetch":
        return {"error": "query 不能为空"}

    try:
        if action == "research":
            result = research(
                query=query,
                num_results=input_data.get("num_results", 5),
                crawl_depth=input_data.get("crawl_depth", 3),
                engines=input_data.get("engines"),
                output_format=output_format,
            )

        elif action == "search":
            engine = input_data.get("engine", "baidu")
            results = smart_search(
                query=query,
                engine=engine,
                num_results=input_data.get("num_results", 10),
            )
            if output_format == "json":
                result = format_json(results, query)
            elif output_format == "markdown":
                result = format_markdown(results, query)
            else:
                result = {"query": query, "engine": engine, "success": True, "results": [r.to_dict() for r in results], "message": "Search completed"}

        elif action == "fetch":
            url = input_data.get("url", "")
            if not url:
                return {"error": "url 不能为空"}
            fetch_result = fetch_with_fallback(url)
            result = {
                "url": url,
                "success": fetch_result.is_success,
                "content": fetch_result.content,
                "title": fetch_result.title,
                "source": fetch_result.fetcher_name,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "fetch_time_ms": fetch_result.fetch_time_ms,
                "error": fetch_result.error,
            }

        elif action == "deep_search":
            result = deep_search(
                query=query,
                num_results=input_data.get("num_results", 10),
                crawl_depth=input_data.get("crawl_depth", 3),
            )
            if output_format in ("markdown", "json"):
                result = research(
                    query=query,
                    num_results=input_data.get("num_results", 10),
                    crawl_depth=input_data.get("crawl_depth", 3),
                    output_format=output_format,
                )
        else:
            return {"error": f"未知 action: {action}"}

        return result if isinstance(result, dict) else result.to_dict()

    except Exception as e:
        logger.exception(f"[{action}] 执行失败: {e}")
        return {"error": str(e)}


# ===========================
# CLI 入口
# ===========================

if __name__ == "__main__":
    import json, sys

    if len(sys.argv) < 2:
        print("用法: python smart_research.py <json_input>")
        print("示例: python smart_research.py '{\"action\":\"search\",\"query\":\"Python教程\",\"engine\":\"baidu\"}'")
        sys.exit(1)

    try:
        input_data = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("JSON 解析失败")
        sys.exit(1)

    result = main(input_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
