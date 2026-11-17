"""
可信度引擎 — 5维度评分
────────────────────────
从 Analyzer 拆分出的独立模块。
专注来源可信度评估，不关心 NLP/LLM/报告。
"""
from __future__ import annotations

import logging
import re
from urllib.parse import urlparse

from contracts.analysis_schema import CredibilityResults, CredibilityScore

logger = logging.getLogger(__name__)


class CredibilityEngine:
    """
    可信度引擎 — 5维度来源评分

    维度:
    - 域名权威性 (25%): .gov/.edu=5, 正规新闻=4, 行业站=3, 博客=2, 论坛=1
    - 内容质量 (20%): 完整度+字数+引用
    - 时效性 (15%): 越新越高
    - 跨源一致性 (25%): 多独立源报道一致=高分
    - 引用来源 (15%): 有引用=高分

    用法:
        engine = CredibilityEngine()
        results = engine.score(pages=[...])
    """

    def score(self, pages: list[dict]) -> CredibilityResults:
        """对页面列表进行可信度评分"""
        scores: list[CredibilityScore] = []
        high = medium = low = dubious = 0

        for page in pages:
            url = page.get("url", "")
            content = page.get("content_md", "")

            domain_score = self._domain_authority(url)
            content_score = self._content_quality(content)
            freshness_score = 3  # 默认中等

            total = (
                domain_score * 0.25 +
                content_score * 0.20 +
                freshness_score * 0.15 +
                3 * 0.25 +  # 跨源一致性（简化：假设中等）
                3 * 0.15    # 引用来源（简化：假设中等）
            )

            if total >= 4.0:
                level = "高可信"
                high += 1
            elif total >= 3.0:
                level = "中等可信"
                medium += 1
            elif total >= 2.0:
                level = "低可信"
                low += 1
            else:
                level = "存疑"
                dubious += 1

            scores.append(CredibilityScore(
                url=url,
                title=page.get("title", ""),
                domain_score=domain_score,
                content_score=content_score,
                total_score=round(total, 2),
                level=level,
            ))

        avg = round(
            sum(s.total_score for s in scores) / max(len(scores), 1), 2
        )

        return CredibilityResults(
            scores=scores,
            high=high,
            medium=medium,
            low=low,
            dubious=dubious,
            average_score=avg,
        )

    def _domain_authority(self, url: str) -> int:
        """评估域名权威性 (1-5)"""
        try:
            domain = urlparse(url).netloc.lower()
        except Exception:
            return 1

        if any(tld in domain for tld in [".gov", ".edu", ".ac."]):
            return 5

        news_domains = [
            "reuters.com", "ap.org", "bbc.com", "bbc.co.uk", "nytimes.com",
            "wsj.com", "economist.com", "nature.com", "science.org",
            "xinhuanet.com", "people.com.cn", "cctv.com", "chinadaily.com.cn",
            "thepaper.cn", "caixin.com", "36kr.com", "jiemian.com",
        ]
        if any(nd in domain for nd in news_domains):
            return 4

        tech_domains = [
            "github.com", "stackoverflow.com", "wikipedia.org",
            "arxiv.org", "ieee.org", "acm.org", "mit.edu", "stanford.edu",
        ]
        if any(td in domain for td in tech_domains):
            return 4

        tech_media = [
            "techcrunch.com", "theverge.com", "wired.com", "arstechnica.com",
            "hackernoon.com", "dev.to", "medium.com",
        ]
        if any(tm in domain for tm in tech_media):
            return 3

        blog_indicators = ["blog", "wordpress", "medium.com/", "substack.com"]
        if any(bi in domain for bi in blog_indicators):
            return 2

        forum_indicators = ["reddit.com", "zhihu.com", "tieba.baidu.com", "forum"]
        if any(fi in domain for fi in forum_indicators):
            return 1

        return 3

    def _content_quality(self, content: str) -> int:
        """评估内容质量 (1-5)"""
        if not content:
            return 1

        length = len(content)

        if length > 5000:
            length_score = 5
        elif length > 2000:
            length_score = 4
        elif length > 500:
            length_score = 3
        elif length > 100:
            length_score = 2
        else:
            length_score = 1

        has_citations = bool(re.search(r'\[\d+\]|参考文献|引用|来源', content))
        citation_bonus = 1 if has_citations else 0

        return min(5, length_score + citation_bonus)
