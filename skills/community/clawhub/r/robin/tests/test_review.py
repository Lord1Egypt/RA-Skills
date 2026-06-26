from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from robin.config import load_index, save_index
from robin.parser import SEPARATOR, load_all_entries
from robin.review_logic import parse_timestamp, pick_best_candidate, rate_item
from robin.serializer import build_media_entry, build_text_entry, serialize_entry
from scripts import review


def _save_review_entry(robin_env, filename: str, entry) -> None:
    topic_file = robin_env["topics_dir"] / filename
    topic_file.write_text(serialize_entry(entry) + "\n", encoding="utf-8")
    save_index(
        {
            "items": {
                entry.entry_id: {
                    "id": entry.entry_id,
                    "topic": entry.topic,
                    "date": entry.date_added,
                    "rating": None,
                    "last_surfaced": None,
                    "times_surfaced": 0,
                }
            }
        }
    )


def test_review_uses_entry_ids_for_same_day_duplicates(robin_env):
    topic_file = robin_env["topics_dir"] / "ai-reasoning.md"
    topic_file.write_text(
        f"{SEPARATOR}".join(
            [
                serialize_entry(
                    build_text_entry(
                        topic="AI Reasoning",
                        content="First entry.",
                        description="First description.",
                        source="",
                        note="",
                        tags=["writing"],
                        date_added="2026-04-08",
                        entry_id="20260408-a1f3c9",
                    )
                ),
                serialize_entry(
                    build_text_entry(
                        topic="AI Reasoning",
                        content="Second entry.",
                        description="Second description.",
                        source="",
                        note="",
                        tags=["writing"],
                        date_added="2026-04-08",
                        entry_id="20260408-b7k2d1",
                    )
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    now = datetime.now(timezone.utc).isoformat()
    index = {
        "items": {
            "20260408-a1f3c9": {
                "id": "20260408-a1f3c9",
                "topic": "ai-reasoning",
                "date": "2026-04-08",
                "rating": None,
                "last_surfaced": now,
                "times_surfaced": 1,
            },
            "20260408-b7k2d1": {
                "id": "20260408-b7k2d1",
                "topic": "ai-reasoning",
                "date": "2026-04-08",
                "rating": None,
                "last_surfaced": None,
                "times_surfaced": 0,
            },
        },
    }
    save_index(index)

    candidate = pick_best_candidate(
        load_index(),
        load_all_entries(json.loads((robin_env["state_dir"] / "robin-config.json").read_text(encoding="utf-8")), str(robin_env["state_dir"])),
        {"review_cooldown_days": 60},
    )
    assert candidate is not None
    _, entry = candidate
    assert entry.entry_id == "20260408-b7k2d1"
    assert entry.description == "Second description."
    assert entry.body == "Second entry."


def test_review_surfaces_media_metadata(robin_env):
    topic_file = robin_env["topics_dir"] / "poetry.md"
    topic_file.write_text(
        serialize_entry(
            build_media_entry(
                topic="Poetry",
                media_kind="image",
                media_source="media/poetry/20260408-a1f3c9.png",
                description="A photographed excerpt to revisit.",
                creator="Mary Oliver",
                published_at="1986",
                summary="An excerpt about attention and observation.",
                content="Opening lines from the page.",
                source="",
                note="",
                tags=["poetry"],
                date_added="2026-04-08",
                entry_id="20260408-a1f3c9",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    index = {
        "items": {
            "20260408-a1f3c9": {
                "id": "20260408-a1f3c9",
                "topic": "poetry",
                "date": "2026-04-08",
                "rating": None,
                "last_surfaced": None,
                "times_surfaced": 0,
            }
        },
    }
    save_index(index)

    candidate = pick_best_candidate(
        load_index(),
        load_all_entries(json.loads((robin_env["state_dir"] / "robin-config.json").read_text(encoding="utf-8")), str(robin_env["state_dir"])),
        {"review_cooldown_days": 60},
    )
    assert candidate is not None
    _, entry = candidate
    assert entry.entry_type == "image"
    assert entry.media_source == "media/poetry/20260408-a1f3c9.png"
    assert entry.creator == "Mary Oliver"
    assert entry.summary.startswith("An excerpt")


def test_review_text_output_includes_source(robin_env, monkeypatch, capsys):
    _save_review_entry(
        robin_env,
        "writing.md",
        build_text_entry(
            topic="Writing",
            content="Write as if speaking to a smart friend.",
            description="Writing advice.",
            source="https://example.com/article",
            note="",
            tags=["writing"],
            date_added="2026-04-08",
            entry_id="20260408-a1f3c9",
        ),
    )

    monkeypatch.setattr("sys.argv", ["review.py"])
    review.main()
    output = capsys.readouterr().out

    assert "📚 Robin Recall" in output
    assert "Topic: writing" in output
    assert "Type: text" in output
    assert "Source: https://example.com/article" in output
    assert "Creator: Not provided" in output
    assert "Saved on: 2026-04-08" in output
    assert "Description:\nWriting advice." in output
    assert "Body:\nWrite as if speaking to a smart friend." in output
    assert "Rate it" not in output
    assert "How well do you remember" not in output
    assert "To rate" not in output


def test_review_recall_text_output_uses_media_source_when_source_missing(robin_env, monkeypatch, capsys):
    _save_review_entry(
        robin_env,
        "poetry.md",
        build_media_entry(
            topic="Poetry",
            media_kind="image",
            media_source="media/poetry/20260408-a1f3c9.png",
            description="A photographed excerpt to revisit.",
            creator="Mary Oliver",
            published_at="1986",
            summary="An excerpt about attention and observation.",
            content="Opening lines from the page.",
            source="",
            note="",
            tags=["poetry"],
            date_added="2026-04-08",
            entry_id="20260408-a1f3c9",
        ),
    )

    monkeypatch.setattr("sys.argv", ["review.py"])
    review.main()
    output = capsys.readouterr().out

    assert "📚 Robin Recall" in output
    assert "Topic: poetry" in output
    assert "Type: image" in output
    assert "Source: media/poetry/20260408-a1f3c9.png" in output
    assert "Creator: Mary Oliver" in output
    assert "Saved on: 2026-04-08" in output
    assert "Description:\nA photographed excerpt to revisit." in output
    assert "Body:\nOpening lines from the page." in output
    assert "Rate it" not in output
    assert "To rate" not in output


def test_review_recall_text_output_is_consistent_for_video(robin_env, monkeypatch, capsys):
    _save_review_entry(
        robin_env,
        "public-speaking.md",
        build_media_entry(
            topic="Public Speaking",
            media_kind="video",
            media_source="https://www.youtube.com/watch?v=abc123",
            description="Patrick Winston's classic MIT lecture on How to Speak.",
            creator="Patrick Winston (MIT)",
            published_at="1970",
            summary="A lecture about effective technical speaking.",
            content="Start with an empowerment promise, not a joke.",
            source="Patrick Winston -- How to Speak (YouTube)",
            note="",
            tags=["speaking"],
            date_added="2026-04-11",
            entry_id="20260411-003b06",
        ),
    )

    monkeypatch.setattr("sys.argv", ["review.py"])
    review.main()
    output = capsys.readouterr().out

    assert "📚 Robin Recall" in output
    assert "Topic: public-speaking" in output
    assert "Type: video" in output
    assert "Source: Patrick Winston -- How to Speak (YouTube)" in output
    assert "Creator: Patrick Winston (MIT)" in output
    assert "Saved on: 2026-04-11" in output
    assert "Description:\nPatrick Winston's classic MIT lecture on How to Speak." in output
    assert "Body:\nStart with an empowerment promise, not a joke." in output
    assert "Rate it" not in output
    assert "How well do you remember" not in output
    assert "To rate" not in output


def test_rate_item_writes_parseable_timestamp(robin_env):
    index = load_index()
    index["items"]["20260408-a1f3c9"] = {
        "id": "20260408-a1f3c9",
        "topic": "ai-reasoning",
        "date": "2026-04-08",
        "rating": None,
        "last_surfaced": None,
        "times_surfaced": 0,
    }

    item = rate_item(index, "20260408-a1f3c9", 5)
    parsed = parse_timestamp(item["last_surfaced"])

    assert parsed.tzinfo is not None
    assert item["times_surfaced"] == 1
    assert item["rating"] == 5


def test_scheduled_recall_marks_item_surfaced_without_awaiting_rating(robin_env, monkeypatch, capsys):
    topic_file = robin_env["topics_dir"] / "ai-reasoning.md"
    topic_file.write_text(
        serialize_entry(
            build_text_entry(
                topic="AI Reasoning",
                content="Only entry.",
                description="Only description.",
                source="",
                note="",
                tags=["writing"],
                date_added="2026-04-08",
                entry_id="20260408-a1f3c9",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    save_index(
        {
            "items": {
                "20260408-a1f3c9": {
                    "id": "20260408-a1f3c9",
                    "topic": "ai-reasoning",
                    "date": "2026-04-08",
                    "rating": None,
                    "last_surfaced": None,
                    "times_surfaced": 0,
                }
            }
        }
    )

    monkeypatch.setattr("sys.argv", ["review.py"])
    review.main()
    capsys.readouterr()

    item = load_index()["items"]["20260408-a1f3c9"]
    assert item["last_surfaced"] is not None
    assert item["times_surfaced"] == 1
    assert item["_awaiting_rating"] is False


def test_active_review_marks_item_awaiting_rating(robin_env, monkeypatch, capsys):
    topic_file = robin_env["topics_dir"] / "ai-reasoning.md"
    topic_file.write_text(
        serialize_entry(
            build_text_entry(
                topic="AI Reasoning",
                content="Only entry.",
                description="Only description.",
                source="",
                note="",
                tags=["writing"],
                date_added="2026-04-08",
                entry_id="20260408-a1f3c9",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    save_index(
        {
            "items": {
                "20260408-a1f3c9": {
                    "id": "20260408-a1f3c9",
                    "topic": "ai-reasoning",
                    "date": "2026-04-08",
                    "rating": None,
                    "last_surfaced": None,
                    "times_surfaced": 0,
                }
            }
        }
    )

    monkeypatch.setattr("sys.argv", ["review.py", "--active-review"])
    review.main()
    capsys.readouterr()

    item = load_index()["items"]["20260408-a1f3c9"]
    assert item["last_surfaced"] is not None
    assert item["times_surfaced"] == 1
    assert item["_awaiting_rating"] is True


def test_rate_after_surface_does_not_increment_times_surfaced_twice(robin_env, monkeypatch, capsys):
    topic_file = robin_env["topics_dir"] / "ai-reasoning.md"
    topic_file.write_text(
        serialize_entry(
            build_text_entry(
                topic="AI Reasoning",
                content="Only entry.",
                description="Only description.",
                source="",
                note="",
                tags=["writing"],
                date_added="2026-04-08",
                entry_id="20260408-a1f3c9",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    save_index(
        {
            "items": {
                "20260408-a1f3c9": {
                    "id": "20260408-a1f3c9",
                    "topic": "ai-reasoning",
                    "date": "2026-04-08",
                    "rating": None,
                    "last_surfaced": None,
                    "times_surfaced": 0,
                }
            }
        }
    )

    monkeypatch.setattr("sys.argv", ["review.py", "--active-review"])
    review.main()
    capsys.readouterr()

    monkeypatch.setattr("sys.argv", ["review.py", "--rate", "20260408-a1f3c9", "5"])
    review.main()
    capsys.readouterr()

    item = load_index()["items"]["20260408-a1f3c9"]
    assert item["rating"] == 5
    assert item["times_surfaced"] == 1
    assert item["_awaiting_rating"] is False


def test_review_rejects_non_numeric_rating(robin_env, monkeypatch, capsys):
    index = load_index()
    index["items"]["20260408-a1f3c9"] = {
        "id": "20260408-a1f3c9",
        "topic": "ai-reasoning",
        "date": "2026-04-08",
        "rating": None,
        "last_surfaced": None,
        "times_surfaced": 0,
    }
    save_index(index)

    monkeypatch.setattr("sys.argv", ["review.py", "--rate", "20260408-a1f3c9", "abc"])

    try:
        review.main()
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("Expected SystemExit for invalid rating")

    assert "Rating must be a number between 1 and 5." in capsys.readouterr().out


def test_review_json_rejects_non_numeric_rating(robin_env, monkeypatch, capsys):
    index = load_index()
    index["items"]["20260408-a1f3c9"] = {
        "id": "20260408-a1f3c9",
        "topic": "ai-reasoning",
        "date": "2026-04-08",
        "rating": None,
        "last_surfaced": None,
        "times_surfaced": 0,
    }
    save_index(index)

    monkeypatch.setattr("sys.argv", ["review.py", "--rate", "20260408-a1f3c9", "abc", "--json"])

    with pytest.raises(SystemExit) as exc:
        review.main()

    assert exc.value.code == 1
    output = json.loads(capsys.readouterr().out)
    assert output["error"] == "Rating must be a number between 1 and 5."


def test_review_json_rejects_invalid_index_timestamp(robin_env, monkeypatch, capsys):
    topic_file = robin_env["topics_dir"] / "ai-reasoning.md"
    topic_file.write_text(
        serialize_entry(
            build_text_entry(
                topic="AI Reasoning",
                content="Only entry.",
                description="Only description.",
                source="",
                note="",
                tags=["writing"],
                date_added="2026-04-08",
                entry_id="20260408-a1f3c9",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    save_index(
        {
            "items": {
                "20260408-a1f3c9": {
                    "id": "20260408-a1f3c9",
                    "topic": "ai-reasoning",
                    "date": "2026-04-08",
                    "rating": None,
                    "last_surfaced": "not-a-timestamp",
                    "times_surfaced": 1,
                }
            }
        }
    )

    monkeypatch.setattr("sys.argv", ["review.py", "--json"])

    with pytest.raises(SystemExit) as exc:
        review.main()

    assert exc.value.code == 1
    output = json.loads(capsys.readouterr().out)
    assert "invalid timestamp" in output["error"].lower()


def test_review_json_skips_when_not_enough_items(robin_env, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["review.py", "--json"])
    review.main()
    output = json.loads(capsys.readouterr().out)

    assert output["status"] == "skip"
    assert output["reason"] == "not_enough_items"
    assert output["total_items"] == 0


def test_review_json_skips_when_no_eligible_items(robin_env, monkeypatch, capsys):
    topic_file = robin_env["topics_dir"] / "ai-reasoning.md"
    topic_file.write_text(
        serialize_entry(
            build_text_entry(
                topic="AI Reasoning",
                content="Only entry.",
                description="Only description.",
                source="",
                note="",
                tags=["writing"],
                date_added="2026-04-08",
                entry_id="20260408-a1f3c9",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    now = datetime.now(timezone.utc).isoformat()
    save_index(
        {
            "items": {
                "20260408-a1f3c9": {
                    "id": "20260408-a1f3c9",
                    "topic": "ai-reasoning",
                    "date": "2026-04-08",
                    "rating": None,
                    "last_surfaced": now,
                    "times_surfaced": 1,
                }
            }
        }
    )

    monkeypatch.setattr("sys.argv", ["review.py", "--json"])
    review.main()
    output = json.loads(capsys.readouterr().out)

    assert output["status"] == "skip"
    assert output["reason"] == "no_eligible_items"
