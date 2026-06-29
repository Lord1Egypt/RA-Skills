"""Unit tests for research_mode_utils: slugify, timestamps, TSV, JSONL, StateEditor, etc."""
from __future__ import annotations

import datetime as dt
from pathlib import Path

from .helpers import assert_eq, assert_in, assert_true

from research_mode_utils import (
    StateEditor,
    StateNotFoundError,
    ValidationError,
    append_jsonl,
    append_tsv_row,
    atomic_json_write,
    compact_text,
    minutes_since,
    parse_ts,
    read_json,
    read_jsonl,
    read_tsv_rows,
    slugify,
    tsv_escape,
)


def test_slugify_ascii(root: Path) -> None:
    assert_eq(slugify("Hello World!"), "hello-world", "simple ASCII slugify")


def test_slugify_cyrillic_fallback(root: Path) -> None:
    """Pure Cyrillic should fall back to hash-based slug."""
    result = slugify("Исследование рынка")
    assert_true(result.startswith("task-"), f"cyrillic should fallback to task-<hash>, got {result!r}")
    assert_eq(len(result), 13, "task- + 8 hex chars = 13")


def test_slugify_mixed(root: Path) -> None:
    result = slugify("Project Alpha — 2026")
    assert_in("project-alpha", result, "ASCII part should be preserved")


def test_slugify_truncation(root: Path) -> None:
    long_text = "a" * 100
    result = slugify(long_text)
    assert_true(len(result) <= 48, f"slug should be max 48 chars, got {len(result)}")


def test_parse_ts_none(root: Path) -> None:
    assert_eq(parse_ts(None), None, "None -> None")
    assert_eq(parse_ts(""), None, "empty string -> None")


def test_parse_ts_iso_z(root: Path) -> None:
    result = parse_ts("2026-04-04T12:00:00Z")
    assert_true(result is not None, "should parse Z-suffixed ISO timestamp")
    assert_eq(result.year, 2026, "year should be 2026")
    assert_eq(result.hour, 12, "hour should be 12")
    assert_true(result.tzinfo is not None, "should be timezone-aware")


def test_minutes_since_none(root: Path) -> None:
    assert_eq(minutes_since(None), None, "None -> None")
    assert_eq(minutes_since(""), None, "empty -> None")


def test_minutes_since_known_delta(root: Path) -> None:
    now = dt.datetime(2026, 4, 4, 12, 30, 0, tzinfo=dt.timezone.utc)
    result = minutes_since("2026-04-04T12:00:00Z", now=now)
    assert_eq(result, 30.0, "30 minutes difference")


def test_compact_text_short(root: Path) -> None:
    assert_eq(compact_text("Hello"), "Hello", "short text unchanged")


def test_compact_text_truncates(root: Path) -> None:
    result = compact_text("a " * 100, limit=20)
    assert_true(len(result) <= 20, f"should be <= 20 chars, got {len(result)}")
    assert_true(result.endswith("…"), "should end with ellipsis")


def test_compact_text_collapses_whitespace(root: Path) -> None:
    result = compact_text("  hello   world  \n\n  foo  ")
    assert_eq(result, "hello world foo", "whitespace should be collapsed")


def test_compact_text_none(root: Path) -> None:
    assert_eq(compact_text(None), "", "None -> empty string")


def test_tsv_escape_none(root: Path) -> None:
    assert_eq(tsv_escape(None), "", "None -> empty")


def test_tsv_escape_bool(root: Path) -> None:
    assert_eq(tsv_escape(True), "yes", "True -> yes")
    assert_eq(tsv_escape(False), "no", "False -> no")


def test_tsv_escape_special_chars(root: Path) -> None:
    assert_eq(tsv_escape("a\tb\nc\rd"), "a b / c d", "tabs/newlines/CRs should be replaced")


def test_atomic_json_write_and_read(root: Path) -> None:
    path = root / "test-utils-atomic" / "data.json"
    data = {"key": "value", "число": 42}
    atomic_json_write(path, data)
    assert_true(path.exists(), "file should exist after write")
    loaded = read_json(path)
    assert_eq(loaded["key"], "value", "string value preserved")
    assert_eq(loaded["число"], 42, "non-ASCII key and int value preserved")


def test_atomic_json_write_no_tmp_left(root: Path) -> None:
    """After atomic write, no .tmp file should remain."""
    path = root / "test-utils-notmp" / "data.json"
    atomic_json_write(path, {"ok": True})
    tmp_path = path.with_suffix(".json.tmp")
    assert_true(not tmp_path.exists(), ".tmp file should not remain after atomic write")


def test_read_json_missing_file(root: Path) -> None:
    try:
        read_json(root / "nonexistent.json")
        raise AssertionError("should raise StateNotFoundError")
    except StateNotFoundError:
        pass


def test_read_json_invalid_json(root: Path) -> None:
    bad_path = root / "test-utils-badjson" / "bad.json"
    bad_path.parent.mkdir(parents=True, exist_ok=True)
    bad_path.write_text("{ not valid json }", encoding="utf-8")
    try:
        read_json(bad_path)
        raise AssertionError("should raise ValidationError")
    except ValidationError:
        pass


def test_append_jsonl_and_read(root: Path) -> None:
    path = root / "test-utils-jsonl" / "log.jsonl"
    append_jsonl(path, [{"a": 1}, {"b": 2}])
    append_jsonl(path, [{"c": 3}])
    records = read_jsonl(path)
    assert_eq(len(records), 3, "should have 3 records")
    assert_eq(records[0]["a"], 1, "first record")
    assert_eq(records[2]["c"], 3, "third record")


def test_append_jsonl_empty_list(root: Path) -> None:
    path = root / "test-utils-jsonl-empty" / "log.jsonl"
    append_jsonl(path, [])
    assert_true(not path.exists(), "empty append should not create file")


def test_read_jsonl_missing_file(root: Path) -> None:
    result = read_jsonl(root / "nonexistent.jsonl")
    assert_eq(result, [], "missing file -> empty list")


def test_read_jsonl_invalid_line(root: Path) -> None:
    path = root / "test-utils-jsonl-bad" / "bad.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"ok": true}\n{ broken json }\n', encoding="utf-8")
    try:
        read_jsonl(path)
        raise AssertionError("should raise ValidationError for invalid JSONL line")
    except ValidationError:
        pass


def test_append_tsv_and_read(root: Path) -> None:
    path = root / "test-utils-tsv" / "log.tsv"
    cols = ["name", "value", "active"]
    append_tsv_row(path, cols, {"name": "alpha", "value": "100", "active": True})
    append_tsv_row(path, cols, {"name": "beta", "value": "200", "active": False})
    rows = read_tsv_rows(path)
    assert_eq(len(rows), 2, "should have 2 rows")
    assert_eq(rows[0]["name"], "alpha", "first row name")
    assert_eq(rows[1]["active"], "no", "bool should be tsv_escaped to no")


def test_read_tsv_missing_file(root: Path) -> None:
    result = read_tsv_rows(root / "nonexistent.tsv")
    assert_eq(result, [], "missing file -> empty list")


def test_state_editor_roundtrip(root: Path) -> None:
    path = root / "test-utils-editor" / "state.json"
    atomic_json_write(path, {"status": "idle", "count": 0})

    with StateEditor(path) as state:
        state["count"] = 42
        state["status"] = "active"

    loaded = read_json(path)
    assert_eq(loaded["count"], 42, "count should be updated")
    assert_eq(loaded["status"], "active", "status should be updated")


def test_state_editor_rollback_on_error(root: Path) -> None:
    """If an exception occurs inside the context manager, changes should NOT be written."""
    path = root / "test-utils-editor-err" / "state.json"
    atomic_json_write(path, {"status": "idle", "count": 0})

    try:
        with StateEditor(path) as state:
            state["count"] = 999
            raise ValueError("deliberate error")
    except ValueError:
        pass

    loaded = read_json(path)
    assert_eq(loaded["count"], 0, "changes should not persist after exception")


def test_state_editor_invalid_json(root: Path) -> None:
    path = root / "test-utils-editor-bad" / "state.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json at all", encoding="utf-8")

    try:
        with StateEditor(path) as _state:
            raise AssertionError("should not reach here")
    except ValidationError:
        pass
