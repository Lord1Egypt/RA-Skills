#!/usr/bin/env python3
"""Unit tests for scripts/spl_distance.py."""

from __future__ import annotations

import math
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import spl_distance as S  # noqa: E402


class TestSplAtDistance(unittest.TestCase):
    def test_six_db_per_doubling(self):
        drop = 20.0 * math.log10(2.0)
        self.assertAlmostEqual(drop, 6.020599913279624, places=12)
        self.assertAlmostEqual(S.spl_at_distance(100.0, 1.0, 2.0), 100.0 - drop, places=12)
        self.assertAlmostEqual(S.spl_at_distance(100.0, 1.0, 4.0), 100.0 - 2 * drop, places=12)
        # The familiar "6 dB per doubling" rule is this value rounded to the nearest decibel.
        self.assertAlmostEqual(drop, 6.0, delta=0.03)

    def test_ten_metres_from_one(self):
        # 20 * log10(10) = 20
        self.assertAlmostEqual(S.spl_at_distance(100.0, 1.0, 10.0), 80.0, places=9)

    def test_inverse_round_trip(self):
        l2 = S.spl_at_distance(112.0, 2.5, 20.0)
        self.assertAlmostEqual(S.spl_at_distance(l2, 20.0, 2.5), 112.0, places=9)

    def test_rejects_non_positive_distance(self):
        with self.assertRaises(ValueError):
            S.spl_at_distance(100.0, 0.0, 1.0)
        with self.assertRaises(ValueError):
            S.spl_at_distance(100.0, 1.0, -3.0)


class TestOccupationalDurations(unittest.TestCase):
    def test_niosh_anchor_and_exchange(self):
        self.assertAlmostEqual(S.niosh_allowed_minutes(85.0), 480.0, places=9)
        self.assertAlmostEqual(S.niosh_allowed_minutes(88.0), 240.0, places=9)
        self.assertAlmostEqual(S.niosh_allowed_minutes(91.0), 120.0, places=9)

    def test_osha_table_g16_anchors(self):
        self.assertAlmostEqual(S.osha_allowed_hours(90.0), 8.0, places=9)
        self.assertAlmostEqual(S.osha_allowed_hours(95.0), 4.0, places=9)
        self.assertAlmostEqual(S.osha_allowed_hours(100.0), 2.0, places=9)
        self.assertAlmostEqual(S.osha_allowed_hours(115.0), 0.25, places=9)

    def test_niosh_formula_direct(self):
        L = 92.0
        expected = 480.0 / (2.0 ** ((L - 85.0) / 3.0))
        self.assertAlmostEqual(S.niosh_allowed_minutes(L), expected, places=12)
        self.assertTrue(math.isfinite(expected))


class TestCli(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "spl_distance.py"), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_cli_distance(self):
        proc = self._run("--level-db", "100", "--at-m", "1", "--to-m", "2")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("93.98 dB at 2 m", proc.stdout)

    def test_cli_duration(self):
        proc = self._run("--continuous-dba", "88", "--duration")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("240.0 minutes", proc.stdout)
        self.assertIn("train horn", proc.stdout.lower())


if __name__ == "__main__":
    unittest.main()
