from __future__ import annotations

import pytest

from robin.parser import RobinEntryParseError, load_topic_entries, parse_entry, topic_to_filename
from robin.serializer import build_media_entry, build_text_entry, generate_entry_id, serialize_entry


def test_serialize_and_parse_round_trip():
    entry = build_text_entry(
        topic="AI Reasoning",
        content="Clear thinking beats ornament.",
        description="A short reminder about valuing clarity over ornate phrasing. Useful when reviewing writing advice.",
        source="https://example.com",
        note="Keep this near writing advice.",
        tags=["writing", "clarity"],
        date_added="2026-04-08",
        entry_id="20260408-a1f3c9",
    )

    parsed = parse_entry(serialize_entry(entry), "ai-reasoning")

    assert parsed.entry_id == "20260408-a1f3c9"
    assert parsed.topic == "ai-reasoning"
    assert parsed.source == "https://example.com"
    assert parsed.description.startswith("A short reminder")
    assert parsed.tags == ["writing", "clarity"]
    assert "**Source:**" not in parsed.body
    assert "Robin note" in parsed.body


def test_parse_media_entry_round_trip():
    entry = build_media_entry(
        topic="Poetry",
        media_kind="image",
        media_source="media/poetry/20260408-a1f3c9.png",
        description="A photographed poem excerpt worth revisiting for tone and imagery.",
        creator="Mary Oliver",
        published_at="1986",
        summary="An excerpt about attention and observation in everyday life.",
        content="Opening lines from the photographed page.",
        source="",
        note="Useful for later reflection.",
        tags=["poetry"],
        date_added="2026-04-08",
        entry_id="20260408-a1f3c9",
    )

    parsed = parse_entry(serialize_entry(entry), "poetry")

    assert parsed.entry_type == "image"
    assert parsed.media_source == "media/poetry/20260408-a1f3c9.png"
    assert parsed.creator == "Mary Oliver"
    assert parsed.summary.startswith("An excerpt")


def test_parse_text_entry_with_attached_image_round_trip():
    entry = build_text_entry(
        topic="Wisdom",
        content="Filed this screenshot to wisdom.",
        description="A text note with a local screenshot attached for later context.",
        source="",
        note="",
        tags=["screenshot"],
        date_added="2026-04-08",
        media_source="media/wisdom/20260408-a1f3c9.png",
        entry_id="20260408-a1f3c9",
    )

    parsed = parse_entry(serialize_entry(entry), "wisdom")

    assert parsed.entry_type == "text"
    assert parsed.media_kind == ""
    assert parsed.media_source == "media/wisdom/20260408-a1f3c9.png"
    assert parsed.body == "Filed this screenshot to wisdom."


def test_parse_entry_generates_legacy_fallback_id():
    parsed = parse_entry(
        "date_added: 2026-04-08\nsource: \ndescription: Legacy entry without explicit id.\ntags: [notes]\n\nSomething worth keeping.",
        "notes",
    )

    assert parsed.entry_id.startswith("legacy-")
    assert parsed.date_added == "2026-04-08"


def test_topic_to_filename_sanitizes_special_characters():
    assert topic_to_filename("AI/ML Concepts") == "ai-ml-concepts.md"
    assert topic_to_filename("  :::  ") == "untitled.md"


def test_generate_entry_id_uses_six_hex_suffix():
    entry_id = generate_entry_id("2026-04-08")

    assert entry_id.startswith("20260408-")
    assert len(entry_id.split("-", 1)[1]) == 6


def test_serialize_entry_skips_empty_optional_fields():
    entry = build_text_entry(
        topic="Notes",
        content="Something worth keeping.",
        description="Context for later review.",
        source="",
        note="",
        tags=[],
        date_added="2026-04-08",
        entry_id="20260408-a1f3c9",
    )

    serialized = serialize_entry(entry)

    assert "entry_type:" not in serialized
    assert "media_kind:" not in serialized
    assert "media_source:" not in serialized
    assert "source:" not in serialized
    assert "tags:" not in serialized


def test_load_topic_entries_reports_malformed_entry_with_file_context(tmp_path):
    topic_file = tmp_path / "bad-topic.md"
    topic_file.write_text("date_added 2026-04-08\n\nBroken entry", encoding="utf-8")

    with pytest.raises(RobinEntryParseError, match="bad-topic.md"):
        load_topic_entries(topic_file)
