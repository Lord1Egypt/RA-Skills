#!/usr/bin/env python3
"""Unit tests for the stock watchlist helper."""

import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import stock_watchlist


class StockWatchlistTests(unittest.TestCase):
    def test_infer_quote_id_from_symbol(self) -> None:
        self.assertEqual(stock_watchlist.infer_quote_id_from_symbol("SH600519"), "1.600519")
        self.assertEqual(stock_watchlist.infer_quote_id_from_symbol("sz000001"), "0.000001")
        self.assertEqual(stock_watchlist.infer_quote_id_from_symbol("HK700"), "116.00700")
        self.assertIsNone(stock_watchlist.infer_quote_id_from_symbol("BABA"))
        self.assertEqual(stock_watchlist.normalize_lookup_key("腾讯"), "腾讯")

    def test_parse_and_render_watchlist_table(self) -> None:
        text = """
| query | symbol | quote_id | name | cost_price | quantity | note |
| --- | --- | --- | --- | --- | --- | --- |
| 贵州茅台 | SH600519 | 1.600519 | 贵州茅台 | 1395 | 100 | core |
""".strip()
        rows = stock_watchlist.parse_watchlist_table(text)
        self.assertEqual(rows[0]["symbol"], "SH600519")
        rendered = stock_watchlist.render_watchlist_table(rows)
        self.assertIn("SH600519", rendered)
        self.assertIn("quote_id", rendered)

    def test_save_watchlist_keeps_markers(self) -> None:
        prefix = "# Demo\n\n" + stock_watchlist.WATCHLIST_START
        suffix = stock_watchlist.WATCHLIST_END + "\n"
        rows = [
            {
                "query": "贵州茅台",
                "symbol": "SH600519",
                "quote_id": "1.600519",
                "name": "贵州茅台",
                "cost_price": "1395",
                "quantity": "100",
                "note": "core",
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "watchlist.md"
            stock_watchlist.save_watchlist(path, prefix, suffix, rows)
            content = path.read_text(encoding="utf-8")
            self.assertIn(stock_watchlist.WATCHLIST_START, content)
            self.assertIn(stock_watchlist.WATCHLIST_END, content)
            self.assertIn("SH600519", content)

    def test_summarize_watchlist(self) -> None:
        rows = [
            {
                "cost_value": 1000.0,
                "market_value": 1200.0,
            },
            {
                "cost_value": None,
                "market_value": None,
            },
        ]
        summary = stock_watchlist.summarize_watchlist(rows)
        self.assertEqual(summary["positions"], 2)
        self.assertEqual(summary["cost_positions"], 1)
        self.assertEqual(summary["total_profit_loss"], 200.0)
        self.assertEqual(summary["total_profit_loss_percent"], 20.0)

    def test_price_scale_for_quote(self) -> None:
        self.assertEqual(stock_watchlist.price_scale_for_quote("CN", "沪A", 2), 100)
        self.assertEqual(stock_watchlist.price_scale_for_quote("CN", "基金", 3), 1000)
        self.assertEqual(stock_watchlist.price_scale_for_quote("CN", "", 3), 1000)
        self.assertEqual(stock_watchlist.price_scale_for_quote("HK", "港股", 3), 1000)
        self.assertEqual(stock_watchlist.price_scale_for_quote("US", "美股", 3), 1000)

    def test_choose_candidate_prefers_primary_stock(self) -> None:
        candidates = [
            {
                "code": "00700",
                "name": "腾讯控股",
                "symbol": "HK00700",
                "quote_id": "116.00700",
                "market": "HK",
                "security_type": "港股",
            },
            {
                "code": "TME",
                "name": "腾讯音乐",
                "symbol": "TME",
                "quote_id": "106.TME",
                "market": "US",
                "security_type": "美股",
            },
        ]
        chosen = stock_watchlist.choose_candidate("腾讯", candidates)
        self.assertEqual(chosen["symbol"], "HK00700")

    def test_resolve_watchlist_path_rejects_non_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch("stock_watchlist.Path.cwd", return_value=Path(tmpdir)):
                with self.assertRaises(stock_watchlist.StockWatchlistError):
                    stock_watchlist.resolve_watchlist_path("./watchlist.txt")

    def test_resolve_watchlist_path_rejects_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as otherdir:
                with mock.patch("stock_watchlist.Path.cwd", return_value=Path(tmpdir)):
                    with self.assertRaises(stock_watchlist.StockWatchlistError):
                        stock_watchlist.resolve_watchlist_path(
                            str(Path(otherdir) / "watchlist.md")
                        )

    def test_resolve_watchlist_path_allows_explicit_safe_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as otherdir:
                with mock.patch("stock_watchlist.Path.cwd", return_value=Path(tmpdir)):
                    with mock.patch.dict(
                        os.environ,
                        {
                            stock_watchlist.WATCHLIST_ALLOWED_ROOTS_ENV: otherdir,
                        },
                        clear=False,
                    ):
                        resolved = stock_watchlist.resolve_watchlist_path(
                            str(Path(otherdir) / "watchlist.md")
                        )
                        self.assertEqual(
                            resolved, (Path(otherdir) / "watchlist.md").resolve()
                        )

    def test_force_init_rejects_non_watchlist_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch("stock_watchlist.Path.cwd", return_value=Path(tmpdir)):
                target = Path(tmpdir) / "watchlist.md"
                target.write_text("# Notes\n", encoding="utf-8")
                args = type("Args", (), {"file": str(target), "force": True})()
                with self.assertRaises(stock_watchlist.StockWatchlistError):
                    stock_watchlist.command_watchlist_init(args)


if __name__ == "__main__":
    unittest.main()
