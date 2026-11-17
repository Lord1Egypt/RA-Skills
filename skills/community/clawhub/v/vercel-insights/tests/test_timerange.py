"""Tests for vercel_insights/timerange.py."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from helpers import NOW, utc

from vercel_insights import ConfigError
from vercel_insights import timerange as tr


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("30m", NOW - timedelta(minutes=30)),
        ("24h", NOW - timedelta(hours=24)),
        ("7d", NOW - timedelta(days=7)),
        ("4w", NOW - timedelta(weeks=4)),
        ("7D", NOW - timedelta(days=7)),
        ("now", NOW),
        ("NOW", NOW),
        ("today", utc(2026, 8, 14)),
        ("yesterday", utc(2026, 8, 13)),
        ("2026-08-01", utc(2026, 8, 1)),
        ("2026-08-01T12:00:00Z", utc(2026, 8, 1, 12)),
        ("2026-08-01T12:00:00z", utc(2026, 8, 1, 12)),
        ("2026-08-01T12:00:00+02:00", utc(2026, 8, 1, 10)),
        ("2026-08-01T12:00:00-05:00", utc(2026, 8, 1, 17)),
        ("2026-08-01T12:00:00", utc(2026, 8, 1, 12)),
        ("1700000000000", utc(2023, 11, 14, 22, 13, 20)),
    ],
    ids=lambda value: value if isinstance(value, str) else "",
)
def test_parse_time_value_accepts_every_documented_format(
    value: str, expected: datetime
) -> None:
    parsed = tr.parse_time_value(value, NOW)
    assert parsed == expected
    assert parsed.tzinfo is not None
    assert parsed.utcoffset() == timedelta(0)


@pytest.mark.parametrize(
    "value",
    ["", "   ", "banana", "7x", "d7", "2026-13-01", "next tuesday", "--since", "1e9"],
)
def test_parse_time_value_rejects_garbage_with_a_config_error(value: str) -> None:
    with pytest.raises(ConfigError) as excinfo:
        tr.parse_time_value(value, NOW)
    assert "time value" in str(excinfo.value)


def test_parse_time_value_tells_unix_seconds_apart_from_milliseconds() -> None:
    with pytest.raises(ConfigError) as excinfo:
        tr.parse_time_value("1700000000", NOW)
    message = str(excinfo.value)
    assert "millisecond" in message
    assert "1700000000000" in message


def test_to_api_timestamp_renders_utc_with_a_z_suffix() -> None:
    assert tr.to_api_timestamp(utc(2026, 8, 1, 12, 30, 45)) == "2026-08-01T12:30:45Z"


def test_to_api_timestamp_converts_a_non_utc_offset_to_utc() -> None:
    aware = datetime(2026, 8, 1, 12, tzinfo=timezone(timedelta(hours=2)))
    assert tr.to_api_timestamp(aware) == "2026-08-01T10:00:00Z"


def test_resolve_range_returns_both_ends_in_order() -> None:
    start, end = tr.resolve_range("7d", "now", NOW)
    assert start == NOW - timedelta(days=7)
    assert end == NOW


@pytest.mark.parametrize(
    ("since", "until"),
    [("now", "7d"), ("now", "now"), ("2026-08-02", "2026-08-01")],
)
def test_resolve_range_requires_since_strictly_before_until(
    since: str, until: str
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        tr.resolve_range(since, until, NOW)
    message = str(excinfo.value)
    assert "--since must be strictly earlier than --until" in message
    assert "--since 7d --until now" in message


def test_reporting_window_warns_only_beyond_twenty_four_months() -> None:
    assert tr.reporting_window_warning(NOW - timedelta(days=400), NOW) is None
    warning = tr.reporting_window_warning(NOW - timedelta(days=900), NOW)
    assert warning is not None
    assert "reporting window" in warning


@pytest.mark.parametrize(
    "value", ["99999999999999999", "253402300800000", "99999999999999999999999"]
)
def test_an_out_of_range_unix_millisecond_value_is_a_config_error(value: str) -> None:
    with pytest.raises(ConfigError) as excinfo:
        tr.parse_time_value(value, NOW)
    message = str(excinfo.value)
    assert "outside the representable range" in message
    assert str(tr.MAX_UNIX_MS) in message


def test_the_largest_representable_unix_millisecond_value_still_parses() -> None:
    parsed = tr.parse_time_value(str(tr.MAX_UNIX_MS), NOW)
    assert parsed.year == 9999


def test_to_unix_ms_renders_milliseconds_as_a_string() -> None:
    # The request-logs API takes startDate and endDate in Unix milliseconds,
    # and every query parameter this client sends is a string.
    assert tr.to_unix_ms(datetime(1970, 1, 1, tzinfo=timezone.utc)) == "0"
    assert tr.to_unix_ms(utc(2026, 8, 17, 11, 6, 8)) == "1786964768000"


def test_to_unix_ms_assumes_utc_for_a_naive_datetime() -> None:
    naive = datetime(2026, 8, 17, 11, 6, 8)
    assert tr.to_unix_ms(naive) == tr.to_unix_ms(utc(2026, 8, 17, 11, 6, 8))


def test_the_logs_surface_has_a_name_and_a_label() -> None:
    assert tr.LOGS in tr.SURFACES
    assert tr.SURFACE_LABELS[tr.LOGS] == "request logs"
