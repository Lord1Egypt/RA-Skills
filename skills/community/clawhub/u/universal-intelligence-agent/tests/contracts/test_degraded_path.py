"""
降级路径契约测试 — Phase 8 核心测试
────────────────────────────────────
验证降级输出也走 Schema 校验，不再手工拼裸 dict。
这是"降级路径契约化"的证明。
"""
from __future__ import annotations

import pytest

from contracts.analysis_schema import (
    AnalysisOutput,
    NLPResults,
    CredibilityResults,
    LLMAnalysis,
    SentimentResult,
    CrossValidationResult,
    SourceEntry,
)
from contracts.search_schema import SearchHit, SearchOutput


class TestDegradedAnalysisOutput:
    """降级模式下 AnalysisOutput 仍应通过 Schema 校验"""

    def test_degraded_partial_status_valid(self):
        """status=partial + key_findings + 空 conclusions 应合法"""
        output = AnalysisOutput(
            query="测试查询",
            status="partial",
            nlp_results=NLPResults(
                summary="[降级] 分析阶段未完成",
                text_length=0,
            ),
            credibility_scores=CredibilityResults(average_score=0.0),
            llm_analysis=LLMAnalysis(
                key_findings=["[降级] 分析阶段未完成"],
                sentiment=SentimentResult(overall="中性"),
                cross_validation=CrossValidationResult(total_sources=0),
                conclusions=[],
                provider="degraded",
            ),
            key_findings=["[降级] 分析阶段未完成"],
            conclusions=[],
            errors=["Search phase failed"],
            warnings=["Pipeline degraded"],
        )
        assert output.status == "partial"
        assert output.key_findings == ["[降级] 分析阶段未完成"]

    def test_degraded_sources_accept_empty_url(self):
        """降级来源的 URL 可以为空字符串（Pydantic SourceEntry 默认值）"""
        entry = SourceEntry(
            source="未知",
            title="无标题",
            url="",  # 空 URL 是合法的（默认值）
            trust_level=2.0,
            date="N/A",
        )
        assert entry.url == ""

    def test_degraded_sources_with_valid_url(self):
        """降级来源带合法 URL 应通过校验"""
        entry = SourceEntry(
            source="baidu",
            title="测试结果",
            url="https://example.com/article",
            trust_level=2.0,
            date="N/A",
        )
        assert entry.url == "https://example.com/article"

    def test_degraded_sources_invalid_url_rejected(self):
        """
        降级来源带非法 URL 应被拒绝。
        注意：SourceEntry 自身的 url 字段没有 validator，
        但 AnalysisOutput.sources_have_valid_urls 会拦截。
        所以必须把 SourceEntry 放入 AnalysisOutput.sources 中测试。
        """
        with pytest.raises(Exception):
            AnalysisOutput(
                query="测试",
                status="partial",
                key_findings=["发现"],
                conclusions=[],
                sources=[SourceEntry(
                    source="baidu",
                    title="测试",
                    url="not-a-url",  # 非法 URL
                    trust_level=2.0,
                )],
            )

    def test_degraded_model_dump_contains_all_keys(self):
        """降级 AnalysisOutput model_dump() 应包含所有必需 key"""
        output = AnalysisOutput(
            query="完整测试",
            status="partial",
            key_findings=["发现A"],
            conclusions=[],
        )
        dump = output.model_dump()

        expected_keys = [
            "query", "status", "key_findings", "conclusions",
            "nlp_results", "credibility_scores", "llm_analysis",
            "sources", "errors", "warnings", "decision_framework",
            "entities", "sentiment", "cross_validation",
        ]
        for key in expected_keys:
            assert key in dump, f"Missing key: {key}"
        assert dump["status"] == "partial"

    def test_degraded_credibility_zero_is_valid(self):
        """降级模式 average_score=0 是合法的"""
        cred = CredibilityResults(average_score=0.0)
        assert cred.average_score == 0.0

    def test_degraded_no_scores_average_is_zero(self):
        """无 scores 时 average_score=0 合法"""
        cred = CredibilityResults(scores=[], average_score=0.0)
        assert cred.average_score == 0.0
        assert cred.high == 0
        assert cred.medium == 0
        assert cred.low == 0
        assert cred.dubious == 0

    def test_degraded_key_findings_with_special_chars(self):
        """降级 key_findings 包含特殊字符应合法"""
        output = AnalysisOutput(
            query="test",
            status="partial",
            key_findings=["[降级] 分析失败: NetworkError(timeout=30s)"],
            conclusions=[],
        )
        assert output.status == "partial"
        assert "timeout" in output.key_findings[0]

    def test_degraded_empty_sources_valid(self):
        """降级模式下空 sources 列表合法"""
        output = AnalysisOutput(
            query="test",
            status="partial",
            key_findings=["降级"],
            conclusions=[],
            sources=[],
        )
        assert output.sources == []


class TestDegradedOutputConsumedByAdapter:
    """降级 AnalysisOutput.model_dump() 能被 OutputAdapter 正确消费"""

    def test_resolve_analysis_fields_from_degraded_output(self):
        """OutputAdapter._resolve_analysis_fields 正确处理降级数据"""
        from layers.output_adapter import OutputAdapter

        adapter = OutputAdapter()
        degraded_data = AnalysisOutput(
            query="降级测试",
            status="partial",
            nlp_results=NLPResults(
                keywords=[],
                entities={"人物": [], "地点": [], "机构": [], "时间": []},
                summary="降级摘要",
                text_length=0,
            ),
            credibility_scores=CredibilityResults(average_score=0.0),
            llm_analysis=LLMAnalysis(
                key_findings=["降级发现"],
                sentiment=SentimentResult(overall="中性"),
                cross_validation=CrossValidationResult(total_sources=0),
                conclusions=[],
                provider="degraded",
            ),
            key_findings=["降级发现"],
            conclusions=[],
            sources=[
                SourceEntry(
                    source="baidu",
                    title="结果1",
                    url="https://example.com/1",
                    trust_level=2.0,
                    date="N/A",
                )
            ],
        ).model_dump()

        resolved = adapter._resolve_analysis_fields(degraded_data)
        assert resolved["query"] == "降级测试"
        assert resolved["conclusions"] == []
        # sources 被正确映射
        assert len(resolved["sources"]) == 1
        # credibility 被正确提取
        assert resolved["credibility"]["high"] == 0

    def test_resolve_with_schema_objects_inline(self):
        """
        _resolve_analysis_fields 处理内嵌 Pydantic 对象（非 dict）。
        Phase 8: sources 中可能包含 SourceEntry 对象而非 dict。
        """
        from layers.output_adapter import OutputAdapter
        from contracts.analysis_schema import CredibilityResults as CR

        adapter = OutputAdapter()
        # 模拟 pipeline_coordinator 传入的 Schema 对象（尚未 model_dump）
        data = {
            "query": "test",
            "nlp_results": NLPResults(summary="test", text_length=10),
            "credibility_scores": CR(average_score=3.5, high=2, medium=1, low=0, dubious=0),
            "llm_analysis": LLMAnalysis(
                key_findings=["发现"],
                sentiment=SentimentResult(overall="正面"),
                cross_validation=CrossValidationResult(total_sources=1),
                conclusions=["结论"],
            ),
            "key_findings": ["发现"],
            "conclusions": ["结论"],
            # sources 是 Pydantic SourceEntry 对象，不是 dict
            "sources": [SourceEntry(url="https://example.com", trust_level=3.0)],
        }

        resolved = adapter._resolve_analysis_fields(data)
        assert resolved["query"] == "test"
        assert resolved["credibility"]["high"] == 2
        assert resolved["sentiment"]["overall"] == "正面"
        # sources 应被正确转换为 dict
        assert len(resolved["sources"]) == 1
        assert isinstance(resolved["sources"][0], dict)
        assert resolved["sources"][0]["url"] == "https://example.com"

    def test_resolve_old_dict_format_backward_compat(self):
        """_resolve_analysis_fields 兼容旧版裸 dict 格式"""
        from layers.output_adapter import OutputAdapter

        adapter = OutputAdapter()
        # 旧版 dict 格式（Phase 4 之前的数据）
        old_format = {
            "query": "old test",
            "total_engines": 3,
            "total_results": 10,
            "deduplicated": 7,
            "credibility_score": 3.5,
            "key_findings": ["old finding"],
            "sources": [{"source": "google", "title": "Old", "url": "https://old.com", "trust_level": 3}],
        }

        resolved = adapter._resolve_analysis_fields(old_format)
        # 旧版字段应被保留
        assert resolved["query"] == "old test"
        assert resolved["total_engines"] == 3  # 旧版显式传入的应保留
        assert len(resolved["sources"]) == 1


class TestDegradedPathEndToEnd:
    """降级路径端到端：模拟 pipeline 降级流程"""

    def test_degraded_analysis_to_brief(self):
        """降级 AnalysisOutput 能生成简报不崩溃"""
        from layers.output_adapter import OutputAdapter, DeliveryStatus

        adapter = OutputAdapter()
        degraded_data = AnalysisOutput(
            query="降级端到端测试",
            status="partial",
            key_findings=["[降级] 分析未完成"],
            conclusions=[],
            sources=[
                SourceEntry(
                    source="baidu",
                    title="结果",
                    url="https://example.com",
                    trust_level=2.0,
                    date="N/A",
                )
            ],
        ).model_dump()

        result = adapter.generate_brief(degraded_data, "test_session")
        assert result.status in (DeliveryStatus.SUCCESS, DeliveryStatus.PARTIAL)
        assert result.is_success
        assert "降级端到端测试" in result.data.get("content_preview", "")


class TestDegradedOutputFieldMapping:
    """降级 AnalysisOutput 各字段到 OutputAdapter 的完整映射"""

    def test_all_degraded_fields_mapped(self):
        """验证 AnalysisOutput.model_dump() 的所有关键 key 都存在"""
        output = AnalysisOutput(
            query="完整测试",
            status="partial",
            key_findings=["发现A", "发现B"],
            conclusions=["结论1"],
            sources=[
                SourceEntry(
                    source="google",
                    title="Page",
                    url="https://example.com",
                    trust_level=3.5,
                    date="2024-01-01",
                )
            ],
        )
        dump = output.model_dump()

        # 所有期望的 key 都应存在
        expected_keys = [
            "query", "status", "key_findings", "conclusions",
            "nlp_results", "credibility_scores", "llm_analysis",
            "sources", "errors", "warnings", "decision_framework",
            "entities", "sentiment", "cross_validation",
        ]
        for key in expected_keys:
            assert key in dump, f"Missing key: {key}"
