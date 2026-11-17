from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SelfTest(unittest.TestCase):
    def test_validator_regressions(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v"],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Ran 6 tests", result.stderr)


if __name__ == "__main__":
    unittest.main()
