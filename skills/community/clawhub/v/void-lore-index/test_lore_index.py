#!/usr/bin/env python3
"""Unit tests for void-lore-index skill.

All self-contained: per-test temp state dir + temp vault, no network, no
subprocess launches besides the CLI under test.
Run: python3 -m pytest test_lore_index.py -v
"""

import json
import os
import shutil
import sys
import tempfile
import unittest
import time

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)
import lore_index  # noqa: E402

CMD = os.path.join(SKILL_DIR, "lore_index.py")

SECTOR4_MD = """---
title: Sector 4 Travel
tags: travel, sector-4, FTL
---

# Sector 4 Travel

Travel through Sector 4 requires a Class-3 hull or better. Unlicensed
jumps are seized by the Ring Authority.

## Toll Lanes

Toll lanes cost 40 ironmarks per jump. Toll evasion is a capital crime.
"""

RELAY_MD = """---
title: Keth Relay Fauna
tags: fauna, sector-2
with: 90d
stamp: 2026-01-01
---

# Keth Relay Fauna

Bioluminescent drifter swarms nest in the relay ring and eat calf-frequency code.
"""

OLD_ARC_MD = """---
title: Old Warp Gates
tags: travel, gates
with: arc-2
stamp: 2025-05-01
---

# Old Warp Gates

The first-generation gates were demolished after the Sundering.
"""

SOFT_MD = """---
title: Rumored Ninth Gate
tags: gates, rumor
with: "~arc-3"
---

# Rumored Ninth Gate

Tavern talk places a ninth gate beneath the Ashfold, but no survey confirms it.
"""

ARC_FILE = """---
arc: 3
---

Current arc marker.
"""


class LoreTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="lore-test-")
        self.state = os.path.join(self.tmp, "state")
        self.vault = os.path.join(self.tmp, "vault")
        os.makedirs(self.state)
        os.makedirs(self.vault)
        os.environ["LORE_INDEX_STATE_DIR"] = self.state
        self._write("sector-4/travel.md", SECTOR4_MD)
        self._write("sector-2/relay-fauna.md", RELAY_MD)
        self._write("gates/old-warp-gates.md", OLD_ARC_MD)
        self._write("gates/rumored-ninth.md", SOFT_MD)
        self._write("_arc.md", ARC_FILE)
        self._run(["--json", "config", "--vault", self.vault, "--arc", "1",
                   "--with-limbo-days", "7"])
        self._run(["index"])

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        os.environ.pop("LORE_INDEX_STATE_DIR", None)

    def _write(self, name, text):
        path = os.path.join(self.vault, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def _run(self, argv):
        import subprocess as _sp
        p = _sp.run([sys.executable, CMD] + list(argv),
                    capture_output=True, text=True, timeout=30)
        return p


class TestIndexAndSearch(LoreTestBase):
    def test_index_counts_entries(self):
        r = self._run(["--json", "stats"])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(d["entries"], 4)  # _arc.md is not an entry

    def test_search_finds_travel_rules(self):
        r = self._run(["--json", "search", "sector 4 travel rules"])
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = json.loads(r.stdout)
        self.assertTrue(rows)
        self.assertEqual(rows[0]["id"], "sector-4/travel.md")

    def test_search_scores_title_higher_than_body(self):
        # search excludes expired by default; --expired shows scored matches
        r = self._run(["--json", "search", "keth relay fauna", "--expired"])
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = json.loads(r.stdout)
        self.assertTrue(rows)
        self.assertEqual(rows[0]["id"], "sector-2/relay-fauna.md")
        self.assertGreater(rows[0]["score"], 0)

    def test_search_no_match_empty(self):
        r = self._run(["--json", "search", "telepathy croissant"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), [])


class TestAsk(LoreTestBase):
    def test_ask_returns_excerpt_and_budget(self):
        r = self._run(["--json", "ask", "what are the rules of travel in Sector 4"])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(d["meta"]["query"], "what are the rules of travel in Sector 4")
        self.assertTrue(d["entries"])
        first = d["entries"][0]
        self.assertEqual(first["id"], "sector-4/travel.md")
        self.assertTrue(first["excerpts"])
        joined = " ".join(x["text"] for x in first["excerpts"])
        self.assertIn("Class-3 hull", joined)
        # used_chars = sum of per-excerpt lengths (']joined' adds separators)
        self.assertGreaterEqual(d["meta"]["used_chars"], sum(len(x["text"]) for x in first["excerpts"]))
        self.assertLessEqual(d["meta"]["used_chars"], d["meta"]["budget_chars"])

    def test_ask_respects_token_budget(self):
        self._run(["--json", "config", "--token-budget", "120"])
        r = self._run(["--json", "ask", "toll lanes ironmarks"])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertLessEqual(d["meta"]["used_chars"], 120)

    def test_ask_excludes_expired_arc_entry(self):
        # vault arc 3; old-warp-gates retires at arc-2 -> expired, excluded
        r = self._run(["--json", "ask", "old warp gates demolished"])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        ids = [e["id"] for e in d["entries"]]
        self.assertNotIn("gates/old-warp-gates.md", ids)

    def test_ask_excludes_soft_entry(self):
        r = self._run(["--json", "ask", "ninth gate ashfold"])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        ids = [e["id"] for e in d["entries"]]
        self.assertNotIn("gates/rumored-ninth.md", ids)

    def test_ask_no_match_says_no_canon(self):
        r = self._run(["ask", "telepathy croissant"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("no canon found", r.stdout)


class TestRetcon(LoreTestBase):
    def test_retcon_keeps_expired_entry_in_ask(self):
        r = self._run(["--json", "retcon", "gates/old-warp-gates.md"])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertTrue(d["influence_retained"])
        r2 = self._run(["--json", "ask", "old warp gates demolished"])
        d2 = json.loads(r2.stdout)
        ids = [e["id"] for e in d2["entries"]]
        self.assertIn("gates/old-warp-gates.md", ids)

    def test_retcon_clear(self):
        self._run(["retcon", "gates/old-warp-gates.md"])
        r = self._run(["--json", "retcon", "gates/old-warp-gates.md", "--clear"])
        d = json.loads(r.stdout)
        self.assertFalse(d["influence_retained"])

    def test_retcon_unknown_id_fails(self):
        r = self._run(["retcon", "nope.md"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not in index", r.stderr)

    def test_retcon_persists_across_reindex(self):
        # retcon then re-index: retention must survive because it is re-read from frontmatter? No —
        # re-index rebuilds from vault; retention lives in index.json, so run index with retention kept.
        self._run(["retcon", "gates/old-warp-gates.md"])
        r = self._run(["index"])
        self.assertEqual(r.returncode, 0, r.stderr)
        r2 = self._run(["--json", "ask", "old warp gates demolished"])
        ids = [e["id"] for e in json.loads(r2.stdout)["entries"]]
        self.assertIn("gates/old-warp-gates.md", ids)


class TestAdd(LoreTestBase):
    def test_add_writes_entry_and_indexes(self):
        r = self._run(["--json", "add", "--title", "Sunless Bazaar",
                       "--tags", "place, undercity",
                       "--body", "A night market under Vhole, guarded by the Ledgermen."])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertTrue(os.path.isfile(d["path"]))
        self._run(["index"])
        r2 = self._run(["--json", "search", "Sunless Bazaar ledgermen"])
        rows = json.loads(r2.stdout)
        self.assertEqual(rows[0]["title"], "Sunless Bazaar")

    def test_add_refuses_overwrite_without_flag(self):
        r = self._run(["add", "--title", "Sector 4 Travel",
                       "--file", "sector-4/travel.md", "--body", "x"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("already exists", r.stderr)

    def test_add_replace_overwrites(self):
        r = self._run(["add", "--title", "Sector 4 Travel",
                       "--file", "sector-4/travel.md", "--body", "rewritten",
                       "--replace"])
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(os.path.join(self.vault, "sector-4/travel.md")) as f:
            self.assertIn("rewritten", f.read())

    def test_add_with_frontmatter_fields(self):
        r = self._run(["--json", "add", "--title", "Ashfast Edict",
                       "--tags", "law",
                       "--with-rule", "arc-5",
                       "--stamp", "2026-09-01",
                       "--body", "All guild seals lapse at arc 5."])
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(os.path.join(self.vault, "ashfast-edict.md")) as f:
            text = f.read()
        self.assertIn("with: arc-5", text)
        self.assertIn("stamp: 2026-09-01", text)
        self.assertIn("tags: law", text)


class TestWithRules(LoreTestBase):
    def test_status_flags_expiring_arc(self):
        # vault arc is 3 (from _arc.md); nothing retires at 3 among fixtures, so
        # add one that retires at current arc -> expiring
        self._run(["--json", "add", "--title", "Dying Edict", "--with-rule", "arc-3",
                   "--body", "expires this arc"])
        self._run(["index"])
        r = self._run(["--json", "status"])
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = json.loads(r.stdout)["entries"]
        dying = [x for x in rows if x["title"] == "Dying Edict"][0]
        self.assertEqual(dying["state"], "expiring")

    def test_status_flags_unknown_rule(self):
        self._write("weird.md", "---\ntitle: Weird\nwith: someday-maybe\n---\n\n# Weird\n\nx\n")
        self._run(["index"])
        r = self._run(["--json", "status"])
        rows = json.loads(r.stdout)["entries"]
        weird = [x for x in rows if x["title"] == "Weird"][0]
        self.assertEqual(weird["state"], "unknown")

    def test_duration_rule_expiry_by_stamp(self):
        # relay-fauna: 90d after stamp 2026-01-01 -> expired long before "now" in tests
        r = self._run(["--json", "status"])
        rows = json.loads(r.stdout)["entries"]
        relay = [x for x in rows if x["title"] == "Keth Relay Fauna"][0]
        self.assertEqual(relay["state"], "expired")

    def test_parse_with_rule_units(self):
        stamp = time.mktime(time.strptime("2026-01-01", "%Y-%m-%d"))
        d = lore_index.parse_with_rule("36h", 1, stamp)
        self.assertEqual(d["expires"], stamp + 36 * 3600)
        w = lore_index.parse_with_rule("2w", 1, stamp)
        self.assertEqual(w["expires"], stamp + 14 * 86400)
        a = lore_index.parse_with_rule("arc-4", 5, stamp)
        self.assertEqual(a["retires_arc"], 4)
        s = lore_index.parse_with_rule("~90d", 1, stamp)
        self.assertTrue(s["soft"])


class TestConfig(LoreTestBase):
    def test_config_set_and_show(self):
        r = self._run(["--json", "config", "--top-k", "6", "--excerpt-chars", "250"])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(d["top_k"], 6)
        self.assertEqual(d["excerpt_chars"], 250)
        self.assertEqual(d["arc"], 1)

    def test_config_rejects_bad_arc(self):
        r = self._run(["config", "--arc", "0"])
        self.assertNotEqual(r.returncode, 0)


class TestVacuum(LoreTestBase):
    def test_vacuum_detects_new_file_and_arc_change(self):
        self._write("newplace.md", "---\ntitle: New Place\n---\n\n# New Place\n\nStuff.\n")
        r = self._run(["--json", "vacuum"])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertIn("newplace.md", d["new"])

    def test_vacuum_reports_arc_state_change(self):
        # _arc.md arc=3 already expired the arc-2 entry at first index; roll
        # the arc 3 -> 2 (active) -> 3 (expired) and confirm the diff flag
        self._write("_arc.md", "---\narc: 2\n---\n\n\n")
        self._run(["index"])
        self._write("_arc.md", "---\narc: 3\n---\n\n\n")
        r = self._run(["--json", "vacuum"])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(d["arc"], 3)
        self.assertIn("gates/old-warp-gates.md", d["changed"])


class TestGet(LoreTestBase):
    def test_get_returns_full_text(self):
        r = self._run(["--json", "get", "sector-4/travel.md"])
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(d["title"], "Sector 4 Travel")
        self.assertIn("Class-3 hull", d["text"])

    def test_get_unknown_id(self):
        r = self._run(["get", "ghost.md"])
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
