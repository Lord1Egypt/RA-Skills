# -*- coding: utf-8 -*-
"""防回归：公共能力必须从共享 platform-kit 导入，而非技能 vendored 副本。"""
from __future__ import annotations

import importlib.metadata as metadata
import os
import re
import sys
import unittest

from _support import get_scripts_dir, get_skill_root


def _parse_platform_kit_min_version(skill_md_text: str) -> str:
    parts = skill_md_text.split("---", 2)
    if len(parts) < 2:
        raise ValueError("missing frontmatter")
    m = re.search(
        r"platform_kit_min_version:\s*[\"']?([^\"'\s]+)[\"']?",
        parts[1],
    )
    if not m:
        raise ValueError("platform_kit_min_version not found")
    return m.group(1).strip()


def _requirement_dependency_lines(req_text: str) -> list[str]:
    return [
        line.strip()
        for line in req_text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


class TestPlatformImportSource(unittest.TestCase):
    def test_jiangchang_skill_core_not_from_skill_scripts(self) -> None:
        scripts_dir = os.path.abspath(get_scripts_dir())
        skill_root = os.path.abspath(get_skill_root())
        vendored = os.path.join(scripts_dir, "jiangchang_skill_core")

        self.assertFalse(
            os.path.isdir(vendored),
            f"vendored package must not exist: {vendored}",
        )

        import jiangchang_skill_core
        import jiangchang_skill_core.rpa.video_session as video_session

        core_file = os.path.abspath(jiangchang_skill_core.__file__)
        video_file = os.path.abspath(video_session.__file__)

        self.assertNotIn(
            scripts_dir.lower(),
            core_file.lower(),
            msg=f"jiangchang_skill_core loaded from skill scripts: {core_file}",
        )
        self.assertNotIn(
            skill_root.lower(),
            core_file.lower(),
            msg=f"jiangchang_skill_core loaded from skill tree: {core_file}",
        )
        self.assertNotIn(
            scripts_dir.lower(),
            video_file.lower(),
            msg=f"video_session loaded from skill scripts: {video_file}",
        )

        from jiangchang_skill_core.rpa.video_session import RpaVideoSession

        self.assertTrue(callable(RpaVideoSession))

    def test_skill_tree_load_issue_helper(self) -> None:
        from jiangchang_skill_core import is_jiangchang_skill_core_from_skill_tree

        skill_root = os.path.abspath(get_skill_root())
        fake = os.path.join(skill_root, "scripts", "jiangchang_skill_core", "__init__.py")
        self.assertTrue(
            is_jiangchang_skill_core_from_skill_tree(skill_root=skill_root, core_file=fake)
        )
        self.assertFalse(
            is_jiangchang_skill_core_from_skill_tree(
                skill_root=skill_root, core_file=sys.executable
            )
        )

    def test_platform_kit_min_version_is_1_0_14(self) -> None:
        from jiangchang_skill_core import version_ge
        from util.constants import PLATFORM_KIT_MIN_VERSION

        self.assertEqual(PLATFORM_KIT_MIN_VERSION, "1.0.17")

        md_path = os.path.join(get_skill_root(), "SKILL.md")
        with open(md_path, encoding="utf-8") as f:
            md = f.read()
        self.assertEqual(_parse_platform_kit_min_version(md), "1.0.17")

        req_path = os.path.join(get_skill_root(), "requirements.txt")
        with open(req_path, encoding="utf-8") as f:
            req = f.read()
        dep_lines = _requirement_dependency_lines(req)
        dep_body = "\n".join(dep_lines).lower()
        self.assertNotIn("jiangchang-platform-kit", dep_body)
        self.assertNotIn("playwright", dep_body)

        try:
            installed = metadata.version("jiangchang-platform-kit")
        except metadata.PackageNotFoundError:
            self.skipTest("jiangchang-platform-kit not installed in current interpreter")
        if not version_ge(installed, PLATFORM_KIT_MIN_VERSION):
            self.skipTest(
                f"installed jiangchang-platform-kit {installed!r} < required "
                f"{PLATFORM_KIT_MIN_VERSION!r}; upgrade shared runtime to enforce this check"
            )
        self.assertTrue(
            version_ge(installed, PLATFORM_KIT_MIN_VERSION),
            msg=f"installed {installed!r} < required {PLATFORM_KIT_MIN_VERSION!r}",
        )

    def test_collect_runtime_diagnostics_importable(self) -> None:
        from jiangchang_skill_core import collect_runtime_diagnostics

        self.assertTrue(callable(collect_runtime_diagnostics))

    def test_main_import_smoke(self) -> None:
        scripts_dir = get_scripts_dir()
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)

        from cli.app import build_parser

        parser = build_parser()
        self.assertIsNotNone(parser)


if __name__ == "__main__":
    unittest.main()
