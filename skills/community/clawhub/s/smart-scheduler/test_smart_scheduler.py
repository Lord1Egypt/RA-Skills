import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class SmartSchedulerTests(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).parent
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_arg = ["--base-dir", self.temp_dir.name]

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_cli(self, *args):
        result = subprocess.run(
            [sys.executable, str(self.base_dir / "scripts" / "smart_scheduler.py"), *self.base_arg, *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_booking_flow_and_ics_export(self):
        created = self.run_cli(
            "create-request",
            "--title",
            "Weekly sync",
            "--organizer",
            "Mehul",
            "--timezone",
            "Europe/Berlin",
            "--duration-minutes",
            "30",
            "--participant",
            "Priya|telegram|@priya",
        )
        self.assertEqual(created["request"]["status"], "open")

        proposals = self.run_cli(
            "propose-slots",
            "--request-id",
            "1",
            "--slot",
            "2026-03-25T09:00|2026-03-25T09:30",
            "--slot",
            "2026-03-25T16:00|2026-03-25T16:30",
        )
        self.assertEqual(len(proposals["proposals"]), 2)

        booking = self.run_cli(
            "confirm-slot",
            "--request-id",
            "1",
            "--slot-id",
            "2",
            "--confirmed-by",
            "Priya",
        )
        self.assertEqual(booking["booking"]["proposal_id"], 2)

        output_path = Path(self.temp_dir.name) / "weekly-sync.ics"
        exported = self.run_cli("export-ics", "--request-id", "1", "--output", str(output_path))
        self.assertEqual(exported["output"], str(output_path))
        self.assertTrue(output_path.exists())
        self.assertIn("BEGIN:VCALENDAR", output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
