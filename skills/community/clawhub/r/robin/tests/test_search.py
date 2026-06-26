from __future__ import annotations

import json
from pathlib import Path

from robin.config import load_index, save_index
from robin.serializer import build_media_entry, build_text_entry, serialize_entry
from scripts import search, topics


def test_search_and_topics_json(robin_env, monkeypatch, capsys):
    topic_file = robin_env["topics_dir"] / "writing.md"
    topic_file.write_text(
        serialize_entry(
            build_text_entry(
                topic="Writing",
                content="Write as if you were speaking to a smart friend.",
                description="Guidance on conversational clarity in writing.",
                source="https://example.com",
                note="",
                tags=["writing", "clarity"],
                date_added="2026-04-08",
                entry_id="20260408-a1f3c9",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    index = load_index()
    index["items"]["20260408-a1f3c9"] = {
        "id": "20260408-a1f3c9",
        "topic": "writing",
        "date": "2026-04-08",
        "rating": 4,
        "last_surfaced": None,
        "times_surfaced": 0,
    }
    save_index(index)

    monkeypatch.setattr("sys.argv", ["search.py", "smart friend", "--json"])
    search.main()
    search_output = json.loads(capsys.readouterr().out)
    assert search_output["count"] == 1
    assert search_output["entries"][0]["description"] == "Guidance on conversational clarity in writing."
    assert search_output["entries"][0]["rating"] == 4

    monkeypatch.setattr("sys.argv", ["topics.py", "--json"])
    topics.main()
    topics_output = json.loads(capsys.readouterr().out)
    assert topics_output == [
        {
            "topic": "writing",
            "filename": "writing.md",
            "entries": 1,
            "rated": 1,
            "unrated": 0,
        }
    ]


def test_search_matches_media_metadata(robin_env, monkeypatch, capsys):
    topic_file = robin_env["topics_dir"] / "talks.md"
    topic_file.write_text(
        serialize_entry(
            build_media_entry(
                topic="Talks",
                media_kind="video",
                media_source="https://www.youtube.com/watch?v=abc123",
                description="A talk to revisit later.",
                creator="Speaker Name",
                published_at="2025-01-01",
                summary="A concise summary of the talk.",
                content="",
                source="",
                note="",
                tags=["talks"],
                date_added="2026-04-08",
                entry_id="20260408-v1a2b3",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr("sys.argv", ["search.py", "Speaker Name", "--json"])
    search.main()
    output = json.loads(capsys.readouterr().out)
    assert output["count"] == 1
    assert output["entries"][0]["media_source"] == "https://www.youtube.com/watch?v=abc123"
    assert output["entries"][0]["summary"] == "A concise summary of the talk."


def test_search_topic_filter_normalizes_user_input(robin_env, monkeypatch, capsys):
    topic_file = robin_env["topics_dir"] / "ai-reasoning.md"
    topic_file.write_text(
        serialize_entry(
            build_text_entry(
                topic="AI Reasoning",
                content="Distinguish claims from evidence.",
                description="Guidance on reasoning clearly.",
                source="",
                note="",
                tags=["reasoning"],
                date_added="2026-04-08",
                entry_id="20260408-a1f3c9",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr("sys.argv", ["search.py", "--topic", "AI Reasoning", "--json"])
    search.main()
    output = json.loads(capsys.readouterr().out)

    assert output["count"] == 1
    assert output["entries"][0]["topic"] == "ai-reasoning"


def test_search_topic_filter_only_reads_target_topic_file(robin_env, monkeypatch, capsys):
    good_topic = robin_env["topics_dir"] / "ai-reasoning.md"
    good_topic.write_text(
        serialize_entry(
            build_text_entry(
                topic="AI Reasoning",
                content="Distinguish claims from evidence.",
                description="Guidance on reasoning clearly.",
                source="",
                note="",
                tags=["reasoning"],
                date_added="2026-04-08",
                entry_id="20260408-a1f3c9",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    broken_topic = robin_env["topics_dir"] / "broken.md"
    broken_topic.write_text("date_added 2026-04-08\n\nBroken entry\n", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["search.py", "--topic", "AI Reasoning", "--json"])
    search.main()
    output = json.loads(capsys.readouterr().out)

    assert output["count"] == 1
    assert output["entries"][0]["topic"] == "ai-reasoning"


def test_search_matches_tags_in_free_text_query(robin_env, monkeypatch, capsys):
    topic_file = robin_env["topics_dir"] / "writing.md"
    topic_file.write_text(
        serialize_entry(
            build_text_entry(
                topic="Writing",
                content="Write simply.",
                description="Guidance on clearer prose.",
                source="",
                note="",
                tags=["machine-learning", "clarity"],
                date_added="2026-04-08",
                entry_id="20260408-a1f3c9",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr("sys.argv", ["search.py", "machine-learning", "--json"])
    search.main()
    output = json.loads(capsys.readouterr().out)

    assert output["count"] == 1
    assert output["entries"][0]["tags"] == ["machine-learning", "clarity"]


def test_search_rejects_empty_tags_filter(robin_env, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["search.py", "--tags", ",", "--json"])

    try:
        search.main()
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("Expected SystemExit for empty tag filter")

    output = json.loads(capsys.readouterr().out)
    assert output["error"] == "Provide at least one non-empty tag."


def test_search_reports_malformed_entry_as_json_error(robin_env, monkeypatch, capsys):
    topic_file = robin_env["topics_dir"] / "broken.md"
    topic_file.write_text("date_added 2026-04-08\n\nBroken entry\n", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["search.py", "--json"])

    try:
        search.main()
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("Expected SystemExit for malformed entry")

    output = json.loads(capsys.readouterr().out)
    assert "Failed to parse entry" in output["error"]


def test_search_tags_heading_omits_empty_elements(robin_env, monkeypatch, capsys):
    topic_file = robin_env["topics_dir"] / "writing.md"
    topic_file.write_text(
        serialize_entry(
            build_text_entry(
                topic="Writing",
                content="Write simply.",
                description="Guidance on clearer prose.",
                source="",
                note="",
                tags=["foo", "bar"],
                date_added="2026-04-08",
                entry_id="20260408-a1f3c9",
            )
        )
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr("sys.argv", ["search.py", "--tags", "foo,,bar"])
    search.main()
    output = capsys.readouterr().out

    assert "Tags [foo, bar]: 1 results" in output
