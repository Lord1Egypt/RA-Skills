# -*- coding: utf-8 -*-
"""skill-template 脚手架与 Git 防串库守护。"""
from __future__ import annotations

import os
import unittest

from _support import get_skill_root

TEMPLATE_MARKER = ".openclaw-skill-template"
TEMPLATE_SLUG = "your-skill-slug"


def _read_skill_slug() -> str:
    constants_path = os.path.join(get_skill_root(), "scripts", "util", "constants.py")
    with open(constants_path, encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("SKILL_SLUG"):
                _, _, value = line.partition("=")
                return value.strip().strip('"').strip("'")
    return ""


class TestScaffoldGuard(unittest.TestCase):
    def test_template_repo_has_marker(self) -> None:
        slug = _read_skill_slug()
        if slug != TEMPLATE_SLUG:
            self.skipTest(f"当前 SKILL_SLUG={slug!r}，非模板占位，跳过 template marker 断言")
        marker = os.path.join(get_skill_root(), TEMPLATE_MARKER)
        self.assertTrue(
            os.path.isfile(marker),
            msg=f"skill-template 源仓库根目录必须存在 {TEMPLATE_MARKER}",
        )

    def test_business_skill_must_not_keep_template_marker(self) -> None:
        slug = _read_skill_slug()
        if slug == TEMPLATE_SLUG:
            self.skipTest("当前仍为模板占位 slug，由 test_template_repo_has_marker 守护")
        marker = os.path.join(get_skill_root(), TEMPLATE_MARKER)
        self.assertFalse(
            os.path.isfile(marker),
            msg=(
                "业务技能不得保留 .openclaw-skill-template；"
                "请使用 tools/scaffold_skill 或删除标记文件并检查是否误复制了模板 .git"
            ),
        )

    def test_development_md_documents_git_cleanup(self) -> None:
        path = os.path.join(get_skill_root(), "development", "DEVELOPMENT.md")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        self.assertIn(".git", text)
        self.assertTrue(
            "scaffold_skill" in text or "scaffold" in text.lower(),
            msg="DEVELOPMENT.md must document scaffold_skill",
        )
        self.assertTrue(
            "remote" in text.lower() or "git remote" in text.lower(),
            msg="DEVELOPMENT.md must mention git remote self-check",
        )


if __name__ == "__main__":
    unittest.main()
