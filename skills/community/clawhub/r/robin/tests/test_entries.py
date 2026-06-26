from __future__ import annotations

import json

from robin.config import load_index, save_index
from robin.parser import SEPARATOR
from robin.serializer import build_text_entry, serialize_entry
from scripts import entries


def _write_entries(robin_env, filename: str, items: list) -> None:
    (robin_env["topics_dir"] / filename).write_text(
        SEPARATOR.join(serialize_entry(item) for item in items) + "\n",
        encoding="utf-8",
    )


def _entry(entry_id: str, topic: str = "Writing", *, media_source: str = ""):
    return build_text_entry(
        topic=topic,
        content=f"Body for {entry_id}.",
        description=f"Description for {entry_id}.",
        source="",
        note="",
        tags=["writing"],
        date_added="2026-04-08",
        media_source=media_source,
        entry_id=entry_id,
    )


def test_entries_delete_removes_entry_and_index(robin_env, monkeypatch, capsys):
    first = _entry("20260408-a1f3c9")
    second = _entry("20260408-b7k2d1")
    _write_entries(robin_env, "writing.md", [first, second])
    save_index(
        {
            "items": {
                first.entry_id: {"id": first.entry_id, "topic": "writing", "date": first.date_added, "rating": 4, "last_surfaced": None, "times_surfaced": 1},
                second.entry_id: {"id": second.entry_id, "topic": "writing", "date": second.date_added, "rating": None, "last_surfaced": None, "times_surfaced": 0},
            }
        }
    )

    monkeypatch.setattr("sys.argv", ["entries.py", "--delete", first.entry_id, "--json"])
    try:
        entries.main()
    except SystemExit as exc:
        assert exc.code == 0

    output = json.loads(capsys.readouterr().out)
    content = (robin_env["topics_dir"] / "writing.md").read_text(encoding="utf-8")
    index = load_index()

    assert output["status"] == "deleted"
    assert first.entry_id not in content
    assert second.entry_id in content
    assert first.entry_id not in index["items"]
    assert second.entry_id in index["items"]


def test_entries_delete_removes_empty_topic_file_and_keeps_media(robin_env, monkeypatch, capsys):
    media = robin_env["state_dir"] / "media" / "writing" / "20260408-a1f3c9.png"
    media.parent.mkdir(parents=True)
    media.write_bytes(b"fake-image")
    item = _entry("20260408-a1f3c9", media_source="media/writing/20260408-a1f3c9.png")
    _write_entries(robin_env, "writing.md", [item])
    save_index({"items": {item.entry_id: {"id": item.entry_id, "topic": "writing", "date": item.date_added, "rating": None, "last_surfaced": None, "times_surfaced": 0}}})

    monkeypatch.setattr("sys.argv", ["entries.py", "--delete", item.entry_id, "--json"])
    try:
        entries.main()
    except SystemExit as exc:
        assert exc.code == 0

    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "deleted"
    assert not (robin_env["topics_dir"] / "writing.md").exists()
    assert media.exists()


def test_entries_move_preserves_entry_and_index_state(robin_env, monkeypatch, capsys):
    item = _entry("20260408-a1f3c9")
    _write_entries(robin_env, "writing.md", [item])
    save_index({"items": {item.entry_id: {"id": item.entry_id, "topic": "writing", "date": item.date_added, "rating": 5, "last_surfaced": "2026-04-09T10:00:00+00:00", "times_surfaced": 2}}})

    monkeypatch.setattr("sys.argv", ["entries.py", "--move", item.entry_id, "--topic", "AI Reasoning", "--json"])
    try:
        entries.main()
    except SystemExit as exc:
        assert exc.code == 0

    output = json.loads(capsys.readouterr().out)
    new_file = robin_env["topics_dir"] / "ai-reasoning.md"
    index = load_index()

    assert output["status"] == "moved"
    assert output["from_topic"] == "writing"
    assert output["to_topic"] == "ai-reasoning"
    assert not (robin_env["topics_dir"] / "writing.md").exists()
    assert item.entry_id in new_file.read_text(encoding="utf-8")
    assert index["items"][item.entry_id]["topic"] == "ai-reasoning"
    assert index["items"][item.entry_id]["rating"] == 5
    assert index["items"][item.entry_id]["times_surfaced"] == 2


def test_entries_move_requires_topic(robin_env, monkeypatch, capsys):
    item = _entry("20260408-a1f3c9")
    _write_entries(robin_env, "writing.md", [item])

    monkeypatch.setattr("sys.argv", ["entries.py", "--move", item.entry_id, "--json"])
    try:
        entries.main()
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("Expected SystemExit")

    output = json.loads(capsys.readouterr().out)
    assert output["error"] == "--move requires --topic."


def test_entries_move_rejects_invalid_topic(robin_env, monkeypatch, capsys):
    item = _entry("20260408-a1f3c9")
    _write_entries(robin_env, "writing.md", [item])

    monkeypatch.setattr("sys.argv", ["entries.py", "--move", item.entry_id, "--topic", ":::", "--json"])
    try:
        entries.main()
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("Expected SystemExit")

    output = json.loads(capsys.readouterr().out)
    assert "valid filename" in output["error"]


def test_entries_missing_id_fails_json(robin_env, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["entries.py", "--delete", "missing", "--json"])
    try:
        entries.main()
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("Expected SystemExit")

    output = json.loads(capsys.readouterr().out)
    assert "not found" in output["error"]
