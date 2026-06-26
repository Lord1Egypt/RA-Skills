#!/usr/bin/env python3
"""
Regression tests for weak-model skill validation.
"""

import sys
import tempfile
from pathlib import Path
from unittest import TestCase, main

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import validate_weak_models


class TestValidateWeakModels(TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_validate_weak_models_"))

    def tearDown(self):
        import shutil

        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def make_skill(self, name: str, body: str) -> Path:
        skill_dir = self.temp_dir / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = f"---\nname: {name}\ndescription: test skill\n---\n\n# Skill\n\n{body}\n"
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
        return skill_dir

    def test_accepts_skill_with_explicit_navigation_and_outputs(self):
        skill_dir = self.make_skill(
            "good-skill",
            """
## Instructions
1. Read `references/errors.md` when an error appears. Purpose: match error codes.
2. Write unique codes to `error_codes.txt`. Stop.
""",
        )

        ok, issues, summary = validate_weak_models.validate_weak_model_readiness(skill_dir)

        self.assertTrue(ok, summary)
        self.assertEqual([], issues)

    def test_rejects_reference_without_navigation_format(self):
        skill_dir = self.make_skill(
            "nav-skill",
            """
## Instructions
Read `references/errors.md` for more details.
""",
        )

        ok, issues, _summary = validate_weak_models.validate_weak_model_readiness(skill_dir)

        self.assertFalse(ok)
        self.assertTrue(any(issue.code == "navigation-cue-format" for issue in issues))

    def test_warns_for_ordered_step_missing_output_or_stop(self):
        skill_dir = self.make_skill(
            "step-skill",
            """
## Execution
1. Review the log
""",
        )

        ok, issues, _summary = validate_weak_models.validate_weak_model_readiness(skill_dir)

        self.assertTrue(ok)
        self.assertTrue(any(issue.code == "missing-output-or-stop" for issue in issues))

    def test_warns_when_no_execution_section_exists(self):
        skill_dir = self.make_skill(
            "doc-skill",
            """
## Overview
This skill explains a workflow but does not expose an execution section.
""",
        )

        ok, issues, _summary = validate_weak_models.validate_weak_model_readiness(skill_dir)

        self.assertTrue(ok)
        self.assertTrue(any(issue.code == "no-execution-section" for issue in issues))


if __name__ == "__main__":
    main()
