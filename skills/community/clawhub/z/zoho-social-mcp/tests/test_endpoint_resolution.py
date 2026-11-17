"""Credential-free tests for shared multi-account MCP endpoint resolution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from mcp_endpoint import (  # noqa: E402
    EndpointResolutionError,
    add_endpoint_arguments,
    resolve_mcp_url,
)


def parse(*arguments):
    parser = add_endpoint_arguments(argparse.ArgumentParser())
    return parser.parse_args(list(arguments))


class EndpointResolutionTests(unittest.TestCase):
    def test_direct_url_argument_wins(self):
        args = parse("--mcp-url", "https://direct.example.org/mcp/1/message")
        resolved = resolve_mcp_url(
            args,
            service="social",
            env_vars=("ZOHO_SOCIAL_MCP_URL",),
            environ={"ZOHO_SOCIAL_MCP_URL": "https://env.example.org/mcp/env/message"},
        )
        self.assertEqual(resolved, "https://direct.example.org/mcp/1/message")

    def test_profile_resolution_from_profiles_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            profiles_path = Path(temp_dir) / "profiles.json"
            profiles_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "profiles": {
                            "kunde-a": {
                                "services": {
                                    "social": {
                                        "url": "https://social-a.example.org/mcp/token-a/message"
                                    }
                                }
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            args = parse("--profile", "kunde-a", "--profiles-file", str(profiles_path))
            resolved = resolve_mcp_url(
                args,
                service="social",
                env_vars=("ZOHO_SOCIAL_MCP_URL",),
                environ={},
            )
            self.assertEqual(resolved, "https://social-a.example.org/mcp/token-a/message")

    def test_profile_indirection_to_env_var(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            profiles_path = Path(temp_dir) / "profiles.json"
            profiles_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "profiles": {
                            "kunde-b": {
                                "services": {"social": {"env": "KUNDE_B_SOCIAL_URL"}}
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            args = parse("--profile", "kunde-b", "--profiles-file", str(profiles_path))
            resolved = resolve_mcp_url(
                args,
                service="social",
                env_vars=("ZOHO_SOCIAL_MCP_URL",),
                environ={"KUNDE_B_SOCIAL_URL": "https://social-b.example.org/mcp/token-b/message"},
            )
            self.assertEqual(resolved, "https://social-b.example.org/mcp/token-b/message")

    def test_single_org_fallback_environment_variable(self):
        args = parse()
        resolved = resolve_mcp_url(
            args,
            service="social",
            env_vars=("ZOHO_SOCIAL_MCP_URL",),
            environ={"ZOHO_SOCIAL_MCP_URL": "https://fallback.example.org/mcp/fallback/message"},
        )
        self.assertEqual(resolved, "https://fallback.example.org/mcp/fallback/message")

    def test_missing_endpoint_raises_helpful_error(self):
        args = parse()
        with self.assertRaises(EndpointResolutionError) as ctx:
            resolve_mcp_url(
                args,
                service="social",
                env_vars=("ZOHO_SOCIAL_MCP_URL",),
                environ={},
            )
        self.assertIn("no Zoho Social MCP endpoint configured", str(ctx.exception))

    def test_rejects_whitespace_in_url(self):
        args = parse("--mcp-url", "https://bad.example.org/mcp/ token /message")
        with self.assertRaises(EndpointResolutionError):
            resolve_mcp_url(
                args,
                service="social",
                env_vars=("ZOHO_SOCIAL_MCP_URL",),
                environ={},
            )


if __name__ == "__main__":
    unittest.main()
