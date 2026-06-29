"""
Tests for axiom-rebrand — Generic rebrand pipeline.

Verifies:
- strip_jargon() catches all major patterns
- fix_sys_path() rewrites hardcoded paths
- rebrand_file() is deterministic
- rebrand_project() is idempotent byte-to-byte
- Custom config patterns work
- Excludes work
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent to import path
sys.path.insert(0, str(Path(__file__).parent))
from axiom_rebrand import rebrand_project, rebrand_file, strip_jargon, fix_sys_path, sha256_file
from axiom_rebrand.rebrand import (
    DEFAULT_JARGON_PATTERNS, DEFAULT_EXCLUDE_PATTERNS, load_jargon_from_config
)


class TestStripJargon(unittest.TestCase):
    """Verify strip_jargon() catches all known patterns."""

    def test_auteur_line(self):
        text = "# Auteur: 🐺 Alice\nrest of line\n"
        cleaned, n = strip_jargon(text)
        self.assertNotIn("Auteur", cleaned)
        self.assertGreaterEqual(n, 1)

    def test_author_line(self):
        text = "# Author: Bob\nrest\n"
        cleaned, n = strip_jargon(text)
        self.assertNotIn("Author", cleaned)
        self.assertGreaterEqual(n, 1)

    def test_premier_jet(self):
        text = "Some text (premier jet) here.\n"
        cleaned, n = strip_jargon(text)
        self.assertNotIn("premier jet", cleaned)
        self.assertGreaterEqual(n, 1)

    def test_premier_jet_uppercase(self):
        text = "Some text (PREMIER JET) here.\n"
        cleaned, n = strip_jargon(text)
        self.assertNotIn("PREMIER JET", cleaned)
        self.assertGreaterEqual(n, 1)

    def test_first_draft_replaced(self):
        text = "This is the first draft of v0.1.0.\n"
        cleaned, n = strip_jargon(text)
        self.assertIn("first version", cleaned)
        self.assertNotIn("first draft", cleaned)
        self.assertGreaterEqual(n, 1)

    def test_in_altum(self):
        text = "# _In Altum Per Cluster._\nrest\n"
        cleaned, n = strip_jargon(text)
        self.assertNotIn("In Altum", cleaned)
        self.assertGreaterEqual(n, 1)

    # === Ezekiel Fix #2: cluster patterns NOT in defaults ===
    # These patterns are loaded via --config examples/cluster-jargon.yaml
    # They should NOT be stripped by default (risk of destroying innocent code)
    def test_cluster_axioma_stellaris_NOT_in_defaults(self):
        text = "Part of the cluster Axioma Stellaris, validated by the L9 Hub.\n"
        cleaned, n = strip_jargon(text)  # defaults only
        # Generic defaults should NOT strip this
        self.assertIn("Axioma Stellaris", cleaned)
        self.assertIn("L9 Hub", cleaned)
        self.assertEqual(n, 0)

    def test_cluster_patterns_via_config(self):
        # When cluster config is loaded, patterns ARE stripped
        from axiom_rebrand.rebrand import load_jargon_from_config
        config_path = Path(__file__).parent / "examples" / "cluster-jargon.yaml"
        if config_path.exists():
            patterns = load_jargon_from_config(config_path)
            text = "Part of the cluster Axioma Stellaris, validated by the L9 Hub.\n"
            cleaned, n = strip_jargon(text, patterns)
            self.assertNotIn("Axioma Stellaris", cleaned)
            self.assertNotIn("L9 Hub", cleaned)
            self.assertGreaterEqual(n, 2)

    def test_emoji_merlin_souleymane_via_config(self):
        # Emojis only stripped via config (could be in test data)
        from axiom_rebrand.rebrand import load_jargon_from_config
        config_path = Path(__file__).parent / "examples" / "cluster-jargon.yaml"
        if config_path.exists():
            patterns = load_jargon_from_config(config_path)
            text = "Magic happens here 🐺🌬️ — bytes and air together.\n"
            cleaned, n = strip_jargon(text, patterns)
            self.assertNotIn("🐺", cleaned)
            self.assertNotIn("🌬️", cleaned)
            self.assertGreaterEqual(n, 1)

    def test_path_removed(self):
        text = "Path: /run/internal/secret/path\n"
        cleaned, n = strip_jargon(text)
        self.assertNotIn("/run/internal", cleaned)

    def test_custom_patterns(self):
        text = "Internal Team Reference Here\n"
        custom = [(__import__("re").compile(r"Internal Team"), "")]
        cleaned, n = strip_jargon(text, custom)
        self.assertNotIn("Internal Team", cleaned)
        self.assertEqual(n, 1)


class TestFixSysPath(unittest.TestCase):
    """Verify fix_sys_path() rewrites hardcoded paths."""

    def test_double_quote(self):
        text = (
            'import sys\n'
            'sys.path.insert(0, "/run/media/axioma/skills/foo")\n'
        )
        fixed, n = fix_sys_path(text)
        self.assertIn("str(Path(__file__).parent)", fixed)
        self.assertIn("from pathlib import Path", fixed)
        self.assertEqual(n, 1)

    def test_single_quote(self):
        text = (
            "import sys\n"
            "sys.path.insert(0, '/run/media/axioma/skills/foo')\n"
        )
        fixed, n = fix_sys_path(text)
        self.assertIn("str(Path(__file__).parent)", fixed)
        self.assertEqual(n, 1)

    def test_no_op_when_already_fixed(self):
        text = 'import sys\nsys.path.insert(0, str(Path(__file__).parent))\n'
        fixed, n = fix_sys_path(text)
        self.assertEqual(n, 0)


class TestSHA256(unittest.TestCase):
    def test_basic(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("hello world")
            path = Path(f.name)
        try:
            h = sha256_file(path)
            self.assertEqual(h, "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9")
        finally:
            path.unlink()


class TestConfigLoading(unittest.TestCase):
    def test_json_config(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            f.write('{"jargon": [{"pattern": "Author.*", "replacement": ""}, {"pattern": "Internal", "replacement": ""}]}')
            path = Path(f.name)
        try:
            patterns = load_jargon_from_config(path)
            self.assertEqual(len(patterns), 2)
        finally:
            path.unlink()

    # === BUG #1 fix: extension-based detection for YAML ===
    def test_yaml_config_by_extension(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
            f.write("jargon:\n  - pattern: 'foo'\n    replacement: 'bar'\n")
            path = Path(f.name)
        try:
            patterns = load_jargon_from_config(path)
            self.assertEqual(len(patterns), 1)
            pat, rep = patterns[0]
            self.assertEqual(pat.pattern, "foo")
            self.assertEqual(rep, "bar")
        finally:
            path.unlink()

    def test_yml_config_by_extension(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yml") as f:
            f.write("jargon:\n  - pattern: 'hello'\n    replacement: ''\n  - pattern: 'world'\n    replacement: ''\n")
            path = Path(f.name)
        try:
            patterns = load_jargon_from_config(path)
            self.assertEqual(len(patterns), 2)
        finally:
            path.unlink()

    def test_text_fallback_config(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("# comment\nAuthor.*:\nInternal:\n")
            path = Path(f.name)
        try:
            patterns = load_jargon_from_config(path)
            self.assertEqual(len(patterns), 2)
        finally:
            path.unlink()


class TestIdempotence(unittest.TestCase):
    """Verify rebrand_project is idempotent byte-to-byte."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.src = Path(self.tmpdir) / "src"
        self.src.mkdir()
        (self.src / "README.md").write_text(
            "# test-project\n"
            "# Author: Bob\n"
            "Some content.\n"
            "Reference to (premier jet) should be removed.\n"
            "cluster Axioma Stellaris, validated by the L9 Hub.\n"  # NOT stripped by defaults
            "Author: \U0001f43a Merlin (L9 Hub) and \U0001f32c\ufe0f Souleymane\n"
        )
        (self.src / "main.py").write_text(
            "import sys\n"
            'sys.path.insert(0, "/run/internal/secret")\n'
            "def main():\n"
            "    pass\n"
        )
        (self.src / "test_main.py").write_text(
            "import unittest\n\n"
            "class TestMain(unittest.TestCase):\n"
            "    def test_run(self):\n"
            "        pass\n"
        )
        (self.src / "main.py.auto.md").write_text("# backup\n")
        (self.src / "ORCHESTRATION.md").write_text("internal\n")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_byte_to_byte_identical(self):
        dst = Path(self.tmpdir) / "dst"
        # Run 1
        rebrand_project(self.src, dst, project_name="test", skip_validate=True)
        files_1 = sorted(
            (p.name, sha256_file(p))
            for p in dst.iterdir()
            if p.is_file() and p.name != "MANIFEST.txt"
        )
        # Run 2
        rebrand_project(self.src, dst, project_name="test", skip_validate=True)
        files_2 = sorted(
            (p.name, sha256_file(p))
            for p in dst.iterdir()
            if p.is_file() and p.name != "MANIFEST.txt"
        )
        self.assertEqual(files_1, files_2, "Idempotence failed")
        # Verify GENERIC jargon gone (cluster patterns stay — not in defaults)
        readme = (dst / "README.md").read_text()
        self.assertNotIn("premier jet", readme)
        # Cluster patterns are preserved by default (Ezekiel Fix #2)
        self.assertIn("Axioma Stellaris", readme)
        self.assertIn("L9 Hub", readme)
        # The Author: line is eaten by the Author pattern, so 🐺/🌬️ are
        # incidentally removed too. That's OK — the test for explicit
        # emoji stripping is in test_emoji_merlin_souleymane_via_config
        # (requires the cluster config to load).
        # Verify sys.path fixed
        main_py = (dst / "main.py").read_text()
        self.assertIn("str(Path(__file__).parent)", main_py)
        self.assertNotIn("/run/internal", main_py)
        # Verify excludes
        dst_files = {p.name for p in dst.iterdir() if p.is_file()}
        self.assertNotIn("main.py.auto.md", dst_files)
        self.assertNotIn("ORCHESTRATION.md", dst_files)


class TestExcludes(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.src = Path(self.tmpdir) / "src"
        self.src.mkdir()
        (self.src / "README.md").write_text("hi\n")
        (self.src / "main.py").write_text("pass\n")
        (self.src / "main.pyc").write_text("bytecode\n")
        (self.src / ".DS_Store").write_text("mac\n")
        (self.src / "main.swp").write_text("vim\n")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_excluded_files_not_copied(self):
        dst = Path(self.tmpdir) / "dst"
        rebrand_project(self.src, dst, project_name="test", skip_validate=True)
        dst_files = {p.name for p in dst.iterdir() if p.is_file()}
        self.assertIn("README.md", dst_files)
        self.assertIn("main.py", dst_files)
        self.assertNotIn("main.pyc", dst_files)
        self.assertNotIn(".DS_Store", dst_files)
        self.assertNotIn("main.swp", dst_files)


if __name__ == "__main__":
    unittest.main()
