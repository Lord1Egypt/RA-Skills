from __future__ import annotations

from robin.index import rebuild_index
from robin.parser import SEPARATOR, load_all_entries
from robin.serializer import build_text_entry, serialize_entry


def test_reindex_preserves_legacy_review_state(robin_env):
    topic_file = robin_env["topics_dir"] / "ai-reasoning.md"
    topic_file.write_text(
        SEPARATOR.join(
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

    old_index = {
        "items": {
            "ai-reasoning:2026-04-08:001": {
                "rating": 2,
                "last_surfaced": "2026-04-01T10:00:00+00:00",
                "times_surfaced": 4,
            },
            "ai-reasoning:2026-04-08:002": {
                "rating": 5,
                "last_surfaced": None,
                "times_surfaced": 1,
            },
        },
    }

    rebuilt = rebuild_index(
        load_all_entries({"topics_dir": "topics"}, str(robin_env["state_dir"])),
        old_index,
    )

    assert rebuilt["items"]["20260408-a1f3c9"]["rating"] == 2
    assert rebuilt["items"]["20260408-a1f3c9"]["times_surfaced"] == 4
    assert rebuilt["items"]["20260408-b7k2d1"]["rating"] == 5


def test_reindex_preserves_awaiting_rating_state(robin_env):
    topic_file = robin_env["topics_dir"] / "ai-reasoning.md"
    topic_file.write_text(
        serialize_entry(
            build_text_entry(
                topic="AI Reasoning",
                content="Entry.",
                description="Description.",
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

    old_index = {
        "items": {
            "20260408-a1f3c9": {
                "id": "20260408-a1f3c9",
                "topic": "ai-reasoning",
                "date": "2026-04-08",
                "rating": None,
                "last_surfaced": "2026-04-01T10:00:00+00:00",
                "times_surfaced": 1,
                "_awaiting_rating": True,
            }
        },
    }

    rebuilt = rebuild_index(
        load_all_entries({"topics_dir": "topics"}, str(robin_env["state_dir"])),
        old_index,
    )

    assert rebuilt["items"]["20260408-a1f3c9"]["_awaiting_rating"] is True
