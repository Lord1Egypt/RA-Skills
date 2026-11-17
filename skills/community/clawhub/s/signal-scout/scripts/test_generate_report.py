#!/usr/bin/env python3
"""Regression tests for generate_report.py's novelty badges and history auto-detection.

Run: python3 test_generate_report.py    (stdlib only)

generate_report.py reuses diff_reports.py's own history accumulation and
outcome index (accumulate_history, load_prospects, OutcomeIndex) instead of
reimplementing "have we seen this prospect before" a second time. These tests
check that reuse actually wires up end to end: sibling analysis-*.json files
are auto-detected by the SKILL.md storage convention, new/recurring/
resurfacing prospects are classified the same way diff_reports.py itself
would, and the HTML output actually contains the badge markup rather than
just annotating the in-memory dict.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import generate_report


def individual(name: str, source_url: str, score: int = 70, **extra) -> dict:
    base = {
        "name": name,
        "source_url": source_url,
        "score": score,
        "stage": "Problem aware",
        "pain_signal": "some pain",
        "dimensions": {
            "pain_strength": 4, "product_fit": 4, "timing": 3,
            "reachability": 3, "evidence_quality": 4,
        },
    }
    base.update(extra)
    return base


def snapshot(generated_at: str, individuals: list[dict]) -> dict:
    return {"generated_at": generated_at, "individuals": individuals}


class TestHistoryDiscovery(unittest.TestCase):
    def test_discovers_sibling_analysis_files_excluding_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            current = tmp_path / "analysis-2026-07-16.json"
            prior = tmp_path / "analysis-2026-07-01.json"
            other = tmp_path / "notes.json"
            for p in (current, prior, other):
                p.write_text("{}")
            found = generate_report.discover_history(current)
        self.assertEqual(found, [prior])

    def test_no_siblings_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            current = Path(tmp) / "analysis-2026-07-16.json"
            current.write_text("{}")
            self.assertEqual(generate_report.discover_history(current), [])


class TestOutcomesDiscovery(unittest.TestCase):
    def test_discovers_sibling_outcomes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            current = tmp_path / "analysis-2026-07-16.json"
            outcomes = tmp_path / "outcomes.jsonl"
            current.write_text("{}")
            outcomes.write_text("")
            self.assertEqual(generate_report.discover_outcomes(current), outcomes)

    def test_missing_outcomes_file_is_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            current = Path(tmp) / "analysis-2026-07-16.json"
            current.write_text("{}")
            self.assertIsNone(generate_report.discover_outcomes(current))


class TestComputeNovelty(unittest.TestCase):
    def test_no_history_is_empty(self):
        data = snapshot("2026-07-16", [individual("Alex Chen", "https://example.com/a")])
        self.assertEqual(generate_report.compute_novelty(data, [], None), {})

    def test_never_seen_before_is_new(self):
        with tempfile.TemporaryDirectory() as tmp:
            prior = Path(tmp) / "analysis-2026-07-01.json"
            prior.write_text(json.dumps(snapshot("2026-07-01", [individual("Sam Lee", "https://example.com/b")])))
            current = snapshot("2026-07-16", [individual("Alex Chen", "https://example.com/a")])
            novelty = generate_report.compute_novelty(current, [prior], None)
        key = ("individuals", "alex chen", "https://example.com/a")
        self.assertTrue(novelty[key]["is_new"])

    def test_seen_before_is_recurring_not_new(self):
        with tempfile.TemporaryDirectory() as tmp:
            prior = Path(tmp) / "analysis-2026-07-01.json"
            prior.write_text(json.dumps(snapshot("2026-07-01", [individual("Alex Chen", "https://example.com/a")])))
            current = snapshot("2026-07-16", [individual("Alex Chen", "https://example.com/a")])
            novelty = generate_report.compute_novelty(current, [prior], None)
        key = ("individuals", "alex chen", "https://example.com/a")
        self.assertFalse(novelty[key]["is_new"])
        self.assertEqual(novelty[key]["times_seen"], 2)

    def test_recurring_with_logged_outcome_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            prior = tmp_path / "analysis-2026-07-01.json"
            prior.write_text(json.dumps(snapshot("2026-07-01", [individual("Alex Chen", "https://example.com/a")])))
            outcomes = tmp_path / "outcomes.jsonl"
            outcomes.write_text(json.dumps({
                "name": "Alex Chen", "source_url": "https://example.com/a",
                "outcome": "no_reply", "date": "2026-07-02",
            }) + "\n")
            current = snapshot("2026-07-16", [individual("Alex Chen", "https://example.com/a")])
            novelty = generate_report.compute_novelty(current, [prior], outcomes)
        key = ("individuals", "alex chen", "https://example.com/a")
        self.assertIn("prior_outcome", novelty[key])


class TestAnnotateNovelty(unittest.TestCase):
    def test_mutates_matching_items_in_place(self):
        data = snapshot("2026-07-16", [individual("Alex Chen", "https://example.com/a")])
        key = ("individuals", "alex chen", "https://example.com/a")
        generate_report.annotate_novelty(data, {key: {"is_new": True}})
        self.assertEqual(data["individuals"][0]["_novelty"], {"is_new": True})


class TestNoveltyBadgeRendering(unittest.TestCase):
    def test_new_prospect_gets_new_badge(self):
        html = generate_report.render_novelty_badge({"_novelty": {"is_new": True}})
        self.assertIn("novelty new", html)

    def test_recurring_prospect_gets_seen_count_badge(self):
        item = {"_novelty": {"is_new": False, "times_seen": 3, "first_seen": "2026-06-01"}}
        html = generate_report.render_novelty_badge(item)
        self.assertIn("novelty recurring", html)
        self.assertIn("Seen 3x", html)

    def test_decided_prospect_gets_resurfacing_badge_over_recurring(self):
        item = {"_novelty": {"is_new": False, "times_seen": 2, "prior_outcome": "no_reply on 2026-07-02"}}
        html = generate_report.render_novelty_badge(item)
        self.assertIn("novelty decided", html)
        self.assertIn("Resurfacing", html)

    def test_no_novelty_key_renders_nothing(self):
        self.assertEqual(generate_report.render_novelty_badge({}), "")


class TestEndToEndCLI(unittest.TestCase):
    def _write(self, path: Path, data: dict) -> None:
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_auto_detects_history_and_renders_new_badge(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            prior = tmp_path / "analysis-2026-07-01.json"
            current = tmp_path / "analysis-2026-07-16.json"
            output = tmp_path / "out.html"
            self._write(prior, snapshot("2026-07-01", [individual("Sam Lee", "https://example.com/b")]))
            self._write(current, snapshot("2026-07-16", [individual("Alex Chen", "https://example.com/a")]))
            argv = ["generate_report.py", str(current), str(output)]
            with mock.patch.object(sys, "argv", argv):
                generate_report.main()
            html = output.read_text(encoding="utf-8")
        self.assertIn("badge novelty new", html)

    def test_no_history_flag_suppresses_auto_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            prior = tmp_path / "analysis-2026-07-01.json"
            current = tmp_path / "analysis-2026-07-16.json"
            output = tmp_path / "out.html"
            self._write(prior, snapshot("2026-07-01", [individual("Sam Lee", "https://example.com/b")]))
            self._write(current, snapshot("2026-07-16", [individual("Alex Chen", "https://example.com/a")]))
            argv = ["generate_report.py", str(current), str(output), "--no-history"]
            with mock.patch.object(sys, "argv", argv):
                generate_report.main()
            html = output.read_text(encoding="utf-8")
        self.assertNotIn("badge novelty", html)

    def test_verified_at_renders_as_data_attribute(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            current = tmp_path / "in.json"
            output = tmp_path / "out.html"
            item = individual("Alex Chen", "https://example.com/a")
            item["verification_tier"] = "verified"
            item["verified_at"] = "2026-07-16"
            self._write(current, {"individuals": [item]})
            argv = ["generate_report.py", str(current), str(output), "--no-history"]
            with mock.patch.object(sys, "argv", argv):
                generate_report.main()
            html = output.read_text(encoding="utf-8")
        self.assertIn('data-verified-at="2026-07-16"', html)

    def test_opener_grounding_note_renders_as_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            current = tmp_path / "in.json"
            output = tmp_path / "out.html"
            item = individual("Alex Chen", "https://example.com/a")
            item["opener"] = "Hey - noticed your post"
            item["opener_grounding_note"] = (
                "Opener references specifics not found in the checked evidence "
                "(topical 0.00) - ground the message in the evidence text before sending"
            )
            self._write(current, {"individuals": [item]})
            argv = ["generate_report.py", str(current), str(output), "--no-history"]
            with mock.patch.object(sys, "argv", argv):
                generate_report.main()
            html = output.read_text(encoding="utf-8")
        self.assertIn("opener-warning", html)


class TestUntrustedTextInOutput(unittest.TestCase):
    """Prospect fields are copied from web pages. They must not be able to end
    the report's inline script or become a spreadsheet formula."""

    def test_closing_script_tag_cannot_end_the_inline_script(self):
        payload = "x</script><img src=x onerror=alert(1)>"
        html_out = generate_report.build_html(
            {"title": "T", "individuals": [individual("Jane", "https://example.com/a", pain_signal=payload)]}
        )
        start = html_out.index("const CSV_DATA")
        script = html_out[start:html_out.index("const CSV_FILENAME", start)]
        self.assertNotIn("</script>", script)
        self.assertIn("<\\/script>", script)

    def test_formula_cells_are_neutralised_in_embedded_csv(self):
        rows = generate_report.build_csv(
            [individual('=HYPERLINK("http://evil.example","x")', "https://example.com/a", pain_signal="@SUM(1+1)",
                        why_fit="+1", why_now="-2")], [], [])
        self.assertIn('"\'=HYPERLINK(', rows)
        self.assertIn('"\'@SUM(1+1)"', rows)
        self.assertIn('"\'+1"', rows)
        self.assertIn('"\'-2"', rows)
        self.assertIn(',"70",', rows)


class TestHtmlEscaping(unittest.TestCase):
    """Field text is copied from web pages and must reach the page as text."""

    def test_markup_in_fields_is_escaped(self):
        payload = '<img src=x onerror=alert(1)>'
        data = {
            "title": f"T {payload}", "verdict": f'v "{payload}',
            "individuals": [individual(
                f"Jane {payload}", "https://example.com/a", pain_signal=payload, evidence=payload,
                source_title=payload, opener=payload, verification_note=f'" onmouseover="{payload}',
            )],
        }
        html_out = generate_report.build_html(data)
        body = html_out[:html_out.index("const CSV_DATA")]
        self.assertNotIn(payload, body)
        self.assertNotIn('" onmouseover="', body)
        self.assertIn("&lt;img src=x onerror=alert(1)&gt;", body)


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestClientDeliverableSections(unittest.TestCase):
    """The 1.6.0 client-grade sections: authored executive summary, company
    tiers, verified battlecard, and the footer trust mark."""

    def _base(self) -> dict:
        return {
            "title": "T", "generated_at": "2026-07-21", "verdict": "v",
            "individuals": [individual("Jane", "https://example.com/a",
                                       verification_tier="verified")],
        }

    def test_authored_executive_summary_renders(self):
        data = self._base()
        data["executive_summary"] = {
            "overview": "We researched the thing.",
            "key_findings": ["Finding one"],
            "next_steps": ["Message Jane"],
        }
        html = generate_report.build_html(data)
        self.assertIn("Executive summary", html)
        self.assertIn("We researched the thing.", html)
        self.assertIn("Do this Monday", html)

    def test_no_executive_summary_no_section(self):
        html = generate_report.build_html(self._base())
        self.assertNotIn("client-summary\"", html.replace("class=\"client-summary\"", "client-summary\""))
        self.assertNotIn("<section class=\"client-summary\">", html)

    def test_companies_grouped_by_tier(self):
        data = self._base()
        data["companies"] = [
            {"name": "AcmeOne", "source_url": "https://example.com/1", "score": 80,
             "stage": "High intent", "tier": 1, "tier_rationale": "self-serve program open"},
            {"name": "AcmeThree", "source_url": "https://example.com/3", "score": 55,
             "stage": "Potential fit", "tier": 3, "tier_rationale": "no live trigger"},
        ]
        html = generate_report.build_html(data)
        self.assertIn("Tier 1 — pursue now", html)
        self.assertIn("Tier 3 — monitor", html)
        self.assertNotIn("Tier 2 — nurture", html)

    def test_untiered_companies_render_flat(self):
        data = self._base()
        data["companies"] = [{"name": "Acme", "source_url": "https://example.com/1",
                              "score": 70, "stage": "Problem aware"}]
        html = generate_report.build_html(data)
        self.assertIn("Partners to pitch", html)
        self.assertNotIn("Tier 1", html)

    def test_battlecard_renders_and_drops_disqualified(self):
        data = self._base()
        data["competitive_context"] = {
            "top_competitors": ["GoodComp", "BadComp"],
            "battlecard": [
                {"competitor": "GoodComp", "claim": "users complain about pricing",
                 "evidence": "quoted complaint", "source_url": "https://example.com/g",
                 "counter_angle": "we are cheaper", "verification_tier": "verified",
                 "corroboration_count": 1},
                {"competitor": "BadComp", "claim": "fabricated claim",
                 "evidence": "not on page", "source_url": "https://example.com/b",
                 "counter_angle": "x", "verification_tier": "unsupported"},
            ],
        }
        html = generate_report.build_html(data)
        self.assertIn("GoodComp", html)
        self.assertIn("Corroborated by 1 prospect", html)
        self.assertNotIn("fabricated claim", html)

    def test_single_source_battlecard_flagged(self):
        data = self._base()
        data["competitive_context"] = {
            "battlecard": [
                {"competitor": "SoloComp", "claim": "c", "evidence": "e",
                 "source_url": "https://example.com/s", "counter_angle": "a",
                 "verification_tier": "verified", "corroboration_count": 0,
                 "corroboration_note": "No prospect in this run independently mentions this competitor — single-source claim"},
            ],
        }
        html = generate_report.build_html(data)
        self.assertIn("Single-source", html)

    def test_footer_trust_mark_counts_prospects_and_battlecard(self):
        data = self._base()
        data["competitive_context"] = {
            "battlecard": [
                {"competitor": "C", "claim": "c", "evidence": "e",
                 "source_url": "https://example.com/s", "counter_angle": "a",
                 "verification_tier": "verified"},
            ],
        }
        html = generate_report.build_html(data)
        self.assertIn("<b>2 of 2</b> claims verified", html)

    def test_no_verification_no_trust_mark(self):
        data = {"title": "T", "generated_at": "2026-07-21", "verdict": "v",
                "individuals": [individual("Jane", "https://example.com/a")]}
        html = generate_report.build_html(data)
        self.assertNotIn('<span class="trust-mark">', html)
