import importlib.util
import json
import os
import tempfile
import subprocess
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("renderer", ROOT / "scripts/render_architecture.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.scripts = []
        self.in_script = False
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag == "script":
            self.in_script = True
            self.scripts.append("")
    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
    def handle_data(self, data):
        if self.in_script:
            self.scripts[-1] += data

class EscapingTests(unittest.TestCase):
    payload = '\" onload=\"window.INJECTED=1 <script>window.INJECTED=1</script> & \' '
    def data(self):
        return {"title": self.payload, "summary": self.payload, "nodes": [{"id": self.payload, "label": self.payload, "kind": "service", "x": 120, "y": 160}], "edges": []}
    def assert_no_active_payload(self, html, scripts):
        parser = Parser()
        parser.feed(html)
        self.assertEqual(len(parser.scripts), scripts)
        for _, attrs in parser.tags:
            self.assertFalse(any(k.lower().startswith("on") for k in attrs))
        return parser
    def test_svg_attributes_round_trip_without_handlers(self):
        for svg in (renderer.render(self.data()), renderer.render_share_card(self.data(), "example.json")):
            tree = ET.fromstring(svg)
            self.assertEqual(tree.attrib["aria-label"], self.payload)
            for node in tree.iter():
                self.assertFalse(any(k.lower().startswith("on") for k in node.attrib))
                self.assertNotEqual(node.tag.split("}")[-1], "script")
        self.assert_no_active_payload(renderer.render_html(self.data(), renderer.render(self.data()), "example.json"), 0)
    def test_gallery_script_terminator_and_filename_are_data(self):
        original = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                Path("examples").mkdir()
                data = self.data()
                data["story"] = [{"title": "</ScRiPt><script>window.INJECTED=1</script>", "text": "x"}]
                Path('examples/quoted\" onmouseover=\"bad.json').write_text(json.dumps(data))
                renderer.handle_gallery(SimpleNamespace(output="index.html"))
                html = Path("index.html").read_text()
                parser = self.assert_no_active_payload(html, 1)
                script = parser.scripts[0]
                payload = script.split("const artifacts = ", 1)[1].split(";\n", 1)[0]
                self.assertEqual(json.loads(payload)[0]["title"], self.payload)
                self.assertNotIn("</script", script.lower())
            finally:
                os.chdir(original)
    def test_json_preserves_special_characters(self):
        value = {"text": "<>&\u2028\u2029"}
        encoded = renderer.script_json(value)
        self.assertEqual(json.loads(encoded), value)
        self.assertNotIn("<", encoded)

class GitRevisionTests(unittest.TestCase):
    def test_revision_options_cannot_create_or_truncate_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "keep.txt"
            target.write_text("preserve")
            for base, head in [("--output=" + str(target), "WORKTREE"), ("HEAD", "--output=" + str(target))]:
                with self.assertRaises(ValueError):
                    renderer.changed_files(base, head, root)
                self.assertEqual(target.read_text(), "preserve")

    def test_valid_commit_and_worktree_diffs_use_selected_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()
            git("init")
            file = root / "sample.txt"
            file.write_text("before")
            git("add", "sample.txt")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "base")
            base = git("rev-parse", "HEAD")
            file.write_text("after")
            self.assertEqual(renderer.changed_files(base, "WORKTREE", root), [("M", "sample.txt")])
            git("add", "sample.txt")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "head")
            self.assertEqual(renderer.changed_files(base, "HEAD", root), [("M", "sample.txt")])
            for base_ref, head_ref in [("--output=keep.txt", "WORKTREE"), (base, "--output=keep.txt"), ("missing-ref", "HEAD")]:
                with self.assertRaises(ValueError):
                    renderer.changed_files(base_ref, head_ref, root)
            self.assertFalse((root / "keep.txt").exists())

if __name__ == "__main__":
    unittest.main()
