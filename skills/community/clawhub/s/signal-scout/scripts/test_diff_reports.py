#!/usr/bin/env python3
"""Regression tests for diff_reports.py's cross-run novelty tracking.

Run: python3 test_diff_reports.py    (stdlib only)

These exist because the original diff_reports.py compared exactly two
snapshots — immediately-previous vs current. That undercounts staleness: a
prospect seen in run 1, absent from run 2, then resurfacing in run 3 would
read as "new" again if you only ever diff run 2 against run 3, even though
run 1 already saw them. The invariant this defends: "new" means never seen
in ANY prior snapshot passed in, not just absent from the last one.
"""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import diff_reports


def individual(name: str, source_url: str, score: int = 70, pain_signal: str = "some pain") -> dict:
    return {"name": name, "source_url": source_url, "score": score, "pain_signal": pain_signal}


def snapshot(generated_at: str, individuals: list[dict], patterns: list[dict] | None = None) -> dict:
    return {"generated_at": generated_at, "individuals": individuals, "patterns": patterns or []}


def run_diff(paths: list[Path], extra_args: list[str] | None = None) -> dict:
    argv = ["diff_reports.py", *[str(p) for p in paths], "--json", *(extra_args or [])]
    buf = io.StringIO()
    with mock.patch.object(sys, "argv", argv), redirect_stdout(buf):
        diff_reports.main()
    return json.loads(buf.getvalue())


def names(items: list[dict]) -> set[str]:
    return {item["name"] for item in items}


class TestCumulativeHistory(unittest.TestCase):
    def test_prospect_missing_one_run_then_resurfacing_is_recurring_not_new(self):
        """The core bug: seen in run 1, absent run 2, back in run 3 — must not read as new."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            run1 = tmp_path / "run1.json"
            run2 = tmp_path / "run2.json"
            run3 = tmp_path / "run3.json"
            run1.write_text(json.dumps(snapshot("2026-06-01", [individual("Alex Chen", "https://example.com/a")])))
            run2.write_text(json.dumps(snapshot("2026-06-08", [individual("Sam Lee", "https://example.com/b")])))
            run3.write_text(json.dumps(snapshot("2026-06-15", [
                individual("Alex Chen", "https://example.com/a"),
                individual("Sam Lee", "https://example.com/b"),
            ])))

            result = run_diff([run1, run2, run3])

            self.assertNotIn("Alex Chen", names(result["new_prospects"]))
            self.assertIn("Alex Chen", names(result["recurring_prospects"]))

    def test_prospect_never_seen_before_is_new(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            run1 = tmp_path / "run1.json"
            run2 = tmp_path / "run2.json"
            run1.write_text(json.dumps(snapshot("2026-06-01", [individual("Alex Chen", "https://example.com/a")])))
            run2.write_text(json.dumps(snapshot("2026-06-08", [
                individual("Alex Chen", "https://example.com/a"),
                individual("Jordan Kim", "https://example.com/c"),
            ])))

            result = run_diff([run1, run2])

            self.assertIn("Jordan Kim", names(result["new_prospects"]))
            self.assertIn("Alex Chen", names(result["recurring_prospects"]))

    def test_dropped_is_relative_to_immediately_prior_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            run1 = tmp_path / "run1.json"
            run2 = tmp_path / "run2.json"
            run3 = tmp_path / "run3.json"
            run1.write_text(json.dumps(snapshot("2026-06-01", [individual("Alex Chen", "https://example.com/a")])))
            run2.write_text(json.dumps(snapshot("2026-06-08", [individual("Alex Chen", "https://example.com/a")])))
            run3.write_text(json.dumps(snapshot("2026-06-15", [])))

            result = run_diff([run1, run2, run3])

            self.assertIn("Alex Chen", names(result["dropped_prospects"]))

    def test_argument_order_does_not_matter_sorted_by_generated_at(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            run1 = tmp_path / "run1.json"
            run2 = tmp_path / "run2.json"
            run1.write_text(json.dumps(snapshot("2026-06-01", [individual("Alex Chen", "https://example.com/a")])))
            run2.write_text(json.dumps(snapshot("2026-06-08", [
                individual("Alex Chen", "https://example.com/a"),
                individual("Jordan Kim", "https://example.com/c"),
            ])))

            forward = run_diff([run1, run2])
            backward = run_diff([run2, run1])

            self.assertEqual(names(forward["new_prospects"]), names(backward["new_prospects"]))
            self.assertIn("Jordan Kim", names(forward["new_prospects"]))

    def test_two_snapshot_call_still_works(self):
        """Backward compatibility: the original previous/current 2-arg call shape."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            previous = tmp_path / "previous.json"
            current = tmp_path / "current.json"
            previous.write_text(json.dumps(snapshot("2026-06-01", [individual("Alex Chen", "https://example.com/a")])))
            current.write_text(json.dumps(snapshot("2026-06-08", [individual("Jordan Kim", "https://example.com/c")])))

            result = run_diff([previous, current])

            self.assertIn("Jordan Kim", names(result["new_prospects"]))
            self.assertIn("Alex Chen", names(result["dropped_prospects"]))

    def test_grown_patterns_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            previous = tmp_path / "previous.json"
            current = tmp_path / "current.json"
            previous.write_text(json.dumps(snapshot("2026-06-01", [], [{"title": "Manual spreadsheet pain", "count": 3}])))
            current.write_text(json.dumps(snapshot("2026-06-08", [], [{"title": "Manual spreadsheet pain", "count": 7}])))

            result = run_diff([previous, current])

            self.assertEqual(len(result["grown_patterns"]), 1)
            self.assertEqual(result["grown_patterns"][0]["previous_count"], 3)
            self.assertEqual(result["grown_patterns"][0]["current_count"], 7)


class TestOutcomeCrossReference(unittest.TestCase):
    def test_resurfacing_prospect_with_logged_outcome_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            previous = tmp_path / "previous.json"
            current = tmp_path / "current.json"
            outcomes = tmp_path / "outcomes.jsonl"
            previous.write_text(json.dumps(snapshot("2026-06-01", [individual("Alex Chen", "https://example.com/a")])))
            current.write_text(json.dumps(snapshot("2026-06-08", [individual("Alex Chen", "https://example.com/a")])))
            outcomes.write_text(json.dumps({
                "name": "Alex Chen", "type": "individual", "outcome": "no_reply",
                "date": "2026-06-03", "source_url": "https://example.com/a",
            }) + "\n")

            result = run_diff([previous, current], ["--outcomes", str(outcomes)])

            recurring = result["recurring_prospects"]
            self.assertEqual(len(recurring), 1)
            self.assertIn("no_reply", recurring[0]["_prior_outcome"])

    def test_outcome_match_prefers_source_url_over_name_only(self):
        """Same name, two different prospects — the source_url-tagged outcome must not bleed onto the wrong one."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            previous = tmp_path / "previous.json"
            current = tmp_path / "current.json"
            outcomes = tmp_path / "outcomes.jsonl"
            previous.write_text(json.dumps(snapshot("2026-06-01", [
                individual("Alex Chen", "https://example.com/pricing-thread"),
                individual("Alex Chen", "https://example.com/onboarding-thread"),
            ])))
            current.write_text(json.dumps(snapshot("2026-06-08", [
                individual("Alex Chen", "https://example.com/pricing-thread"),
                individual("Alex Chen", "https://example.com/onboarding-thread"),
            ])))
            outcomes.write_text(json.dumps({
                "name": "Alex Chen", "type": "individual", "outcome": "converted",
                "date": "2026-06-03", "source_url": "https://example.com/pricing-thread",
            }) + "\n")

            result = run_diff([previous, current], ["--outcomes", str(outcomes)])

            by_url = {item["source_url"]: item for item in result["recurring_prospects"]}
            self.assertIn("converted", by_url["https://example.com/pricing-thread"]["_prior_outcome"])
            self.assertNotIn("_prior_outcome", by_url["https://example.com/onboarding-thread"])

    def test_no_outcomes_file_is_a_silent_noop(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            previous = tmp_path / "previous.json"
            current = tmp_path / "current.json"
            previous.write_text(json.dumps(snapshot("2026-06-01", [individual("Alex Chen", "https://example.com/a")])))
            current.write_text(json.dumps(snapshot("2026-06-08", [individual("Alex Chen", "https://example.com/a")])))

            result = run_diff([previous, current], ["--outcomes", str(tmp_path / "missing.jsonl")])

            self.assertNotIn("_prior_outcome", result["recurring_prospects"][0])


if __name__ == "__main__":
    unittest.main()
