from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import monte_carlo_propagate as propagate  # noqa: E402


class MonteCarloPropagateTests(unittest.TestCase):
    def test_summary_statistics_handle_entropy_record(self) -> None:
        record = {"entropy": [0.0, 0.5, None, 1.0]}
        self.assertEqual(propagate.max_entropy(record), 1.0)
        self.assertAlmostEqual(propagate.mean_entropy(record), 0.5)

    def test_trial_out_paths_requires_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                propagate.trial_out_paths(Path(tmp))

    def test_plot_entropy_curves_writes_png(self) -> None:
        times = [f"1994-01-11 0{i}:00:00" for i in range(3)]
        records = {
            "J6": {"time": times, "entropy": [0.0, 0.5, 0.2]},
            "OUT_0": {"time": times, "entropy": [0.0, 0.2, 0.1]},
        }
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entropy.png"
            propagate.plot_entropy_curves(records, out)
            self.assertTrue(out.exists())
            self.assertGreater(out.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()

