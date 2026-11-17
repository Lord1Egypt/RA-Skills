"""Tests for state assembly and the end-to-end flow, all with injected
fixtures — no network, no SIMMER_API_KEY, no LIVETENNIS_API_KEY required."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tennis_live_gate_skill import (  # noqa: E402
    fetch_live_tennis_state,
    fold_name,
    run_one_market_with_live_gate,
)

_LIVE_MATCHES = [
    {
        "id": 7,
        "status": "live",
        "event_status": None,
        "players": {"p1": {"name": "Carlos Alcaraz"}, "p2": {"name": "Jannik Sinner"}},
    },
    {
        "id": 8,
        "status": "live",
        "event_status": None,
        "players": {"p1": {"name": "Coco Gauff"}, "p2": {"name": "Elena Rybakina"}},
    },
]


def _score_ok(_id):
    return {"server": 1, "points": ["30", "15"], "is_tiebreak": False, "timestamp": None}


def _match_ok(match_id):
    return next(m for m in _LIVE_MATCHES if m["id"] == match_id)


class TestFoldName(unittest.TestCase):
    def test_strips_diacritics_and_case(self):
        self.assertEqual(fold_name("Stéfanos Tsitsipás"), "stefanos tsitsipas")

    def test_collapses_punctuation(self):
        self.assertEqual(fold_name("Auger-Aliassime, Félix"), "auger aliassime felix")


class TestFetchState(unittest.TestCase):
    def test_resolves_match_order_insensitive(self):
        state = fetch_live_tennis_state(
            ["Jannik Sinner", "Carlos Alcaraz"],  # reversed order
            api_key="x",
            live_matches=_LIVE_MATCHES,
            score_fetch=_score_ok,
            match_fetch=_match_ok,
        )
        self.assertIsNotNone(state)
        self.assertEqual(state.match_id, 7)
        self.assertEqual(state.status, "live")

    def test_unknown_players_return_none(self):
        state = fetch_live_tennis_state(
            ["Nobody One", "Nobody Two"],
            api_key="x",
            live_matches=_LIVE_MATCHES,
            score_fetch=_score_ok,
            match_fetch=_match_ok,
        )
        self.assertIsNone(state)

    def test_retirement_event_status_maps_to_retired(self):
        matches = [
            {
                "id": 9,
                "status": "completed",
                "event_status": "Retired",
                "players": {"p1": {"name": "A Player"}, "p2": {"name": "B Player"}},
            }
        ]
        state = fetch_live_tennis_state(
            ["A Player", "B Player"],
            api_key="x",
            live_matches=matches,
            score_fetch=lambda _id: {"server": None, "points": [None, None], "timestamp": None},
            match_fetch=lambda _id: matches[0],
        )
        self.assertEqual(state.status, "retired")

    def test_staleness_age_computed_from_timestamp(self):
        matches = [_LIVE_MATCHES[0]]
        state = fetch_live_tennis_state(
            ["Carlos Alcaraz", "Jannik Sinner"],
            api_key="x",
            now=1_000_000.0,
            live_matches=matches,
            score_fetch=lambda _id: {
                "server": 1,
                "points": ["30", "15"],
                "is_tiebreak": False,
                "timestamp": "1970-01-12T13:46:40+00:00",  # epoch 1_000_000
            },
            match_fetch=_match_ok,
        )
        self.assertIsNotNone(state.age_s)
        self.assertAlmostEqual(state.age_s, 0.0, delta=1.0)


class TestEndToEndFlow(unittest.TestCase):
    def _size(self, p_win, market_price, bankroll):
        return round(bankroll * max(0.0, p_win - market_price), 2)

    def test_allowed_flow_returns_full_size(self):
        amount = run_one_market_with_live_gate(
            ["Carlos Alcaraz", "Jannik Sinner"],
            p_win=0.60,
            market_price=0.50,
            bankroll=1000.0,
            api_key="x",
            live_matches=_LIVE_MATCHES,
            score_fetch=_score_ok,
            match_fetch=_match_ok,
            size_position_fn=self._size,
        )
        self.assertAlmostEqual(amount, 100.0, places=2)

    def test_break_point_flow_returns_zero(self):
        amount = run_one_market_with_live_gate(
            ["Carlos Alcaraz", "Jannik Sinner"],
            p_win=0.60,
            market_price=0.50,
            bankroll=1000.0,
            api_key="x",
            live_matches=_LIVE_MATCHES,
            score_fetch=lambda _id: {"server": 1, "points": ["30", "40"], "is_tiebreak": False, "timestamp": None},
            match_fetch=_match_ok,
            size_position_fn=self._size,
        )
        self.assertEqual(amount, 0.0)

    def test_break_point_downsize_flow_halves_size(self):
        amount = run_one_market_with_live_gate(
            ["Carlos Alcaraz", "Jannik Sinner"],
            p_win=0.60,
            market_price=0.50,
            bankroll=1000.0,
            api_key="x",
            break_point_size_factor=0.5,
            live_matches=_LIVE_MATCHES,
            score_fetch=lambda _id: {"server": 1, "points": ["30", "40"], "is_tiebreak": False, "timestamp": None},
            match_fetch=_match_ok,
            size_position_fn=self._size,
        )
        self.assertAlmostEqual(amount, 50.0, places=2)

    def test_no_match_flow_returns_zero(self):
        amount = run_one_market_with_live_gate(
            ["Nobody One", "Nobody Two"],
            p_win=0.60,
            market_price=0.50,
            bankroll=1000.0,
            api_key="x",
            live_matches=_LIVE_MATCHES,
            score_fetch=_score_ok,
            match_fetch=_match_ok,
            size_position_fn=self._size,
        )
        self.assertEqual(amount, 0.0)


if __name__ == "__main__":
    unittest.main()
