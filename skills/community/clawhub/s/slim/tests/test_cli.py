import unittest

from slim.cli import main


class StdinModeTest(unittest.TestCase):
    def test_filters_stdin_with_command_hint(self):
        raw = (
            "Collecting x\n"
            "  Downloading x-1.0.tar.gz (1 kB)\n"
            "     |####| 1 kB 5.2 MB/s\n"
            "Successfully installed x-1.0\n"
        )
        out, err, code = main(["--cmd", "pip install x"], stdin_text=raw)
        self.assertEqual(code, 0)
        self.assertIn("Successfully installed x-1.0", out)
        self.assertNotIn("MB/s", out)

    def test_report_flag_writes_savings_to_stderr_not_stdout(self):
        raw = "\x1b[31mhi\x1b[0m\n\n\n\nbye\n"
        out, err, code = main(["--report"], stdin_text=raw)
        self.assertEqual(out, "hi\n\nbye\n")
        self.assertIn("saved", err)


class ExecModeTest(unittest.TestCase):
    def test_runs_command_and_filters_its_output(self):
        out, err, code = main(["--", "printf", "a\n\n\n\nb\n"], stdin_text="")
        self.assertEqual(out, "a\n\nb\n")
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
