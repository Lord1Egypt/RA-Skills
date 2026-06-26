import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "compute_code800.py"

# Real declaration used as an integration fixture. The path is committed; the file
# and its contents are not. Tests skip where the file is absent.
FIXTURE = Path(
    "/home/fredj/Dropbox/private/tax/VaudTax2025/"
    "CTB55813603_PF2025_5HBACH-DKCL1J_2026-03-31.vaudtax"
)


@unittest.skipUnless(FIXTURE.exists(), f"fixture not present: {FIXTURE}")
class TestComputeContext(unittest.TestCase):
    def _json(self):
        out = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE), "--json"],
            capture_output=True, text=True, check=True,
        )
        return json.loads(out.stdout)

    def test_json_includes_commune_and_marital_status(self):
        data = self._json()
        self.assertIn("commune", data)
        self.assertIn("marital_status", data)

    def test_context_values_are_populated(self):
        data = self._json()
        self.assertTrue(data["commune"])
        self.assertTrue(data["marital_status"])


if __name__ == "__main__":
    unittest.main()
