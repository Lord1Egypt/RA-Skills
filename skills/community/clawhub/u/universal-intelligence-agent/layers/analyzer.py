"""
分析引擎 — Facade 编排器
─────────────────────────
职责：
  - 编排 NLP / 可信度 / LLM 三个子引擎
  - 决策框架匹配
  - 构建统一输出
  - 输出强制通过 contracts/analysis_schema.py 的 AnalysisOutput Schema

严禁：
  - 持有业务逻辑（已拆分到 nlp_engine / credibility_engine / llm_hub）
  - 直接调用搜索引擎
  - 跨阶段通信（输入通过ACL校验）
"""
from __future__ import annotations

import logging
from typing import Any, Optional

from middlewares.circuit_breaker import TieredCircuitBreaker
from contracts.analysis_schema import (
    AnalysisOutput,
    NLPResults,
    CredibilityResults,
    LLMAnalysis,
    SentimentResult,
    SourceEntry,
)
from layers.nlp_engine import NLPEngine
from layers.credibility_engine import CredibilityEngine
from layers.llm_hub import LLMHub

logger = logging.getLogger(__name__)


class Analyzer:
    """
    分析引擎 Facade — 纯编排器

    将 NLP、可信度、LLM 三个子引擎的产出组装成统一输出。

    用法:
        analyzer = Analyzer(circuit_breaker=tcb)
        result = analyzer.analyze(
            query="AI趋势",
            crawl_data={"pages": [...]},
            intent="deep",
        )
    """

    # 决策框架映射
    _FRAMEWORK_MAP = {
        "deep": "第一性原理 + 系统思维",
        "quick": "奥卡姆剃刀",
        "compare": "系统思维 + 二阶思维",
        "verify": "反证法 + 贝叶斯更新",
        "monitor": "二阶思维",
        "trend": "系统思维 + 贝叶斯更新",
    }

    def __init__(self, circuit_breaker: Optional[TieredCircuitBreaker] = None):
        self._circuit_breaker = circuit_breaker or TieredCircuitBreaker()
        self._nlp = NLPEngine()
        self._credibility = CredibilityEngine()
        self._llm = LLMHub()

    def analyze(
        self,
        query: str,
        crawl_data: dict,
        intent: str = "deep",
        session_id: str = "",
    ) -> AnalysisOutput:
        """
        执行全维度分析

        Args:
            query: 原始查询
            crawl_data: 爬取阶段数据（dict 格式，兼容 Scraper 输出）
                Phase 5.1: 保留 dict 参数以兼容 PipelineCoordinator 传入的 ACL 校验后的 dict。
                内部通过 .get("pages", []) 提取页面列表。
            intent: 用户意图
            session_id: 会话ID

        Returns:
            AnalysisOutput: 通过 Pydantic Schema 校验的分析输出对象
        """
        pages = crawl_data.get("pages", [])
        errors: list[str] = []
        warnings: list[str] = []

        if not pages:
            return AnalysisOutput(
                query=query,
                status="failed",
                errors=["No pages to analyze"],
            )

        all_text = " ".join([p.get("content_md", "") for p in pages])

        # 1. NLP 分析
        nlp_results = NLPResults()
        try:
            nlp_results = self._nlp.analyze(text=all_text, query=query)
        except Exception as e:
            logger.error(f"NLP analysis failed: {e}")
            errors.append(f"NLP: {e}")

        # 2. 可信度评分
        credibility = CredibilityResults()
        try:
            credibility = self._credibility.score(pages)
        except Exception as e:
            logger.error(f"Credibility scoring failed: {e}")
            errors.append(f"Credibility: {e}")

        # 3. LLM 分析
        llm_analysis = LLMAnalysis()
        try:
            llm_analysis = self._llm.analyze(query=query, pages=pages, intent=intent)
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            errors.append(f"LLM: {e}")

        # 4. 决策框架匹配
        decision_framework = self._FRAMEWORK_MAP.get(intent, "系统思维")

        # 5. 构建来源列表
        sources = self._build_source_entries(pages, credibility)

        # 确定状态
        if not llm_analysis.key_findings and errors:
            status = "failed"
        elif errors:
            status = "partial"
        else:
            status = "complete"

        # ── 通过 Pydantic Schema 构造输出 ──
        # Phase 4.1: 返回强类型 AnalysisOutput 对象，不再 model_dump()
        try:
            return AnalysisOutput(
                query=query,
                nlp_results=nlp_results,
                credibility_scores=credibility,
                llm_analysis=llm_analysis,
                decision_framework=decision_framework,
                key_findings=llm_analysis.key_findings,
                entities=nlp_results.entities,
                sentiment=llm_analysis.sentiment,
                cross_validation=llm_analysis.cross_validation,
                conclusions=llm_analysis.conclusions,
                sources=sources,
                status=status,
                errors=errors,
                warnings=warnings,
            )
        except Exception as e:
            logger.error(f"[Analyzer:{session_id}] Schema validation failed: {e}")
            return AnalysisOutput(
                query=query,
                status="failed",
                errors=errors + [f"Schema validation failed: {e}"],
            )

    def _build_source_entries(
        self, pages: list[dict], credibility: CredibilityResults
    ) -> list[SourceEntry]:
        """构建带可信度的来源列表"""
        score_map = {s.url: s for s in credibility.scores}

        sources = []
        for page in pages:
            url = page.get("url", "")
            score_info = score_map.get(url)
            sources.append(SourceEntry(
                source=page.get("source_engine", "未知"),
                title=page.get("title", "无标题"),
                url=url,
                trust_level=float(score_info.total_score) if score_info else 2.0,
                date="N/A",
            ))

        return sources
