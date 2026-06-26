from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import query_orders
import recommendation_logic
from skill_http import SkillHttpError


class QueryOrdersScriptTest(unittest.TestCase):
    @patch.object(query_orders, "load_mobile", return_value=None)
    @patch.object(
        query_orders,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(query_orders, "fetch_json")
    def test_main_fetches_dedicated_orders_endpoint_and_summarizes_drinks(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
    ) -> None:
        fetch_json_mock.return_value = {
            "data": {
                "orders": [
                    {
                        "createdAt": "2025-08-08 14:16:25",
                        "orderSn": "20250808141625274275",
                        "state": 6,
                        "pickNo": "A001",
                        "serverTime": "2025-08-08 14:36:25",
                        "goodsNum": 2,
                        "goods": [
                            {
                                "name": "苦尽甘来拿铁",
                                "spec": "大杯",
                                "attr": "热 / 3分糖",
                            },
                            {
                                "name": "花魁毛尖",
                                "spec": "大杯",
                                "attr": "少冰 / 5分糖",
                            },
                        ],
                        "store": {"name": "幂茶幂咖望京小街店"},
                    },
                    {
                        "createdAt": "2025-08-09 10:10:00",
                        "orderSn": "20250809101000000001",
                        "state": 2,
                        "pickNo": "B108",
                        "serverTime": "2025-08-09 10:30:00",
                        "goodsNum": 1,
                        "goods": [
                            {
                                "name": "桂花美式",
                                "spec": "中杯",
                                "attr": "少冰 / 无糖",
                            }
                        ],
                        "store": {"name": "幂茶幂咖国贸店"},
                    },
                ]
            }
        }
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            [
                "query_orders.py",
                "--mobile",
                "15712459595",
                "--query",
                "我都定了哪些饮料，我喝了多少咖啡",
            ],
        ), patch("sys.stdout", stdout):
            exit_code = query_orders.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("## 订单历史", output)
        self.assertIn("苦尽甘来拿铁", output)
        self.assertIn("花魁毛尖", output)
        self.assertIn("桂花美式", output)
        self.assertIn("## 订单摘要", output)
        self.assertIn("当前可见订单数：2单。", output)
        self.assertIn("已完成订单数：1单。", output)
        self.assertIn("可见饮品杯数：3杯。", output)
        self.assertIn("## 给用户的订单等级", output)
        self.assertIn("你已经在新一咖啡点单3杯，我们越来越有默契了！", output)
        self.assertNotIn("Level 2", output)
        self.assertIn("买过的饮品：苦尽甘来拿铁、花魁毛尖、桂花美式。", output)
        self.assertIn("可确认咖啡相关杯数：1杯。", output)
        self.assertIn("混合订单里还有无法精确计杯的咖啡相关饮品：苦尽甘来拿铁。", output)
        self.assertIn("咖啡相关饮品：2项（按商品名初步识别）：苦尽甘来拿铁、桂花美式。", output)
        self.assertIn("订单信息只能基于本次查询到的订单字段，不能预估、估算或模糊处理。", output)
        self.assertNotIn("/skill/xinyi/context", output)
        self.assertEqual(
            fetch_json_mock.call_args.args,
            (
                "http://127.0.0.1:8020/skill/xinyi/orders?mobile=15712459595",
                5,
            ),
        )

    def test_order_rating_uses_non_overlapping_cup_levels(self) -> None:
        cases = [
            (1, "你已经在新一咖啡点单1杯，欢迎开启美味体验！"),
            (2, "你已经在新一咖啡点单2杯，欢迎开启美味体验！"),
            (3, "你已经在新一咖啡点单3杯，我们越来越有默契了！"),
            (5, "你已经在新一咖啡点单5杯，我们越来越有默契了！"),
            (6, "你已经在新一咖啡点单6杯，你一定是新一咖啡的忠实铁粉吧！"),
            (10, "你已经在新一咖啡点单10杯，你一定是新一咖啡的忠实铁粉吧！"),
            (11, "你已经在新一咖啡点单11杯，简直是我们的超级品鉴官！"),
            (14, "你已经在新一咖啡点单14杯，简直是我们的超级品鉴官！"),
            (
                15,
                "你已经在新一咖啡点单15杯，你不仅懂咖啡，有品位，更是新一不可或缺的灵魂伴侣，殿堂级知音！",
            ),
        ]

        for cup_count, message in cases:
            with self.subTest(cup_count=cup_count):
                lines = query_orders.build_order_rating_lines(cup_count)

                self.assertEqual(lines, [message])

    def test_zero_cups_do_not_output_order_rating(self) -> None:
        self.assertEqual(query_orders.build_order_rating_lines(0), [])

    def test_render_orders_result_outputs_rating_copy_without_level_label(self) -> None:
        output = query_orders.render_orders_result(
            {
                "orders": [
                    {
                        "createdAt": "2026-05-06 12:00:00",
                        "orderSn": "A001",
                        "state": 6,
                        "goodsNum": 5,
                        "goods": [{"name": "椰椰糯米冰浆", "num": 5}],
                    },
                    {
                        "createdAt": "2026-05-06 13:00:00",
                        "orderSn": "A002",
                        "state": 6,
                        "goodsNum": 4,
                        "goods": [{"name": "芒芒糯米冰浆", "num": 4}],
                    },
                ]
            }
        )

        self.assertIn("## 给用户的订单等级", output)
        self.assertIn("你已经在新一咖啡点单9杯，你一定是新一咖啡的忠实铁粉吧！", output)
        self.assertNotIn("Level 3", output)

    def test_english_coffee_keywords_are_shared_with_preference_tags(self) -> None:
        self.assertTrue(query_orders.is_coffee_name("Espresso Tonic"))
        self.assertIn(
            "espresso",
            recommendation_logic.extract_name_preference_tags("Espresso Tonic"),
        )

    @patch.object(query_orders, "load_mobile", return_value="15712459595")
    @patch.object(
        query_orders,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(query_orders, "fetch_json")
    def test_status_filter_can_reuse_saved_mobile(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
    ) -> None:
        fetch_json_mock.return_value = {"data": {"orders": []}}
        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["query_orders.py", "--use-saved-mobile", "--status", "4", "--debug"],
        ), patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            exit_code = query_orders.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("暂无订单记录。", stdout.getvalue())
        self.assertIn("DEBUG query_orders: resolved mobile from local state", stderr.getvalue())
        self.assertEqual(
            fetch_json_mock.call_args.args,
            (
                "http://127.0.0.1:8020/skill/xinyi/orders?mobile=15712459595&status=4",
                5,
            ),
        )

    @patch.object(query_orders, "load_mobile", return_value=None)
    @patch.object(query_orders, "fetch_json")
    def test_missing_mobile_outputs_actionable_prompt(
        self,
        fetch_json_mock,
        _load_mobile_mock,
    ) -> None:
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["query_orders.py", "--query", "我喝了多少咖啡"],
        ), patch("sys.stdout", stdout):
            exit_code = query_orders.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("未提供手机号，不能查询订单历史。", stdout.getvalue())
        self.assertIn("微信小程序【新一咖啡】绑定手机号", stdout.getvalue())
        fetch_json_mock.assert_not_called()

    @patch.object(query_orders, "load_mobile", return_value=None)
    @patch.object(
        query_orders,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(query_orders, "fetch_json")
    def test_http_error_outputs_order_specific_unavailable_message(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
    ) -> None:
        fetch_json_mock.side_effect = SkillHttpError("服务暂时返回 HTTP 500")
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["query_orders.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = query_orders.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("订单历史暂时没拿到：服务暂时返回 HTTP 500", stdout.getvalue())
        self.assertIn("不要猜用户下过几单", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
