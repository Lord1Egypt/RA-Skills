# -*- coding: utf-8 -*-
"""配置落盘、合并与读取优先级。"""
from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from _support import IsolatedDataRoot, get_skill_root, platform_kit_version_patch

from jiangchang_skill_core import config
from cli.app import main
from util.config_bootstrap import bootstrap_skill_config
from util.constants import SKILL_SLUG


class TestConfigBootstrap(unittest.TestCase):
    def test_first_run_creates_user_env(self) -> None:
        with IsolatedDataRoot(user_id="_cfg_test"):
            config.reset_cache()
            path = bootstrap_skill_config()
            self.assertTrue(os.path.isfile(path))
            self.assertTrue(path.replace("\\", "/").endswith(f"/{SKILL_SLUG}/.env"))

    def test_existing_env_not_overwritten(self) -> None:
        with IsolatedDataRoot(user_id="_cfg_keep"):
            config.reset_cache()
            path = bootstrap_skill_config()
            with open(path, "w", encoding="utf-8") as f:
                f.write("OPENCLAW_TEST_TARGET=simulator_rpa\n")
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".example") as tmp:
                tmp.write("OPENCLAW_TEST_TARGET=mock\nHUMAN_WAIT_TIMEOUT=60\n")
                tmp_path = tmp.name
            try:
                config.merge_missing_env_keys(tmp_path, path, comment_skill="test")
                with open(path, encoding="utf-8") as f:
                    content = f.read()
                self.assertIn("OPENCLAW_TEST_TARGET=simulator_rpa", content)
                self.assertNotIn("OPENCLAW_TEST_TARGET=mock", content)
            finally:
                os.unlink(tmp_path)
            config.reset_cache()

    def test_merge_appends_missing_keys(self) -> None:
        with IsolatedDataRoot(user_id="_cfg_merge"):
            config.reset_cache()
            path = bootstrap_skill_config()
            with open(path, "w", encoding="utf-8") as f:
                f.write("OPENCLAW_TEST_TARGET=simulator_rpa\n")
            example = os.path.join(get_skill_root(), ".env.example")
            added = config.merge_missing_env_keys(example, path, comment_skill="test")
            self.assertIn("HUMAN_WAIT_TIMEOUT", added)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("HUMAN_WAIT_TIMEOUT=180", content)

    def test_config_priority_process_user_example(self) -> None:
        with IsolatedDataRoot(user_id="_cfg_prio"):
            config.reset_cache()
            example = os.path.join(get_skill_root(), ".env.example")
            path = config.ensure_env_file(SKILL_SLUG, example)
            with open(path, "w", encoding="utf-8") as f:
                f.write("PRIORITY_TEST_KEY=from_user\n")
            config.reset_cache()

            os.environ["PRIORITY_TEST_KEY"] = "from_process"
            self.assertEqual(config.get("PRIORITY_TEST_KEY"), "from_process")

            del os.environ["PRIORITY_TEST_KEY"]
            config.reset_cache()
            self.assertEqual(config.get("PRIORITY_TEST_KEY"), "from_user")

            with open(path, "w", encoding="utf-8") as f:
                f.write("# empty user\n")
            config.reset_cache()
            with open(example, encoding="utf-8") as f:
                example_text = f.read()
            self.assertIn("OPENCLAW_TEST_TARGET=mock", example_text)
            self.assertEqual(config.get("OPENCLAW_TEST_TARGET"), "mock")

    def test_config_path_outputs_json(self) -> None:
        with IsolatedDataRoot(user_id="_cfg_path"):
            config.reset_cache()
            bootstrap_skill_config()
            buf = io.StringIO()
            with redirect_stdout(buf), redirect_stderr(io.StringIO()):
                rc = main(["config-path"])
            self.assertEqual(rc, 0)
            payload = json.loads(buf.getvalue().strip())
            self.assertEqual(payload["skill"], SKILL_SLUG)
            self.assertTrue(payload["env_path"])
            self.assertTrue(payload["example_path"].endswith(".env.example"))

    def test_health_does_not_print_sensitive_plaintext(self) -> None:
        with IsolatedDataRoot(user_id="_cfg_health"):
            os.environ["OPENCLAW_RECORD_VIDEO"] = "0"
            config.reset_cache()
            path = bootstrap_skill_config()
            with open(path, "a", encoding="utf-8") as f:
                f.write("FAKE_SECRET_TOKEN=supersecret12345\n")
            config.reset_cache()
            buf = io.StringIO()
            with platform_kit_version_patch(), redirect_stdout(buf), redirect_stderr(io.StringIO()):
                rc = main(["health"])
            self.assertEqual(rc, 0)
            out = buf.getvalue()
            self.assertNotIn("supersecret12345", out)
            self.assertIn("env_path:", out)
            self.assertIn("env_exists: True", out)


if __name__ == "__main__":
    unittest.main()
