#!/usr/bin/env python3
"""
Regression tests for quick skill validation.
"""

import json
import tempfile
from pathlib import Path
from unittest import TestCase, main

import quick_validate


class TestQuickValidate(TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_quick_validate_"))

    def tearDown(self):
        import shutil

        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_accepts_crlf_frontmatter(self):
        skill_dir = self.temp_dir / "crlf-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = "---\r\nname: crlf-skill\r\ndescription: ok\r\n---\r\n# Skill\r\n"
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertTrue(valid, message)

    def test_rejects_missing_frontmatter_closing_fence(self):
        skill_dir = self.temp_dir / "bad-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = "---\nname: bad-skill\ndescription: missing end\n# no closing fence\n"
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertEqual(message, "Invalid frontmatter format")

    def test_fallback_parser_handles_multiline_frontmatter_without_pyyaml(self):
        skill_dir = self.temp_dir / "multiline-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = """---
name: multiline-skill
description: Works without pyyaml
allowed-tools:
  - gh
metadata: |
  {
    "owners": ["team-openclaw"]
  }
---
# Skill
"""
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        previous_yaml = quick_validate.yaml
        quick_validate.yaml = None
        try:
            valid, message = quick_validate.validate_skill(skill_dir)
        finally:
            quick_validate.yaml = previous_yaml

        self.assertTrue(valid, message)

    def test_accepts_documented_optional_openclaw_frontmatter_keys(self):
        skill_dir = self.temp_dir / "optional-keys-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = """---
name: optional-keys-skill
description: Accepts documented optional keys
homepage: https://example.com/skill
user-invocable: true
disable-model-invocation: false
command-dispatch: tool
command-tool: demo-tool
command-arg-mode: raw
---
# Skill
"""
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertTrue(valid, message)

    def test_init_template_produces_validator_clean_skill(self):
        import init_skill

        output_root = self.temp_dir / "generated"
        output_root.mkdir(parents=True, exist_ok=True)

        created = init_skill.init_skill("generated-skill", output_root, [], False)

        self.assertIsNotNone(created)
        valid, message = quick_validate.validate_skill(created)
        self.assertTrue(valid, message)

    def test_init_template_creates_publish_support_files(self):
        import init_skill

        output_root = self.temp_dir / "publishable"
        output_root.mkdir(parents=True, exist_ok=True)

        created = init_skill.init_skill("publishable-skill", output_root, [], False)

        self.assertIsNotNone(created)
        meta_path = created / "_meta.json"
        ignore_path = created / ".clawhubignore"
        self.assertTrue(meta_path.exists())
        self.assertTrue(ignore_path.exists())
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        self.assertEqual(meta["slug"], "publishable-skill")
        self.assertEqual(meta["version"], "0.1.0")
        ignore_text = ignore_path.read_text(encoding="utf-8")
        self.assertIn("*.skill", ignore_text)
        self.assertIn(".clawhub/", ignore_text)


if __name__ == "__main__":
    main()
