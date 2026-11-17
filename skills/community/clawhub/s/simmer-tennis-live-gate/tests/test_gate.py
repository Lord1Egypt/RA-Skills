"""Unit tests for the live-tennis-state gate decision. No network."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tennis_live_gate_skill import (  # noqa: E402
    MatchState,
    STATUS_COMPLETED,
    STATUS_INTERRUPTED,
    STATUS_LIVE,
    STATUS_RETIRED,
    STATUS_WALKOVER,
    live_tennis_state_gate,
)


def _state(status=STATUS_LIVE, score=None, age_s=0.0, match_id=42):
    return MatchState(
        match_id=match_id,
        status=status,
        score=score if score is not None else {"server": 1, "points": ["30", "15"], "is_tiebreak": False, "timestamp": "t"},
        as_of="t",
        age_s=age_s,
    )


class TestGate(unittest.TestCase):
    def test_clean_live_state_is_allowed_full_size(self):
        d = live_tennis_state_gate(_state())
        self.assertTrue(d.allowed)
        self.assertEqual(d.size_factor, 1.0)
        self.assertEqual(d.reason, "ok")

    def test_none_state_fails_closed(self):
        d = live_tennis_state_gate(None)
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "state_unavailable")
        self.assertEqual(d.size_factor, 0.0)

    def test_missing_match_id_fails_closed(self):
        d = live_tennis_state_gate(_state(match_id=None))
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "state_unavailable")

    def test_retired_skips(self):
        d = live_tennis_state_gate(_state(status=STATUS_RETIRED))
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "retirement")

    def test_walkover_skips(self):
        d = live_tennis_state_gate(_state(status=STATUS_WALKOVER))
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "retirement")

    def test_interrupted_skips(self):
        d = live_tennis_state_gate(_state(status=STATUS_INTERRUPTED))
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "interrupted")

    def test_completed_skips_as_not_live(self):
        d = live_tennis_state_gate(_state(status=STATUS_COMPLETED))
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "match_not_live")

    def test_stale_snapshot_fails_closed(self):
        d = live_tennis_state_gate(_state(age_s=999.0), max_staleness_s=120.0)
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "state_stale")
        self.assertTrue(d.stale)

    def test_undetermined_break_point_fails_closed(self):
        score = {"server": None, "points": [None, None], "is_tiebreak": False, "timestamp": "t"}
        d = live_tennis_state_gate(_state(score=score))
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "state_undetermined")

    def test_live_break_point_skips_by_default(self):
        score = {"server": 1, "points": ["30", "40"], "is_tiebreak": False, "timestamp": "t"}
        d = live_tennis_state_gate(_state(score=score))
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "break_point_live")
        self.assertIs(d.break_point, True)

    def test_live_break_point_downsizes_when_factor_set(self):
        score = {"server": 1, "points": ["30", "40"], "is_tiebreak": False, "timestamp": "t"}
        d = live_tennis_state_gate(_state(score=score), break_point_size_factor=0.5)
        self.assertTrue(d.allowed)
        self.assertEqual(d.size_factor, 0.5)
        self.assertEqual(d.reason, "break_point_downsize")

    def test_break_point_ignored_when_skip_disabled(self):
        score = {"server": 1, "points": ["30", "40"], "is_tiebreak": False, "timestamp": "t"}
        d = live_tennis_state_gate(_state(score=score), skip_on_break_point=False)
        self.assertTrue(d.allowed)
        self.assertEqual(d.reason, "ok")
        self.assertEqual(d.size_factor, 1.0)

    def test_no_age_means_not_stale(self):
        # age_s None (no timestamp) should not trip the staleness gate.
        d = live_tennis_state_gate(_state(age_s=None))
        self.assertTrue(d.allowed)


if __name__ == "__main__":
    unittest.main()
