from __future__ import annotations

from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from case_store import CaseStore, REQUIRED_FIELDS  # noqa: E402


class DataTestCase(unittest.TestCase):
    def test_case_count_and_fields(self) -> None:
        store = CaseStore(REPO_ROOT / "data" / "historical_cases.json", REPO_ROOT / "data" / "user_cases.json")
        cases = store.load_core_cases()
        self.assertGreaterEqual(len(cases), 40)
        for case in cases:
            self.assertTrue(REQUIRED_FIELDS.issubset(case.keys()))
            self.assertTrue(case["source_note"])

    def test_user_cases_file_exists(self) -> None:
        self.assertTrue((REPO_ROOT / "data" / "user_cases.json").exists())


if __name__ == "__main__":
    unittest.main()
