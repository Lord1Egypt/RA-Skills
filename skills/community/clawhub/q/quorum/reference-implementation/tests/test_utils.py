"""Layer 1e: Unit tests for utilities — GrepTool, SchemaTool, path resolution, hashing."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from quorum.models import Locus
from quorum.tools.grep_tool import GrepMatch, GrepTool
from quorum.tools.schema_tool import SchemaTool, SchemaViolation
from quorum.pipeline import resolve_targets, _validate_path, _write_json


# ── GrepTool ─────────────────────────────────────────────────────────────────


class TestGrepToolSearchText:
    def test_basic_search(self):
        gt = GrepTool()
        matches = gt.search_text("hello world\nfoo bar\nhello again", "hello")
        assert len(matches) == 2
        assert matches[0].line_number == 1
        assert matches[1].line_number == 3

    def test_no_match(self):
        gt = GrepTool()
        matches = gt.search_text("nothing here", "missing")
        assert matches == []

    def test_case_insensitive(self):
        gt = GrepTool()
        matches = gt.search_text("Hello World", "hello", ignore_case=True)
        assert len(matches) == 1

    def test_case_sensitive_default(self):
        gt = GrepTool()
        matches = gt.search_text("Hello World", "hello", ignore_case=False)
        assert len(matches) == 0

    def test_literal_mode(self):
        gt = GrepTool()
        # Without literal, "." matches any char
        matches_regex = gt.search_text("abc", ".", literal=False)
        assert len(matches_regex) == 1
        # With literal, "." must be exact
        matches_literal = gt.search_text("abc", ".", literal=True)
        assert len(matches_literal) == 0

    def test_context_lines(self):
        text = "L1\nL2\nL3\nL4\nL5"
        gt = GrepTool(context_lines=1)
        matches = gt.search_text(text, "L3")
        assert matches[0].context_before == ["L2"]
        assert matches[0].context_after == ["L4"]

    def test_context_at_start(self):
        text = "L1\nL2\nL3"
        gt = GrepTool(context_lines=2)
        matches = gt.search_text(text, "L1")
        assert matches[0].context_before == []

    def test_context_at_end(self):
        text = "L1\nL2\nL3"
        gt = GrepTool(context_lines=2)
        matches = gt.search_text(text, "L3")
        assert matches[0].context_after == []

    def test_override_context_lines(self):
        text = "L1\nL2\nL3\nL4\nL5"
        gt = GrepTool(context_lines=2)
        matches = gt.search_text(text, "L3", context_lines=0)
        assert matches[0].context_before == []
        assert matches[0].context_after == []


class TestGrepToolSearchFile:
    def test_search_existing_file(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello\nworld\nhello again\n")
        gt = GrepTool()
        matches = gt.search_file(f, "hello")
        assert len(matches) == 2
        assert matches[0].file_path == str(f)

    def test_search_missing_file(self, tmp_path):
        gt = GrepTool()
        matches = gt.search_file(tmp_path / "missing.txt", "anything")
        assert matches == []


class TestGrepToolFindMissing:
    def test_all_present(self):
        gt = GrepTool()
        text = "abstract methods results conclusion"
        missing = gt.find_missing(text, ["abstract", "methods", "results"])
        assert missing == []

    def test_some_missing(self):
        gt = GrepTool()
        text = "abstract methods"
        missing = gt.find_missing(text, ["abstract", "methods", "results", "conclusion"])
        assert "results" in missing
        assert "conclusion" in missing

    def test_all_missing(self):
        gt = GrepTool()
        missing = gt.find_missing("empty", ["alpha", "beta"])
        assert len(missing) == 2


class TestGrepToolSummarize:
    def test_summarize_empty(self):
        gt = GrepTool()
        s = gt.summarize_matches([])
        assert "no matches" in s.lower()

    def test_summarize_matches(self):
        gt = GrepTool()
        matches = [GrepMatch(line_number=1, line="hello", pattern="hello")]
        s = gt.summarize_matches(matches)
        assert "hello" in s

    def test_summarize_truncation(self):
        gt = GrepTool()
        matches = [
            GrepMatch(line_number=i, line="x" * 100, pattern="x")
            for i in range(50)
        ]
        s = gt.summarize_matches(matches, max_chars=200)
        assert "more matches" in s


class TestGrepMatchFormat:
    def test_format_basic(self):
        m = GrepMatch(line_number=5, line="found it", pattern="found")
        formatted = m.format()
        assert "5" in formatted
        assert "found it" in formatted

    def test_format_with_file(self):
        m = GrepMatch(line_number=1, line="x", pattern="x", file_path="test.py")
        formatted = m.format()
        assert "test.py" in formatted

    def test_format_without_context(self):
        m = GrepMatch(
            line_number=3, line="target_line", pattern="target",
            context_before=["before_1", "before_2"], context_after=["after_1"],
        )
        formatted = m.format(show_context=False)
        assert "before_1" not in formatted
        assert "after_1" not in formatted
        assert "target_line" in formatted


# ── SchemaTool ───────────────────────────────────────────────────────────────


class TestSchemaToolLoad:
    def test_load_json(self, tmp_path):
        f = tmp_path / "data.json"
        f.write_text('{"key": "value"}')
        st = SchemaTool()
        data, err = st.load(f)
        assert data == {"key": "value"}
        assert err is None

    def test_load_yaml(self, tmp_path):
        f = tmp_path / "data.yaml"
        f.write_text("key: value\n")
        st = SchemaTool()
        data, err = st.load(f)
        assert data == {"key": "value"}
        assert err is None

    def test_load_missing_file(self, tmp_path):
        st = SchemaTool()
        data, err = st.load(tmp_path / "missing.json")
        assert data is None
        assert "not found" in err.lower()

    def test_load_invalid_json(self, tmp_path):
        f = tmp_path / "bad.json"
        f.write_text("{invalid}")
        st = SchemaTool()
        data, err = st.load(f)
        assert data is None
        assert "parse error" in err.lower()

    def test_load_non_dict_root(self, tmp_path):
        f = tmp_path / "list.json"
        f.write_text("[1, 2, 3]")
        st = SchemaTool()
        data, err = st.load(f)
        assert data is None
        assert "mapping" in err.lower()


class TestSchemaToolCheckRequired:
    def test_all_present(self):
        st = SchemaTool()
        violations = st.check_required_keys(
            {"name": "x", "version": "1.0"}, ["name", "version"]
        )
        assert violations == []

    def test_missing_key(self):
        st = SchemaTool()
        violations = st.check_required_keys({"name": "x"}, ["name", "version"])
        assert len(violations) == 1
        assert "version" in violations[0].path

    def test_nested_key(self):
        st = SchemaTool()
        data = {"config": {"model": "opus"}}
        violations = st.check_required_keys(data, ["config.model"])
        assert violations == []

    def test_nested_missing(self):
        st = SchemaTool()
        data = {"config": {}}
        violations = st.check_required_keys(data, ["config.model"])
        assert len(violations) == 1


class TestSchemaToolCheckTypes:
    def test_correct_types(self):
        st = SchemaTool()
        data = {"name": "x", "count": 42}
        violations = st.check_types(data, {"name": str, "count": int})
        assert violations == []

    def test_wrong_type(self):
        st = SchemaTool()
        data = {"name": "x", "count": "not a number"}
        violations = st.check_types(data, {"count": int})
        assert len(violations) == 1
        assert "Wrong type" in violations[0].message

    def test_tuple_type(self):
        st = SchemaTool()
        data = {"value": 42}
        violations = st.check_types(data, {"value": (int, float)})
        assert violations == []

    def test_missing_key_not_type_error(self):
        st = SchemaTool()
        data = {}
        violations = st.check_types(data, {"missing": str})
        assert violations == []  # Missing keys are not type violations


class TestSchemaToolFormat:
    def test_format_violations(self):
        st = SchemaTool()
        violations = [
            SchemaViolation(path="name", message="Required", expected="string", actual="absent"),
        ]
        s = st.format_violations(violations)
        assert "name" in s
        assert "Required" in s

    def test_format_empty(self):
        st = SchemaTool()
        s = st.format_violations([])
        assert "no schema violations" in s.lower()


class TestSchemaViolationFormat:
    def test_basic_format(self):
        v = SchemaViolation(path="$.name", message="Missing", expected="string", actual="null")
        s = v.format()
        assert "$.name" in s
        assert "Missing" in s
        assert "string" in s


# ── Path resolution ──────────────────────────────────────────────────────────


class TestResolveTargets:
    def test_single_file(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("# Hello")
        result = resolve_targets(f)
        assert len(result) == 1
        assert result[0] == f.resolve()

    def test_directory(self, tmp_path):
        (tmp_path / "a.md").write_text("a")
        (tmp_path / "b.py").write_text("b")
        (tmp_path / "c.bin").write_bytes(b"\x00")  # not a text extension
        result = resolve_targets(tmp_path)
        # Should find .md and .py but not .bin
        extensions = {p.suffix for p in result}
        assert ".md" in extensions
        assert ".py" in extensions

    def test_directory_with_pattern(self, tmp_path):
        (tmp_path / "a.md").write_text("a")
        (tmp_path / "b.py").write_text("b")
        result = resolve_targets(tmp_path, pattern="*.md")
        assert len(result) == 1
        assert result[0].suffix == ".md"

    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            resolve_targets(tmp_path / "missing.md")

    def test_null_byte_rejected(self):
        with pytest.raises(ValueError, match="null bytes"):
            resolve_targets("test\x00file.md")

    def test_pattern_traversal_rejected(self, tmp_path):
        (tmp_path / "a.md").write_text("a")
        with pytest.raises(ValueError, match="path traversal"):
            resolve_targets(tmp_path, pattern="../../*.md")

    def test_pattern_shell_chars_rejected(self, tmp_path):
        (tmp_path / "a.md").write_text("a")
        with pytest.raises(ValueError, match="disallowed"):
            resolve_targets(tmp_path, pattern="*.md; rm -rf /")


class TestValidatePath:
    def test_valid_path(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("x")
        result = _validate_path(f, boundary=tmp_path)
        assert result == f.resolve()

    def test_traversal_blocked(self, tmp_path):
        f = tmp_path / ".." / "escape.md"
        with pytest.raises(ValueError, match="escapes"):
            _validate_path(f, boundary=tmp_path)


# ── File hashing ─────────────────────────────────────────────────────────────


class TestFileHashing:
    def test_hash_consistency(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("line1\nline2\nline3\n")
        h1 = Locus.compute_hash(f, 1, 3)
        h2 = Locus.compute_hash(f, 1, 3)
        assert h1 == h2

    def test_hash_changes_with_content(self, tmp_path):
        f1 = tmp_path / "a.txt"
        f1.write_text("aaa\nbbb\n")
        f2 = tmp_path / "b.txt"
        f2.write_text("aaa\nccc\n")
        h1 = Locus.compute_hash(f1, 1, 2)
        h2 = Locus.compute_hash(f2, 1, 2)
        assert h1 != h2

    def test_hash_from_content(self):
        content = "hello\nworld\n"
        h = Locus.compute_hash_from_content(content, 1, 2)
        assert isinstance(h, str)
        assert len(h) == 64  # SHA-256 hex

    def test_hash_subset(self):
        content = "line1\nline2\nline3\n"
        h_all = Locus.compute_hash_from_content(content, 1, 3)
        h_sub = Locus.compute_hash_from_content(content, 1, 1)
        assert h_all != h_sub


# ── JSON writing ─────────────────────────────────────────────────────────────


class TestJSONWriting:
    def test_write_json(self, tmp_path):
        path = tmp_path / "output.json"
        _write_json(path, {"key": "value"})
        with open(path) as f:
            data = json.load(f)
        assert data["key"] == "value"

    def test_write_json_creates_parents(self, tmp_path):
        path = tmp_path / "sub" / "dir" / "output.json"
        _write_json(path, {"nested": True})
        assert path.exists()

    def test_write_json_indent(self, tmp_path):
        path = tmp_path / "output.json"
        _write_json(path, {"key": "value"})
        text = path.read_text()
        # Should be indented (pretty-printed)
        assert "  " in text
