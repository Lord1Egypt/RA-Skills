#!/usr/bin/env python3
"""Unit tests for receipt-warranty-tracker skill.

All self-contained: a per-test temp state dir, no network, no subprocess.
Run: python3 -m pytest test_receipt.py -v
"""

import json
import os
import shutil
import sys
import tempfile
import unittest
from datetime import date, timedelta

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)
import receipt_warranty  # noqa: E402

DEFAULT_REMIND_DAYS = 3
CMD = os.path.join(SKILL_DIR, "receipt_warranty.py")


class ReceiptTestBase(unittest.TestCase):
    """Thin base: isolated temp state dir + helper wrappers around the real CLI."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="rw-test-")
        self.state = os.path.join(self.tmp, "state")
        os.makedirs(self.state, exist_ok=True)
        os.environ["RECEIPT_WARRANTY_STATE_DIR"] = self.state
        with open(os.path.join(self.state, "config.json"), "w") as f:
            json.dump({"remind_ahead_days": DEFAULT_REMIND_DAYS}, f)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        os.environ.pop("RECEIPT_WARRANTY_STATE_DIR", None)

    def ledger(self):
        with open(os.path.join(self.state, "ledger.json")) as f:
            return json.load(f)

    def add(self, item, price=10.0, days=30, until=None, currency="USD",
            receipt="photo of receipt", remind_days=None):
        """Run the `add` command; return the human-readable output text."""
        argv = ["add", "--item", item, "--price", str(price), "--currency", currency,
                "--receipt", receipt, "--days-before",
                str(remind_days or DEFAULT_REMIND_DAYS)]
        if days is not None:
            argv += ["--warranty-days", str(days)]
        if until:
            argv += ["--warranty-until", until]
        p = self._run(argv)
        return p.stdout

    def _run(self, argv):
        """Run the CLI as a subprocess. Returns CompletedProcess."""
        import subprocess as _sp
        _cmd = [sys.executable, CMD] + list(argv)
        p = _sp.run(_cmd, capture_output=True, text=True, timeout=30)
        return p

    def _raw(self, argv):
        """Return (returncode, stdout, stderr) for plain-text commands."""
        import subprocess as _sp
        _cmd = [sys.executable, CMD] + list(argv)
        p = _sp.run(_cmd, capture_output=True, text=True, timeout=30)
        return p.returncode, p.stdout, p.stderr


class TestAdd(ReceiptTestBase):
    def test_add_without_warranty_args_does_not_crash(self):
        # regression: add with no --warranty-days/--warranty-until used to hit
        # UnboundLocalError (entry referenced before assignment)
        rc, out, err = self._raw(["add", "--item", "Bare", "--receipt", "snap"])
        self.assertEqual(rc, 0, err)
        self.assertIn("no warranty window", out)
        led = self.ledger()
        e = led["entries"]["Bare"]
        self.assertIsNone(e["warranty_until"])
        self.assertEqual(e["warranty_days"], 0)

    def test_add_rejects_bad_warranty_until_date(self):
        rc, out, err = self._raw(["add", "--item", "Bad", "--receipt", "x",
                                  "--warranty-until", "2026-13-99"])
        self.assertNotEqual(rc, 0)
        self.assertIn("not a valid date", err)

    def test_add_currency_defaults_to_usd(self):
        self.add("C1", price=3)
        e = self.ledger()["entries"]["C1"]
        self.assertEqual(e["currency"], "USD")

    def test_add_records_ledger_with_warranty_days(self):
        out = self.add("Laptop", price=999, days=365, currency="USD")
        self.assertEqual(out, "stored: Laptop (999.0USD money, warranty until no warranty window)\n")
        led = self.ledger()
        self.assertEqual(len(led["entries"]), 1)
        e = led["entries"]["Laptop"]
        self.assertEqual(e["warranty_days"], 365)
        self.assertEqual(e["price"], 999)
        self.assertEqual(e["currency"], "USD")
        self.assertIsInstance(e["added_at"], float)

    def test_add_without_warranty_warns_state(self):
        # add with price only -> no warranty window -> ledger has no warranty_until
        out = self.add("Naked", price=5)
        self.assertEqual(out, "stored: Naked (5.0USD money, warranty until no warranty window)\n")
        led = self.ledger()
        entry = led["entries"]["Naked"]
        self.assertIsNone(entry.get("warranty_until"))
        self.assertIsInstance(entry["added_at"], float)


class TestEstimate(ReceiptTestBase):
    def test_estimate_keeps_weeks(self):
        # estimate with --weeks keeps the value as a whole week count
        r = self._run(["--json", "estimate", "--date", "2026-10-01", "--days", "28"])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(d["days_remaining"], 20)  # 2026-10-29 - 2026-10-09
        self.assertEqual(d["warranty_until"], "2026-10-29")

    def test_estimate_rejects_bad_arg(self):
        # --date must be a valid ISO date
        r = self._run(["--json", "estimate", "--date", "not-a-date"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not a valid date", r.stderr)

    def test_estimate_rejects_negative_days(self):
        r = self._run(["--json", "estimate", "--date", "2026-10-01", "--days", "-5"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("must be provided and positive", r.stderr)


class TestExpiryStates(ReceiptTestBase):
    def test_status_shows_expired(self):
        until = date.today() - timedelta(days=1)
        self.add("Old", days=30, until=until.isoformat())
        r = self._run(["--json", "status"])
        self.assertEqual(r.returncode, 0, r.stderr)
        entries = json.loads(r.stdout)["entries"]
        self.assertEqual(entries[0]["state"], "EXPIRED")

    def test_status_shows_remind_when_within_window(self):
        until = date.today() + timedelta(days=2)
        self.add("Soon", days=30, until=until.isoformat())
        r = self._run(["--json", "status"])
        self.assertEqual(r.returncode, 0, r.stderr)
        entries = json.loads(r.stdout)["entries"]
        self.assertEqual(entries[0]["state"], "REMIND")

    def test_status_shows_ok(self):
        until = date.today() + timedelta(days=365)
        self.add("Fine", days=365, until=until.isoformat())
        r = self._run(["--json", "status"])
        self.assertEqual(r.returncode, 0, r.stderr)
        entries = json.loads(r.stdout)["entries"]
        self.assertEqual(entries[0]["state"], "ok")

    def test_status_shows_no_warranty(self):
        self.add("NoWarranty", price=1)
        r = self._run(["--json", "status"])
        self.assertEqual(r.returncode, 0, r.stderr)
        entries = json.loads(r.stdout)["entries"]
        self.assertEqual(entries[0]["state"], "no-warranty")


class TestRemind(ReceiptTestBase):
    def setUp(self):
        super().setUp()
        self.config = {"remind_ahead_days": DEFAULT_REMIND_DAYS}
        with open(os.path.join(self.state, "config.json"), "w") as f:
            json.dump(self.config, f)

    def test_remind_marks_today(self):
        until = date.today() + timedelta(days=2)
        self.add("Soon", days=30, until=until.isoformat())
        r = self._run(["remind"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Soon", r.stdout)
        led = self.ledger()
        self.assertTrue(led["entries"]["Soon"]["reminded"])

    def test_remind_never_repeats(self):
        until = date.today() + timedelta(days=2)
        self.add("Soon", days=30, until=until.isoformat())
        self._run(["remind"])
        r = self._run(["remind"])
        self.assertEqual(r.returncode, 0, r.stderr)
        # remind prints plain text when nothing is due
        self.assertIn("nothing to remind", r.stdout)
        led = self.ledger()
        self.assertTrue(led["entries"]["Soon"]["reminded"])

    def test_remind_skips_without_warranty_until(self):
        self.add("NoCoverage", price=1)
        r = self._run(["remind"])
        self.assertEqual(r.returncode, 0, r.stderr)
        # no warranty window => nothing to remind (plain text)
        self.assertIn("nothing to remind", r.stdout)

    def test_remind_with_config_days(self):
        # Re-run within one test process where the config file is on disk
        # and the state dir persisted, matching the real CLI behavior.
        self.config["remind_ahead_days"] = 14
        with open(os.path.join(self.state, "config.json"), "w") as f:
            json.dump(self.config, f)
        until = date.today() + timedelta(days=10)
        self.add("W10", days=30, until=until.isoformat())
        self._run(["remind"])
        led = self.ledger()
        self.assertTrue(led["entries"]["W10"]["reminded"])

    def test_expired_reminder_prevents_old_entry_firing(self):
        until = date.today() - timedelta(days=10)
        self.add("Dead", days=30, until=until.isoformat())
        self._run(["remind"])
        led = self.ledger()
        self.assertTrue(led["entries"]["Dead"]["reminded"])


class TestRemoval(ReceiptTestBase, unittest.TestCase):
    def test_rm_delete(self):
        self.add("ToDelete", price=1, receipt="photo of receipt")
        r = self._run(["--json", "rm", "ToDelete"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["removed"], "ToDelete")
        self.assertEqual(len(self.ledger()["entries"]), 0)

    def test_rm_not_found(self):
        r = self._run(["rm", "Nobody"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not in ledger", r.stderr)


class TestConfiguration(ReceiptTestBase, unittest.TestCase):
    def test_config_set(self):
        rc, out, err = self._raw(["config", "--remind-ahead-days", "10"])
        self.assertEqual(rc, 0)
        self.assertEqual(out.strip(), "remind_ahead_days: 10")
        r2, out2, _ = self._raw(["config"])
        self.assertEqual(r2, 0)
        self.assertEqual(out2.strip(), "remind_ahead_days: 10")

    def test_config_set_rejects_negative(self):
        r = self._run(["config", "--remind-ahead-days", "-1"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(">= 0", r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
