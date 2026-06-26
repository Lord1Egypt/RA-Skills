#!/usr/bin/env python3
"""Regression tests for the daily reading briefing workflow."""

from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from weread_daily_read import (  # noqa: E402
    build_content_analysis,
    choose_daily_request,
    classify_book_type,
    classify_highlight_text,
    keyword_candidates,
)


class DailyReadTests(unittest.TestCase):
    def test_choose_daily_request_rotates_by_date(self) -> None:
        requests = [{"book": "A"}, {"book": "B"}, {"book": "C"}]
        selected, index = choose_daily_request(requests, date(2026, 6, 22), "date")

        self.assertEqual(index, date(2026, 6, 22).toordinal() % len(requests))
        self.assertEqual(selected, requests[index])

    def test_choose_daily_request_can_force_first(self) -> None:
        requests = [{"book": "A"}, {"book": "B"}]
        selected, index = choose_daily_request(requests, date(2026, 6, 22), "first")

        self.assertEqual(index, 0)
        self.assertEqual(selected, {"book": "A"})

    def test_classify_highlight_detects_multiple_analysis_tags(self) -> None:
        text = "这个理论的关键不是预测，而是解释系统如何运行，因此结论很清楚。"
        tags = classify_highlight_text(text, book_type="nonfiction")

        self.assertIn("theory", tags)
        self.assertIn("viewpoint", tags)
        self.assertIn("conclusion", tags)

    def test_classify_book_type_uses_metadata_and_chapters(self) -> None:
        book = {"title": "制度与经济增长", "category": "经济-社科", "intro": "讨论制度、市场和国家能力。"}
        chapters = [{"title": "第一章 理论框架"}]

        self.assertEqual(classify_book_type(book, chapters), "nonfiction")

    def test_keyword_candidates_excludes_common_stop_terms(self) -> None:
        terms = keyword_candidates(["我们需要理解制度，制度塑造市场，市场反馈制度。"], limit=5)

        self.assertIn("制度", terms)
        self.assertNotIn("我们", terms)

    def test_build_content_analysis_returns_expected_sections(self) -> None:
        book = {"title": "样本书", "author": "作者", "intro": "一本关于系统、机制和行动的书。"}
        chapters = [{"chapterUid": 1, "chapterIdx": 1, "title": "理论框架", "level": 1}]
        highlights = [
            {
                "markText": "这个理论解释了系统运行的机制。",
                "chapterTitle": "理论框架",
                "totalCount": 120,
                "tags": ["theory"],
            },
            {
                "markText": "因此，真正重要的是把观点落实为行动。",
                "chapterTitle": "结论",
                "totalCount": 90,
                "tags": ["viewpoint", "conclusion", "practice"],
            },
        ]

        analysis = build_content_analysis(book=book, chapters=chapters, highlights=highlights, reviews={}, book_type="nonfiction")

        self.assertEqual(analysis["bookType"], "nonfiction")
        self.assertTrue(analysis["theory"]["evidence"])
        self.assertTrue(analysis["conclusions"]["evidence"])
        self.assertTrue(analysis["practice"]["evidence"])
        self.assertIn("dataBoundary", analysis)


if __name__ == "__main__":
    unittest.main()
