"""Tests for vercel_insights/webanalytics.py: validation, requests, parsing."""

from __future__ import annotations

from typing import Any

import pytest
from helpers import (
    COUNTRY_PAYLOAD,
    COUNTRY_WITH_OTHERS_PAYLOAD,
    DAILY_PAYLOAD,
    EMPTY_AGGREGATE_PAYLOAD,
    EVENT_DATA_PAYLOAD,
    EVENTS_COUNT_PAYLOAD,
    FLAGS_PAYLOAD,
    PROJECT,
    TIME_ONLY_OTHERS_PAYLOAD,
    TOKEN,
    TWO_DIMENSION_PAYLOAD,
    TWO_DIMENSIONS,
    VISITS_COUNT_PAYLOAD,
    WEB_ANALYTICS_BASE,
    prepared,
)

from vercel_insights import ApiError, ConfigError
from vercel_insights import webanalytics as wa
from vercel_insights.render import format_table

# ---------------------------------------------------------------------------
# Dimension, grouping and limit validation
# ---------------------------------------------------------------------------


def test_validate_dimension_accepts_every_documented_visits_dimension() -> None:
    for dimension in wa.VISIT_DIMENSIONS:
        assert wa.validate_dimension(dimension, "visits") == dimension


def test_validate_dimension_accepts_event_only_dimensions_on_events() -> None:
    assert wa.validate_dimension("eventName", "events") == "eventName"
    assert wa.validate_dimension("eventData/plan", "events") == "eventData/plan"
    assert (
        wa.validate_dimension("eventData/'sign-up'", "events") == "eventData/'sign-up'"
    )
    assert wa.validate_dimension("flags/beta_banner", "events") == "flags/beta_banner"


def test_validate_dimension_requires_quoting_for_a_key_with_punctuation() -> None:
    with pytest.raises(ConfigError) as excinfo:
        wa.validate_dimension("eventData/sign-up", "events")
    assert "eventData/'sign-up'" in str(excinfo.value)


def test_validate_dimension_rejects_an_unknown_json_base() -> None:
    with pytest.raises(ConfigError) as excinfo:
        wa.validate_dimension("metadata/plan", "events")
    assert "unknown JSON dimension" in str(excinfo.value)


def test_validate_group_by_rejects_a_repeated_dimension() -> None:
    with pytest.raises(ConfigError) as excinfo:
        wa.validate_group_by(["day", "day"], "visits")
    assert "grouped by twice" in str(excinfo.value)


def test_validate_limit_accepts_the_inclusive_bounds() -> None:
    assert wa.validate_limit(wa.MIN_LIMIT) == 1
    assert wa.validate_limit(wa.MAX_LIMIT) == 100


def test_a_multi_segment_json_key_is_accepted_per_the_openapi_schema() -> None:
    assert wa.validate_dimension("eventData/a/b", "events") == "eventData/a/b"
    assert wa.validate_dimension("flags/'a/b'", "visits") == "flags/'a/b'"


@pytest.mark.parametrize(
    "dimension",
    ["eventData/'a' or 1 eq '1'", "eventData/'unbalanced", "eventData/a'b", "flags/''"],
)
def test_a_malformed_quoted_json_key_is_rejected(dimension: str) -> None:
    with pytest.raises(ConfigError):
        wa.validate_dimension(dimension, "events")


# ---------------------------------------------------------------------------
# Endpoint selection and request building
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("group_by", "expected"),
    [
        ([], "count"),
        (["day"], "aggregate"),
        (["requestPath"], "aggregate"),
        (["day", "country"], "aggregate"),
    ],
)
def test_select_endpoint_picks_aggregate_only_when_grouping_is_present(
    group_by: list[str], expected: str
) -> None:
    assert wa.select_endpoint(group_by) == expected


def test_a_count_request_carries_neither_by_nor_limit() -> None:
    request = prepared(group_by=[], limit=10)
    keys = [name for name, _ in request.params]
    assert request.url == f"{WEB_ANALYTICS_BASE}/visits/count"
    assert "by" not in keys
    assert "limit" not in keys
    assert keys == ["projectId", "since", "until"]


def test_an_aggregate_request_carries_by_since_until_and_limit() -> None:
    request = prepared(group_by=["requestPath"], limit=25)
    assert request.url == f"{WEB_ANALYTICS_BASE}/visits/aggregate"
    assert request.params == [
        ("projectId", PROJECT),
        ("by", "requestPath"),
        ("since", "2026-08-07T00:00:00Z"),
        ("until", "2026-08-14T00:00:00Z"),
        ("limit", "25"),
    ]


def test_two_grouping_dimensions_become_two_repeated_by_parameters() -> None:
    request = prepared(group_by=["day", "country"])
    assert [value for name, value in request.params if name == "by"] == [
        "day",
        "country",
    ]


def test_build_request_places_the_events_dataset_in_the_path() -> None:
    request = prepared(dataset="events", group_by=["eventName"])
    assert request.url == f"{WEB_ANALYTICS_BASE}/events/aggregate"


def test_build_request_passes_filter_team_and_slug_through_as_parameters() -> None:
    request = prepared(filter_expr="country eq 'US'", team="team_abc", team_slug="acme")
    params = dict(request.params)
    assert params["filter"] == "country eq 'US'"
    assert params["teamId"] == "team_abc"
    assert params["slug"] == "acme"


def test_build_request_puts_the_token_only_in_the_authorization_header() -> None:
    request = prepared()
    assert request.headers["Authorization"] == f"Bearer {TOKEN}"
    assert TOKEN not in request.url
    assert all(TOKEN not in value for _, value in request.params)
    assert request.method == "GET"


def test_build_request_omits_the_authorization_header_without_a_token() -> None:
    request = prepared(token=None)
    assert "Authorization" not in request.headers


def test_build_request_uses_the_web_analytics_operation_key() -> None:
    # The key, not a method and not a host: the dispatcher reads both back out
    # of the allowlist, so this is the only thing the surface gets to choose.
    request = prepared()
    assert request.operation == "web_analytics"
    assert request.json_body is None


# ---------------------------------------------------------------------------
# Response normalization
# ---------------------------------------------------------------------------


def test_normalize_reads_a_visits_count_as_a_single_keyless_row() -> None:
    result = wa.normalize(VISITS_COUNT_PAYLOAD, "visits", [])
    assert result.is_count is True
    assert result.metric_names == ["pageviews", "visitors"]
    assert len(result.rows) == 1
    assert result.rows[0].key is None
    assert result.rows[0].metrics == {"pageviews": 1250, "visitors": 980}
    assert result.query["filter"] == "requestPath eq '/blog/my-post'"


def test_normalize_reads_an_events_count_with_the_events_metric_names() -> None:
    result = wa.normalize(EVENTS_COUNT_PAYLOAD, "events", [])
    assert result.is_count is True
    assert result.metric_names == ["count", "visitors"]
    assert result.rows[0].metrics == {"count": 42, "visitors": 36}
    assert "pageviews" not in result.rows[0].metrics


def test_normalize_reads_timestamp_rows_when_grouping_by_a_granularity() -> None:
    result = wa.normalize(DAILY_PAYLOAD, "visits", ["day"])
    assert result.is_count is False
    assert result.granularity == "day"
    assert result.group_dimension is None
    assert [row.timestamp for row in result.rows] == [
        "2024-10-01T00:00:00.000Z",
        "2024-10-02T00:00:00.000Z",
    ]
    assert [row.key for row in result.rows] == [None, None]
    assert result.totals() == {"pageviews": 465, "visitors": 381}


def test_normalize_labels_rows_with_the_plain_grouping_dimension() -> None:
    result = wa.normalize(COUNTRY_PAYLOAD, "visits", ["country"])
    assert result.group_dimension == "country"
    assert [row.key for row in result.rows] == ["US", "DE"]
    assert result.rows[0].metrics == {"pageviews": 640, "visitors": 510}
    assert all(row.timestamp is None for row in result.rows)


def test_normalize_remaps_event_data_rows_back_onto_the_requested_dimension() -> None:
    result = wa.normalize(EVENT_DATA_PAYLOAD, "events", ["eventData/plan"])
    assert result.group_dimension == "eventData/plan"
    assert [row.key for row in result.rows] == ["pro", "enterprise"]
    assert result.metric_names == ["count", "visitors"]
    assert "eventData" not in result.rows[0].metrics


def test_normalize_remaps_flag_rows_and_stringifies_non_string_labels() -> None:
    result = wa.normalize(FLAGS_PAYLOAD, "visits", ["flags/beta_banner"])
    assert [row.key for row in result.rows] == ["true", "false"]
    assert result.rows[0].metrics == {"pageviews": 90, "visitors": 70}


def test_normalize_marks_the_others_bucket_and_counts_it_in_the_total() -> None:
    result = wa.normalize(COUNTRY_WITH_OTHERS_PAYLOAD, "visits", ["country"])
    assert [row.is_others for row in result.rows] == [False, False, True]
    assert result.totals()["pageviews"] == 900


def test_normalize_handles_an_empty_data_array_without_losing_metric_names() -> None:
    result = wa.normalize(EMPTY_AGGREGATE_PAYLOAD, "visits", ["requestPath"])
    assert result.rows == []
    assert result.metric_names == ["pageviews", "visitors"]
    assert result.totals() == {"pageviews": 0, "visitors": 0}


def test_normalize_ignores_unexpected_extra_row_fields() -> None:
    payload = {
        "version": 1,
        "query": {"groupBy": ["country"]},
        "data": [{"country": "US", "pageviews": 5, "visitors": 4, "aiTokens": 7}],
    }
    result = wa.normalize(payload, "visits", ["country"])
    assert result.rows[0].key == "US"
    assert result.rows[0].metrics["pageviews"] == 5
    assert result.metric_names[:2] == ["pageviews", "visitors"]


def test_normalize_carries_the_dataset_metrics_as_the_render_fallback() -> None:
    # The renderers are surface agnostic, so the fallback metric names travel
    # on the result rather than being looked up in a Web Analytics table.
    assert wa.normalize(VISITS_COUNT_PAYLOAD, "visits", []).fallback_metrics == (
        "pageviews",
        "visitors",
    )
    assert wa.normalize(EVENTS_COUNT_PAYLOAD, "events", []).fallback_metrics == (
        "count",
        "visitors",
    )


def test_a_two_dimension_grouping_keeps_both_labels_on_every_row() -> None:
    result = wa.normalize(TWO_DIMENSION_PAYLOAD, "events", TWO_DIMENSIONS)
    assert result.group_dimensions == TWO_DIMENSIONS
    assert [row.labels for row in result.rows] == [
        ("signup", "free"),
        ("signup", "pro"),
        ("purchase", "pro"),
    ]
    assert result.metric_names == ["count", "visitors"]
    assert "eventData" not in result.rows[0].metrics
    assert "eventName" not in result.rows[0].metrics


def test_a_json_dimension_label_comes_from_its_base_key_not_a_stray_string() -> None:
    # eventData/plan rows arrive keyed plain "eventData". A row that also
    # carries some other string field must still take its label from the base
    # key, not from whichever string field happens to come first.
    payload = {
        "version": 1,
        "query": {"groupBy": ["eventName", "eventData/plan"]},
        "data": [
            {
                "eventName": "signup",
                "note": "unrelated",
                "eventData": "free",
                "count": 30,
                "visitors": 28,
            }
        ],
    }
    result = wa.normalize(payload, "events", TWO_DIMENSIONS)
    assert result.rows[0].labels == ("signup", "free")
    assert "note" not in result.rows[0].metrics


def test_the_others_bucket_is_detected_on_a_time_only_grouping() -> None:
    result = wa.normalize(TIME_ONLY_OTHERS_PAYLOAD, "visits", ["day"])
    assert [row.is_others for row in result.rows] == [False, False, True]
    assert result.totals()["pageviews"] == 21


# ---------------------------------------------------------------------------
# Defensive parsing of malformed payloads
# ---------------------------------------------------------------------------


def test_normalize_rejects_an_aggregate_payload_with_no_data_key() -> None:
    with pytest.raises(ApiError) as excinfo:
        wa.normalize({"version": 1, "query": {}}, "visits", ["country"])
    assert excinfo.value.code == "invalid_response"
    assert "missing or null" in str(excinfo.value)


def test_normalize_rejects_a_count_payload_with_no_data_key() -> None:
    with pytest.raises(ApiError) as excinfo:
        wa.normalize({"version": 1, "query": {}}, "visits", [])
    assert excinfo.value.code == "invalid_response"
    assert "count response" in str(excinfo.value)


@pytest.mark.parametrize(
    ("group_by", "data", "expected"),
    [
        (["country"], {"pageviews": 5}, "aggregate response"),
        (["country"], "rows", "aggregate response"),
        (["country"], 7, "aggregate response"),
        ([], [{"pageviews": 5}], "count response"),
        ([], "totals", "count response"),
    ],
    ids=["aggregate-dict", "aggregate-str", "aggregate-int", "count-list", "count-str"],
)
def test_normalize_rejects_a_data_value_of_the_wrong_type(
    group_by: list[str], data: Any, expected: str
) -> None:
    payload = {"version": 1, "query": {}, "data": data}
    with pytest.raises(ApiError) as excinfo:
        wa.normalize(payload, "visits", group_by)
    rendered = str(excinfo.value)
    assert expected in rendered
    assert excinfo.value.status == 200
    # The message names the shape only, so nothing from the body is echoed back.
    assert "pageviews" not in rendered
    assert "totals" not in rendered


def test_normalize_survives_a_row_that_carries_no_metrics() -> None:
    payload = {
        "version": 1,
        "query": {"groupBy": ["country"]},
        "data": [{"country": "US"}, {"country": "DE", "pageviews": 4}],
    }
    result = wa.normalize(payload, "visits", ["country"])
    assert [row.key for row in result.rows] == ["US", "DE"]
    assert result.rows[0].metrics == {}
    assert result.totals()["pageviews"] == 4
    text = format_table(result)
    assert "US" in text and "DE" in text
    assert "Traceback" not in text


def test_normalize_skips_a_row_that_is_not_an_object() -> None:
    payload = {
        "version": 1,
        "query": {},
        "data": ["nonsense", 42, None, {"country": "US", "pageviews": 3}],
    }
    result = wa.normalize(payload, "visits", ["country"])
    assert [row.key for row in result.rows] == ["US"]
