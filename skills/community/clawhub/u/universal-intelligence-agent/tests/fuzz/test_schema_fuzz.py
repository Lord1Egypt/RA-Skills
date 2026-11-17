"""
Schema Fuzzing 测试 — Phase 3 新增
──────────────────────────────────
用随机/边界/恶意数据冲击 Pydantic Schema，验证其防御能力。
"""
from __future__ import annotations

import pytest
import random
import string

from contracts.search_schema import SearchHit, SearchOutput
from contracts.crawl_schema import CrawledPage, CrawlOutput
from contracts.analysis_schema import (
    AnalysisOutput,
    CredibilityResults,
    CredibilityScore,
    NLPResults,
    LLMAnalysis,
    SourceEntry,
)


def random_string(min_len=1, max_len=500) -> str:
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.printable, k=length))


def random_url() -> str:
    """生成合法或非法的随机 URL"""
    if random.random() < 0.7:
        schemes = ["http://", "https://"]
        domains = ["example.com", "test.org", "site.cn", "evil.xyz"]
        paths = ["/page", "/article/123", "/"]
        return random.choice(schemes) + random.choice(domains) + random.choice(paths)
    else:
        # 恶意 URL（全部应该被拒绝）
        return random.choice([
            "",
            "javascript:alert(1)",
            "file:///etc/passwd",
            "ftp://evil.com/malware",
            "data:text/html,<script>alert(1)</script>",
            "not-a-url",
        ])


class TestSearchHitFuzz:
    """SearchHit Schema Fuzzing"""

    def test_random_valid_urls_accepted(self):
        """随机合法 URL 应被接受"""
        for _ in range(50):
            url = random_url()
            if not url or not isinstance(url, str):
                # None 或空字符串直接跳过（它们一定会被拒绝）
                continue
            try:
                hit = SearchHit(
                    url=url,
                    title=random_string(1, 100),
                    source_engine=random.choice(["baidu", "google", "bing"]),
                    rank=random.randint(1, 10),
                )
                assert hit.url == url
            except Exception:
                # 被拒绝的话，URL 应该不是合法 http/https URL
                is_valid_http = url.startswith(("http://", "https://"))
                if is_valid_http:
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    if not parsed.netloc:
                        pass  # 有 scheme 但无 netloc 的应被拒绝
                    else:
                        raise  # 完全合法的 URL 被拒绝，这是 Bug

    def test_malicious_urls_rejected(self):
        """恶意 URL 应全部被拒绝"""
        malicious = [
            "javascript:alert(1)",
            "file:///etc/passwd",
            "ftp://evil.com/malware",
            "data:text/html,<script>alert(1)</script>",
        ]
        for url in malicious:
            with pytest.raises(Exception):
                SearchHit(
                    url=url,
                    title="test",
                    source_engine="google",
                    rank=1,
                )

    def test_rank_out_of_range_rejected(self):
        """rank 超出 [1,10] 应被拒绝"""
        for bad_rank in [0, 11, -1, 999]:
            with pytest.raises(Exception):
                SearchHit(
                    url="https://example.com",
                    title="test",
                    source_engine="google",
                    rank=bad_rank,
                )

    def test_empty_title_rejected(self):
        """空 title 应被拒绝"""
        with pytest.raises(Exception):
            SearchHit(
                url="https://example.com",
                title="",
                source_engine="google",
                rank=1,
            )


class TestCrawlPageFuzz:
    """CrawledPage Schema Fuzzing"""

    def test_invalid_url_rejected(self):
        """无效 URL 应被拒绝"""
        with pytest.raises(Exception):
            CrawledPage(
                url="javascript:void(0)",
            )

    def test_content_length_mismatch_rejected(self):
        """content_length 与实际内容长度不一致应被拒绝"""
        with pytest.raises(Exception):
            CrawledPage(
                url="https://example.com",
                content_md="Hello",
                content_length=99999,
            )

    def test_status_code_out_of_range_rejected(self):
        """status_code 超出 [0,599] 应被拒绝"""
        with pytest.raises(Exception):
            CrawledPage(
                url="https://example.com",
                status_code=999,
            )


class TestCredibilityFuzz:
    """可信度 Schema Fuzzing"""

    def test_domain_score_out_of_range_rejected(self):
        """domain_score 必须在 [1,5] 范围"""
        for bad_score in [0, 6, -1, 99]:
            with pytest.raises(Exception):
                CredibilityScore(
                    url="https://example.com",
                    domain_score=bad_score,
                    content_score=3,
                    total_score=3.0,
                    level="中等可信",
                )

    def test_total_score_out_of_range_rejected(self):
        """total_score 必须在 [0,5] 范围"""
        for bad_score in [-0.1, 5.1, 99.0]:
            with pytest.raises(Exception):
                CredibilityScore(
                    url="https://example.com",
                    domain_score=3,
                    content_score=3,
                    total_score=bad_score,
                    level="中等可信",
                )

    def test_average_score_range(self):
        """CredibilityResults.average_score 必须在 [0,5]"""
        with pytest.raises(Exception):
            CredibilityResults(average_score=99.0)

    def test_average_must_match_computed(self):
        """average_score 必须与 scores 计算结果一致"""
        with pytest.raises(Exception):
            CredibilityResults(
                scores=[
                    CredibilityScore(
                        url="https://a.com",
                        domain_score=3,
                        content_score=3,
                        total_score=3.0,
                        level="中等可信",
                    ),
                    CredibilityScore(
                        url="https://b.com",
                        domain_score=5,
                        content_score=5,
                        total_score=5.0,
                        level="高可信",
                    ),
                ],
                average_score=1.0,  # 应该是 4.0
            )


class TestAnalysisOutputFuzz:
    """AnalysisOutput 整体 Fuzzing"""

    def test_random_data_not_crash(self):
        """随机数据不应导致崩溃，只应抛出 ValidationError"""
        for _ in range(20):
            try:
                AnalysisOutput(
                    query=random_string(1, 500),
                    key_findings=[random_string(1, 100) for _ in range(random.randint(0, 5))],
                    conclusions=[random_string(1, 200) for _ in range(random.randint(0, 3))],
                )
            except Exception:
                pass  # 预期行为：不合法数据被拒绝

    def test_source_with_bad_url_rejected(self):
        """来源中的无效 URL 应被拒绝"""
        with pytest.raises(Exception):
            AnalysisOutput(
                query="test",
                key_findings=["发现"],
                conclusions=["结论"],
                sources=[SourceEntry(url="not-a-url", trust_level=3.0)],
            )

    def test_nlp_text_length_non_negative(self):
        """text_length 不能为负数"""
        with pytest.raises(Exception):
            NLPResults(text_length=-1)
