#!/usr/bin/env python3
"""Tests for subscription-auditor skill.

Self-contained: per-test temp state dir, subprocess-run CLI.
Run: python3 -m pytest test_skill.py -v
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CMD = os.path.join(SKILL_DIR, "subscription_auditor.py")


class SubscriptionAuditorTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sa-test-")
        self.state = os.path.join(self.tmp, "state")
        os.makedirs(self.state)
        os.environ["SUBSCRIPTION_AUDITOR_STATE_DIR"] = self.state
        self.env = os.environ.copy()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        os.environ.pop("SUBSCRIPTION_AUDITOR_STATE_DIR", None)

    def run_skill(self, argv):
        return subprocess.run([sys.executable, CMD] + argv,
                              capture_output=True, text=True, env=self.env, timeout=30)

    def add(self, *args):
        return self.run_skill(["--json", "add"] + list(args))

    def ledger(self):
        with open(os.path.join(self.state, "ledger.json")) as f:
            return json.load(f)

    def config(self):
        with open(os.path.join(self.state, "config.json")) as f:
            return json.load(f)

    def days_ahead(self, n):
        return (date.today() + timedelta(days=n)).isoformat()


class TestAdd(SubscriptionAuditorTestBase):
    def test_add_basic(self):
        r = self.add("Netflix", "--cost", "15.99", "--next-renewal", self.days_ahead(30),
                     "--cycle", "monthly")
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        out = json.loads(r.stdout)
        led = self.ledger()
        self.assertIn(out["id"], led["entries"])
        e = led["entries"][out["id"]]
        self.assertEqual(e["cycle"], "monthly")
        self.assertEqual(e["cost"], 15.99)

    def test_add_defaults(self):
        r = self.add("Spotify", "--cost", "9.99")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        e = self.ledger()["entries"][out["id"]]
        self.assertEqual(e["cycle"], "monthly")
        self.assertEqual(e["currency"], "USD")
        # default renewal = today + 30, allow small clock slack
        days = (date.fromisoformat(e["next_renewal"]) - date.today()).days
        self.assertIn(days, (29, 30))

    def test_add_idempotent_by_name(self):
        self.add("Gym", "--cost", "10.00")
        self.add("Gym", "--cost", "12.00")
        led = self.ledger()
        self.assertEqual(len(led["entries"]), 1)
        self.assertEqual(led["entries"]["gym"]["cost"], 12.00)

    def test_add_ids_normalized(self):
        r = self.add("IDE Rider", "--cost", "1.00")
        self.assertEqual(json.loads(r.stdout)["id"], "ide_rider")

    def test_add_rejects_negative_cost(self):
        # regression: negative cost previously stored and poisoned totals
        r = self.add("Neg", "--cost", "-50")
        self.assertNotEqual(r.returncode, 0)
        led = self.ledger()
        self.assertEqual(led["entries"], {})

    def test_add_rejects_bad_date(self):
        r = self.add("Bad", "--cost", "1.00", "--next-renewal", "not-a-date")
        self.assertNotEqual(r.returncode, 0)

    def test_add_all_cycles_valid(self):
        for cycle in ("monthly", "yearly", "quarterly", "weekly", "daily"):
            r = self.add(f"C{cycle}", "--cost", "10.00", "--cycle", cycle)
            self.assertEqual(r.returncode, 0, r.stderr)


class TestCycleMath(SubscriptionAuditorTestBase):
    def _status(self, cycles_costs):
        now = date.today().year
        for i, (cycle, cost) in enumerate(cycles_costs):
            self.add(f"S{i}", "--cost", str(cost),
                     "--cycle", cycle, "--next-renewal", f"{now + 1}-01-01")
        r = self.run_skill(["--json", "status"])
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def test_monthly(self):
        out = self._status([("monthly", 10.0)])
        self.assertAlmostEqual(out["total_monthly"], 10.0, places=2)
        self.assertAlmostEqual(out["total_yearly"], 120.0, places=2)

    def test_yearly(self):
        out = self._status([("yearly", 120.0)])
        self.assertAlmostEqual(out["total_monthly"], 10.0, places=2)
        self.assertAlmostEqual(out["total_yearly"], 120.0, places=2)

    def test_quarterly(self):
        out = self._status([("quarterly", 30.0)])
        self.assertAlmostEqual(out["total_monthly"], 10.0, places=2)
        self.assertAlmostEqual(out["total_yearly"], 120.0, places=2)

    def test_weekly(self):
        out = self._status([("weekly", 10.0)])
        self.assertAlmostEqual(out["total_monthly"], 10.0 * 52 / 12, places=2)
        self.assertAlmostEqual(out["total_yearly"], 520.0, places=2)

    def test_daily(self):
        out = self._status([("daily", 1.0)])
        self.assertAlmostEqual(out["total_monthly"], 365 / 12, places=2)
        self.assertAlmostEqual(out["total_yearly"], 365.0, places=2)


class TestStatusRemind(SubscriptionAuditorTestBase):
    def test_status_upcoming_sorted_and_flags(self):
        self.add("Soon", "--cost", "5.00", "--next-renewal", self.days_ahead(2))
        self.add("Later", "--cost", "5.00", "--next-renewal", self.days_ahead(60))
        r = self.run_skill(["--json", "status"])
        out = json.loads(r.stdout)
        ups = out["upcoming"]
        self.assertEqual(ups[0]["name"], "Soon")

    def test_status_past_due_day_negative_not_clamped(self):
        # regression: old code clamped days_left at 0, hiding overdue-ness
        self.add("Overdue", "--cost", "5.00", "--next-renewal",
                 (date.today() - timedelta(days=8)).isoformat())
        r = self.run_skill(["--json", "status"])
        out = json.loads(r.stdout)
        self.assertEqual(out["upcoming"][0]["days_left"], -8)

    def test_status_human_shows_past_due_flag(self):
        self.add("Overdue", "--cost", "5.00", "--next-renewal",
                 (date.today() - timedelta(days=3)).isoformat())
        r = self.run_skill(["status"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("PAST-DUE", r.stdout)

    def test_remind_filters_by_days(self):
        self.add("SoonSub", "--cost", "5.00", "--next-renewal", self.days_ahead(2))
        self.add("LaterSub", "--cost", "5.00", "--next-renewal", self.days_ahead(30))
        r = self.run_skill(["--json", "remind", "--days", "7"])
        items = json.loads(r.stdout)
        names = [i["name"] for i in items]
        self.assertIn("SoonSub", names)
        self.assertNotIn("LaterSub", names)

    def test_remind_includes_past_due(self):
        self.add("OldSub", "--cost", "5.00", "--next-renewal",
                 (date.today() - timedelta(days=20)).isoformat())
        r = self.run_skill(["--json", "remind", "--days", "7"])
        items = json.loads(r.stdout)
        self.assertEqual([i["name"] for i in items], ["OldSub"])
        self.assertEqual(items[0]["days_left"], -20)

    def test_remind_uses_config_days(self):
        self.run_skill(["config", "--remind-ahead-days", "10"])
        self.add("Soonish", "--cost", "3.00", "--next-renewal", self.days_ahead(5))
        r = self.run_skill(["--json", "remind"])
        items = json.loads(r.stdout)
        self.assertTrue(any(i["name"] == "Soonish" for i in items))

    def test_empty_state(self):
        r = self.run_skill(["status"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("subs: 0", r.stdout)
        r = self.run_skill(["remind", "--days", "7"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("nothing renews", r.stdout)
        r = self.run_skill(["--json", "list"])
        self.assertEqual(json.loads(r.stdout), {})


class TestRmConfig(SubscriptionAuditorTestBase):
    def test_rm_removes_entry(self):
        r = self.add("Temp", "--cost", "1.00")
        sid = json.loads(r.stdout)["id"]
        r = self.run_skill(["--json", "rm", sid])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["removed"], sid)
        self.assertNotIn(sid, self.ledger()["entries"])

    def test_rm_unknown_fails(self):
        r = self.run_skill(["rm", "nope"])
        self.assertNotEqual(r.returncode, 0)

    def test_config_get_and_set(self):
        r = self.run_skill(["--json", "config", "--remind-ahead-days", "14"])
        cfg = json.loads(r.stdout)
        self.assertEqual(cfg["remind_ahead_days"], 14)
        r = self.run_skill(["--json", "config"])
        self.assertEqual(json.loads(r.stdout)["remind_ahead_days"], 14)

    def test_config_rejects_zero(self):
        r = self.run_skill(["config", "--remind-ahead-days", "0"])
        self.assertNotEqual(r.returncode, 0)

    def test_config_rejects_empty_currency(self):
        r = self.run_skill(["config", "--currency", "  "])
        self.assertNotEqual(r.returncode, 0)

    def test_currency_applies_to_new_entries(self):
        self.run_skill(["config", "--currency", "EUR"])
        r = self.add("Thing", "--cost", "5.00")
        sid = json.loads(r.stdout)["id"]
        self.assertEqual(self.ledger()["entries"][sid]["currency"], "EUR")


class TestStateIntegrity(SubscriptionAuditorTestBase):
    def test_corrupt_ledger_fails_cleanly(self):
        with open(os.path.join(self.state, "ledger.json"), "w") as f:
            f.write("{bad")
        r = self.add("X", "--cost", "1.00")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("ledger unreadable", (r.stderr or r.stdout))

    def test_version_mismatch_fails(self):
        with open(os.path.join(self.state, "ledger.json"), "w") as f:
            json.dump({"version": 2, "entries": {}}, f)
        r = self.add("X", "--cost", "1.00")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("unrecognized", (r.stderr or r.stdout))

    def test_empty_ledger_file_recovers(self):
        # zero-byte ledger is a common crash artifact; treat like missing
        with open(os.path.join(self.state, "ledger.json"), "w"):
            pass
        r = self.add("X", "--cost", "1.00")
        self.assertEqual(r.returncode, 0, (r.stderr or r.stdout))

    def test_auto_renew_flag(self):
        r = self.add("Service", "--cost", "10.00", "--no-auto-renew")
        sid = json.loads(r.stdout)["id"]
        self.assertFalse(self.ledger()["entries"][sid]["auto_renew"])

    def test_ledger_write_is_atomic_and_sorted(self):
        self.add("B Second", "--cost", "2")
        self.add("A First", "--cost", "1")
        with open(os.path.join(self.state, "ledger.json")) as f:
            raw = f.read()
        self.assertTrue(raw.endswith("\n"))
        text = json.loads(raw)
        self.assertEqual(set(text["entries"]), {"b_second", "a_first"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
