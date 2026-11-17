"""Structural test inputs only; no real conversation or demonstration data."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate_atlas.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class AtlasTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "test-only.jsonl"
        self.out = self.base / "index"
        self.records = [
            {"type": "user", "origin": {"kind": "human"}, "message": {"content": "TEST ONLY request"}},
            {"type": "assistant", "message": {"content": [
                {"type": "thinking", "thinking": "TEST_PRIVATE_REASONING_SENTINEL"},
                {"type": "text", "text": "TEST ONLY response"},
                {"type": "tool_use", "id": "test-1", "name": "Read", "input": {"path": "test-only.txt"}}]}},
            {"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "test-1", "content": "TEST ONLY result"}]}}
        ]
    def index(self):
        self.source.write_text("\n".join(json.dumps(r) for r in self.records) + "\n")
        return subprocess.run([sys.executable, str(ROOT / "scripts/index_claude_session.py"),
                               "--source", str(self.source), "--out-dir", str(self.out)],
                              capture_output=True, text=True)
    def test_roundtrip_and_reasoning_not_reproduced(self):
        self.assertEqual(self.index().returncode, 0)
        result = validator.validate(self.out, self.source, True)
        self.assertTrue(result["source_verified"])
        self.assertTrue(result["tool_linkage_complete"])
        for path in self.out.iterdir():
            self.assertNotIn("TEST_PRIVATE_REASONING_SENTINEL", path.read_text())
    def test_no_source_means_explicitly_unverified(self):
        self.index()
        self.assertFalse(validator.validate(self.out)["source_verified"])
    def test_tampered_source_fails(self):
        self.index()
        self.source.write_text("changed")
        with self.assertRaisesRegex(ValueError, "prefix mismatch"):
            validator.validate(self.out, self.source)
    def test_appended_source_preserves_snapshot(self):
        self.index()
        with self.source.open("a") as handle:
            handle.write("{}\n")
        self.assertTrue(validator.validate(self.out, self.source)["source_verified"])
    def test_missing_result_detected(self):
        self.records.pop()
        self.index()
        self.assertFalse(validator.validate(self.out)["tool_linkage_complete"])
        with self.assertRaisesRegex(ValueError, "incomplete"):
            validator.validate(self.out, require_complete=True)
    def test_private_coverage_text_rejected(self):
        self.index()
        (self.out / "thinking-coverage.jsonl").write_text(json.dumps({"thinking": "TEST ONLY"}) + "\n")
        with self.assertRaisesRegex(ValueError, "metadata only"):
            validator.validate(self.out)
    def test_invalid_json_refused(self):
        self.source.write_text("not-json\n")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/index_claude_session.py"),
                                 "--source", str(self.source), "--out-dir", str(self.out)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.out / "snapshot-manifest.json").exists())
    def test_turn_count_tamper_detected(self):
        self.index()
        (self.out / "turn-index.jsonl").write_text("")
        with self.assertRaisesRegex(ValueError, "count differs"):
            validator.validate(self.out)

    def test_assistant_evidence_tamper_detected_from_source(self):
        self.index()
        index = self.out / "turn-index.jsonl"
        turn = json.loads(index.read_text())
        turn["assistant_text"] = ["tampered"]
        index.write_text(json.dumps(turn) + "\n")
        with self.assertRaisesRegex(ValueError, "evidence differs"):
            validator.validate(self.out, self.source)

    def test_existing_output_refused_and_not_overwritten(self):
        self.index()
        before = (self.out / "turn-index.jsonl").read_bytes()
        self.assertNotEqual(self.index().returncode, 0)
        self.assertEqual((self.out / "turn-index.jsonl").read_bytes(), before)

    def test_output_symlink_refused(self):
        self.out.symlink_to(self.base, target_is_directory=True)
        self.assertNotEqual(self.index().returncode, 0)
        self.assertFalse((self.base / "snapshot-manifest.json").exists())

    def test_private_output_permissions(self):
        self.assertEqual(self.index().returncode, 0)
        self.assertEqual(self.out.stat().st_mode & 0o777, 0o700)
        for path in self.out.iterdir():
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

if __name__ == "__main__":
    unittest.main()
