import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class KickoffAlertsCliTests(unittest.TestCase):
    def run_cli(self, payload, *minutes_before, timezone="Asia/Hong_Kong"):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "matches.json"
            input_path.write_text(json.dumps(payload), encoding="utf-8")
            command = [
                sys.executable,
                str(ROOT / "scripts" / "kickoff_alerts.py"),
                "--input",
                str(input_path),
                "--timezone",
                timezone,
            ]
            if minutes_before:
                command.append("--minutes-before")
                command.extend(str(value) for value in minutes_before)
            result = subprocess.run(command, capture_output=True, text=True)
            return result

    def test_default_offset_supports_single_match_object_input(self):
        payload = {
            "match": "Argentina vs Netherlands",
            "teams": ["Argentina", "Netherlands"],
            "kickoff": "2026-07-19T20:00:00+00:00",
        }

        result = self.run_cli(payload)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        alerts = json.loads(result.stdout)["alerts"]
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["match"], "Argentina vs Netherlands")
        self.assertEqual(alerts[0]["kickoff"], "2026-07-20T04:00+08:00")
        self.assertEqual(alerts[0]["alert_at"], "2026-07-20T03:50+08:00")
        self.assertEqual(alerts[0]["label"], "T-10min")
        self.assertIn("$world-cup-2026-predictor", alerts[0]["prompt"])
        self.assertNotIn("$world-cup-odds-forecaster", alerts[0]["prompt"])

    def test_four_alert_mode_emits_expected_labels_and_chronological_order(self):
        payload = {
            "matches": [
                {
                    "match": "Argentina vs Netherlands",
                    "kickoff": "2026-07-19T20:00:00+00:00",
                }
            ]
        }

        result = self.run_cli(payload, 190, 130, 70, 10)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        alerts = json.loads(result.stdout)["alerts"]
        self.assertEqual(
            [alert["label"] for alert in alerts],
            ["T-3h10", "T-2h10", "T-1h10", "T-10min"],
        )
        self.assertEqual(
            [alert["alert_at"] for alert in alerts],
            [
                "2026-07-20T00:50+08:00",
                "2026-07-20T01:50+08:00",
                "2026-07-20T02:50+08:00",
                "2026-07-20T03:50+08:00",
            ],
        )
        self.assertTrue(all("$world-cup-2026-predictor" in alert["prompt"] for alert in alerts))
        self.assertTrue(all("$world-cup-odds-forecaster" not in alert["prompt"] for alert in alerts))

    def test_multiple_matches_and_offsets_are_sorted_deterministically(self):
        payload = [
            {
                "match": "Argentina vs Netherlands",
                "kickoff": "2026-07-19T12:00:00+00:00",
            },
            {
                "match": "Brazil vs France",
                "kickoff": "2026-07-19T13:00:00+00:00",
            },
        ]

        result = self.run_cli(payload, 70, 10, timezone="UTC")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        alerts = json.loads(result.stdout)["alerts"]
        self.assertEqual(
            [(alert["alert_at"], alert["match"], alert["label"]) for alert in alerts],
            [
                ("2026-07-19T10:50+00:00", "Argentina vs Netherlands", "T-1h10"),
                ("2026-07-19T11:50+00:00", "Argentina vs Netherlands", "T-10min"),
                ("2026-07-19T11:50+00:00", "Brazil vs France", "T-1h10"),
                ("2026-07-19T12:50+00:00", "Brazil vs France", "T-10min"),
            ],
        )

    def test_minutes_before_must_be_positive(self):
        payload = {
            "match": "Argentina vs Netherlands",
            "kickoff": "2026-07-19T20:00:00+00:00",
        }

        result = self.run_cli(payload, 10, 0, -5)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("positive integers", result.stderr)

    def test_invalid_timezone_fails_without_traceback(self):
        payload = {
            "match": "Argentina vs Netherlands",
            "kickoff": "2026-07-19T20:00:00+00:00",
        }

        result = self.run_cli(payload, timezone="Mars/Olympus")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())
        self.assertNotIn("traceback", result.stderr.lower())

    def test_naive_kickoff_is_rejected(self):
        payload = {
            "match": "Argentina vs Netherlands",
            "kickoff": "2026-07-19T20:00:00",
        }

        result = self.run_cli(payload)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("explicit timezone", result.stderr.lower())
        self.assertNotIn("traceback", result.stderr.lower())

    def test_dst_fallback_alerts_are_sorted_by_real_time(self):
        payload = [
            {
                "match": "Before fallback",
                "kickoff": "2026-11-01T05:40:00+00:00",
            },
            {
                "match": "After fallback",
                "kickoff": "2026-11-01T06:20:00+00:00",
            },
        ]

        result = self.run_cli(payload, 10, timezone="America/New_York")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        alerts = json.loads(result.stdout)["alerts"]
        self.assertEqual([alert["match"] for alert in alerts], ["Before fallback", "After fallback"])
        self.assertEqual(alerts[0]["alert_at"], "2026-11-01T01:30-04:00")
        self.assertEqual(alerts[1]["alert_at"], "2026-11-01T01:10-05:00")

    def test_offset_is_subtracted_on_absolute_timeline_across_dst(self):
        payload = {
            "match": "After fallback",
            "kickoff": "2026-11-01T07:20:00+00:00",
        }

        result = self.run_cli(payload, 70, timezone="America/New_York")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        alert = json.loads(result.stdout)["alerts"][0]
        self.assertEqual(alert["kickoff"], "2026-11-01T02:20-05:00")
        self.assertEqual(alert["alert_at"], "2026-11-01T01:10-05:00")


if __name__ == "__main__":
    unittest.main()
