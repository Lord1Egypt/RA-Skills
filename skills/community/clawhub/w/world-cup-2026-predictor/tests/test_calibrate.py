from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import calibrate


class CalibrationMetricsTests(unittest.TestCase):
    def make_record(self, **overrides):
        record = {
            "probabilities_90m": {"home": 0.60, "draw": 0.25, "away": 0.15},
            "outcome_90m": "home",
            "bucket": "world_cup|1x2",
        }
        record.update(overrides)
        return record

    def test_brier_and_log_loss(self):
        probs = {"home": 0.60, "draw": 0.25, "away": 0.15}
        self.assertAlmostEqual(calibrate.multiclass_brier(probs, "home"), 0.245)
        self.assertAlmostEqual(calibrate.log_loss(probs, "home"), 0.5108256, places=6)

    def test_build_report_includes_metrics_and_thresholds(self):
        records = [
            {
                "probabilities_90m": {"home": 0.60, "draw": 0.25, "away": 0.15},
                "outcome_90m": "home",
                "bucket": "world_cup|1x2",
                "confidence": {"label": "high"},
                "btts": {"yes": 0.62, "no": 0.38},
                "outcome_btts": "yes",
                "totals": [
                    {
                        "line": 2.5,
                        "model_probabilities": {"over": 0.58, "under": 0.42},
                    }
                ],
                "outcome_totals": {"2.5": "over"},
                "expected_goals": {"home": 1.40, "away": 0.80},
                "actual_score": {"home": 2, "away": 1},
                "closing_consensus_90m": {"home": 0.56, "draw": 0.27, "away": 0.17},
            },
            {
                "probabilities_90m": {"home": 0.40, "draw": 0.35, "away": 0.25},
                "outcome_90m": "draw",
                "bucket": "world_cup|1x2",
                "confidence_bucket": "medium",
            },
        ]

        report = calibrate.build_report(records)

        self.assertEqual(report["valid_records"], 2)
        self.assertEqual(report["invalid_records"], 0)
        self.assertFalse(report["weight_change_eligible"])
        self.assertEqual(report["minimum_overall_sample"], 100)
        self.assertEqual(report["minimum_bucket_sample"], 30)
        self.assertEqual(report["sample_eligibility"]["eligible_buckets"], [])
        self.assertAlmostEqual(report["metrics"]["1x2"]["brier"], (0.245 + 0.645) / 2.0)
        self.assertAlmostEqual(report["metrics"]["1x2"]["log_loss"], (-math.log(0.60) - math.log(0.35)) / 2.0)
        self.assertAlmostEqual(report["metrics"]["1x2"]["top_pick_accuracy"], 0.5)
        self.assertAlmostEqual(report["metrics"]["btts"]["brier"], (1.0 - 0.62) ** 2)
        self.assertAlmostEqual(report["metrics"]["totals"]["brier"], (1.0 - 0.58) ** 2)
        self.assertAlmostEqual(report["score_mae"]["home"], 0.6)
        self.assertAlmostEqual(report["score_mae"]["away"], 0.2)
        self.assertAlmostEqual(report["score_mae"]["total"], 0.4)
        self.assertEqual(report["confidence_bucket_calibration"]["high"]["count"], 1)
        self.assertEqual(report["confidence_bucket_calibration"]["medium"]["count"], 1)
        self.assertAlmostEqual(report["confidence_bucket_calibration"]["high"]["top_pick_accuracy"], 1.0)
        self.assertAlmostEqual(report["confidence_bucket_calibration"]["medium"]["top_pick_accuracy"], 0.0)
        self.assertAlmostEqual(report["closing_consensus_movement"]["mean_absolute_delta_pp"], 4.0)

    def test_invalid_records_are_counted(self):
        report = calibrate.build_report(
            [
                {
                    "probabilities_90m": {"home": 0.70, "draw": 0.20, "away": 0.20},
                    "outcome_90m": "home",
                    "bucket": "world_cup|1x2",
                },
                {
                    "probabilities_90m": {"home": 0.55, "draw": 0.25, "away": 0.20},
                    "outcome_90m": "invalid",
                    "bucket": "world_cup|1x2",
                },
                {
                    "probabilities_90m": {"home": 0.55, "draw": 0.25, "away": 0.20},
                    "outcome_90m": "home",
                    "bucket": "world_cup|1x2",
                },
            ]
        )

        self.assertEqual(report["valid_records"], 1)
        self.assertEqual(report["invalid_records"], 2)

    def test_large_balanced_sample_marks_each_bucket_eligible(self):
        records = []
        for index in range(40):
            records.append(
                {
                    "probabilities_90m": {"home": 0.55, "draw": 0.25, "away": 0.20},
                    "outcome_90m": "home" if index % 2 == 0 else "draw",
                    "bucket": "world_cup|1x2",
                }
            )
        for index in range(30):
            records.append(
                {
                    "probabilities_90m": {"home": 0.45, "draw": 0.30, "away": 0.25},
                    "outcome_90m": "away" if index % 2 == 0 else "home",
                    "bucket": "league|1x2",
                }
            )
        for index in range(30):
            records.append(
                {
                    "probabilities_90m": {"home": 0.50, "draw": 0.28, "away": 0.22},
                    "outcome_90m": "draw" if index % 2 == 0 else "home",
                    "bucket": "knockout|1x2",
                }
            )

        report = calibrate.build_report(records)

        self.assertEqual(report["valid_records"], 100)
        self.assertTrue(report["weight_change_eligible"])
        self.assertEqual(
            report["sample_eligibility"]["bucket_weight_change_eligibility"],
            {
                "knockout|1x2": True,
                "league|1x2": True,
                "world_cup|1x2": True,
            },
        )
        self.assertEqual(
            report["sample_eligibility"]["eligible_buckets"],
            ["knockout|1x2", "league|1x2", "world_cup|1x2"],
        )

    def test_bucket_eligibility_is_independent_after_overall_threshold(self):
        records = []
        for index in range(95):
            records.append(
                self.make_record(
                    probabilities_90m={"home": 0.55, "draw": 0.25, "away": 0.20},
                    outcome_90m="home" if index % 2 == 0 else "draw",
                    bucket="world_cup|1x2",
                )
            )
        for index in range(5):
            records.append(
                self.make_record(
                    probabilities_90m={"home": 0.45, "draw": 0.30, "away": 0.25},
                    outcome_90m="away" if index % 2 == 0 else "home",
                    bucket="league|1x2",
                )
            )

        report = calibrate.build_report(records)

        self.assertEqual(report["valid_records"], 100)
        self.assertTrue(report["weight_change_eligible"])
        self.assertEqual(
            report["sample_eligibility"]["bucket_weight_change_eligibility"],
            {"league|1x2": False, "world_cup|1x2": True},
        )
        self.assertEqual(report["sample_eligibility"]["eligible_buckets"], ["world_cup|1x2"])

    def test_four_alerts_for_one_match_count_as_one_distinct_sample(self):
        records = []
        for event in range(25):
            for offset in ("T-3h10", "T-2h10", "T-1h10", "T-10min"):
                records.append(
                    self.make_record(
                        event_id=f"event-{event}",
                        forecast_id=f"forecast-{event}-{offset}",
                        alert_offset=offset,
                        as_of=f"2026-07-{(event % 9) + 1:02d}T0{(event % 4)}:00:00+00:00",
                        kickoff=f"2026-07-{(event % 9) + 1:02d}T04:00:00+00:00",
                        bucket="world_cup|1x2",
                    )
                )

        report = calibrate.build_report(records)

        self.assertEqual(report["valid_records"], 100)
        self.assertEqual(report["distinct_matches"], 25)
        self.assertFalse(report["weight_change_eligible"])
        self.assertEqual(report["sample_eligibility"]["distinct_matches"], 25)
        self.assertEqual(report["sample_eligibility"]["bucket_samples"], {"world_cup|1x2": 25})
        self.assertEqual(
            {offset: metrics["count"] for offset, metrics in report["alert_offset_diagnostics"].items()},
            {"T-10min": 25, "T-1h10": 25, "T-2h10": 25, "T-3h10": 25},
        )

    def test_latest_valid_snapshot_is_primary_evolution_record(self):
        grouped = calibrate.primary_event_records(
            [
                self.make_record(
                    event_id="e1",
                    forecast_id="forecast-1",
                    alert_offset="T-3h10",
                    as_of="2026-07-10T00:50:00Z",
                    kickoff="2026-07-10T04:00:00Z",
                ),
                self.make_record(
                    event_id="e1",
                    forecast_id="forecast-2",
                    alert_offset="T-10min",
                    as_of="2026-07-10T03:50:00Z",
                    kickoff="2026-07-10T04:00:00Z",
                ),
            ]
        )

        self.assertEqual(len(grouped), 1)
        self.assertEqual(grouped[0]["alert_offset"], "T-10min")

    def test_pre_kickoff_snapshot_beats_later_post_kickoff_snapshot(self):
        grouped = calibrate.primary_event_records(
            [
                self.make_record(
                    event_id="e1",
                    forecast_id="forecast-1",
                    alert_offset="T-10min",
                    as_of="2026-07-10T03:50:00Z",
                    kickoff="2026-07-10T04:00:00Z",
                ),
                self.make_record(
                    event_id="e1",
                    forecast_id="forecast-2",
                    alert_offset="post",
                    as_of="2026-07-10T04:05:00Z",
                    kickoff="2026-07-10T04:00:00Z",
                ),
            ]
        )

        self.assertEqual(len(grouped), 1)
        self.assertEqual(grouped[0]["forecast_id"], "forecast-1")

    def test_modern_event_with_only_post_kickoff_snapshots_is_excluded_from_distinct_gates(self):
        records = [
            self.make_record(
                event_id="e1",
                forecast_id="forecast-1",
                alert_offset="post-1",
                as_of="2026-07-10T04:05:00Z",
                kickoff="2026-07-10T04:00:00Z",
            ),
            self.make_record(
                event_id="e1",
                forecast_id="forecast-2",
                alert_offset="post-2",
                as_of="2026-07-10T04:06:00Z",
                kickoff="2026-07-10T04:00:00Z",
            ),
        ]

        self.assertEqual(calibrate.primary_event_records(records), [])

        report = calibrate.build_report(records)

        self.assertEqual(report["valid_records"], 2)
        self.assertEqual(report["distinct_matches"], 0)
        self.assertEqual(report["sample_eligibility"]["bucket_samples"], {})
        self.assertEqual(report["sample_eligibility"]["excluded_valid_records_from_distinct_gates"], 2)

    def test_modern_event_with_missing_timestamps_is_excluded_from_distinct_gates(self):
        records = [
            self.make_record(
                event_id="e1",
                forecast_id="forecast-1",
                alert_offset="missing-as-of",
                as_of=None,
                kickoff="2026-07-10T04:00:00Z",
            ),
            self.make_record(
                event_id="e1",
                forecast_id="forecast-2",
                alert_offset="missing-kickoff",
                as_of="2026-07-10T03:50:00Z",
                kickoff=None,
            ),
        ]

        self.assertEqual(calibrate.primary_event_records(records), [])

        report = calibrate.build_report(records)

        self.assertEqual(report["valid_records"], 2)
        self.assertEqual(report["distinct_matches"], 0)
        self.assertEqual(report["sample_eligibility"]["excluded_valid_records_from_distinct_gates"], 2)

    def test_parse_timestamp_rejects_timezone_naive_values(self):
        self.assertIsNone(calibrate._parse_timestamp("2026-07-10T03:50:00"))

    def test_modern_event_with_timezone_naive_timestamps_is_excluded_from_distinct_gates(self):
        records = [
            self.make_record(
                event_id="e1",
                forecast_id="forecast-1",
                alert_offset="naive",
                as_of="2026-07-10T03:50:00",
                kickoff="2026-07-10T04:00:00",
            )
        ]

        self.assertEqual(calibrate.primary_event_records(records), [])

        report = calibrate.build_report(records)

        self.assertEqual(report["valid_records"], 1)
        self.assertEqual(report["distinct_matches"], 0)
        self.assertEqual(report["sample_eligibility"]["excluded_valid_records_from_distinct_gates"], 1)

    def test_modern_event_at_exact_kickoff_is_excluded_from_distinct_gates(self):
        records = [
            self.make_record(
                event_id="e1",
                forecast_id="forecast-1",
                alert_offset="kickoff",
                as_of="2026-07-10T04:00:00Z",
                kickoff="2026-07-10T04:00:00Z",
            )
        ]

        self.assertEqual(calibrate.primary_event_records(records), [])

        report = calibrate.build_report(records)

        self.assertEqual(report["valid_records"], 1)
        self.assertEqual(report["distinct_matches"], 0)
        self.assertEqual(report["sample_eligibility"]["excluded_valid_records_from_distinct_gates"], 1)

    def test_invalid_records_do_not_contribute_to_distinct_match_gates(self):
        report = calibrate.build_report(
            [
                self.make_record(
                    event_id="e1",
                    forecast_id="forecast-1",
                    alert_offset="T-10min",
                    as_of="2026-07-10T03:50:00Z",
                    kickoff="2026-07-10T04:00:00Z",
                ),
                self.make_record(
                    event_id="e1",
                    forecast_id="forecast-2",
                    alert_offset="T-3h10",
                    as_of="2026-07-10T00:50:00Z",
                    kickoff="2026-07-10T04:00:00Z",
                    probabilities_90m={"home": 0.70, "draw": 0.20, "away": 0.20},
                ),
            ]
        )

        self.assertEqual(report["valid_records"], 1)
        self.assertEqual(report["invalid_records"], 1)
        self.assertEqual(report["distinct_matches"], 1)
        self.assertEqual(report["sample_eligibility"]["bucket_samples"], {"world_cup|1x2": 1})

    def test_legacy_records_without_ids_remain_independently_unique(self):
        records = []
        for index in range(100):
            records.append(
                self.make_record(
                    bucket="world_cup|1x2",
                    probabilities_90m={"home": 0.55, "draw": 0.25, "away": 0.20},
                    outcome_90m="home" if index % 2 == 0 else "draw",
                    event_id=None,
                    forecast_id=None,
                    alert_offset="legacy",
                    as_of=None,
                )
            )

        report = calibrate.build_report(records)

        self.assertEqual(report["valid_records"], 100)
        self.assertEqual(report["distinct_matches"], 100)
        self.assertTrue(report["weight_change_eligible"])
        self.assertEqual(report["sample_eligibility"]["bucket_samples"], {"world_cup|1x2": 100})

    def test_primary_event_records_keeps_legacy_records_without_timestamps(self):
        grouped = calibrate.primary_event_records(
            [
                self.make_record(event_id=None, forecast_id=None, as_of=None, kickoff=None, alert_offset="legacy-1"),
                self.make_record(event_id=None, forecast_id=None, as_of=None, kickoff=None, alert_offset="legacy-2"),
            ]
        )

        self.assertEqual([record["alert_offset"] for record in grouped], ["legacy-1", "legacy-2"])

    def test_score_distribution_metrics_are_reported(self):
        report = calibrate.build_report(
            [
                self.make_record(
                    actual_score={"home": 1, "away": 0},
                    score_distribution={"1-0": 0.6, "0-0": 0.4},
                )
            ]
        )

        self.assertEqual(report["metrics"]["score_distribution"]["count"], 1)
        self.assertAlmostEqual(report["metrics"]["score_distribution"]["brier"], 0.32)
        self.assertAlmostEqual(report["metrics"]["score_distribution"]["log_loss"], -math.log(0.6))

    def test_totals_lines_must_match_exactly_in_both_directions(self):
        report = calibrate.build_report(
            [
                self.make_record(
                    totals=[
                        {
                            "line": 2.5,
                            "model_probabilities": {"over": 0.58, "under": 0.42},
                        }
                    ],
                    outcome_totals={"3.5": "over"},
                )
            ]
        )

        self.assertEqual(report["valid_records"], 0)
        self.assertEqual(report["invalid_records"], 1)
        self.assertEqual(report["metrics"]["1x2"]["count"], 0)

    def test_duplicate_normalized_outcome_totals_keys_are_invalid(self):
        report = calibrate.build_report(
            [
                self.make_record(
                    totals=[
                        {
                            "line": 2.5,
                            "model_probabilities": {"over": 0.58, "under": 0.42},
                        }
                    ],
                    outcome_totals={"2.5": "over", "2.50": "under"},
                )
            ]
        )

        self.assertEqual(report["valid_records"], 0)
        self.assertEqual(report["invalid_records"], 1)
        self.assertEqual(report["metrics"]["totals"]["count"], 0)

    def test_totals_entries_require_exactly_one_probability_source(self):
        report = calibrate.build_report(
            [
                self.make_record(
                    totals=[
                        {
                            "line": 2.5,
                            "model_probabilities": {"over": 0.58, "under": 0.42},
                            "probabilities": {"over": 0.57, "under": 0.43},
                        }
                    ],
                    outcome_totals={"2.5": "over"},
                )
            ]
        )

        self.assertEqual(report["valid_records"], 0)
        self.assertEqual(report["invalid_records"], 1)
        self.assertEqual(report["metrics"]["1x2"]["count"], 0)

    def test_confidence_bucket_and_label_must_match_when_both_supplied(self):
        report = calibrate.build_report(
            [
                self.make_record(
                    confidence_bucket="high",
                    confidence={"label": "medium"},
                )
            ]
        )

        self.assertEqual(report["valid_records"], 0)
        self.assertEqual(report["invalid_records"], 1)
        self.assertEqual(report["confidence_bucket_calibration"], {})

    def test_malformed_optional_fields_do_not_partially_contribute(self):
        report = calibrate.build_report(
            [
                self.make_record(confidence_bucket="high"),
                self.make_record(
                    confidence_bucket="medium",
                    btts={"yes": 0.70},
                    outcome_btts="yes",
                ),
            ]
        )

        self.assertEqual(report["valid_records"], 1)
        self.assertEqual(report["invalid_records"], 1)
        self.assertEqual(report["metrics"]["1x2"]["count"], 1)
        self.assertEqual(report["sample_eligibility"]["bucket_samples"], {"world_cup|1x2": 1})
        self.assertEqual(report["confidence_bucket_calibration"]["high"]["count"], 1)
        self.assertNotIn("medium", report["confidence_bucket_calibration"])

    def test_bool_optional_probability_does_not_partially_contribute(self):
        report = calibrate.build_report(
            [
                self.make_record(confidence_bucket="high"),
                self.make_record(
                    confidence_bucket="medium",
                    btts={"yes": True, "no": 0.0},
                    outcome_btts="yes",
                ),
            ]
        )

        self.assertEqual(report["valid_records"], 1)
        self.assertEqual(report["invalid_records"], 1)
        self.assertEqual(report["metrics"]["1x2"]["count"], 1)
        self.assertEqual(report["metrics"]["btts"]["count"], 0)
        self.assertEqual(report["sample_eligibility"]["bucket_samples"], {"world_cup|1x2": 1})
        self.assertEqual(report["confidence_bucket_calibration"]["high"]["count"], 1)
        self.assertNotIn("medium", report["confidence_bucket_calibration"])

    def test_bool_actual_score_does_not_partially_contribute(self):
        report = calibrate.build_report(
            [
                self.make_record(confidence_bucket="high"),
                self.make_record(
                    confidence_bucket="medium",
                    expected_goals={"home": 1.4, "away": 0.8},
                    actual_score={"home": True, "away": 1},
                ),
            ]
        )

        self.assertEqual(report["valid_records"], 1)
        self.assertEqual(report["invalid_records"], 1)
        self.assertEqual(report["metrics"]["1x2"]["count"], 1)
        self.assertIsNone(report["score_mae"])
        self.assertEqual(report["sample_eligibility"]["bucket_samples"], {"world_cup|1x2": 1})
        self.assertEqual(report["confidence_bucket_calibration"]["high"]["count"], 1)
        self.assertNotIn("medium", report["confidence_bucket_calibration"])

    def test_bool_totals_line_does_not_partially_contribute(self):
        report = calibrate.build_report(
            [
                self.make_record(confidence_bucket="high"),
                self.make_record(
                    confidence_bucket="medium",
                    totals=[
                        {
                            "line": True,
                            "model_probabilities": {"over": 0.58, "under": 0.42},
                        }
                    ],
                    outcome_totals={"1": "over"},
                ),
            ]
        )

        self.assertEqual(report["valid_records"], 1)
        self.assertEqual(report["invalid_records"], 1)
        self.assertEqual(report["metrics"]["1x2"]["count"], 1)
        self.assertEqual(report["metrics"]["totals"]["count"], 0)
        self.assertEqual(report["sample_eligibility"]["bucket_samples"], {"world_cup|1x2": 1})
        self.assertEqual(report["confidence_bucket_calibration"]["high"]["count"], 1)
        self.assertNotIn("medium", report["confidence_bucket_calibration"])


class CalibrationCliTests(unittest.TestCase):
    def test_cli_reads_jsonl_and_reports_invalid_records(self):
        rows = [
            json.dumps(
                {
                    "probabilities_90m": {"home": 0.60, "draw": 0.25, "away": 0.15},
                    "outcome_90m": "home",
                    "bucket": "world_cup|1x2",
                    "confidence_bucket": "high",
                }
            ),
            json.dumps(
                {
                    "probabilities_90m": {"home": 0.60, "draw": 0.25, "away": 0.25},
                    "outcome_90m": "home",
                    "bucket": "world_cup|1x2",
                }
            ),
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "completed.jsonl"
            path.write_text("\n".join(rows) + "\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "calibrate.py"), "--input", str(path)],
                check=True,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["valid_records"], 1)
        self.assertEqual(payload["invalid_records"], 1)

    def test_cli_missing_input_fails_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "missing.jsonl"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "calibrate.py"), "--input", str(path)],
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("error", result.stderr.lower())
        self.assertNotIn("traceback", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
