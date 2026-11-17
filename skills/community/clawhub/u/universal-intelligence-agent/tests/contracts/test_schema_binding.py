"""
Schema-运行时绑定测试 — Phase 3 核心测试
────────────────────────────────────────
验证每个阶段容器返回的数据能通过对应 Pydantic Schema 校验。

这是"契约锁死"的证明：如果这些测试失败，说明阶段容器返回了
不符合契约的数据。
"""
from __future__ import annotations

import pytest

from contracts.search_schema import SearchHit, SearchOutput
from contracts.crawl_schema import CrawledPage, CrawlOutput
from contracts.analysis_schema import (
    AnalysisOutput,
    NLPResults,
    CredibilityResults,
    CredibilityScore,
    LLMAnalysis,
    SentimentResult,
    CrossValidationResult,
    SourceEntry,
)


class TestSearchOutputSchema:
    """搜索阶段输出 Schema 校验"""

    def test_valid_search_output(self):
        """合法搜索输出应通过 Schema 校验"""
        hit = SearchHit(
            url="https://example.com/article",
            title="测试文章",
            snippet="这是摘要",
            source_engine="baidu",
            source_region="cn",
            rank=1,
        )
        output = SearchOutput(
            request_id="test_001",
            query="测试查询",
            deduplicated_results=[hit],
            total_raw=1,
            total_deduped=1,
            total_engines=1,
        )
        assert output.status == "complete"
        assert output.total_deduped == 1

    def test_invalid_url_rejected(self):
        """非法 URL 应被拒绝"""
        with pytest.raises(Exception):
            SearchHit(
                url="not-a-valid-url",
                title="测试",
                source_engine="google",
                rank=1,
            )

    def test_empty_url_rejected(self):
        """空 URL 应被拒绝"""
        with pytest.raises(Exception):
            SearchHit(
                url="",
                title="测试",
                source_engine="google",
                rank=1,
            )

    def test_non_http_scheme_rejected(self):
        """非 http/https scheme 应被拒绝"""
        with pytest.raises(Exception):
            SearchHit(
                url="ftp://example.com/file",
                title="测试",
                source_engine="google",
                rank=1,
            )

    def test_deduped_not_exceed_raw(self):
        """deduped 不应超过 raw"""
        with pytest.raises(Exception):
            SearchOutput(
                request_id="test",
                query="test",
                total_raw=5,
                total_deduped=10,
                total_engines=1,
            )

    def test_failed_status_accepted(self):
        """搜索全部失败时 status=failed 应合法"""
        output = SearchOutput(
            request_id="test_002",
            query="测试",
            total_raw=0,
            total_deduped=0,
            total_engines=5,
            failed_engines=["baidu", "google"],
            status="failed",
        )
        assert output.status == "failed"


class TestCrawlOutputSchema:
    """爬取阶段输出 Schema 校验"""

    def test_valid_crawl_output(self):
        """合法爬取输出应通过 Schema 校验"""
        page = CrawledPage(
            url="https://example.com/page",
            title="测试页面",
            content_md="# Hello\n\nWorld",
            content_length=0,
            status_code=200,
        )
        output = CrawlOutput(
            pages=[page],
            total_pages=1,
            successful_pages=1,
        )
        assert output.status == "complete"

    def test_invalid_url_in_page_rejected(self):
        """页面 URL 无效应被拒绝"""
        with pytest.raises(Exception):
            CrawledPage(
                url="bad-url",
                title="测试",
            )

    def test_content_length_mismatch_rejected(self):
        """content_length 与 content_md 长度不一致应被拒绝"""
        with pytest.raises(Exception):
            CrawledPage(
                url="https://example.com",
                content_md="Hello World",
                content_length=999,  # 不匹配
            )

    def test_empty_pages_ok(self):
        """空 pages 列表在 status=failed 时合法"""
        output = CrawlOutput(
            pages=[],
            total_pages=0,
            successful_pages=0,
            status="failed",
            errors=["No results"],
        )
        assert output.status == "failed"


class TestAnalysisOutputSchema:
    """分析阶段输出 Schema 校验"""

    def test_valid_analysis_output(self):
        """合法分析输出应通过 Schema 校验"""
        nlp = NLPResults(
            keywords=["AI", "趋势"],
            entities={"人物": [], "地点": [], "机构": ["OpenAI"], "时间": []},
            summary="这是摘要",
            text_length=100,
        )
        cred = CredibilityResults(
            scores=[
                CredibilityScore(
                    url="https://example.com",
                    domain_score=4,
                    content_score=4,
                    total_score=3.25,
                    level="中等可信",
                )
            ],
            high=0,
            medium=1,
            low=0,
            dubious=0,
            average_score=3.25,
        )
        llm = LLMAnalysis(
            key_findings=["发现1"],
            sentiment=SentimentResult(overall="中性"),
            cross_validation=CrossValidationResult(total_sources=1),
            conclusions=["结论1"],
        )
        output = AnalysisOutput(
            query="测试",
            nlp_results=nlp,
            credibility_scores=cred,
            llm_analysis=llm,
            key_findings=["发现1"],
            conclusions=["结论1"],
            sources=[SourceEntry(url="https://example.com", trust_level=3.0)],
        )
        assert output.status == "complete"

    def test_complete_status_requires_findings(self):
        """status=complete 但 key_findings 为空应被拒绝"""
        with pytest.raises(Exception):
            AnalysisOutput(
                query="测试",
                status="complete",
                key_findings=[],
                conclusions=["结论"],
            )

    def test_complete_status_requires_conclusions(self):
        """status=complete 但 conclusions 为空应被拒绝"""
        with pytest.raises(Exception):
            AnalysisOutput(
                query="测试",
                status="complete",
                key_findings=["发现"],
                conclusions=[],
            )

    def test_failed_status_accepts_empty(self):
        """status=failed 时允许空 key_findings 和 conclusions"""
        output = AnalysisOutput(
            query="测试",
            status="failed",
            errors=["No data"],
        )
        assert output.status == "failed"

    def test_invalid_url_in_sources_rejected(self):
        """sources 中有无效 URL 应被拒绝"""
        with pytest.raises(Exception):
            AnalysisOutput(
                query="测试",
                key_findings=["发现"],
                conclusions=["结论"],
                sources=[SourceEntry(url="bad-url", trust_level=2.0)],
            )

    def test_credibility_range_validated(self):
        """可信度 average_score 超出范围应被拒绝"""
        with pytest.raises(Exception):
            CredibilityResults(
                average_score=99.0,
            )


class TestModelDump:
    """验证 model_dump() 可被下游直接使用"""

    def test_search_output_model_dump_is_dict(self):
        hit = SearchHit(
            url="https://example.com",
            title="Test",
            source_engine="google",
            rank=1,
        )
        output = SearchOutput(
            request_id="test",
            query="test",
            deduplicated_results=[hit],
            total_raw=1,
            total_deduped=1,
            total_engines=1,
        )
        result = output.model_dump()
        assert isinstance(result, dict)
        assert result["status"] == "complete"
        assert len(result["deduplicated_results"]) == 1

    def test_analysis_output_model_dump_has_all_keys(self):
        output = AnalysisOutput(
            query="test",
            key_findings=["发现1"],
            conclusions=["结论1"],
        )
        result = output.model_dump()
        assert "nlp_results" in result
        assert "credibility_scores" in result
        assert "llm_analysis" in result
        assert "sources" in result
