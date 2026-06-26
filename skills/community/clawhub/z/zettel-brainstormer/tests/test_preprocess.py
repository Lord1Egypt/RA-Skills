import unittest
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from obsidian_utils import extract_tags
from find_links import find_tag_similar_docs


class TestPreprocess(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.zettel_dir = Path(self.test_dir)

        (self.zettel_dir / "Note1.md").write_text("---\ntags: [apple, banana]\n---\nContent", encoding='utf-8')
        (self.zettel_dir / "Note2.md").write_text("Text with #apple tag", encoding='utf-8')
        (self.zettel_dir / "Note3.md").write_text("---\ntags: [cherry]\n---\nNo overlap", encoding='utf-8')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_extract_tags_inline(self):
        content = "This has #tag1 and #tag-2 embedded."
        tags = extract_tags(content)
        self.assertIn("tag1", tags)
        self.assertIn("tag-2", tags)

    def test_extract_tags_frontmatter_list(self):
        content = "---\ntags: [foo, bar]\n---\nContent"
        tags = extract_tags(content)
        self.assertIn("foo", tags)
        self.assertIn("bar", tags)

    def test_extract_tags_frontmatter_comma(self):
        content = "---\ntags: foo, bar\n---\nContent"
        tags = extract_tags(content)
        self.assertIn("foo", tags)
        self.assertIn("bar", tags)

    def test_find_tag_similar_docs(self):
        seed_path = self.zettel_dir / "seed.md"
        seed_path.write_text("Query tag #apple", encoding='utf-8')

        seed_tags = {"apple"}
        similar_paths = find_tag_similar_docs(seed_tags, self.zettel_dir, seed_path)

        self.assertTrue(any("Note1.md" in p for p in similar_paths))
        self.assertTrue(any("Note2.md" in p for p in similar_paths))
        self.assertFalse(any("Note3.md" in p for p in similar_paths))


if __name__ == '__main__':
    unittest.main()
