import copy
import json
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


class ForecastOddsConversionTests(unittest.TestCase):
    def assertAlmostEqualFloat(self, actual, expected):
        self.assertAlmostEqual(actual, expected, places=9)

    def test_odds_to_decimal_requires_explicit_format(self):
        with self.assertRaises(ValueError):
            forecast.odds_to_decimal("1.80", None)

    def test_decimal_odds_to_decimal(self):
        self.assertAlmostEqualFloat(forecast.odds_to_decimal("1.80", "decimal"), 1.8)

    def test_american_negative_odds_to_decimal(self):
        self.assertAlmostEqualFloat(forecast.odds_to_decimal("-150", "american"), 1.6666666666666665)

    def test_american_positive_odds_to_decimal(self):
        self.assertAlmostEqualFloat(forecast.odds_to_decimal("+240", "american"), 3.4)

    def test_fractional_odds_to_decimal(self):
        self.assertAlmostEqualFloat(forecast.odds_to_decimal("4/5", "fractional"), 1.8)

    def test_hong_kong_odds_to_decimal(self):
        self.assertAlmostEqualFloat(forecast.odds_to_decimal("0.92", "hong_kong"), 1.92)

    def test_malay_negative_odds_to_decimal(self):
        self.assertAlmostEqualFloat(forecast.odds_to_decimal("-0.85", "malay"), 2.1764705882352944)

    def test_indonesian_negative_odds_to_decimal(self):
        self.assertAlmostEqualFloat(forecast.odds_to_decimal("-1.20", "indonesian"), 1.8333333333333335)

    def test_invalid_odds_value_raises(self):
        with self.assertRaises(ValueError):
            forecast.odds_to_decimal("bad", "decimal")

    def test_ambiguous_format_raises(self):
        with self.assertRaises(ValueError):
            forecast.odds_to_decimal("1.80", "water")


class ForecastProbabilityTests(unittest.TestCase):
    def assertAlmostEqualFloat(self, actual, expected):
        self.assertAlmostEqual(actual, expected, places=9)

    def test_implied_probability_decimal(self):
        self.assertAlmostEqualFloat(forecast.implied_probability("1.80", "decimal"), 1.0 / 1.8)

    def test_implied_probability_american_negative(self):
        self.assertAlmostEqualFloat(forecast.implied_probability("-150", "american"), 150.0 / 250.0)

    def test_implied_probability_american_positive(self):
        self.assertAlmostEqualFloat(forecast.implied_probability("+240", "american"), 100.0 / 340.0)

    def test_implied_probability_fractional(self):
        self.assertAlmostEqualFloat(forecast.implied_probability("4/5", "fractional"), 1.0 / 1.8)

    def test_implied_probability_hong_kong(self):
        self.assertAlmostEqualFloat(forecast.implied_probability("0.92", "hong_kong"), 1.0 / 1.92)

    def test_implied_probability_malay_negative(self):
        self.assertAlmostEqualFloat(forecast.implied_probability("-0.85", "malay"), 1.0 / 2.1764705882352944)

    def test_implied_probability_indonesian_negative(self):
        self.assertAlmostEqualFloat(forecast.implied_probability("-1.20", "indonesian"), 1.0 / 1.8333333333333335)


class ForecastCliCompatibilityTests(unittest.TestCase):
    def test_legacy_cli_fixture_runs(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "forecast.py"),
                "--input",
                str(ROOT / "examples" / "legacy-match.json"),
                "--pretty",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload["matches"]), 1)
        match = payload["matches"][0]
        self.assertEqual(match["match"], "Argentina vs Netherlands")
        self.assertEqual(match["favorite"], "Argentina")
        self.assertIn("market_read", match)
        self.assertIn("asian_handicap", match["market_read"])


class ConsensusTests(unittest.TestCase):
    def assertAlmostEqualFloat(self, actual, expected, places=9):
        self.assertAlmostEqual(actual, expected, places=places)

    def make_quote(
        self,
        bookmaker,
        selection,
        odds,
        *,
        source_tier="B",
        source="direct",
        underlying_bookmaker=None,
        observed_at="2026-07-11T12:00:00+00:00",
        snapshot="current",
        period="90m",
        market="1x2",
        line=None,
        odds_format="decimal",
    ):
        return {
            "bookmaker": bookmaker,
            "underlying_bookmaker": underlying_bookmaker or bookmaker,
            "selection": selection,
            "odds": odds,
            "odds_format": odds_format,
            "source": source,
            "source_tier": source_tier,
            "observed_at": observed_at,
            "snapshot": snapshot,
            "period": period,
            "market": market,
            "line": line,
        }

    def test_devig_probabilities_power_method_three_way_market(self):
        probabilities = forecast.devig_probabilities([1 / 1.70, 1 / 3.80, 1 / 5.80], method="power")
        self.assertAlmostEqualFloat(sum(probabilities), 1.0, places=9)
        self.assertGreater(probabilities[0], probabilities[1])
        self.assertGreater(probabilities[1], probabilities[2])

    def test_deduplicate_quotes_prefers_higher_tier_direct_book(self):
        quotes = [
            self.make_quote(
                "Aggregator feed",
                "home",
                "1.82",
                source="aggregator",
                source_tier="C",
                underlying_bookmaker="Book A",
            ),
            self.make_quote(
                "Book A",
                "home",
                "1.80",
                source="direct",
                source_tier="B",
                underlying_bookmaker="Book A",
                observed_at="2026-07-11T12:01:00+00:00",
            ),
        ]

        deduped, diagnostics = forecast.deduplicate_quotes(quotes)

        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0]["bookmaker"], "Book A")
        self.assertEqual(deduped[0]["source"], "direct")
        self.assertEqual(diagnostics["duplicates_removed"], 1)

    def test_aggregator_quote_requires_underlying_bookmaker(self):
        for underlying_bookmaker in (None, "", "   "):
            with self.subTest(underlying_bookmaker=underlying_bookmaker):
                quote = self.make_quote(
                    "Aggregator feed",
                    "home",
                    "1.82",
                    source="aggregator",
                    source_tier="C",
                )
                if underlying_bookmaker is None:
                    quote.pop("underlying_bookmaker")
                else:
                    quote["underlying_bookmaker"] = underlying_bookmaker

                with self.assertRaisesRegex(ValueError, "underlying_bookmaker is required"):
                    forecast.deduplicate_quotes([quote])

    def test_build_consensus_for_five_complete_current_books(self):
        as_of = datetime(2026, 7, 11, 12, 0, tzinfo=timezone.utc)
        books = {
            "Book A": {"home": "1.72", "draw": "3.85", "away": "5.60"},
            "Book B": {"home": "1.70", "draw": "3.80", "away": "5.80"},
            "Book C": {"home": "1.74", "draw": "3.78", "away": "5.70"},
            "Book D": {"home": "1.71", "draw": "3.82", "away": "5.75"},
            "Book E": {"home": "1.73", "draw": "3.76", "away": "5.65"},
        }
        quotes = []
        for index, (bookmaker, selections) in enumerate(books.items()):
            observed_at = (as_of - timedelta(minutes=index * 4)).isoformat()
            for selection, odds in selections.items():
                quotes.append(
                    self.make_quote(
                        bookmaker,
                        selection,
                        odds,
                        observed_at=observed_at,
                        source_tier="B",
                    )
                )

        consensus = forecast.build_consensus(quotes, as_of=as_of)
        market = consensus["1x2|90m|None|current"]

        self.assertEqual(market["independent_books"], 5)
        self.assertAlmostEqual(sum(market["probabilities"].values()), 1.0, places=6)
        self.assertIn("dispersion", market)
        self.assertIn("mad", market["dispersion"])

    def test_build_consensus_supports_team_vs_team_to_qualify_market(self):
        quotes = [
            self.make_quote("Book A", "Argentina", "1.62", market="to_qualify"),
            self.make_quote("Book A", "Netherlands", "2.35", market="to_qualify"),
            self.make_quote("Book B", "Argentina", "1.65", market="to_qualify"),
            self.make_quote("Book B", "Netherlands", "2.30", market="to_qualify"),
        ]

        consensus = forecast.build_consensus(quotes)
        market = consensus["to_qualify|90m|None|current"]

        self.assertEqual(set(market["probabilities"]), {"argentina", "netherlands"})
        self.assertAlmostEqual(sum(market["probabilities"].values()), 1.0, places=6)
        self.assertTrue(market["unvigged"])
        self.assertTrue(market["completeness"]["anchor_ready"])

    def test_build_consensus_leaves_probabilities_empty_when_only_incomplete_books_exist(self):
        quotes = [
            self.make_quote("Book A", "home", "1.45"),
            self.make_quote("Book B", "home", "1.40"),
            self.make_quote("Book C", "home", "1.42"),
        ]

        consensus = forecast.build_consensus(quotes)
        market = consensus["1x2|90m|None|current"]

        self.assertFalse(market["completeness"]["anchor_ready"])
        self.assertEqual(market["probabilities"], {})

    def test_build_consensus_ignores_incomplete_books_when_complete_anchor_exists(self):
        complete_quotes = [
            self.make_quote("Book A", "home", "1.72"),
            self.make_quote("Book A", "draw", "3.85"),
            self.make_quote("Book A", "away", "5.60"),
            self.make_quote("Book B", "home", "1.70"),
            self.make_quote("Book B", "draw", "3.80"),
            self.make_quote("Book B", "away", "5.80"),
        ]
        with_incomplete = complete_quotes + [
            self.make_quote("Book C", "home", "1.15", source_tier="A"),
            self.make_quote("Book D", "home", "1.12", source_tier="A"),
        ]

        anchored_only = forecast.build_consensus(complete_quotes)["1x2|90m|None|current"]
        anchored_with_incomplete = forecast.build_consensus(with_incomplete)["1x2|90m|None|current"]

        self.assertTrue(anchored_with_incomplete["completeness"]["anchor_ready"])
        self.assertEqual(anchored_with_incomplete["probabilities"], anchored_only["probabilities"])

    def test_build_consensus_exposes_usable_complete_books(self):
        quotes = [
            self.make_quote("Book A", "home", "1.72"),
            self.make_quote("Book A", "draw", "3.85"),
            self.make_quote("Book A", "away", "5.60"),
            self.make_quote("Book B", "home", "1.70"),
        ]

        market = forecast.build_consensus(quotes)["1x2|90m|None|current"]

        self.assertEqual(market.get("usable_books"), ["Book A"])
        self.assertEqual(market.get("usable_book_count"), 1)
        self.assertEqual(market["independent_books"], 2)

    def test_build_consensus_raw_source_count_uses_pre_dedup_quote_total(self):
        quotes = [
            self.make_quote(
                "Aggregator feed",
                "home",
                "1.82",
                source="aggregator",
                source_tier="C",
                underlying_bookmaker="Book A",
            ),
            self.make_quote("Book A", "home", "1.80", underlying_bookmaker="Book A"),
            self.make_quote("Book A", "draw", "3.60", underlying_bookmaker="Book A"),
            self.make_quote("Book A", "away", "4.80", underlying_bookmaker="Book A"),
        ]

        market = forecast.build_consensus(quotes)["1x2|90m|None|current"]

        self.assertEqual(market["raw_source_count"], 4)
        self.assertEqual(market["independent_books"], 1)
        self.assertEqual(market["deduplication"]["raw_quotes"], 4)
        self.assertEqual(market["deduplication"]["kept_quotes"], 3)
        self.assertEqual(market["deduplication"]["duplicates_removed"], 1)

    def test_build_consensus_rejects_mixed_qualification_selection_schemes(self):
        quotes = [
            self.make_quote("Book A", "yes", "1.70", market="to_qualify"),
            self.make_quote("Book A", "no", "2.10", market="to_qualify"),
            self.make_quote("Book B", "Argentina", "1.68", market="to_qualify"),
            self.make_quote("Book B", "Netherlands", "2.20", market="to_qualify"),
        ]

        with self.assertRaises(ValueError):
            forecast.build_consensus(quotes)

    def test_build_consensus_excludes_zero_mad_outlier_and_keeps_diagnostic(self):
        common_quotes = []
        for bookmaker in ("Book A", "Book B", "Book C", "Book D"):
            common_quotes.extend(
                [
                    self.make_quote(bookmaker, "home", "1.90"),
                    self.make_quote(bookmaker, "draw", "3.60"),
                    self.make_quote(bookmaker, "away", "4.80"),
                ]
            )
        rogue_quotes = common_quotes + [
            self.make_quote("Rogue", "home", "1.20", source_tier="A"),
            self.make_quote("Rogue", "draw", "8.00", source_tier="A"),
            self.make_quote("Rogue", "away", "12.00", source_tier="A"),
        ]

        market = forecast.build_consensus(rogue_quotes)["1x2|90m|None|current"]

        self.assertTrue(
            any(
                entry["bookmaker"] == "Rogue" and entry["candidate"] and entry["excluded"]
                for entry in market["outliers"]
            )
        )

    def test_build_consensus_canonicalizes_totals_line_and_rejects_invalid_required_line(self):
        quotes = [
            self.make_quote("Book A", "over", "1.95", market="totals", line=2.5),
            self.make_quote("Book A", "under", "1.90", market="totals", line=2.5),
            self.make_quote("Book B", "over", "1.94", market="totals", line="2.5"),
            self.make_quote("Book B", "under", "1.91", market="totals", line="2.5"),
        ]

        consensus = forecast.build_consensus(quotes)
        self.assertEqual(list(consensus), ["totals|90m|2.5|current"])
        self.assertEqual(consensus["totals|90m|2.5|current"]["independent_books"], 2)

        bad_quotes = list(quotes)
        bad_quotes[0] = self.make_quote("Book A", "over", "1.95", market="totals", line="bad")
        with self.assertRaises(ValueError):
            forecast.build_consensus(bad_quotes)

    def test_build_consensus_rejects_non_mirrored_asian_handicap_lines(self):
        cases = {
            "same_sign": [
                self.make_quote("Book A", "home", "1.95", market="asian_handicap", line=-0.75),
                self.make_quote("Book A", "away", "1.91", market="asian_handicap", line=-0.75),
            ],
            "different_absolute_lines": [
                self.make_quote("Book A", "home", "1.95", market="asian_handicap", line=-0.75),
                self.make_quote("Book A", "away", "1.91", market="asian_handicap", line=1.0),
            ],
            "missing_mirror": [
                self.make_quote("Book A", "home", "1.95", market="asian_handicap", line=-0.75),
            ],
        }

        for case, quotes in cases.items():
            with self.subTest(case=case):
                with self.assertRaisesRegex(ValueError, "mirrored home/away lines"):
                    forecast.build_consensus(quotes)

    def test_deduplicate_quotes_breaks_exact_ties_deterministically_under_reversal(self):
        direct_quote = self.make_quote(
            "Book A",
            "home",
            "1.80",
            source="direct",
            underlying_bookmaker="Book A",
        )
        aggregator_quote = self.make_quote(
            "Aggregator feed",
            "home",
            "1.82",
            source="aggregator",
            underlying_bookmaker="Book A",
        )

        forward, _ = forecast.deduplicate_quotes([aggregator_quote, direct_quote])
        reverse, _ = forecast.deduplicate_quotes([direct_quote, aggregator_quote])

        self.assertEqual(forward[0]["source"], "direct")
        self.assertEqual(reverse[0]["source"], "direct")
        self.assertEqual(forward[0]["bookmaker"], reverse[0]["bookmaker"])


class ScoreModelTests(unittest.TestCase):
    def assertSettlementSumsToOne(self, settlement):
        self.assertEqual(
            set(settlement),
            {"win", "half_win", "push", "half_loss", "loss"},
        )
        self.assertAlmostEqual(sum(settlement.values()), 1.0, places=9)

    def assertSettlementBuckets(self, settlement, **expected):
        self.assertSettlementSumsToOne(settlement)
        for bucket, value in expected.items():
            self.assertAlmostEqual(settlement[bucket], value, places=9)

    def make_market(
        self,
        market,
        probabilities,
        *,
        period="90m",
        line=None,
        snapshot="current",
        independent_books=5,
        dispersion=None,
        anchor_ready=True,
        unvigged=True,
    ):
        if dispersion is None:
            dispersion = {key: 0.015 for key in probabilities}
        return {
            "market": market,
            "period": period,
            "line": line,
            "snapshot": snapshot,
            "probabilities": dict(probabilities),
            "independent_books": independent_books,
            "dispersion": {"mad": dict(dispersion)},
            "completeness": {"anchor_ready": anchor_ready},
            "unvigged": unvigged,
        }

    def make_consensus(self, *, one_x_two=None, total_over=None, btts_yes=None):
        consensus = {}
        if one_x_two is not None:
            consensus["1x2|90m|None|current"] = self.make_market(
                "1x2",
                one_x_two,
                dispersion={"home": 0.015, "draw": 0.012, "away": 0.01},
            )
        if total_over is not None:
            consensus["totals|90m|2.5|current"] = self.make_market(
                "totals",
                {"over": total_over, "under": 1.0 - total_over},
                line="2.5",
                independent_books=4,
                dispersion={"over": 0.014, "under": 0.014},
            )
        if btts_yes is not None:
            consensus["btts|90m|None|current"] = self.make_market(
                "btts",
                {"yes": btts_yes, "no": 1.0 - btts_yes},
                independent_books=3,
                dispersion={"yes": 0.02, "no": 0.02},
            )
        return consensus

    def test_poisson_prob_rejects_invalid_inputs(self):
        for rate in (-0.1, float("nan"), float("inf"), "bad", None):
            with self.subTest(rate=rate):
                with self.assertRaises((TypeError, ValueError)):
                    forecast.poisson_prob(rate, 1)

        for goals in (-1, 1.5, "2", None):
            with self.subTest(goals=goals):
                with self.assertRaises((TypeError, ValueError)):
                    forecast.poisson_prob(1.2, goals)

    def test_score_matrix_is_normalized(self):
        matrix = forecast.poisson_matrix(1.60, 0.90, max_goals=10)
        self.assertAlmostEqual(sum(sum(row) for row in matrix), 1.0, places=9)

    def test_poisson_matrix_rejects_invalid_inputs(self):
        with self.assertRaises((TypeError, ValueError)):
            forecast.poisson_matrix(1.0, 1.0, max_goals=-1)
        with self.assertRaises((TypeError, ValueError)):
            forecast.poisson_matrix(1.0, float("nan"), max_goals=10)

    def test_model_metrics_are_coherent(self):
        metrics = forecast.metrics_from_matrix(forecast.poisson_matrix(1.60, 0.90, 10))
        self.assertAlmostEqual(metrics["home"] + metrics["draw"] + metrics["away"], 1.0, places=9)
        self.assertGreater(metrics["home"], metrics["away"])
        self.assertGreater(metrics["under_3_5"], metrics["under_2_5"])
        self.assertAlmostEqual(metrics["btts_yes"] + metrics["btts_no"], 1.0, places=9)
        self.assertIn("home_win_by_1", metrics)
        self.assertIn("away_win_by_2_plus", metrics)

    def test_metrics_reject_malformed_matrix(self):
        for matrix in (
            [],
            [[]],
            [[0.5, 0.5], [0.25]],
            [[0.5, -0.1], [0.2, 0.4]],
            [[0.5, float("nan")], [0.2, 0.3]],
        ):
            with self.subTest(matrix=matrix):
                with self.assertRaises((TypeError, ValueError)):
                    forecast.metrics_from_matrix(matrix)

    def test_quarter_handicap_has_half_outcomes(self):
        settlement = forecast.settle_asian_handicap(
            forecast.poisson_matrix(1.50, 1.00, 10),
            side="home",
            line=-0.25,
        )
        self.assertGreater(settlement["half_win"] + settlement["half_loss"], 0.0)
        self.assertSettlementSumsToOne(settlement)

    def test_quarter_handicap_combines_win_and_push_to_half_win(self):
        matrix = [
            [0.0, 0.0],
            [0.5, 0.5],
        ]
        settlement = forecast.settle_asian_handicap(matrix, side="home", line=0.25)

        self.assertAlmostEqual(settlement["half_win"], 0.5, places=9)
        self.assertAlmostEqual(settlement["win"], 0.5, places=9)
        self.assertAlmostEqual(settlement["push"], 0.0, places=9)
        self.assertAlmostEqual(settlement["half_loss"], 0.0, places=9)
        self.assertAlmostEqual(settlement["loss"], 0.0, places=9)

    def test_away_quarter_handicap_supports_positive_and_negative_lines(self):
        matrix = [
            [0.2, 0.3],
            [0.1, 0.4],
        ]

        away_plus = forecast.settle_asian_handicap(matrix, side="away", line=0.25)
        away_minus = forecast.settle_asian_handicap(matrix, side="away", line=-0.25)

        self.assertSettlementBuckets(
            away_plus,
            win=0.3,
            half_win=0.6,
            push=0.0,
            half_loss=0.0,
            loss=0.1,
        )
        self.assertSettlementBuckets(
            away_minus,
            win=0.3,
            half_win=0.0,
            push=0.0,
            half_loss=0.6,
            loss=0.1,
        )

    def test_total_settlement_supports_push_and_quarter_lines(self):
        matrix = [
            [0.0, 0.3, 0.0],
            [0.0, 0.0, 0.0],
            [0.7, 0.0, 0.0],
        ]

        push = forecast.settle_total(matrix, side="under", line=2.0)
        quarter = forecast.settle_total(matrix, side="under", line=2.25)

        self.assertAlmostEqual(push["push"], 0.7, places=9)
        self.assertSettlementSumsToOne(push)
        self.assertAlmostEqual(quarter["half_win"], 0.7, places=9)
        self.assertAlmostEqual(quarter["win"], 0.3, places=9)
        self.assertAlmostEqual(quarter["push"], 0.0, places=9)
        self.assertSettlementSumsToOne(quarter)

    def test_over_total_settlement_supports_push_and_quarter_lines(self):
        matrix = [
            [0.0, 0.3, 0.0],
            [0.0, 0.0, 0.0],
            [0.7, 0.0, 0.0],
        ]

        push = forecast.settle_total(matrix, side="over", line=2.0)
        quarter = forecast.settle_total(matrix, side="over", line=2.25)

        self.assertSettlementBuckets(
            push,
            win=0.0,
            half_win=0.0,
            push=0.7,
            half_loss=0.0,
            loss=0.3,
        )
        self.assertSettlementBuckets(
            quarter,
            win=0.0,
            half_win=0.0,
            push=0.0,
            half_loss=0.7,
            loss=0.3,
        )

    def test_selection_probability_from_settlement_excludes_pushes_and_weights_half_outcomes(self):
        matrix = [
            [0.0, 0.1, 0.2],
            [0.0, 0.2, 0.3],
            [0.0, 0.0, 0.2],
        ]
        expectations = {
            2.0: 1.0 / 6.0,
            2.25: 0.375,
            2.5: 0.5,
            3.0: 5.0 / 7.0,
        }

        for line, expected in expectations.items():
            with self.subTest(line=line):
                settlement = forecast.settle_total(matrix, side="under", line=line)
                self.assertAlmostEqual(
                    forecast._selection_probability_from_settlement(settlement),
                    expected,
                    places=9,
                )

    def test_selection_probability_from_settlement_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            forecast._selection_probability_from_settlement({"win": 0.0, "half_win": 0.0, "push": 1.0, "half_loss": 0.0, "loss": 0.0})
        with self.assertRaises(ValueError):
            forecast._selection_probability_from_settlement({"win": 0.5, "half_win": 0.0, "push": 0.5, "half_loss": 0.0})

    def test_settlement_rejects_invalid_arguments(self):
        matrix = forecast.poisson_matrix(1.2, 0.8, 8)
        with self.assertRaises((TypeError, ValueError)):
            forecast.settle_asian_handicap(matrix, side="draw", line=0.0)
        with self.assertRaises((TypeError, ValueError)):
            forecast.settle_total(matrix, side="middle", line=2.5)
        with self.assertRaises((TypeError, ValueError)):
            forecast.settle_total(matrix, side="over", line="bad")

    def test_fit_expected_goals_matches_fixture_and_is_deterministic(self):
        consensus = self.make_consensus(
            one_x_two={"home": 0.58, "draw": 0.24, "away": 0.18},
            total_over=0.51,
            btts_yes=0.48,
        )

        first = forecast.fit_expected_goals(consensus)
        second = forecast.fit_expected_goals(consensus)

        self.assertEqual(first, second)
        self.assertGreater(first["home_xg"], first["away_xg"])
        self.assertGreaterEqual(first["home_xg"], 0.15)
        self.assertLessEqual(first["home_xg"], 4.0)
        self.assertGreaterEqual(first["away_xg"], 0.15)
        self.assertLessEqual(first["away_xg"], 4.0)
        self.assertLess(first["residual"], 0.03)
        self.assertAlmostEqual(first["metrics"]["home"] + first["metrics"]["draw"] + first["metrics"]["away"], 1.0, places=9)
        self.assertIn("objective", first)
        self.assertIn("diagnostics", first)

    def test_fit_expected_goals_does_not_expose_mutable_cached_metrics(self):
        consensus = self.make_consensus(
            one_x_two={"home": 0.58, "draw": 0.24, "away": 0.18},
            total_over=0.51,
            btts_yes=0.48,
        )
        baseline = forecast.fit_expected_goals(consensus)
        expected_rates = (baseline["home_xg"], baseline["away_xg"])
        expected_residual = baseline["residual"]
        expected_metrics = dict(baseline["metrics"])

        baseline["metrics"]["home"] = -1.0
        repeated = forecast.fit_expected_goals(consensus)

        self.assertEqual((repeated["home_xg"], repeated["away_xg"]), expected_rates)
        self.assertEqual(repeated["residual"], expected_residual)
        self.assertEqual(repeated["metrics"], expected_metrics)
        self.assertIsNot(repeated["metrics"], baseline["metrics"])

    def test_fit_expected_goals_grid_cache_tracks_current_constants(self):
        original = (forecast.FIT_GRID_MIN, forecast.FIT_GRID_MAX, forecast.FIT_GRID_STEP)
        try:
            forecast.FIT_GRID_MIN = 1.0
            forecast.FIT_GRID_MAX = 1.1
            forecast.FIT_GRID_STEP = 0.05
            fit = forecast.fit_expected_goals(
                self.make_consensus(one_x_two={"home": 0.40, "draw": 0.30, "away": 0.30})
            )
        finally:
            forecast.FIT_GRID_MIN, forecast.FIT_GRID_MAX, forecast.FIT_GRID_STEP = original

        self.assertEqual(fit["diagnostics"]["grid"]["candidates"], 3)
        self.assertGreaterEqual(fit["home_xg"], 1.0)
        self.assertLessEqual(fit["home_xg"], 1.1)
        self.assertGreaterEqual(fit["away_xg"], 1.0)
        self.assertLessEqual(fit["away_xg"], 1.1)

    def test_fit_expected_goals_ignores_opening_and_non_90m_groups(self):
        baseline = self.make_consensus(
            one_x_two={"home": 0.58, "draw": 0.24, "away": 0.18},
            total_over=0.51,
            btts_yes=0.48,
        )
        with_ignored_groups = dict(baseline)
        with_ignored_groups["1x2|90m|None|opening"] = self.make_market(
            "1x2",
            {"home": 0.20, "draw": 0.20, "away": 0.60},
            snapshot="opening",
            dispersion={"home": 0.001, "draw": 0.001, "away": 0.001},
        )
        with_ignored_groups["totals|1st_half|2.5|current"] = self.make_market(
            "totals",
            {"over": 0.90, "under": 0.10},
            period="1st_half",
            line="2.5",
            dispersion={"over": 0.001, "under": 0.001},
        )

        baseline_fit = forecast.fit_expected_goals(baseline)
        filtered_fit = forecast.fit_expected_goals(with_ignored_groups)

        self.assertEqual(
            (
                baseline_fit["home_xg"],
                baseline_fit["away_xg"],
                baseline_fit["residual"],
            ),
            (
                filtered_fit["home_xg"],
                filtered_fit["away_xg"],
                filtered_fit["residual"],
            ),
        )
        self.assertEqual(baseline_fit["diagnostics"]["family_weights"], filtered_fit["diagnostics"]["family_weights"])
        self.assertEqual(len(baseline_fit["diagnostics"]["targets"]), len(filtered_fit["diagnostics"]["targets"]))

    def test_fit_expected_goals_roundtrips_fair_totals_targets(self):
        home_xg = 1.8
        away_xg = 0.9
        matrix = forecast.poisson_matrix(home_xg, away_xg, 10)
        metrics = forecast.metrics_from_matrix(matrix)

        for line in (2.0, 2.25, 3.0):
            with self.subTest(line=line):
                total_over = forecast._selection_probability_from_settlement(
                    forecast.settle_total(matrix, side="over", line=line)
                )
                consensus = self.make_consensus(
                    one_x_two={
                        "home": metrics["home"],
                        "draw": metrics["draw"],
                        "away": metrics["away"],
                    },
                    btts_yes=metrics["btts_yes"],
                )
                consensus[f"totals|90m|{line}|current"] = self.make_market(
                    "totals",
                    {"over": total_over, "under": 1.0 - total_over},
                    line=str(line),
                    independent_books=4,
                    dispersion={"over": 0.014, "under": 0.014},
                )

                fit = forecast.fit_expected_goals(consensus)
                fitted_total = forecast._selection_probability_from_settlement(
                    forecast.settle_total(
                        forecast.poisson_matrix(fit["home_xg"], fit["away_xg"], 10),
                        side="over",
                        line=line,
                    )
                )

                self.assertAlmostEqual(fitted_total, total_over, places=9)
                self.assertLess(fit["residual"], 1e-9)

    def test_fit_expected_goals_family_weights_respect_caps(self):
        fit = forecast.fit_expected_goals(
            self.make_consensus(
                one_x_two={"home": 0.58, "draw": 0.24, "away": 0.18},
                total_over=0.51,
                btts_yes=0.48,
            )
        )

        targets = fit["diagnostics"]["targets"]
        family_weights = fit["diagnostics"]["family_weights"]

        for family, cap in forecast.FIT_FAMILY_CAPS.items():
            with self.subTest(family=family):
                self.assertLessEqual(family_weights[family], cap)
                summed_weight = sum(target["weight"] for target in targets if target["family"] == family)
                self.assertLessEqual(summed_weight, cap)
                self.assertAlmostEqual(summed_weight, family_weights[family], places=9)

    def test_fit_expected_goals_lower_quality_reduces_family_weight(self):
        strong = forecast.fit_expected_goals(
            {
                "1x2|90m|None|current": self.make_market(
                    "1x2",
                    {"home": 0.58, "draw": 0.24, "away": 0.18},
                    independent_books=5,
                    dispersion={"home": 0.015, "draw": 0.012, "away": 0.01},
                )
            }
        )
        low_coverage = forecast.fit_expected_goals(
            {
                "1x2|90m|None|current": self.make_market(
                    "1x2",
                    {"home": 0.58, "draw": 0.24, "away": 0.18},
                    independent_books=1,
                    dispersion={"home": 0.015, "draw": 0.012, "away": 0.01},
                )
            }
        )
        high_dispersion = forecast.fit_expected_goals(
            {
                "1x2|90m|None|current": self.make_market(
                    "1x2",
                    {"home": 0.58, "draw": 0.24, "away": 0.18},
                    independent_books=5,
                    dispersion={"home": 0.08, "draw": 0.08, "away": 0.08},
                )
            }
        )

        strong_weight = strong["diagnostics"]["family_weights"]["1x2"]
        self.assertGreater(strong_weight, low_coverage["diagnostics"]["family_weights"]["1x2"])
        self.assertGreater(strong_weight, high_dispersion["diagnostics"]["family_weights"]["1x2"])

    def test_fit_expected_goals_rejects_invalid_consensus_provenance_and_probability_maps(self):
        invalid_markets = [
            self.make_market("1x2", {"home": 0.9, "draw": 0.9, "away": 0.9}),
            self.make_market("btts", {"yes": 0.8, "no": 0.8}),
            self.make_market("totals", {"over": 0.8, "under": 0.8}, line="2.5"),
            dict(self.make_market("1x2", {"home": 0.58, "draw": 0.24, "away": 0.18}), unvigged=False),
            dict(self.make_market("1x2", {"home": 0.58, "draw": 0.24, "away": 0.18}), unvigged="yes"),
            {
                key: value
                for key, value in self.make_market("1x2", {"home": 0.58, "draw": 0.24, "away": 0.18}).items()
                if key != "unvigged"
            },
            dict(self.make_market("1x2", {"home": 0.58, "draw": 0.24, "away": 0.18}), completeness={"anchor_ready": False}),
            dict(self.make_market("1x2", {"home": 0.58, "draw": 0.24, "away": 0.18}), completeness={"anchor_ready": "true"}),
            {
                key: value
                for key, value in self.make_market("1x2", {"home": 0.58, "draw": 0.24, "away": 0.18}).items()
                if key != "completeness"
            },
            self.make_market("totals", {"over": 0.51}, line="2.5"),
        ]

        for index, market in enumerate(invalid_markets):
            with self.subTest(index=index, market=market.get("market")):
                with self.assertRaisesRegex(ValueError, "no valid current 90m 1X2, totals, or BTTS targets"):
                    forecast.fit_expected_goals({f"market-{index}": market})

    def test_fit_expected_goals_tolerates_missing_families(self):
        consensus = self.make_consensus(one_x_two={"home": 0.50, "draw": 0.27, "away": 0.23})

        fit = forecast.fit_expected_goals(consensus)

        self.assertGreaterEqual(fit["home_xg"], 0.15)
        self.assertLessEqual(fit["away_xg"], 4.0)
        self.assertLessEqual(fit["residual"], 0.1)

    def test_fit_expected_goals_accepts_build_consensus_output(self):
        quotes = []
        books = {
            "Book A": {
                "1x2": {"home": "1.72", "draw": "3.85", "away": "5.60"},
                "totals": {"over": "1.95", "under": "1.90"},
                "btts": {"yes": "1.98", "no": "1.82"},
            },
            "Book B": {
                "1x2": {"home": "1.70", "draw": "3.80", "away": "5.80"},
                "totals": {"over": "1.94", "under": "1.91"},
                "btts": {"yes": "2.00", "no": "1.80"},
            },
            "Book C": {
                "1x2": {"home": "1.74", "draw": "3.78", "away": "5.70"},
                "totals": {"over": "1.96", "under": "1.89"},
                "btts": {"yes": "1.97", "no": "1.83"},
            },
        }
        for bookmaker, markets in books.items():
            for selection, odds in markets["1x2"].items():
                quotes.append(
                    {
                        "bookmaker": bookmaker,
                        "underlying_bookmaker": bookmaker,
                        "selection": selection,
                        "odds": odds,
                        "odds_format": "decimal",
                        "source": "direct",
                        "source_tier": "B",
                        "observed_at": "2026-07-11T12:00:00+00:00",
                        "snapshot": "current",
                        "period": "90m",
                        "market": "1x2",
                        "line": None,
                    }
                )
            for selection, odds in markets["totals"].items():
                quotes.append(
                    {
                        "bookmaker": bookmaker,
                        "underlying_bookmaker": bookmaker,
                        "selection": selection,
                        "odds": odds,
                        "odds_format": "decimal",
                        "source": "direct",
                        "source_tier": "B",
                        "observed_at": "2026-07-11T12:00:00+00:00",
                        "snapshot": "current",
                        "period": "90m",
                        "market": "totals",
                        "line": "2.5",
                    }
                )
            for selection, odds in markets["btts"].items():
                quotes.append(
                    {
                        "bookmaker": bookmaker,
                        "underlying_bookmaker": bookmaker,
                        "selection": selection,
                        "odds": odds,
                        "odds_format": "decimal",
                        "source": "direct",
                        "source_tier": "B",
                        "observed_at": "2026-07-11T12:00:00+00:00",
                        "snapshot": "current",
                        "period": "90m",
                        "market": "btts",
                        "line": None,
                    }
                )

        consensus = forecast.build_consensus(quotes)
        fit = forecast.fit_expected_goals(consensus)

        self.assertGreater(fit["home_xg"], fit["away_xg"])
        self.assertLess(fit["residual"], 0.1)

    def test_fit_expected_goals_rejects_missing_supported_targets(self):
        with self.assertRaises(ValueError):
            forecast.fit_expected_goals(
                {
                    "to_qualify|90m|None|current": {
                        "market": "to_qualify",
                        "period": "90m",
                        "line": None,
                        "snapshot": "current",
                        "probabilities": {"argentina": 0.6, "netherlands": 0.4},
                        "independent_books": 5,
                        "dispersion": {"mad": {}},
                        "completeness": {"anchor_ready": True},
                    }
                }
            )


class EvidenceTests(unittest.TestCase):
    def base_score_kwargs(self):
        return {
            "independent_books": 5,
            "freshest_age_minutes": 10,
            "market_families": 5,
            "max_dispersion": 0.02,
            "fit_residual": 0.02,
            "lineup_confirmed": True,
            "match_started": False,
            "has_live_quotes": False,
            "match_type": "league_or_group",
        }

    def test_classify_movement_strengthened_price_and_asian_line(self):
        result = forecast.classify_movement(0.55, 0.59, -0.75, -1.0)

        self.assertEqual(result["price_direction"], "strengthened")
        self.assertEqual(result["asian_direction"], "strengthened")
        self.assertAlmostEqual(result["probability_change_pp"], 4.0, places=9)

    def test_score_evidence_abstains_when_match_started_without_live_quotes(self):
        evidence = forecast.score_evidence(
            independent_books=5,
            freshest_age_minutes=10,
            market_families=5,
            max_dispersion=0.02,
            fit_residual=0.02,
            lineup_confirmed=True,
            match_started=True,
            has_live_quotes=False,
            match_type="league_or_group",
        )

        self.assertTrue(evidence["abstain"])
        self.assertIn("already_started", evidence["abstain_reasons"])

    def test_score_evidence_category_maximums_sum_to_100_and_high_boundary(self):
        evidence = forecast.score_evidence(**self.base_score_kwargs())

        self.assertEqual(sum(evidence["components"].values()), 100)
        self.assertEqual(evidence["score"], 100)
        self.assertEqual(evidence["label"], "high")

    def test_score_evidence_label_boundaries_are_deterministic(self):
        medium = forecast.score_evidence(
            independent_books=2,
            freshest_age_minutes=10,
            market_families=5,
            max_dispersion=0.07,
            fit_residual=0.09,
            lineup_confirmed=False,
            match_started=False,
            has_live_quotes=False,
            match_type="league_or_group",
            near_kickoff=False,
        )
        low = forecast.score_evidence(
            independent_books=2,
            freshest_age_minutes=180,
            market_families=5,
            max_dispersion=0.06,
            fit_residual=0.09,
            lineup_confirmed=False,
            match_started=False,
            has_live_quotes=False,
            match_type="league_or_group",
            near_kickoff=False,
        )

        self.assertEqual(medium["score"], 50)
        self.assertEqual(medium["label"], "medium")
        self.assertEqual(low["score"], 49)
        self.assertEqual(low["label"], "low")

    def test_score_evidence_abstains_with_fewer_than_three_books(self):
        evidence = forecast.score_evidence(**{**self.base_score_kwargs(), "independent_books": 2})

        self.assertTrue(evidence["abstain"])
        self.assertEqual(evidence["abstain_reasons"], ["insufficient_books"])

    def test_score_evidence_stale_near_kickoff_can_be_disabled(self):
        stale = forecast.score_evidence(
            **{**self.base_score_kwargs(), "freshest_age_minutes": 61}
        )
        allowed = forecast.score_evidence(
            **{**self.base_score_kwargs(), "freshest_age_minutes": 61, "near_kickoff": False}
        )

        self.assertTrue(stale["abstain"])
        self.assertEqual(stale["abstain_reasons"], ["stale_near_kickoff"])
        self.assertFalse(allowed["abstain"])
        self.assertEqual(allowed["abstain_reasons"], [])

    def test_score_evidence_friendly_penalty_subtracts_10(self):
        evidence = forecast.score_evidence(**{**self.base_score_kwargs(), "match_type": "friendly"})

        self.assertEqual(evidence["score"], 90)
        self.assertEqual(evidence["penalties"], {"friendly": 10})

    def test_validate_match_context_requires_aggregate_score_for_two_leg_second(self):
        errors = forecast.validate_match_context(
            {
                "match_type": "two_leg_second",
                "teams": ["Argentina", "Netherlands"],
            }
        )

        self.assertEqual(errors, ["aggregate_score_required"])

    def test_validate_match_context_treats_whitespace_aggregate_score_as_missing(self):
        errors = forecast.validate_match_context(
            {
                "match_type": "two_leg_second",
                "teams": ["Argentina", "Netherlands"],
                "aggregate_score": "   ",
            }
        )

        self.assertEqual(errors, ["aggregate_score_required"])

    def test_validate_match_context_requires_second_leg_tiebreak_rules(self):
        errors = forecast.validate_match_context(
            {
                "match_type": "two_leg_second",
                "teams": ["Argentina", "Netherlands"],
                "aggregate_score": "1-1",
            }
        )

        self.assertEqual(errors, ["tiebreak_rules_required"])

    def test_validate_match_context_rejects_invalid_match_type(self):
        errors = forecast.validate_match_context(
            {
                "match_type": "round_robin",
                "teams": ["Argentina", "Netherlands"],
            }
        )

        self.assertEqual(errors, ["invalid_match_type"])

    def test_score_evidence_abstains_on_ambiguous_match_identity(self):
        evidence = forecast.score_evidence(
            **{
                **self.base_score_kwargs(),
                "match": {
                    "match_type": "league_or_group",
                    "teams": ["Argentina", "Argentina"],
                },
            }
        )

        self.assertTrue(evidence["abstain"])
        self.assertEqual(evidence["abstain_reasons"], ["ambiguous_match"])

    def test_score_evidence_maps_invalid_context_errors_to_invalid_context(self):
        evidence = forecast.score_evidence(
            **{
                **self.base_score_kwargs(),
                "match": {
                    "match_type": "two_leg_second",
                    "teams": ["Argentina", "Netherlands"],
                },
            }
        )

        self.assertTrue(evidence["abstain"])
        self.assertEqual(evidence["abstain_reasons"], ["invalid_context"])

    def test_score_evidence_maps_whitespace_aggregate_score_to_invalid_context(self):
        evidence = forecast.score_evidence(
            **{
                **self.base_score_kwargs(),
                "match": {
                    "match_type": "two_leg_second",
                    "teams": ["Argentina", "Netherlands"],
                    "aggregate_score": "   ",
                },
            }
        )

        self.assertTrue(evidence["abstain"])
        self.assertEqual(evidence["abstain_reasons"], ["invalid_context"])

    def test_score_evidence_invalid_nonfinite_metrics_cannot_raise_score(self):
        evidence = forecast.score_evidence(
            independent_books=-5,
            freshest_age_minutes=float("nan"),
            market_families=-2,
            max_dispersion=float("inf"),
            fit_residual=float("nan"),
            lineup_confirmed=False,
            match_started=False,
            has_live_quotes=False,
            match_type="league_or_group",
            near_kickoff=False,
        )

        self.assertEqual(evidence["score"], 0)
        self.assertEqual(
            evidence["components"],
            {
                "independent_books": 0,
                "freshness": 0,
                "market_families": 0,
                "dispersion": 0,
                "agreement": 0,
                "lineup": 0,
            },
        )

    def test_score_evidence_rejects_bool_numeric_metrics_and_abstains(self):
        evidence = forecast.score_evidence(
            independent_books=True,
            freshest_age_minutes=10,
            market_families=True,
            max_dispersion=False,
            fit_residual=True,
            lineup_confirmed=False,
            match_started=False,
            has_live_quotes=False,
            match_type="league_or_group",
            near_kickoff=False,
        )

        self.assertEqual(evidence["components"]["independent_books"], 0)
        self.assertEqual(evidence["components"]["market_families"], 0)
        self.assertEqual(evidence["components"]["dispersion"], 0)
        self.assertEqual(evidence["components"]["agreement"], 0)
        self.assertTrue(evidence["abstain"])
        self.assertEqual(evidence["abstain_reasons"], ["insufficient_books"])

    def test_score_evidence_bool_freshness_is_worst_evidence_near_kickoff(self):
        evidence = forecast.score_evidence(
            **{**self.base_score_kwargs(), "freshest_age_minutes": True}
        )

        self.assertEqual(evidence["components"]["freshness"], 0)
        self.assertTrue(evidence["abstain"])
        self.assertEqual(evidence["abstain_reasons"], ["stale_near_kickoff"])

    def test_score_evidence_rejects_string_flags(self):
        for flag_name, value in (
            ("lineup_confirmed", "false"),
            ("match_started", "true"),
            ("has_live_quotes", "false"),
            ("near_kickoff", "true"),
        ):
            with self.subTest(flag_name=flag_name, value=value):
                kwargs = dict(self.base_score_kwargs())
                kwargs[flag_name] = value
                with self.assertRaisesRegex(ValueError, flag_name):
                    forecast.score_evidence(**kwargs)

    def test_score_evidence_rejects_numeric_flags(self):
        for flag_name in ("lineup_confirmed", "match_started", "has_live_quotes", "near_kickoff"):
            for value in (0, 1, 1.0):
                with self.subTest(flag_name=flag_name, value=value):
                    kwargs = dict(self.base_score_kwargs())
                    kwargs[flag_name] = value
                    with self.assertRaisesRegex(ValueError, flag_name):
                        forecast.score_evidence(**kwargs)

    def test_score_evidence_rejects_none_flags(self):
        for flag_name in ("lineup_confirmed", "match_started", "has_live_quotes", "near_kickoff"):
            with self.subTest(flag_name=flag_name):
                kwargs = dict(self.base_score_kwargs())
                kwargs[flag_name] = None
                with self.assertRaisesRegex(ValueError, flag_name):
                    forecast.score_evidence(**kwargs)

    def test_score_evidence_unknown_match_type_keeps_context_limitation_visible(self):
        evidence = forecast.score_evidence(**{**self.base_score_kwargs(), "match_type": "unknown"})

        self.assertFalse(evidence["abstain"])
        self.assertEqual(evidence["context_limitations"], ["unknown_match_type"])


class ForecastV2Tests(unittest.TestCase):
    def load_fixture(self):
        return json.loads((ROOT / "examples" / "multi-book-match.json").read_text(encoding="utf-8"))

    def analyze_fixture(self, payload=None, *, as_of=None):
        candidate = copy.deepcopy(self.load_fixture() if payload is None else payload)
        return forecast.analyze_v2_match(candidate, as_of=as_of)

    def test_multi_book_forecast_exposes_auditable_output(self):
        result = self.analyze_fixture()

        self.assertEqual(result["schema_version"], "2.0")
        self.assertGreaterEqual(result["source_coverage"]["independent_books"], 5)
        self.assertAlmostEqual(sum(result["probabilities_90m"].values()), 1.0, places=6)
        self.assertIn("expected_goals", result)
        self.assertEqual(len(result["score_ladder"]), 3)
        self.assertEqual(len({entry["score"] for entry in result["score_ladder"]}), 3)
        self.assertIn(result["confidence"]["label"], {"high", "medium", "low"})
        self.assertIn("changed", result["movement"])
        self.assertIn("unchanged", result["movement"])
        self.assertNotIn("current:to_qualify:qualification", result["missing_fields"])

    def test_v2_rejects_non_boolean_lineup_confirmed(self):
        for value in ("false", 1, 0, None):
            with self.subTest(value=value):
                payload = self.load_fixture()
                payload["lineup_confirmed"] = value

                with self.assertRaisesRegex(ValueError, "lineup_confirmed must be a bool"):
                    self.analyze_fixture(payload)

    def test_v2_uses_validated_false_lineup_in_output_and_evidence(self):
        payload = self.load_fixture()
        payload["lineup_confirmed"] = False

        result = self.analyze_fixture(payload)

        self.assertIs(result["lineup_confirmed"], False)
        self.assertEqual(result["confidence"]["components"]["lineup"], 0)

    def test_qualification_market_is_separate_from_90m_probabilities(self):
        baseline = self.analyze_fixture()
        payload = self.load_fixture()
        for quote in payload["quotes"]:
            if quote["market"] == "to_qualify":
                if quote["selection"] == "Argentina":
                    quote["odds"] = "3.30"
                if quote["selection"] == "Netherlands":
                    quote["odds"] = "1.34"

        mutated = self.analyze_fixture(payload)

        self.assertEqual(mutated["qualification"]["favorite"], "Netherlands")
        for selection, probability in baseline["probabilities_90m"].items():
            self.assertAlmostEqual(probability, mutated["probabilities_90m"][selection], places=6)

    def test_v2_explains_stronger_favorite_with_weaker_handicap(self):
        payload = self.load_fixture()
        for quote in payload["quotes"]:
            if quote["market"] != "asian_handicap":
                continue
            magnitude = "1.25" if quote["snapshot"] == "opening" else "0.75"
            quote["line"] = f"-{magnitude}" if quote["selection"] == "home" else magnitude

        result = self.analyze_fixture(payload)

        conflict = result["cross_market_conflicts"][0]
        self.assertEqual(conflict["code"], "favorite_win_but_cover_risk")
        self.assertEqual(conflict["favorite"], "Argentina")
        self.assertLess(
            abs(conflict["handicap_signal"]["current_line"]),
            abs(conflict["handicap_signal"]["opening_line"]),
        )
        self.assertIn("handicap weakened", conflict["read"])

    def test_source_coverage_excludes_opening_only_books(self):
        payload = self.load_fixture()
        payload["quotes"].extend(
            [
                {
                    "source": "direct",
                    "bookmaker": "Book F",
                    "market": "1x2",
                    "selection": "home",
                    "odds": "1.82",
                    "odds_format": "decimal",
                    "observed_at": "2026-07-18T11:59:00+00:00",
                    "period": "90m",
                    "source_tier": "B",
                    "snapshot": "opening",
                },
                {
                    "source": "direct",
                    "bookmaker": "Book F",
                    "market": "1x2",
                    "selection": "draw",
                    "odds": "3.66",
                    "odds_format": "decimal",
                    "observed_at": "2026-07-18T11:59:00+00:00",
                    "period": "90m",
                    "source_tier": "B",
                    "snapshot": "opening",
                },
                {
                    "source": "direct",
                    "bookmaker": "Book F",
                    "market": "1x2",
                    "selection": "away",
                    "odds": "5.00",
                    "odds_format": "decimal",
                    "observed_at": "2026-07-18T11:59:00+00:00",
                    "period": "90m",
                    "source_tier": "B",
                    "snapshot": "opening",
                },
            ]
        )

        result = self.analyze_fixture(payload)

        self.assertEqual(result["source_coverage"]["independent_books"], 5)

    def test_qualification_only_books_do_not_inflate_core_90m_coverage(self):
        payload = self.load_fixture()
        payload["quotes"] = [
            quote
            for quote in payload["quotes"]
            if quote["period"] == "qualification" or quote["bookmaker"] == "Book A"
        ]

        result = self.analyze_fixture(payload)

        coverage = result["source_coverage"]
        self.assertEqual(coverage["independent_books"], 1)
        self.assertEqual(coverage["qualification_independent_books"], 3)
        self.assertEqual(coverage["core_90m_books_by_family"]["1x2"], ["Book A"])
        self.assertEqual(coverage["confidence_market_families"], 0)
        self.assertEqual(result["confidence"]["components"]["market_families"], 0)
        self.assertTrue(result["abstention"]["abstain"])
        self.assertIn("insufficient_books", result["abstention"]["reasons"])

    def test_core_90m_coverage_does_not_union_disjoint_family_books(self):
        payload = self.load_fixture()
        family_book = {"1x2": "Book A", "totals": "Book B", "btts": "Book C"}
        payload["quotes"] = [
            quote
            for quote in payload["quotes"]
            if quote["market"] in family_book
            and quote["bookmaker"] == family_book[quote["market"]]
        ]

        result = self.analyze_fixture(payload)

        coverage = result["source_coverage"]
        self.assertEqual(coverage["independent_books"], 1)
        self.assertEqual(
            coverage["core_90m_books_by_family"],
            {"1x2": ["Book A"], "btts": ["Book C"], "totals": ["Book B"]},
        )
        self.assertEqual(coverage["confidence_market_families"], 0)
        self.assertEqual(result["confidence"]["components"]["market_families"], 0)
        self.assertIn("insufficient_books", result["abstention"]["reasons"])

    def test_already_started_without_live_quotes_abstains(self):
        result = self.analyze_fixture(as_of="2026-07-19T20:05:00+00:00")

        self.assertTrue(result["abstention"]["abstain"])
        self.assertIn("already_started", result["abstention"]["reasons"])

    def test_live_only_snapshots_are_rejected_as_unsupported(self):
        payload = self.load_fixture()
        for quote in payload["quotes"]:
            if quote["snapshot"] in {"current", "t-10min"}:
                quote["snapshot"] = "live"
                quote["observed_at"] = "2026-07-19T20:05:00+00:00"

        with self.assertRaisesRegex(ValueError, "live-only snapshots are unsupported"):
            self.analyze_fixture(payload, as_of="2026-07-19T20:05:00+00:00")

    def test_started_match_ignores_live_quotes_and_keeps_pre_match_abstention(self):
        payload = self.load_fixture()
        live_quotes = []
        for quote in payload["quotes"]:
            if quote["market"] == "1x2" and quote["snapshot"] == "current":
                live_quote = copy.deepcopy(quote)
                live_quote["snapshot"] = "live"
                live_quote["observed_at"] = "2026-07-19T20:05:00+00:00"
                live_quote["odds"] = "1.20" if quote["selection"] == "home" else "8.00"
                live_quotes.append(live_quote)
        payload["quotes"].extend(live_quotes)

        result = self.analyze_fixture(payload, as_of="2026-07-19T20:05:00+00:00")

        self.assertEqual(result["forecast_mode"], "frozen_pre_match")
        self.assertTrue(result["abstention"]["abstain"])
        self.assertIn("already_started", result["abstention"]["reasons"])
        self.assertEqual(result["diagnostics"]["live_quotes"]["provided"], len(live_quotes))
        self.assertEqual(result["diagnostics"]["live_quotes"]["used"], 0)
        self.assertIn("unsupported", result["diagnostics"]["live_quotes"]["policy"])

    def test_missing_market_diagnostics_report_missing_fields(self):
        payload = self.load_fixture()
        payload["quotes"] = [quote for quote in payload["quotes"] if quote["market"] != "btts"]

        result = self.analyze_fixture(payload)

        self.assertIn("current:btts:90m", result["missing_fields"])
        self.assertIn("current:btts:90m", result["diagnostics"]["missing_markets"])

    def test_missing_market_diagnostics_include_asian_handicap(self):
        payload = self.load_fixture()
        payload["quotes"] = [
            quote for quote in payload["quotes"] if quote["market"] != "asian_handicap"
        ]

        result = self.analyze_fixture(payload)

        missing = "current:asian_handicap:90m"
        self.assertIn(missing, result["missing_fields"])
        self.assertIn(missing, result["diagnostics"]["missing_markets"])

    def test_qualification_movement_uses_qualification_period(self):
        payload = self.load_fixture()
        opening_quotes = []
        for quote in payload["quotes"]:
            if quote["market"] != "to_qualify":
                continue
            opening = copy.deepcopy(quote)
            opening["snapshot"] = "opening"
            opening["observed_at"] = "2026-07-18T12:30:00+00:00"
            opening_quotes.append(opening)
        payload["quotes"].extend(opening_quotes)

        result = self.analyze_fixture(payload)

        qualification = [
            entry for entry in result["movement"]["unchanged"] if entry["market"] == "to_qualify"
        ]
        self.assertEqual(len(qualification), 1)
        self.assertEqual(qualification[0]["period"], "qualification")
        self.assertEqual(qualification[0]["to_snapshot"], "current")
        self.assertNotIn(
            "to_qualify",
            {entry["market"] for entry in result["movement"]["missing_snapshots"]},
        )

    def test_movement_uses_ten_minute_snapshot_when_current_is_missing(self):
        payload = self.load_fixture()
        opening_quotes = []
        for quote in payload["quotes"]:
            if quote["market"] != "to_qualify":
                continue
            quote["snapshot"] = "t-10min"
            quote["observed_at"] = "2026-07-19T19:50:00+00:00"
            opening = copy.deepcopy(quote)
            opening["snapshot"] = "opening"
            opening["observed_at"] = "2026-07-18T12:30:00+00:00"
            opening_quotes.append(opening)
        payload["quotes"].extend(opening_quotes)

        result = self.analyze_fixture(payload)

        qualification = [
            entry for bucket in ("changed", "unchanged")
            for entry in result["movement"][bucket]
            if entry["market"] == "to_qualify"
        ]
        self.assertEqual(len(qualification), 1)
        self.assertEqual(qualification[0]["period"], "qualification")
        self.assertEqual(qualification[0]["to_snapshot"], "t-10min")
        self.assertNotIn(
            "to_qualify",
            {entry["market"] for entry in result["movement"]["missing_snapshots"]},
        )

    def test_asian_handicap_line_moves_are_tracked_as_changed_not_missing(self):
        result = self.analyze_fixture()

        asian_movements = [entry for entry in result["movement"]["changed"] if entry["market"] == "asian_handicap"]

        self.assertEqual(len(asian_movements), 1)
        self.assertEqual(asian_movements[0]["line"], "1")
        self.assertEqual(asian_movements[0]["opening_line"], "0.75")
        self.assertNotIn(
            "asian_handicap",
            {entry["market"] for entry in result["movement"]["missing_snapshots"]},
        )
        self.assertEqual(result["asian_handicap"][0]["home_line"], -1.0)
        self.assertEqual(result["asian_handicap"][0]["away_line"], 1.0)

    def test_asian_handicap_preserves_home_underdog_direction(self):
        payload = self.load_fixture()
        for quote in payload["quotes"]:
            if quote["market"] == "asian_handicap":
                quote["line"] = str(-float(quote["line"]))

        result = self.analyze_fixture(payload)

        self.assertEqual(result["asian_handicap"][0]["line"], 1.0)
        self.assertEqual(result["asian_handicap"][0]["home_line"], 1.0)
        self.assertEqual(result["asian_handicap"][0]["away_line"], -1.0)

    def test_news_classification_does_not_change_mathematical_baseline(self):
        with_news = self.analyze_fixture()
        payload = self.load_fixture()
        payload.pop("news")
        without_news = self.analyze_fixture(payload)

        self.assertEqual(
            {entry["classification"] for entry in with_news["news"]},
            {"confirmed", "credible_unconfirmed", "narrative"},
        )
        self.assertEqual(with_news["probabilities_90m"], without_news["probabilities_90m"])
        self.assertEqual(with_news["expected_goals"], without_news["expected_goals"])

    def test_cli_routes_v2_and_propagates_as_of(self):
        as_of = "2026-07-19T19:55:00+00:00"
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "forecast.py"),
                "--input",
                str(ROOT / "examples" / "multi-book-match.json"),
                "--pretty",
                "--as-of",
                as_of,
                "--no-record",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload["matches"]), 1)
        match = payload["matches"][0]
        self.assertEqual(match["schema_version"], "2.0")
        self.assertEqual(match["as_of"], as_of)
        self.assertAlmostEqual(match["source_coverage"]["freshest_age_minutes"], 2.3333333333333335, places=6)

    def test_cli_supports_matches_wrapper_for_v2_objects(self):
        wrapped = {"matches": [self.load_fixture()]}
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
            json.dump(wrapped, handle)
            temp_path = handle.name
        self.addCleanup(lambda: Path(temp_path).unlink(missing_ok=True))

        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "forecast.py"),
                "--input",
                temp_path,
                "--no-record",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["matches"][0]["schema_version"], "2.0")


class ForecastRecordTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads((ROOT / "examples" / "multi-book-match.json").read_text(encoding="utf-8"))

    def test_record_has_explicit_periods_full_score_support_and_replay_input(self):
        match = self.load_fixture()
        analysis = forecast.analyze_v2_match(copy.deepcopy(match))
        record = analysis["forecast_record"]

        self.assertEqual(record["schema_version"], "1.0")
        self.assertEqual(record["markets"]["1x2"]["period"], "90m")
        self.assertEqual(record["markets"]["totals"][0]["period"], "90m")
        self.assertEqual(record["markets"]["btts"]["period"], "90m")
        self.assertEqual(record["markets"]["asian_handicap"][0]["period"], "90m")
        self.assertEqual(record["markets"]["qualification"]["period"], "qualification")
        self.assertEqual(len(record["score_distribution_90m"]), 121)
        self.assertAlmostEqual(sum(record["score_distribution_90m"].values()), 1.0, places=12)
        self.assertEqual(record["raw_match"], match)
        self.assertEqual(record["profile_id"], "v2-default")
        self.assertEqual(record["alert_offset"], "T-10min")

    def test_forecast_id_is_deterministic_and_input_sensitive(self):
        match = self.load_fixture()
        first = forecast.analyze_v2_match(copy.deepcopy(match))["forecast_record"]
        second = forecast.analyze_v2_match(copy.deepcopy(match))["forecast_record"]
        changed = copy.deepcopy(match)
        changed["quotes"][0]["odds"] = "1.79"
        third = forecast.analyze_v2_match(changed)["forecast_record"]

        self.assertEqual(first["forecast_id"], second["forecast_id"])
        self.assertEqual(first["event_id"], second["event_id"])
        self.assertNotEqual(first["forecast_id"], third["forecast_id"])
        self.assertEqual(first["event_id"], third["event_id"])

    def test_append_is_idempotent_and_rejects_same_id_with_different_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "forecasts.jsonl"
            record = {"forecast_id": "forecast-1", "schema_version": "1.0", "value": 1}

            self.assertTrue(forecast.append_unique_jsonl(path, record, "forecast_id"))
            self.assertFalse(forecast.append_unique_jsonl(path, copy.deepcopy(record), "forecast_id"))
            with self.assertRaisesRegex(ValueError, "conflicting"):
                forecast.append_unique_jsonl(path, {**record, "value": 2}, "forecast_id")
            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), 1)

    def test_batch_append_is_all_or_nothing_on_late_conflict(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "forecasts.jsonl"
            original = {"forecast_id": "forecast-1", "schema_version": "1.0", "value": 1}
            forecast.append_unique_jsonl(path, original, "forecast_id")
            before = path.read_bytes()

            with self.assertRaisesRegex(ValueError, "conflicting"):
                forecast.append_unique_jsonl_batch(
                    path,
                    [
                        {"forecast_id": "forecast-2", "schema_version": "1.0", "value": 2},
                        {**original, "value": 99},
                    ],
                    "forecast_id",
                )

            self.assertEqual(path.read_bytes(), before)

    def test_persistence_fails_closed_without_a_process_lock(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "forecasts.jsonl"
            record = {"forecast_id": "forecast-1", "schema_version": "1.0"}

            with (
                mock.patch.object(forecast, "fcntl", None),
                mock.patch.object(forecast, "msvcrt", None, create=True),
            ):
                with self.assertRaisesRegex(RuntimeError, "process lock"):
                    forecast.append_unique_jsonl(path, record, "forecast_id")

            self.assertFalse(path.exists())

    def test_atomic_replace_syncs_parent_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "forecasts.jsonl"
            record = {"forecast_id": "forecast-1", "schema_version": "1.0"}

            with mock.patch.object(forecast, "_fsync_directory", create=True) as sync_directory:
                forecast.append_unique_jsonl(path, record, "forecast_id")

            sync_directory.assert_called_once_with(path.parent)

    def test_cli_record_out_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "forecasts.jsonl"
            command = [
                sys.executable,
                str(ROOT / "scripts" / "forecast.py"),
                "--input",
                str(ROOT / "examples" / "multi-book-match.json"),
                "--record-out",
                str(path),
            ]

            first = subprocess.run(command, check=True, capture_output=True, text=True)
            second = subprocess.run(command, check=True, capture_output=True, text=True)

            self.assertEqual(
                json.loads(first.stdout)["matches"][0]["forecast_record"]["forecast_id"],
                json.loads(second.stdout)["matches"][0]["forecast_record"]["forecast_id"],
            )
            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), 1)

    def test_cli_uses_default_data_dir_and_record_out_takes_precedence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            default_dir = Path(tmpdir) / "default"
            environment = {**os.environ, "FOOTBALL_FORECASTER_DATA_DIR": str(default_dir)}
            base_command = [
                sys.executable,
                str(ROOT / "scripts" / "forecast.py"),
                "--input",
                str(ROOT / "examples" / "multi-book-match.json"),
            ]

            subprocess.run(base_command, check=True, capture_output=True, text=True, env=environment)
            self.assertTrue((default_dir / "forecasts.jsonl").is_file())

            second_default = Path(tmpdir) / "second-default"
            explicit = Path(tmpdir) / "explicit.jsonl"
            environment["FOOTBALL_FORECASTER_DATA_DIR"] = str(second_default)
            subprocess.run(
                [*base_command, "--record-out", str(explicit)],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertTrue(explicit.is_file())
            self.assertFalse((second_default / "forecasts.jsonl").exists())

    def test_cli_no_record_disables_default_ledger(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            environment = {**os.environ, "FOOTBALL_FORECASTER_DATA_DIR": tmpdir}
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "forecast.py"),
                    "--input",
                    str(ROOT / "examples" / "multi-book-match.json"),
                    "--no-record",
                ],
                check=False,
                capture_output=True,
                text=True,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertFalse((Path(tmpdir) / "forecasts.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
