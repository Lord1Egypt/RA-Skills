from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import scripts.check_skill as MODULE


FIXTURES = ROOT / "tests" / "fixtures"


class SkillCheckerTests(unittest.TestCase):
    def audit_fixture(self, name: str):
        return MODULE.audit_target(str(FIXTURES / name))

    def test_minimal_pass_fixture_passes(self):
        result = self.audit_fixture("minimal-pass")
        self.assertEqual(result.status, "通过")
        self.assertEqual(result.severe_count, 0)

    def test_strong_pass_fixture_avoids_false_positive(self):
        result = self.audit_fixture("strong-pass")
        self.assertEqual(result.status, "通过")
        self.assertEqual(result.severe_count, 0)

    def test_absolute_skill_file_path_is_supported(self):
        result = MODULE.audit_target(
            str((FIXTURES / "strong-pass" / "SKILL.md").resolve())
        )
        self.assertEqual(result.status, "通过")
        self.assertEqual(result.resolved_from, "file")

    def test_absolute_skill_directory_path_is_supported(self):
        result = MODULE.audit_target(str((FIXTURES / "strong-pass").resolve()))
        self.assertEqual(result.status, "通过")
        self.assertEqual(result.resolved_from, "directory")

    def test_missing_name_is_severe(self):
        result = self.audit_fixture("spec-fail-missing-name")
        self.assertEqual(result.status, "通过")
        self.assertTrue(any(item.rule_id == "spec.required-name" for item in result.findings))

    def test_unknown_field_and_generic_description_fail_threshold(self):
        result = self.audit_fixture("threshold-two-severe")
        self.assertEqual(result.status, "不通过")
        self.assertGreaterEqual(result.severe_count, 2)

    def test_single_severe_issue_can_still_pass(self):
        result = self.audit_fixture("threshold-one-severe")
        self.assertEqual(result.status, "通过")
        self.assertEqual(result.severe_count, 1)

    def test_missing_skill_file_is_blocking_failure(self):
        result = self.audit_fixture("missing-skill-file")
        self.assertEqual(result.status, "不通过")
        self.assertGreaterEqual(result.severe_count, 2)
        self.assertIsNone(result.skill_path)

    def test_invalid_yaml_blocks_audit(self):
        result = self.audit_fixture("spec-fail-invalid-yaml")
        self.assertEqual(result.status, "不通过")
        self.assertTrue(any(item.rule_id == "spec.frontmatter-invalid" for item in result.findings))

    def test_license_and_metadata_keys_are_required(self):
        result = self.audit_fixture("spec-fail-missing-required-fields")
        self.assertEqual(result.status, "不通过")
        self.assertTrue(any(item.rule_id == "spec.required-license" for item in result.findings))
        self.assertTrue(
            any(item.rule_id == "spec.required-metadata-version" for item in result.findings)
        )

    def test_recommended_bilingual_descriptions_emit_warnings(self):
        result = self.audit_fixture("threshold-one-severe")
        self.assertTrue(
            any(
                item.rule_id == "semantics.recommended-description_en"
                for item in result.findings
            )
        )
        self.assertTrue(
            any(
                item.rule_id == "semantics.recommended-description_zh"
                for item in result.findings
            )
        )

    def test_html_report_contains_summary_and_findings(self):
        result = self.audit_fixture("semantic-fail-empty-body")
        report_path = ROOT / "tests" / "_report-test.html"
        try:
            MODULE.write_report(result, str(report_path))
            rendered = report_path.read_text(encoding="utf-8")
        finally:
            if report_path.exists():
                report_path.unlink()
        self.assertIn("Skill Checker Report", rendered)
        self.assertIn("Findings", rendered)
        self.assertIn("setLang(\"en\")", rendered)
        self.assertIn("semantics.empty-body", rendered)
        self.assertIn("中文", rendered)


if __name__ == "__main__":
    unittest.main()
