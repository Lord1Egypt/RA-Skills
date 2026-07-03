import unittest

from slim.report import measure


class MeasureTest(unittest.TestCase):
    def test_reports_char_and_line_savings(self):
        before = "a\n" * 100  # 200 chars, 100 lines
        after = "a\n" * 10  # 20 chars, 10 lines
        m = measure(before, after)
        self.assertEqual(m["chars_before"], 200)
        self.assertEqual(m["chars_after"], 20)
        self.assertEqual(m["lines_before"], 100)
        self.assertEqual(m["lines_after"], 10)
        self.assertEqual(m["pct_chars_saved"], 90.0)

    def test_zero_length_input_is_safe(self):
        m = measure("", "")
        self.assertEqual(m["pct_chars_saved"], 0.0)


if __name__ == "__main__":
    unittest.main()
