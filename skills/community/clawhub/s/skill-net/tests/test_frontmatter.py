#!/usr/bin/env python3
"""
Tests for analyze_deps.py frontmatter parsing.

BUG FIXED (2026-05-15):
- Original code: parts = content[3:].split("---", 2)
  This stripped the first 3 chars before splitting, causing body to always be empty
  when frontmatter exists, because the split point was consumed by the slice.
- Fixed code: parts = content.split("---", 2)
  Now correctly splits on both frontmatter delimiters.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import analyze_deps


class TestFrontmatterParsing(unittest.TestCase):
    def test_body_with_use_when_in_body(self):
        """Use when phrase in body should be detected (was broken before fix)."""
        content = """---
name: example-skill
description: "A skill"
---
# Example Skill

Use when: user asks about something specific

Some body content here.
"""
        frontmatter, body = analyze_deps.parse_frontmatter(content)
        self.assertEqual(frontmatter.get("name"), "example-skill")
        self.assertIn("Use when", body)
        self.assertIn("Some body content here.", body)

    def test_body_with_use_when_multiline(self):
        """Multi-line body with Use when in middle."""
        content = """---
name: test
---
# Title

Use when: user says trigger phrase
And also when they say this

## Section
More content.
"""
        _, body = analyze_deps.parse_frontmatter(content)
        self.assertIn("Use when", body)
        self.assertIn("## Section", body)

    def test_no_frontmatter(self):
        """Content without frontmatter should return full content as body."""
        content = "# No Frontmatter\n\nSome text without YAML delimiters."
        _, body = analyze_deps.parse_frontmatter(content)
        self.assertEqual(body, content)

    def test_empty_frontmatter_single_delimiter(self):
        """Single --- without closing delimiter."""
        content = """---
name: single-delimiter
---
# Body
Use when: this is in body
"""
        _, body = analyze_deps.parse_frontmatter(content)
        self.assertIn("Use when", body)

    def test_complex_yaml_value(self):
        """Description with multi-line YAML literal block."""
        content = """---
name: complex
description: >
  This is a multi-line
  description value
---
# Body
Use when: trigger here
"""
        fm, body = analyze_deps.parse_frontmatter(content)
        self.assertEqual(fm.get("name"), "complex")
        self.assertIn("Use when", body)

    def test_frontmatter_with_inline_use_when(self):
        """Use when phrase on same line as frontmatter field."""
        content = """---
name: inline-test
description: "Use when: inline description"
---
# Body
More content.
"""
        fm, body = analyze_deps.parse_frontmatter(content)
        self.assertEqual(fm.get("description"), '"Use when: inline description"')
        self.assertEqual(body.strip(), "# Body\nMore content.")

    def test_frontmatter_key_value_pairs(self):
        """Multiple key-value pairs in frontmatter are parsed correctly."""
        content = """---
name: multi-field
version: 1.0.0
description: Test skill
author: test
---
# Body content
"""
        fm, body = analyze_deps.parse_frontmatter(content)
        self.assertEqual(fm.get("name"), "multi-field")
        self.assertEqual(fm.get("version"), "1.0.0")
        self.assertEqual(fm.get("description"), "Test skill")
        self.assertEqual(fm.get("author"), "test")


if __name__ == "__main__":
    unittest.main(verbosity=2)