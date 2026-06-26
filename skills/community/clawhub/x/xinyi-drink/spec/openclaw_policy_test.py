from __future__ import annotations

import json
import unittest
from pathlib import Path


class OpenClawPolicyTest(unittest.TestCase):
    MAIN_USE_CASES = [
        "领取Skill用户大礼包",
        "查询及分析个人历史订单",
        "查询菜单及饮品热量",
        "查询门店及等候时长",
    ]

    def test_skill_md_frontmatter_declares_openclaw_metadata(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")

        frontmatter = skill_md.split("---", 2)[1]
        self.assertIn("name: xinyi-drink", frontmatter)
        self.assertIn("description: >-", frontmatter)
        for use_case in self.MAIN_USE_CASES:
            self.assertIn(use_case, frontmatter)
        for keyword in ("新一好喝", "新一咖啡", "Skill用户大礼包", "今天喝什么", "订单", "购买记录"):
            self.assertIn(f"  - {keyword}", frontmatter)
        self.assertIn("metadata:", frontmatter)
        self.assertIn("packageType: executable-skill", frontmatter)
        self.assertIn("instructionOnly: false", frontmatter)
        self.assertIn("sourceDirectory: skill", frontmatter)
        self.assertIn("installSpec:", frontmatter)
        self.assertIn("script: install.sh", frontmatter)
        self.assertIn("openclaw:", frontmatter)
        self.assertIn("packageType: executable-skill", frontmatter)
        self.assertIn("instructionOnly: false", frontmatter)
        self.assertIn("dataClassification: optional-phone-number", frontmatter)
        self.assertIn('privacyReviewed: "2026-04-28"', frontmatter)
        self.assertIn("homepage: https://github.com/xinyi-drink/xinyi-drink", frontmatter)
        self.assertIn("runtime:", frontmatter)
        self.assertIn("requiresNetwork: true", frontmatter)
        self.assertIn("installSpec:", frontmatter)
        self.assertIn("sourceDirectory: skill", frontmatter)
        self.assertIn("network:", frontmatter)
        self.assertIn("defaultApiBaseUrl: https://ai.xinyicoffee.com/api", frontmatter)
        self.assertIn("localStorage:", frontmatter)
        self.assertIn("defaultPath: ~/.xinyi-drink/state.json", frontmatter)
        self.assertIn("contents: [mobile, activityJoined, updatedAt]", frontmatter)
        self.assertIn("permissions: \"0600 when supported\"", frontmatter)
        self.assertIn("clearCommand: python3 scripts/recommend_drink.py --clear-mobile", frontmatter)
        self.assertIn("sharedMachineWarning: true", frontmatter)
        self.assertIn("version: 1.2.5", frontmatter)

    def test_skill_md_contains_compact_operating_guidance(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        body = skill_md.split("---", 2)[2]

        self.assertLessEqual(len(body.splitlines()), 145)
        for heading in ("## AI 必读", "## 隐私与手机号使用", "## 触发表", "## 主流程", "## 盲区应对", "## 内嵌示例"):
            self.assertIn(heading, skill_md)
        self.assertIn("懂茶饮也懂咖啡的店员姐姐", skill_md)
        self.assertIn("今天这个温度喝它刚好", skill_md)
        self.assertIn("帮我领取新一Skill福利", skill_md)
        self.assertIn("望京店目前有多少杯待做，等待时间多久", skill_md)
        self.assertIn("某某饮品热量多少", skill_md)
        self.assertIn("个人订单、下单、购买、消费、喝过、买过、点过、取餐、制作中或历史记录", skill_md)
        for use_case in self.MAIN_USE_CASES:
            self.assertIn(use_case, skill_md)
        self.assertIn("不要求用户说出“订单”两个字", skill_md)
        self.assertIn("订单信息只能基于本次查询结果，不能预估、估算或模糊处理", skill_md)
        self.assertIn("订单等级提示语由脚本按本次查询到的杯数计算", skill_md)
        self.assertIn("不输出 `Level 1/2/3/4/5` 标签", skill_md)
        self.assertIn("本地已领取状态优先", skill_md)
        self.assertIn("手机号会保存到本机 `~/.xinyi-drink/state.json`", skill_md)
        self.assertIn("同一机器或同一 Agent profile 的后续合规请求可能复用或展示该手机号", skill_md)
        self.assertIn("`claim_reward.py` 是状态变更工具", skill_md)
        self.assertIn("服务端必须负责小程序绑定手机号的账号归属和订单访问控制", skill_md)
        self.assertIn("活动状态查询、订单查询、活动总览、口味偏好分析或明确个性化推荐可以复用本机缓存手机号", skill_md)
        self.assertIn("python3 scripts/recommend_drink.py --show-mobile-status", skill_md)
        self.assertIn("不要请求后端，也不要凭 Agent 记忆回答", skill_md)
        self.assertIn("普通推荐、门店和菜单查询不要复用缓存手机号", skill_md)
        self.assertIn("手机号会发送到配置的后端", skill_md)
        self.assertIn("只使用用户自己的手机号", skill_md)
        self.assertIn("python3 scripts/recommend_drink.py --clear-mobile", skill_md)
        self.assertIn("不要输出发放统计明细等技术化表述", skill_md)
        self.assertIn("实时接口失败", skill_md)
        self.assertNotIn("如果你在附近", skill_md)

    def test_static_scan_guidance_declares_boundaries_without_behavior_changes(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        repo_root = skill_root.parents[0]
        skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        privacy = (skill_root / "references" / "privacy-boundaries.md").read_text(encoding="utf-8")
        readme = (repo_root / "README.md").read_text(encoding="utf-8")
        payload = json.loads((skill_root / "skill.json").read_text(encoding="utf-8"))

        self.assertIn("领取礼包和查询订单只接受用户本人的【新一咖啡】绑定手机号", skill_md)
        self.assertIn("用户明确表示代查或使用他人手机号时，不调用领取或订单脚本", skill_md)
        self.assertIn("`install.sh --dry-run`", skill_md)
        self.assertIn("`install.sh --check-installed`", skill_md)

        self.assertTrue(payload["privacy"]["backend_trust_required"])
        self.assertIn("server-side-account-ownership-check-required", payload["privacy"]["user_guidance"])
        self.assertEqual(
            payload["privacy"]["third_party_phone_policy"],
            "reject-claim-and-order-query",
        )
        self.assertEqual(payload["install"]["check_installed"], "install.sh --check-installed")
        self.assertEqual(payload["install_spec"]["install"]["check_installed"], "install.sh --check-installed")
        self.assertEqual(payload["openclaw"]["installSpec"]["checkInstalled"], "install.sh --check-installed")

        annotations = {tool["name"]: tool["annotations"] for tool in payload["tools"]}
        for tool_name in ("claim_reward", "query_orders"):
            self.assertTrue(annotations[tool_name]["requiresUserOwnedPhone"])
            self.assertTrue(annotations[tool_name]["rejectThirdPartyPhone"])
            self.assertEqual(annotations[tool_name]["trustBoundary"], "xinyi-backend")

        self.assertIn("用户明确表示代查或使用他人手机号时，不调用领取或订单脚本", privacy)
        self.assertIn("不要把 `XINYI_API_BASE_URL` 指向不信任后端", privacy)
        self.assertIn("安装前可先运行 `bash skill/install.sh --dry-run --platform openclaw`", readme)
        self.assertIn("已安装后可运行 `bash skill/install.sh --platform codex --check-installed`", readme)

    def test_mobile_switch_intents_are_forced_through_claim_reward(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        intent_routing = (skill_root / "references" / "intent-routing.md").read_text(encoding="utf-8")
        activity_flow = (skill_root / "references" / "activity-flow.md").read_text(encoding="utf-8")
        payload = json.loads((skill_root / "skill.json").read_text(encoding="utf-8"))

        claim_description = next(
            tool["description"]
            for tool in payload["tools"]
            if tool["name"] == "claim_reward"
        )
        system_instruction = payload["brand_prompt"]["system_instruction"]

        switch_preflight_phrase = "手机号变更、换号、改号、重新绑定或重新输入手机号"
        self.assertIn(switch_preflight_phrase, skill_md)
        self.assertIn("先调用 `scripts/recommend_drink.py --show-mobile-status --candidate-mobile <手机号>`", skill_md)
        self.assertIn("只有用户明确确认继续领取或同步后，才调用 `scripts/claim_reward.py --mobile <手机号>`", skill_md)
        self.assertIn("状态查询和换号预检不能直接调用 `claim_reward.py`", skill_md)

        for phrase in ("换手机号", "改手机号", "重新绑定", "重新输入手机号", "另一个手机号"):
            self.assertIn(phrase, intent_routing)
        self.assertIn("先调用 `recommend_drink.py --show-mobile-status --candidate-mobile <手机号>`", intent_routing)
        self.assertIn("状态查询和换号预检不能直接调用 `claim_reward.py`", intent_routing)
        self.assertIn("先走 `recommend_drink.py --show-mobile-status --candidate-mobile <手机号>`", activity_flow)

        for phrase in ("这个手机号领过了吗", "换手机号", "改手机号", "重新绑定", "重新输入手机号"):
            self.assertNotIn(phrase, claim_description)
        self.assertIn("确认继续领取", claim_description)
        self.assertIn("状态查询和换号预检必须先走 showMobileStatus", system_instruction)

    def test_activity_mobile_status_queries_are_forced_through_local_state(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        intent_routing = (skill_root / "references" / "intent-routing.md").read_text(encoding="utf-8")
        payload = json.loads((skill_root / "skill.json").read_text(encoding="utf-8"))

        recommend_description = next(
            tool["description"]
            for tool in payload["tools"]
            if tool["name"] == "recommend_drink"
        )
        system_instruction = payload["brand_prompt"]["system_instruction"]

        semantic_rule = "参与活动所用手机号、已保存手机号、历史参与手机号、领取礼包手机号、绑定活动手机号或当前活动手机号"
        for content in (skill_md, intent_routing, recommend_description, system_instruction):
            self.assertIn(semantic_rule, content)
            self.assertIn("不限于示例原文", content)

        for phrase in ("新一咖啡参与活动手机号是什么", "之前参与活动的手机号", "我上次领礼包用的手机号"):
            self.assertIn(phrase, skill_md)
            self.assertIn(phrase, intent_routing)
        self.assertIn("必须调用 `scripts/recommend_drink.py --show-mobile-status`", skill_md)
        self.assertIn("不要查 Agent 记忆、历史记忆或对话记忆", skill_md)
        self.assertIn("不要回答成固定的活动手机号", skill_md)
        self.assertIn("必须走本地状态文件", system_instruction)

    def test_skill_json_declares_scripts_network_and_privacy(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        payload = json.loads((skill_root / "skill.json").read_text(encoding="utf-8"))
        skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")

        self.assertEqual(payload["name"], "xinyi-drink")
        self.assertEqual(payload["post_install_prompts"], self.MAIN_USE_CASES)
        for use_case in self.MAIN_USE_CASES:
            self.assertIn(use_case, payload["description"])
        self.assertIn('"version": "1.2.5"', json.dumps(payload, ensure_ascii=False))
        self.assertIn(f"version: {payload['version']}", skill_md)
        self.assertEqual(payload["homepage"], "https://github.com/xinyi-drink/xinyi-drink")
        self.assertEqual(payload["repository"], "https://github.com/xinyi-drink/xinyi-drink")
        self.assertEqual(payload["source"]["type"], "git")
        self.assertEqual(payload["source"]["url"], "https://github.com/xinyi-drink/xinyi-drink")
        self.assertEqual(payload["source"]["directory"], "skill")
        self.assertEqual(payload["install"]["type"], "local-script")
        self.assertEqual(payload["install"]["script"], "install.sh")
        self.assertEqual(payload["install"]["dry_run"], "install.sh --dry-run")
        self.assertIn("~/.openclaw/skills/xinyi-drink", payload["install"]["writes_to"])
        self.assertEqual(payload["packageType"], "executable-skill")
        self.assertFalse(payload["instructionOnly"])
        self.assertEqual(payload["sourceDirectory"], "skill")
        self.assertEqual(payload["installSpec"]["packageType"], "executable-skill")
        self.assertFalse(payload["installSpec"]["instructionOnly"])
        self.assertEqual(payload["installSpec"]["sourceDirectory"], "skill")
        self.assertEqual(payload["installSpec"]["script"], "install.sh")
        self.assertEqual(payload["installSpec"]["dryRun"], "install.sh --dry-run")
        self.assertEqual(payload["installSpec"]["checkInstalled"], "install.sh --check-installed")
        self.assertEqual(payload["install_spec"]["package_type"], "executable-skill")
        self.assertFalse(payload["install_spec"]["instruction_only"])
        self.assertEqual(payload["install_spec"]["source_directory"], "skill")
        self.assertEqual(payload["install_spec"]["install"]["script"], "install.sh")
        self.assertEqual(payload["openclaw"]["installSpec"]["script"], "install.sh")
        self.assertEqual(payload["runtime"]["type"], "python-scripts")
        self.assertTrue(payload["runtime"]["requires_network"])
        self.assertIn("scripts/claim_reward.py", payload["runtime"]["entrypoints"])
        self.assertIn("scripts/fetch_stores.py", payload["runtime"]["entrypoints"])
        self.assertIn("scripts/query_orders.py", payload["runtime"]["entrypoints"])
        self.assertIn("scripts/recommend_drink.py", payload["runtime"]["entrypoints"])

        endpoint_paths = {
            endpoint["path"]
            for endpoint in payload["network"]["endpoints"]
        }
        self.assertEqual(
            endpoint_paths,
            {
                "/skill/xinyi/claim",
                "/skill/xinyi/context",
                "/skill/xinyi/orders",
                "/skill/xinyi/stores",
            },
        )
        claim_endpoint = next(
            endpoint
            for endpoint in payload["network"]["endpoints"]
            if endpoint["path"] == "/skill/xinyi/claim"
        )
        self.assertIn("mobile", claim_endpoint["sends"])
        self.assertEqual(payload["localStorage"]["defaultPath"], "~/.xinyi-drink/state.json")
        self.assertEqual(payload["localStorage"]["clearCommand"], "python3 scripts/recommend_drink.py --clear-mobile")
        self.assertTrue(payload["localStorage"]["sharedMachineWarning"])
        self.assertEqual(payload["openclaw"]["packageType"], "executable-skill")
        self.assertFalse(payload["openclaw"]["instructionOnly"])
        self.assertEqual(payload["privacy"]["data_subject"], "user-provided-or-saved-mobile-owner")
        self.assertIn("only-use-your-own-phone-number", payload["privacy"]["user_guidance"])
        self.assertIn("clear-cache-on-shared-machines", payload["privacy"]["user_guidance"])

        keywords = set(payload["keywords"])
        for keyword in ("今天喝什么", "困了", "下午茶", "上班犯困", "提神", "门店", "订单", "清爽", "热量", "果茶", "等待时长", "饮品偏好"):
            self.assertIn(keyword, keywords)

        tool_descriptions = {
            tool["name"]: tool["description"]
            for tool in payload["tools"]
        }
        tool_annotations = {
            tool["name"]: tool["annotations"]
            for tool in payload["tools"]
        }
        tool_display_names = {
            tool["name"]: tool["display_name"]
            for tool in payload["tools"]
        }
        self.assertEqual(tool_display_names["fetch_stores"], "查询门店及等候时长")
        self.assertIn("用户问“帮我领取新一Skill福利”", tool_descriptions["claim_reward"])
        self.assertIn("用户问“新一咖啡有哪些门店”", tool_descriptions["fetch_stores"])
        self.assertIn("望京店目前有多少杯待做", tool_descriptions["fetch_stores"])
        self.assertIn("默认不读取本地缓存手机号", tool_descriptions["recommend_drink"])
        self.assertIn("useSavedMobile", tool_descriptions["recommend_drink"])
        self.assertIn("showMobileStatus", tool_descriptions["recommend_drink"])
        self.assertIn("某某饮品热量多少", tool_descriptions["recommend_drink"])
        self.assertIn("有哪些不太甜的果茶", tool_descriptions["recommend_drink"])
        self.assertIn("我买过多少杯", tool_descriptions["query_orders"])
        self.assertIn("我都定了哪些饮料", tool_descriptions["query_orders"])
        self.assertIn("我喝了多少咖啡", tool_descriptions["query_orders"])
        self.assertIn("全部订单", tool_descriptions["query_orders"])
        self.assertIn("历史订单", tool_descriptions["query_orders"])
        self.assertIn("正在进行中订单", tool_descriptions["query_orders"])
        self.assertIn("不要求出现“订单”", tool_descriptions["query_orders"])
        self.assertIn("帮我分析我的口味偏好", tool_descriptions["query_orders"])
        self.assertIn("咖啡/饮品统计只是基于订单数据的回答方式", tool_descriptions["query_orders"])
        self.assertIn("不能预估、估算或模糊处理", tool_descriptions["query_orders"])
        self.assertIn("订单等级提示语由脚本按本次查询到的杯数计算", tool_descriptions["query_orders"])
        self.assertIn("不输出 Level 标签", tool_descriptions["query_orders"])
        self.assertIn("不要输出发放统计明细等技术化表述", tool_descriptions["claim_reward"])
        self.assertTrue(tool_annotations["claim_reward"]["requiresExplicitUserIntent"])
        self.assertTrue(tool_annotations["claim_reward"]["stateChanging"])
        self.assertEqual(tool_annotations["claim_reward"]["personalData"], ["mobile"])
        self.assertTrue(tool_annotations["query_orders"]["requiresExplicitUserIntent"])
        self.assertTrue(tool_annotations["query_orders"]["requiresUserOwnedPhone"])
        self.assertEqual(tool_annotations["query_orders"]["personalData"], ["mobile", "order_history"])
        claim_reward_schema = next(
            tool["inputSchema"]
            for tool in payload["tools"]
            if tool["name"] == "claim_reward"
        )
        self.assertEqual(claim_reward_schema["required"], [])
        self.assertIn("useSavedMobile", claim_reward_schema["properties"])
        self.assertIn("明确确认继续领取", claim_reward_schema["properties"]["useSavedMobile"]["description"])
        query_orders_schema = next(
            tool["inputSchema"]
            for tool in payload["tools"]
            if tool["name"] == "query_orders"
        )
        self.assertIn("不传查询全部订单", query_orders_schema["properties"]["status"]["description"])
        recommend_schema = next(
            tool["inputSchema"]
            for tool in payload["tools"]
            if tool["name"] == "recommend_drink"
        )
        self.assertIn("useSavedMobile", recommend_schema["properties"])
        self.assertIn("showMobileStatus", recommend_schema["properties"])
        self.assertIn("candidateMobile", recommend_schema["properties"])
        self.assertIn("默认不读取缓存手机号", payload["localStorage"]["autoReadPolicy"])

    def test_recommend_drink_does_not_claim_or_read_saved_mobile_by_default(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        script = (skill_root / "scripts" / "recommend_drink.py").read_text(encoding="utf-8")

        self.assertIn("--use-saved-mobile", script)
        self.assertIn("resolved_mobile = args.mobile", script)
        self.assertIn("if not resolved_mobile and args.use_saved_mobile:", script)
        self.assertNotIn("post_json", script)
        self.assertNotIn("/skill/xinyi/claim", script)

    def test_readme_documents_default_backend_and_phone_data_flow(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        readme = (repo_root / "README.md").read_text(encoding="utf-8")

        self.assertIn("Skill用户大礼包", readme)
        self.assertIn("skill/SKILL.md", readme)
        self.assertIn("frontmatter 同时保留 Agent 触发用的 `name/description` 和 OpenClaw/ClawHub 审查用的 `keywords/metadata/version`", readme)
        self.assertIn("skill/skill.json", readme)
        self.assertNotIn("发布前两处版本号需要保持一致", readme)
        self.assertIn("默认后端", readme)
        self.assertIn("https://ai.xinyicoffee.com/api", readme)
        self.assertIn("POST /skill/xinyi/claim", readme)
        self.assertIn("GET /skill/xinyi/context", readme)
        self.assertIn("GET /skill/xinyi/orders", readme)
        self.assertIn("手机号会作为请求数据发送到后端", readme)
        self.assertIn("普通推荐、门店和菜单查询不会自动复用缓存手机号", readme)
        self.assertIn("订单摘要和口味偏好分析走专用订单接口", readme)
        self.assertIn("不是 instruction-only", readme)
        self.assertIn("Registry install spec", readme)
        self.assertIn("只使用本人手机号", readme)
        self.assertIn("共享机器或共享 Agent profile", readme)

    def test_privacy_reference_addresses_static_scan_concerns(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        privacy = (skill_root / "references" / "privacy-boundaries.md").read_text(encoding="utf-8")

        self.assertIn("只使用本人手机号", privacy)
        self.assertIn("共享机器或共享 Agent profile", privacy)
        self.assertIn("订单查询必须由用户明确询问个人订单、购买记录、饮品历史、取餐或口味偏好分析触发", privacy)
        self.assertIn("本 Skill 客户端不采集密码、短信验证码、OAuth token 或 Cookie", privacy)
        self.assertIn("服务端仍应负责账号归属和订单访问控制", privacy)

    def test_user_facing_capability_examples_are_specific(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        readme = (repo_root / "README.md").read_text(encoding="utf-8")
        intro_section = readme.split("## Skill用户大礼包", 1)[0]

        self.assertIn("固定推荐问题", intro_section)
        self.assertNotIn("数据来源", intro_section)
        self.assertNotIn("/skill/xinyi/", intro_section)
        for example in self.MAIN_USE_CASES:
            self.assertIn(example, intro_section)
        self.assertNotIn("给我推荐一杯适合当下午茶的饮品", intro_section)


if __name__ == "__main__":
    unittest.main()
