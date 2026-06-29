#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from entropy_metrics import normalized_discrete_entropy  # noqa: E402


class EntropyMetricsTests(unittest.TestCase):
    def test_degenerate_ensemble_has_zero_entropy(self) -> None:
        values = np.array([[1.0, 2.0], [1.0, 2.0], [1.0, 2.0]])
        entropy = normalized_discrete_entropy(values, bins=10, value_min=0.0, value_max=5.0)
        self.assertTrue(np.allclose(entropy, [0.0, 0.0]))

    def test_spread_ensemble_has_positive_normalized_entropy(self) -> None:
        values = np.array([[0.1], [0.3], [0.5], [0.7], [0.9]])
        entropy = normalized_discrete_entropy(values, bins=5, value_min=0.0, value_max=1.0)
        self.assertGreater(float(entropy[0]), 0.9)
        self.assertLessEqual(float(entropy[0]), 1.0)


if __name__ == "__main__":
    unittest.main()
