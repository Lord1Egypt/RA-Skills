# -*- coding: utf-8 -*-
"""禁止 import account-manager 内部 RPA 辅助模块。"""
from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

FORBIDDEN_PATTERNS = (
    re.compile(r"\brpa_helpers\b"),
    re.compile(r"\binject_account_manager_scripts_path\b"),
    re.compile(r"\bget_account_credential\b"),
)

SCRIPTS_ROOT = Path(__file__).resolve().parents[1] / "scripts"


class TestNoRpaHelpersImport(unittest.TestCase):
    def test_scripts_tree_has_no_forbidden_account_manager_imports(self) -> None:
        violations: list[str] = []
        for root, _dirs, files in os.walk(SCRIPTS_ROOT):
            for name in files:
                if not name.endswith(".py"):
                    continue
                path = Path(root) / name
                text = path.read_text(encoding="utf-8")
                for pattern in FORBIDDEN_PATTERNS:
                    if pattern.search(text):
                        violations.append(f"{path.relative_to(SCRIPTS_ROOT)}: {pattern.pattern}")
        self.assertEqual(
            violations,
            [],
            msg="Forbidden account-manager internal imports found:\n" + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
