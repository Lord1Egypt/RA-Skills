# -*- coding: utf-8 -*-
"""Docs guard: template must promote shared runtime, not vendored jiangchang_skill_core."""
from __future__ import annotations

import os
import unittest

from _support import get_skill_root

DOC_PATHS = (
    "README.md",
    "SKILL.md",
    "development/RUNTIME.md",
    "references/CLI.md",
    "development/DEVELOPMENT.md",
    "development/RPA.md",
    "development/CONFIG.md",
)

RUNTIME_DOC_PATHS = tuple(p for p in DOC_PATHS if p != "README.md")

FORBIDDEN_PHRASES = (
    "scripts/jiangchang_skill_core/：运行时",
    "运行时与统一日志副本",
    "vendor 源码在 scripts/jiangchang_skill_core",
    "模板通过 vendor 拷贝引用",
    "vendor 自 platform-kit",
    "模板 vendor 拷贝在 scripts/jiangchang_skill_core",
    "模板默认声明 `jiangchang-platform-kit",
    "模板默认包含 `jiangchang-platform-kit",
    "默认已含 `jiangchang-platform-kit",
    "保留仅含 `jiangchang-platform-kit",
)

POSITIVE_MARKERS = (
    "jiangchang-platform-kit",
    "1.0.17",
    "共享 runtime",
)


class TestTemplateRuntimeStandard(unittest.TestCase):
    def _read(self, rel_path: str) -> str:
        path = os.path.join(get_skill_root(), rel_path)
        with open(path, encoding="utf-8") as f:
            return f.read()

    def test_guarded_docs_avoid_vendored_core_guidance(self) -> None:
        for rel_path in DOC_PATHS:
            text = self._read(rel_path)
            for phrase in FORBIDDEN_PHRASES:
                self.assertNotIn(
                    phrase,
                    text,
                    msg=f"{rel_path} must not contain {phrase!r}",
                )

    def test_guarded_docs_promote_shared_runtime_standard(self) -> None:
        combined = "\n".join(self._read(p) for p in RUNTIME_DOC_PATHS)
        for marker in POSITIVE_MARKERS:
            self.assertIn(
                marker,
                combined,
                msg=f"docs should mention {marker!r}",
            )
        self.assertTrue(
            "不得 vendored" in combined or "不要 vendor" in combined,
            msg="docs should state skills must not vendor jiangchang_skill_core",
        )

    def test_runtime_md_mentions_collect_runtime_diagnostics(self) -> None:
        text = self._read("development/RUNTIME.md")
        self.assertIn("collect_runtime_diagnostics", text)

    def test_cli_md_mentions_health_runtime_diagnostics(self) -> None:
        text = self._read("references/CLI.md")
        self.assertIn("python_executable", text)
        self.assertIn("platform_kit_version", text)
        self.assertIn("jiangchang_skill_core_file", text)
        self.assertIn("python-runtime", text)


if __name__ == "__main__":
    unittest.main()
