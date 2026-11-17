"""
降级路径处理器 — 统一降级输出构造
────────────────────────────────
从 PipelineCoordinator 拆分出的独立模块。
与正常路径共用相同的 Schema 构造逻辑，确保降级输出与正常输出格式一致。
"""
from __future__ import annotations

import logging
from typing import Optional

from contracts.analysis_schema import (
    AnalysisOutput,
    SourceEntry,
    NLPResults,
    CredibilityResults,
    LLMAnalysis,
    SentimentResult,
    CrossValidationResult,
)
from contracts.context_schema import PipelineBus, StageContext

logger = logging.getLogger(__name__)


class DegradedHandler:
    """降级路径统一处理器

    用法:
        handler = DegradedHandler()
        degraded_output = handler.build_degraded_analysis(
            bus=ctx.bus,
            query="测试查询",
            reason="Search phase failed",
        )
    """

    def build_degraded_analysis(
        self,
        bus: PipelineBus,
        query: str,
        reason: str,
    ) -> AnalysisOutput:
        """从 PipelineBus 构建降级的 AnalysisOutput

        优先使用搜索阶段的已有数据构造来源列表。
        所有字段都通过 Pydantic Schema 校验。
        """
        # 从搜索结果构建来源列表（最多 5 个）
        sources: list[SourceEntry] = []
        try:
            if bus.has_search_succeeded():
                search_output = bus.get_search_output()
                raw_hits = search_output.deduplicated_results[:5]
                for hit in raw_hits:
                    try:
                        sources.append(SourceEntry(
                            source=hit.source_engine,
                            title=hit.title,
                            url=hit.url,
                            trust_level=2.0,
                            date="N/A",
                        ))
                    except Exception:
                        pass
        except Exception:
            pass

        return AnalysisOutput(
            query=query,
            status="partial",
            nlp_results=NLPResults(
                keywords=[],
                entities={"人物": [], "地点": [], "机构": [], "时间": []},
                summary=f"[降级] 分析阶段未完成: {reason}",
                text_length=0,
            ),
            credibility_scores=CredibilityResults(average_score=0.0),
            llm_analysis=LLMAnalysis(
                key_findings=[f"[降级] 分析阶段未完成: {reason}"],
                sentiment=SentimentResult(overall="中性"),
                cross_validation=CrossValidationResult(total_sources=len(sources)),
                conclusions=[],
                provider="degraded",
            ),
            key_findings=[f"[降级] 分析阶段未完成: {reason}"],
            conclusions=[],
            sources=sources,
            errors=[reason],
            warnings=[f"Pipeline degraded: {reason}"],
        )
