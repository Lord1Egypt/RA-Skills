#!/usr/bin/env python3
"""Regression test for persisted token-price provenance."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("ledger_watcher.py")
SPEC = importlib.util.spec_from_file_location("ledger_watcher_under_test", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class PriceVersionTests(unittest.TestCase):
    def test_get_db_persists_every_bundled_price(self):
        original_db = MODULE.LEDGER_DB
        with tempfile.TemporaryDirectory(prefix="token-ledger-test-") as temp_dir:
            MODULE.LEDGER_DB = Path(temp_dir) / "ledger.db"
            try:
                db = MODULE.get_db()
                rows = db.execute(
                    """
                    SELECT provider, model, input_per_m, output_per_m,
                           cache_read_per_m, cache_write_per_m, fetched_at, source_url
                    FROM price_versions
                    WHERE version = ?
                    """,
                    (MODULE.PRICE_VERSION,),
                ).fetchall()
            finally:
                MODULE.LEDGER_DB = original_db

        self.assertEqual(len(rows), len(MODULE.PRICING))
        by_model = {row[1]: row for row in rows}
        for model, price in MODULE.PRICING.items():
            row = by_model[model]
            self.assertEqual(row[2], price["input"])
            self.assertEqual(row[3], price["output"])
            self.assertEqual(row[4], price["cacheRead"])
            self.assertEqual(row[5], price["cacheWrite"])
            self.assertEqual(row[6], MODULE.PRICE_VERSION_FETCHED_AT)
            if row[0] not in MODULE.LOCAL_PROVIDERS:
                self.assertTrue(row[7], f"missing source URL for {model}")


if __name__ == "__main__":
    unittest.main()
