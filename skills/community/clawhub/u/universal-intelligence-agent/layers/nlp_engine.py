"""
NLP 引擎 — 分词、实体识别、摘要生成
────────────────────────────────────
从 Analyzer 拆分出的独立模块。
专注纯 NLP 处理，不关心搜索/爬取/报告。
"""
from __future__ import annotations

import logging
import re
from collections import Counter

from contracts.nlp_schema import NLPAnalysisOutput, EntityList
from contracts.analysis_schema import NLPResults

logger = logging.getLogger(__name__)


class NLPEngine:
    """
    NLP 引擎 — 文本分析核心

    用法:
        engine = NLPEngine()
        results = engine.analyze(
            text="全文内容...",
            query="原始查询",
            language="zh",
        )
    """

    def analyze(
        self,
        text: str,
        query: str = "",
        language: str = "zh",
        max_keywords: int = 20,
        max_summary_length: int = 500,
    ) -> NLPResults:
        """
        执行 NLP 分析

        Returns:
            NLPResults: 符合 AnalysisOutput Schema 的 NLP 结果
        """
        if not text or not text.strip():
            return NLPResults()

        # 关键词提取
        keywords = self._extract_keywords(text, top_n=max_keywords)

        # 实体识别
        entities = self._extract_entities(text)

        # 摘要生成
        summary = self._generate_summary(text, max_length=max_summary_length)

        return NLPResults(
            keywords=keywords,
            entities={
                "人物": entities.persons,
                "地点": entities.locations,
                "机构": entities.organizations,
                "时间": entities.dates,
            },
            summary=summary,
            text_length=len(text),
        )

    def _extract_keywords(self, text: str, top_n: int = 20) -> list[str]:
        """提取关键词 — 简化版 TF-IDF"""
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text.lower())

        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "in", "on", "at",
            "to", "for", "of", "and", "or", "but", "with", "by", "from",
            "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都",
            "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你",
            "会", "着", "没有", "看", "好", "自己", "这", "他", "她", "它",
        }

        filtered = [w for w in words if w not in stopwords and len(w) > 1]
        counter = Counter(filtered)
        return [word for word, _ in counter.most_common(top_n)]

    def _extract_entities(self, text: str) -> EntityList:
        """实体识别 — 简化版"""
        entities = EntityList()

        # 中文人名（2-4字常见姓+名）
        person_pattern = re.findall(
            r'(?:[李王张刘陈杨赵黄周吴徐孙马胡朱郭何罗高林郑梁谢唐许冯宋韩]'
            r'[\u4e00-\u9fff]{1,2})',
            text,
        )
        entities.persons = list(set(person_pattern))[:10]

        # 时间表达式
        time_pattern = re.findall(
            r'\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{2}-\d{2}|\d{4}年',
            text,
        )
        entities.dates = list(set(time_pattern))[:10]

        # 机构（常见后缀）
        org_pattern = re.findall(
            r'[\u4e00-\u9fff]{2,10}(?:公司|集团|大学|研究院|学院|政府|部|委员会|局|中心)',
            text,
        )
        entities.organizations = list(set(org_pattern))[:10]

        return entities

    def _generate_summary(self, text: str, max_length: int = 500) -> str:
        """生成文本摘要 — 提取前N个句子"""
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

        summary_sentences = sentences[:5]
        summary = "。".join(summary_sentences)

        if len(summary) > max_length:
            summary = summary[:max_length] + "..."

        return summary
