"""llm.py 单元测试 — 不调真实 API，只测纯函数 + 客户端构造。"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from content_engine.llm import (
    OfoxLLMClient,
    OfoxError,
    ofox_credentials_present,
    _load_ofox_key,
    _xdg_config_dir,
)


class TestKeyLoading(unittest.TestCase):

    def setUp(self):
        # 备份环境
        self._saved = {
            k: os.environ.pop(k, None)
            for k in ("OFOX_API_KEY", "OPENROUTER_API_KEY")
        }

    def tearDown(self):
        for k, v in self._saved.items():
            if v is not None:
                os.environ[k] = v

    def test_loads_from_env(self):
        os.environ["OFOX_API_KEY"] = "ofox-test"
        self.assertEqual(_load_ofox_key(), "ofox-test")

    def test_falls_back_to_openrouter(self):
        os.environ["OPENROUTER_API_KEY"] = "or-test"
        self.assertEqual(_load_ofox_key(), "or-test")

    def test_ofox_takes_priority(self):
        os.environ["OFOX_API_KEY"] = "ofox-priority"
        os.environ["OPENROUTER_API_KEY"] = "or-fallback"
        self.assertEqual(_load_ofox_key(), "ofox-priority")

    def test_strips_whitespace(self):
        os.environ["OFOX_API_KEY"] = "  ofox-padded  "
        self.assertEqual(_load_ofox_key(), "ofox-padded")

    def test_returns_none_when_missing(self):
        with patch("content_engine.llm._TOKEN_SEARCH_PATHS", []):
            self.assertIsNone(_load_ofox_key())

    def test_credentials_present_when_set(self):
        os.environ["OFOX_API_KEY"] = "ofox-anything"
        self.assertTrue(ofox_credentials_present())

    def test_credentials_absent_when_missing(self):
        with patch("content_engine.llm._TOKEN_SEARCH_PATHS", []):
            self.assertFalse(ofox_credentials_present())


class TestClientInit(unittest.TestCase):

    def test_raises_when_no_key(self):
        with patch("content_engine.llm._load_ofox_key", return_value=None):
            with self.assertRaises(OfoxError) as ctx:
                OfoxLLMClient()
            self.assertIn("OFOX_API_KEY", str(ctx.exception))

    def test_constructs_with_explicit_key(self):
        client = OfoxLLMClient(api_key="explicit-key", model="my-model")
        self.assertEqual(client.api_key, "explicit-key")
        self.assertEqual(client.model, "my-model")
        self.assertTrue(client.base_url.startswith("https://"))

    def test_base_url_strips_trailing_slash(self):
        client = OfoxLLMClient(api_key="k", base_url="https://foo.com/")
        self.assertEqual(client.base_url, "https://foo.com")

    def test_default_endpoint(self):
        client = OfoxLLMClient(api_key="k")
        self.assertIn("ofox.ai", client.base_url)


class TestXDGConfig(unittest.TestCase):

    def test_xdg_default(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("XDG_CONFIG_HOME", None)
            d = _xdg_config_dir()
            self.assertIn(".config", str(d))
            self.assertTrue(str(d).endswith("content-engine"))

    def test_xdg_override(self):
        with patch.dict(os.environ, {"XDG_CONFIG_HOME": "/tmp/myxdg"}):
            d = _xdg_config_dir()
            self.assertEqual(str(d), "/tmp/myxdg/content-engine")


if __name__ == "__main__":
    unittest.main()
