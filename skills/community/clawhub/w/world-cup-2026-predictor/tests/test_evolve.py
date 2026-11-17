import copy
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import forecast
import model_profile
import postmatch_review
import evolve


def official_source():
    return {
        "name": "FIFA",
        "official": True,
        "observed_at": "2026-07-12T06:45:00+00:00",
        "url": "https://example.test/match/finished",
    }


class PromotionGateTests(unittest.TestCase):
    def eligible_sample(self, **overrides):
        sample = {
            "overall": 130,
            "buckets": {"world_cup|1x2": 40},
            "affected_buckets": {"world_cup|1x2": 40},
            "quarantined_conflicts": 0,
        }
        sample.update(overrides)
        return sample

    def good_metrics(self, **overrides):
        metrics = {
            "brier_1x2": 0.20,
            "log_loss_1x2": 0.55,
            "totals_brier": 0.22,
            "totals_count": 30,
            "btts_brier": 0.21,
            "btts_count": 30,
            "calibration_error": 0.04,
            "bucket_brier": {"world_cup|1x2": 0.18},
            "top_pick_accuracy": 0.60,
        }
        metrics.update(overrides)
        return metrics

    def test_one_match_never_changes_profile(self):
        decision = evolve.decide_promotion(
            sample={"overall": 1, "buckets": {"world_cup|1x2": 1}},
            champion={},
            challenger={},
        )

        self.assertFalse(decision["promote"])
        self.assertIn("minimum_overall_sample", decision["failed_gates"])

    def test_overall_improvement_cannot_hide_bucket_regression(self):
        champion = self.good_metrics(bucket_brier={"world_cup|1x2": 0.18})
        challenger = self.good_metrics(
            brier_1x2=0.195,
            log_loss_1x2=0.54,
            bucket_brier={"world_cup|1x2": 0.19},
        )

        decision = evolve.decide_promotion(self.eligible_sample(), champion, challenger)

        self.assertFalse(decision["promote"])
        self.assertIn("bucket_regression", decision["failed_gates"])

    def test_totals_or_confidence_regression_blocks_promotion(self):
        champion = self.good_metrics(totals_brier=0.22, calibration_error=0.04)
        challenger = self.good_metrics(
            brier_1x2=0.195,
            log_loss_1x2=0.54,
            totals_brier=0.23,
            calibration_error=0.05,
        )

        decision = evolve.decide_promotion(self.eligible_sample(), champion, challenger)

        self.assertFalse(decision["promote"])
        self.assertIn("secondary_market_regression", decision["failed_gates"])
        self.assertIn("calibration_regression", decision["failed_gates"])

    def test_malformed_or_nonfinite_metrics_fail_closed(self):
        champion = self.good_metrics()
        challenger = self.good_metrics(log_loss_1x2=float("nan"))

        decision = evolve.decide_promotion(self.eligible_sample(), champion, challenger)

        self.assertEqual(decision["failed_gates"], ["malformed_metrics"])
        self.assertFalse(decision["promote"])

    def test_negative_metrics_and_empty_affected_buckets_fail_closed(self):
        champion = self.good_metrics()
        challenger = self.good_metrics(brier_1x2=-0.01)

        malformed = evolve.decide_promotion(self.eligible_sample(), champion, challenger)
        no_bucket = evolve.decide_promotion(
            self.eligible_sample(affected_buckets={}),
            champion,
            self.good_metrics(brier_1x2=0.195, log_loss_1x2=0.54),
        )

        self.assertEqual(malformed["failed_gates"], ["malformed_metrics"])
        self.assertIn("minimum_bucket_sample", no_bucket["failed_gates"])

    def test_sparse_secondary_markets_are_diagnostic_not_blocking(self):
        champion = self.good_metrics(totals_count=1, btts_count=1)
        challenger = self.good_metrics(
            brier_1x2=0.195,
            log_loss_1x2=0.54,
            totals_brier=0.30,
            totals_count=1,
            btts_brier=0.30,
            btts_count=1,
        )

        decision = evolve.decide_promotion(self.eligible_sample(), champion, challenger)

        self.assertTrue(decision["promote"], decision)

    def test_secondary_metric_without_observation_count_fails_closed(self):
        champion = self.good_metrics()
        challenger = self.good_metrics(brier_1x2=0.195, log_loss_1x2=0.54)
        champion.pop("totals_count")

        decision = evolve.decide_promotion(self.eligible_sample(), champion, challenger)

        self.assertEqual(decision["failed_gates"], ["malformed_metrics"])

    def test_quarantined_settlement_conflicts_fail_closed(self):
        champion = self.good_metrics()
        challenger = self.good_metrics(brier_1x2=0.195, log_loss_1x2=0.54)

        decision = evolve.decide_promotion(
            self.eligible_sample(quarantined_conflicts=1),
            champion,
            challenger,
        )

        self.assertFalse(decision["promote"])
        self.assertIn("quarantined_settlement_conflict", decision["failed_gates"])

    def test_rollback_requires_30_new_matches_and_both_primary_metrics_worse(self):
        parent = {"brier_1x2": 0.20, "log_loss_1x2": 0.55}
        child = {"brier_1x2": 0.21, "log_loss_1x2": 0.57}

        self.assertFalse(evolve.should_rollback(29, parent, child))
        self.assertTrue(evolve.should_rollback(30, parent, child))
        self.assertFalse(evolve.should_rollback(30, parent, {"brier_1x2": 0.21, "log_loss_1x2": 0.54}))

    def test_rollback_rejects_malformed_or_nonfinite_inputs(self):
        with self.assertRaisesRegex(ValueError, "new_distinct_matches"):
            evolve.should_rollback("30", {"brier_1x2": 0.20, "log_loss_1x2": 0.55}, {"brier_1x2": 0.21, "log_loss_1x2": 0.57})
        with self.assertRaisesRegex(ValueError, "brier_1x2"):
            evolve.should_rollback(30, {"brier_1x2": math.nan, "log_loss_1x2": 0.55}, {"brier_1x2": 0.21, "log_loss_1x2": 0.57})


class GroupedSplitTests(unittest.TestCase):
    def snapshot(self, event_id, kickoff, as_of, *, offset, forecast_suffix):
        return {
            "event_id": event_id,
            "forecast_id": f"forecast-{event_id}-{forecast_suffix}",
            "kickoff": kickoff,
            "as_of": as_of,
            "alert_offset": offset,
        }

    def make_many_snapshots(self, events, snapshots_per_event):
        records = []
        base = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)
        for event_index in range(events):
            kickoff = (base + timedelta(days=event_index)).isoformat()
            for snapshot_index in range(snapshots_per_event):
                as_of = (base + timedelta(days=event_index, hours=-(snapshot_index + 1))).isoformat()
                records.append(
                    self.snapshot(
                        f"event-{event_index:03d}",
                        kickoff,
                        as_of,
                        offset=f"snap-{snapshot_index}",
                        forecast_suffix=str(snapshot_index),
                    )
                )
        return records

    def test_snapshots_from_same_event_never_cross_train_holdout(self):
        train, holdout = evolve.grouped_time_split(self.make_many_snapshots(120, 4), holdout_matches=30)

        train_ids = {item["event_id"] for item in train}
        holdout_ids = {item["event_id"] for item in holdout}
        self.assertFalse(train_ids & holdout_ids)
        self.assertEqual(len(holdout_ids), 30)

    def test_newest_30_distinct_event_ids_form_holdout(self):
        train, holdout = evolve.grouped_time_split(self.make_many_snapshots(40, 2), holdout_matches=30)

        self.assertEqual({item["event_id"] for item in train}, {f"event-{index:03d}" for index in range(10)})
        self.assertEqual({item["event_id"] for item in holdout}, {f"event-{index:03d}" for index in range(10, 40)})

    def test_grouped_time_split_rejects_modern_missing_or_naive_kickoff(self):
        missing = [self.snapshot("event-a", None, "2026-07-01T10:00:00+00:00", offset="T-10min", forecast_suffix="1")]
        naive = [self.snapshot("event-b", "2026-07-01T12:00:00", "2026-07-01T10:00:00+00:00", offset="T-10min", forecast_suffix="1")]

        with self.assertRaisesRegex(ValueError, "kickoff"):
            evolve.grouped_time_split(missing, holdout_matches=1)
        with self.assertRaisesRegex(ValueError, "kickoff"):
            evolve.grouped_time_split(naive, holdout_matches=1)


class CandidateGenerationTests(unittest.TestCase):
    def test_generate_candidates_is_deterministic_and_one_coordinate_only(self):
        champion = model_profile.load_profile(ROOT / "profiles" / "default.json")

        first = evolve.generate_coordinate_candidates(champion)
        second = evolve.generate_coordinate_candidates(champion)

        self.assertEqual([item["profile_id"] for item in first], [item["profile_id"] for item in second])
        self.assertTrue(first)
        for candidate in first:
            self.assertEqual(candidate["parent_id"], champion["profile_id"])
            self.assertEqual(candidate["source_weights"]["D"], 0.0)
            changed = []
            for section in ("source_weights", "fit_family_caps", "recency_weights", "confidence_thresholds"):
                for key, value in champion[section].items():
                    if not math.isclose(candidate[section][key], value, rel_tol=0.0, abs_tol=1e-12):
                        changed.append((section, key))
            if not math.isclose(
                candidate["cross_market_conflict_penalty"],
                champion["cross_market_conflict_penalty"],
                rel_tol=0.0,
                abs_tol=1e-12,
            ):
                changed.append(("cross_market_conflict_penalty", None))
            self.assertEqual(len(changed), 1)
        with self.assertRaisesRegex(ValueError, "unknown"):
            evolve.generate_coordinate_candidates({**champion, "execute": "code"})


class EvolveCliTests(unittest.TestCase):
    def load_example_match(self):
        return json.loads((ROOT / "examples" / "multi-book-match.json").read_text(encoding="utf-8"))

    def make_completed_record(self, event_id="event-001", kickoff_day=1, *, as_of_minutes=10, score_90m=None):
        match = self.load_example_match()
        kickoff = datetime(2026, 7, kickoff_day, 12, 0, tzinfo=timezone.utc)
        match["teams"] = [f"Home {event_id}", f"Away {event_id}"]
        match["match"] = f"Home {event_id} vs Away {event_id}"
        match["kickoff"] = kickoff.isoformat()
        as_of = (kickoff - timedelta(minutes=as_of_minutes)).isoformat()
        analysis = forecast.analyze_v2_match(copy.deepcopy(match), as_of=as_of)
        analysis["forecast_record"]["markets"]["qualification"] = None
        if score_90m is None:
            score_90m = {"home": 2, "away": 1}
        result = {
            "schema_version": "1.0",
            "status": "final",
            "event_id": analysis["forecast_record"]["event_id"],
            "score_90m": score_90m,
            "qualified": analysis["teams"][0],
            "sources": [official_source()],
        }
        review = postmatch_review.build_review(analysis["forecast_record"], result)
        completed = review["completed_record"]
        completed["bucket"] = "world_cup|1x2"
        return completed

    def test_one_match_never_writes_active_pointer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            completed_path = data_dir / "completed.jsonl"
            completed_path.write_text(json.dumps(self.make_completed_record()) + "\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "evolve.py"),
                    "--completed",
                    str(completed_path),
                    "--data-dir",
                    str(data_dir),
                    "--mode",
                    "promote",
                    "--pretty",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["decision"]["promote"])
            self.assertFalse((data_dir / "active-profile.json").exists())
            audit_dir = data_dir / "evolution"
            self.assertTrue((audit_dir / "candidates.json").exists())
            self.assertTrue((audit_dir / "evaluation.json").exists())
            self.assertTrue((audit_dir / "decision.json").exists())

    def test_cli_error_has_no_traceback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing_path = Path(tmpdir) / "missing.jsonl"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "evolve.py"),
                    "--completed",
                    str(missing_path),
                    "--mode",
                    "evaluate",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("error:", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_audit_artifacts_precede_activation(self):
        champion = model_profile.load_profile(ROOT / "profiles" / "default.json")
        challenger = copy.deepcopy(champion)
        challenger["profile_id"] = "challenger-1"
        challenger["parent_id"] = champion["profile_id"]
        challenger["source_weights"]["A"] = 1.1875
        challenger = model_profile.validate_challenger(champion, challenger)
        report = {
            "sample": {"overall": 130, "buckets": {"world_cup|1x2": 40}, "affected_buckets": {"world_cup|1x2": 40}},
            "candidates": [{"profile_id": challenger["profile_id"]}],
            "evaluation": {"champion": {"brier_1x2": 0.20}, "challenger": {"brier_1x2": 0.19}},
            "decision": {"promote": True, "failed_gates": []},
            "selected_candidate_profile": challenger,
        }
        activations = []

        def fake_activate(data_dir, profile):
            audit_dir = Path(data_dir) / "evolution"
            self.assertTrue((audit_dir / "candidates.json").exists())
            self.assertTrue((audit_dir / "evaluation.json").exists())
            self.assertTrue((audit_dir / "decision.json").exists())
            activations.append(profile["profile_id"])
            return profile

        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            completed_path = data_dir / "completed.jsonl"
            completed_path.write_text(json.dumps(self.make_completed_record()) + "\n", encoding="utf-8")
            with mock.patch.object(evolve, "evaluate_evolution", return_value=report):
                with mock.patch.object(model_profile, "activate_profile", side_effect=fake_activate):
                    result = evolve.execute_mode(completed_path, data_dir, mode="promote")

        self.assertEqual(len(activations), 1)
        self.assertTrue(activations[0].startswith("challenger-1-"))
        self.assertTrue(result["decision"]["promote"])
        self.assertIn("evolution", result["selected_candidate_profile"])

    def test_invalid_completed_records_do_not_inflate_sample_floor(self):
        valid = self.make_completed_record()
        invalid_records = []
        kickoff = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
        for index in range(99):
            invalid = copy.deepcopy(valid)
            invalid["event_id"] = f"invalid-{index:03d}"
            invalid["forecast_id"] = f"forecast-invalid-{index:03d}"
            invalid["kickoff"] = (kickoff + timedelta(days=index)).isoformat()
            invalid["as_of"] = (kickoff + timedelta(days=index, minutes=-10)).isoformat()
            invalid.pop("raw_match", None)
            invalid_records.append(invalid)

        with tempfile.TemporaryDirectory() as tmpdir:
            completed_path = Path(tmpdir) / "completed.jsonl"
            completed_path.write_text(
                "".join(json.dumps(item) + "\n" for item in [valid, *invalid_records]),
                encoding="utf-8",
            )
            with mock.patch.object(evolve, "generate_coordinate_candidates", return_value=[]):
                report = evolve.evaluate_evolution(completed_path, tmpdir)

        self.assertEqual(report["sample"]["overall"], 1)
        self.assertEqual(report["sample"]["invalid_records"], 99)
        self.assertIn("minimum_overall_sample", report["decision"]["failed_gates"])

    def test_full_archive_buckets_do_not_require_missing_holdout_metrics(self):
        champion = model_profile.load_profile(ROOT / "profiles" / "default.json")
        challenger = evolve.generate_coordinate_candidates(champion)[0]
        records = []
        start = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
        for index in range(100):
            kickoff = start + timedelta(days=index)
            records.append(
                {
                    "event_id": f"event-{index:03d}",
                    "forecast_id": f"forecast-{index:03d}",
                    "kickoff": kickoff.isoformat(),
                    "as_of": (kickoff - timedelta(minutes=10)).isoformat(),
                    "bucket": "older_league|1x2" if index < 70 else "world_cup|1x2",
                }
            )

        good = PromotionGateTests().good_metrics(
            brier_1x2=0.20,
            log_loss_1x2=0.55,
            bucket_brier={"world_cup|1x2": 0.18},
        )
        improved = PromotionGateTests().good_metrics(
            brier_1x2=0.195,
            log_loss_1x2=0.54,
            bucket_brier={"world_cup|1x2": 0.18},
        )

        def evaluation(profile, replayed, metrics, invalid=0):
            return {
                "profile_id": profile["profile_id"],
                "metrics": metrics,
                "report": {},
                "replayed_records": replayed,
                "invalid_records": invalid,
                "quarantined_conflicts": 0,
            }

        side_effects = [
            evaluation(champion, records, good),
            evaluation(champion, records[-30:], good),
            evaluation(challenger, records[:-30], improved),
            evaluation(challenger, records[-30:], improved),
        ]
        with mock.patch.object(evolve, "load_completed_records", return_value=records):
            with mock.patch.object(model_profile, "load_active_profile", return_value=champion):
                with mock.patch.object(evolve, "generate_coordinate_candidates", return_value=[challenger]):
                    with mock.patch.object(evolve, "evaluate_profile", side_effect=side_effects):
                        report = evolve.evaluate_evolution("unused.jsonl", "/tmp/unused")

        self.assertEqual(report["sample"]["buckets"]["older_league|1x2"], 70)
        self.assertEqual(report["sample"]["affected_buckets"], {"world_cup|1x2": 30})
        self.assertNotIn("malformed_metrics", report["decision"]["failed_gates"])

    def test_audit_write_fsyncs_file_and_parent_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "audit" / "decision.json"
            with mock.patch.object(evolve.os, "fsync", wraps=os.fsync) as fsync:
                evolve._atomic_write_json(target, {"promote": False})

        self.assertGreaterEqual(fsync.call_count, 2)

    def test_successful_promotion_persists_bound_evolution_evidence(self):
        champion = model_profile.load_profile(ROOT / "profiles" / "default.json")
        challenger = copy.deepcopy(champion)
        challenger["profile_id"] = "challenger-audit"
        challenger["parent_id"] = champion["profile_id"]
        challenger["source_weights"]["A"] = 1.1875
        challenger = model_profile.validate_challenger(champion, challenger)
        report = {
            "sample": {
                "overall": 130,
                "buckets": {"world_cup|1x2": 130},
                "affected_buckets": {"world_cup|1x2": 30},
            },
            "split": {
                "training_cutoff": "2026-07-01T12:00:00+00:00",
                "train_record_ids": ["review-train"],
                "holdout_record_ids": ["review-holdout"],
            },
            "candidates": [{"profile_id": challenger["profile_id"]}],
            "evaluation": {
                "champion": {"brier_1x2": 0.20, "log_loss_1x2": 0.55},
                "challenger": {"brier_1x2": 0.19, "log_loss_1x2": 0.54},
            },
            "decision": {"promote": True, "failed_gates": []},
            "selected_candidate_profile": challenger,
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            completed_path = Path(tmpdir) / "completed.jsonl"
            completed_path.write_text("", encoding="utf-8")
            with mock.patch.object(evolve, "evaluate_evolution", return_value=report):
                result = evolve.execute_mode(completed_path, tmpdir, mode="promote")
            profile_id = result["activation"]["activated_profile_id"]
            artifact = json.loads(
                (Path(tmpdir) / "profiles" / f"{profile_id}.json").read_text(encoding="utf-8")
            )

        evidence = artifact["evolution"]
        self.assertEqual(evidence["training_record_ids"], ["review-train"])
        self.assertEqual(evidence["holdout_record_ids"], ["review-holdout"])
        self.assertEqual(evidence["parameter_diff"]["source_weights.A"]["to"], 1.1875)
        self.assertTrue(evidence["promotion_decision"]["promote"])


class ReplayIntegrityTests(unittest.TestCase):
    def make_completed_record(self):
        return EvolveCliTests().make_completed_record()

    def test_replay_requires_archived_pre_kickoff_as_of(self):
        record = self.make_completed_record()
        record["as_of"] = None

        with self.assertRaisesRegex(ValueError, "as_of"):
            evolve.replay_completed_record(record, model_profile.load_profile())

    def test_replay_rejects_raw_match_event_identity_mismatch(self):
        record = self.make_completed_record()
        record["event_id"] = "different-event"

        with self.assertRaisesRegex(ValueError, "event_id"):
            evolve.replay_completed_record(record, model_profile.load_profile())

    def test_completed_review_preserves_archived_input_fingerprint(self):
        record = self.make_completed_record()

        self.assertEqual(
            record["input_fingerprint"],
            forecast.canonical_hash(record["raw_match"]),
        )

    def test_replay_rejects_same_event_raw_match_mutation(self):
        record = self.make_completed_record()
        record["input_fingerprint"] = forecast.canonical_hash(record["raw_match"])
        quote = next(
            item
            for item in record["raw_match"]["quotes"]
            if item["market"] == "1x2"
        )
        quote["odds"] = float(quote["odds"]) + 0.25

        with self.assertRaisesRegex(ValueError, "input_fingerprint"):
            evolve.replay_completed_record(record, model_profile.load_profile())


class EvaluateDeterminismTests(unittest.TestCase):
    def test_evaluate_mode_does_not_create_time_versioned_profile(self):
        champion = model_profile.load_profile(ROOT / "profiles" / "default.json")
        challenger = copy.deepcopy(champion)
        challenger["profile_id"] = "challenger-deterministic"
        challenger["parent_id"] = champion["profile_id"]
        challenger["source_weights"]["A"] = 1.1875
        challenger = model_profile.validate_challenger(champion, challenger)
        report = {
            "sample": {"overall": 130},
            "split": {},
            "candidates": [{"profile_id": challenger["profile_id"]}],
            "evaluation": {},
            "decision": {"promote": True, "failed_gates": []},
            "selected_candidate_profile": challenger,
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            completed_path = Path(tmpdir) / "completed.jsonl"
            completed_path.write_text("", encoding="utf-8")
            with mock.patch.object(
                evolve,
                "evaluate_evolution",
                side_effect=[copy.deepcopy(report), copy.deepcopy(report)],
            ):
                first = evolve.execute_mode(completed_path, tmpdir, mode="evaluate")
                second = evolve.execute_mode(completed_path, tmpdir, mode="evaluate")

        self.assertEqual(
            first["selected_candidate_profile"]["profile_id"],
            second["selected_candidate_profile"]["profile_id"],
        )
        self.assertEqual(
            first["selected_candidate_profile"]["profile_id"],
            "challenger-deterministic",
        )
        self.assertNotIn("evolution", first["selected_candidate_profile"])


if __name__ == "__main__":
    unittest.main()
