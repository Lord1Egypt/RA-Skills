import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "transweb_ai.py"


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
    )


class CliTests(unittest.TestCase):
    def test_help(self):
        result = run("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("selftest", result.stdout)
        self.assertNotIn("agent", result.stdout)

    def test_selftest_json(self):
        result = run("selftest", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["skill"], "transweb-ai")

    def test_version(self):
        result = run("--version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1.2.3", result.stdout)

    def test_help_lists_demo(self):
        result = run("--help")
        self.assertIn("demo", result.stdout)
        self.assertIn("selftest", result.stdout)

    def test_demo_json_offline(self):
        result = run("demo", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertTrue(payload["sample"])
        self.assertFalse(payload["created"])
        self.assertFalse(payload["network"])
        self.assertEqual(len(payload["preview"]["workflow"]), 3)

    def test_demo_subcommands_offline(self):
        for kind in ("list", "run", "ppt"):
            with self.subTest(kind=kind):
                result = run("demo", kind, "--json")
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["command"], kind)
                self.assertTrue(payload["sample"])

    def test_list_dry_run_offline(self):
        result = run("list", "--dry-run", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["command"], "list")
        self.assertTrue(payload["sample"])
        self.assertGreaterEqual(len(payload["apps"]), 1)

    def test_ppt_dry_run_offline(self):
        result = run("ppt", "--input", "做一份季度汇报 PPT", "--dry-run", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["command"], "ppt")
        self.assertGreaterEqual(len(payload["preview"]["slideOutline"]), 5)
        self.assertIsNone(payload["preview"]["link"])

    def test_run_dry_run_offline(self):
        result = run("run", "--ids", "11111111111111111111111111111111",
                     "--input", "先写大纲", "--dry-run", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["command"], "run")
        self.assertTrue(payload["sample"])

    def test_selftest_checks_offline_preview(self):
        result = run("selftest", "--json")
        payload = json.loads(result.stdout)
        names = {c["name"] for c in payload["checks"]}
        self.assertIn("offline-preview", names)
        self.assertIn("version-match", names)
        self.assertIn("frontmatter:author", names)


if __name__ == "__main__":
    unittest.main()
