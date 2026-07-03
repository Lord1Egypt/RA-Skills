import unittest

from slim.core import slim_text, truncate_middle


class CollapseBlankLinesTest(unittest.TestCase):
    def test_collapses_runs_of_blank_lines_to_one(self):
        raw = "a\n\n\n\n\nb\n"
        self.assertEqual(slim_text(raw), "a\n\nb\n")


class StripAnsiTest(unittest.TestCase):
    def test_removes_ansi_colour_codes(self):
        raw = "\x1b[31mERROR\x1b[0m: boom\n"
        self.assertEqual(slim_text(raw), "ERROR: boom\n")


class TrailingWhitespaceTest(unittest.TestCase):
    def test_strips_trailing_whitespace_per_line(self):
        raw = "hello   \nworld\t\n"
        self.assertEqual(slim_text(raw), "hello\nworld\n")


class DedupeConsecutiveTest(unittest.TestCase):
    def test_collapses_repeated_identical_lines_with_count(self):
        raw = "downloading\n" * 5 + "done\n"
        self.assertEqual(slim_text(raw), "downloading\n  ... (repeated 5x)\ndone\n")

    def test_two_identical_lines_are_not_collapsed(self):
        raw = "a\na\nb\n"
        self.assertEqual(slim_text(raw), "a\na\nb\n")


class TruncateMiddleTest(unittest.TestCase):
    def test_keeps_head_and_tail_and_marks_elision(self):
        raw = "".join(f"line{i}\n" for i in range(100))
        out = truncate_middle(raw, head=3, tail=2)
        self.assertEqual(
            out,
            "line0\nline1\nline2\n"
            "  ... (95 lines elided by slim) ...\n"
            "line98\nline99\n",
        )

    def test_short_text_is_unchanged(self):
        raw = "a\nb\nc\n"
        self.assertEqual(truncate_middle(raw, head=3, tail=2), raw)


if __name__ == "__main__":
    unittest.main()
