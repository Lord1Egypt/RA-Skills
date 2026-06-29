#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from probabilistic_sampling import generate_monte_carlo_parameter_sets  # noqa: E402


class ProbabilisticSamplingTests(unittest.TestCase):
    def test_generate_reproducible_lognormal_and_truncnorm_samples(self) -> None:
        space = {
            "parameters": {
                "ks": {"distribution": "lognormal", "median": 6.5, "p05": 3.0, "p95": 10.0, "precision": 4},
                "theta": {"distribution": "truncnorm", "mean": 0.45, "p05": 0.39, "p95": 0.51, "clip_min": 0.2, "clip_max": 0.6},
            }
        }
        trials_a = generate_monte_carlo_parameter_sets(space, samples=5, seed=42)
        trials_b = generate_monte_carlo_parameter_sets(space, samples=5, seed=42)
        self.assertEqual(trials_a, trials_b)
        self.assertEqual(len(trials_a), 5)
        self.assertTrue(all(0.2 <= trial["params"]["theta"] <= 0.6 for trial in trials_a))

    def test_bind_and_greater_than_constraints(self) -> None:
        space = {
            "parameters": {
                "ks": {"distribution": "uniform", "min": 3.0, "max": 3.0},
                "fc": {"distribution": "uniform", "min": 0.0, "max": 0.0},
                "f0": {"distribution": "uniform", "min": 5.0, "max": 5.0},
            },
            "constraints": [
                {"type": "bind", "target": "fc", "source": "ks"},
                {"type": "greater_than", "left": "f0", "right": "fc"},
            ],
        }
        trials = generate_monte_carlo_parameter_sets(space, samples=2, seed=7)
        self.assertEqual([trial["params"]["fc"] for trial in trials], [3.0, 3.0])


if __name__ == "__main__":
    unittest.main()
