#!/usr/bin/env python3
"""Regression tests for evidence verification.

Run: python3 test_verification.py    (stdlib only, no pytest, no network)

These exist because the check they cover shipped inverted from 1.0.0 through
1.2.0: it rated a verbatim quote on a normal page *below* a fabricated claim
on a short page, so the badge that is this tool's entire differentiating
claim was not just wrong but backwards, on every report, silently.

The invariant that failure violated, and that every test here defends:

    A claim's score must depend on whether the claim is in the page.
    It must not depend on how long the page is.

If you change the matcher, these must still pass. If a test here starts
looking inconvenient, that is the test doing its job.
"""

from __future__ import annotations

import unittest

from signal_scout_core import (
    QUOTED_THRESHOLD,
    SUPPORTED_THRESHOLD,
    TIER_LOW_MATCH,
    TIER_UNSUPPORTED,
    TIER_UNVERIFIED,
    TIER_VERIFIED,
    evidence_signals,
    tier_for_evidence,
)

QUOTE = (
    "We've been tracking inventory in a giant Google Sheet for two years and it takes "
    "about six hours every single week to reconcile. It keeps breaking and I'm losing my mind."
)
# Same claim, reworded — a legitimate research summary, not a fabrication.
PARAPHRASE_OF_QUOTE = (
    "The poster spends roughly six hours weekly reconciling inventory kept in a giant "
    "Google Sheet, and says it keeps breaking."
)
# Plausible, specific, and entirely invented. The failure mode that matters:
# it is *about* the same subject as the page, so topicality alone won't catch it.
FABRICATION = (
    "The poster said they evaluated NetSuite and Fishbowl but rejected both because of "
    "the seat-based pricing model."
)
NOISE = "Navigation Home About Pricing Blog Contact Sign up Log in. Related discussions. "


def page_of(size: int, *, containing: str = "") -> str:
    """A page of roughly `size` characters of chrome, optionally with a real
    thread body embedded in it — the shape of any actual source page."""
    pad = NOISE * max(1, size // len(NOISE) // 2)
    return f"{pad}{containing}{pad}"


PAGE_SIZES = (500, 2_000, 10_000, 40_000, 120_000)


class TestPageLengthIndependence(unittest.TestCase):
    """The exact defect from 1.0.0-1.2.0."""

    def test_verbatim_evidence_verifies_at_every_page_size(self):
        for size in PAGE_SIZES:
            with self.subTest(page_size=size):
                tier, _, quoted, _ = tier_for_evidence(QUOTE, page_of(size, containing=QUOTE))
                self.assertEqual(tier, TIER_VERIFIED)
                self.assertGreaterEqual(quoted, QUOTED_THRESHOLD)

    def test_fabricated_evidence_never_verifies_at_any_page_size(self):
        for size in PAGE_SIZES:
            with self.subTest(page_size=size):
                tier, _, _, _ = tier_for_evidence(FABRICATION, page_of(size, containing=QUOTE))
                self.assertEqual(tier, TIER_UNSUPPORTED)

    def test_score_is_stable_as_page_grows(self):
        """The old metric's score collapsed ~100x between a small and a large
        page for identical evidence. Containment must barely move."""
        scores = [evidence_signals(QUOTE, page_of(s, containing=QUOTE))[0] for s in PAGE_SIZES]
        self.assertLess(max(scores) - min(scores), 0.05, f"score drifted with page length: {scores}")


class TestInversion(unittest.TestCase):
    """The old code ranked these two backwards. This is the whole bug in one test."""

    def test_real_quote_on_long_page_beats_fabrication_on_short_page(self):
        real_quoted, _ = evidence_signals(QUOTE, page_of(40_000, containing=QUOTE))
        fake_quoted, _ = evidence_signals(FABRICATION, page_of(500))
        self.assertGreater(
            real_quoted, fake_quoted,
            "a true claim on a long page must outrank an invented claim on a short page",
        )


class TestTierBoundaries(unittest.TestCase):
    def test_paraphrase_is_supported_not_accused(self):
        """A reworded real signal must never be called fabricated — that's a
        false accusation against honest research, and it would train the agent
        to pad `evidence` with padding text to game the matcher."""
        tier, _, _, topical = tier_for_evidence(
            PARAPHRASE_OF_QUOTE, page_of(40_000, containing=QUOTE)
        )
        self.assertNotEqual(tier, TIER_UNSUPPORTED)
        self.assertGreater(topical, SUPPORTED_THRESHOLD)

    def test_fabrication_scores_zero_on_both_signals(self):
        quoted, topical = evidence_signals(FABRICATION, page_of(20_000, containing=QUOTE))
        self.assertLess(quoted, SUPPORTED_THRESHOLD)
        self.assertLess(topical, SUPPORTED_THRESHOLD)

    def test_empty_page_is_a_fetch_failure_not_a_fabrication(self):
        """A JS-rendered or gated page yields no text. Calling that 'fabricated'
        would blame the research for our fetch problem."""
        tier, _, _, _ = tier_for_evidence(QUOTE, "")
        self.assertEqual(tier, TIER_UNVERIFIED)

    def test_short_page_is_a_fetch_failure_not_a_fabrication(self):
        tier, _, _, _ = tier_for_evidence(QUOTE, "Enable JavaScript to continue.")
        self.assertEqual(tier, TIER_UNVERIFIED)

    def test_empty_evidence_is_unverified(self):
        tier, _, _, _ = tier_for_evidence("", page_of(20_000, containing=QUOTE))
        self.assertEqual(tier, TIER_UNVERIFIED)


class TestSpecifics(unittest.TestCase):
    """A made-up detail about a real company shares the company's name with the
    page, so it clears the topical signal. Its specifics are what give it away."""

    ACME_PAGE = (
        "Acme Robotics builds warehouse picking arms for mid-size retailers. "
        "The company has added engineers across its Austin office this year. "
    ) * 4

    def test_fabricated_funding_round_on_a_real_company_is_unsupported(self):
        tier, note, _, _ = tier_for_evidence("Acme Robotics raised a $12M Series A led by Sequoia", self.ACME_PAGE)
        self.assertEqual(tier, TIER_UNSUPPORTED)
        self.assertIn("Sequoia", note)
        self.assertIn("12", note)

    def test_wrong_number_in_a_quote_is_unsupported(self):
        page = "We raised a $15M Series A led by Sequoia last spring. " * 10
        self.assertEqual(tier_for_evidence("raised a $12M Series A led by Sequoia", page)[0], TIER_UNSUPPORTED)

    def test_wrong_scale_is_unsupported(self):
        page = "We raised a $40 million Series B led by Northwind last spring. " * 10
        tier, note, _, _ = tier_for_evidence("raised a $40 billion Series B led by Northwind", page)
        self.assertEqual(tier, TIER_UNSUPPORTED)
        self.assertIn("40 billion", note)

    def test_wrong_one_letter_identifier_is_unsupported(self):
        page = "We raised a $40 million Series B led by Northwind last spring. " * 10
        tier, note, _, _ = tier_for_evidence("raised a $40 million Series C led by Northwind", page)
        self.assertEqual(tier, TIER_UNSUPPORTED)
        self.assertIn("Series C", note)

    def test_formatting_differences_are_not_missing_specifics(self):
        page = "We raised a $12 million Series A led by Sequoia last spring. " * 10
        for evidence in ("raised a $12M Series A led by Sequoia", "raised a $12.0 million Series A led by Sequoia"):
            self.assertEqual(tier_for_evidence(evidence, page)[0], TIER_VERIFIED, evidence)

    def test_paraphrase_with_its_specifics_on_the_page_stays_low_match(self):
        tier, _, _, _ = tier_for_evidence("Acme is adding engineering staff in Austin", self.ACME_PAGE)
        self.assertEqual(tier, TIER_LOW_MATCH)

    def test_sentence_initial_word_is_not_a_name(self):
        tier, note, _, _ = tier_for_evidence(
            "Acme Robotics builds warehouse picking arms for mid-size retailers. "
            "Moreover the company has added engineers.",
            self.ACME_PAGE,
        )
        self.assertNotEqual(tier, TIER_UNSUPPORTED, note)

    def test_invented_name_opening_a_later_sentence_is_unsupported(self):
        tier, note, _, _ = tier_for_evidence(
            "Acme Robotics builds warehouse picking arms for mid-size retailers. Sequoia led the round.",
            self.ACME_PAGE,
        )
        self.assertEqual(tier, TIER_UNSUPPORTED, note)


if __name__ == "__main__":
    unittest.main(verbosity=2)
