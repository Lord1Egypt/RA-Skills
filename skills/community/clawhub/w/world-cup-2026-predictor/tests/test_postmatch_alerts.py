import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import postmatch_alerts


class PostmatchAlertTests(unittest.TestCase):
    def match(self, match_type="league_or_group"):
        return {
            "event_id": "arg-ned-2026",
            "match": "Argentina vs Netherlands",
            "teams": ["Argentina", "Netherlands"],
            "kickoff": "2026-07-12T22:30:00+08:00",
            "match_type": match_type,
        }

    def test_group_match_initial_check_is_kickoff_plus_135_minutes(self):
        alert = postmatch_alerts.build_alert(self.match("league_or_group"))

        self.assertEqual(alert["run_at"], "2026-07-13T00:45:00+08:00")

    def test_knockout_initial_check_is_kickoff_plus_165_minutes(self):
        alert = postmatch_alerts.build_alert(self.match("single_leg_knockout"))

        self.assertEqual(alert["run_at"], "2026-07-13T01:15:00+08:00")

    def test_retry_is_bounded_to_four_checks_at_fifteen_minute_intervals(self):
        retries = postmatch_alerts.retry_schedule(
            "2026-07-13T01:15:00+08:00", count=4
        )

        self.assertEqual(len(retries), 4)
        self.assertEqual(retries[-1], "2026-07-13T02:15:00+08:00")
        with self.assertRaisesRegex(ValueError, "between 0 and 4"):
            postmatch_alerts.retry_schedule(
                "2026-07-13T01:15:00+08:00", count=5
            )

    def test_prompt_requires_verified_sources_and_period_safe_review(self):
        prompt = postmatch_alerts.build_alert(self.match())["prompt"]

        self.assertIn("$world-cup-2026-predictor", prompt)
        self.assertIn("one official", prompt)
        self.assertIn("two agreeing independent", prompt)
        self.assertIn("score_90m", prompt)
        self.assertIn("score_after_extra_time", prompt)
        self.assertIn("penalties", prompt)
        self.assertIn("postmatch_review.py", prompt)
        self.assertIn("user's language", prompt)
        for status in ("postponed", "abandoned", "suspended"):
            self.assertIn(status, prompt)

    def test_unknown_match_type_and_naive_kickoff_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "match_type"):
            postmatch_alerts.build_alert(self.match("unknown"))

        match = self.match()
        match["kickoff"] = "2026-07-12T22:30:00"
        with self.assertRaisesRegex(ValueError, "explicit timezone"):
            postmatch_alerts.build_alert(match)

    def test_only_final_status_can_be_completed(self):
        self.assertTrue(postmatch_alerts.can_finalize("final"))
        for status in ("scheduled", "live", "postponed", "abandoned", "suspended"):
            self.assertFalse(postmatch_alerts.can_finalize(status))

    def test_absolute_timeline_is_used_across_dst_fallback(self):
        match = self.match()
        match["kickoff"] = "2026-11-01T00:30:00-04:00"
        alert = postmatch_alerts.build_alert(match, timezone_name="America/New_York")

        self.assertEqual(alert["run_at"], "2026-11-01T01:45:00-05:00")

    def test_retries_keep_absolute_time_across_dst_fallback(self):
        retries = postmatch_alerts.retry_schedule(
            "2026-11-01T01:30:00-04:00",
            count=2,
            timezone_name="America/New_York",
        )

        self.assertEqual(
            retries,
            ["2026-11-01T01:45:00-04:00", "2026-11-01T01:00:00-05:00"],
        )

    def test_initial_alert_keeps_absolute_time_across_dst_spring_forward(self):
        match = self.match()
        match["kickoff"] = "2026-03-08T00:30:00-05:00"
        alert = postmatch_alerts.build_alert(match, timezone_name="America/New_York")

        self.assertEqual(alert["run_at"], "2026-03-08T03:45:00-04:00")


class PostmatchAlertCliTests(unittest.TestCase):
    def run_cli(self, payload, *extra):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "matches.json"
            input_path.write_text(json.dumps(payload), encoding="utf-8")
            command = [
                sys.executable,
                str(ROOT / "scripts" / "postmatch_alerts.py"),
                "--input",
                str(input_path),
                *extra,
            ]
            return subprocess.run(command, capture_output=True, text=True)

    def test_cli_emits_initial_alert_and_bounded_retries(self):
        payload = {
            "match": "Argentina vs Netherlands",
            "kickoff": "2026-07-12T14:30:00+00:00",
            "match_type": "single_leg_knockout",
        }

        result = self.run_cli(payload, "--timezone", "Asia/Hong_Kong")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        alert = json.loads(result.stdout)["alerts"][0]
        self.assertEqual(alert["run_at"], "2026-07-13T01:15:00+08:00")
        self.assertEqual(len(alert["retry_at"]), 4)
        self.assertEqual(alert["retry_at"][-1], "2026-07-13T02:15:00+08:00")

    def test_cli_errors_do_not_emit_tracebacks(self):
        result = self.run_cli(
            {
                "match": "Argentina vs Netherlands",
                "kickoff": "2026-07-12T14:30:00+00:00",
                "match_type": "unknown",
            }
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())
        self.assertNotIn("traceback", result.stderr.lower())

    def test_cli_rejects_invalid_timezone_and_retry_count_without_tracebacks(self):
        payload = {
            "match": "Argentina vs Netherlands",
            "kickoff": "2026-07-12T14:30:00+00:00",
            "match_type": "league_or_group",
        }
        for arguments in (
            ("--timezone", "Mars/Olympus"),
            ("--retry-count", "5"),
            ("--retry-count", "-1"),
        ):
            with self.subTest(arguments=arguments):
                result = self.run_cli(payload, *arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("error", result.stderr.lower())
                self.assertNotIn("traceback", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
