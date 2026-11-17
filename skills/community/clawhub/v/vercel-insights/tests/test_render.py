"""Tests for vercel_insights/render.py: tables, JSON, CSV and the overview."""

from __future__ import annotations

import csv
import io
import json

import pytest
from helpers import (
    ANSI_CAMPAIGN,
    CONTROL_CHARACTER_CAMPAIGN_PAYLOAD,
    COUNTRY_PAYLOAD,
    COUNTRY_WITH_OTHERS_PAYLOAD,
    DAILY_PAYLOAD,
    ESCAPED_ANSI_CAMPAIGN,
    ESCAPED_C1_CAMPAIGN,
    EVENTS_COUNT_PAYLOAD,
    PROJECT,
    REFERRERS_PAYLOAD,
    TIME_ONLY_OTHERS_PAYLOAD,
    TOP_PAGES_PAYLOAD,
    TWO_DIMENSION_PAYLOAD,
    TWO_DIMENSIONS,
    UNICODE_CAMPAIGN,
    VISITS_COUNT_PAYLOAD,
    utc,
)

from vercel_insights import sanitize_label
from vercel_insights.render import (
    Result,
    format_csv,
    format_json,
    format_table,
    render_overview,
    stringify_label,
)
from vercel_insights.webanalytics import normalize


def test_format_table_shows_groups_shares_and_a_totals_row() -> None:
    result = normalize(COUNTRY_PAYLOAD, "visits", ["country"])
    text = format_table(
        result,
        time_range=(utc(2026, 8, 7), utc(2026, 8, 14)),
        filter_expr="country in ('US', 'DE')",
        limit=10,
    )
    assert "Range: 2026-08-07T00:00:00Z to 2026-08-14T00:00:00Z (UTC)" in text
    assert "Filter: country in ('US', 'DE')" in text
    assert "country" in text and "pageviews" in text and "% pageviews" in text
    assert "US" in text and "640" in text and "510" in text
    assert "78.0%" in text
    assert "TOTAL" in text and "820" in text and "100.0%" in text


def test_format_table_renders_time_buckets_at_day_precision() -> None:
    result = normalize(DAILY_PAYLOAD, "visits", ["day"])
    text = format_table(result)
    assert "2024-10-01" in text
    assert "T00:00:00.000Z" not in text
    assert "220" in text and "245" in text
    assert "465" in text


def test_format_table_annotates_the_others_row_as_the_limit_overflow() -> None:
    result = normalize(COUNTRY_WITH_OTHERS_PAYLOAD, "visits", ["country"])
    text = format_table(result, limit=2)
    assert "Others" in text
    assert "is not a real value" in text
    assert "--limit 2" in text


def test_format_table_renders_a_count_as_a_labelled_block() -> None:
    result = normalize(VISITS_COUNT_PAYLOAD, "visits", [])
    text = format_table(result, time_range=(utc(2026, 8, 7), utc(2026, 8, 14)))
    assert "Range: 2026-08-07T00:00:00Z" in text
    assert "pageviews" in text and "1,250" in text
    assert "visitors" in text and "980" in text
    assert "TOTAL" not in text


def test_format_json_carries_query_range_rows_totals_and_the_raw_payload() -> None:
    result = normalize(COUNTRY_PAYLOAD, "visits", ["country"])
    document = json.loads(
        format_json(
            result, COUNTRY_PAYLOAD, time_range=(utc(2026, 8, 7), utc(2026, 8, 14))
        )
    )
    assert document["query"] == COUNTRY_PAYLOAD["query"]
    assert document["range"] == {
        "since": "2026-08-07T00:00:00Z",
        "until": "2026-08-14T00:00:00Z",
    }
    assert document["rows"][0] == {
        "key": "US",
        "groups": {"country": "US"},
        "timestamp": None,
        "metrics": {"pageviews": 640, "visitors": 510},
    }
    assert document["totals"] == {"pageviews": 820, "visitors": 660}
    assert document["raw"] == COUNTRY_PAYLOAD
    assert document["groupBy"] == ["country"]


def test_format_json_of_a_count_marks_it_as_a_count() -> None:
    result = normalize(VISITS_COUNT_PAYLOAD, "visits", [])
    document = json.loads(format_json(result, VISITS_COUNT_PAYLOAD))
    assert document["isCount"] is True
    assert document["rows"] == [
        {
            "key": None,
            "groups": {},
            "timestamp": None,
            "metrics": {"pageviews": 1250, "visitors": 980},
        }
    ]
    assert document["range"] is None


def test_format_csv_of_a_grouped_result_parses_back_to_the_expected_rows() -> None:
    result = normalize(COUNTRY_PAYLOAD, "visits", ["country"])
    rows = list(csv.reader(io.StringIO(format_csv(result))))
    assert rows == [
        ["country", "pageviews", "visitors"],
        ["US", "640", "510"],
        ["DE", "180", "150"],
    ]


def test_format_csv_of_a_time_grouped_result_uses_the_granularity_as_the_header() -> (
    None
):
    result = normalize(DAILY_PAYLOAD, "visits", ["day"])
    rows = list(csv.reader(io.StringIO(format_csv(result))))
    assert rows == [
        ["day", "pageviews", "visitors"],
        ["2024-10-01", "220", "180"],
        ["2024-10-02", "245", "201"],
    ]


def test_format_csv_of_a_count_writes_one_header_and_one_value_row() -> None:
    result = normalize(EVENTS_COUNT_PAYLOAD, "events", [])
    rows = list(csv.reader(io.StringIO(format_csv(result))))
    assert rows == [["count", "visitors"], ["42", "36"]]


def test_format_csv_quotes_a_label_containing_a_comma() -> None:
    payload = {
        "version": 1,
        "query": {"groupBy": ["requestPath"]},
        "data": [{"requestPath": "/a,b", "pageviews": 1, "visitors": 1}],
    }
    result = normalize(payload, "visits", ["requestPath"])
    text = format_csv(result)
    assert '"/a,b"' in text
    assert list(csv.reader(io.StringIO(text)))[1] == ["/a,b", "1", "1"]


def test_render_overview_composes_the_three_sections() -> None:
    daily = normalize(DAILY_PAYLOAD, "visits", ["day"])
    pages = normalize(TOP_PAGES_PAYLOAD, "visits", ["requestPath"])
    referrers = normalize(REFERRERS_PAYLOAD, "visits", ["referrerHostname"])
    text = render_overview(
        [daily, pages, referrers],
        project=PROJECT,
        time_range=(utc(2026, 8, 7), utc(2026, 8, 14)),
    )
    assert f"Vercel Web Analytics: {PROJECT}" in text
    assert "By day" in text
    assert "2024-10-01" in text
    assert "Top pages (top 5)" in text and "/pricing" in text
    assert "Top referrers (top 5)" in text and "news.ycombinator.com" in text


def test_a_two_dimension_grouping_renders_both_columns_in_the_table() -> None:
    result = normalize(TWO_DIMENSION_PAYLOAD, "events", TWO_DIMENSIONS)
    lines = format_table(result).splitlines()
    assert lines[0].split() == [
        "eventName",
        "eventData/plan",
        "count",
        "visitors",
        "%",
        "count",
    ]
    assert lines[2].split()[:2] == ["signup", "free"]
    assert lines[3].split()[:2] == ["signup", "pro"]
    assert lines[4].split()[:2] == ["purchase", "pro"]


def test_a_two_dimension_grouping_renders_both_columns_in_csv() -> None:
    result = normalize(TWO_DIMENSION_PAYLOAD, "events", TWO_DIMENSIONS)
    rows = list(csv.reader(io.StringIO(format_csv(result))))
    assert rows == [
        ["eventName", "eventData/plan", "count", "visitors"],
        ["signup", "free", "30", "28"],
        ["signup", "pro", "12", "11"],
        ["purchase", "pro", "3", "3"],
    ]


def test_a_two_dimension_grouping_names_both_labels_in_json_rows() -> None:
    result = normalize(TWO_DIMENSION_PAYLOAD, "events", TWO_DIMENSIONS)
    document = json.loads(format_json(result, TWO_DIMENSION_PAYLOAD))
    assert [row["groups"] for row in document["rows"]] == [
        {"eventName": "signup", "eventData/plan": "free"},
        {"eventName": "signup", "eventData/plan": "pro"},
        {"eventName": "purchase", "eventData/plan": "pro"},
    ]


def test_a_time_plus_dimension_grouping_puts_the_timestamp_column_first() -> None:
    payload = {
        "version": 1,
        "query": {"groupBy": ["day", "country"]},
        "data": [
            {
                "timestamp": "2026-08-01T00:00:00.000Z",
                "country": "US",
                "pageviews": 4,
                "visitors": 3,
            },
        ],
    }
    result = normalize(payload, "visits", ["day", "country"])
    rows = list(csv.reader(io.StringIO(format_csv(result))))
    assert rows == [
        ["day", "country", "pageviews", "visitors"],
        ["2026-08-01", "US", "4", "3"],
    ]


def test_the_others_bucket_is_visible_and_annotated_on_a_time_only_grouping() -> None:
    result = normalize(TIME_ONLY_OTHERS_PAYLOAD, "visits", ["day"])
    text = format_table(result, limit=2)
    assert "Others" in text
    assert "is not a real value" in text
    assert "--limit 2" in text
    assert "21" in text


# ---------------------------------------------------------------------------
# The untrusted input boundary
# ---------------------------------------------------------------------------
#
# A UTM campaign is whatever a visitor typed into a query string, and request
# paths, referrer hostnames, event names and routes are no better. Any of them
# can carry an ANSI escape sequence that recolours the terminal, a carriage
# return that rewrites the line already printed, or a byte that breaks a CSV
# cell open. The whole control character class is escaped rather than any one
# sequence being pattern matched.


def campaign_result() -> Result:
    return normalize(
        CONTROL_CHARACTER_CAMPAIGN_PAYLOAD, "visits", ["utmCampaign"]
    )


@pytest.mark.parametrize(
    ("raw", "escaped"),
    [
        ("\x1b[31mred", "\\x1b[31mred"),
        ("before\rafter", "before\\x0dafter"),
        ("split\nline", "split\\x0aline"),
        ("tab\there", "tab\\x09here"),
        ("nul\x00byte", "nul\\x00byte"),
        ("del\x7fchar", "del\\x7fchar"),
        ("c1\x9bintroducer", "c1\\x9bintroducer"),
        ("csi\x1b]0;title\x07", "csi\\x1b]0;title\\x07"),
    ],
    ids=["esc", "cr", "lf", "tab", "nul", "del", "c1", "osc"],
)
def test_sanitize_label_escapes_every_control_character_visibly(
    raw: str, escaped: str
) -> None:
    assert sanitize_label(raw) == escaped


@pytest.mark.parametrize(
    "text",
    ["/pricing", "news.ycombinator.com", UNICODE_CAMPAIGN, "Ærø", "a b c", ""],
)
def test_sanitize_label_leaves_printable_text_exactly_as_it_arrived(
    text: str,
) -> None:
    assert sanitize_label(text) == text


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, "(none)"),
        (True, "true"),
        (False, "false"),
        (12, "12"),
        (1.5, "1.5"),
        ("", "(empty)"),
        (ANSI_CAMPAIGN, ESCAPED_ANSI_CAMPAIGN),
    ],
    ids=["none", "true", "false", "int", "float", "empty", "control-chars"],
)
def test_stringify_label_is_the_one_boundary_every_label_crosses(
    value: object, expected: str
) -> None:
    assert stringify_label(value) == expected


def test_a_campaign_label_carrying_an_ansi_escape_is_neutralised_in_the_table() -> None:
    text = format_table(campaign_result())
    assert ESCAPED_ANSI_CAMPAIGN in text
    assert ESCAPED_C1_CAMPAIGN in text
    # Nothing raw survives: no escape, no carriage return, no NUL, no DEL.
    for character in ("\x1b", "\r", "\x00", "\x07", "\x7f", "\x9b"):
        assert character not in text
    # And a legitimate label is untouched beside them.
    assert UNICODE_CAMPAIGN in text


def test_a_campaign_label_carrying_an_ansi_escape_is_neutralised_in_csv() -> None:
    text = format_csv(campaign_result())
    rows = list(csv.reader(io.StringIO(text)))
    assert rows == [
        ["utmCampaign", "pageviews", "visitors"],
        [ESCAPED_ANSI_CAMPAIGN, "5", "4"],
        [ESCAPED_C1_CAMPAIGN, "2", "2"],
        [UNICODE_CAMPAIGN, "1", "1"],
    ]
    # A carriage return inside a cell would split one row across two lines.
    assert len(text.splitlines()) == 4
    for character in ("\x1b", "\r", "\x00", "\x7f"):
        assert character not in text


def test_a_campaign_label_carrying_an_ansi_escape_is_neutralised_in_json() -> None:
    text = format_json(campaign_result(), CONTROL_CHARACTER_CAMPAIGN_PAYLOAD)
    document = json.loads(text)
    assert [row["key"] for row in document["rows"]] == [
        ESCAPED_ANSI_CAMPAIGN,
        ESCAPED_C1_CAMPAIGN,
        UNICODE_CAMPAIGN,
    ]
    assert document["rows"][0]["groups"] == {"utmCampaign": ESCAPED_ANSI_CAMPAIGN}
    # The escaping is in the value itself, not merely in the JSON encoding: the
    # raw payload under "raw" is the only place the original bytes remain.
    assert "\\u001b" not in json.dumps(document["rows"])
    assert "\x1b" not in text


def test_a_time_bucket_label_is_sanitized_like_any_other_label() -> None:
    payload = {
        "version": 1,
        "query": {"groupBy": ["day"]},
        "data": [{"timestamp": "2026-08-01\x1b[2J", "pageviews": 4, "visitors": 3}],
    }
    result = normalize(payload, "visits", ["day"])
    assert result.rows[0].timestamp == "2026-08-01\\x1b[2J"
    assert "\x1b" not in format_table(result)
    assert "\x1b" not in format_csv(result)


def test_an_others_row_without_a_label_never_renders_as_a_blank_cell() -> None:
    payload = {
        "version": 1,
        "query": {"groupBy": ["country"]},
        "data": [
            {"country": "US", "pageviews": 10, "visitors": 8},
            {"country": "Others", "pageviews": 6, "visitors": 5},
        ],
    }
    result = normalize(payload, "visits", ["country"])
    rows = list(csv.reader(io.StringIO(format_csv(result))))
    assert rows[2][0] == "Others"
