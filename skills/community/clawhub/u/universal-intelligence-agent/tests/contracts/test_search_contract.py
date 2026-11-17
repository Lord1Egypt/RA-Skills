"""
契约测试 — 搜索阶段
────────────────────
验证 SearchRequest/SearchHit/SearchOutput 的类型校验。
"""
import pytest
from contracts.search_schema import (
    SearchRequest,
    SearchHit,
    SearchBatch,
    SearchOutput,
    QueryIntent,
    QueryLanguage,
)


class TestSearchRequest:
    """SearchRequest 契约测试"""

    def test_valid_request(self):
        """有效请求应通过校验"""
        req = SearchRequest(query="AI趋势分析", intent=QueryIntent.DEEP)
        assert req.query == "AI趋势分析"
        assert req.intent == QueryIntent.DEEP
        assert req.max_results == 100
        assert req.engine_group == "all"

    def test_query_too_short(self):
        """查询过短应拒绝"""
        with pytest.raises(ValueError, match="查询内容过短"):
            SearchRequest(query="A")

    def test_query_empty(self):
        """空查询应拒绝"""
        with pytest.raises(ValueError):
            SearchRequest(query="")

    def test_query_too_long(self):
        """超长查询应拒绝"""
        with pytest.raises(ValueError):
            SearchRequest(query="A" * 501)

    def test_max_results_out_of_range_low(self):
        """max_results 低于最小值应拒绝"""
        with pytest.raises(ValueError):
            SearchRequest(query="test", max_results=5)

    def test_max_results_out_of_range_high(self):
        """max_results 超过最大值应拒绝"""
        with pytest.raises(ValueError):
            SearchRequest(query="test", max_results=501)

    def test_timeout_out_of_range(self):
        """timeout 超出范围应拒绝"""
        with pytest.raises(ValueError):
            SearchRequest(query="test", timeout=10)

    def test_default_values(self):
        """默认值应正确设置"""
        req = SearchRequest(query="test")
        assert req.intent == QueryIntent.DEEP
        assert req.language == QueryLanguage.AUTO
        assert req.max_results == 100
        assert req.engine_group == "all"
        assert req.timeout == 600


class TestSearchHit:
    """SearchHit 契约测试"""

    def test_valid_hit(self):
        hit = SearchHit(
            url="https://example.com/article",
            title="测试文章",
            source_engine="baidu",
            rank=1,
        )
        assert hit.url == "https://example.com/article"
        assert hit.rank == 1

    def test_frozen(self):
        """SearchHit 应该是不可变的"""
        hit = SearchHit(
            url="https://example.com",
            title="Test",
            source_engine="google",
            rank=1,
        )
        with pytest.raises(Exception):
            hit.title = "New Title"


class TestSearchOutput:
    """SearchOutput 契约测试"""

    def test_valid_output(self):
        hit = SearchHit(
            url="https://example.com",
            title="Test",
            source_engine="baidu",
            rank=1,
        )
        output = SearchOutput(
            request_id="test-001",
            query="AI",
            deduplicated_results=[hit],
            total_raw=10,
            total_deduped=5,
            total_engines=16,
            status="complete",
        )
        assert output.total_deduped <= output.total_raw

    def test_deduped_exceeds_raw(self):
        """去重结果数不能超过原始结果数"""
        with pytest.raises(ValueError):
            SearchOutput(
                request_id="test",
                query="test",
                total_raw=5,
                total_deduped=10,
                total_engines=1,
            )

    def test_failed_engines_preserved(self):
        output = SearchOutput(
            request_id="test",
            query="test",
            total_raw=0,
            total_deduped=0,
            total_engines=3,
            failed_engines=["engine1", "engine2"],
            status="partial",
        )
        assert len(output.failed_engines) == 2
        assert output.status == "partial"
