# -*- coding: utf-8 -*-
"""SKILL.md 与 util.constants.SKILL_SLUG 一致性（防复制后漏改 constants）。"""
from __future__ import annotations

import os
import re
import unittest

from _support import get_skill_root


def _parse_openclaw_slug(skill_md_text: str) -> str:
    """从 YAML frontmatter 中解析 metadata.openclaw.slug（无 PyYAML 依赖）。"""
    parts = skill_md_text.split("---", 2)
    if len(parts) < 2:
        raise ValueError("missing frontmatter")
    fm = parts[1]
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^\s+openclaw:\s*$", line):
            for j in range(i + 1, len(lines)):
                inner = lines[j]
                if inner.strip() and inner[0] not in (" ", "\t"):
                    break
                m = re.match(r"^(\s+)slug:\s*(.+)\s*$", inner)
                if m:
                    return m.group(2).strip().strip("\"'")
            break
    raise ValueError("slug not found under openclaw")


class TestSkillMetadata(unittest.TestCase):
    def test_skill_slug_alignment(self) -> None:
        root = get_skill_root()
        skill_dir = os.path.basename(root)
        md_path = os.path.join(root, "SKILL.md")
        with open(md_path, encoding="utf-8") as f:
            md = f.read()
        slug_md = _parse_openclaw_slug(md)

        from util.constants import SKILL_SLUG

        self.assertEqual(slug_md, SKILL_SLUG, "SKILL.md slug 必须与 constants.SKILL_SLUG 一致")

        if skill_dir == "skill-template":
            # 模板仓库本体：允许占位 slug
            self.assertEqual(SKILL_SLUG, "your-skill-slug")
        else:
            self.assertNotEqual(SKILL_SLUG, "your-skill-slug", "复制为真实技能后不得保留占位 slug")
            self.assertEqual(SKILL_SLUG, skill_dir)
            self.assertEqual(slug_md, skill_dir)


if __name__ == "__main__":
    unittest.main()
