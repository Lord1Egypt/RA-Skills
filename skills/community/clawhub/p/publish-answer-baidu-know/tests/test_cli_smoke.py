# -*- coding: utf-8 -*-
"""通用 CLI 冒烟：用法、health、version、logs、log-get、run 参数校验。"""
from __future__ import annotations

import io
import json
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout

from _support import IsolatedDataRoot, platform_kit_version_patch

from jiangchang_skill_core import config

# scripts/ 已由 _support 注入 sys.path
from cli.app import main
from util.constants import SKILL_SLUG


class TestCliSmoke(unittest.TestCase):
    def test_main_empty_argv_shows_usage_and_nonzero(self) -> None:
        buf = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(err):
            rc = main([])
        self.assertEqual(rc, 1)
        out = buf.getvalue()
        self.assertIn(SKILL_SLUG, out)
        self.assertIn("health", out)

    def test_health_zero(self) -> None:
        old_record = os.environ.get("OPENCLAW_RECORD_VIDEO")
        os.environ["OPENCLAW_RECORD_VIDEO"] = "0"
        try:
            buf = io.StringIO()
            with platform_kit_version_patch(), redirect_stdout(buf), redirect_stderr(io.StringIO()):
                rc = main(["health"])
            self.assertEqual(rc, 0)
            out = buf.getvalue()
            self.assertIn("health:", out)
            self.assertIn("python_executable:", out)
            self.assertIn("platform_kit_version:", out)
            self.assertIn("jiangchang_skill_core_file:", out)
        finally:
            if old_record is None:
                os.environ.pop("OPENCLAW_RECORD_VIDEO", None)
            else:
                os.environ["OPENCLAW_RECORD_VIDEO"] = old_record

    def test_version_json_and_matches_constants_slug(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(io.StringIO()):
            rc = main(["version"])
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue().strip())
        self.assertIn("version", payload)
        self.assertIn("skill", payload)
        self.assertEqual(payload["skill"], SKILL_SLUG)

    def test_logs_empty_returns_zero(self) -> None:
        with IsolatedDataRoot():
            buf = io.StringIO()
            with redirect_stdout(buf), redirect_stderr(io.StringIO()):
                rc = main(["logs"])
            self.assertEqual(rc, 0)
            self.assertIn("暂无", buf.getvalue())

    def test_log_get_non_numeric_returns_nonzero(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(io.StringIO()):
            rc = main(["log-get", "not-a-number"])
        self.assertNotEqual(rc, 0)
        self.assertIn("数字", buf.getvalue())

    def test_run_without_required_params_returns_nonzero(self) -> None:
        """run 缺少 --question-url / --input-id 时返回非零并输出结构化错误 JSON。"""
        old_auth = os.environ.pop("JIANGCHANG_AUTH_BASE_URL", None)
        old_record = os.environ.get("OPENCLAW_RECORD_VIDEO")
        os.environ["OPENCLAW_RECORD_VIDEO"] = "0"
        try:
            with IsolatedDataRoot(user_id="_cli_run"):
                config.reset_cache()
                buf = io.StringIO()
                with redirect_stdout(buf), redirect_stderr(io.StringIO()):
                    rc = main(["run"])
                self.assertNotEqual(rc, 0)
                out = buf.getvalue().strip()
                # 应输出包含 error.code 的 JSON
                self.assertIn("QUESTION_URL_EMPTY", out)
        finally:
            if old_auth is not None:
                os.environ["JIANGCHANG_AUTH_BASE_URL"] = old_auth
            if old_record is None:
                os.environ.pop("OPENCLAW_RECORD_VIDEO", None)
            else:
                os.environ["OPENCLAW_RECORD_VIDEO"] = old_record


if __name__ == "__main__":
    unittest.main()
