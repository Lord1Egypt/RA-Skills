#!/usr/bin/env python3
"""{{skill_name}} 测试：{{summary}}"""
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLI = HERE / "{{cli_module}}.py"
sys.path.insert(0, str(HERE))
import {{cli_module}} as mod  # noqa: E402


def run_cli(*argv):
    r = subprocess.run([sys.executable, str(CLI)] + list(argv),
                       capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", errors="replace")


class TestCli(unittest.TestCase):
    def test_version(self):
        code, out = run_cli("--version")
        self.assertEqual(code, 0)
        self.assertIn("{{skill_name}}", out)

    def test_hello(self):
        code, out = run_cli("hello", "--name", "测试")
        self.assertEqual(code, 0)
        self.assertIn("测试", out)

    def test_main_returns_int(self):
        self.assertIsInstance(mod.main([]), int)


if __name__ == "__main__":
    unittest.main()