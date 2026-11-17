#!/usr/bin/env python3
"""Owner authority comes only from explicit skill config, in both distributions."""

from contextlib import redirect_stderr
import io
import importlib.util
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parents[4]
MODULES = []
for directory in (SCRIPTS, ROOT / "container/openclaw/src/extensions/gitlab-agent/scripts"):
    for name in ("list-active-items.py", "list-directly-addressed-todos.py"):
        spec = importlib.util.spec_from_file_location(f"owner_{len(MODULES)}", directory / name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        MODULES.append(module)


def configuration(owner):
    return {"skills": {"entries": {"gitlab-agent": {"config": {"owner": owner}}}}}


class OwnerConfigurationTests(unittest.TestCase):
    def test_explicit_config_overrides_legacy_environment_and_profile(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "openclaw.json"
            path.write_text(json.dumps(configuration("  project-owner  ")))
            with patch.dict(os.environ, OPENCLAW_CONFIG_PATH=str(path), GITLAB_AGENT_OWNER="untrusted"):
                for module in MODULES:
                    with self.subTest(module=module.__file__):
                        self.assertEqual(module.configured_owner(), "project-owner")

    def test_default_path_is_the_openclaw_configuration(self):
        with TemporaryDirectory() as directory:
            home = Path(directory)
            path = home / ".openclaw/openclaw.json"
            path.parent.mkdir()
            path.write_text(json.dumps(configuration("configured-owner")))
            with patch.dict(os.environ, OPENCLAW_CONFIG_PATH=""), patch.object(Path, "home", return_value=home):
                for module in MODULES:
                    self.assertEqual(module.configured_owner(), "configured-owner")

    def test_missing_invalid_and_malformed_config_never_use_legacy_authority(self):
        invalid = ["not json", "[]", "{}", json.dumps({"skills": []}),
                   json.dumps({"skills": {"entries": []}}),
                   json.dumps({"skills": {"entries": {"gitlab-agent": []}}}),
                   json.dumps({"skills": {"entries": {"gitlab-agent": {"config": []}}}})]
        invalid += [json.dumps(configuration(value)) for value in
                    (None, True, 5, [], {}, "", " ", "@owner", "group/owner", "bad name")]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "openclaw.json"
            with patch.dict(os.environ, OPENCLAW_CONFIG_PATH=str(path), GITLAB_AGENT_OWNER="xrow"):
                for module in MODULES:
                    with self.subTest(module=module.__file__, missing=True):
                        with self.assertRaises(OSError):
                            module.configured_owner()
                for content in invalid:
                    path.write_text(content)
                    for module in MODULES:
                        with self.subTest(module=module.__file__, config=content):
                            with self.assertRaises(ValueError):
                                module.configured_owner()

    def test_discovery_and_todos_fail_before_api_calls_without_owner(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "openclaw.json"
            path.write_text("{}")
            with patch.dict(os.environ, OPENCLAW_CONFIG_PATH=str(path), GITLAB_AGENT_OWNER="xrow"):
                for module in MODULES:
                    with self.subTest(module=module.__file__), patch.object(module, "api_json") as api:
                        with redirect_stderr(io.StringIO()):
                            self.assertNotEqual(module.main(), 0)
                        api.assert_not_called()


if __name__ == "__main__":
    unittest.main()
