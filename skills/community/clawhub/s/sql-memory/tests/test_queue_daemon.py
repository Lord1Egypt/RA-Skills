#!/usr/bin/env python3
"""
test_queue_daemon.py — Unit tests for queue daemon routing and task processing
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'infrastructure'))


class TestAgentRegistry(unittest.TestCase):
    """Test that agent registry is properly configured."""

    def test_registry_has_entries(self):
        from queue_daemon import AGENT_REGISTRY
        self.assertGreater(len(AGENT_REGISTRY), 5)

    def test_registry_values_are_tuples(self):
        from queue_daemon import AGENT_REGISTRY
        for name, val in AGENT_REGISTRY.items():
            self.assertIsInstance(val, tuple, f"{name} should map to (module, class) tuple")
            self.assertEqual(len(val), 2, f"{name} tuple should have 2 elements")


class TestStubAgent(unittest.TestCase):
    """Test the fallback stub agent."""

    def test_stub_handles_any_task(self):
        from queue_daemon import _get_stub_agent
        stub = _get_stub_agent()
        result = stub.run_task({
            'id': '999', 'agent': 'unknown', 'task_type': 'unknown_type'
        })
        self.assertIn('Stub', result)

    def test_stub_singleton(self):
        from queue_daemon import _get_stub_agent
        a = _get_stub_agent()
        b = _get_stub_agent()
        self.assertIs(a, b)


class TestResolveAgent(unittest.TestCase):
    """Test agent resolution logic."""

    def test_resolve_registered_agent(self):
        from queue_daemon import resolve_agent_for_task
        agent = resolve_agent_for_task('dispatcher', 'github_setup')
        self.assertIsNotNone(agent)

    def test_resolve_unknown_agent_returns_stub(self):
        from queue_daemon import resolve_agent_for_task, _StubAgent
        agent = resolve_agent_for_task('totally_fake_agent', 'fake_task')
        self.assertIsInstance(agent, _StubAgent)


class TestFetchParsing(unittest.TestCase):
    """Test that fetch_next_task returns proper structure."""

    def test_fetch_returns_none_or_dict(self):
        from sql_memory import get_memory
        from queue_daemon import fetch_next_task
        mem = get_memory('local')
        result = fetch_next_task(mem)
        self.assertTrue(result is None or isinstance(result, dict))


if __name__ == '__main__':
    unittest.main(verbosity=2)
