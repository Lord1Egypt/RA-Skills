#!/usr/bin/env python3
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROXY_PATH = ROOT / "scripts" / "codex_sage_router_proxy.py"

spec = importlib.util.spec_from_file_location("codex_sage_router_proxy", PROXY_PATH)
codex_proxy = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = codex_proxy
spec.loader.exec_module(codex_proxy)


class CodexSageRouterProxyTests(unittest.TestCase):

    def test_sanitizes_replayed_prefix_noise(self):
        raw = (
            "[ollama-2/kimi-k2.5] [tool calls omitted]\n"
            "[ollama-2/kimi-k2.5] [ollama-2/kimi-k2.5] [tool calls omitted]"
        )

        self.assertEqual("", codex_proxy.sanitize_visible_output(raw))

    def test_sanitizes_large_replayed_prefix_storms(self):
        raw = " ".join("[ollama-2/kimi-k2.5] [tool calls omitted]" for _ in range(1000))

        self.assertEqual("", codex_proxy.sanitize_visible_output(raw))

    def test_sanitizes_prefix_only_storms(self):
        raw = " ".join("[ollama-2/kimi-k2.5]" for _ in range(1000))

        self.assertEqual("", codex_proxy.sanitize_visible_output(raw))

    def test_sanitizes_truncated_prefix_storm_tail(self):
        raw = " ".join("[ollama-2/glm-5.2]" for _ in range(1000)) + " [olama"

        self.assertEqual("", codex_proxy.sanitize_visible_output(raw))

    def test_sanitizes_prefix_only_partial_tail(self):
        self.assertEqual("", codex_proxy.sanitize_visible_output("[ollama-2/glm"))

    def test_sanitizes_newline_split_prefix_placeholder_noise(self):
        raw = (
            "[ollama-2/kimi-k2.5]\n"
            "[tool calls omitted]\n"
            "[ollama-2/kimi-k2.5]\n"
            "[ollama-2/kimi-k2.5] [tool calls omitted]"
        )

        self.assertEqual("", codex_proxy.sanitize_visible_output(raw))

    def test_preserves_visible_text_before_replayed_prefix_storm(self):
        raw = "Done.\n" + "\n".join(
            "[ollama-2/kimi-k2.5] [tool calls omitted]" for _ in range(1000)
        )

        self.assertEqual("Done.", codex_proxy.sanitize_visible_output(raw))

    def test_response_request_preserves_function_calls_and_tool_outputs(self):
        messages = codex_proxy.messages_from_response_request({
            "input": [
                {
                    "type": "function_call",
                    "call_id": "call_1",
                    "name": "lookup_record",
                    "arguments": {"id": "abc"},
                },
                {
                    "type": "function_call_output",
                    "call_id": "call_1",
                    "output": "record",
                },
                {
                    "type": "message",
                    "role": "user",
                    "content": [{"type": "input_text", "text": "continue"}],
                },
            ],
        })

        self.assertEqual("assistant", messages[0]["role"])
        self.assertEqual("call_1", messages[0]["tool_calls"][0]["id"])
        self.assertEqual('{"id":"abc"}', messages[0]["tool_calls"][0]["function"]["arguments"])
        self.assertEqual("tool", messages[1]["role"])
        self.assertEqual("call_1", messages[1]["tool_call_id"])
        self.assertEqual({"role": "user", "content": "continue"}, messages[2])

    def test_response_request_drops_orphan_tool_outputs(self):
        messages = codex_proxy.messages_from_response_request({
            "input": [
                {"type": "function_call_output", "call_id": "", "output": "orphan"},
                {"type": "function_call_output", "output": "orphan"},
                {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "continue"}]},
            ],
        })

        self.assertEqual([{"role": "user", "content": "continue"}], messages)


if __name__ == "__main__":
    unittest.main()
