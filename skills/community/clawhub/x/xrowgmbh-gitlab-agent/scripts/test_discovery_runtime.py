"""Fresh API responses and deferred discovery-only libraries."""

from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("list-active-items.py")


def load():
    spec = importlib.util.spec_from_file_location("discovery_runtime", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DiscoveryRuntimeTests(unittest.TestCase):
    def test_repeated_metadata_and_enumeration_reads_always_contact_gitlab(self):
        active = load()
        for endpoint, payloads in (
            ("projects/1", [{"id": 1, "archived": False}, {"id": 1, "archived": True}]),
            ("projects?membership=true&simple=true&per_page=100&page=1", [[{"id": 1}], [{"id": 2}]]),
        ):
            with self.subTest(endpoint=endpoint), patch.object(
                active.subprocess, "run", side_effect=[
                    subprocess.CompletedProcess([], 0, stdout=json.dumps(value)) for value in payloads
                ],
            ) as run:
                self.assertEqual([active.api_json(endpoint), active.api_json(endpoint)], payloads)
                self.assertEqual(run.call_count, 2)
                self.assertTrue(all(call.args[0] == ["glab", "api", endpoint] for call in run.call_args_list))

    def test_discovery_ignores_legacy_cache_without_creating_or_changing_files(self):
        active = load()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            legacy = root / "gitlab-agent/requests-v1/old-user/project.json"
            legacy.parent.mkdir(parents=True)
            legacy.write_text('{"payload":{"archived":true}}')
            before = {p.relative_to(root): (p.is_dir(), None if p.is_dir() else p.read_bytes()) for p in root.rglob("*")}
            with patch.dict(os.environ, {"XDG_CACHE_HOME": directory, "GITLAB_AGENT_REQUEST_CACHE": "1"}), \
                    patch.object(active.shutil, "which", return_value="glab"), \
                    patch.object(active, "api_json", return_value={"id": 7, "username": "robot", "web_url": "https://gitlab.example/robot"}), \
                    patch.object(active, "configured_owner", return_value="robot"), \
                    patch.object(active, "unassigned_incidents", return_value=[]), \
                    patch.object(active, "assign_unassigned_items", return_value=[]), \
                    patch.object(active, "paginated", return_value=[]), \
                    redirect_stdout(io.StringIO()) as output:
                self.assertEqual(active.main(), 0)
            self.assertEqual(json.loads(output.getvalue()), [])
            after = {p.relative_to(root): (p.is_dir(), None if p.is_dir() else p.read_bytes()) for p in root.rglob("*")}
            self.assertEqual(before, after)

    def test_optional_libraries_are_not_imported_on_load_or_serial_path(self):
        program = '''
import builtins, importlib.util, sys
original = builtins.__import__
blocked = {"fcntl", "tempfile", "time", "concurrent.futures", "datetime", "pathlib", "urllib.parse"}
def guarded(name, globals=None, *args, **kwargs):
    if globals and globals.get("__name__") == "discovery_runtime" and name in blocked:
        raise AssertionError("Eager discovery import: " + name)
    return original(name, globals, *args, **kwargs)
builtins.__import__ = guarded
spec = importlib.util.spec_from_file_location("discovery_runtime", sys.argv[1])
active = importlib.util.module_from_spec(spec)
spec.loader.exec_module(active)
assert active.parallel_reads(lambda x: x + 1, [1]) == [2]
active.configured_accept_entries = lambda: []
assert active.assign_unassigned_items(7, "robot", "robot", {}) == []
'''
        subprocess.run([sys.executable, "-S", "-c", program, str(SCRIPT)], check=True, capture_output=True, text=True)


if __name__ == "__main__":
    unittest.main()
