"""
smart-research scripts package
"""

from .smart_research import (
    # 数据类型
    SearchResult,
    FetchResult,
    ResearchResult,
    # 搜索函数
    search_baidu,
    search_duckduckgo,
    search_bing,
    search_all,
    smart_search,
    # 抓取函数
    fetch_crawl4ai,
    fetch_jina,
    fetch_markdown_new,
    fetch_defuddle,
    fetch_playwright,
    fetch_with_fallback,
    fetch_url,
    # 融合函数
    merge_results,
    score_and_sort,
    format_markdown,
    format_json,
    # 主流程
    research,
    deep_search,
    # 统一入口
    main,
    # 配置
    DEFAULT_CONFIG,
)

__all__ = [
    # 数据类型
    "SearchResult",
    "FetchResult",
    "ResearchResult",
    # 搜索层
    "search_baidu",
    "search_duckduckgo",
    "search_bing",
    "search_all",
    "smart_search",
    # 抓取层
    "fetch_crawl4ai",
    "fetch_jina",
    "fetch_markdown_new",
    "fetch_defuddle",
    "fetch_playwright",
    "fetch_with_fallback",
    "fetch_url",
    # 融合层
    "merge_results",
    "score_and_sort",
    "format_markdown",
    "format_json",
    # 主流程
    "research",
    "deep_search",
    # 统一入口
    "main",
    # 配置
    "DEFAULT_CONFIG",
]
