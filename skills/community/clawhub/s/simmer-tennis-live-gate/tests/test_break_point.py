"""Unit tests for the three-valued break-point derivation. No network."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tennis_live_gate_skill import derive_break_point  # noqa: E402


class TestDeriveBreakPoint(unittest.TestCase):
    def test_receiver_at_ad_is_break_point(self):
        # server=1, so receiver is p2 (index 1); AD -> break point
        score = {"server": 1, "points": ["40", "AD"], "is_tiebreak": False}
        self.assertIs(derive_break_point(score), True)

    def test_receiver_at_40_server_at_30_is_break_point(self):
        score = {"server": 1, "points": ["30", "40"], "is_tiebreak": False}
        self.assertIs(derive_break_point(score), True)

    def test_receiver_at_40_server_at_40_is_not_break_point(self):
        # deuce -> receiver at 40 but server also at 40 -> not a break point
        score = {"server": 1, "points": ["40", "40"], "is_tiebreak": False}
        self.assertIs(derive_break_point(score), False)

    def test_server_perspective_swaps_with_server_2(self):
        # server=2 -> receiver is p1 (index 0)
        score = {"server": 2, "points": ["AD", "40"], "is_tiebreak": False}
        self.assertIs(derive_break_point(score), True)

    def test_tiebreak_is_never_break_point(self):
        score = {"server": 1, "points": ["6", "5"], "is_tiebreak": True}
        self.assertIs(derive_break_point(score), False)

    def test_null_server_is_undef(self):
        score = {"server": None, "points": ["40", "AD"], "is_tiebreak": False}
        self.assertIsNone(derive_break_point(score))

    def test_null_points_is_undef(self):
        score = {"server": 1, "points": [None, None], "is_tiebreak": False}
        self.assertIsNone(derive_break_point(score))

    def test_missing_points_is_undef(self):
        score = {"server": 1, "is_tiebreak": False}
        self.assertIsNone(derive_break_point(score))

    def test_empty_or_none_score_is_undef(self):
        self.assertIsNone(derive_break_point(None))
        self.assertIsNone(derive_break_point({}))

    def test_not_a_break_point_when_receiver_below_40(self):
        score = {"server": 1, "points": ["30", "15"], "is_tiebreak": False}
        self.assertIs(derive_break_point(score), False)


if __name__ == "__main__":
    unittest.main()
