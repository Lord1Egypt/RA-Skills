#!/usr/bin/env python3
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sanitize_codex_session_prefix_replay.py"

spec = importlib.util.spec_from_file_location("codex_session_sanitizer", SCRIPT)
sanitizer = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sanitizer
spec.loader.exec_module(sanitizer)


class CodexSessionSanitizerTests(unittest.TestCase):
    def test_sanitizes_response_item_prefix_storm(self):
        storm = " ".join("[ollama-2/glm-5.2]" for _ in range(1000)) + " [olama"
        obj = {
            "type": "response_item",
            "payload": {"content": [{"type": "output_text", "text": storm}]},
        }

        self.assertEqual(1, sanitizer.sanitize_event(obj))

        self.assertEqual("", obj["payload"]["content"][0]["text"])

    def test_sanitizes_prefix_only_partial_tail(self):
        obj = {
            "type": "response_item",
            "payload": {"content": [{"type": "output_text", "text": "[ollama-2/glm"}]},
        }

        self.assertEqual(1, sanitizer.sanitize_event(obj))

        self.assertEqual("", obj["payload"]["content"][0]["text"])

    def test_sanitizes_prefixes_before_visible_text(self):
        text = " ".join("[ollama-2/glm-5.2]" for _ in range(21)) + " The goal is already complete. No further action needed."
        obj = {
            "type": "response_item",
            "payload": {"content": [{"type": "output_text", "text": text}]},
        }

        self.assertEqual(1, sanitizer.sanitize_event(obj))

        self.assertEqual(
            "The goal is already complete. No further action needed.",
            obj["payload"]["content"][0]["text"],
        )

    def test_sanitizes_event_message_mirrors(self):
        text = "[ollama-2/kimi-k2.5] [tool calls omitted]"
        obj = {
            "type": "event_msg",
            "payload": {"message": text, "last_agent_message": text},
        }

        self.assertEqual(2, sanitizer.sanitize_event(obj))

        self.assertEqual("", obj["payload"]["message"])
        self.assertEqual("", obj["payload"]["last_agent_message"])

    def test_does_not_rewrite_user_messages(self):
        obj = {
            "type": "user_message",
            "payload": {"text": "Bug report: [tool calls omitted] should stay literal here."},
        }

        self.assertEqual(0, sanitizer.sanitize_event(obj))
        self.assertEqual("Bug report: [tool calls omitted] should stay literal here.", obj["payload"]["text"])

    def test_file_repair_creates_backup_only_when_changed(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "session.jsonl"
            path.write_text(
                json.dumps({
                    "type": "response_item",
                    "payload": {"content": [{"type": "output_text", "text": "[ollama-2/glm-5.2] final"}]},
                })
                + "\n"
            )

            result = sanitizer.sanitize_file(path, in_place=True)

            self.assertEqual(1, result["changedFields"])
            self.assertEqual(1, result["changedLines"])
            self.assertTrue(Path(result["backup"]).exists())
            repaired = json.loads(path.read_text())
            self.assertEqual("final", repaired["payload"]["content"][0]["text"])


if __name__ == "__main__":
    unittest.main()
