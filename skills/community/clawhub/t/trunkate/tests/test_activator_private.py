import unittest
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from activator import _filter_sensitive_content, _restore_sensitive_content


class TestFilterSensitiveContent(unittest.TestCase):
    """Tests for _filter_sensitive_content() in activator.py."""

    def test_private_tags_extracted(self):
        text = "Hello [PRIVATE]secret data[/PRIVATE] world"
        filtered, protected = _filter_sensitive_content(text)
        self.assertNotIn("secret data", filtered)
        self.assertIn("__PRIVATE_", filtered)
        self.assertTrue(any("[PRIVATE]secret data[/PRIVATE]" in v for v in protected.values()))

    def test_keep_tags_extracted(self):
        text = "Hello [KEEP]important[/KEEP] world"
        filtered, protected = _filter_sensitive_content(text)
        self.assertNotIn("[KEEP]important[/KEEP]", filtered)
        self.assertIn("__PRIVATE_", filtered)

    def test_system_tags_extracted(self):
        text = "Hello <system>system prompt</system> world"
        filtered, protected = _filter_sensitive_content(text)
        self.assertNotIn("<system>system prompt</system>", filtered)
        self.assertIn("__PRIVATE_", filtered)

    def test_indexed_placeholders(self):
        """Placeholders should use __PRIVATE_N__ format (not UUID)."""
        text = "[PRIVATE]a[/PRIVATE] [KEEP]b[/KEEP]"
        filtered, protected = _filter_sensitive_content(text)
        self.assertIn("__PRIVATE_0__", filtered)
        self.assertIn("__PRIVATE_1__", filtered)
        self.assertNotIn("__TRUNKATE_PROTECTED_", filtered)

    def test_multiple_private_tags(self):
        text = "[PRIVATE]first[/PRIVATE] and [PRIVATE]second[/PRIVATE]"
        filtered, protected = _filter_sensitive_content(text)
        self.assertNotIn("first", filtered)
        self.assertNotIn("second", filtered)
        self.assertEqual(len(protected), 2)

    def test_no_sensitive_content(self):
        text = "Just a normal sentence with no tags."
        filtered, protected = _filter_sensitive_content(text)
        # May still detect "secrets" via regex, but no tags should mean minimal changes
        self.assertIn("Just a normal sentence", filtered)


class TestRestoreSensitiveContent(unittest.TestCase):
    """Tests for _restore_sensitive_content() in activator.py."""

    def test_roundtrip(self):
        """Filter -> restore should recover original content."""
        original = "Hello [PRIVATE]secret[/PRIVATE] and [KEEP]kept[/KEEP] world"
        filtered, protected = _filter_sensitive_content(original)
        restored = _restore_sensitive_content(filtered, protected)
        self.assertIn("[PRIVATE]secret[/PRIVATE]", restored)
        self.assertIn("[KEEP]kept[/KEEP]", restored)

    def test_restore_preserves_positions(self):
        original = "Start [PRIVATE]data[/PRIVATE] middle [PRIVATE]more[/PRIVATE] end"
        filtered, protected = _filter_sensitive_content(original)
        restored = _restore_sensitive_content(filtered, protected)
        self.assertEqual(restored, original)


if __name__ == '__main__':
    unittest.main()
