# -*- coding: utf-8 -*-
"""禁止在模板主骨架 scripts/ 中 import account-manager 内部 RPA 辅助模块。"""
from __future__ import annotations

import os
import re
import unittest

from _support import get_skill_root

FORBIDDEN_PATTERNS = (
    re.compile(r"\brpa_helpers\b"),
    re.compile(r"\binject_account_manager_scripts_path\b"),
    re.compile(r"\bget_account_credential\b"),
)


class TestNoRpaHelpersImport(unittest.TestCase):
    def test_scripts_tree_has_no_forbidden_account_manager_imports(self) -> None:
        scripts_dir = os.path.join(get_skill_root(), "scripts")
        violations: list[str] = []
        for root, _dirs, files in os.walk(scripts_dir):
            for name in files:
                if not name.endswith(".py"):
                    continue
                rel = os.path.relpath(os.path.join(root, name), scripts_dir)
                text = open(os.path.join(root, name), encoding="utf-8").read()
                for pattern in FORBIDDEN_PATTERNS:
                    if pattern.search(text):
                        violations.append(f"{rel}: {pattern.pattern}")
        self.assertEqual(
            violations,
            [],
            msg="Forbidden account-manager internal imports in scripts/:\n" + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
