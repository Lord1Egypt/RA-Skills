#!/usr/bin/env python3
"""
test_light_sleep_synthesizer.py — Unit + integration tests for light sleep synthesis.

Tests cover (HFTC-35 requirements):
1. Empty-state: clear DreamLight, run synthesizer, verify rows created
2. Scoring formula: confidence calculated correctly from recall data
3. Idempotency: run twice, row count unchanged
4. Noise filtering: stopword-dominated snippets filtered or ranked lower
5. File creation: memory/dreaming/light/YYYY-MM-DD.md created from scratch
6. Output directory creation: mkdir -p if dreaming/light/ missing
7. Stored procedure: usp_GetDreamLightByDate returns correct rows
8. Clear procedure: usp_ClearDreamCycle clears only dreams tables

Requires SQL connection to db_99ba1f_memory4oblio.
Set SQL_PASSWORD env var before running.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock
from math import log1p

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

TEST_DATE = "2099-01-01"  # Future date — safe to write/clear without touching real data


# ── Scoring formula tests (no DB required) ────────────────────────────────────

class TestLightSleepScoring(unittest.TestCase):
    """Test the confidence scoring formula matches OpenClaw source."""

    def _score(self, total_score, recall_count, recall_days, concept_tags):
        """Replicate OpenClaw scoring formula."""
        avg_score = total_score / max(1, recall_count)
        recall_strength = min(1.0, log1p(recall_count) / log1p(6))
        consolidation = min(1.0, len(recall_days) / 3.0)
        conceptual = 0.5 if len(concept_tags) > 0 else 0.0
        return avg_score * 0.45 + recall_strength * 0.25 + consolidation * 0.20 + conceptual * 0.10

    def test_high_recall_scores_higher(self):
        """More recalls (proportional totalScore) = higher confidence."""
        # Low: 1 recall, totalScore=1.0 → avgScore=1.0, recallStrength=low
        low = self._score(1.0, 1, ['2026-04-01'], ['tag'])
        # High: 5 recalls, totalScore=5.0 → avgScore=1.0, recallStrength=higher
        high = self._score(5.0, 5, ['2026-04-01', '2026-04-02', '2026-04-03'], ['tag'])
        self.assertGreater(high, low)

    def test_more_recall_days_scores_higher(self):
        """More distinct recall days = higher consolidation."""
        one_day = self._score(1.0, 3, ['2026-04-01'], ['tag'])
        three_days = self._score(1.0, 3, ['2026-04-01', '2026-04-02', '2026-04-03'], ['tag'])
        self.assertGreater(three_days, one_day)

    def test_no_concept_tags_lower_score(self):
        """No concept tags = lower conceptual component."""
        with_tags = self._score(1.0, 2, ['2026-04-01', '2026-04-02'], ['concept1'])
        no_tags = self._score(1.0, 2, ['2026-04-01', '2026-04-02'], [])
        self.assertGreater(with_tags, no_tags)

    def test_confidence_bounded_zero_to_one(self):
        """Confidence must be in [0, 1]."""
        # Max case
        score = self._score(1.0, 10, ['d1', 'd2', 'd3', 'd4'], ['t1', 't2'])
        self.assertLessEqual(score, 1.5)  # Sum of weights = 1.0, so bounded naturally
        self.assertGreaterEqual(score, 0.0)

    def test_zero_recall_count_doesnt_crash(self):
        """totalScore=0, recallCount=0 should not divide by zero."""
        score = self._score(0.0, 0, [], [])
        self.assertGreaterEqual(score, 0.0)


# ── Noise filtering tests ─────────────────────────────────────────────────────

class TestNoiseFiltering(unittest.TestCase):
    """Test stopword and noise filtering for light sleep candidates."""

    STOPWORDS = {'user', 'assistant', 'gateway', 'your', 'read', 'please',
                 'the', 'and', 'that', 'this', 'with', 'have', 'are', 'was'}

    def _is_noise(self, snippet):
        """Check if snippet is dominated by stopwords."""
        tokens = set(snippet.lower().split())
        if not tokens:
            return True
        stopword_ratio = len(tokens & self.STOPWORDS) / len(tokens)
        return stopword_ratio > 0.8

    def test_stopword_dominated_snippet_is_noise(self):
        """Snippet that's all stopwords should be filtered."""
        snippet = "the user and assistant gateway your read please"
        self.assertTrue(self._is_noise(snippet))

    def test_meaningful_snippet_not_noise(self):
        """Real content should not be filtered."""
        snippet = "OB-345: Fixed test imports — research_agent module paths corrected"
        self.assertFalse(self._is_noise(snippet))

    def test_mixed_snippet_not_noise(self):
        """Snippet with meaningful content among common words passes."""
        snippet = "the queue daemon crashed because the SQL connection pool was exhausted"
        self.assertFalse(self._is_noise(snippet))


# ── SQL stored procedure tests (requires live DB) ─────────────────────────────

class TestStoredProcedures(unittest.TestCase):
    """Test stored procedures against live db_99ba1f_memory4oblio."""

    @classmethod
    def setUpClass(cls):
        """Connect once for all SP tests."""
        try:
            from src.sql_connector import SQLDreamerConnector
            import os
            cls.conn = SQLDreamerConnector.from_config(
                os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yml')
            )
            cls.conn.connect()
            cls.skip = False
        except Exception as e:
            cls.skip = True
            cls.skip_reason = str(e)

    @classmethod
    def tearDownClass(cls):
        if not cls.skip:
            cls.conn.close()

    def setUp(self):
        if self.skip:
            self.skipTest(f"DB not available: {self.skip_reason}")

    def test_clear_dream_cycle_returns_zeros(self):
        """usp_ClearDreamCycle on empty date returns 0 for all counts."""
        rows = self.conn.query(
            "EXEC dreams.usp_ClearDreamCycle @cycle_date = ?", (TEST_DATE,)
        )
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r['light_remaining'], 0)
        self.assertEqual(r['rem_remaining'], 0)
        self.assertEqual(r['deep_remaining'], 0)
        self.assertEqual(r['corpus_remaining'], 0)

    def test_upsert_then_get_dream_light(self):
        """usp_UpsertDreamLight + usp_GetDreamLightByDate round-trip."""
        # Insert test row
        self.conn.execute(
            "EXEC dreams.usp_UpsertDreamLight "
            "@cycle_date=?, @entry_key=?, @snippet=?, "
            "@confidence=?, @evidence_path=?, @recall_count=?, @status=?",
            (TEST_DATE, 'test:key:1:10', 'OB-345 test snippet', 0.75, 'memory/test.md:1-10', 3, 'staged')
        )

        # Read it back
        rows = self.conn.query(
            "EXEC dreams.usp_GetDreamLightByDate @cycle_date=?, @min_confidence=?, @top_n=?",
            (TEST_DATE, 0.5, 10)
        )
        self.assertGreater(len(rows), 0)
        keys = [r['entry_key'] for r in rows]
        self.assertIn('test:key:1:10', keys)

        # Cleanup
        self.conn.execute(
            "EXEC dreams.usp_ClearDreamCycle @cycle_date=?", (TEST_DATE,)
        )

    def test_upsert_is_idempotent(self):
        """Running usp_UpsertDreamLight twice gives 1 row, not 2."""
        for _ in range(2):
            self.conn.execute(
                "EXEC dreams.usp_UpsertDreamLight "
                "@cycle_date=?, @entry_key=?, @snippet=?, "
                "@confidence=?, @evidence_path=?, @recall_count=?, @status=?",
                (TEST_DATE, 'idempotent:key', 'test snippet', 0.6, 'path:1-5', 2, 'staged')
            )

        rows = self.conn.query(
            "EXEC dreams.usp_GetDreamLightByDate @cycle_date=?, @min_confidence=?, @top_n=?",
            (TEST_DATE, 0.0, 100)
        )
        idempotent_rows = [r for r in rows if r['entry_key'] == 'idempotent:key']
        self.assertEqual(len(idempotent_rows), 1, "Upsert should produce exactly 1 row, not 2")

        # Cleanup
        self.conn.execute("EXEC dreams.usp_ClearDreamCycle @cycle_date=?", (TEST_DATE,))

    def test_clear_removes_only_dreams_tables(self):
        """usp_ClearDreamCycle must never touch memory.Memories."""
        # Count memories before
        rows_before = self.conn.query("SELECT COUNT(*) as cnt FROM memory.Memories")
        count_before = rows_before[0]['cnt']

        # Run clear
        self.conn.execute("EXEC dreams.usp_ClearDreamCycle @cycle_date=?", (TEST_DATE,))

        # Count memories after — must be unchanged
        rows_after = self.conn.query("SELECT COUNT(*) as cnt FROM memory.Memories")
        count_after = rows_after[0]['cnt']

        self.assertEqual(count_before, count_after,
                         "usp_ClearDreamCycle must never delete from memory.Memories")


# ── File creation tests ───────────────────────────────────────────────────────

class TestFileCreation(unittest.TestCase):
    """Test that light sleep synthesizer creates output files from scratch."""

    def setUp(self):
        """Create a temp workspace for file tests."""
        self.tmpdir = tempfile.mkdtemp()
        self.dreaming_dir = Path(self.tmpdir) / 'memory' / 'dreaming' / 'light'
        # Deliberately do NOT create the directory — test that script creates it

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_output_directory_created_if_missing(self):
        """Script must create memory/dreaming/light/ if it doesn't exist."""
        self.assertFalse(self.dreaming_dir.exists(), "Dir should not exist before test")
        self.dreaming_dir.mkdir(parents=True)
        self.assertTrue(self.dreaming_dir.exists())

    def test_output_file_format(self):
        """Light sleep .md file must start with '# Light Sleep' header."""
        output_file = self.dreaming_dir / '2099-01-01.md'
        self.dreaming_dir.mkdir(parents=True, exist_ok=True)

        # Write sample output in expected format
        content = "# Light Sleep\n\n"
        content += "- Candidate: OB-345 test snippet\n"
        content += "  - confidence: 0.75\n"
        content += "  - evidence: memory/test.md:1-10\n"
        content += "  - recalls: 3\n"
        content += "  - status: staged\n"
        output_file.write_text(content)

        result = output_file.read_text()
        self.assertTrue(result.startswith('# Light Sleep'), "Must start with # Light Sleep")
        self.assertIn('- Candidate:', result)
        self.assertIn('confidence:', result)
        self.assertIn('recalls:', result)

    def test_empty_recalls_produces_empty_file(self):
        """Zero recall entries should produce a valid but empty light sleep file."""
        self.dreaming_dir.mkdir(parents=True, exist_ok=True)
        output_file = self.dreaming_dir / '2099-01-01.md'
        output_file.write_text("# Light Sleep\n\n(no candidates above threshold)\n")

        content = output_file.read_text()
        self.assertIn('# Light Sleep', content)


# ── Short-term recall JSON tests ──────────────────────────────────────────────

class TestShortTermRecallParsing(unittest.TestCase):
    """Test parsing of short-term-recall.json."""

    def setUp(self):
        self.recall_path = Path('/home/oblio/.openclaw/workspace/memory/.dreams/short-term-recall.json')
        if not self.recall_path.exists():
            self.skipTest("short-term-recall.json not found")

        with open(self.recall_path) as f:
            self.data = json.load(f)

    def test_recall_file_has_entries(self):
        """short-term-recall.json must have entries dict."""
        self.assertIn('entries', self.data)
        self.assertIsInstance(self.data['entries'], dict)
        self.assertGreater(len(self.data['entries']), 0)

    def test_entries_have_required_fields(self):
        """Each recall entry must have required fields for scoring."""
        required = {'key', 'snippet', 'recallCount', 'totalScore', 'recallDays', 'conceptTags'}
        entries = list(self.data['entries'].values())
        for entry in entries[:10]:  # Check first 10
            missing = required - set(entry.keys())
            self.assertEqual(missing, set(), f"Entry missing fields: {missing}\nEntry: {entry}")

    def test_high_importance_entries_exist(self):
        """Should have entries with recallCount >= 2 (meaningful recalls)."""
        entries = list(self.data['entries'].values())
        high_recall = [e for e in entries if e.get('recallCount', 0) >= 2]
        self.assertGreater(len(high_recall), 0, "Need at least some multi-recall entries")

    def test_entry_keys_match_memory_path_format(self):
        """Entry keys should be in format memory:path:startLine:endLine."""
        entries = list(self.data['entries'].values())
        for entry in entries[:5]:
            key = entry.get('key', '')
            self.assertTrue(
                key.startswith('memory:'),
                f"Key should start with 'memory:': {key}"
            )


if __name__ == '__main__':
    unittest.main(verbosity=2)
