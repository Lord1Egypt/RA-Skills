#!/usr/bin/env python3
import json
import unittest
import importlib.util
from pathlib import Path

PARSER_PATH = Path(__file__).with_name("poll-parser.py")
spec = importlib.util.spec_from_file_location("poll_parser", PARSER_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class PollParserTests(unittest.TestCase):
    def test_workspace_scoped_pending(self):
        pending = {
            "workspace": {"_id": "w1", "repoUrl": "https://github.com/a/b"},
            "tasks": [{"_id": "t1", "title": "x"}],
        }
        env = mod.build_envelope(json.dumps(pending), '{"tasks":[]}', '{"tasks":[]}', now_ms=1_800_000_000_000)
        self.assertEqual(env["counts"]["pending"], 1)

    def test_review_filters_picked_up(self):
        review = {
            "tasks": [
                {"_id": "r1", "deliverables": [{"type": "pr"}]},
                {"_id": "r2", "deliverables": [{"type": "pr"}], "pickedUpAt": 123},
            ]
        }
        env = mod.build_envelope('{"tasks":[]}', json.dumps(review), '{"tasks":[]}', now_ms=1_800_000_000_000)
        self.assertEqual(env["counts"]["review"], 1)
        self.assertEqual(env["review"]["tasks"][0]["_id"], "r1")

    def test_stuck_needs_old_started_at_and_no_recent_activity(self):
        now = 1_800_000_000_000
        working = {
            "tasks": [
                {"_id": "s1", "deliverables": [{"type": "pr"}], "startedAt": now - (31 * 60 * 1000)},
                {"_id": "s2", "deliverables": [{"type": "pr"}], "startedAt": now - (31 * 60 * 1000), "updatedAt": now - (5 * 60 * 1000)},
            ]
        }
        env = mod.build_envelope('{"tasks":[]}', '{"tasks":[]}', json.dumps(working), now_ms=now)
        self.assertEqual(env["counts"]["stuck"], 1)
        self.assertEqual(env["stuck"]["tasks"][0]["_id"], "s1")


if __name__ == "__main__":
    unittest.main()
