"""
LLM Hub — Provider 自动发现 + 规则分析降级
─────────────────────────────────────────
从 Analyzer 拆分出的独立模块。
负责 LLM Provider 检测、调用、降级分析和结论生成。
"""
from __future__ import annotations

import logging
import os
import re
import subprocess

from contracts.llm_schema import (
    LLMProvider,
    CrossValidation,
    SentimentAnalysis,
    LLMResponse,
)
from contracts.analysis_schema import (
    LLMAnalysis,
    SentimentResult,
    CrossValidationResult,
)

logger = logging.getLogger(__name__)


class LLMHub:
    """
    LLM Hub — Provider 管理与分析

    自动检测可用 Provider:
    1. ollama (本地)
    2. OpenClaw Gateway
    3. DeepSeek
    4. 通义千问
    5. 降级：规则分析

    用法:
        hub = LLMHub()
        results = hub.analyze(query="AI趋势", pages=[...], intent="deep")
    """

    def analyze(
        self,
        query: str,
        pages: list[dict],
        intent: str = "deep",
    ) -> LLMAnalysis:
        """执行 LLM 分析"""
        provider = self._detect_provider()

        if provider == LLMProvider.NONE:
            logger.warning("No LLM provider available, using rule-based analysis")
            return self._rule_based_analysis(query, pages)

        # 实际 LLM 调用（由 runtime 执行）
        return self._rule_based_analysis(query, pages)

    def _detect_provider(self) -> LLMProvider:
        """检测可用的 LLM Provider"""
        # 检测 ollama
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                logger.info("LLM Provider: ollama (local)")
                return LLMProvider.OLLAMA
        except Exception:
            pass

        # 检测 OpenClaw Gateway
        if os.environ.get("OPENCLAW_GATEWAY_TOKEN"):
            logger.info("LLM Provider: OpenClaw Gateway")
            return LLMProvider.GATEWAY

        # 检测 DeepSeek
        if os.environ.get("DEEPSEEK_API_KEY"):
            logger.info("LLM Provider: DeepSeek")
            return LLMProvider.DEEPSEEK

        # 检测 通义千问
        if os.environ.get("DASHSCOPE_API_KEY"):
            logger.info("LLM Provider: DashScope (通义千问)")
            return LLMProvider.DASHSCOPE

        logger.info("LLM Provider: none (using rule-based fallback)")
        return LLMProvider.NONE

    def _rule_based_analysis(self, query: str, pages: list[dict]) -> LLMAnalysis:
        """基于规则的分析（LLM降级方案）"""
        all_text = " ".join([p.get("content_md", "") for p in pages])

        key_findings = self._extract_key_findings(query, pages)
        cross_validation = self._cross_validate(pages)
        sentiment = self._analyze_sentiment(all_text)
        conclusions = self._generate_conclusions(key_findings, sentiment)

        return LLMAnalysis(
            key_findings=key_findings,
            cross_validation=cross_validation,
            sentiment=sentiment,
            conclusions=conclusions,
            provider="rule_based",
        )

    def _extract_key_findings(self, query: str, pages: list[dict]) -> list[str]:
        """提取关键发现"""
        findings = []
        for page in pages[:10]:
            title = page.get("title", "")
            content = page.get("content_md", "")
            if title and len(title) > 5:
                findings.append(title)
            elif content:
                first_para = (
                    content.split("\n\n")[0] if "\n\n" in content else content[:200]
                )
                if len(first_para) > 10:
                    findings.append(first_para[:200])

        return findings[:5]

    def _cross_validate(self, pages: list[dict]) -> CrossValidationResult:
        """多源交叉验证"""
        titles = [p.get("title", "") for p in pages]
        consistent: list[str] = []
        divergent: list[str] = []

        for i, t1 in enumerate(titles):
            for j, t2 in enumerate(titles):
                if i >= j:
                    continue
                similarity = self._text_similarity(t1, t2)
                if similarity > 0.6:
                    if t1 not in consistent:
                        consistent.append(t1)
                elif similarity < 0.2:
                    if t1 not in divergent:
                        divergent.append(t1)

        return CrossValidationResult(
            consistent=consistent[:5],
            divergent=divergent[:5],
            unverified=[],
            total_sources=len(pages),
        )

    def _text_similarity(self, a: str, b: str) -> float:
        """简单的 Jaccard 相似度"""
        if not a or not b:
            return 0.0
        set_a = set(a)
        set_b = set(b)
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return intersection / union if union > 0 else 0.0

    def _analyze_sentiment(self, text: str) -> SentimentResult:
        """情感分析（简化版关键词匹配）"""
        positive_words = [
            "增长", "突破", "创新", "领先", "优势", "成功", "利好",
            "提升", "改善", "进步", "优秀", "卓越", "积极",
            "growth", "breakthrough", "innovation", "success", "positive",
            "improve", "advance", "leading", "advantage",
        ]
        negative_words = [
            "下降", "风险", "危机", "失败", "亏损", "问题", "挑战",
            "困难", "衰退", "下滑", "恶化", "负面", "消极", "争议",
            "decline", "risk", "crisis", "failure", "loss", "problem",
            "challenge", "negative", "controversy", "dispute",
        ]

        pos_count = sum(1 for w in positive_words if w in text.lower())
        neg_count = sum(1 for w in negative_words if w in text.lower())

        if pos_count > neg_count * 1.5:
            overall = "正面"
        elif neg_count > pos_count * 1.5:
            overall = "负面"
        else:
            overall = "中性"

        return SentimentResult(
            overall=overall,
            positive_count=pos_count,
            negative_count=neg_count,
        )

    def _generate_conclusions(
        self, findings: list[str], sentiment: SentimentResult
    ) -> list[str]:
        """生成结论"""
        if not findings:
            return ["信息不足，无法得出可靠结论。"]

        return [
            f"共收集到 {len(findings)} 条相关信息",
            f"整体情感倾向: {sentiment.overall}",
            "建议进一步核实关键来源的可信度",
        ]
