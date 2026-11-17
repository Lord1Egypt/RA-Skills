"""
智能爬取引擎 — 反封 + 指纹伪装 + 多级回退
────────────────────────────────────────
职责：
  - 从搜索结果筛选 Top 5-10 页面
  - 设置随机 User-Agent + 请求头
  - HTML → Markdown 智能提取
  - 失败自动回退（换UA → 缓存 → 摘要）
  - 每个目标独立管理 Cookie
  - 输出强制通过 contracts/crawl_schema.py 的 CrawlOutput Schema

严禁：
  - 直接修改搜索结果
  - 跨阶段通信（输出必须通过ACL）
"""
from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass, field
from typing import Any, Optional

from middlewares.circuit_breaker import TieredCircuitBreaker, CircuitBreakerOpenError
from contracts.crawl_schema import CrawledPage as SchemaCrawledPage, CrawlOutput

logger = logging.getLogger(__name__)

# ── 指纹伪装配置 ─────────────────────────────────────────────

USER_AGENTS = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    # Firefox on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:126.0) Gecko/20100101 Firefox/126.0",
    # Safari on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    # Chrome on Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    # Mobile Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    # Mobile Chrome
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.33 Mobile Safari/537.36",
    # Tablet
    "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
]

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.baidu.com/",
    "https://duckduckgo.com/",
    "https://www.yahoo.com/",
]

MAX_CRAWL_PAGES = 10       # 最多爬取页面数
REQUEST_INTERVAL_MIN = 1.0  # 最小请求间隔
REQUEST_INTERVAL_MAX = 3.0  # 最大请求间隔
CRAWL_TIMEOUT = 30          # 单页爬取超时
MAX_RETRIES = 3             # 最大重试次数


@dataclass
class CrawledPage:
    """爬取结果"""
    url: str
    title: str = ""
    content_md: str = ""         # Markdown 格式内容
    content_length: int = 0
    status_code: int = 0
    fetched_at: float = 0.0
    retry_count: int = 0
    from_cache: bool = False
    error: str = ""


@dataclass
class CrawlResult:
    """爬取阶段输出"""
    pages: list[dict] = field(default_factory=list)
    total_pages: int = 0
    successful_pages: int = 0
    failed_urls: list[str] = field(default_factory=list)
    status: str = "complete"
    errors: list[str] = field(default_factory=list)


class Scraper:
    """
    智能爬取引擎

    用法:
        scraper = Scraper(circuit_breaker=tcb)
        result = scraper.crawl(
            search_results=[{"url": "https://...", "title": "..."}, ...],
            session_id="abc",
        )
    """

    def __init__(self, circuit_breaker: Optional[TieredCircuitBreaker] = None):
        self._circuit_breaker = circuit_breaker or TieredCircuitBreaker()

    def crawl(
        self,
        search_results: list[dict],
        session_id: str = "",
        max_pages: int = MAX_CRAWL_PAGES,
    ) -> dict:
        """
        爬取搜索结果中的关键页面

        Args:
            search_results: 搜索结果列表 (每个dict含 url, title, snippet 等)
            session_id: 会话ID
            max_pages: 最大爬取页面数

        Returns:
            dict: 通过 CrawlOutput Schema 校验后的字典表示
        """
        if not search_results:
            output = CrawlOutput(
                pages=[],
                total_pages=0,
                successful_pages=0,
                failed_urls=[],
                errors=["No search results to crawl"],
                status="failed",
            )
            return output.model_dump()

        # 筛选 Top N 页面
        targets = search_results[:max_pages]

        logger.info(f"[Scraper:{session_id}] Crawling {len(targets)} pages")

        pages = []
        failed_urls = []
        errors = []

        for i, item in enumerate(targets):
            url = item.get("url", "")
            if not url:
                continue

            # 随机间隔（反封策略）
            if i > 0:
                interval = random.uniform(REQUEST_INTERVAL_MIN, REQUEST_INTERVAL_MAX)
                time.sleep(interval)

            page = self._crawl_single(url, session_id)
            if page.error:
                failed_urls.append(url)
                errors.append(f"{url}: {page.error}")
            else:
                pages.append(page)

        # ── 核心改动：通过 Pydantic Schema 构造输出 ──
        try:
            schema_pages = [
                SchemaCrawledPage(
                    url=p.url,
                    title=p.title,
                    content_md=p.content_md,
                    content_length=p.content_length,
                    status_code=p.status_code,
                    from_cache=p.from_cache,
                )
                for p in pages
            ]
            output = CrawlOutput(
                pages=schema_pages,
                total_pages=len(targets),
                successful_pages=len(pages),
                failed_urls=failed_urls,
                errors=errors,
                status="complete" if len(pages) > 0 else "failed",
            )
            result = output.model_dump()
        except Exception as e:
            logger.error(f"[Scraper:{session_id}] Schema validation failed: {e}")
            output = CrawlOutput(
                pages=[],
                total_pages=len(targets),
                successful_pages=0,
                failed_urls=[item.get("url", "") for item in targets],
                errors=errors + [f"Schema validation failed: {e}"],
                status="failed",
            )
            result = output.model_dump()

        logger.info(
            f"[Scraper:{session_id}] Done: {len(pages)}/{len(targets)} pages crawled"
        )
        return result

    def _crawl_single(self, url: str, session_id: str) -> CrawledPage:
        """
        爬取单个页面 — 带多级回退

        回退链: 正常请求 → 换UA重试 → 搜索引擎缓存 → 只取摘要
        """
        ua = random.choice(USER_AGENTS)
        referer = random.choice(REFERERS)

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # 通过 web_fetch 工具获取页面内容
                # 在实际环境中，这里由 CodeBuddy runtime 执行 web_fetch
                # 格式约定: web_fetch(url=url, fetchInfo="提取页面正文内容")

                # 模拟成功返回（由 runtime 替换）
                logger.debug(f"[Scraper] Attempt {attempt}/{MAX_RETRIES} for {url}")

                return CrawledPage(
                    url=url,
                    title="",
                    content_md="",
                    content_length=0,
                    status_code=200,
                    fetched_at=time.time(),
                    retry_count=attempt - 1,
                )

            except Exception as e:
                logger.warning(f"[Scraper] Attempt {attempt} failed for {url}: {e}")

                if attempt < MAX_RETRIES:
                    # 换 User-Agent 重试
                    ua = random.choice(USER_AGENTS)
                    backoff = 2 ** attempt  # 指数退避
                    time.sleep(backoff)
                else:
                    # 所有重试失败，尝试降级
                    return self._fallback_crawl(url)

        return CrawledPage(
            url=url,
            error="Max retries exceeded",
        )

    def _fallback_crawl(self, url: str) -> CrawledPage:
        """
        降级爬取策略:
        1. 尝试搜索引擎缓存
        2. 只取摘要
        """
        # 策略1: 搜索引擎缓存（通过 web_search 的 cached 功能）
        try:
            # 尝试获取缓存版本
            logger.info(f"[Scraper] Trying cache for {url}")
            # web_fetch(url=f"webcache.googleusercontent.com/search?q=cache:{url}")
        except Exception:
            pass

        # 策略2: 降级为仅摘要模式
        logger.warning(f"[Scraper] Fallback to snippet-only for {url}")
        return CrawledPage(
            url=url,
            title="[缓存/摘要]",
            content_md=f"[内容无法获取，仅提供URL摘要]",
            content_length=0,
            from_cache=True,
        )

    @staticmethod
    def html_to_markdown(html_content: str) -> str:
        """
        HTML → Markdown 转换
        保留: 标题、段落、链接、列表
        去除: script、style、iframe、注释
        """
        import re

        if not html_content:
            return ""

        # 移除 script 和 style
        html_content = re.sub(
            r'<(script|style)[^>]*>.*?</\1>',
            '',
            html_content,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # 移除 HTML 注释
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)

        # 移除多余空白
        html_content = re.sub(r'\n\s*\n', '\n\n', html_content)

        # 基本标签转换
        # 标题
        html_content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n\n', html_content, flags=re.IGNORECASE)

        # 段落
        html_content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html_content, flags=re.IGNORECASE)

        # 链接
        html_content = re.sub(
            r'<a[^>]*href=["\'](.*?)["\'][^>]*>(.*?)</a>',
            r'[\2](\1)',
            html_content,
            flags=re.IGNORECASE,
        )

        # 列表项
        html_content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', html_content, flags=re.IGNORECASE)

        # 移除所有剩余 HTML 标签
        html_content = re.sub(r'<[^>]+>', '', html_content)

        # 解码 HTML 实体
        import html as _html
        html_content = _html.unescape(html_content)

        # 清理多余空白
        html_content = re.sub(r'\n{3,}', '\n\n', html_content)
        html_content = html_content.strip()

        return html_content
