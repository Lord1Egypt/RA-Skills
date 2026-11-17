# -*- coding: utf-8 -*-
"""Architecture guard: runtime diagnostics must come from platform-kit."""
from __future__ import annotations

import os
import unittest

from _support import get_scripts_dir, get_skill_root

_FORBIDDEN_DEFINITIONS = (
    "class RuntimeDiagnostics",
    "class RuntimeIssue",
    "def collect_runtime_diagnostics",
    "def format_runtime_health_lines",
    "def runtime_diagnostics_dict",
    "def _is_git_lfs_pointer",
    "def _is_usable_audio_file",
    "def _probe_background_music",
)


class TestRuntimeDiagnosticsIntegration(unittest.TestCase):
    def test_no_vendored_jiangchang_skill_core(self) -> None:
        vendored = os.path.join(get_scripts_dir(), "jiangchang_skill_core")
        self.assertFalse(os.path.isdir(vendored), vendored)

    def test_runtime_diagnostics_module_removed(self) -> None:
        legacy = os.path.join(get_scripts_dir(), "util", "runtime_diagnostics.py")
        self.assertFalse(os.path.isfile(legacy), legacy)

    def test_util_py_files_do_not_reimplement_runtime_diagnostics(self) -> None:
        util_dir = os.path.join(get_scripts_dir(), "util")
        for name in os.listdir(util_dir):
            if not name.endswith(".py"):
                continue
            path = os.path.join(util_dir, name)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            for forbidden in _FORBIDDEN_DEFINITIONS:
                self.assertNotIn(
                    forbidden,
                    text,
                    msg=f"{name} must not define {forbidden}",
                )

    def test_task_service_imports_platform_kit_diagnostics(self) -> None:
        path = os.path.join(get_scripts_dir(), "service", "task_service.py")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        self.assertIn("from jiangchang_skill_core import", text)
        self.assertIn("collect_runtime_diagnostics", text)
        self.assertIn("format_runtime_health_lines", text)
        self.assertIn("PLATFORM_KIT_MIN_VERSION", text)
        self.assertNotIn("from util.runtime_diagnostics import", text)

    def test_collect_runtime_diagnostics_callable_from_platform_kit(self) -> None:
        from jiangchang_skill_core import collect_runtime_diagnostics

        from util.constants import PLATFORM_KIT_MIN_VERSION, SKILL_SLUG
        from util.runtime_paths import get_skill_root

        diag = collect_runtime_diagnostics(
            skill_slug=SKILL_SLUG,
            platform_kit_min_version=PLATFORM_KIT_MIN_VERSION,
            skill_root=get_skill_root(),
        )
        self.assertEqual(diag.skill_slug, SKILL_SLUG)
        self.assertEqual(diag.platform_kit_min_version, PLATFORM_KIT_MIN_VERSION)


if __name__ == "__main__":
    unittest.main()
