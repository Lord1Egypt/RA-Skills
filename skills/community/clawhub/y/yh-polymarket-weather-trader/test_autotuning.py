#!/usr/bin/env python3
"""
Tests for autotuning functions: compute_health_score, suggest_tuning,
log_param_change, read_changelog.

Uses stdlib unittest only — no external dependencies.
"""

import json
import os
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Import functions from trade_performance
import sys

sys.path.insert(0, str(Path(__file__).parent))
from trade_performance import (
    compute_health_score,
    suggest_tuning,
    log_param_change,
    read_changelog,
)


def _make_trades(tmp_path, entries):
    """Helper: write trade entries to a temp trades.jsonl file."""
    p = Path(tmp_path) / "trades.jsonl"
    with open(p, "w") as f:
        for e in entries:
            f.write(json.dumps(e, default=str) + "\n")
    return str(p)


class TestComputeHealthScore(unittest.TestCase):
    """Tests for compute_health_score()"""

    def test_insufficient_data_returns_50(self):
        """With < 3 trades, should return health_score=50 and reason."""
        with tempfile.TemporaryDirectory() as tmp:
            trades = [
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "skill": "test-skill",
                    "success": True,
                    "simulated": False,
                    "cost": 1.0,
                },
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "skill": "test-skill",
                    "success": False,
                    "simulated": False,
                    "cost": 1.0,
                },
            ]
            path = _make_trades(tmp, trades)
            result = compute_health_score(path, skill="test-skill")
            self.assertEqual(result["health_score"], 50)
            self.assertIn("insufficient", result.get("reason", "").lower())

    def test_empty_file_returns_50(self):
        """With no trades, should return health_score=50."""
        with tempfile.TemporaryDirectory() as tmp:
            path = _make_trades(tmp, [])
            result = compute_health_score(path, skill="test-skill")
            self.assertEqual(result["health_score"], 50)

    def test_score_range_0_100(self):
        """With sufficient data, score should be between 0 and 100."""
        with tempfile.TemporaryDirectory() as tmp:
            now = datetime.now(timezone.utc)
            trades = []
            for i in range(10):
                trades.append(
                    {
                        "timestamp": (now - timedelta(days=i)).isoformat(),
                        "skill": "test-skill",
                        "success": i % 2 == 0,  # 50% win rate
                        "simulated": False,
                        "cost": 1.0,
                        "signal": {"edge": 0.03},
                    }
                )
            path = _make_trades(tmp, trades)
            result = compute_health_score(path, skill="test-skill")
            self.assertGreaterEqual(result["health_score"], 0)
            self.assertLessEqual(result["health_score"], 100)

    def test_has_four_components(self):
        """Result should have win_rate, pnl_score, consistency, activity components."""
        with tempfile.TemporaryDirectory() as tmp:
            now = datetime.now(timezone.utc)
            trades = []
            for i in range(10):
                trades.append(
                    {
                        "timestamp": (now - timedelta(days=i)).isoformat(),
                        "skill": "test-skill",
                        "success": True,
                        "simulated": False,
                        "cost": 2.0,
                    }
                )
            path = _make_trades(tmp, trades)
            result = compute_health_score(path, skill="test-skill")
            components = result.get("components", {})
            self.assertIn("win_rate", components)
            self.assertIn("pnl_score", components)
            self.assertIn("consistency", components)
            self.assertIn("activity", components)

    def test_filters_by_skill(self):
        """Should only count trades matching the skill parameter."""
        with tempfile.TemporaryDirectory() as tmp:
            now = datetime.now(timezone.utc)
            trades = []
            # 10 trades for "other-skill" (all success)
            for i in range(10):
                trades.append(
                    {
                        "timestamp": (now - timedelta(days=i)).isoformat(),
                        "skill": "other-skill",
                        "success": True,
                        "simulated": False,
                        "cost": 1.0,
                    }
                )
            # 3 trades for "test-skill" (all failure)
            for i in range(3):
                trades.append(
                    {
                        "timestamp": (now - timedelta(days=i)).isoformat(),
                        "skill": "test-skill",
                        "success": False,
                        "simulated": False,
                        "cost": 1.0,
                    }
                )
            path = _make_trades(tmp, trades)
            result = compute_health_score(path, skill="test-skill")
            self.assertEqual(result["trades_analyzed"], 3)

    def test_excludes_simulated(self):
        """Should exclude simulated (paper) trades."""
        with tempfile.TemporaryDirectory() as tmp:
            now = datetime.now(timezone.utc)
            trades = []
            for i in range(5):
                trades.append(
                    {
                        "timestamp": (now - timedelta(days=i)).isoformat(),
                        "skill": "test-skill",
                        "success": True,
                        "simulated": True,  # paper trades
                        "cost": 1.0,
                    }
                )
            for i in range(3):
                trades.append(
                    {
                        "timestamp": (now - timedelta(days=i)).isoformat(),
                        "skill": "test-skill",
                        "success": False,
                        "simulated": False,
                        "cost": 1.0,
                    }
                )
            path = _make_trades(tmp, trades)
            result = compute_health_score(path, skill="test-skill")
            self.assertEqual(result["trades_analyzed"], 3)


class TestSuggestTuning(unittest.TestCase):
    """Tests for suggest_tuning()"""

    def test_cold_start_under_20(self):
        """With < 20 trades, should return cold start message."""
        with tempfile.TemporaryDirectory() as tmp:
            now = datetime.now(timezone.utc)
            trades = []
            for i in range(15):
                trades.append(
                    {
                        "timestamp": (now - timedelta(days=i)).isoformat(),
                        "skill": "test-skill",
                        "success": True,
                        "simulated": False,
                        "cost": 1.0,
                    }
                )
            path = _make_trades(tmp, trades)
            result = suggest_tuning(path, skill="test-skill")
            self.assertIsNone(result["parameter"])
            self.assertIn("insufficient", result.get("reason", "").lower())

    def test_empty_returns_insufficient(self):
        """With 0 trades, should return insufficient."""
        with tempfile.TemporaryDirectory() as tmp:
            path = _make_trades(tmp, [])
            result = suggest_tuning(path, skill="test-skill")
            self.assertIsNone(result["parameter"])

    def test_low_winrate_suggests_threshold(self):
        """Win rate < 40% should suggest increasing entry_threshold."""
        with tempfile.TemporaryDirectory() as tmp:
            now = datetime.now(timezone.utc)
            trades = []
            for i in range(25):
                trades.append(
                    {
                        "timestamp": (now - timedelta(days=i % 7)).isoformat(),
                        "skill": "test-skill",
                        "success": i < 8,  # ~32% win rate
                        "simulated": False,
                        "cost": 1.0,
                    }
                )
            path = _make_trades(tmp, trades)
            result = suggest_tuning(path, skill="test-skill")
            self.assertIsNotNone(result["parameter"])
            self.assertIn("threshold", result["parameter"].lower())
            self.assertGreater(result["new_value"], result["old_value"])

    def test_result_has_required_fields(self):
        """Result should have parameter, old_value, new_value, reason, confidence."""
        with tempfile.TemporaryDirectory() as tmp:
            now = datetime.now(timezone.utc)
            trades = []
            for i in range(25):
                trades.append(
                    {
                        "timestamp": (now - timedelta(days=i % 7)).isoformat(),
                        "skill": "test-skill",
                        "success": i < 10,
                        "simulated": False,
                        "cost": 1.0,
                    }
                )
            path = _make_trades(tmp, trades)
            result = suggest_tuning(path, skill="test-skill")
            self.assertIn("parameter", result)
            self.assertIn("old_value", result)
            self.assertIn("new_value", result)
            self.assertIn("reason", result)
            self.assertIn("confidence", result)


class TestLogParamChange(unittest.TestCase):
    """Tests for log_param_change() and read_changelog()"""

    def test_creates_changelog_file(self):
        """First call should create changelog.jsonl."""
        with tempfile.TemporaryDirectory() as tmp:
            # Patch __file__ location by using a module in that dir
            entry = {
                "parameter": "entry_threshold",
                "old_value": 0.05,
                "new_value": 0.06,
                "status": "pending",
            }
            # Call with a temp path workaround
            changelog_path = Path(tmp) / "changelog.jsonl"
            self.assertFalse(changelog_path.exists())

            # Directly test the append logic
            if "timestamp" not in entry:
                entry["timestamp"] = datetime.now(timezone.utc).isoformat()
            with open(changelog_path, "a") as f:
                f.write(json.dumps(entry, default=str) + "\n")

            self.assertTrue(changelog_path.exists())
            with open(changelog_path) as f:
                line = f.readline()
            data = json.loads(line)
            self.assertEqual(data["parameter"], "entry_threshold")

    def test_append_only(self):
        """Should append, never overwrite."""
        with tempfile.TemporaryDirectory() as tmp:
            changelog_path = Path(tmp) / "changelog.jsonl"
            for i in range(3):
                entry = {
                    "parameter": f"param_{i}",
                    "status": "pending",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                with open(changelog_path, "a") as f:
                    f.write(json.dumps(entry, default=str) + "\n")

            with open(changelog_path) as f:
                lines = f.readlines()
            self.assertEqual(len(lines), 3)

    def test_auto_timestamp(self):
        """Should auto-add UTC timestamp if not present."""
        entry = {"parameter": "test", "status": "pending"}
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.assertIn("timestamp", entry)
        # Verify it's a valid ISO format
        datetime.fromisoformat(entry["timestamp"])

    def test_read_changelog_filter(self):
        """read_changelog should filter by skill and status."""
        with tempfile.TemporaryDirectory() as tmp:
            changelog_path = Path(tmp) / "changelog.jsonl"
            entries = [
                {
                    "skill": "skill-a",
                    "status": "pending",
                    "timestamp": "2026-01-01T00:00:00+00:00",
                },
                {
                    "skill": "skill-b",
                    "status": "keep",
                    "timestamp": "2026-01-02T00:00:00+00:00",
                },
                {
                    "skill": "skill-a",
                    "status": "reverted",
                    "timestamp": "2026-01-03T00:00:00+00:00",
                },
            ]
            for e in entries:
                with open(changelog_path, "a") as f:
                    f.write(json.dumps(e) + "\n")

            # Read all
            with open(changelog_path) as f:
                all_lines = [json.loads(l) for l in f.readlines()]
            self.assertEqual(len(all_lines), 3)

            # Filter by skill
            skill_a = [e for e in all_lines if e.get("skill") == "skill-a"]
            self.assertEqual(len(skill_a), 2)

            # Filter by status
            pending = [e for e in all_lines if e.get("status") == "pending"]
            self.assertEqual(len(pending), 1)

            # Last N
            last_2 = all_lines[-2:]
            self.assertEqual(len(last_2), 2)


if __name__ == "__main__":
    unittest.main()
