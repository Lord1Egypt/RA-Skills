#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sanjianke-chatbox 脚本自测：全部离线，用假数据构造，不联网、不需要 Key。

运行：python -X utf8 scripts/selftest.py -v
"""
import base64
import json
import os
import sys
import unittest
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_import_config as g  # noqa: E402


def fake_model(code, name=None, vision=0, reasoning=0, type_code="text",
               call_type=1, max_tokens=8192):
    return {"model_code": code, "model_name": name or code, "supports_vision": vision,
            "supports_reasoning": reasoning, "type_code": type_code,
            "call_type": call_type, "max_tokens": max_tokens}


class TestToModelInfo(unittest.TestCase):
    def test_basic_mapping(self):
        info = g.to_model_info(fake_model("DeepSeek-V4-Flash"))
        self.assertEqual(info["modelId"], "DeepSeek-V4-Flash")
        self.assertEqual(info["type"], "chat")
        self.assertEqual(info["nickname"], "DeepSeek-V4-Flash")
        self.assertNotIn("capabilities", info)

    def test_vision_capability(self):
        info = g.to_model_info(fake_model("Qwen3.6-Plus", vision=1))
        self.assertEqual(info["capabilities"], ["vision"])

    def test_reasoning_capability(self):
        info = g.to_model_info(fake_model("ERNIE-5.0-Thinking", reasoning=1))
        self.assertEqual(info["capabilities"], ["reasoning"])

    def test_both_capabilities(self):
        info = g.to_model_info(fake_model("X", vision=1, reasoning=1))
        self.assertEqual(info["capabilities"], ["vision", "reasoning"])

    def test_note_appended_to_nickname(self):
        info = g.to_model_info(fake_model("A", name="模型A"), note="日常对话")
        self.assertEqual(info["nickname"], "模型A ｜ 日常对话")

    def test_max_output_skipped_when_trivial(self):
        self.assertNotIn("maxOutput", g.to_model_info(fake_model("A", max_tokens=1)))
        self.assertEqual(g.to_model_info(fake_model("A", max_tokens=4096))["maxOutput"], 4096)

    def test_falls_back_to_id_field(self):
        self.assertEqual(g.to_model_info({"id": "legacy-id"})["modelId"], "legacy-id")


class TestPickModels(unittest.TestCase):
    def test_curated_hits_in_order(self):
        api = [fake_model("DeepSeek-V4-Flash"), fake_model("GLM-5.2")]
        models, missing = g.pick_models(api)
        self.assertEqual([m["modelId"] for m in models], ["DeepSeek-V4-Flash", "GLM-5.2"])
        self.assertIn("DeepSeek-V4-Pro", missing)   # 库里没有 → 记入 missing

    def test_fallback_when_curated_all_miss(self):
        api = [fake_model("Some-Unknown-Model")]
        models, _ = g.pick_models(api)
        self.assertEqual([m["modelId"] for m in models], ["Some-Unknown-Model"])

    def test_use_all_filters_async_and_non_text(self):
        api = [
            fake_model("t-sync", type_code="text", call_type=1),
            fake_model("t-async", type_code="text", call_type=2),
            fake_model("img", type_code="image", call_type=1),
        ]
        models, _ = g.pick_models(api, use_all=True)
        self.assertEqual([m["modelId"] for m in models], ["t-sync"])

    def test_limit_respected(self):
        api = [fake_model("DeepSeek-V4-Flash"), fake_model("DeepSeek-V4-Pro"),
               fake_model("Qwen3.6-Plus")]
        models, _ = g.pick_models(api, limit=2)
        self.assertEqual(len(models), 2)


class TestBuildConfig(unittest.TestCase):
    def test_structure_and_apihost(self):
        cfg = g.build_provider_config([{"modelId": "m", "type": "chat"}])
        self.assertEqual(cfg["type"], "openai")
        self.assertEqual(cfg["settings"]["apiHost"], "https://api.a7w.cn/api")
        self.assertEqual(cfg["settings"]["apiPath"], "/v1/chat/completions")
        self.assertEqual(len(cfg["settings"]["models"]), 1)
        self.assertIn("website", cfg["urls"])

    def test_api_host_never_ends_with_api_v1(self):
        """回归：apiHost 若带 /api/v1 会被 Chatbox 再拼一次 → 404。"""
        cfg = g.build_provider_config([])
        self.assertFalse(cfg["settings"]["apiHost"].rstrip("/").endswith("/api/v1"))

    def test_api_key_omitted_by_default(self):
        self.assertNotIn("apiKey", g.build_provider_config([])["settings"])

    def test_build_config_has_no_api_key_param(self):
        """回归（安全）：build_provider_config 不再接受 api_key，
        生成的配置里永远没有凭证。"""
        import inspect
        self.assertNotIn("api_key", inspect.signature(g.build_provider_config).parameters)
        self.assertNotIn("apiKey", g.build_provider_config([])["settings"])

    def test_deep_link_refuses_api_key(self):
        """回归（安全）：配置里若混进 Key，to_deep_link 必须拒绝生成。
        深链会被转发、留在浏览器历史，携带可复用凭证会造成泄露。"""
        cfg = g.build_provider_config([{"modelId": "m", "type": "chat"}])
        cfg["settings"]["apiKey"] = "DUMMY_KEY_SHOULD_NEVER_SHIP"
        with self.assertRaises(ValueError):
            g.to_deep_link(cfg)
        cfg["settings"].pop("apiKey")
        cfg["settings"]["api_key"] = "DUMMY_KEY_ALSO_REFUSED"
        with self.assertRaises(ValueError):
            g.to_deep_link(cfg)


class TestDeepLink(unittest.TestCase):
    def test_prefix_and_base64_roundtrip(self):
        cfg = g.build_provider_config([{"modelId": "m", "type": "chat"}])
        link = g.to_deep_link(cfg)
        self.assertTrue(link.startswith("chatbox://provider/import?config="))
        q = parse_qs(urlparse(link).query)
        decoded = json.loads(base64.b64decode(q["config"][0]).decode("utf-8"))
        self.assertEqual(decoded, cfg)

    def test_chinese_survives_roundtrip(self):
        cfg = g.build_provider_config([], api_host="https://api.a7w.cn/api")
        cfg["name"] = "算力集市 a7w"
        link = g.to_deep_link(cfg)
        q = parse_qs(urlparse(link).query)
        decoded = json.loads(base64.b64decode(q["config"][0]).decode("utf-8"))
        self.assertEqual(decoded["name"], "算力集市 a7w")


class TestVerifyScriptShape(unittest.TestCase):
    """只检查 verify 脚本的可导入性与纯逻辑，不发网络请求。"""

    def test_importable_and_defaults(self):
        import verify_a7w as v
        self.assertEqual(v.DEFAULT_APIHOST, "https://api.a7w.cn/api")
        self.assertTrue(v.DEFAULT_MODEL)

    def test_sources_contain_no_key_literal(self):
        """源码里不应出现形如 <prefix>-xxxx 的密钥字面量。

        注意：**本测试自身也不能出现该前缀的字面量**——静态扫描器会把
        它当成「硬编码 API Key」并标记为可疑。所以这里用拼接构造前缀。
        """
        prefix = "s" + "k" + "-"
        d = os.path.dirname(os.path.abspath(__file__))
        for fn in ("verify_a7w.py", "gen_import_config.py"):
            with open(os.path.join(d, fn), "r", encoding="utf-8") as f:
                txt = f.read()
            self.assertNotIn(prefix, txt, "%s 不应出现密钥字面量" % fn)
