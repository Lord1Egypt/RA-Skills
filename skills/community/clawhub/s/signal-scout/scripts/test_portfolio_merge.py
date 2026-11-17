#!/usr/bin/env python3
"""Regression tests for portfolio_merge.py's glob-based multi-snapshot support.

Run: python3 test_portfolio_merge.py    (stdlib only)

portfolio_merge.py originally took exactly one analysis.json per product and
cross-referenced their single snapshots. That misses a real case: a prospect
that dropped out of product A's latest run (evidence went stale, or this
week's search just didn't resurface them) but is still live in product B's
current run is still worth surfacing — the overlap is the whole point of this
script. So each product argument may now be a glob matching every snapshot
ever saved for that product, and cross-referencing runs against the full
cumulative set (reusing diff_reports.accumulate_history), not just the latest
file. These tests check the glob/label parsing, that cumulative cross-
referencing actually surfaces a prospect dropped from a product's latest
snapshot, and that plain single-file usage (the original call shape) still
works unchanged.
"""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import diff_reports
import portfolio_merge


def individual(name: str, source_url: str, score: int = 70, **extra) -> dict:
    base = {"name": name, "source_url": source_url, "score": score, "pain_signal": "some pain"}
    base.update(extra)
    return base


def snapshot(generated_at: str, individuals: list[dict], title: str | None = None) -> dict:
    out = {"generated_at": generated_at, "individuals": individuals}
    if title is not None:
        out["title"] = title
    return out


def prospects_dict(entries: list[tuple[str, str, str, dict]]) -> dict:
    """entries: (kind, name, source_url, extra) -> {(kind, name, url): item}, the
    same shape diff_reports.load_prospects()/accumulate_history() produce."""
    out = {}
    for kind, name, url, extra in entries:
        item = {"name": name, "source_url": url, **extra}
        out[diff_reports.prospect_key(kind, item)] = item
    return out


def run_merge(argv_tail: list[str]) -> str:
    argv = ["portfolio_merge.py", *argv_tail]
    buf = io.StringIO()
    with mock.patch.object(sys, "argv", argv), redirect_stdout(buf):
        portfolio_merge.main()
    return buf.getvalue()


class TestResolvePaths(unittest.TestCase):
    def test_literal_existing_path_returns_single_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "analysis.json"
            f.write_text("{}")
            self.assertEqual(portfolio_merge.resolve_paths(str(f)), [f])

    def test_glob_pattern_returns_all_matches_sorted(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            older = tmp_path / "analysis-2026-06-01.json"
            newer = tmp_path / "analysis-2026-07-01.json"
            newer.write_text("{}")
            older.write_text("{}")
            found = portfolio_merge.resolve_paths(str(tmp_path / "analysis-*.json"))
            self.assertEqual(found, [older, newer])

    def test_no_match_raises_system_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                portfolio_merge.resolve_paths(str(Path(tmp) / "nope-*.json"))


class TestParseLabeledArgs(unittest.TestCase):
    def test_label_with_single_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "a.json"
            f.write_text(json.dumps(snapshot("2026-07-01", [])))
            products = portfolio_merge.parse_labeled_args([f"Shelfie={f}"], [])
            self.assertEqual(products, [("Shelfie", [f])])

    def test_label_with_glob_matches_multiple_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            older = tmp_path / "analysis-2026-06-01.json"
            newer = tmp_path / "analysis-2026-07-01.json"
            older.write_text(json.dumps(snapshot("2026-06-01", [])))
            newer.write_text(json.dumps(snapshot("2026-07-01", [])))
            products = portfolio_merge.parse_labeled_args([f"Shelfie={tmp_path}/analysis-*.json"], [])
            self.assertEqual(products, [("Shelfie", [older, newer])])

    def test_malformed_label_without_equals_raises(self):
        with self.assertRaises(SystemExit):
            portfolio_merge.parse_labeled_args(["NoEqualsSign"], [])

    def test_positional_glob_derives_label_from_latest_snapshots_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            older = tmp_path / "analysis-2026-06-01.json"
            newer = tmp_path / "analysis-2026-07-01.json"
            older.write_text(json.dumps(snapshot("2026-06-01", [], title="Old Title")))
            newer.write_text(json.dumps(snapshot("2026-07-01", [], title="Shelfie Weekly Scout")))
            products = portfolio_merge.parse_labeled_args([], [str(tmp_path / "analysis-*.json")])
            self.assertEqual(len(products), 1)
            label, paths = products[0]
            self.assertEqual(label, "Shelfie Weekly Scout")
            self.assertEqual(paths, [older, newer])

    def test_positional_single_file_without_title_falls_back_to_stem(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "analysis.json"
            f.write_text(json.dumps(snapshot("2026-07-01", [])))
            products = portfolio_merge.parse_labeled_args([], [str(f)])
            self.assertEqual(products[0][0], "analysis")


class TestBuildCrossReferences(unittest.TestCase):
    def test_matched_by_source_url_across_two_products(self):
        shelfie = ("Shelfie", prospects_dict([
            ("individuals", "Alex Chen", "https://example.com/a", {"score": 80, "stage": "Aware"}),
        ]))
        budgetly = ("Budgetly", prospects_dict([
            ("individuals", "Alex Chen", "https://example.com/a", {"score": 65, "stage": "Considering"}),
        ]))
        refs = portfolio_merge.build_cross_references([shelfie, budgetly])
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0]["products"], ["Budgetly", "Shelfie"])

    def test_matched_by_normalized_name_when_urls_differ(self):
        shelfie = ("Shelfie", prospects_dict([
            ("individuals", "Alex  Chen", "https://example.com/a", {}),
        ]))
        budgetly = ("Budgetly", prospects_dict([
            ("individuals", "alex chen!!", "https://example.com/different", {}),
        ]))
        refs = portfolio_merge.build_cross_references([shelfie, budgetly])
        self.assertEqual(len(refs), 1)

    def test_single_product_prospect_is_not_cross_referenced(self):
        shelfie = ("Shelfie", prospects_dict([
            ("individuals", "Alex Chen", "https://example.com/a", {}),
        ]))
        self.assertEqual(portfolio_merge.build_cross_references([shelfie]), [])

    def test_appearances_carry_per_product_score_and_stage(self):
        shelfie = ("Shelfie", prospects_dict([
            ("individuals", "Alex Chen", "https://example.com/a", {"score": 80, "stage": "Aware"}),
        ]))
        budgetly = ("Budgetly", prospects_dict([
            ("individuals", "Alex Chen", "https://example.com/a", {"score": 65, "stage": "Considering"}),
        ]))
        refs = portfolio_merge.build_cross_references([shelfie, budgetly])
        by_product = {a["product"]: a for a in refs[0]["appearances"]}
        self.assertEqual(by_product["Shelfie"]["score"], 80)
        self.assertEqual(by_product["Budgetly"]["stage"], "Considering")

    def test_prospect_dropped_from_latest_snapshot_still_cross_references(self):
        """The core Gap 6 scenario: product A's cumulative history (old + new
        snapshot folded via accumulate_history) still contains a prospect that
        product A's latest run alone no longer surfaces, and product B's
        current run has the same prospect — the overlap must still be found."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            a_old = tmp_path / "a-old.json"
            a_new = tmp_path / "a-new.json"
            b_file = tmp_path / "b.json"
            a_old.write_text(json.dumps(snapshot("2026-06-01", [individual("Alex Chen", "https://example.com/a")])))
            a_new.write_text(json.dumps(snapshot("2026-07-01", [individual("Sam Lee", "https://example.com/b")])))
            b_file.write_text(json.dumps(snapshot("2026-07-01", [individual("Alex Chen", "https://example.com/a")])))

            loaded_a = [(a_old, json.loads(a_old.read_text())), (a_new, json.loads(a_new.read_text()))]
            history_a, _times, _first = diff_reports.accumulate_history(loaded_a)
            loaded_b = [(b_file, json.loads(b_file.read_text()))]
            history_b, _times_b, _first_b = diff_reports.accumulate_history(loaded_b)

            refs = portfolio_merge.build_cross_references([("A", history_a), ("B", history_b)])
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0]["name"], "Alex Chen")


class TestEndToEndCLI(unittest.TestCase):
    def test_two_single_files_backward_compatible(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            a = tmp_path / "a.json"
            b = tmp_path / "b.json"
            a.write_text(json.dumps(snapshot("2026-07-01", [individual("Alex Chen", "https://example.com/a")], title="Shelfie")))
            b.write_text(json.dumps(snapshot("2026-07-01", [individual("Alex Chen", "https://example.com/a")], title="Budgetly")))
            out = run_merge([str(a), str(b)])
        self.assertIn("2 products loaded", out)
        self.assertIn("Alex Chen", out)
        self.assertIn("in 2 products", out)

    def test_glob_multi_snapshot_surfaces_prospect_dropped_from_latest(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            a_dir = tmp_path / "shelfie"
            b_dir = tmp_path / "budgetly"
            a_dir.mkdir()
            b_dir.mkdir()
            (a_dir / "analysis-2026-06-01.json").write_text(json.dumps(
                snapshot("2026-06-01", [individual("Alex Chen", "https://example.com/a")], title="Shelfie")))
            (a_dir / "analysis-2026-07-01.json").write_text(json.dumps(
                snapshot("2026-07-01", [individual("Sam Lee", "https://example.com/b")], title="Shelfie")))
            (b_dir / "analysis-2026-07-01.json").write_text(json.dumps(
                snapshot("2026-07-01", [individual("Alex Chen", "https://example.com/a")], title="Budgetly")))

            out = run_merge([str(a_dir / "analysis-*.json"), str(b_dir / "analysis-*.json")])
        self.assertIn("2 snapshot(s)", out)
        self.assertIn("Alex Chen", out)
        self.assertIn("in 2 products", out)

    def test_label_with_glob_reports_snapshot_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            a1 = tmp_path / "shelfie-1.json"
            a2 = tmp_path / "shelfie-2.json"
            b = tmp_path / "budgetly.json"
            a1.write_text(json.dumps(snapshot("2026-06-01", [individual("Alex Chen", "https://example.com/a")])))
            a2.write_text(json.dumps(snapshot("2026-07-01", [individual("Sam Lee", "https://example.com/b")])))
            b.write_text(json.dumps(snapshot("2026-07-01", [individual("Alex Chen", "https://example.com/a")])))
            out = run_merge(["--label", f"Shelfie={tmp_path}/shelfie-*.json", "--label", f"Budgetly={b}"])
        self.assertIn("Shelfie (2 snapshot(s))", out)
        self.assertIn("Budgetly (1 snapshot(s))", out)

    def test_out_writes_merged_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            a = tmp_path / "a.json"
            b = tmp_path / "b.json"
            out_path = tmp_path / "merged.json"
            a.write_text(json.dumps(snapshot("2026-07-01", [individual("Alex Chen", "https://example.com/a")], title="Shelfie")))
            b.write_text(json.dumps(snapshot("2026-07-01", [individual("Alex Chen", "https://example.com/a")], title="Budgetly")))
            run_merge([str(a), str(b), "--out", str(out_path)])
            payload = json.loads(out_path.read_text(encoding="utf-8"))
        self.assertEqual(set(payload["products"]), {"Shelfie", "Budgetly"})
        self.assertEqual(len(payload["cross_references"]), 1)

    def test_fewer_than_two_reports_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.json"
            a.write_text(json.dumps(snapshot("2026-07-01", [])))
            with self.assertRaises(SystemExit):
                run_merge([str(a)])

    def test_no_overlap_reports_none_found(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            a = tmp_path / "a.json"
            b = tmp_path / "b.json"
            a.write_text(json.dumps(snapshot("2026-07-01", [individual("Alex Chen", "https://example.com/a")])))
            b.write_text(json.dumps(snapshot("2026-07-01", [individual("Sam Lee", "https://example.com/b")])))
            out = run_merge([str(a), str(b)])
        self.assertIn("No prospects overlap", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
