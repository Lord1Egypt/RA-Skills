#!/usr/bin/env python3
"""Focused tests for owner-addressed to-do discovery."""

from __future__ import annotations

import importlib.util
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


script = Path(__file__).with_name("list-directly-addressed-todos.py")
spec = importlib.util.spec_from_file_location("list_directly_addressed_todos", script)
assert spec and spec.loader
todos = importlib.util.module_from_spec(spec)
spec.loader.exec_module(todos)


def todo(item_id=1, *, author_id=44745, author="xrow", action="directly_addressed", state="pending"):
    return {"id": item_id, "author": {"id": author_id, "username": author},
            "action_name": action, "state": state, "body": "@agent Please inspect this."}


class DirectlyAddressedTests(unittest.TestCase):
    def test_owner_lookup_requires_one_exact_user(self):
        with patch.object(todos, "api_json", return_value=[{"id": 44745, "username": "xrow"}]):
            self.assertEqual(todos.owner_identity("xrow"), (44745, "xrow"))
        with patch.object(todos, "api_json", return_value=[{"id": 1, "username": "xrow-helper"}]):
            with self.assertRaises(ValueError):
                todos.owner_identity("xrow")

    def test_filters_every_page_by_owner_action_and_pending_state(self):
        first = [todo(item_id=index) for index in range(1, 101)]
        second = [todo(101), todo(102, author="other"),
                  todo(103, author_id=2), todo(104, action="mentioned"),
                  todo(105, state="done")]
        with patch.object(todos, "api_json", side_effect=[first, second]) as api:
            result = todos.pending_owner_todos(44745, "xrow")
        self.assertEqual(len(result), 101)
        self.assertEqual(result[-1]["id"], 101)
        self.assertIn("page=2", api.call_args.args[0])
        self.assertIn("author_id=44745", api.call_args.args[0])

    def test_main_emits_json_without_mutating_todos(self):
        with patch.object(todos, "configured_owner", return_value="xrow"), patch.object(
            todos, "owner_identity", return_value=(44745, "xrow")
        ), patch.object(todos, "pending_owner_todos", return_value=[todo()]), redirect_stdout(io.StringIO()) as output:
            self.assertEqual(todos.main(), 0)
        self.assertEqual(json.loads(output.getvalue())[0]["id"], 1)


if __name__ == "__main__":
    unittest.main()
