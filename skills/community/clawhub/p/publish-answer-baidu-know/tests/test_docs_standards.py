# -*- coding: utf-8 -*-
"""文档与 pytest 配置守护：防止模板标准退化。"""
from __future__ import annotations

import configparser
import os
import re
import unittest

from _support import get_skill_root


FORBIDDEN_README_DESCRIPTION_TERMS_EN = (
    "cli",
    "schema",
    "references",
    "development",
    "playwright",
    "python",
    "dom",
    "rpa",
)

FORBIDDEN_README_DESCRIPTION_TERMS_ZH = (
    "Agent 参考索引",
    "契约",
    "数据结构",
    "开发规范",
)


def _description_has_forbidden_term(description: str) -> str | None:
    lowered = description.lower()
    for term in FORBIDDEN_README_DESCRIPTION_TERMS_EN:
        if term in lowered:
            return term
    for term in FORBIDDEN_README_DESCRIPTION_TERMS_ZH:
        if term in description:
            return term
    return None


def _extract_workflow_uses_line(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("uses:"):
            return stripped
    return None


class TestDocsStandards(unittest.TestCase):
    def _read(self, rel_path: str) -> str:
        path = os.path.join(get_skill_root(), rel_path)
        with open(path, encoding="utf-8") as f:
            return f.read()

    def _parse_frontmatter(self, text: str) -> str:
        parts = text.split("---", 2)
        if len(parts) < 2:
            return ""
        return parts[1]

    def test_root_readme_has_yaml_frontmatter(self) -> None:
        text = self._read("README.md")
        self.assertTrue(text.startswith("---"), "README.md must start with YAML frontmatter")
        parts = text.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "README.md frontmatter must be closed")

    def test_root_readme_frontmatter_has_description(self) -> None:
        frontmatter = self._parse_frontmatter(self._read("README.md"))
        self.assertIn("description:", frontmatter, "README.md frontmatter must include description")

    def test_root_readme_description_avoids_technical_index_terms(self) -> None:
        frontmatter = self._parse_frontmatter(self._read("README.md"))
        match = re.search(r"description:\s*(.+)", frontmatter)
        self.assertIsNotNone(match, "README.md description field not found")
        description = match.group(1).strip().strip("\"'")
        forbidden = _description_has_forbidden_term(description)
        self.assertIsNone(
            forbidden,
            msg=f"README.md description must not contain technical index term {forbidden!r}",
        )

    def test_description_forbidden_terms_are_case_insensitive_for_english(self) -> None:
        fail_cases = (
            "CLI 契约说明",
            "cli 工具入口",
            "SCHEMA 定义",
            "Schema 映射",
            "schema 字段",
            "Playwright 自动化",
            "python 脚本",
            "RPA 流程",
        )
        pass_cases = (
            "用用户能理解的方式说明这个技能能做什么、适合什么场景，以及如何开始使用。",
            "帮你自动整理订单并生成处理报告",
            "适合每天需要重复核对的业务场景",
        )
        for description in fail_cases:
            with self.subTest(description=description):
                self.assertIsNotNone(
                    _description_has_forbidden_term(description),
                    msg=f"expected forbidden term in {description!r}",
                )
        for description in pass_cases:
            with self.subTest(description=description):
                self.assertIsNone(
                    _description_has_forbidden_term(description),
                    msg=f"expected no forbidden term in {description!r}",
                )

    def test_references_readme_has_no_yaml_frontmatter(self) -> None:
        text = self._read("references/README.md")
        self.assertFalse(
            text.lstrip().startswith("---"),
            "references/README.md must not contain YAML frontmatter",
        )

    def test_references_readme_has_no_description_field(self) -> None:
        text = self._read("references/README.md")
        self.assertNotRegex(
            text,
            r"(?m)^description\s*:",
            msg="references/README.md must not contain description field",
        )

    def test_skill_md_requires_read_readme_first_rule(self) -> None:
        text = self._read("SKILL.md")
        self.assertIn("README.md", text)
        self.assertTrue(
            "优先读取" in text or "优先读" in text,
            msg="SKILL.md must require reading README.md first for user-facing questions",
        )

    def test_skill_md_states_readme_is_for_users(self) -> None:
        text = self._read("SKILL.md")
        self.assertIn("README.md", text)
        self.assertTrue(
            any(marker in text for marker in ("面向用户", "普通用户", "用户市场")),
            msg="SKILL.md must state README.md is user-facing documentation",
        )

    def test_naming_md_exists_and_covers_standards(self) -> None:
        text = self._read("development/NAMING.md")
        self.assertIn("verb-noun-platform", text)
        self.assertIn("48", text)
        self.assertTrue("LEGACY" in text or "历史" in text)
        self.assertTrue("verbs.txt" in text or "动词白名单" in text)
        self.assertTrue("platforms.txt" in text or "平台白名单" in text)
        self.assertTrue("仅适用于新创建" in text or "新技能" in text)

    def test_release_workflow_uses_main_channel(self) -> None:
        text = self._read(".github/workflows/release_skill.yaml")
        uses_line = _extract_workflow_uses_line(text)
        self.assertIsNotNone(uses_line, "release_skill.yaml must contain a uses: line")
        self.assertIn(
            "client-jiangchang/jiangchang-platform-kit/.github/workflows/reusable-release-skill.yaml",
            uses_line,
        )
        self.assertRegex(
            uses_line,
            r"reusable-release-skill\.yaml@main\b",
            msg="workflow uses must reference reusable-release-skill.yaml@main",
        )

    def test_rpa_md_covers_video_and_playwright_standards(self) -> None:
        text = self._read("development/RPA.md")
        self.assertIn("title", text)
        self.assertIn("closing_title", text)
        self.assertIn("中文", text)
        self.assertIn("--no-sandbox", text)
        self.assertIn("--disable-blink-features=AutomationControlled", text)
        self.assertIn("RpaVideoSession", text)
        self.assertIn("1.0.17", text)

    def test_rpa_md_forbids_rpa_helpers_import(self) -> None:
        text = self._read("development/RPA.md")
        self.assertIn("rpa_helpers", text)
        self.assertTrue(
            "不要 import" in text or "不要" in text and "import" in text,
            msg="RPA.md must document forbidding rpa_helpers import",
        )

    def test_rpa_md_covers_simulator_playwright_layering(self) -> None:
        text = self._read("development/RPA.md")
        self.assertTrue(
            "simulator_playwright" in text
            or ("薄 adapter" in text and "playwright.py" in text),
            msg="RPA.md must describe thin adapter + *_playwright.py layering",
        )

    def test_rpa_md_covers_industry_simulator_portal(self) -> None:
        text = self._read("development/RPA.md")
        self.assertTrue(
            any(marker in text for marker in ("jc2009", "行业仿真", "门户")),
            msg="RPA.md must mention jc2009 / industry simulator / portal gate",
        )

    def test_simulator_example_readme_covers_async_and_account_manager(self) -> None:
        text = self._read("examples/simulator_browser_rpa/README.md")
        self.assertIn("async", text.lower())
        self.assertTrue(
            "account-manager" in text.lower() or "pick-web" in text or "pick_web_account" in text,
            msg="simulator_browser_rpa README must mention async and account-manager",
        )

    def test_development_md_documents_scaffold_and_git_cleanup(self) -> None:
        text = self._read("development/DEVELOPMENT.md")
        self.assertTrue(
            "scaffold_skill" in text or "scaffold_skill.ps1" in text,
            msg="DEVELOPMENT.md must document scaffold_skill",
        )
        self.assertTrue(
            ("Remove-Item" in text and ".git" in text)
            or ("删除" in text and ".git" in text),
            msg="DEVELOPMENT.md must document deleting .git",
        )

    def test_naming_md_copy_flow_documents_scaffold_or_git_cleanup(self) -> None:
        text = self._read("development/NAMING.md")
        self.assertTrue(
            "scaffold" in text.lower() or ("清理" in text and ".git" in text),
            msg="NAMING.md §9 must mention scaffold or Git cleanup",
        )

    def test_scaffold_ps1_exists(self) -> None:
        path = os.path.join(get_skill_root(), "tools", "scaffold_skill.ps1")
        self.assertTrue(os.path.isfile(path), msg="tools/scaffold_skill.ps1 must exist")

    def test_guarded_docs_do_not_reference_amazon_implementation(self) -> None:
        forbidden = (
            "download-settlement-report-amazon",
            "amazon_sim",
            "#amz-email",
        )
        guarded_docs = (
            "development/RPA.md",
            "development/ADAPTER.md",
            "development/DEVELOPMENT.md",
            "development/CONFIG.md",
            "development/TESTING.md",
            "examples/README.md",
            "examples/simulator_browser_rpa/README.md",
        )
        for rel in guarded_docs:
            text = self._read(rel)
            for fragment in forbidden:
                self.assertNotIn(
                    fragment,
                    text,
                    msg=f"{rel} must not reference Amazon implementation {fragment!r}",
                )

    def test_adapter_md_covers_four_tiers_and_config_get(self) -> None:
        text = self._read("development/ADAPTER.md")
        for marker in (
            "mock",
            "simulator_rpa",
            "real_api",
            "real_rpa",
            "config.get",
            "sibling_bridge",
        ):
            self.assertIn(marker, text, msg=f"ADAPTER.md missing {marker!r}")
        self.assertNotIn("ALLOW_REAL_API", text)
        self.assertNotIn("ALLOW_WRITE_ACTIONS", text)

    def test_cli_md_mentions_shared_python_runtime(self) -> None:
        text = self._read("references/CLI.md")
        self.assertIn("python-runtime", text)
        self.assertIn("uv run python", text)

    def test_testing_md_mentions_pytest_txt_collection_guard(self) -> None:
        text = self._read("development/TESTING.md")
        self.assertIn(".txt", text)
        self.assertIn("pytest.ini", text)

    def test_docs_do_not_claim_1_0_11_as_current_standard(self) -> None:
        for rel in (
            "SKILL.md",
            "development/RUNTIME.md",
            "development/RPA.md",
            "development/CONFIG.md",
            "development/TESTING.md",
        ):
            text = self._read(rel)
            self.assertNotIn(
                ">=1.0.11",
                text.replace(" ", ""),
                msg=f"{rel} still claims 1.0.11 as current minimum",
            )

    def test_scripts_has_no_legacy_example_artifacts(self) -> None:
        scripts_dir = os.path.join(get_skill_root(), "scripts")
        service_dir = os.path.join(scripts_dir, "service")
        self.assertFalse(
            os.path.isfile(os.path.join(service_dir, "example_browser_rpa.py")),
            "scripts/service/example_browser_rpa.py must not exist",
        )
        self.assertFalse(
            os.path.isdir(os.path.join(service_dir, "example_adapter")),
            "scripts/service/example_adapter/ must not exist",
        )

    def test_gitignore_covers_python_runtime_artifacts(self) -> None:
        text = self._read(".gitignore")
        self.assertIn("__pycache__", text)
        self.assertIn(".pytest_cache", text)
        self.assertTrue(
            "py[cod]" in text or ".pyc" in text,
            msg=".gitignore must ignore Python bytecode (e.g. *.py[cod])",
        )

    def test_scripts_runtime_artifacts_not_tracked_by_git(self) -> None:
        import subprocess

        try:
            out = subprocess.run(
                ["git", "ls-files", "scripts"],
                cwd=get_skill_root(),
                capture_output=True,
                text=True,
                check=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            self.skipTest("git not available or not a git repo")
        tracked = out.stdout.splitlines()
        for rel in tracked:
            lowered = rel.replace("\\", "/").lower()
            self.assertNotIn("__pycache__", lowered, msg=f"tracked cache path: {rel}")
            self.assertNotIn(".pytest_cache", lowered, msg=f"tracked cache path: {rel}")
            self.assertFalse(lowered.endswith(".pyc"), msg=f"tracked .pyc file: {rel}")

    def test_examples_top_level_modes_present(self) -> None:
        examples_dir = os.path.join(get_skill_root(), "examples")
        for mode in ("real_api", "real_browser_rpa", "simulator_api", "simulator_browser_rpa"):
            self.assertTrue(
                os.path.isdir(os.path.join(examples_dir, mode)),
                msg=f"examples/{mode}/ must exist",
            )

    def test_examples_are_not_full_skill_repos(self) -> None:
        examples_dir = os.path.join(get_skill_root(), "examples")
        for mode in os.listdir(examples_dir):
            mode_path = os.path.join(examples_dir, mode)
            if not os.path.isdir(mode_path):
                continue
            self.assertFalse(
                os.path.isfile(os.path.join(mode_path, "SKILL.md")),
                msg=f"examples/{mode}/SKILL.md must not exist",
            )
            self.assertFalse(
                os.path.isdir(os.path.join(mode_path, "references")),
                msg=f"examples/{mode}/references/ must not exist",
            )
            self.assertFalse(
                os.path.isdir(os.path.join(mode_path, "development")),
                msg=f"examples/{mode}/development/ must not exist",
            )
            self.assertFalse(
                os.path.isdir(os.path.join(mode_path, ".github")),
                msg=f"examples/{mode}/.github/ must not exist",
            )

    def test_examples_readme_states_copy_boundary(self) -> None:
        text = self._read("examples/README.md")
        self.assertIn("不是完整 skill 仓库", text)
        self.assertIn("核心实现案例", text)
        self.assertTrue(
            "不要整包照搬" in text or "不要整包" in text,
            msg="examples/README.md must warn against copying whole example tree",
        )
        self.assertTrue(
            "scripts" in text and ("复制" in text or "copy map" in text.lower()),
            msg="examples/README.md must describe copying into scripts/",
        )

    def test_placeholder_api_examples_are_not_implementation_references(self) -> None:
        for rel in ("examples/real_api/README.md", "examples/simulator_api/README.md"):
            text = self._read(rel)
            self.assertTrue(
                "占位" in text or "规划" in text,
                msg=f"{rel} must state placeholder/planned status",
            )
            self.assertTrue(
                "尚未沉淀" in text or "不可作为实现参考" in text or "不可" in text,
                msg=f"{rel} must warn not to use as implementation reference",
            )

    def test_docs_do_not_reference_scripts_legacy_examples(self) -> None:
        forbidden_fragments = (
            "scripts/service/example_browser_rpa",
            "scripts/service/example_adapter",
            "example_browser_rpa.py",
            "example_adapter/",
        )
        doc_paths = []
        for root, _dirs, files in os.walk(get_skill_root()):
            rel_root = os.path.relpath(root, get_skill_root())
            if rel_root.startswith(".git"):
                continue
            for name in files:
                if name.endswith(".md"):
                    doc_paths.append(os.path.join(rel_root, name).replace("\\", "/"))
        for rel in doc_paths:
            text = self._read(rel)
            for fragment in forbidden_fragments:
                self.assertNotIn(
                    fragment,
                    text,
                    msg=f"{rel} must not reference legacy scripts example path {fragment!r}",
                )


class TestPytestIniCollection(unittest.TestCase):
    def test_pytest_ini_exists_and_limits_python_files(self) -> None:
        ini_path = os.path.join(get_skill_root(), "pytest.ini")
        self.assertTrue(os.path.isfile(ini_path), "pytest.ini must exist at repo root")
        parser = configparser.ConfigParser()
        parser.read(ini_path, encoding="utf-8")
        python_files = parser.get("pytest", "python_files", fallback="")
        self.assertIn("test_*.py", python_files)
        self.assertIn("*_test.py", python_files)


if __name__ == "__main__":
    unittest.main()
