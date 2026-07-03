import unittest

from slim.plugins import apply, select_filter, default_filter


class DefaultFilterTest(unittest.TestCase):
    def test_default_truncates_large_plain_output(self):
        raw = "".join(f"line{i}\n" for i in range(500))
        out = apply(raw)
        self.assertIn("elided by slim", out)
        self.assertLess(len(out.splitlines()), 120)

    def test_default_does_not_clamp_medium_output(self):
        raw = "".join(f"line{i}\n" for i in range(150))
        out = apply(raw)
        self.assertNotIn("elided", out)
        self.assertEqual(len(out.splitlines()), 150)

    def test_default_passes_small_output_through_slimmed(self):
        raw = "\x1b[31mhi\x1b[0m\n\n\n\nbye\n"
        self.assertEqual(apply(raw), "hi\n\nbye\n")


class KubectlDumpTest(unittest.TestCase):
    def test_large_yaml_dump_is_clamped_hard(self):
        raw = "".join(f"  field{i}: value{i}\n" for i in range(1000))
        out = apply(raw, command="kubectl get pods -o yaml")
        self.assertIn("elided by slim", out)
        self.assertLess(len(out.splitlines()), 60)


class DispatchTest(unittest.TestCase):
    def test_select_filter_unknown_command_returns_default(self):
        self.assertIs(select_filter("totallyunknown -x"), default_filter)

    def test_apply_uses_command_specific_plugin(self):
        raw = (
            "Collecting requests\n"
            "  Downloading requests-2.0.tar.gz (100 kB)\n"
            "     |################################| 100 kB 5.2 MB/s\n"
            "Installing collected packages: requests\n"
            "Successfully installed requests-2.0\n"
        )
        out = apply(raw, command="pip install requests")
        self.assertIn("Successfully installed requests-2.0", out)
        self.assertNotIn("MB/s", out)
        self.assertNotIn("Downloading", out)


if __name__ == "__main__":
    unittest.main()
