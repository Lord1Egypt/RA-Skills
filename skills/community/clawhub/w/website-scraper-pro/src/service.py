# pyright: reportMissingImports=false

import asyncio
import io
import json
from contextlib import redirect_stderr, redirect_stdout
from typing import Any

from constants import (
    BM25_THRESHOLD,
    DEFAULT_DELAY_BEFORE_RETURN_HTML,
    DEFAULT_PAGE_TIMEOUT_MS,
    DEFAULT_WAIT_FOR,
    DEFAULT_WAIT_UNTIL,
    DEFAULT_WORD_COUNT_THRESHOLD,
    EXCLUDED_TAGS,
    JS_DELAY_BEFORE_RETURN_HTML,
    JS_PAGE_TIMEOUT_MS,
    JS_WAIT_FOR,
    JS_SCROLL_DELAY_SECONDS,
    JS_WAIT_UNTIL,
    PRUNING_MIN_WORD_THRESHOLD,
    PRUNING_THRESHOLD,
    PRUNING_THRESHOLD_TYPE,
    QUERY_FALLBACK_MIN_LENGTH,
)
from utils import (
    build_setup_error,
    clean_markdown,
    looks_like_browser_setup_error,
    normalize_links,
    select_relevant_markdown,
    to_json_safe,
)

try:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
    from crawl4ai.content_filter_strategy import BM25ContentFilter, PruningContentFilter
    from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

    CRAWL4AI_IMPORT_ERROR = None
except ImportError as exc:
    AsyncWebCrawler = None  # type: Any
    BrowserConfig = None  # type: Any
    CacheMode = None  # type: Any
    CrawlerRunConfig = None  # type: Any
    BM25ContentFilter = None  # type: Any
    PruningContentFilter = None  # type: Any
    DefaultMarkdownGenerator = None  # type: Any
    CRAWL4AI_IMPORT_ERROR = exc


def build_markdown_generator(query: str | None):
    """Build the markdown generator for default or query-focused retrieval."""
    if query:
        content_filter = BM25ContentFilter(
            user_query=query,
            bm25_threshold=BM25_THRESHOLD,
        )
    else:
        content_filter = PruningContentFilter(
            threshold=PRUNING_THRESHOLD,
            threshold_type=PRUNING_THRESHOLD_TYPE,
            min_word_threshold=PRUNING_MIN_WORD_THRESHOLD,
        )

    return DefaultMarkdownGenerator(content_filter=content_filter)


def build_run_config(use_js: bool, query: str | None):
    """Build the Crawl4AI run configuration."""
    config = {
        "cache_mode": CacheMode.BYPASS,
        "word_count_threshold": DEFAULT_WORD_COUNT_THRESHOLD,
        "wait_for": DEFAULT_WAIT_FOR,
        "excluded_tags": EXCLUDED_TAGS,
        "remove_forms": True,
        "markdown_generator": build_markdown_generator(query),
    }

    if use_js:
        config.update(
            {
                "wait_for": JS_WAIT_FOR,
                "wait_until": JS_WAIT_UNTIL,
                "page_timeout": JS_PAGE_TIMEOUT_MS,
                "delay_before_return_html": JS_DELAY_BEFORE_RETURN_HTML,
                "scan_full_page": True,
                "scroll_delay": JS_SCROLL_DELAY_SECONDS,
                "wait_for_images": True,
                "remove_overlay_elements": True,
                "simulate_user": True,
                "magic": True,
            }
        )
    else:
        config.update(
            {
                "wait_until": DEFAULT_WAIT_UNTIL,
                "page_timeout": DEFAULT_PAGE_TIMEOUT_MS,
                "delay_before_return_html": DEFAULT_DELAY_BEFORE_RETURN_HTML,
            }
        )

    return CrawlerRunConfig(**config)


def extract_markdown(result, query: str | None) -> tuple[str, str]:
    """Extract the best markdown payload and describe its source."""
    markdown_object = getattr(result, "markdown", None)
    raw_markdown = clean_markdown(getattr(markdown_object, "raw_markdown", ""))
    fit_markdown = clean_markdown(getattr(markdown_object, "fit_markdown", ""))

    if query:
        if len(fit_markdown) >= QUERY_FALLBACK_MIN_LENGTH:
            return fit_markdown, "bm25_fit_markdown"

        fallback_markdown = select_relevant_markdown(raw_markdown, query)
        if fallback_markdown:
            return fallback_markdown, "deterministic_query_fallback"

        if fit_markdown:
            return fit_markdown, "bm25_fit_markdown"
        return raw_markdown, "raw_markdown"

    if fit_markdown:
        return fit_markdown, "pruned_markdown"
    return raw_markdown, "raw_markdown"


async def crawl_page(url: str, use_js: bool, query: str | None) -> dict:
    """Crawl a single page and return structured output."""
    if CRAWL4AI_IMPORT_ERROR is not None:
        return {
            "error": build_setup_error("Crawl4AI is not available in this runtime.")
        }

    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = build_run_config(use_js, query)

    try:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            async with AsyncWebCrawler(config=browser_config, verbose=False) as crawler:
                result = await crawler.arun(url=url, config=run_config)
    except Exception as exc:
        message = str(exc)
        if looks_like_browser_setup_error(message):
            return {
                "error": build_setup_error(
                    "Crawl4AI browser setup is missing or incomplete."
                )
            }
        return {"error": f"Could not scrape {url}: {message}"}

    if not getattr(result, "success", False):
        message = getattr(result, "error_message", "Unknown crawl failure")
        if looks_like_browser_setup_error(message):
            return {
                "error": build_setup_error(
                    "Crawl4AI browser setup is missing or incomplete."
                )
            }
        return {"error": f"Could not scrape {url}: {message}"}

    metadata = to_json_safe(getattr(result, "metadata", {}) or {})
    if not isinstance(metadata, dict):
        metadata = {}
    raw_title = metadata.get("title") or ""
    title = raw_title if isinstance(raw_title, str) else str(raw_title)
    markdown, markdown_source = extract_markdown(result, query)

    return {
        "requested_url": url,
        "url": getattr(result, "url", "") or url,
        "title": title,
        "markdown": markdown,
        "markdown_source": markdown_source,
        "links": normalize_links(getattr(result, "links", {})),
        "metadata": metadata,
        "js_mode": use_js,
        "query": query,
    }


def get_website_scrape(
    url: str,
    use_js: bool,
    query: str | None,
    output_format: str,
) -> dict:
    """Run the website scrape and attach the requested output format."""
    result = asyncio.run(crawl_page(url, use_js, query))
    result["output_format"] = output_format
    return result


def format_output(data: dict) -> str:
    """Format crawl output for markdown or JSON CLI delivery."""
    output_format = data.get("output_format", "markdown")

    if "error" in data:
        if output_format == "json":
            return json.dumps({"error": data["error"]}, indent=2, sort_keys=True)
        return f"Error: {data['error']}"

    if output_format == "json":
        payload = {
            "js_mode": data.get("js_mode", False),
            "links": data.get("links", {"internal": [], "external": []}),
            "markdown": data.get("markdown", ""),
            "markdown_source": data.get("markdown_source", ""),
            "metadata": data.get("metadata", {}),
            "query": data.get("query"),
            "requested_url": data.get("requested_url", ""),
            "title": data.get("title", ""),
            "url": data.get("url", data.get("requested_url", "")),
        }
        return json.dumps(payload, indent=2, sort_keys=True)

    return data.get("markdown", "")
