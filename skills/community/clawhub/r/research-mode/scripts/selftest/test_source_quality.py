from __future__ import annotations

from research_mode_lifecycle_helpers import compute_source_quality_score


def test_source_quality_does_not_use_title_or_note_keywords() -> None:
    source = {
        "url": "https://example.com/post",
        "title": "official government report",
        "note": "verified primary source",
    }

    result = compute_source_quality_score(source)

    assert result["factors"] == []
    assert result["quality_score"] == 0.5


def test_source_quality_does_not_infer_authority_from_domain_or_tags() -> None:
    source = {
        "url": "https://agency.gov/report",
        "tags": ["official_source", "primary_source"],
    }

    result = compute_source_quality_score(source)

    assert result["factors"] == []
    assert result["quality_score"] == 0.5


def test_source_quality_does_not_penalize_hosts_or_tags() -> None:
    source = {
        "url": "https://reddit.com/r/test",
        "tags": ["user_generated", "stale", "unverified"],
    }

    result = compute_source_quality_score(source)

    assert result["factors"] == []
    assert result["quality_score"] == 0.5


def test_source_quality_ignores_uncontrolled_tag_text() -> None:
    source = {
        "url": "https://example.com/report",
        "tags": ["this says verified but is not a controlled tag"],
    }

    result = compute_source_quality_score(source)

    assert result["factors"] == []


def test_source_quality_uses_only_fetch_timestamp() -> None:
    fresh = compute_source_quality_score({
        "url": "https://example.com/report",
        "fetched_at": "2999-01-01T00:00:00Z",
    })
    old = compute_source_quality_score({
        "url": "https://example.com/report",
        "fetched_at": "2020-01-01T00:00:00Z",
    })

    assert fresh["factors"] == ["fresh_30d"]
    assert old["factors"] == ["stale_over_1yr"]
