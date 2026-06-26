from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import recommend_drink
from skill_http import SkillHttpError


class RecommendDrinkScriptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.load_activity_joined_patcher = patch.object(
            recommend_drink,
            "load_activity_joined",
            return_value=None,
        )
        self.load_activity_joined_mock = self.load_activity_joined_patcher.start()
        self.addCleanup(self.load_activity_joined_patcher.stop)

    def test_clear_mobile_exits_without_fetching_context(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch.object(recommend_drink, "clear_mobile") as clear_mobile_mock, patch.object(
            recommend_drink,
            "fetch_json",
        ) as fetch_json_mock, patch.object(
            recommend_drink,
            "load_config",
        ) as load_config_mock, patch.object(
            recommend_drink,
            "load_mobile",
        ) as load_mobile_mock, patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--clear-mobile"],
        ), patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("已清空本地手机号缓存和活动状态。", stdout.getvalue())
        clear_mobile_mock.assert_called_once_with()
        fetch_json_mock.assert_not_called()
        load_config_mock.assert_not_called()
        load_mobile_mock.assert_not_called()
        self.load_activity_joined_mock.assert_not_called()

    def test_show_mobile_status_reads_local_state_without_fetching_context(self) -> None:
        stdout = io.StringIO()

        with patch.object(
            recommend_drink,
            "load_state",
            return_value={
                "mobile": "18210234223",
                "activityJoined": True,
                "updatedAt": "2026-05-07T03:00:00+00:00",
            },
        ) as load_state_mock, patch.object(
            recommend_drink,
            "fetch_json",
        ) as fetch_json_mock, patch.object(
            recommend_drink,
            "load_config",
        ) as load_config_mock, patch.object(
            recommend_drink,
            "load_mobile",
        ) as load_mobile_mock, patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--show-mobile-status"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertIn("本地已保存手机号：18210234223", output)
        self.assertIn("活动状态：已领取过", output)
        self.assertIn("已领取内容：Skill用户大礼包包含", output)
        self.assertIn("缓存更新时间：2026-05-07T03:00:00+00:00", output)
        load_state_mock.assert_called_once_with()
        fetch_json_mock.assert_not_called()
        load_config_mock.assert_not_called()
        load_mobile_mock.assert_not_called()
        self.load_activity_joined_mock.assert_not_called()

    def test_show_mobile_status_preflights_locked_mobile_switch_without_fetching_context(self) -> None:
        stdout = io.StringIO()

        with patch.object(
            recommend_drink,
            "load_state",
            return_value={
                "mobile": "18210234223",
                "activityJoined": True,
                "updatedAt": "2026-05-07T03:00:00+00:00",
            },
        ) as load_state_mock, patch.object(
            recommend_drink,
            "fetch_json",
        ) as fetch_json_mock, patch.object(
            recommend_drink,
            "load_config",
        ) as load_config_mock, patch.object(
            recommend_drink,
            "load_mobile",
        ) as load_mobile_mock, patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--show-mobile-status", "--candidate-mobile", "18539991423"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertIn("本地已保存手机号：18210234223", output)
        self.assertIn("活动状态：已领取过", output)
        self.assertIn("已领取内容：Skill用户大礼包包含", output)
        self.assertIn("候选手机号：18539991423", output)
        self.assertIn("本机缓存已确认当前手机号参与活动，不能更换手机号重复领取", output)
        load_state_mock.assert_called_once_with()
        fetch_json_mock.assert_not_called()
        load_config_mock.assert_not_called()
        load_mobile_mock.assert_not_called()
        self.load_activity_joined_mock.assert_not_called()

    def test_show_mobile_status_preflights_unconfirmed_mobile_switch_without_fetching_context(self) -> None:
        stdout = io.StringIO()

        with patch.object(
            recommend_drink,
            "load_state",
            return_value={
                "mobile": "18210234223",
                "activityJoined": False,
            },
        ), patch.object(
            recommend_drink,
            "fetch_json",
        ) as fetch_json_mock, patch.object(
            recommend_drink,
            "load_config",
        ) as load_config_mock, patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--show-mobile-status", "--candidate-mobile", "18539991423"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertIn("候选手机号：18539991423", output)
        self.assertIn("本地未确认已参与", output)
        self.assertIn("需要用户明确确认后再走领取流程", output)
        fetch_json_mock.assert_not_called()
        load_config_mock.assert_not_called()
        self.load_activity_joined_mock.assert_not_called()

    def test_show_mobile_status_handles_missing_local_state(self) -> None:
        stdout = io.StringIO()

        with patch.object(
            recommend_drink,
            "load_state",
            return_value={},
        ) as load_state_mock, patch.object(
            recommend_drink,
            "fetch_json",
        ) as fetch_json_mock, patch.object(
            recommend_drink,
            "load_config",
        ) as load_config_mock, patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--show-mobile-status"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("本地未保存新一咖啡手机号。", stdout.getvalue())
        load_state_mock.assert_called_once_with()
        fetch_json_mock.assert_not_called()
        load_config_mock.assert_not_called()
        self.load_activity_joined_mock.assert_not_called()

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value=None)
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_main_outputs_llm_friendly_text_instead_of_json(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
        post_json_mock,
    ) -> None:
        events: list[tuple[str, str]] = []
        post_json_mock.side_effect = lambda url, timeout, payload: (
            events.append(("claim", payload["mobile"])),
            {
                "data": {
                    "kind": "already_claimed",
                    "user": {"mobile": "15712459595", "nickname": "双龙"},
                }
            },
        )[1]
        self.load_activity_joined_mock.return_value = True
        fetch_json_mock.return_value = {
            "data": {
                "goods": [
                    {
                        "name": "杨枝甘露|轻乳版",
                        "categories": ["果咖", "轻负担"],
                        "price": "16.80",
                        "cupSizes": ["大杯"],
                        "temperatures": ["少冰", "去冰"],
                        "sugarLevels": ["3分糖", "5分糖"],
                        "calories": "120\nkcal",
                        "ingredients": ["芒果", "西柚"],
                    }
                ],
                "stores": [
                    {
                        "name": "幂茶幂咖|望京店",
                        "address": "北京市朝阳区望京街9号\n商业楼1层",
                        "facilities": "外摆区，休息区，宠物友好。",
                        "storeMobile": "010-12345678",
                        "businessStatus": 1,
                        "labels": [{"name": "休息区"}],
                        "lat": "39.990326",
                        "lng": "116.483659",
                        "operatingStatus": 1,
                        "realtimeState": 1,
                        "makingCupCount": 4,
                        "makingCupMinutes": 18,
                        "storeType": 2,
                        "supportUnattendedMode": 1,
                    }
                ],
                "weather": {
                    "city": "Beijing",
                    "condition": "sunny",
                    "temperatureC": 26,
                },
                "orders": {
                    "orders": [
                        {
                            "createdAt": "2025-08-08 14:16:25",
                            "orderSn": "20250808141625274275",
                            "state": 2,
                            "pickNo": "Z108",
                            "serverTime": "2025-08-08 14:36:25",
                            "goodsNum": 1,
                            "goods": [
                                {
                                    "name": "葡萄毛尖轻咖",
                                    "spec": "中杯",
                                    "attr": "正常冰|7分糖",
                                }
                            ],
                            "store": {
                                "name": "幂茶幂咖望京小街店",
                            },
                        }
                    ]
                },
            }
        }

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            [
                "recommend_drink.py",
                "--mobile",
                "15712459595",
                "--query",
                "想喝不苦的",
                "--scene",
                "下午茶",
                "--preference",
                "低卡",
            ],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("## 用户上下文", output)
        self.assertIn("## 商品列表", output)
        self.assertIn("| 商品名称 | 分类 | 价格 | 杯型 | 温度 | 糖度 | 卡路里 | 配料 |", output)
        self.assertIn("果咖、轻负担", output)
        self.assertNotIn("## 门店列表", output)
        self.assertIn("## 订单历史", output)
        self.assertNotIn("## 订单追问素材", output)
        self.assertIn("## 推荐素材", output)
        self.assertIn("## 回答要求", output)
        self.assertNotIn("## 门店摘要建议", output)
        self.assertNotIn('"context"', output)
        self.assertIn("杨枝甘露\\|轻乳版", output)
        self.assertIn("正常冰\\|7分糖", output)
        self.assertIn("120<br>kcal", output)
        self.assertNotIn("北京市朝阳区望京街9号<br>商业楼1层", output)
        self.assertNotIn("010-12345678", output)
        self.assertNotIn("外摆区，休息区，宠物友好。", output)
        self.assertNotIn("Box 门店", output)
        self.assertNotIn("支持无人模式", output)
        self.assertIn("像懂茶饮也懂咖啡的店员姐姐给朋友建议一样自然", output)
        self.assertIn("今天这个温度喝它刚好", output)
        self.assertIn("回答需要有层次和重点", output)
        self.assertIn("主推饮品名必须加粗", output)
        self.assertIn("只有用户明确提到门店时，才返回门店信息", output)
        self.assertIn("少量使用合适 emoji", output)
        self.assertIn("不要使用“推荐理由”", output)
        self.assertIn("有人情味", output)
        self.assertIn("接口没返回的数据不要编造", output)
        self.assertIn("不要使用“根据你的历史订单偏好”", output)
        self.assertNotIn("是否已参加活动", output)
        self.assertIn("当前问题不需要账户权益信息", output)
        self.assertIn("不要追加无关的账户、礼包或领取状态", output)
        self.assertNotIn("三重福利已经到账", output)
        self.assertNotIn("可说明身份验证成功", output)
        self.assertNotIn("登录成功后只提示用户已经领取礼包", output)
        self.assertNotIn("您可以通过绑定【新一咖啡】的注册手机号", output)
        self.assertIn("推荐候选饮品：杨枝甘露|轻乳版", output)
        self.assertIn("挺舒服", output)
        self.assertIn("商品分类：果咖、轻负担", output)
        self.assertIn("主要配料：芒果、西柚", output)
        self.assertNotIn("若回答中展示门店，必须展示全部返回门店", output)
        self.assertNotIn("不要只推荐某一家门店", output)
        self.assertNotIn("若展示门店，门店电话也一并给出", output)
        self.assertNotIn("若展示门店且门店返回了 facilities", output)
        self.assertNotIn("根据用户这次意图自然承接门店", output)
        self.assertNotIn("您可以到我们的店领取奖励", output)
        self.assertNotIn("您可以到我们店畅饮", output)
        self.assertNotIn("如果你在附近", output)
        self.assertNotIn("附近可去的门店", output)
        self.assertNotIn("当前查询到的门店", output)
        self.assertNotIn("目前查到的门店", output)
        self.assertEqual(fetch_json_mock.call_count, 1)
        post_json_mock.assert_not_called()
        self.assertEqual(events, [])
        self.assertEqual(
            fetch_json_mock.call_args_list[0].args,
            (
                "http://127.0.0.1:8020/skill/xinyi/context?mobile=15712459595",
                5,
            ),
        )
        self.load_activity_joined_mock.assert_called_once_with("15712459595")

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value=None)
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_non_activity_query_omits_brand_activity_block(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
        post_json_mock,
    ) -> None:
        post_json_mock.return_value = {
            "data": {
                "kind": "already_claimed",
                "user": {"mobile": "15712459595", "nickname": "双龙"},
            }
        }
        self.load_activity_joined_mock.return_value = True
        fetch_json_mock.return_value = {
            "data": {"goods": [], "stores": [], "weather": None, "orders": {"orders": []}}
        }
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--mobile", "15712459595", "--query", "今天喝什么"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertNotIn("## 品牌活动", output)
        self.assertNotIn("## 门店列表", output)
        self.assertNotIn("暂无门店数据", output)

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value=None)
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_personalized_recommendation_suggests_less_ordered_similar_drink(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
        post_json_mock,
    ) -> None:
        self.load_activity_joined_mock.return_value = True
        fetch_json_mock.return_value = {
            "data": {
                "goods": [
                    {
                        "name": "苦尽甘来拿铁",
                        "categories": ["咖啡", "拿铁"],
                        "price": "18.80",
                        "temperatures": ["热", "少冰"],
                        "sugarLevels": ["无糖", "3分糖"],
                        "ingredients": ["咖啡", "牛奶"],
                    },
                    {
                        "name": "桂花燕麦拿铁",
                        "categories": ["咖啡", "拿铁"],
                        "price": "19.80",
                        "temperatures": ["热", "少冰"],
                        "sugarLevels": ["3分糖", "5分糖"],
                        "ingredients": ["咖啡", "燕麦奶", "桂花"],
                    },
                    {
                        "name": "柠檬毛尖",
                        "categories": ["果茶"],
                        "price": "15.80",
                        "temperatures": ["少冰"],
                        "sugarLevels": ["5分糖"],
                        "ingredients": ["柠檬", "毛尖茶"],
                    },
                ],
                "stores": [],
                "weather": {"city": "Beijing", "condition": "sunny", "temperatureC": 18},
                "orders": {
                    "orders": [
                        {"goods": [{"name": "苦尽甘来拿铁", "num": 2}]},
                        {"goods": [{"name": "苦尽甘来拿铁", "num": 1}]},
                    ]
                },
            }
        }

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            [
                "recommend_drink.py",
                "--mobile",
                "15712459595",
                "--query",
                "推荐尝试一些我不常点的饮品",
            ],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("推荐候选饮品：桂花燕麦拿铁", output)
        self.assertIn("推荐尝试方向：优先推荐口味相邻但不常点或未点过的饮品", output)
        self.assertIn("常点参考：苦尽甘来拿铁（3次）", output)
        self.assertIn("这杯在可见订单里没有出现，适合做新尝试", output)
        self.assertNotIn("推荐候选饮品：苦尽甘来拿铁", output)
        post_json_mock.assert_not_called()

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value="15712459595")
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_main_does_not_use_saved_mobile_by_default(
        self,
        fetch_json_mock,
        _load_config_mock,
        load_mobile_mock,
        post_json_mock,
    ) -> None:
        fetch_json_mock.return_value = {
            "data": {"goods": [], "stores": [], "weather": None, "orders": None}
        }
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--query", "给我推荐一杯适合当下午茶的饮品"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        load_mobile_mock.assert_not_called()
        post_json_mock.assert_not_called()
        self.assertEqual(
            fetch_json_mock.call_args_list[0].args,
            ("http://127.0.0.1:8020/skill/xinyi/context", 5),
        )
        self.load_activity_joined_mock.assert_called_once_with(None)

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value=None)
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_order_followup_outputs_completed_count_materials(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
        post_json_mock,
    ) -> None:
        post_json_mock.return_value = {
            "data": {
                "kind": "already_claimed",
                "user": {"mobile": "15712459595", "nickname": "双龙"},
            }
        }
        self.load_activity_joined_mock.return_value = True
        fetch_json_mock.return_value = {
            "data": {
                "goods": [],
                "stores": [],
                "weather": None,
                "orders": {
                    "orders": [
                        {
                            "createdAt": "2025-08-08 14:16:25",
                            "orderSn": "20250808141625274275",
                            "state": 6,
                            "pickNo": "A001",
                            "serverTime": "2025-08-08 14:36:25",
                            "goodsNum": 1,
                            "goods": [{"name": "苦尽甘来拿铁"}],
                            "store": {"name": "幂茶幂咖望京店"},
                        },
                        {
                            "createdAt": "2025-08-09 10:10:00",
                            "orderSn": "20250809101000000001",
                            "state": 2,
                            "pickNo": "B002",
                            "serverTime": "2025-08-09 10:30:00",
                            "goodsNum": 1,
                            "goods": [{"name": "花魁毛尖"}],
                            "store": {"name": "幂茶幂咖望京店"},
                        },
                        {
                            "createdAt": "2025-08-10 10:10:00",
                            "orderSn": "20250810101000000002",
                            "state": 2,
                            "pickNo": "B003",
                            "serverTime": "2025-08-10 10:30:00",
                            "goodsNum": 1,
                            "goods": [{"name": "苦尽甘来拿铁"}],
                            "store": {"name": "幂茶幂咖望京店"},
                        },
                    ]
                },
            }
        }

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--mobile", "15712459595", "--query", "我完成了几单"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("## 订单追问素材", output)
        self.assertIn("你已完成1单，看得出来是真喜欢新一。", output)
        self.assertNotIn("骨灰级粉丝", output)
        self.assertIn("当前可见订单数：3单", output)
        self.assertIn("买过的商品可以提这些：苦尽甘来拿铁、花魁毛尖", output)
        self.assertNotIn("苦尽甘来拿铁、花魁毛尖、苦尽甘来拿铁", output)
        self.assertIn("到过的门店可以提这些：幂茶幂咖望京店", output)

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value=None)
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_activity_query_includes_lobster_activity(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
        post_json_mock,
    ) -> None:
        post_json_mock.return_value = {
            "data": {
                "kind": "already_claimed",
                "user": {"mobile": "15712459595", "nickname": "双龙"},
            }
        }
        self.load_activity_joined_mock.return_value = True
        fetch_json_mock.return_value = {
            "data": {
                "goods": [
                    {
                        "name": "中烘美式·耶加雪菲",
                        "categories": ["咖啡"],
                        "price": "14.80",
                        "cupSizes": ["中杯"],
                        "temperatures": ["正常冰"],
                        "sugarLevels": ["无糖"],
                        "calories": "10 kcal",
                        "ingredients": ["咖啡豆"],
                    }
                ],
                "stores": [],
                "weather": None,
                "orders": {"orders": []},
            }
        }

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--mobile", "15712459595", "--query", "有什么活动"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("## 品牌活动", output)
        self.assertIn("| 是否已参加活动 | 是 |", output)
        self.assertIn("Skill用户大礼包", output)
        self.assertIn("用户身份已验证成功", output)
        self.assertIn("登录成功后只提示用户已经领取礼包", output)
        self.assertIn("Skill用户大礼包包含", output)
        self.assertIn("小龙虾贴纸", output)
        self.assertIn("Skill用户专享赠饮券", output)
        self.assertIn("Skill用户身份标识", output)
        self.assertIn("活动规则：", output)
        self.assertIn("小龙虾贴纸：到任意门店对暗号【小龙虾】领取，先到先得", output)
        self.assertIn("Skill用户专享赠饮券：（前100名）爆款苦尽甘来拿铁免费兑换券 / （101-500名）5折饮品券 / （501-以后）8折饮品券", output)
        self.assertIn("Skill用户身份标识：参与即可添加SKILL 标签、龙虾头像", output)
        self.assertIn("用户正在问活动", output)
        self.assertIn("不要扩展到其它商品信息", output)
        self.assertIn("中烘美式·耶加雪菲", output)

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value=None)
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_obtained_after_registration_marks_activity_joined(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
        post_json_mock,
    ) -> None:
        post_json_mock.return_value = {
            "data": {
                "kind": "obtained_after_registration",
                "user": {"mobile": "18539991423", "nickname": "用户_991423"},
            }
        }
        self.load_activity_joined_mock.return_value = True
        fetch_json_mock.return_value = {
            "data": {"goods": [], "stores": [], "weather": None, "orders": {"orders": []}}
        }
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--mobile", "18539991423", "--query", "给我推荐一杯"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value=None)
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_main_falls_back_to_generic_copy_when_weather_api_fails(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
        post_json_mock,
    ) -> None:
        post_json_mock.return_value = {
            "data": {
                "kind": "already_claimed",
                "user": {"mobile": "15712459595", "nickname": "双龙"},
            }
        }
        fetch_json_mock.return_value = {
            "data": {
                "goods": [
                    {
                        "name": "葡萄毛尖轻咖",
                        "categories": ["果咖"],
                        "price": "16.80",
                        "cupSizes": ["大杯"],
                        "temperatures": ["热", "少冰"],
                        "sugarLevels": ["3分糖"],
                        "calories": "120 kcal",
                        "ingredients": ["葡萄"],
                    }
                ],
                "stores": [],
                "weather": None,
                "orders": {
                    "orders": [
                        {
                            "createdAt": "2025-08-08 14:16:25",
                            "orderSn": "20250808141625274275",
                            "state": 6,
                            "pickNo": "A001",
                            "serverTime": "2025-08-08 14:36:25",
                            "goodsNum": 1,
                            "goods": [
                                {
                                    "name": "葡萄毛尖轻咖",
                                    "spec": "大杯",
                                    "attr": "热 / 3分糖",
                                }
                            ],
                            "store": {"name": "幂茶幂咖望京店"},
                        }
                    ]
                },
            }
        }

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            [
                "recommend_drink.py",
                "--mobile",
                "15712459595",
            ],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("推荐候选饮品：葡萄毛尖轻咖", output)
        self.assertIn("像懂茶饮也懂咖啡的店员姐姐给朋友建议一样自然", output)
        self.assertIn("主推饮品名必须加粗", output)
        self.assertIn("只有用户明确提到门店时，才返回门店信息", output)
        self.assertIn("不要连续堆 emoji", output)
        self.assertIn("不要使用“推荐理由”", output)
        self.assertIn("分割线 `---` 单独隔开主动留资文案", output)
        self.assertIn("请把您微信小程序【新一咖啡】绑定的手机号发过来", output)
        self.assertIn("领取Skill用户大礼包", output)
        self.assertIn("如果仍未注册，再提示", output)
        self.assertIn("请先到微信小程序搜索【新一咖啡】", output)
        self.assertNotIn("今天天气", output)
        post_json_mock.assert_not_called()

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value="15712459595")
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_main_outputs_debug_logs_to_stderr(
        self,
        fetch_json_mock,
        _load_config_mock,
        load_mobile_mock,
        post_json_mock,
    ) -> None:
        post_json_mock.return_value = {
            "data": {
                "kind": "already_claimed",
                "user": {"mobile": "15712459595", "nickname": "双龙"},
            }
        }
        fetch_json_mock.return_value = {
            "data": {
                "goods": [],
                "stores": [],
                "weather": {"city": "Beijing", "condition": "sunny", "temperatureC": 26},
                "orders": None,
            }
        }

        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch.object(
            sys,
            "argv",
            [
                "recommend_drink.py",
                "--debug",
                "--use-saved-mobile",
                "--query",
                "有什么活动",
            ],
        ), patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("DEBUG recommend_drink: resolved mobile from local state", stderr.getvalue())
        self.assertNotIn("posting claim request", stderr.getvalue())
        self.assertIn("DEBUG recommend_drink: fetching context from http://127.0.0.1:8020/skill/xinyi/context?mobile=15712459595", stderr.getvalue())
        self.assertIn("DEBUG recommend_drink: context includes weather data", stderr.getvalue())
        self.assertIn("## 用户上下文", stdout.getvalue())
        load_mobile_mock.assert_called_once_with()
        post_json_mock.assert_not_called()

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value=None)
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_main_with_explicit_mobile_uses_context_without_claim_lookup(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
        post_json_mock,
    ) -> None:
        self.load_activity_joined_mock.return_value = True
        fetch_json_mock.return_value = {
            "data": {
                "goods": [],
                "stores": [],
                "weather": None,
                "orders": None,
            }
        }

        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--mobile", "15712459595", "--debug"],
        ), patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        self.assertNotIn("claim lookup failed", stderr.getvalue())
        post_json_mock.assert_not_called()
        self.assertNotIn("是否已参加活动", stdout.getvalue())
        self.assertIn("当前问题不需要账户权益信息", stdout.getvalue())
        self.assertEqual(
            fetch_json_mock.call_args_list[0].args,
            (
                "http://127.0.0.1:8020/skill/xinyi/context?mobile=15712459595",
                5,
            ),
        )

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value=None)
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_main_encodes_mobile_query_parameter(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
        post_json_mock,
    ) -> None:
        post_json_mock.return_value = {
            "data": {
                "kind": "unregistered",
                "user": None,
            }
        }
        fetch_json_mock.return_value = {
            "data": {"goods": [], "stores": [], "weather": None, "orders": None}
        }

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--mobile", "15712&x=1"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            fetch_json_mock.call_args_list[0].args,
            (
                "http://127.0.0.1:8020/skill/xinyi/context?mobile=15712%26x%3D1",
                5,
            ),
        )

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value=None)
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_main_outputs_graceful_fallback_when_context_request_fails(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
        post_json_mock,
    ) -> None:
        post_json_mock.return_value = {
            "data": {
                "kind": "already_claimed",
                "user": {"mobile": "15712459595"},
            }
        }
        fetch_json_mock.side_effect = SkillHttpError("服务暂时返回 HTTP 500")

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("## 实时数据状态", stdout.getvalue())
        self.assertIn("推荐上下文暂时没拿到：服务暂时返回 HTTP 500", stdout.getvalue())
        self.assertIn("本地已确认领取的手机号以本地状态优先", stdout.getvalue())
        self.assertIn("门店、菜单、价格、库存和排队信息不要编造", stdout.getvalue())

    @patch.object(recommend_drink, "post_json", create=True)
    @patch.object(recommend_drink, "load_mobile", return_value=None)
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_main_does_not_save_or_use_mobile_when_claim_does_not_match_user(
        self,
        fetch_json_mock,
        _load_config_mock,
        _load_mobile_mock,
        post_json_mock,
    ) -> None:
        post_json_mock.return_value = {
            "data": {
                "kind": "unregistered",
                "user": None,
            }
        }
        fetch_json_mock.return_value = {
            "data": {"goods": [], "stores": [], "weather": None, "orders": None}
        }

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["recommend_drink.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        post_json_mock.assert_not_called()
        self.assertEqual(
            fetch_json_mock.call_args_list[0].args,
            (
                "http://127.0.0.1:8020/skill/xinyi/context?mobile=15712459595",
                5,
            ),
        )

    @patch.object(recommend_drink, "load_mobile", return_value="15712459595")
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_use_saved_mobile_is_skipped_for_generic_recommendation_query(
        self,
        fetch_json_mock,
        _load_config_mock,
        load_mobile_mock,
    ) -> None:
        """普通菜单/热量/推荐查询即使带 --use-saved-mobile，也不能复用缓存手机号。"""
        fetch_json_mock.return_value = {
            "data": {"goods": [], "weather": None, "orders": None}
        }
        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch.object(
            sys,
            "argv",
            [
                "recommend_drink.py",
                "--use-saved-mobile",
                "--query",
                "杨枝甘露热量多少",
                "--debug",
            ],
        ), patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        self.assertIn(
            "DEBUG recommend_drink: saved mobile not reused: query is not activity/order/personalized",
            stderr.getvalue(),
        )
        self.assertEqual(
            fetch_json_mock.call_args_list[0].args,
            (
                "http://127.0.0.1:8020/skill/xinyi/context",
                5,
            ),
        )
        load_mobile_mock.assert_not_called()

    @patch.object(recommend_drink, "load_mobile", return_value="15712459595")
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_use_saved_mobile_is_honored_for_order_keyword_query(
        self,
        fetch_json_mock,
        _load_config_mock,
        load_mobile_mock,
    ) -> None:
        """订单类查询命中关键词时，应正常复用缓存手机号。"""
        fetch_json_mock.return_value = {
            "data": {"goods": [], "weather": None, "orders": None}
        }
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            [
                "recommend_drink.py",
                "--use-saved-mobile",
                "--query",
                "我买过多少杯",
            ],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            fetch_json_mock.call_args_list[0].args,
            (
                "http://127.0.0.1:8020/skill/xinyi/context?mobile=15712459595",
                5,
            ),
        )
        load_mobile_mock.assert_called_once_with()

    @patch.object(recommend_drink, "load_mobile", return_value="15712459595")
    @patch.object(
        recommend_drink,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(recommend_drink, "fetch_json")
    def test_use_saved_mobile_is_honored_for_personalized_recommendation_query(
        self,
        fetch_json_mock,
        _load_config_mock,
        load_mobile_mock,
    ) -> None:
        """明确个性化推荐应复用缓存手机号，普通菜单/热量查询仍不复用。"""
        fetch_json_mock.return_value = {
            "data": {"goods": [], "weather": None, "orders": None}
        }
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            [
                "recommend_drink.py",
                "--use-saved-mobile",
                "--query",
                "按我的口味推荐一杯没喝过的",
            ],
        ), patch("sys.stdout", stdout):
            exit_code = recommend_drink.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            fetch_json_mock.call_args_list[0].args,
            (
                "http://127.0.0.1:8020/skill/xinyi/context?mobile=15712459595",
                5,
            ),
        )
        load_mobile_mock.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
