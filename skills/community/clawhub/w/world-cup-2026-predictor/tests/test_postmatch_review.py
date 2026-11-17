import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import postmatch_review
import calibrate


def official_source():
    return {
        "name": "FIFA",
        "official": True,
        "observed_at": "2026-07-12T06:45:00+00:00",
        "url": "https://example.test/match/arg-sui",
    }


def make_forecast_record():
    return {
        "schema_version": "1.0",
        "forecast_id": "forecast-arg-sui-t10",
        "event_id": "arg-sui-2026",
        "teams": ["Argentina", "Switzerland"],
        "kickoff": "2026-07-12T03:00:00+00:00",
        "match_type": "single_leg_knockout",
        "as_of": "2026-07-12T02:50:00+00:00",
        "alert_offset": "T-10min",
        "markets": {
            "1x2": {
                "period": "90m",
                "probabilities": {"home": 0.58, "draw": 0.25, "away": 0.17},
                "pick": "home",
            },
            "qualification": {
                "period": "qualification",
                "probabilities": {"Argentina": 0.70, "Switzerland": 0.30},
                "favorite": "Argentina",
            },
            "totals": [
                {
                    "period": "90m",
                    "line": 2.5,
                    "model_probabilities": {"over": 0.56, "under": 0.44},
                    "pick": "over",
                }
            ],
            "btts": {
                "period": "90m",
                "probabilities": {"yes": 0.54, "no": 0.46},
                "pick": "yes",
            },
            "asian_handicap": [
                {
                    "period": "90m",
                    "home_line": -0.75,
                    "away_line": 0.75,
                    "model_probabilities": {"home": 0.55, "away": 0.45},
                    "pick": "home",
                }
            ],
            "correct_score": {
                "period": "90m",
                "displayed": [
                    {"score": "2-1", "probability": 0.12},
                    {"score": "1-1", "probability": 0.11},
                ],
            },
        },
        "probabilities_90m": {"home": 0.58, "draw": 0.25, "away": 0.17},
        "expected_goals": {"home": 1.7, "away": 0.9},
        "score_distribution_90m": {"2-1": 0.12, "1-1": 0.11, "0-0": 0.77},
        "confidence": {"label": "high", "score": 80},
        "profile_id": "v2-default",
    }


def argentina_result():
    return {
        "schema_version": "1.0",
        "status": "final",
        "event_id": "arg-sui-2026",
        "score_90m": {"home": 1, "away": 1},
        "score_after_extra_time": {"home": 3, "away": 1},
        "qualified": "Argentina",
        "sources": [official_source()],
    }


class SettlementRegressionTests(unittest.TestCase):
    def test_argentina_aet_score_cannot_settle_90m_markets(self):
        settled = postmatch_review.settle_forecast(make_forecast_record(), argentina_result())

        self.assertEqual(settled["1x2"]["period"], "90m")
        self.assertEqual(settled["1x2"]["outcome"], "draw")
        self.assertEqual(settled["1x2"]["pick_verdict"], "loss")
        self.assertEqual(settled["1x2"]["score_used"], {"home": 1, "away": 1})
        total = settled["totals"]["2.5"]
        self.assertEqual(total["period"], "90m")
        self.assertEqual(total["verdicts"]["over"], "loss")
        self.assertEqual(total["verdicts"]["under"], "win")
        self.assertEqual(total["score_used"], {"home": 1, "away": 1})
        self.assertEqual(settled["btts"]["outcome"], "yes")
        self.assertEqual(settled["qualification"]["period"], "qualification")
        self.assertEqual(settled["qualification"]["verdicts"]["Argentina"], "win")
        self.assertEqual(settled["qualification"]["pick_verdict"], "win")

    def test_actual_quarter_handicap_and_total_settlement(self):
        self.assertEqual(postmatch_review.settle_handicap("home", -0.75, 1, 0), "half_win")
        self.assertEqual(postmatch_review.settle_handicap("away", 0.75, 1, 0), "half_loss")
        self.assertEqual(postmatch_review.settle_total("over", 2.25, 1, 1), "half_loss")
        self.assertEqual(postmatch_review.settle_total("under", 2.25, 1, 1), "half_win")

    def test_integer_total_push_has_push_outcome(self):
        record = make_forecast_record()
        record["markets"]["totals"][0]["line"] = 2.0

        settled = postmatch_review.settle_forecast(record, argentina_result())

        self.assertEqual(settled["totals"]["2"]["outcome"], "push")
        self.assertEqual(
            settled["totals"]["2"]["verdicts"],
            {"over": "push", "under": "push"},
        )

    def test_missing_90m_score_never_falls_back_to_aet(self):
        result = argentina_result()
        result.pop("score_90m")

        with self.assertRaisesRegex(ValueError, "score_90m"):
            postmatch_review.validate_result(result)

    def test_event_identity_must_match_before_settlement(self):
        result = argentina_result()
        result["event_id"] = "different-event"

        with self.assertRaisesRegex(ValueError, "event_id"):
            postmatch_review.settle_forecast(make_forecast_record(), result)

    def test_market_period_mismatch_is_rejected(self):
        record = make_forecast_record()
        record["markets"]["totals"][0]["period"] = "qualification"

        with self.assertRaisesRegex(ValueError, "totals.*90m"):
            postmatch_review.settle_forecast(record, argentina_result())

    def test_correct_score_rejects_malformed_and_duplicate_entries(self):
        malformed = make_forecast_record()
        malformed["markets"]["correct_score"]["displayed"] = ["1-1"]
        with self.assertRaisesRegex(ValueError, r"correct_score.displayed\[0\].*object"):
            postmatch_review.settle_forecast(malformed, argentina_result())

        invalid_score = make_forecast_record()
        invalid_score["markets"]["correct_score"]["displayed"] = [{"score": "unknown"}]
        with self.assertRaisesRegex(ValueError, "home-away"):
            postmatch_review.settle_forecast(invalid_score, argentina_result())

        duplicate = make_forecast_record()
        duplicate["markets"]["correct_score"]["displayed"] = [
            {"score": "1-1"},
            {"score": "1-1"},
        ]
        with self.assertRaisesRegex(ValueError, "duplicate correct score"):
            postmatch_review.settle_forecast(duplicate, argentina_result())

    def test_pending_settlement_preserves_source_conflict_reason(self):
        result = argentina_result()
        result["sources"] = [
            {
                "name": "Provider A",
                "official": False,
                "reputable": True,
                "independent_id": "provider-a",
                "observed_at": "2026-07-12T06:46:00+00:00",
                "identifier": "provider-a-arg-sui",
                "score_90m": {"home": 1, "away": 1},
            },
            {
                "name": "Provider B",
                "official": False,
                "reputable": True,
                "independent_id": "provider-b",
                "observed_at": "2026-07-12T06:47:00+00:00",
                "identifier": "provider-b-arg-sui",
                "score_90m": {"home": 2, "away": 1},
            },
        ]

        pending = postmatch_review.settle_forecast(make_forecast_record(), result)

        self.assertEqual(pending["settlement_status"], "pending")
        self.assertEqual(pending["pending_reason"], "source_conflict")


class ResultValidationTests(unittest.TestCase):
    def test_final_result_accepts_official_source(self):
        result = postmatch_review.validate_result(argentina_result())

        self.assertEqual(result["status"], "final")
        self.assertEqual(result["settlement_status"], "ready")

    def test_nonofficial_result_requires_two_independent_agreeing_sources(self):
        result = argentina_result()
        result["sources"] = [
            {
                "name": "Provider A",
                "official": False,
                "reputable": True,
                "independent_id": "provider-a",
                "observed_at": "2026-07-12T06:46:00+00:00",
                "identifier": "provider-a-arg-sui",
                "score_90m": {"home": 1, "away": 1},
            },
            {
                "name": "Provider B",
                "official": False,
                "reputable": True,
                "independent_id": "provider-b",
                "observed_at": "2026-07-12T06:47:00+00:00",
                "identifier": "provider-b-arg-sui",
                "score_90m": {"home": 1, "away": 1},
            },
        ]

        self.assertEqual(postmatch_review.validate_result(result)["settlement_status"], "ready")

        result["sources"][1]["score_90m"] = {"home": 2, "away": 1}
        pending = postmatch_review.validate_result(result)
        self.assertEqual(pending["settlement_status"], "pending")
        self.assertEqual(pending["pending_reason"], "source_conflict")

    def test_nonofficial_sources_require_explicit_reputation_and_independence(self):
        result = argentina_result()
        result["sources"] = [
            {
                "name": "Provider A mirror 1",
                "official": False,
                "reputable": True,
                "independent_id": "same-provider",
                "observed_at": "2026-07-12T06:46:00+00:00",
                "identifier": "mirror-1",
                "score_90m": {"home": 1, "away": 1},
            },
            {
                "name": "Provider A mirror 2",
                "official": False,
                "reputable": True,
                "independent_id": "same-provider",
                "observed_at": "2026-07-12T06:47:00+00:00",
                "identifier": "mirror-2",
                "score_90m": {"home": 1, "away": 1},
            },
        ]

        with self.assertRaisesRegex(ValueError, "independent"):
            postmatch_review.validate_result(result)

        result["sources"][1]["independent_id"] = "provider-b"
        result["sources"][1]["reputable"] = False
        with self.assertRaisesRegex(ValueError, "reputable"):
            postmatch_review.validate_result(result)

    def test_one_unofficial_source_is_rejected(self):
        result = argentina_result()
        result["sources"] = [
            {
                "name": "Provider A",
                "official": False,
                "reputable": True,
                "independent_id": "provider-a",
                "observed_at": "2026-07-12T06:46:00+00:00",
                "identifier": "provider-a-arg-sui",
                "score_90m": {"home": 1, "away": 1},
            }
        ]

        with self.assertRaisesRegex(ValueError, "two independent"):
            postmatch_review.validate_result(result)

    def test_postponed_match_is_pending_not_completed(self):
        result = postmatch_review.validate_result(
            {
                "event_id": "arg-sui-2026",
                "status": "postponed",
            }
        )

        self.assertEqual(result["settlement_status"], "pending")
        self.assertEqual(result["schema_version"], "1.0")
        self.assertEqual(result["sources"], [])

    def test_boolean_or_decreasing_scores_are_rejected(self):
        boolean_score = argentina_result()
        boolean_score["score_90m"] = {"home": True, "away": 1}
        with self.assertRaisesRegex(ValueError, "whole number"):
            postmatch_review.validate_result(boolean_score)

        decreasing = argentina_result()
        decreasing["score_after_extra_time"] = {"home": 0, "away": 1}
        with self.assertRaisesRegex(ValueError, "extra-time"):
            postmatch_review.validate_result(decreasing)


class ReviewTests(unittest.TestCase):
    def test_wrong_pick_becomes_probabilistic_miss_not_immediate_model_change(self):
        review = postmatch_review.build_review(
            make_forecast_record(),
            argentina_result(),
            language="zh",
        )

        self.assertIn("probabilistic_miss", review["cause_tags"])
        self.assertEqual(review["evolution_status"], "model_unchanged")
        self.assertIn("90分钟", review["summary"])
        self.assertIn("正确", review["message"])
        self.assertIn("错误", review["message"])
        self.assertIn("原因", review["message"])
        self.assertIn("模型状态", review["message"])
        self.assertIn("单场仍可能", review["message"])
        self.assertIn("预测 主队，结果 平局", review["message"])
        self.assertIn("预测 是，结果 是", review["message"])
        self.assertIn("主队：未命中；客队：命中", review["message"])
        self.assertNotIn("{'", review["message"])
        self.assertEqual(
            set(review["localized_sections"]),
            {
                "right",
                "wrong",
                "unsettled",
                "causes",
                "closing",
                "calibration",
                "evolution",
                "probability_reminder",
            },
        )
        self.assertTrue(review["cause_explanations"])
        table = {row["market"]: row for row in review["market_table"]}
        self.assertEqual(table["1x2"]["verdict"], "loss")
        self.assertEqual(table["qualification"]["verdict"], "win")

    def test_correct_pick_is_summarized_without_reinforcing_one_match(self):
        record = make_forecast_record()
        record["markets"]["1x2"]["pick"] = "draw"
        record["markets"]["totals"][0]["pick"] = "under"
        record["markets"]["asian_handicap"][0]["pick"] = "away"
        record["markets"]["correct_score"]["displayed"] = [
            {"score": "1-1", "probability": 0.11}
        ]
        review = postmatch_review.build_review(
            record,
            argentina_result(),
            language="en",
            events=[{"type": "red_card", "source": "rumor"}],
        )

        self.assertNotIn("probabilistic_miss", review["cause_tags"])
        self.assertIn("evidence_unavailable", review["cause_tags"])
        self.assertIn("90 minutes", review["summary"])
        self.assertIn("one match", review["lesson"].lower())
        self.assertIn("Evolution status", review["message"])
        self.assertIn("model unchanged", review["message"])
        self.assertIn("still lose individual matches", review["message"])
        self.assertEqual(review["evolution_status"], "model_unchanged")

    def test_only_verified_events_generate_high_impact_or_late_news_tags(self):
        verified_events = [
            {
                "type": "red_card",
                "team": "Argentina",
                "minute": 12,
                "verified": True,
                "material_impact": True,
                "source": "official match report",
            },
            {
                "type": "confirmed_injury",
                "team": "Switzerland",
                "verified": True,
                "source": "official lineup",
                "observed_at": "2026-07-12T02:55:00+00:00",
            },
        ]
        review = postmatch_review.build_review(
            make_forecast_record(),
            argentina_result(),
            events=verified_events,
        )
        unsupported = postmatch_review.build_review(
            make_forecast_record(),
            argentina_result(),
            events=[{"type": "red_card", "source": "rumor"}],
        )

        self.assertIn("high_impact_match_event", review["cause_tags"])
        self.assertIn("late_information_missed", review["cause_tags"])
        self.assertNotIn("high_impact_match_event", unsupported["cause_tags"])
        self.assertNotIn("late_information_missed", unsupported["cause_tags"])
        self.assertIn("evidence_unavailable", unsupported["cause_tags"])

        nonmaterial = postmatch_review.build_review(
            make_forecast_record(),
            argentina_result(),
            events=[
                {
                    "type": "red_card",
                    "verified": True,
                    "material_impact": False,
                    "source": "official match report",
                }
            ],
        )
        self.assertNotIn("high_impact_match_event", nonmaterial["cause_tags"])
        self.assertNotIn("evidence_unavailable", nonmaterial["cause_tags"])

        mixed = postmatch_review.build_review(
            make_forecast_record(),
            argentina_result(),
            language="zh",
            events=[verified_events[0], {"type": "red_card", "source": "rumor"}],
        )
        self.assertIn("high_impact_match_event", mixed["cause_tags"])
        self.assertIn("evidence_unavailable", mixed["cause_tags"])
        self.assertTrue(
            any("至少一条" in explanation for explanation in mixed["cause_explanations"])
        )

    def test_closing_move_against_pick_is_evidence_backed(self):
        closing = {
            "observed_at": "2026-07-12T02:59:00+00:00",
            "probabilities_90m": {"home": 0.50, "draw": 0.31, "away": 0.19},
        }

        review = postmatch_review.build_review(
            make_forecast_record(),
            argentina_result(),
            closing=closing,
        )

        self.assertIn("closing_market_moved_against_forecast", review["cause_tags"])
        self.assertAlmostEqual(review["closing_movement_pp"], -8.0)
        self.assertIn("closing", review["localized_sections"]["closing"].lower())
        self.assertIn("calibration", review["localized_sections"]["calibration"].lower())

    def test_settlement_scope_error_requires_a_different_score_used(self):
        correct_previous = postmatch_review.build_review(
            make_forecast_record(),
            argentina_result(),
            previous_settlement={"score_used": {"home": 1, "away": 1}},
        )
        wrong_previous = postmatch_review.build_review(
            make_forecast_record(),
            argentina_result(),
            previous_settlement={"score_used": {"home": 3, "away": 1}},
        )

        self.assertNotIn("settlement_scope_error", correct_previous["cause_tags"])
        self.assertIn("settlement_scope_error", wrong_previous["cause_tags"])

    def test_completed_record_is_calibration_compatible(self):
        review = postmatch_review.build_review(make_forecast_record(), argentina_result())
        completed = review["completed_record"]
        report = calibrate.build_report([completed])

        self.assertEqual(completed["event_id"], "arg-sui-2026")
        self.assertEqual(completed["outcome_90m"], "draw")
        self.assertEqual(completed["outcome_totals"], {"2.5": "under"})
        self.assertEqual(completed["outcome_btts"], "yes")
        self.assertEqual(report["valid_records"], 1)
        self.assertIn("btts_brier", review["metrics"])
        self.assertIn("2.5", review["metrics"]["totals_brier"])
        self.assertIn("score_log_loss", review["metrics"])

    def test_completed_ledger_append_is_idempotent(self):
        review = postmatch_review.build_review(make_forecast_record(), argentina_result())
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "completed.jsonl"

            self.assertTrue(postmatch_review.append_completed(path, review))
            self.assertFalse(postmatch_review.append_completed(path, copy.deepcopy(review)))
            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), 1)

    def test_cli_writes_review_and_completed_record(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            forecast_path = Path(tmpdir) / "forecast.json"
            result_path = Path(tmpdir) / "result.json"
            completed_path = Path(tmpdir) / "completed.jsonl"
            forecast_path.write_text(json.dumps(make_forecast_record()), encoding="utf-8")
            result_path.write_text(json.dumps(argentina_result()), encoding="utf-8")

            process = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "postmatch_review.py"),
                    "--forecast",
                    str(forecast_path),
                    "--result",
                    str(result_path),
                    "--language",
                    "zh",
                    "--completed-out",
                    str(completed_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertEqual(payload["evolution_status"], "model_unchanged")
            self.assertEqual(len(completed_path.read_text(encoding="utf-8").splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
