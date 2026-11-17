#!/usr/bin/env python3
"""Regression tests for URL parsing and bounded-scan completeness."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("analyze_skill.py")
SPEC = importlib.util.spec_from_file_location("skill_auditor_under_test", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class AnalyzerTests(unittest.TestCase):
    def test_current_clawhub_url_shape(self):
        parsed = MODULE.parse_input(
            "https://clawhub.ai/jonathanjing/skills/openclaw-dashboard"
        )
        self.assertEqual(parsed["skill_name"], "jonathanjing/openclaw-dashboard")

    def test_legacy_clawhub_url_shape(self):
        parsed = MODULE.parse_input(
            "https://clawhub.ai/jonathanjing/openclaw-dashboard"
        )
        self.assertEqual(parsed["skill_name"], "jonathanjing/openclaw-dashboard")

    def test_file_limit_marks_scan_incomplete_and_unknown(self):
        entries = [
            {"path": f"file-{index}.py", "size": 10}
            for index in range(MODULE.MAX_FETCH_FILES)
        ]
        entries.append({"path": "payload.py", "size": 10})

        original_discover = MODULE._discover_registry
        original_get_json = MODULE._http_get_json
        original_get = MODULE._http_get
        try:
            MODULE._discover_registry = lambda: "https://registry.example"

            def fake_get_json(url, timeout=10):
                if "/versions/" in url:
                    return {"version": {"files": entries}}
                if "/moderation" in url:
                    return {"moderation": {}}
                return {
                    "latestVersion": {"version": "1.0.0"},
                    "skill": {},
                    "owner": {},
                }

            MODULE._http_get_json = fake_get_json
            MODULE._http_get = lambda url, timeout=10: "print('safe')"

            metadata, files = MODULE.fetch_registry_snapshot("owner/slug")
        finally:
            MODULE._discover_registry = original_discover
            MODULE._http_get_json = original_get_json
            MODULE._http_get = original_get

        self.assertEqual(len(files), MODULE.MAX_FETCH_FILES)
        self.assertNotIn("payload.py", files)
        self.assertFalse(metadata["scan_complete"])
        self.assertTrue(
            any(issue.startswith("file_limit_exceeded") for issue in metadata["scan_issues"])
        )
        self.assertEqual(MODULE.verdict(100, metadata), "UNKNOWN")

    def test_known_passive_assets_do_not_make_scan_incomplete(self):
        metadata = {
            "scan_complete": True,
            "clawhub_flagged": False,
        }
        self.assertEqual(MODULE.verdict(100, metadata), "SAFE")


if __name__ == "__main__":
    unittest.main()
