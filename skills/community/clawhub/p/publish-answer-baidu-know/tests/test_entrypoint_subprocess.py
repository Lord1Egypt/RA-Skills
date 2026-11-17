# -*- coding: utf-8 -*-
"""通过 subprocess 调用 ``python scripts/main.py``，验证真实入口（非仅 import main）。"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest

from _support import IsolatedDataRoot, get_skill_root

import importlib.metadata as metadata

from jiangchang_skill_core import version_ge
from util.constants import PLATFORM_KIT_MIN_VERSION


def _platform_kit_meets_template_minimum() -> bool:
    try:
        installed = metadata.version("jiangchang-platform-kit")
    except metadata.PackageNotFoundError:
        return False
    return version_ge(installed, PLATFORM_KIT_MIN_VERSION)


def _run_main(args: list[str], timeout: int = 15) -> subprocess.CompletedProcess[str]:
    root = get_skill_root()
    main_py = os.path.join(root, "scripts", "main.py")
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, main_py, *args],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


class TestEntrypointSubprocess(unittest.TestCase):
    @unittest.skipUnless(
        _platform_kit_meets_template_minimum(),
        f"installed jiangchang-platform-kit below template minimum {PLATFORM_KIT_MIN_VERSION}",
    )
    def test_health_exit_zero(self) -> None:
        with IsolatedDataRoot():
            cp = _run_main(["health"])
            self.assertEqual(cp.returncode, 0, msg=cp.stderr + cp.stdout)

    def test_version_json_and_skill_slug(self) -> None:
        with IsolatedDataRoot():
            cp = _run_main(["version"])
            self.assertEqual(cp.returncode, 0, msg=cp.stderr + cp.stdout)
            payload = json.loads(cp.stdout.strip())
            self.assertIn("version", payload)
            self.assertIn("skill", payload)
            from util.constants import SKILL_SLUG

            self.assertEqual(payload["skill"], SKILL_SLUG)


if __name__ == "__main__":
    unittest.main()
