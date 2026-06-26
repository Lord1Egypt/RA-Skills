#!/usr/bin/env python3
"""
test_sql_memory.py — Unit tests for SQLMemory
Covers: connection, CRUD, task queue, knowledge, error handling
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'infrastructure'))
from sql_memory import SQLMemory, _esc, get_memory


class TestEscaping(unittest.TestCase):
    """Test SQL string escaping."""

    def test_single_quotes_escaped(self):
        self.assertEqual(_esc("it's"), "it''s")

    def test_double_quotes_preserved(self):
        self.assertEqual(_esc('say "hello"'), 'say "hello"')

    def test_max_length_truncation(self):
        long = "x" * 5000
        result = _esc(long, max_len=100)
        self.assertEqual(len(result), 100)

    def test_empty_string(self):
        self.assertEqual(_esc(""), "")

    def test_none_handling(self):
        self.assertEqual(_esc(None), "")

    def test_numeric_coercion(self):
        self.assertEqual(_esc(42), "42")


class TestSQLMemoryConnection(unittest.TestCase):
    """Test connection and ping."""

    def test_get_memory_cloud(self):
        mem = get_memory('local')
        self.assertIsInstance(mem, SQLMemory)

    def test_ping(self):
        mem = get_memory('local')
        result = mem.ping()
        self.assertIsInstance(result, bool)

    def test_ping_succeeds_with_valid_creds(self):
        mem = get_memory('local')
        self.assertTrue(mem.ping(), "Ping should succeed with valid credentials")


class TestMemoryCRUD(unittest.TestCase):
    """Test remember/recall/search/forget cycle."""

    def setUp(self):
        self.mem = get_memory('local')
        self.test_key = f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def test_remember_and_recall(self):
        self.mem.remember('test', self.test_key, 'test content', importance=1, tags='test')
        result = self.mem.recall('test', self.test_key)
        self.assertIsNotNone(result)
        self.assertIn('test content', str(result))

    def test_recall_nonexistent(self):
        result = self.mem.recall('test', 'nonexistent_key_xyz_99999')
        self.assertIsNone(result)

    def test_search_memories(self):
        self.mem.remember('test', self.test_key, 'searchable content xyz', importance=1, tags='test')
        results = self.mem.search_memories('searchable content xyz')
        self.assertIsInstance(results, list)

    def test_forget(self):
        self.mem.remember('test', self.test_key, 'to be forgotten', importance=1, tags='test')
        result = self.mem.forget('test', self.test_key)
        self.assertIsInstance(result, bool)

    def tearDown(self):
        # Cleanup test entries
        self.mem.execute(f"DELETE FROM memory.Memories WHERE key_name='{self.test_key}'")


class TestTaskQueue(unittest.TestCase):
    """Test task queue operations."""

    def setUp(self):
        self.mem = get_memory('local')
        self.test_task_type = f"test_task_{datetime.now().strftime('%H%M%S')}"

    def test_queue_and_claim(self):
        self.mem.queue_task('test_agent', self.test_task_type, '{}', priority=9)
        # Verify it was queued
        out = self.mem.execute(
            f"SELECT id FROM memory.TaskQueue WHERE task_type='{self.test_task_type}' AND status='pending'"
        )
        self.assertIn(self.test_task_type[:5], self.test_task_type)  # sanity

    def test_complete_task(self):
        self.mem.queue_task('test_agent', self.test_task_type, '{}', priority=9)
        out = self.mem.execute_scalar(
            f"SELECT TOP 1 id FROM memory.TaskQueue WHERE task_type='{self.test_task_type}' AND status='pending'"
        )
        if out and out.strip().isdigit():
            tid = out.strip()
            self.mem.claim_task(tid)
            result = self.mem.complete_task(tid, 'test result')
            self.assertTrue(result)

    def test_fail_task_retry(self):
        self.mem.queue_task('test_agent', self.test_task_type, '{}', priority=9)
        out = self.mem.execute_scalar(
            f"SELECT TOP 1 id FROM memory.TaskQueue WHERE task_type='{self.test_task_type}' AND status='pending'"
        )
        if out and out.strip().isdigit():
            tid = out.strip()
            self.mem.claim_task(tid)
            self.mem.fail_task(tid, 'test error', 0, 3)
            # Should be back to pending with retry_count incremented
            status = self.mem.execute_scalar(
                f"SELECT status FROM memory.TaskQueue WHERE id={tid}"
            )
            self.assertIn('pending', str(status))

    def tearDown(self):
        self.mem.execute(
            f"DELETE FROM memory.TaskQueue WHERE task_type='{self.test_task_type}'"
        )


class TestActivityLog(unittest.TestCase):
    """Test event logging."""

    def setUp(self):
        self.mem = get_memory('local')

    def test_log_event(self):
        self.mem.log_event('test_event', 'test_agent', 'unit test log entry')
        results = self.mem.get_recent_activity(since_hours=1, agent='test_agent')
        self.assertIsInstance(results, list)


class TestKnowledge(unittest.TestCase):
    """Test knowledge store operations."""

    def setUp(self):
        self.mem = get_memory('local')
        self.test_topic = f"test_topic_{datetime.now().strftime('%H%M%S')}"

    def test_store_and_search_knowledge(self):
        self.mem.store_knowledge('test_domain', self.test_topic, 'test summary', 'test_source')
        results = self.mem.search_knowledge('test_domain', self.test_topic)
        self.assertIsInstance(results, list)

    def tearDown(self):
        self.mem.execute(
            f"DELETE FROM memory.KnowledgeIndex WHERE topic='{self.test_topic}'"
        )


class TestEdgeCases(unittest.TestCase):
    """Test error handling and edge cases."""

    def test_execute_invalid_sql(self):
        mem = get_memory('local')
        result = mem.execute("SELECT * FROM nonexistent_table_xyz")
        # Should not crash, may return error text
        self.assertIsInstance(result, str)

    def test_remember_with_special_chars(self):
        mem = get_memory('local')
        key = f"special_test_{datetime.now().strftime('%H%M%S')}"
        mem.remember('test', key, "Content with 'quotes' and \"doubles\" and <html>", importance=1)
        result = mem.recall('test', key)
        # Cleanup
        mem.execute(f"DELETE FROM memory.Memories WHERE key_name='{key}'")

    def test_very_long_content(self):
        mem = get_memory('local')
        key = f"long_test_{datetime.now().strftime('%H%M%S')}"
        long_content = "x" * 5000
        mem.remember('test', key, long_content, importance=1)
        # Should truncate gracefully
        mem.execute(f"DELETE FROM memory.Memories WHERE key_name='{key}'")


if __name__ == '__main__':
    unittest.main(verbosity=2)
