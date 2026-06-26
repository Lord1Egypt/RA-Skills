#!/usr/bin/env python3

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestPackagingSurface(unittest.TestCase):
    def test_pyproject_declares_console_entrypoint(self):
        pyproject = (REPO_ROOT / "skill-audit" / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('name = "skill-audit"', pyproject)
        self.assertIn('skill-audit = "modeio_skill_audit.cli.skill_safety_assessment:main"', pyproject)


if __name__ == "__main__":
    unittest.main()
