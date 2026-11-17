import unittest

from sluice.core import scan, redact, worst_severity


class TestScan(unittest.TestCase):
    def test_clean_text_no_findings(self):
        t = "We shipped slim today. 88.7% fewer characters. Have a look."
        self.assertEqual(scan(t), [])

    def test_line_numbers(self):
        t = "line one\nline two\nREDACTED-SECRET\n"
        f = scan(t)[0]
        self.assertEqual(f.line, 3)

    def test_min_severity_filters_low(self):
        t = "internal box at 10.0.0.1"
        self.assertEqual(scan(t), scan(t, min_severity="low"))
        self.assertEqual(scan(t, min_severity="medium"), [])

    def test_allow_suppresses(self):
        t = "REDACTED-SECRET"
        self.assertEqual(len(scan(t)), 1)
        self.assertEqual(scan(t, allow=["EXAMPLE"]), [])

    def test_overlap_resolved_to_higher_severity(self):
        # a JWT sitting in a token= assignment: report once, as the JWT
        t = "token=eyJhbGciOiJ.eyJzdWIiOiIxMjM0.SflKxwRJSMeK"
        f = scan(t)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0].detector, "jwt")

    def test_findings_sorted_by_position(self):
        t = "REDACTED-SECRET then ghp_" + "A1b2C3d4e5" * 4
        f = scan(t)
        self.assertEqual([x.start for x in f], sorted(x.start for x in f))


class TestPreview(unittest.TestCase):
    def test_preview_never_shows_full_secret(self):
        t = "REDACTED-SECRET"
        f = scan(t)[0]
        self.assertNotIn("abcDEF1234567890", f.preview)
        self.assertIn("…", f.preview)


class TestRedact(unittest.TestCase):
    def test_redacts_secret(self):
        t = "my key sk-ant-api03-" + "A1b2C3d4" * 6 + " end"
        out = redact(t)
        self.assertNotIn("sk-ant-api03", out)
        self.assertIn("[redacted:anthropic-key]", out)
        self.assertTrue(out.startswith("my key "))
        self.assertTrue(out.endswith(" end"))

    def test_redact_preserves_clean_text(self):
        t = "nothing to see here"
        self.assertEqual(redact(t), t)

    def test_redact_multiple(self):
        t = "a REDACTED-SECRET b REDACTED-SECRET c"
        out = redact(t)
        self.assertEqual(out, "a [redacted:gitlab-token] b [redacted:aws-access-key] c")

    def test_custom_template(self):
        t = "REDACTED-SECRET"
        self.assertEqual(redact(t, template="<{label}>"), "<aws-access-key>")


class TestWorstSeverity(unittest.TestCase):
    def test_none_when_empty(self):
        self.assertIsNone(worst_severity([]))

    def test_high_beats_low(self):
        t = "10.0.0.1 and REDACTED-SECRET"
        self.assertEqual(worst_severity(scan(t)), "high")


if __name__ == "__main__":
    unittest.main()
