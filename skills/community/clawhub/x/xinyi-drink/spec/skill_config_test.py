from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import skill_config


class SkillConfigTest(unittest.TestCase):
    def test_load_config_allows_environment_overrides(self) -> None:
        previous_base_url = os.environ.get("XINYI_API_BASE_URL")
        previous_timeout = os.environ.get("XINYI_TIMEOUT_SECONDS")
        os.environ["XINYI_API_BASE_URL"] = "http://127.0.0.1:8020"
        os.environ["XINYI_TIMEOUT_SECONDS"] = "3"
        try:
            config = skill_config.load_config()
        finally:
            if previous_base_url is None:
                os.environ.pop("XINYI_API_BASE_URL", None)
            else:
                os.environ["XINYI_API_BASE_URL"] = previous_base_url

            if previous_timeout is None:
                os.environ.pop("XINYI_TIMEOUT_SECONDS", None)
            else:
                os.environ["XINYI_TIMEOUT_SECONDS"] = previous_timeout

        self.assertEqual(config["apiBaseUrl"], "http://127.0.0.1:8020")
        self.assertEqual(config["timeoutSeconds"], 3)

    def test_load_config_clamps_timeout_override_to_positive_seconds(self) -> None:
        previous_timeout = os.environ.get("XINYI_TIMEOUT_SECONDS")
        os.environ["XINYI_TIMEOUT_SECONDS"] = "0"
        try:
            config = skill_config.load_config()
        finally:
            if previous_timeout is None:
                os.environ.pop("XINYI_TIMEOUT_SECONDS", None)
            else:
                os.environ["XINYI_TIMEOUT_SECONDS"] = previous_timeout

        self.assertEqual(config["timeoutSeconds"], 1)


if __name__ == "__main__":
    unittest.main()
