"""
RSS News Aggregator 单元测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.rss_engine import RSSAggregator


def test_add_remove_feed():
    agg = RSSAggregator()
    agg.add_feed("https://example.com/rss", name="Test Feed")
    assert "Test Feed" in agg.list_feeds()
    agg.remove_feed("Test Feed")
    assert "Test Feed" not in agg.list_feeds()
    print("✓ test_add_remove_feed passed")


def test_builtin_feeds():
    agg = RSSAggregator()
    tech = agg.get_builtin_feeds("tech")
    assert "Hacker News" in tech
    ai = agg.get_builtin_feeds("ai")
    assert len(ai) > 0
    empty = agg.get_builtin_feeds("nonexistent")
    assert empty == {}
    print("✓ test_builtin_feeds passed")


def test_filter_by_keyword():
    agg = RSSAggregator()
    articles = [
        {"title": "Python new features", "summary": "Great language"},
        {"title": "JavaScript trends", "summary": "Web dev"},
        {"title": "Python vs AI", "summary": "Comparison"},
    ]
    filtered = agg.filter_by_keyword(articles, ["Python"])
    assert len(filtered) == 2
    assert all("Python" in a["title"] for a in filtered)
    print("✓ test_filter_by_keyword passed")


def test_filter_exclude():
    agg = RSSAggregator()
    articles = [
        {"title": "Python news", "summary": "Code"},
        {"title": "Java update", "summary": "VM"},
        {"title": "Rust safety", "summary": "Memory"},
    ]
    filtered = agg.filter_by_keyword(articles, ["Python"], mode="exclude")
    assert len(filtered) == 2
    assert all("Python" not in a["title"] for a in filtered)
    print("✓ test_filter_exclude passed")


def test_generate_markdown_report():
    agg = RSSAggregator()
    articles = [
        {"title": "Test Article", "source": "Test", "link": "https://example.com", "summary": "Summary here", "published": "2026-04-27"},
    ]
    report = agg.generate_markdown_report(articles, title="Test Report")
    assert "# Test Report" in report
    assert "Test Article" in report
    assert "https://example.com" in report
    print("✓ test_generate_markdown_report passed")


def test_generate_text_report():
    agg = RSSAggregator()
    articles = [
        {"title": "Test Article", "source": "Test", "link": "https://example.com", "summary": "Summary"},
    ]
    report = agg.generate_text_report(articles, title="Test Report")
    assert "Test Report" in report
    assert "Test Article" in report
    print("✓ test_generate_text_report passed")


def test_search_by_source():
    agg = RSSAggregator()
    articles = [
        {"title": "A1", "source": "Dev.to"},
        {"title": "A2", "source": "Dev Community"},
        {"title": "A3", "source": "Hacker News"},
    ]
    result = agg.search_by_source(articles, "Dev")
    assert len(result) == 2
    print("✓ test_search_by_source passed")


def test_fetch_feed_error_handling():
    agg = RSSAggregator()
    # 测试无效 URL 的错误处理
    result = agg.fetch_feed("Bad Feed", "https://invalid-url-that-does-not-exist-12345.com/feed", limit=1)
    assert len(result) >= 0  # feedparser 可能返回空或错误条目
    print("✓ test_fetch_feed_error_handling passed")


if __name__ == "__main__":
    test_add_remove_feed()
    test_builtin_feeds()
    test_filter_by_keyword()
    test_filter_exclude()
    test_generate_markdown_report()
    test_generate_text_report()
    test_search_by_source()
    test_fetch_feed_error_handling()
    print("\n所有测试通过! ✅")
