from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "publication_preflight.py"
SPEC = importlib.util.spec_from_file_location("publication_preflight", MODULE_PATH)
assert SPEC and SPEC.loader
preflight = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = preflight
SPEC.loader.exec_module(preflight)


class ScanTests(unittest.TestCase):
    def rules_for(self, text: str) -> set[str]:
        return {finding.rule for finding in preflight.scan("fixture", text, [])}

    def test_clean_synthetic_text_passes(self) -> None:
        text = (
            "Agent A opened Project A from <workspace>/path.\n"
            "Contact user@example.com or visit https://example.invalid/report.\n"
            "The loopback service used 127.0.0.1."
        )
        self.assertEqual(preflight.scan("fixture", text, []), [])

    def test_private_identity_and_network_patterns(self) -> None:
        text = (
            "/" + "Users/alice/project\n"
            "/" + "home/bob/project\n"
            "C:\\" + "Users\\carol\\project\n"
            "person" + "@private.test\n"
            "192" + ".168.10.24\n"
            "chat_id=" + "123456789"
        )
        self.assertEqual(
            self.rules_for(text),
            {
                "macos-user-path",
                "linux-user-path",
                "windows-user-path",
                "email-address",
                "private-ipv4",
                "messaging-id",
            },
        )

    def test_secret_patterns(self) -> None:
        fixtures = {
            "github-token": "ghp_" + "A" * 24,
            "openai-style-key": "sk-" + "B" * 24,
            "anthropic-key": "sk-ant-" + "C" * 24,
            "aws-access-key": "AKIA" + "D" * 16,
            "google-api-key": "AIza" + "E" * 35,
            "slack-token": "xoxb-" + "F" * 24,
            "live-payment-key": "sk_live_" + "G" * 24,
            "bearer-token": "Authorization: Bearer " + "H" * 24,
            "jwt": "eyJ" + "I" * 10 + "." + "J" * 10 + "." + "K" * 10,
            "credential-assignment": "client_secret=" + "L" * 24,
            "sensitive-url-parameter": "https://example.invalid/cb?code=" + "M" * 24,
        }
        for expected_rule, text in fixtures.items():
            with self.subTest(expected_rule=expected_rule):
                self.assertIn(expected_rule, self.rules_for(text))

    def test_custom_deny_terms_are_case_insensitive(self) -> None:
        findings = preflight.scan("fixture", "Project Nightglass", ["nightglass"])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].category, "private-term")

    def test_deny_file_ignores_comments_and_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            deny_file = Path(directory) / "deny.txt"
            deny_file.write_text("# private terms\nAlpha\nalpha\n\nBeta\n", encoding="utf-8")
            args = preflight.parse_args(["--deny-file", str(deny_file), "-"])
            self.assertEqual(preflight.load_deny_terms(args), ["Alpha", "Beta"])


if __name__ == "__main__":
    unittest.main()
