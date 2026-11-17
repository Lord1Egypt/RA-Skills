import json
from pathlib import Path
import unittest

FIXTURE = Path(__file__).parent / "fixtures" / "ai-card.json"
from scripts import query_watch_repair


class QueryWatchRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = query_watch_repair
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_price_matches_grouped_brand(self):
        result = self.m.find_price(self.data, "欧米茄", "基础款")
        self.assertEqual(result["referencePrice"], "3000")
        self.assertEqual(result["verifiedAt"], "2026-07-17")
        self.assertIn("price", result["sourceUrl"])

    def test_price_normalizes_display_name_slug_and_common_alias(self):
        for brand in ("iwc", "万国（IWC）"):
            with self.subTest(brand=brand):
                self.assertEqual(self.m.find_price(self.data, brand, "基础款")["referencePrice"], "3000")
        for brand in ("baume-mercier", "名仕", "名士"):
            with self.subTest(brand=brand):
                self.assertEqual(self.m.find_price(self.data, brand, "基础款")["referencePrice"], "1300")

    def test_load_data_restricts_remote_source_and_validates_schema(self):
        with self.assertRaises(ValueError):
            self.m.load_data("http://example.com/ai-card.json")
        bad = dict(self.data)
        bad["schemaVersion"] = "9.9"
        with self.assertRaises(ValueError):
            self.m.validate_data(bad)
        missing = {"schemaVersion": "1.0"}
        with self.assertRaises(ValueError):
            self.m.validate_data(missing)

    def test_case_limit_rejects_non_positive_and_caps_large_values(self):
        for value in (0, -1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.m.find_cases(self.data, limit=value)
        self.assertLessEqual(len(self.m.find_cases(self.data, limit=1000)), 100)

    def test_estimator_display_brand_name(self):
        result = self.m.estimate_repair(
            self.data, brand="万国（IWC）", movement="基础机械", symptom="晚上停走"
        )
        self.assertEqual(result["brandSlug"], "iwc")
        self.assertEqual(result["priceLabel"], "3000 元")

    def test_price_unknown_brand_does_not_guess(self):
        result = self.m.find_price(self.data, "未知品牌", "基础款")
        self.assertIsNone(result["referencePrice"])
        self.assertEqual(result["status"], "insufficient_evidence")

    def test_case_search_ranks_brand_and_issue(self):
        results = self.m.find_cases(self.data, brand="浪琴", issue="进水", limit=3)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["brand"], "浪琴")
        self.assertIn("进水", results[0]["summary"])
        self.assertTrue(results[0]["url"].startswith("https://www.wuhanhengdeli.cn/cases/"))

    def test_review_never_calls_reference_a_market_average(self):
        result = self.m.review_quote(
            self.data, brand="欧米茄", category="基础款", quoted_price=5200,
            issue="停走", region="武汉"
        )
        rendered = json.dumps(result, ensure_ascii=False)
        self.assertNotIn("市场平均价", rendered)
        self.assertNotIn("行业平均价", rendered)
        self.assertEqual(result["reference"]["referencePrice"], "3000")
        self.assertIn("零件费", result["limits"])
        self.assertIn("实物", result["disclaimer"])

    def test_review_requires_numeric_quote(self):
        for value in (-1, float("nan"), float("inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.m.review_quote(self.data, "浪琴", "基础款", value, "停走", "武汉")

    def test_estimator_deep_link_and_mechanical_price(self):
        result = self.m.estimate_repair(
            self.data, brand="欧米茄", movement="基础机械", symptom="晚上停走"
        )
        self.assertEqual(result["status"], "estimate_found")
        self.assertEqual(result["priceLabel"], "3000 元")
        self.assertEqual(result["actionLabel"], "检修保养")
        self.assertEqual(
            result["estimateUrl"],
            "https://www.wuhanhengdeli.cn/estimate?brand=omega&movement=mechanical-basic&symptom=night-stop",
        )
        self.assertIn("实物检测", result["disclaimer"])

    def test_estimator_accepts_website_brand_slug(self):
        result = self.m.estimate_repair(
            self.data, brand="omega", movement="mechanical-basic", symptom="night-stop"
        )
        self.assertEqual(result["status"], "estimate_found")
        self.assertEqual(result["priceLabel"], "3000 元")
        self.assertEqual(result["reference"]["matchedGroup"], "劳力士、万国、卡地亚、沛纳海、真力时、欧米茄")

    def test_estimator_multifunction_does_not_derive_unpublished_range(self):
        result = self.m.estimate_repair(
            self.data, brand="omega", movement="mechanical-multifunction", symptom="timing-error"
        )
        self.assertEqual(result["status"], "not_directly_comparable")
        self.assertIsNone(result["price"])
        self.assertIsNone(result["priceLabel"])
        self.assertIn("不能据此推算", result["detail"])

    def test_estimator_quartz_failed_does_not_derive_unpublished_price(self):
        result = self.m.estimate_repair(
            self.data, brand="浪琴", movement="基础石英表", symptom="换电池后仍不走"
        )
        self.assertEqual(result["status"], "not_directly_comparable")
        self.assertIsNone(result["price"])
        self.assertIsNone(result["priceLabel"])
        self.assertIn("不能据此推算", result["detail"])

    def test_estimator_output_does_not_add_unsourced_diagnostic_narratives(self):
        scenarios = [
            ("longines", "quartz-basic", "battery-stop"),
            ("longines", "mechanical-basic", "water-ingress"),
            ("longines", "mechanical-basic", "full-stop"),
            ("longines", "mechanical-chronograph", "full-stop"),
        ]
        forbidden = ("长期维修经验", "大概率", "常见情况", "电路", "线圈")
        for brand, movement, symptom in scenarios:
            with self.subTest(movement=movement, symptom=symptom):
                result = self.m.estimate_repair(self.data, brand, movement, symptom)
                detail = result.get("detail", "")
                for phrase in forbidden:
                    self.assertNotIn(phrase, detail)

    def test_estimator_rejects_mismatched_movement_and_symptom(self):
        result = self.m.estimate_repair(
            self.data, brand="浪琴", movement="基础石英表", symptom="晚上停走"
        )
        self.assertEqual(result["status"], "invalid_combination")
        self.assertIsNone(result["priceLabel"])

    def test_estimator_unknown_brand_does_not_guess(self):
        result = self.m.estimate_repair(
            self.data, brand="未知品牌", movement="基础机械", symptom="完全停走"
        )
        self.assertEqual(result["status"], "insufficient_evidence")
        self.assertIsNone(result["priceLabel"])


if __name__ == "__main__":
    unittest.main()
