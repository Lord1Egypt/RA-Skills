"""
Pytest 配置 — 通用 fixtures
"""
import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_dir():
    """创建临时目录"""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def sample_search_results():
    """样本搜索结果"""
    return [
        {
            "url": "https://example.com/article1",
            "title": "AI发展趋势2026",
            "snippet": "人工智能在2026年将继续快速发展...",
            "source_engine": "baidu",
            "source_region": "cn",
            "rank": 1,
        },
        {
            "url": "https://techcrunch.com/ai-report",
            "title": "AI Industry Report",
            "snippet": "The AI industry is growing at an unprecedented rate...",
            "source_engine": "google",
            "source_region": "global",
            "rank": 1,
        },
        {
            "url": "https://example.com/article2",
            "title": "机器学习最新进展",
            "snippet": "深度学习模型在多个领域取得突破...",
            "source_engine": "bing_cn",
            "source_region": "cn",
            "rank": 2,
        },
    ]


@pytest.fixture
def sample_crawled_pages():
    """样本爬取页面"""
    return [
        {
            "url": "https://example.com/article1",
            "title": "AI发展趋势2026",
            "content_md": "# AI发展趋势2026\n\n人工智能在2026年将继续快速发展。深度学习和自然语言处理技术不断进步。",
            "content_length": 150,
            "status_code": 200,
            "from_cache": False,
        },
        {
            "url": "https://techcrunch.com/ai-report",
            "title": "AI Industry Report",
            "content_md": "# AI Industry Report\n\nThe AI industry is growing at an unprecedented rate.",
            "content_length": 100,
            "status_code": 200,
            "from_cache": False,
        },
    ]
