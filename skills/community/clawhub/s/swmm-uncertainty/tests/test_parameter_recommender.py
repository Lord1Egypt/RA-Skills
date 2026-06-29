from pathlib import Path
import sys
import tempfile
import unittest


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from parameter_recommender import recommend  # noqa: E402


class ParameterRecommenderTests(unittest.TestCase):
    def test_recommends_horton_and_routing_parameters(self) -> None:
        text = """
[OPTIONS]
INFILTRATION HORTON

[SUBCATCHMENTS]
S1 RG J1 1.0 50 100 1 0
S2 RG J2 1.0 0 100 1 0

[INFILTRATION]
S1 10 2 4 7 0
S2 10 2 4 7 0

[CONDUITS]
C1 J1 J2 10 0.011 0 0 0 0
"""
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "model.inp"
            inp.write_text(text, encoding="utf-8")
            result = recommend(inp)
        self.assertEqual(result["infiltration_method"], "horton")
        self.assertIn("MaxRate", result["recommended"])
        self.assertIn("Slope", result["recommended"])
        # Every non-core recommendation must carry a rationale.
        core = set(result["core_required"])
        for param in result["recommended"]:
            if param not in core:
                self.assertIn(param, result["rationale"])


if __name__ == "__main__":
    unittest.main()
