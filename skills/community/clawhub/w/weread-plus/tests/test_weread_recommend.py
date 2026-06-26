#!/usr/bin/env python3
"""Regression tests for weread-plus recommendation filtering."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from weread_common import reading_state_from_shelf  # noqa: E402
from weread_report import build_recent_book_entry  # noqa: E402
from weread_recommend import score_candidate  # noqa: E402


class RecommendationFilteringTests(unittest.TestCase):
    def test_finished_books_are_marked_and_penalized(self) -> None:
        shelf = {
            "books": [
                {
                    "bookId": "done-1",
                    "title": "人生之书",
                    "author": "克里希那穆提",
                    "finishReading": 1,
                }
            ]
        }
        state = reading_state_from_shelf(shelf)
        item = {
            "book": {"bookId": "done-1", "title": "人生之书", "author": "克里希那穆提"},
            "sources": ["personalized"],
            "seedTitles": [],
        }

        score_candidate(item, mode="expand", profile={}, reading_state=state, goal=None)

        self.assertTrue(item["finishedReading"])
        self.assertIn("这本书已经读完", item["warnings"])
        self.assertLess(item["score"], 0)

    def test_finished_books_match_by_normalized_title_when_ids_differ(self) -> None:
        shelf = {
            "books": [
                {
                    "bookId": "shelf-edition",
                    "title": "风沙星辰（果麦经典）",
                    "author": "[法]安托万·德·圣埃克苏佩里",
                    "finishReading": 1,
                }
            ]
        }
        state = reading_state_from_shelf(shelf)
        item = {
            "book": {"bookId": "recommended-edition", "title": "风沙星辰", "author": "圣埃克苏佩里"},
            "sources": ["personalized"],
            "seedTitles": [],
        }

        score_candidate(item, mode="expand", profile={}, reading_state=state, goal=None)

        self.assertTrue(item["finishedReading"])

    def test_finished_books_match_second_edition_by_title_and_author(self) -> None:
        shelf = {
            "books": [
                {
                    "bookId": "old-edition",
                    "title": "思考，快与慢",
                    "author": "丹尼尔·卡尼曼",
                    "finishReading": 1,
                },
                {
                    "bookId": "second-edition",
                    "title": "思考，快与慢（第二版）",
                    "author": "[美]丹尼尔·卡尼曼",
                    "finishReading": 0,
                },
            ]
        }
        state = reading_state_from_shelf(shelf)
        item = {
            "book": {
                "bookId": "second-edition",
                "title": "思考，快与慢（第二版）",
                "author": "[美]丹尼尔·卡尼曼",
            },
            "sources": ["personalized"],
            "seedTitles": [],
        }

        score_candidate(item, mode="expand", profile={}, reading_state=state, goal=None)

        self.assertTrue(item["finishedReading"])
        self.assertIn("这本书已经读完", item["warnings"])

    def test_recent_books_flag_related_finished_editions(self) -> None:
        shelf = {
            "books": [
                {
                    "bookId": "old-edition",
                    "title": "思考，快与慢",
                    "author": "丹尼尔·卡尼曼",
                    "finishReading": 1,
                },
                {
                    "bookId": "second-edition",
                    "title": "思考，快与慢（第二版）",
                    "author": "[美]丹尼尔·卡尼曼",
                    "finishReading": 0,
                },
            ]
        }
        state = reading_state_from_shelf(shelf)

        entry = build_recent_book_entry(shelf["books"][1], state)

        self.assertTrue(entry["relatedFinished"])
        self.assertEqual(entry["relatedFinishedBook"]["bookId"], "old-edition")


if __name__ == "__main__":
    unittest.main()
