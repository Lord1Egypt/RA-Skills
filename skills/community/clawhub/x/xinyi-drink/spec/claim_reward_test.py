from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import claim_reward
from skill_http import SkillHttpError


class ClaimRewardScriptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.load_activity_joined_patcher = patch.object(claim_reward, "load_activity_joined", return_value=None)
        self.load_mobile_patcher = patch.object(claim_reward, "load_mobile", return_value=None, create=True)
        self.mark_activity_joined_patcher = patch.object(claim_reward, "mark_activity_joined")
        self.mark_activity_not_joined_patcher = patch.object(claim_reward, "mark_activity_not_joined")
        self.load_activity_joined_mock = self.load_activity_joined_patcher.start()
        self.load_mobile_mock = self.load_mobile_patcher.start()
        self.mark_activity_joined_mock = self.mark_activity_joined_patcher.start()
        self.mark_activity_not_joined_mock = self.mark_activity_not_joined_patcher.start()
        self.addCleanup(self.load_activity_joined_patcher.stop)
        self.addCleanup(self.load_mobile_patcher.stop)
        self.addCleanup(self.mark_activity_joined_patcher.stop)
        self.addCleanup(self.mark_activity_not_joined_patcher.stop)

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(claim_reward, "post_json", side_effect=SkillHttpError("网络请求失败"))
    def test_claim_script_does_not_reset_cached_activity_when_claim_request_fails(
        self,
        _post_json_mock,
        _load_config_mock,
    ) -> None:
        self.load_activity_joined_mock.return_value = None
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        # 与其它读类脚本对齐：网络失败输出可读降级文案，退出码 0。
        self.assertEqual(exit_code, 0)
        self.assertIn("领取活动失败：网络请求失败", stdout.getvalue())
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(claim_reward, "post_json")
    def test_claim_script_uses_local_claimed_state_before_backend_for_same_mobile(
        self,
        post_json_mock,
    ) -> None:
        self.load_mobile_mock.return_value = "15712459595"

        def load_activity_joined(mobile: str | None) -> bool | None:
            return mobile == "15712459595"

        self.load_activity_joined_mock.side_effect = load_activity_joined
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("领取结果：已领取过", output)
        self.assertIn("该手机号已经领取过 Skill用户大礼包", output)
        self.assertIn("已领取内容：小龙虾贴纸", output)
        self.assertIn("Skill用户身份标识", output)
        self.assertIn("Skill用户专享赠饮券", output)
        post_json_mock.assert_not_called()
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(claim_reward, "post_json")
    def test_claim_script_rejects_new_mobile_after_local_cache_claimed(
        self,
        post_json_mock,
    ) -> None:
        self.load_mobile_mock.return_value = "15712459595"

        def load_activity_joined(mobile: str | None) -> bool | None:
            return mobile == "15712459595"

        self.load_activity_joined_mock.side_effect = load_activity_joined
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "18210234223"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("本机缓存已确认手机号 157****9595 领取过 Skill用户大礼包", output)
        self.assertIn("不能更换手机号重复领取", output)
        self.assertNotIn("当前会话", output)
        post_json_mock.assert_not_called()
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(claim_reward, "post_json")
    def test_claim_script_renders_app_error_as_claim_failure(
        self,
        post_json_mock,
        _load_config_mock,
    ) -> None:
        post_json_mock.return_value = {
            "code": 600,
            "message": "领取暂时失败，请稍后再试。",
            "error": {"details": {"kind": "claim_failed"}},
        }
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "18210234223"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("领取活动失败：领取暂时失败，请稍后再试。", output)
        self.assertNotIn("领取结果：处理完成", output)
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(claim_reward, "post_json")
    def test_claim_script_does_not_rewrite_failed_already_claimed_response(
        self,
        post_json_mock,
        _load_config_mock,
    ) -> None:
        self.load_activity_joined_mock.return_value = False
        post_json_mock.return_value = {
            "code": 500,
            "data": {
                "kind": "already_claimed",
                "items": [],
                "user": {"mobile": "15712459595", "nickname": "双龙"},
            },
        }
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("领取结果：处理完成", output)
        self.assertNotIn("身份验证成功", output)
        self.assertNotIn("三重福利发放到账", output)
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(claim_reward, "post_json")
    def test_claim_script_handles_null_data_without_crashing(
        self,
        post_json_mock,
        _load_config_mock,
    ) -> None:
        post_json_mock.return_value = {"code": 200, "data": None}
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("领取结果：处理完成", stdout.getvalue())
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_claim_script_formats_raw_claim_response(
        self,
        urlopen_mock,
        _load_config_mock,
    ) -> None:
        first_response = urlopen_mock.return_value.__enter__.return_value
        first_response.read.return_value = (
            '{"code":200,"data":{"kind":"granted","successCount":1,"failCount":0,'
            '"items":[{"rank":2,"rankLevel":1,"state":1,"message":"发放成功","couponNum":1,'
            '"coupon":{"name":"（前100名）爆款苦尽甘来拿铁免费兑换券"}}],'
            '"user":{"mobile":"15712459595","nickname":"双龙"}}}'
        ).encode("utf-8")
        second_response = type("Resp", (), {})()
        second_response.read = lambda: (
            '{"data":{"goods":[{"name":"苦尽甘来拿铁","categories":["咖啡"],"price":"16.80","cupSizes":["大杯"],'
            '"temperatures":["热","少冰"],"sugarLevels":["3分糖"],"calories":"120 kcal","ingredients":["牛奶"]}],'
            '"stores":[{"name":"幂茶幂咖望京店","address":"北京市朝阳区望京街9号","storeMobile":"01088888888",'
            '"facilities":"休息区","businessStatus":1,'
            '"operatingStatus":1,"realtimeState":1,"labels":[{"name":"休息区"}],"makingCupCount":4,'
            '"makingCupMinutes":18,"storeType":2,"supportUnattendedMode":1},'
            '{"name":"幂茶幂咖诚盈中心店","address":"北京市朝阳区诚盈中心2号楼","storeMobile":"01066666666",'
            '"facilities":"休息区","businessStatus":1,"makingCupCount":0,"makingCupMinutes":0},'
            '{"name":"幂茶幂咖第三店","address":"北京市朝阳区第三街1号","storeMobile":"01033333333",'
            '"facilities":"外摆区","businessStatus":1,"makingCupCount":2,"makingCupMinutes":6}],'
            '"weather":{"city":"Beijing","condition":"cloudy","temperatureC":16},'
            '"orders":{"orders":[{"createdAt":"2025-08-08 14:16:25","orderSn":"20250808141625274275",'
            '"state":6,"pickNo":"A001","serverTime":"2025-08-08 14:36:25","goodsNum":1,'
            '"goods":[{"name":"苦尽甘来拿铁","spec":"大杯","attr":"热 / 3分糖"}],'
            '"store":{"name":"幂茶幂咖望京店"}}]}}}'
        ).encode("utf-8")
        second_context_manager = type(
            "ContextManager",
            (),
            {
                "__enter__": lambda self: second_response,
                "__exit__": lambda self, exc_type, exc, tb: False,
            },
        )()
        urlopen_mock.side_effect = [
            urlopen_mock.return_value,
            second_context_manager,
        ]

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("领取结果：身份验证成功", output)
        self.assertIn("身份验证成功。Skill用户大礼包已发放到账", output)
        self.assertIn("小龙虾贴纸（到任意门店对暗号【小龙虾】领取，先到先得）", output)
        self.assertIn("Skill用户身份标识", output)
        self.assertIn("Skill用户专享赠饮券「（前100名）爆款苦尽甘来拿铁免费兑换券」", output)
        self.assertIn("活动规则：", output)
        self.assertIn("小龙虾贴纸：到任意门店对暗号【小龙虾】领取，先到先得", output)
        self.assertIn("Skill用户专享赠饮券：（前100名）爆款苦尽甘来拿铁免费兑换券 / （101-500名）5折饮品券 / （501-以后）8折饮品券", output)
        self.assertIn("Skill用户身份标识：参与即可添加SKILL 标签、龙虾头像", output)
        self.assertIn("到账券：Skill用户专享赠饮券「（前100名）爆款苦尽甘来拿铁免费兑换券」。", output)
        self.assertNotIn("成功失败数量", output)
        self.assertNotIn("排名：2", output)
        self.assertIn("你已经领取礼包，现在可以查看你过去的订单信息", output)
        self.assertNotIn("你已完成", output)
        self.assertNotIn("骨灰级粉丝", output)
        self.assertNotIn("您可以到我们的店领取奖励", output)
        self.assertNotIn("门店信息我给您列全", output)
        self.assertNotIn("幂茶幂咖望京店", output)
        self.assertNotIn("幂茶幂咖诚盈中心店", output)
        self.assertNotIn("幂茶幂咖第三店", output)
        self.assertIn("哇我们的老朋友，今天天气偏凉，建议您喝苦尽甘来拿铁", output)
        self.assertNotIn('"kind"', output)
        self.mark_activity_joined_mock.assert_called_once_with("15712459595")
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_claim_script_prompts_user_to_share_bound_mobile_when_unregistered(
        self,
        urlopen_mock,
        _load_config_mock,
    ) -> None:
        response = urlopen_mock.return_value.__enter__.return_value
        response.read.return_value = (
            '{"code":200,"data":{"kind":"unregistered","successCount":0,"failCount":0,'
            '"items":[],"user":null}}'
        ).encode("utf-8")

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("领取结果：请先登录小程序", output)
        self.assertIn("15712459595 目前还没查到【新一咖啡】小程序登录/绑定记录", output)
        self.assertIn("🎁 领取步骤", output)
        self.assertIn("第一步：绑定手机号", output)
        self.assertIn("打开微信 → 搜索【新一咖啡】小程序 → 登录/注册并绑定您的手机号", output)
        self.assertIn("第二步：发送手机号给我", output)
        self.assertIn("绑定完成后，把您的手机号发过来，我帮您领取Skill用户大礼包", output)
        self.assertIn("Skill用户大礼包包含", output)
        self.assertIn("小龙虾贴纸", output)
        self.assertIn("Skill用户专享赠饮券", output)
        self.assertIn("Skill用户身份标识", output)
        self.assertIn("活动规则：", output)
        self.assertIn("Skill用户专享赠饮券：（前100名）爆款苦尽甘来拿铁免费兑换券 / （101-500名）5折饮品券 / （501-以后）8折饮品券", output)
        self.assertNotIn("请把您微信小程序【新一咖啡】绑定的手机号发过来", output)
        self.assertNotIn("参与方法：请先在微信小程序搜索【新一咖啡】", output)
        self.assertIn("搜索【新一咖啡】小程序", output)
        self.assertIn("这不是没有活动", output)
        self.assertNotIn("目前暂时没有其他活动", output)
        self.assertNotIn("要不要先来杯咖啡", output)
        self.assertNotIn("本次查询手机号：15712459595", output)
        self.assertNotIn("告知小程序绑定的手机号", output)
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_called_once_with("15712459595")

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_claim_script_marks_joined_when_mobile_already_claimed(
        self,
        urlopen_mock,
        _load_config_mock,
    ) -> None:
        response = urlopen_mock.return_value.__enter__.return_value
        response.read.return_value = (
            '{"code":200,"data":{"kind":"already_claimed","successCount":0,"failCount":0,'
            '"items":[],"user":{"id":10956,"uniacid":1,"mobile":"18210234223","nickname":"用户_4749997"}}}'
        ).encode("utf-8")

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "18210234223"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("领取结果：已领取过", output)
        self.assertIn("该手机号已经领取过 Skill用户大礼包", output)
        self.assertIn("小龙虾贴纸（到任意门店对暗号【小龙虾】领取，先到先得）", output)
        self.assertIn("Skill用户专享赠饮券（具体饮品以小程序卡券为准）", output)
        self.assertIn("Skill用户身份标识", output)
        self.assertNotIn("成功失败数量", output)
        self.assertNotIn("您已参与活动啦", output)
        self.assertNotIn("未找到登录用户", output)
        self.mark_activity_joined_mock.assert_called_once_with("18210234223")
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_claim_script_explains_flow_when_no_reward_config(
        self,
        urlopen_mock,
        _load_config_mock,
    ) -> None:
        response = urlopen_mock.return_value.__enter__.return_value
        response.read.return_value = (
            '{"code":200,"data":{"kind":"no_reward_config","successCount":0,"failCount":0,'
            '"items":[],"user":{"id":10956,"mobile":"13730663700","nickname":"用户_7144228"}}}'
        ).encode("utf-8")

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "13730663700"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("领取方式", output)
        self.assertIn("请把您微信小程序【新一咖啡】绑定的手机号发过来，我帮您领取Skill用户大礼包", output)
        self.assertIn("Skill用户大礼包包含", output)
        self.assertIn("活动规则：", output)
        self.assertIn("小龙虾贴纸：到任意门店对暗号【小龙虾】领取，先到先得", output)
        self.assertIn("Skill用户身份标识：参与即可添加SKILL 标签、龙虾头像", output)
        self.assertIn("我会先按您发来的手机号查询领取", output)
        self.assertNotIn("第一步：绑定手机号", output)
        self.assertNotIn("先绑定【新一咖啡】注册手机号，再把手机号发来", output)
        self.assertNotIn("当前没有可领取的活动奖励", output)
        self.assertNotIn("暂无可领取", output)
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch.object(claim_reward, "fetch_json")
    @patch.object(claim_reward, "post_json")
    def test_no_reward_config_does_not_render_sticker_store_or_failed_message(
        self,
        post_json_mock,
        fetch_json_mock,
        _load_config_mock,
    ) -> None:
        post_json_mock.return_value = {
            "code": 200,
            "data": {
                "kind": "no_reward_config",
                "successCount": 0,
                "failCount": 1,
                "items": [{"state": 0, "message": "暂无活动配置"}],
                "user": {"id": 10956, "mobile": "13730663700", "nickname": "用户_7144228"},
            },
        }
        fetch_json_mock.return_value = {
            "data": {
                "goods": [],
                "stores": [
                    {
                        "name": "幂茶幂咖望京店",
                        "address": "北京市朝阳区望京街9号",
                        "storeMobile": "01088888888",
                        "facilities": "休息区",
                    }
                ],
                "weather": None,
                "orders": {"orders": []},
            }
        }
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "13730663700"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("领取方式", output)
        self.assertIn("领取Skill用户大礼包", output)
        self.assertNotIn("贴纸领取门店信息", output)
        self.assertNotIn("失败原因", output)
        self.assertNotIn("暂无活动配置", output)
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(claim_reward, "load_activity_joined", return_value=False)
    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_claim_script_treats_already_claimed_after_unregistered_as_gift_obtained(
        self,
        urlopen_mock,
        _load_config_mock,
        load_activity_joined_mock,
    ) -> None:
        response = urlopen_mock.return_value.__enter__.return_value
        response.read.return_value = (
            '{"code":200,"data":{"kind":"already_claimed","successCount":0,"failCount":0,'
            '"items":[],"user":{"id":10956,"uniacid":1,"mobile":"18539991423","nickname":"用户_991423"}}}'
        ).encode("utf-8")

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "18539991423"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("领取结果：身份验证成功", output)
        self.assertIn("身份验证成功。Skill用户大礼包已发放到账", output)
        self.assertIn("小龙虾贴纸（到任意门店对暗号【小龙虾】领取，先到先得）", output)
        self.assertIn("Skill用户专享赠饮券（具体饮品以小程序卡券为准）", output)
        self.assertIn("Skill用户身份标识", output)
        self.assertNotIn("已经领过", output)
        self.assertNotIn("您已参与活动啦", output)
        load_activity_joined_mock.assert_called_once_with("18539991423")
        self.mark_activity_joined_mock.assert_called_once_with("18539991423")
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_claim_script_does_not_duplicate_coupon_label_when_coupon_name_missing(
        self,
        urlopen_mock,
        _load_config_mock,
    ) -> None:
        first_response = urlopen_mock.return_value.__enter__.return_value
        first_response.read.return_value = (
            '{"code":200,"data":{"kind":"granted","successCount":1,"failCount":0,'
            '"items":[{"state":1,"message":"发放成功","coupon":{}}],'
            '"user":{"mobile":"15712459595","nickname":"双龙"}}}'
        ).encode("utf-8")
        urlopen_mock.side_effect = [
            urlopen_mock.return_value,
            RuntimeError("context api down"),
        ]

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("Skill用户专享赠饮券（具体饮品以小程序卡券为准）", output)
        self.assertNotIn("龙虾专属饮品券龙虾专属饮品券", output)
        self.mark_activity_joined_mock.assert_called_once_with("15712459595")
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_claim_script_reuses_recommendation_copy_when_activity_already_joined(
        self,
        urlopen_mock,
        _load_config_mock,
    ) -> None:
        first_response = urlopen_mock.return_value.__enter__.return_value
        first_response.read.return_value = (
            '{"code":200,"data":{"kind":"already_claimed","successCount":1,"failCount":0,'
            '"items":[{"state":1,"message":"发放成功","coupon":{"name":"苦尽甘来拿铁"}}],'
            '"user":{"mobile":"15712459595","nickname":"双龙"}}}'
        ).encode("utf-8")
        second_response = type("Resp", (), {})()
        second_response.read = lambda: (
            '{"data":{"goods":[{"name":"柚香燕麦拿铁","categories":["咖啡"],"price":"14.80","cupSizes":["大杯"],'
            '"temperatures":["热","少冰"],"sugarLevels":["3分糖"],"calories":"118 kcal","ingredients":["燕麦奶"]}],'
            '"stores":[{"name":"幂茶幂咖望京店","address":"北京市朝阳区望京街9号","businessStatus":1,'
            '"operatingStatus":1,"realtimeState":1,"labels":[{"name":"休息区"}],"makingCupCount":4,'
            '"makingCupMinutes":18,"storeType":1,"supportUnattendedMode":0}],'
            '"weather":{"city":"Beijing","condition":"sunny","temperatureC":27},'
            '"orders":{"orders":[]}}}'
        ).encode("utf-8")
        second_context_manager = type(
            "ContextManager",
            (),
            {
                "__enter__": lambda self: second_response,
                "__exit__": lambda self, exc_type, exc, tb: False,
            },
        )()
        urlopen_mock.side_effect = [
            urlopen_mock.return_value,
            second_context_manager,
        ]

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("该手机号已经领取过 Skill用户大礼包", output)
        self.assertIn("小龙虾贴纸（到任意门店对暗号【小龙虾】领取，先到先得）", output)
        self.assertIn("Skill用户专享赠饮券「苦尽甘来拿铁」", output)
        self.assertIn("Skill用户身份标识", output)
        self.assertIn("到账券：Skill用户专享赠饮券「苦尽甘来拿铁」。", output)
        self.assertNotIn("成功失败数量", output)
        self.assertNotIn("您已参与活动啦", output)
        self.assertNotIn("您可以到我们的店领取奖励", output)
        self.assertNotIn("门店信息我给您列全", output)
        self.assertNotIn("幂茶幂咖望京店", output)
        self.assertIn("今天天气有点热，建议您喝柚香燕麦拿铁", output)
        self.mark_activity_joined_mock.assert_called_once_with("15712459595")
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_claim_script_falls_back_to_generic_copy_when_weather_api_fails(
        self,
        urlopen_mock,
        _load_config_mock,
    ) -> None:
        first_response = urlopen_mock.return_value.__enter__.return_value
        first_response.read.return_value = (
            '{"code":200,"data":{"kind":"already_claimed","successCount":1,"failCount":0,'
            '"items":[{"state":1,"message":"发放成功","coupon":{"name":"苦尽甘来拿铁"}}],'
            '"user":{"mobile":"15712459595","nickname":"双龙"}}}'
        ).encode("utf-8")
        second_response = type("Resp", (), {})()
        second_response.read = lambda: (
            '{"data":{"goods":[{"name":"苦尽甘来拿铁","categories":["咖啡"],"price":"16.80","cupSizes":["大杯"],'
            '"temperatures":["热","少冰"],"sugarLevels":["3分糖"],"calories":"120 kcal","ingredients":["牛奶"]}],'
            '"stores":[{"name":"幂茶幂咖望京店","address":"北京市朝阳区望京街9号","businessStatus":1,'
            '"operatingStatus":1,"realtimeState":1,"labels":[{"name":"休息区"}],"makingCupCount":4,'
            '"makingCupMinutes":18,"storeType":1,"supportUnattendedMode":0}],'
            '"weather":null,'
            '"orders":{"orders":[]}}}'
        ).encode("utf-8")
        second_context_manager = type(
            "ContextManager",
            (),
            {
                "__enter__": lambda self: second_response,
                "__exit__": lambda self, exc_type, exc, tb: False,
            },
        )()
        urlopen_mock.side_effect = [urlopen_mock.return_value, second_context_manager]

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("今天建议您喝苦尽甘来拿铁", output)
        self.assertNotIn("今天天气", output)
        self.assertIn("该手机号已经领取过 Skill用户大礼包", output)
        self.mark_activity_joined_mock.assert_called_once_with("15712459595")
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_claim_script_keeps_success_message_when_context_fetch_fails(
        self,
        urlopen_mock,
        _load_config_mock,
    ) -> None:
        first_response = urlopen_mock.return_value.__enter__.return_value
        first_response.read.return_value = (
            '{"code":200,"data":{"kind":"granted","successCount":1,"failCount":0,'
            '"items":[{"state":1,"message":"发放成功","coupon":{"name":"苦尽甘来拿铁"}}],'
            '"user":{"mobile":"15712459595","nickname":"双龙"}}}'
        ).encode("utf-8")

        urlopen_mock.side_effect = [
            urlopen_mock.return_value,
            RuntimeError("context api down"),
        ]

        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "15712459595"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("领取结果：身份验证成功", output)
        self.assertIn("身份验证成功。Skill用户大礼包已发放到账", output)
        self.assertIn("Skill用户专享赠饮券「苦尽甘来拿铁」", output)
        self.assertIn("到账券：Skill用户专享赠饮券「苦尽甘来拿铁」。", output)
        self.assertNotIn("成功失败数量", output)
        self.assertNotIn("推荐您就近前往", output)
        self.assertNotIn("建议您喝", output)
        self.mark_activity_joined_mock.assert_called_once_with("15712459595")
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(
        claim_reward,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_claim_script_outputs_debug_logs_to_stderr(
        self,
        urlopen_mock,
        _load_config_mock,
    ) -> None:
        response = urlopen_mock.return_value.__enter__.return_value
        response.read.return_value = (
            '{"code":200,"data":{"kind":"unregistered","successCount":0,"failCount":0,'
            '"items":[],"user":null}}'
        ).encode("utf-8")

        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--mobile", "15712459595", "--debug"],
        ), patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            exit_code = claim_reward.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("DEBUG claim_reward: posting claim request to http://127.0.0.1:8020/skill/xinyi/claim", stderr.getvalue())
        self.assertIn("DEBUG claim_reward: user not found; marking activity as not joined", stderr.getvalue())
        self.assertIn("领取结果：请先登录小程序", stdout.getvalue())
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_called_once_with("15712459595")

    @patch.object(claim_reward, "post_json")
    def test_claim_script_outputs_actionable_prompt_when_mobile_missing(
        self,
        post_json_mock,
    ) -> None:
        stdout = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py"],
        ), patch("sys.stdout", stdout):
            exit_code = claim_reward.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("未提供手机号，无法领取或同步活动状态。", output)
        self.assertIn("请用户发送微信小程序【新一咖啡】绑定手机号", output)
        post_json_mock.assert_not_called()
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch("urllib.request.urlopen")
    def test_claim_script_can_reuse_saved_mobile_for_status_query(
        self,
        urlopen_mock,
    ) -> None:
        self.load_mobile_mock.return_value = "15712459595"

        def load_activity_joined(mobile: str | None) -> bool | None:
            return True if mobile == "15712459595" else None

        self.load_activity_joined_mock.side_effect = load_activity_joined
        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--use-saved-mobile", "--debug"],
        ), patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            exit_code = claim_reward.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("DEBUG claim_reward: resolved mobile from local state", stderr.getvalue())
        self.assertIn("DEBUG claim_reward: resolved mobile already claimed in local state; skipping backend", stderr.getvalue())
        self.assertIn("领取结果：已领取过", stdout.getvalue())
        self.assertIn("该手机号已经领取过 Skill用户大礼包", stdout.getvalue())
        urlopen_mock.assert_not_called()
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_not_called()

    @patch.object(claim_reward, "post_json")
    def test_claim_script_use_saved_mobile_with_no_cache_emits_prompt(
        self,
        post_json_mock,
    ) -> None:
        self.load_mobile_mock.return_value = None
        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["claim_reward.py", "--use-saved-mobile", "--debug"],
        ), patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            exit_code = claim_reward.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("DEBUG claim_reward: saved mobile requested but not found", stderr.getvalue())
        self.assertIn("未提供手机号，无法领取或同步活动状态。", stdout.getvalue())
        post_json_mock.assert_not_called()
        self.mark_activity_joined_mock.assert_not_called()
        self.mark_activity_not_joined_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
