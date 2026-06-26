from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import build_response


class BuildResponseIntentTest(unittest.TestCase):
    def test_generic_past_word_does_not_trigger_order_followup(self) -> None:
        self.assertFalse(
            build_response.is_order_query(
                {"query": "我过去喜欢喝拿铁，这杯热量多少"}
            )
        )
        self.assertFalse(
            build_response.is_order_query(
                {"query": "完成订单后能换吗"}
            )
        )

    def test_specific_order_queries_still_trigger_order_followup(self) -> None:
        cases = (
            "订单",
            "看我的历史订单",
            "我买过什么",
            "我已完成几单",
        )

        for query in cases:
            with self.subTest(query=query):
                self.assertTrue(build_response.is_order_query({"query": query}))


if __name__ == "__main__":
    unittest.main()
