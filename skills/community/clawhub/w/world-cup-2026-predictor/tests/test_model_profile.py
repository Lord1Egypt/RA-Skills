import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import forecast
import model_profile


class ModelProfileTests(unittest.TestCase):
    def test_default_profile_is_valid_and_tier_d_is_fixed(self):
        profile = model_profile.load_profile(ROOT / "profiles" / "default.json")

        self.assertEqual(profile["profile_id"], "v2-default")
        self.assertEqual(profile["source_weights"]["D"], 0.0)

    def test_unknown_field_is_rejected(self):
        profile = model_profile.load_profile(ROOT / "profiles" / "default.json")

        with self.assertRaisesRegex(ValueError, "unknown"):
            model_profile.validate_profile({**profile, "execute": "code"})

    def test_tier_d_cannot_be_enabled(self):
        profile = model_profile.load_profile(ROOT / "profiles" / "default.json")
        profile["source_weights"]["D"] = 0.1

        with self.assertRaisesRegex(ValueError, "Tier D"):
            model_profile.validate_profile(profile)

    def test_large_relative_challenger_change_is_rejected(self):
        champion = model_profile.load_profile(ROOT / "profiles" / "default.json")
        challenger = copy.deepcopy(champion)
        challenger["source_weights"]["A"] = 1.50

        with self.assertRaisesRegex(ValueError, "10 percent"):
            model_profile.validate_challenger(champion, challenger)

    def test_zero_default_conflict_penalty_allows_only_bounded_first_step(self):
        champion = model_profile.load_profile(ROOT / "profiles" / "default.json")
        challenger = copy.deepcopy(champion)
        challenger["cross_market_conflict_penalty"] = 2.5

        accepted = model_profile.validate_challenger(champion, challenger)
        self.assertEqual(accepted["cross_market_conflict_penalty"], 2.5)

        challenger["cross_market_conflict_penalty"] = 2.51
        with self.assertRaisesRegex(ValueError, "10 percent"):
            model_profile.validate_challenger(champion, challenger)

    def test_absolute_profile_bounds_are_enforced(self):
        cases = [
            (("source_weights", "A"), 2.01, "source_weights.A"),
            (("fit_family_caps", "totals"), 2.01, "fit_family_caps.totals"),
            (("recency_weights", "0_15"), 1.01, "recency_weights.0_15"),
            (("confidence_thresholds", "high"), 100.01, "confidence_thresholds.high"),
            (("cross_market_conflict_penalty",), 25.01, "cross_market_conflict_penalty"),
        ]
        for path, value, message in cases:
            with self.subTest(path=path):
                profile = model_profile.load_profile(ROOT / "profiles" / "default.json")
                target = profile
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                with self.assertRaisesRegex(ValueError, message):
                    model_profile.validate_profile(profile)

    def test_recency_weights_must_decrease_with_age(self):
        profile = model_profile.load_profile(ROOT / "profiles" / "default.json")
        profile["recency_weights"]["60_180"] = 0.95

        with self.assertRaisesRegex(ValueError, "recency_weights"):
            model_profile.validate_profile(profile)

    def test_legacy_constants_are_loaded_from_default_profile(self):
        profile = model_profile.load_profile(ROOT / "profiles" / "default.json")

        self.assertEqual(forecast.DEFAULT_MODEL_PROFILE, profile)
        self.assertIs(forecast.SOURCE_WEIGHTS, forecast.DEFAULT_MODEL_PROFILE["source_weights"])
        self.assertIs(forecast.FIT_FAMILY_CAPS, forecast.DEFAULT_MODEL_PROFILE["fit_family_caps"])
        self.assertIs(forecast.RECENCY_WEIGHTS, forecast.DEFAULT_MODEL_PROFILE["recency_weights"])
        self.assertIs(forecast.CONFIDENCE_THRESHOLDS, forecast.DEFAULT_MODEL_PROFILE["confidence_thresholds"])

    def test_default_profile_aliases_are_immutable_and_consistent(self):
        match = json.loads((ROOT / "examples" / "multi-book-match.json").read_text(encoding="utf-8"))
        before = forecast.analyze_v2_match(copy.deepcopy(match))

        with self.assertRaises(TypeError):
            forecast.FIT_FAMILY_CAPS["totals"] = 0.05
        with self.assertRaises(TypeError):
            forecast.DEFAULT_MODEL_PROFILE["fit_family_caps"] = {"1x2": 1.0, "totals": 0.05, "btts": 0.5}

        helper_fit = forecast.fit_expected_goals(
            forecast._fit_consensus_from_latest(
                forecast.build_consensus(match["quotes"], as_of=before["as_of"])
            )
        )
        after = forecast.analyze_v2_match(copy.deepcopy(match))

        self.assertEqual(helper_fit["diagnostics"]["family_weights"], after["diagnostics"]["fit"]["family_weights"])
        self.assertEqual(before["probabilities_90m"], after["probabilities_90m"])

    def test_data_directory_precedence(self):
        with mock.patch.dict(os.environ, {"FOOTBALL_FORECASTER_DATA_DIR": "/tmp/from-env"}):
            self.assertEqual(model_profile.resolve_data_dir(None), Path("/tmp/from-env"))
            self.assertEqual(model_profile.resolve_data_dir("/tmp/from-cli"), Path("/tmp/from-cli"))

    def test_explicit_default_profile_preserves_forecast(self):
        match = json.loads((ROOT / "examples" / "multi-book-match.json").read_text(encoding="utf-8"))
        implicit = forecast.analyze_v2_match(copy.deepcopy(match))
        explicit = forecast.analyze_v2_match(
            copy.deepcopy(match),
            profile=model_profile.load_profile(ROOT / "profiles" / "default.json"),
        )

        self.assertEqual(implicit["probabilities_90m"], explicit["probabilities_90m"])
        self.assertEqual(implicit["expected_goals"], explicit["expected_goals"])

    def test_source_weights_control_duplicate_selection(self):
        quotes = [
            {
                "source": "direct-a",
                "bookmaker": "Same Book",
                "source_tier": "A",
                "market": "1x2",
                "selection": "home",
                "odds": 1.8,
                "odds_format": "decimal",
                "observed_at": "2026-07-10T03:45:00+08:00",
                "snapshot": "current",
                "period": "90m",
            },
            {
                "source": "direct-b",
                "bookmaker": "Same Book",
                "source_tier": "B",
                "market": "1x2",
                "selection": "home",
                "odds": 1.9,
                "odds_format": "decimal",
                "observed_at": "2026-07-10T03:45:00+08:00",
                "snapshot": "current",
                "period": "90m",
            },
        ]
        default_kept, _ = forecast.deduplicate_quotes(copy.deepcopy(quotes))
        custom_kept, _ = forecast.deduplicate_quotes(
            copy.deepcopy(quotes),
            source_weights={"A": 0.5, "B": 2.0, "C": 0.75, "D": 0.0},
        )

        self.assertEqual(default_kept[0]["source_tier"], "A")
        self.assertEqual(custom_kept[0]["source_tier"], "B")

    def test_family_caps_and_confidence_thresholds_affect_analysis(self):
        match = json.loads((ROOT / "examples" / "multi-book-match.json").read_text(encoding="utf-8"))
        default = forecast.analyze_v2_match(copy.deepcopy(match))
        profile = model_profile.load_profile(ROOT / "profiles" / "default.json")
        profile["fit_family_caps"]["totals"] = 0.05
        profile["fit_family_caps"]["btts"] = 0.05
        profile["confidence_thresholds"]["high"] = 95.0
        custom = forecast.analyze_v2_match(copy.deepcopy(match), profile=profile)

        self.assertLess(
            custom["diagnostics"]["fit"]["family_weights"]["totals"],
            default["diagnostics"]["fit"]["family_weights"]["totals"],
        )
        self.assertEqual(default["confidence"]["label"], "high")
        self.assertEqual(custom["confidence"]["label"], "medium")

    def test_cross_market_conflict_penalty_is_explicit_and_profile_driven(self):
        match = json.loads((ROOT / "examples" / "multi-book-match.json").read_text(encoding="utf-8"))
        for quote in match["quotes"]:
            if quote["market"] != "asian_handicap":
                continue
            magnitude = "1.25" if quote["snapshot"] == "opening" else "0.75"
            quote["line"] = f"-{magnitude}" if quote["selection"] == "home" else magnitude

        baseline = forecast.analyze_v2_match(copy.deepcopy(match))
        profile = model_profile.load_profile(ROOT / "profiles" / "default.json")
        profile["cross_market_conflict_penalty"] = 20.0
        penalized = forecast.analyze_v2_match(copy.deepcopy(match), profile=profile)

        self.assertTrue(baseline["cross_market_conflicts"])
        self.assertEqual(baseline["confidence"]["penalties"].get("cross_market_conflict", 0), 0)
        self.assertEqual(penalized["confidence"]["penalties"]["cross_market_conflict"], 20)
        self.assertEqual(penalized["confidence"]["score"], baseline["confidence"]["score"] - 20)


class ModelProfileActivationTests(unittest.TestCase):
    def make_challenger(self, *, profile_id="challenger-1", parent_id="v2-default"):
        champion = model_profile.load_profile(ROOT / "profiles" / "default.json")
        challenger = copy.deepcopy(champion)
        challenger["profile_id"] = profile_id
        challenger["parent_id"] = parent_id
        challenger["source_weights"]["A"] = 1.1875
        return model_profile.validate_challenger(champion, challenger)

    def test_load_active_profile_defaults_to_packaged_profile_when_pointer_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            active = model_profile.load_active_profile(tmpdir)

        self.assertEqual(active["profile_id"], "v2-default")

    def test_activate_and_rollback_are_reversible(self):
        challenger = self.make_challenger()
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            model_profile.activate_profile(data_dir, challenger)
            pointer = json.loads((data_dir / "active-profile.json").read_text(encoding="utf-8"))
            self.assertEqual(pointer["profile_id"], "challenger-1")
            self.assertEqual(pointer["previous_profile_id"], "v2-default")
            self.assertEqual(model_profile.load_active_profile(data_dir)["profile_id"], "challenger-1")

            model_profile.rollback_profile(data_dir)

            self.assertEqual(model_profile.load_active_profile(data_dir)["profile_id"], "v2-default")
            self.assertTrue((data_dir / "profiles" / "challenger-1.json").exists())

    def test_activation_path_traversal_is_rejected(self):
        bad_profile_id = self.make_challenger(profile_id="../escape")
        bad_parent_id = self.make_challenger(parent_id="../parent")

        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(ValueError, "safe file identifier"):
                model_profile.activate_profile(tmpdir, bad_profile_id)
            with self.assertRaisesRegex(ValueError, "safe file identifier"):
                model_profile.activate_profile(tmpdir, bad_parent_id)

    def test_corrupted_pointer_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            (data_dir / "active-profile.json").write_text('{not json', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "active-profile"):
                model_profile.load_active_profile(data_dir)

    def test_unknown_pointer_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            (data_dir / "active-profile.json").write_text(
                json.dumps({
                    "schema_version": "1.0",
                    "profile_id": "missing-profile",
                    "previous_profile_id": "v2-default",
                }),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "unknown active profile"):
                model_profile.load_active_profile(data_dir)

    def test_existing_profile_id_with_conflicting_content_is_rejected(self):
        challenger = self.make_challenger()
        conflicting = self.make_challenger()
        conflicting["source_weights"]["B"] = 1.05
        conflicting = model_profile.validate_challenger(
            model_profile.load_profile(ROOT / "profiles" / "default.json"),
            conflicting,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            model_profile.activate_profile(data_dir, challenger)

            with self.assertRaisesRegex(ValueError, "conflicting content"):
                model_profile.activate_profile(data_dir, conflicting)

    def test_stale_parent_is_rejected_without_corrupting_active_pointer(self):
        first = self.make_challenger(profile_id="challenger-1")
        stale = self.make_challenger(profile_id="challenger-stale")

        with tempfile.TemporaryDirectory() as tmpdir:
            model_profile.activate_profile(tmpdir, first)
            with self.assertRaisesRegex(ValueError, "parent_id"):
                model_profile.activate_profile(tmpdir, stale)

            self.assertEqual(model_profile.load_active_profile(tmpdir)["profile_id"], "challenger-1")

    def test_activation_enforces_bounded_change_against_locked_champion(self):
        champion = model_profile.load_profile(ROOT / "profiles" / "default.json")
        oversized = copy.deepcopy(champion)
        oversized["profile_id"] = "oversized"
        oversized["parent_id"] = champion["profile_id"]
        oversized["source_weights"]["A"] = 1.5

        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(ValueError, "10 percent"):
                model_profile.activate_profile(tmpdir, oversized)
            self.assertEqual(model_profile.load_active_profile(tmpdir)["profile_id"], "v2-default")

    def test_stale_lock_file_does_not_permanently_block_activation(self):
        challenger = self.make_challenger()
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_path = Path(tmpdir) / model_profile.PROFILE_LOCK_FILENAME
            lock_path.write_text("999999999", encoding="utf-8")

            model_profile.activate_profile(tmpdir, challenger)

            self.assertEqual(model_profile.load_active_profile(tmpdir)["profile_id"], "challenger-1")

    def test_promoted_profile_artifact_keeps_validated_evolution_evidence(self):
        challenger = self.make_challenger()
        evidence = {
            "training_cutoff": "2026-07-10T12:00:00+00:00",
            "training_record_ids": ["forecast-1", "forecast-2"],
            "holdout_record_ids": ["forecast-3"],
            "metrics": {"champion": {"brier_1x2": 0.2}, "challenger": {"brier_1x2": 0.19}},
            "parameter_diff": {"source_weights.A": {"from": 1.25, "to": 1.1875}},
            "promotion_decision": {"promote": True, "failed_gates": []},
        }
        fingerprint = hashlib.sha256(
            json.dumps(
                evidence,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        challenger["evolution"] = {
            "schema_version": "1.0",
            "created_at": "2026-07-13T12:00:00+00:00",
            **evidence,
            "evaluation_fingerprint": fingerprint,
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            model_profile.activate_profile(tmpdir, challenger)
            artifact = json.loads(
                (Path(tmpdir) / "profiles" / "challenger-1.json").read_text(encoding="utf-8")
            )
            active = model_profile.load_active_profile(tmpdir)

        self.assertEqual(artifact["evolution"]["training_record_ids"], ["forecast-1", "forecast-2"])
        self.assertEqual(active["evolution"]["promotion_decision"]["promote"], True)

    def test_tampered_evolution_evidence_is_rejected(self):
        challenger = self.make_challenger()
        evidence = {
            "training_cutoff": None,
            "training_record_ids": [],
            "holdout_record_ids": ["forecast-3"],
            "metrics": {"challenger": {"brier_1x2": 0.19}},
            "parameter_diff": {"source_weights.A": {"from": 1.25, "to": 1.1875}},
            "promotion_decision": {"promote": True, "failed_gates": []},
        }
        fingerprint = hashlib.sha256(
            json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        challenger["evolution"] = {
            "schema_version": "1.0",
            "created_at": "2026-07-13T12:00:00+00:00",
            **evidence,
            "evaluation_fingerprint": fingerprint,
        }
        challenger["evolution"]["metrics"]["challenger"]["brier_1x2"] = 0.99

        with self.assertRaisesRegex(ValueError, "fingerprint"):
            model_profile.validate_profile(challenger)

    def test_unknown_evolution_metadata_field_is_rejected(self):
        challenger = self.make_challenger()
        challenger["evolution"] = {"execute": "code"}

        with self.assertRaisesRegex(ValueError, "evolution"):
            model_profile.validate_profile(challenger)


if __name__ == "__main__":
    unittest.main()
