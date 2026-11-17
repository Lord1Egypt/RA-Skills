"""
集成测试 — 完整管道
────────────────────
验证 PipelineCoordinator 从输入到输出的完整流程。
"""
import pytest
from layers.input_adapter import InputAdapter, NormalizedRequest, QueryIntent, QueryLanguage
from layers.pipeline_coordinator import PipelineCoordinator, PipelinePhase
from layers.acl import search_to_crawl_validator, ACLViolationError


class TestInputAdapter:
    """Input Adapter 集成测试"""

    def test_string_input(self):
        adapter = InputAdapter()
        request = adapter.adapt("帮我查一下AI趋势")
        assert isinstance(request, NormalizedRequest)
        assert "AI" in request.query
        assert request.intent in (QueryIntent.DEEP, QueryIntent.TREND)

    def test_dict_input(self):
        adapter = InputAdapter()
        request = adapter.adapt({"query": "快速了解比特币", "max_results": 50})
        assert request.query == "快速了解比特币"
        assert request.max_results == 50

    def test_intent_detection_quick(self):
        adapter = InputAdapter()
        request = adapter.adapt("快速简报：最新科技新闻")
        assert request.intent == QueryIntent.QUICK

    def test_intent_detection_compare(self):
        adapter = InputAdapter()
        request = adapter.adapt("对比iPhone和Android的区别")
        assert request.intent == QueryIntent.COMPARE

    def test_intent_detection_verify(self):
        adapter = InputAdapter()
        request = adapter.adapt("这个新闻可信吗？验证一下")
        assert request.intent == QueryIntent.VERIFY

    def test_language_detection_zh(self):
        adapter = InputAdapter()
        request = adapter.adapt("中国经济发展趋势分析")
        assert request.language == QueryLanguage.ZH

    def test_language_detection_en(self):
        adapter = InputAdapter()
        request = adapter.adapt("What is the latest trend in AI?")
        assert request.language == QueryLanguage.EN

    def test_empty_query_rejected(self):
        adapter = InputAdapter()
        with pytest.raises(ValueError):
            adapter.adapt("")

    def test_short_query_rejected(self):
        adapter = InputAdapter()
        with pytest.raises(ValueError):
            adapter.adapt("A")

    def test_engine_selection_zh(self):
        adapter = InputAdapter()
        engines = adapter.get_engine_list(QueryLanguage.ZH, "all")
        assert len(engines) >= 11  # 7 CN + 4 global
        assert "baidu" in engines
        assert "google" in engines

    def test_engine_selection_en(self):
        adapter = InputAdapter()
        engines = adapter.get_engine_list(QueryLanguage.EN, "all")
        assert len(engines) == 9  # 9 global only


class TestPipelineCoordinator:
    """Pipeline Coordinator 集成测试"""

    def test_coordinator_creation(self):
        coordinator = PipelineCoordinator()
        assert coordinator is not None

    def test_phase_order(self):
        coordinator = PipelineCoordinator()
        assert PipelinePhase.SEARCHING in coordinator._PHASE_ORDER
        assert PipelinePhase.CRAWLING in coordinator._PHASE_ORDER
        assert PipelinePhase.ANALYZING in coordinator._PHASE_ORDER
        assert len(coordinator._PHASE_ORDER) == 5


class TestACLIntegration:
    """ACL 层与 Pipeline 集成测试"""

    def test_valid_search_output_passes_acl(self):
        valid_data = {
            "deduplicated_results": [
                {"url": "https://example.com", "title": "Test", "rank": 1}
            ],
            "total_deduped": 1,
            "status": "complete",
        }
        result = search_to_crawl_validator.validate(valid_data)
        assert result is not None

    def test_none_output_rejected_by_acl(self):
        with pytest.raises(ACLViolationError):
            search_to_crawl_validator.validate(None)

    def test_empty_results_rejected_by_acl(self):
        invalid_data = {
            "deduplicated_results": [],
            "total_deduped": 0,
            "status": "failed",
        }
        with pytest.raises(ACLViolationError):
            search_to_crawl_validator.validate(invalid_data)
