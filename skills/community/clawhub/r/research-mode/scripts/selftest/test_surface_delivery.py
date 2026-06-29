"""Unit tests for research_mode_surface_delivery: channel formatting, splitting, strategy."""
from __future__ import annotations

from pathlib import Path

from .helpers import assert_eq, assert_in, assert_true

from research_mode_surface_delivery import (
    DELIVERY_NOTIFICATION_ERROR,
    classify_delivery_error,
    format_for_channel,
    get_channel_limits,
    get_channel_profile,
    needs_splitting,
    split_for_channel,
    suggest_channel_strategy,
)


def test_delivery_error_text_does_not_infer_addressing_failure(root: Path) -> None:
    assert_eq(
        classify_delivery_error("thread timeout while sending"),
        DELIVERY_NOTIFICATION_ERROR,
        "provider error text should not infer addressing failure",
    )


def test_format_delivery_telegram_short(root: Path) -> None:
    """Short content for Telegram should not be split."""
    result = format_for_channel("Hello world", "telegram")
    assert_eq(result["channel"], "telegram", "channel should be telegram")
    assert_eq(result["strategy"], "summary_first", "telegram strategy should be summary_first")
    assert_eq(result["needs_splitting"], False, "short content should not need splitting")
    assert_eq(result["chunk_count"], 1, "short content should be a single chunk")
    assert_eq(result["chunks"], ["Hello world"], "chunk should contain original content")


def test_format_delivery_telegram_with_summary(root: Path) -> None:
    """Summary should be included for summary_first channels."""
    result = format_for_channel("Report body", "telegram", summary="Key takeaway")
    assert_in("summary", result, "result should contain summary key")
    assert_eq(result["summary"], "Key takeaway", "summary should match input")
    assert_eq(result["has_summary"], True, "has_summary should be True")


def test_format_delivery_mattermost_with_summary(root: Path) -> None:
    """Mattermost should behave like a chat surface with summary-first delivery."""
    result = format_for_channel("Report body", "mattermost", summary="Key takeaway")
    assert_eq(result["channel"], "mattermost", "channel should be mattermost")
    assert_eq(result["strategy"], "summary_first", "mattermost strategy should be summary_first")
    assert_in("summary", result, "mattermost should include summary")
    assert_eq(result["summary"], "Key takeaway", "summary should match input")


def test_format_delivery_email_ignores_summary(root: Path) -> None:
    """Email strategy is report_first — summary should NOT be injected."""
    result = format_for_channel("Report body", "email", summary="Key takeaway")
    assert_true("summary" not in result, "email should not include summary (report_first)")
    assert_eq(result["strategy"], "report_first", "email strategy should be report_first")


def test_format_delivery_with_deliverable_path(root: Path) -> None:
    """deliverable_path should produce a delivery_hint."""
    result = format_for_channel("Content", "file", deliverable_path="/tmp/report.pdf")
    assert_eq(result["deliverable_path"], "/tmp/report.pdf", "path should be preserved")
    assert_in("See attached", result["delivery_hint"], "hint should mention attachment")


def test_format_delivery_unknown_channel_fallback(root: Path) -> None:
    """Unknown channel should fall back to 'file' profile."""
    result = format_for_channel("Content", "whatsapp")
    assert_eq(result["strategy"], "file_first", "unknown channel should use file_first strategy")


def test_needs_splitting_telegram_long(root: Path) -> None:
    """Content exceeding 4096 chars should need splitting on Telegram."""
    long_content = "x" * 5000
    assert_eq(needs_splitting(long_content, "telegram"), True, "5000 chars > 4096 limit")


def test_needs_splitting_email_never(root: Path) -> None:
    """Email has no char limit — should never need splitting."""
    assert_eq(needs_splitting("x" * 100000, "email"), False, "email has no char limit")


def test_split_for_channel_telegram(root: Path) -> None:
    """Long content should be split into multiple chunks for Telegram."""
    lines = [f"Line {i}: some content here" for i in range(200)]
    content = "\n".join(lines)
    chunks = split_for_channel(content, "telegram")
    assert_true(len(chunks) > 1, "long content should produce multiple chunks")
    for chunk in chunks[:-1]:
        if "[...]" not in chunk:
            assert_true(len(chunk) <= 4096, f"chunk should not exceed 4096 chars, got {len(chunk)}")


def test_split_for_channel_long_single_line(root: Path) -> None:
    """A single oversized line should still be split below the channel limit."""
    content = "x" * 5000
    chunks = split_for_channel(content, "mattermost")
    assert_true(len(chunks) > 1, "long single line should split into multiple chunks")
    for chunk in chunks:
        assert_true(
            len(chunk) <= 4000,
            f"mattermost chunk should not exceed 4000 chars, got {len(chunk)}",
        )


def test_split_for_channel_truncation(root: Path) -> None:
    """Chunks exceeding max_inline_items should be truncated."""
    lines = [f"Line {i}: " + "x" * 180 for i in range(500)]
    content = "\n".join(lines)
    chunks = split_for_channel(content, "telegram")
    assert_true(
        any("[...]" in c for c in chunks),
        "should contain a truncation marker when content exceeds inline items limit",
    )


def test_split_for_channel_no_limit(root: Path) -> None:
    """Email (no char limit) should return content as single chunk."""
    content = "x" * 100000
    chunks = split_for_channel(content, "email")
    assert_eq(len(chunks), 1, "email should not split")


def test_suggest_channel_strategy_does_not_parse_deliverable_text(root: Path) -> None:
    """Free-text deliverable descriptions should not choose delivery strategy."""
    assert_eq(
        suggest_channel_strategy("short memo"),
        "file_first",
        "free text should not imply summary_first",
    )
    assert_eq(
        suggest_channel_strategy("краткая записка"),
        "file_first",
        "localized free text should not imply summary_first",
    )
    assert_eq(suggest_channel_strategy("full report"), "file_first", "report -> file_first")


def test_suggest_channel_strategy_none(root: Path) -> None:
    """None deliverable should default to file_first."""
    assert_eq(suggest_channel_strategy(None), "file_first", "None -> file_first")


def test_suggest_channel_strategy_unknown(root: Path) -> None:
    """Unrecognized deliverable should default to file_first."""
    assert_eq(suggest_channel_strategy("something random"), "file_first", "unknown -> file_first")


def test_get_channel_profile_known(root: Path) -> None:
    """Known channels should return their profiles."""
    profile = get_channel_profile("discord")
    assert_eq(profile["strategy"], "summary_first", "discord strategy")
    assert_true(len(profile["recommendations"]) > 0, "should have recommendations")


def test_get_channel_limits_discord(root: Path) -> None:
    """Discord should have 2000 char limit."""
    limits = get_channel_limits("discord")
    assert_eq(limits["message_chars"], 2000, "discord message limit")
    assert_eq(limits["max_inline_items"], 15, "discord max inline items")


def test_get_channel_limits_mattermost(root: Path) -> None:
    """Mattermost should have a chat-sized inline limit."""
    limits = get_channel_limits("mattermost")
    assert_eq(limits["message_chars"], 4000, "mattermost message limit")
    assert_eq(limits["summary_first"], True, "mattermost should prefer summary-first")


def test_format_delivery_summary_truncated(root: Path) -> None:
    """Summary longer than 500 chars should be truncated."""
    long_summary = "A" * 600
    result = format_for_channel("Body", "telegram", summary=long_summary)
    assert_eq(len(result["summary"]), 500, "summary should be capped at 500 chars")
