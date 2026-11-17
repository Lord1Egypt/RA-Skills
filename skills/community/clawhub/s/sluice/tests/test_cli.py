import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from sluice.cli import main


def run(argv, stdin=""):
    out, err = io.StringIO(), io.StringIO()
    import sys
    old = sys.stdin
    sys.stdin = io.StringIO(stdin)
    try:
        with redirect_stdout(out), redirect_stderr(err):
            code = main(argv)
    finally:
        sys.stdin = old
    return code, out.getvalue(), err.getvalue()


class TestCli(unittest.TestCase):
    def test_scan_clean_exit_zero(self):
        code, _, err = run(["scan"], stdin="all good here")
        self.assertEqual(code, 0)
        self.assertIn("clean", err)

    def test_scan_high_finding_exits_one(self):
        code, _, err = run(["scan"], stdin="REDACTED-SECRET")
        self.assertEqual(code, 1)
        self.assertIn("gitlab_pat", err)

    def test_fail_on_never_exits_zero(self):
        code, _, _ = run(
            ["scan", "--fail-on", "never"], stdin="REDACTED-SECRET"
        )
        self.assertEqual(code, 0)

    def test_low_finding_does_not_fail_by_default(self):
        # private IP is low severity; default fail-on is high
        code, _, _ = run(["scan"], stdin="box at 10.0.0.1")
        self.assertEqual(code, 0)

    def test_redact_mode_writes_clean_stdout(self):
        code, out, _ = run(["redact"], stdin="x REDACTED-SECRET y")
        self.assertEqual(code, 0)
        self.assertEqual(out, "x [redacted:aws-access-key] y")

    def test_json_output(self):
        code, _, err = run(
            ["scan", "--json"], stdin="REDACTED-SECRET"
        )
        self.assertIn('"detector": "gitlab_pat"', err)

    def test_allow_flag(self):
        code, _, _ = run(
            ["scan", "--allow", "EXAMPLE"], stdin="REDACTED-SECRET"
        )
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
