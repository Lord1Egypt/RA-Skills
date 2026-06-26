#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for ebird_region_query (no .upstream required for core tests)."""

import tempfile
import unittest
from pathlib import Path

# Load module from same directory
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "ebird_region_query",
    Path(__file__).resolve().parent / "ebird_region_query.py",
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)


class TestLoadBoundsLabels(unittest.TestCase):
    def test_parses_comment_lines(self):
        sample = '''REGION_BOUNDS = {
    "CN-31": (30.7, 31.9, 120.8, 122),    # 上海
    "US-TX": (25.8, 36.5, -106.6,-93.5), # Texas
    "XX": (0, 1, 2, 3),
}
'''
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(sample)
            p = Path(f.name)
        try:
            d = _mod.load_bounds_labels(p)
            self.assertEqual(d.get("CN-31"), "上海")
            self.assertEqual(d.get("US-TX"), "Texas")
            self.assertNotIn("XX", d)
        finally:
            p.unlink(missing_ok=True)


class TestMatchScore(unittest.TestCase):
    def test_code_exact(self):
        rec = {"code": "CN-31", "name": "Shanghai", "name_cn": "上海", "pinyin": "shanghai"}
        self.assertGreaterEqual(_mod.match_score("CN-31", rec), 0.99)

    def test_substring_cn(self):
        rec = {"code": "CN-44", "name": "Guangdong", "name_cn": "广东", "pinyin": "guangdong"}
        self.assertGreaterEqual(_mod.match_score("广东", rec), 0.9)

    def test_fuzzy_en(self):
        rec = {"code": "US-TX", "name": "Texas", "name_cn": "德克萨斯", "pinyin": ""}
        self.assertGreaterEqual(_mod.match_score("texas", rec), 0.9)


class TestIntegrationOptional(unittest.TestCase):
    """Run when .upstream exists."""

    def test_build_records_not_empty(self):
        up = _mod._upstream()
        if not (up / "birdid" / "data" / "ebird_regions.json").is_file():
            self.skipTest("no .upstream clone")
        rows = _mod.build_records(up)
        self.assertGreater(len(rows), 50)
        codes = {r["code"] for r in rows}
        self.assertIn("CN-31", codes)
        self.assertIn("AU", codes)


if __name__ == "__main__":
    unittest.main()
