#!/usr/bin/env python3
"""Tests for finalize.py's offline pieces: validation and CSV export.

The subprocess steps (verify/report/diff) are covered by their own scripts'
tests; these tests exercise only what finalize.py adds itself. No network.
"""

from __future__ import annotations

import contextlib
import csv
import http.server
import io
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

import finalize
from finalize import CSV_COLUMNS, next_action_for, validate, write_csv
from signal_scout_core import compute_score


def valid_individual() -> dict:
    dims = {"pain_strength": 4, "product_fit": 4, "timing": 4, "reachability": 3, "evidence_quality": 3}
    return {
        "name": "Jane Doe", "stage": "High intent",
        "score": 74,  # matches compute_score("individual", dims)
        "pain_signal": "p", "evidence": "e", "why_fit": "w", "why_now": "n",
        "source_title": "t", "source_url": "https://example.com/post",
        "source_type": "Forum", "signal_date": "2026-07-01",
        "suggested_channel": "Forum reply", "opener": "hi", "caution": "c",
        "dimensions": dims,
    }


def valid_report() -> dict:
    return {
        "title": "T", "product": "P", "product_url": "https://example.com",
        "target_customer": "c", "search_scope": "s", "generated_at": "2026-07-21",
        "verdict": "v", "outreach_plan": {"angle": "a"}, "limits": ["l"],
        "individuals": [valid_individual()],
    }


class ValidateTests(unittest.TestCase):
    def test_valid_report_passes(self):
        self.assertEqual(validate(valid_report()), [])

    def test_missing_top_level_field(self):
        data = valid_report()
        del data["verdict"]
        self.assertTrue(any("verdict" in e for e in validate(data)))

    def test_no_prospects_fails(self):
        data = valid_report()
        del data["individuals"]
        self.assertTrue(any("non-empty" in e for e in validate(data)))

    def test_score_drift_flagged(self):
        data = valid_report()
        data["individuals"][0]["score"] = 15
        self.assertTrue(any("does not match" in e for e in validate(data)))

    def test_prospect_schema_violation_named(self):
        data = valid_report()
        data["individuals"][0]["stage"] = "Very keen"
        errors = validate(data)
        self.assertTrue(any("Jane Doe" in e and "stage" in e for e in errors))


class CsvTests(unittest.TestCase):
    def test_next_action_per_type(self):
        self.assertEqual(next_action_for("individuals", {"opener": "hi"}), "hi")
        self.assertEqual(next_action_for("individuals", {"suggested_channel": "DM"}), "DM")
        self.assertEqual(next_action_for("segments", {"content_angle": "angle"}), "angle")
        self.assertEqual(next_action_for("companies", {"bd_angle": "pitch"}), "pitch")

    def test_write_csv_columns_and_rows(self):
        data = valid_report()
        data["individuals"][0]["verification_tier"] = "verified"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "prospects.csv"
            self.assertEqual(write_csv(data, out), 1)
            with out.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.reader(handle))
        self.assertEqual(rows[0], list(CSV_COLUMNS))
        row = dict(zip(rows[0], rows[1], strict=True))
        self.assertEqual(row["type"], "individual")
        self.assertEqual(row["verification"], "Verified")
        self.assertEqual(row["next_action"], "hi")


class CsvFormulaTests(unittest.TestCase):
    def test_formula_cells_are_neutralised(self):
        report = valid_report()
        report["individuals"][0]["name"] = '=HYPERLINK("http://evil.example","x")'
        report["individuals"][0]["why_fit"] = "@SUM(1+1)"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "prospects.csv"
            write_csv(report, out)
            with out.open(newline="", encoding="utf-8") as handle:
                row = list(csv.DictReader(handle))[0]
        self.assertEqual(row["name"], '\'=HYPERLINK("http://evil.example","x")')
        self.assertEqual(row["why_fit"], "'@SUM(1+1)")
        self.assertEqual(row["score"], str(report["individuals"][0]["score"]))


class ClientSectionValidationTests(unittest.TestCase):
    def _company(self, **extra) -> dict:
        company = {
            "name": "Acme", "stage": "High intent", "score": 80,
            "source_url": "https://example.com/acme",
            "execution_path": "Self-serve program", "contact_path": "partner page",
            "dimensions": {"strategic_fit": 4, "timing": 4, "execution_ease": 4, "evidence_quality": 4},
        }
        company.update(extra)
        return company

    def test_tier_without_rationale_fails(self):
        data = valid_report()
        data["companies"] = [self._company(tier=1)]
        errors = validate(data)
        self.assertTrue(any("tier_rationale" in e for e in errors))

    def test_invalid_tier_value_fails(self):
        data = valid_report()
        data["companies"] = [self._company(tier=5, tier_rationale="r")]
        errors = validate(data)
        self.assertTrue(any("tier must be 1, 2, or 3" in e for e in errors))

    def test_company_domain_must_be_bare(self):
        data = valid_report()
        data["companies"] = [self._company(domain="https://acme.com/partners")]
        self.assertTrue(any("domain must be a bare" in e for e in validate(data)))
        data["companies"] = [self._company(domain="acme.com")]
        self.assertEqual(validate(data), [])

    def test_company_domain_in_csv(self):
        data = valid_report()
        data["companies"] = [self._company(domain="acme.com")]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "prospects.csv"
            write_csv(data, out)
            with out.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual([r["domain"] for r in rows], ["", "acme.com"])

    def test_valid_tiered_company_passes(self):
        data = valid_report()
        data["companies"] = [self._company(tier=2, tier_rationale="warm BD only")]
        self.assertEqual(validate(data), [])

    def test_battlecard_missing_fields_and_url_fail(self):
        data = valid_report()
        data["competitive_context"] = {"battlecard": [
            {"competitor": "Comp", "claim": "", "evidence": "e", "counter_angle": "a", "source_url": "not-a-url"},
        ]}
        errors = validate(data)
        self.assertTrue(any("missing claim" in e for e in errors))
        self.assertTrue(any("source_url" in e for e in errors))

    def test_valid_battlecard_passes(self):
        data = valid_report()
        data["competitive_context"] = {"battlecard": [
            {"competitor": "Comp", "claim": "c", "evidence": "e",
             "counter_angle": "a", "source_url": "https://example.com/c"},
        ]}
        self.assertEqual(validate(data), [])


class ScoreWeightTests(unittest.TestCase):
    """Every dimension gets a different rating, so moving weight from one
    dimension to another changes the result."""

    def test_each_weight_is_pinned(self):
        cases = {
            "individual": ({"pain_strength": 5, "product_fit": 4, "timing": 3, "reachability": 2, "evidence_quality": 1}, 66),
            "segment": ({"pain_strength": 5, "product_fit": 4, "timing": 3, "evidence_quality": 2}, 75),
            "company": ({"strategic_fit": 5, "timing": 4, "execution_ease": 3, "evidence_quality": 2}, 73),
        }
        for prospect_type, (dimensions, expected) in cases.items():
            self.assertEqual(compute_score(prospect_type, dimensions), expected, prospect_type)


PAGE_TEXT = "We moved our whole test suite off the hosted runner last month because builds queued for an hour. " * 4


class _Page(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = f"<html><body><p>{PAGE_TEXT}</p></body></html>".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class FinalizeEndToEndVerification(unittest.TestCase):
    """finalize.py run for real against a local page: a claim that is not on
    its page stops the run before any report is written."""

    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Page)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.server.server_address[1]}/post"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def run_finalize(self, tmp: str, evidence: str) -> tuple[int, str]:
        report = valid_report()
        report["individuals"][0].update(source_url=self.url, evidence=evidence)
        src = Path(tmp) / "analysis.json"
        src.write_text(json.dumps(report), encoding="utf-8")
        out = io.StringIO()
        code = 0
        with mock.patch.object(sys, "argv", ["finalize.py", str(src), "--allow-private-addresses"]), \
                contextlib.redirect_stdout(out):
            try:
                finalize.main()
            except SystemExit as exc:
                code = int(exc.code or 0)
        return code, out.getvalue()

    def test_claim_on_the_page_produces_a_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self.run_finalize(tmp, "We moved our whole test suite off the hosted runner last month")
            self.assertEqual(code, 0, out)
            self.assertTrue((Path(tmp) / "signal-scout-report.html").exists())
            handoff = json.loads((Path(tmp) / "handoff.json").read_text(encoding="utf-8"))
            self.assertEqual(len(handoff["individuals"]), 1)

    def test_claim_not_on_the_page_stops_before_the_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self.run_finalize(tmp, "Their platform group signed a contract with Globex for 250 seats")
            self.assertEqual(code, 1, out)
            self.assertIn("verify: FAILED", out)
            self.assertFalse((Path(tmp) / "signal-scout-report.html").exists())
            self.assertFalse((Path(tmp) / "prospects.csv").exists())
            handoff = json.loads((Path(tmp) / "handoff.json").read_text(encoding="utf-8"))
            self.assertNotIn("individuals", handoff)


if __name__ == "__main__":
    unittest.main()
