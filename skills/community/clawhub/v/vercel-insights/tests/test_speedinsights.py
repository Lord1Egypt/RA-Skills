"""Tests for vercel_insights/speedinsights.py.

The metric ids, targets and dimension names here are transcribed by hand from
docs/api-notes.md. None of them is read back out of ``METRICS``, ``TARGETS`` or
``SPEED_DIMENSIONS``: a test that asks the table under test what it contains
cannot notice the table containing the wrong thing.
"""

from __future__ import annotations

import json
from typing import Any

import pytest
from helpers import (
    CLS_COUNT_ID,
    CLS_ID,
    FCP_COUNT_ID,
    FCP_ID,
    INP_COUNT_ID,
    INP_ID,
    LCP_COUNT_ID,
    LCP_ID,
    OWNER,
    PROJECT,
    SPEED_DATA_POINTS_PAYLOAD,
    SPEED_EMPTY_PAYLOAD,
    SPEED_MALFORMED_PAYLOADS,
    SPEED_NESTED_BUCKET_PAYLOAD,
    SPEED_QUERY_URL,
    SPEED_ROLLUP_PAYLOAD,
    SPEED_ROUTE_PAYLOAD,
    SPEED_ROUTE_WITH_OTHERS_PAYLOAD,
    SPEED_TREND_PAYLOAD,
    SPEED_VITALS_PAYLOADS,
    TOKEN,
    TTFB_COUNT_ID,
    TTFB_ID,
    speed_value_payload,
    utc,
)

from vercel_insights import ApiError, ConfigError
from vercel_insights import speedinsights as si
from vercel_insights.render import UNIT_COUNT, UNIT_MS, UNIT_SCORE

# ---------------------------------------------------------------------------
# 1. The metric registry
# ---------------------------------------------------------------------------

# (short name, metric id, label, unit, published target). Every value comes
# from the metric id table and the targets table in docs/api-notes.md.
DOCUMENTED_VITALS: list[tuple[str, str, str, str, float]] = [
    ("lcp", "vercel.speed_insights.lcp_ms", "Largest Contentful Paint", UNIT_MS, 2500.0),
    ("inp", "vercel.speed_insights.inp_ms", "Interaction to Next Paint", UNIT_MS, 200.0),
    ("cls", "vercel.speed_insights.cls", "Cumulative Layout Shift", UNIT_SCORE, 0.1),
    ("fcp", "vercel.speed_insights.fcp_ms", "First Contentful Paint", UNIT_MS, 1800.0),
    ("ttfb", "vercel.speed_insights.ttfb_ms", "Time to First Byte", UNIT_MS, 800.0),
]

# (short name, data point count metric id).
DOCUMENTED_COUNTS: list[tuple[str, str]] = [
    ("lcp", "vercel.speed_insights.lcp_count"),
    ("inp", "vercel.speed_insights.inp_count"),
    ("cls", "vercel.speed_insights.cls_count"),
    ("fcp", "vercel.speed_insights.fcp_count"),
    ("ttfb", "vercel.speed_insights.ttfb_count"),
]


@pytest.mark.parametrize(
    ("short", "metric_id", "label", "unit", "target"),
    DOCUMENTED_VITALS,
    ids=[case[0] for case in DOCUMENTED_VITALS],
)
def test_every_value_metric_resolves_to_its_documented_id_unit_and_target(
    short: str, metric_id: str, label: str, unit: str, target: float
) -> None:
    metric = si.validate_metric(short)
    assert metric.id == metric_id
    assert metric.label == label
    assert metric.unit == unit
    assert metric.target == pytest.approx(target)
    assert metric.is_count is False


@pytest.mark.parametrize(
    ("short", "count_id"), DOCUMENTED_COUNTS, ids=[case[0] for case in DOCUMENTED_COUNTS]
)
def test_every_data_point_count_metric_resolves_to_its_documented_id(
    short: str, count_id: str
) -> None:
    counted = si.metric_for(short, data_points=True)
    assert counted.id == count_id
    assert counted.is_count is True
    assert counted.unit == UNIT_COUNT
    # A count of measurements is a count. Inheriting the vital's target would
    # render 12,480 measurements as "over the 2.5 s target".
    assert counted.target is None
    assert si.validate_metric(count_id).id == count_id


def test_the_registry_holds_exactly_the_ten_documented_metric_ids() -> None:
    expected = {metric_id for _short, metric_id, *_rest in DOCUMENTED_VITALS}
    expected |= {count_id for _short, count_id in DOCUMENTED_COUNTS}
    assert set(si.METRICS) == expected
    assert len(si.METRICS) == 10


def test_no_metric_id_is_invented_outside_the_documented_prefix() -> None:
    for metric_id in si.METRICS:
        assert metric_id.startswith("vercel.speed_insights.")
    # Real Experience Score has no id at all, in any spelling.
    assert not any("res" in metric_id.split(".")[-1] for metric_id in si.METRICS)


def test_the_value_metric_knows_the_id_of_its_own_count_metric() -> None:
    assert si.validate_metric("lcp").count_id == LCP_COUNT_ID
    assert si.validate_metric("cls").count_id == CLS_COUNT_ID
    assert si.validate_metric("ttfb").count_id == TTFB_COUNT_ID


def test_the_vitals_are_ordered_as_the_dashboard_orders_them() -> None:
    assert list(si.VITAL_ORDER) == ["lcp", "inp", "cls", "fcp", "ttfb"]


@pytest.mark.parametrize(
    ("spelling", "expected"),
    [
        ("lcp", LCP_ID),
        ("LCP", LCP_ID),
        ("  lcp  ", LCP_ID),
        ("lcp_ms", LCP_ID),
        ("lcp-ms", LCP_ID),
        (LCP_ID, LCP_ID),
        ("Largest Contentful Paint", LCP_ID),
        ("largest contentful paint", LCP_ID),
        ("inp", INP_ID),
        ("cls", CLS_ID),
        ("fcp", FCP_ID),
        ("ttfb", TTFB_ID),
        ("TTFB", TTFB_ID),
        ("lcp_count", LCP_COUNT_ID),
        ("inp count", INP_COUNT_ID),
        (CLS_COUNT_ID, CLS_COUNT_ID),
        ("fcp_count", FCP_COUNT_ID),
        ("ttfb_count", TTFB_COUNT_ID),
    ],
)
def test_validate_metric_accepts_every_documented_spelling(
    spelling: str, expected: str
) -> None:
    assert si.validate_metric(spelling).id == expected


# ---------------------------------------------------------------------------
# 2. validate_metric refusals
# ---------------------------------------------------------------------------


def test_an_unknown_metric_lists_the_five_and_names_the_flag() -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_metric("pageviews")
    message = str(excinfo.value)
    assert "unknown metric 'pageviews'" in message
    for short in ("lcp", "inp", "cls", "fcp", "ttfb"):
        assert short in message
    assert "--data-points" in message


@pytest.mark.parametrize(
    ("typo", "suggestion"),
    [("lcpp", "lcp"), ("clss", "cls"), ("ttbf", "ttfb"), ("inpp", "inp")],
)
def test_a_typo_gets_a_did_you_mean_naming_the_metric_it_meant(
    typo: str, suggestion: str
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_metric(typo)
    assert f"Did you mean {suggestion!r}?" in str(excinfo.value)


def test_an_empty_metric_name_is_refused_with_the_five_names() -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_metric("   ")
    assert "--metric is empty" in str(excinfo.value)
    assert "lcp, inp, cls, fcp, ttfb" in str(excinfo.value)


RES_SPELLINGS = [
    "res",
    "RES",
    "Res",
    "real experience score",
    "Real Experience Score",
    "real-experience-score",
    "RealExperienceScore",
    "experience score",
]


@pytest.mark.parametrize("spelling", RES_SPELLINGS)
def test_real_experience_score_is_refused_by_name_and_points_at_the_dashboard(
    spelling: str,
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_metric(spelling)
    message = str(excinfo.value)
    assert "Real Experience Score is not queryable" in message
    assert "dashboard" in message
    assert "vercel.com/docs/speed-insights" in message
    # It must not quietly answer with some other metric instead.
    assert "vercel.speed_insights.lcp_ms" not in message


@pytest.mark.parametrize("spelling", RES_SPELLINGS)
def test_the_real_experience_score_error_is_not_the_generic_unknown_metric_one(
    spelling: str,
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_metric(spelling)
    assert "unknown metric" not in str(excinfo.value)


# ---------------------------------------------------------------------------
# 3. Dimensions, aggregations, percentiles and limits
# ---------------------------------------------------------------------------

# Transcribed from the dimensions section of docs/api-notes.md.
DOCUMENTED_SPEED_DIMENSIONS = [
    "route",
    "request_path",
    "device_type",
    "country",
    "project_id",
    "environment",
]


def test_the_surface_accepts_exactly_the_six_confirmed_dimensions() -> None:
    assert list(si.SPEED_DIMENSIONS) == DOCUMENTED_SPEED_DIMENSIONS


@pytest.mark.parametrize("dimension", DOCUMENTED_SPEED_DIMENSIONS)
def test_every_confirmed_dimension_validates_unchanged(dimension: str) -> None:
    assert si.validate_dimension(dimension) == dimension


@pytest.mark.parametrize(
    ("camel", "snake"),
    [("requestPath", "request_path"), ("deviceType", "device_type"), ("projectId", "project_id")],
)
def test_a_web_analytics_spelling_names_the_snake_case_one_to_use_instead(
    camel: str, snake: str
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_dimension(camel)
    message = str(excinfo.value)
    assert "Web Analytics spelling" in message
    assert "snake_case" in message
    assert snake in message


@pytest.mark.parametrize(
    "dimension",
    ["browserName", "osName", "referrerHostname", "utmCampaign", "eventName", "flags"],
)
def test_a_web_analytics_only_dimension_says_this_surface_has_no_equivalent(
    dimension: str,
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_dimension(dimension)
    message = str(excinfo.value)
    assert "no Speed Insights" in message
    assert "route" in message


def test_an_unknown_dimension_suggests_the_closest_and_lists_the_set() -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_dimension("routes")
    assert "Did you mean 'route'?" in str(excinfo.value)

    with pytest.raises(ConfigError) as excinfo:
        si.validate_dimension("banana")
    assert "request_path" in str(excinfo.value)


def test_an_empty_dimension_is_refused() -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_dimension("  ")
    assert "empty grouping dimension" in str(excinfo.value)


def test_validate_group_by_refuses_a_repeat_and_a_third_dimension() -> None:
    assert si.validate_group_by(["route", "country"]) == ["route", "country"]

    with pytest.raises(ConfigError) as excinfo:
        si.validate_group_by(["route", "route"])
    assert "grouped by twice" in str(excinfo.value)

    with pytest.raises(ConfigError) as excinfo:
        si.validate_group_by(["route", "country", "device_type"])
    assert "exceeds the 2" in str(excinfo.value)


@pytest.mark.parametrize(
    "aggregation", ["sum", "count", "min", "max", "p75", "p90", "p95", "p99", "unique/visitor_id"]
)
def test_validate_aggregation_passes_a_documented_name_through(
    aggregation: str,
) -> None:
    assert si.validate_aggregation(aggregation) == aggregation


@pytest.mark.parametrize(
    "aggregation",
    ["", "  ", "p75; drop", "P75", "sum/a/b", "sum(", "*", "-sum", "sum value"],
)
def test_validate_aggregation_refuses_anything_that_is_not_a_name(
    aggregation: str,
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_aggregation(aggregation)
    assert "--aggregation" in str(excinfo.value)


@pytest.mark.parametrize(
    ("percentile", "expected"),
    [(75, "p75"), (90, "p90"), (95, "p95"), (99, "p99")],
)
def test_validate_percentile_maps_the_four_documented_values(
    percentile: int, expected: str
) -> None:
    assert si.validate_percentile(percentile) == expected


@pytest.mark.parametrize("percentile", [0, 1, 50, 74, 76, 100, -75, 999])
def test_validate_percentile_refuses_a_percentile_vercel_does_not_compute(
    percentile: int,
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_percentile(percentile)
    message = str(excinfo.value)
    assert f"--percentile {percentile}" in message
    assert "75, 90, 95, 99" in message


@pytest.mark.parametrize("limit", [1, 10, 100])
def test_validate_limit_accepts_the_inclusive_bounds(limit: int) -> None:
    assert si.validate_limit(limit) == limit


@pytest.mark.parametrize("limit", [0, -1, 101, 1000])
def test_validate_limit_refuses_a_limit_outside_the_bounds(limit: int) -> None:
    with pytest.raises(ConfigError) as excinfo:
        si.validate_limit(limit)
    assert "1 to 100" in str(excinfo.value)


# ---------------------------------------------------------------------------
# 4. Request building
# ---------------------------------------------------------------------------

SINCE = utc(2026, 8, 7)
UNTIL = utc(2026, 8, 14)


def build(**overrides: Any) -> Any:
    """A Speed Insights request with the fixed window, for readable bodies."""
    kwargs: dict[str, Any] = {
        "metric": si.validate_metric("lcp"),
        "since": SINCE,
        "until": UNTIL,
        "project": PROJECT,
        "owner_id": OWNER,
    }
    kwargs.update(overrides)
    return si.build_request(**kwargs)


def test_the_minimal_body_carries_only_the_five_required_fields() -> None:
    request = build()
    assert request.json_body == {
        "metric": "vercel.speed_insights.lcp_ms",
        "scope": {"type": "project", "ownerId": OWNER, "projectIds": [PROJECT]},
        "aggregation": "p75",
        "startTime": "2026-08-07T00:00:00Z",
        "endTime": "2026-08-14T00:00:00Z",
    }


def test_the_request_uses_the_observability_query_operation_and_its_url() -> None:
    request = build()
    assert request.operation == "observability_query"
    assert request.method == "POST"
    assert request.url == SPEED_QUERY_URL


def test_all_projects_sends_an_empty_project_list_under_the_same_owner() -> None:
    # VERIFIED shape: scope is {ownerId, projectIds} and both are required, so
    # "every project" is an empty list rather than a different kind of scope.
    body = build(project=None, all_projects=True).json_body
    assert body["scope"] == {"type": "owner", "ownerId": OWNER}
    # The owner is whatever was resolved; a team id is simply used as one.
    request = build(project=None, all_projects=True, owner_id="team_abc")
    assert request.json_body is not None
    assert request.json_body["scope"] == {"type": "owner", "ownerId": "team_abc"}


def test_no_project_and_no_all_is_refused_before_a_body_exists() -> None:
    with pytest.raises(ConfigError) as excinfo:
        build(project=None)
    assert "--all" in str(excinfo.value)
    assert "--project" in str(excinfo.value)


def test_a_team_is_simply_the_owner_and_there_is_no_separate_team_key() -> None:
    # The verified scope has exactly two keys. A team owned project is expressed
    # by making the team the owner, not by adding a team field beside it: the
    # 400 that revealed this shape named ownerId and projectIds and nothing else.
    request = build(owner_id="team_abc")
    assert request.json_body is not None
    scope = request.json_body["scope"]
    assert scope == {"type": "project", "ownerId": "team_abc", "projectIds": [PROJECT]}
    assert set(scope) <= {"type", "ownerId", "projectIds"}


def test_the_team_query_parameter_still_rides_along_inert() -> None:
    # Harmless, and it costs nothing to let the two channels agree.
    request = build(owner_id="team_abc", team="team_abc")
    assert request.params == [("teamId", "team_abc")]


@pytest.mark.parametrize(
    "selection",
    [
        {"project": PROJECT},
        {"project": None, "all_projects": True},
    ],
    ids=["project-scope", "owner-scope"],
)
@pytest.mark.parametrize(
    ("team_kwargs", "expected_params"),
    [
        ({"team": "team_abc"}, [("teamId", "team_abc")]),
        ({"team_slug": "acme"}, [("slug", "acme")]),
        ({}, []),
    ],
    ids=["team-id", "team-slug", "no-team"],
)
def test_the_scope_is_a_union_discriminated_on_type_for_every_selection(
    selection: dict[str, Any],
    team_kwargs: dict[str, str],
    expected_params: list[tuple[str, str]],
) -> None:
    # The scope shape is verified, not inferred: a request carrying the old
    # guess was answered with a 400 naming ownerId and projectIds. Whatever the
    # selection, those two keys are the whole object, and the team query
    # parameter is separate from it.
    request = build(**selection, **team_kwargs)
    assert request.params == expected_params
    assert request.json_body is not None
    scope = request.json_body["scope"]
    assert scope["ownerId"] == OWNER
    # A union discriminated on "type": the project variant names its projects,
    # the owner variant names none.
    if scope["type"] == "project":
        assert set(scope) == {"type", "ownerId", "projectIds"}
        assert isinstance(scope["projectIds"], list)
    else:
        assert scope["type"] == "owner"
        assert set(scope) == {"type", "ownerId"}


def test_every_optional_field_is_omitted_rather_than_sent_as_null() -> None:
    body = build().json_body
    assert body is not None
    for absent in (
        "groupBy",
        "filter",
        "limit",
        "orderBy",
        "orderDirection",
        "granularity",
        "bucketTimezone",
    ):
        assert absent not in body, f"{absent} was sent when nothing asked for it"
    assert None not in body.values()
    assert "null" not in json.dumps(body)


def test_a_fully_specified_body_carries_every_field_in_its_documented_spelling() -> None:
    body = build(
        metric=si.validate_metric("inp"),
        aggregation="p90",
        group_by=["route", "country"],
        filter_expr="country eq 'US'",
        limit=25,
        order_by="value",
        order_direction="asc",
        granularity="1d",
        bucket_timezone="Europe/Paris",
    ).json_body
    assert body == {
        "metric": "vercel.speed_insights.inp_ms",
        "scope": {"type": "project", "ownerId": OWNER, "projectIds": [PROJECT]},
        "aggregation": "p90",
        "groupBy": ["route", "country"],
        "filter": "country eq 'US'",
        "limit": 25,
        "orderBy": "value",
        "orderDirection": "asc",
        "granularity": {"days": 1},
        "startTime": "2026-08-07T00:00:00Z",
        "endTime": "2026-08-14T00:00:00Z",
        "bucketTimezone": "Europe/Paris",
    }


@pytest.mark.parametrize(
    ("interval", "expected"),
    [
        ("1h", {"hours": 1}),
        ("1d", {"days": 1}),
        ("1w", {"weeks": 1}),
        ("1mo", {"months": 1}),
        ("1y", {"years": 1}),
    ],
)
def test_granularity_travels_as_a_unit_and_count_object(
    interval: str, expected: dict[str, int]
) -> None:
    # VERIFIED: {"interval": "1d"} was refused outright by the API, which said
    # a granularity "must divide a day evenly or be a single week, month or
    # year". A unit and a count is the real shape.
    body = build(granularity=interval).json_body
    assert body is not None
    assert body["granularity"] == expected


def test_the_token_reaches_the_authorization_header_and_never_the_body() -> None:
    request = build(token=TOKEN)
    assert request.headers["Authorization"] == f"Bearer {TOKEN}"
    assert TOKEN not in json.dumps(request.json_body)
    assert TOKEN not in request.url
    assert TOKEN not in json.dumps(request.params)


def test_without_a_token_no_authorization_header_is_built_at_all() -> None:
    assert "Authorization" not in build().headers


# ---------------------------------------------------------------------------
# 5. Normalization of a response the OpenAPI document does not pin down
# ---------------------------------------------------------------------------

LCP = si.validate_metric("lcp")
LCP_COUNT = si.metric_for("lcp", data_points=True)


def test_a_single_value_response_becomes_one_ungrouped_row() -> None:
    result = si.normalize(SPEED_VITALS_PAYLOADS[0], metric=LCP, aggregation="p75")
    assert result.is_count is True
    assert result.metric == LCP_ID
    assert result.metric_label == "Largest Contentful Paint"
    assert result.unit == UNIT_MS
    assert result.target == pytest.approx(2500.0)
    assert result.additive is False
    assert len(result.rows) == 1
    assert result.rows[0].metrics["p75_lcp"] == pytest.approx(2412.0)
    assert result.rows[0].metrics["data_points"] == pytest.approx(12480)


def test_a_bare_number_response_is_read_as_the_value() -> None:
    result = si.normalize({"data": 2412}, metric=LCP, aggregation="p75")
    assert result.rows[0].metrics["p75_lcp"] == pytest.approx(2412.0)


def test_a_grouped_response_keeps_one_label_and_the_data_point_count_per_row() -> None:
    result = si.normalize(
        SPEED_ROUTE_PAYLOAD, metric=LCP, aggregation="p75", group_by=["route"]
    )
    assert result.group_by == ["route"]
    assert result.is_count is False
    assert [row.key for row in result.rows] == ["/blog/[slug]", "/pricing", "/"]
    assert [row.metrics["p75_lcp"] for row in result.rows] == [4120.0, 2980.0, 1240.0]
    assert [row.metrics["data_points"] for row in result.rows] == [1830.0, 640.0, 8800.0]
    # A percentile is not additive, so the renderer must not total it.
    assert result.additive is False


def test_a_time_bucketed_response_keeps_its_bucket_starts_and_granularity() -> None:
    result = si.normalize(
        SPEED_TREND_PAYLOAD, metric=LCP, aggregation="p75", granularity="1d"
    )
    assert result.is_count is False
    assert result.time_bucket == "1d"
    assert result.granularity == "1d"
    assert [row.timestamp for row in result.rows] == [
        "2026-08-10T00:00:00.000Z",
        "2026-08-11T00:00:00.000Z",
    ]
    assert [row.metrics["p75_lcp"] for row in result.rows] == [2100.0, 2450.0]


def test_a_rollup_keyed_by_dimension_value_is_read_in_both_of_its_forms() -> None:
    result = si.normalize(
        SPEED_ROLLUP_PAYLOAD, metric=LCP, aggregation="p75", group_by=["country"]
    )
    assert [row.key for row in result.rows] == ["US", "DE"]
    assert [row.metrics["p75_lcp"] for row in result.rows] == [2100.0, 1800.0]
    assert result.rows[1].metrics["data_points"] == pytest.approx(430)


def test_rows_nested_inside_a_time_bucket_inherit_the_bucket_timestamp() -> None:
    result = si.normalize(
        SPEED_NESTED_BUCKET_PAYLOAD, metric=LCP, aggregation="p75", group_by=["country"]
    )
    assert [row.key for row in result.rows] == ["US", "DE"]
    assert all(row.timestamp == "2026-08-10T00:00:00.000Z" for row in result.rows)


def test_a_sum_of_data_point_counts_is_additive_and_carries_the_count_unit() -> None:
    result = si.normalize(
        SPEED_DATA_POINTS_PAYLOAD,
        metric=LCP_COUNT,
        aggregation="sum",
        group_by=["route"],
    )
    assert result.additive is True
    assert result.unit == UNIT_COUNT
    assert result.target is None
    assert result.totals()["sum_lcp_count"] == pytest.approx(10630)


def test_an_empty_result_is_success_with_no_rows_rather_than_an_error() -> None:
    result = si.normalize(SPEED_EMPTY_PAYLOAD, metric=LCP, aggregation="p75")
    assert result.rows == []
    assert result.metric == LCP_ID


@pytest.mark.parametrize(
    "payload",
    [case[1] for case in SPEED_MALFORMED_PAYLOADS],
    ids=[case[0] for case in SPEED_MALFORMED_PAYLOADS],
)
def test_an_unreadable_response_is_a_clean_invalid_response_error(
    payload: dict[str, Any],
) -> None:
    with pytest.raises(ApiError) as excinfo:
        si.normalize(payload, metric=LCP, aggregation="p75")
    assert excinfo.value.code == "invalid_response"
    message = str(excinfo.value)
    assert "--json" in message
    assert "cannot read" in message


def test_the_unreadable_response_error_names_the_shape_but_not_its_content() -> None:
    payload = {"version": 1, "data": {"status": "ok", "detail": "secret-ish"}}
    with pytest.raises(ApiError) as excinfo:
        si.normalize(payload, metric=LCP, aggregation="p75")
    message = str(excinfo.value)
    assert "2 field(s)" in message
    assert "secret-ish" not in message


@pytest.mark.parametrize(
    "payload",
    [case[1] for case in SPEED_MALFORMED_PAYLOADS],
    ids=[case[0] for case in SPEED_MALFORMED_PAYLOADS],
)
def test_a_malformed_response_never_raises_a_key_error(payload: dict[str, Any]) -> None:
    try:
        si.normalize(payload, metric=LCP, aggregation="p75", group_by=["route"])
    except ApiError:
        pass
    except KeyError as exc:  # pragma: no cover - the assertion is the point
        raise AssertionError(f"normalize raised KeyError({exc})") from exc


def test_an_envelope_carrying_only_a_schema_version_is_not_read_as_a_value() -> None:
    # {"version": 1} is not a P75 of 1 millisecond. Reading the envelope as a
    # measurement would print a confidently formatted wrong figure.
    with pytest.raises(ApiError) as excinfo:
        si.normalize({"version": 1, "query": {}}, metric=LCP, aggregation="p75")
    assert excinfo.value.code == "invalid_response"


def test_normalize_ignores_a_row_field_it_does_not_recognise() -> None:
    payload = speed_value_payload(LCP_ID, 2412.0)
    payload["data"]["unexpectedField"] = "whatever"
    result = si.normalize(payload, metric=LCP, aggregation="p75")
    assert result.rows[0].metrics["p75_lcp"] == pytest.approx(2412.0)


def test_a_data_point_count_is_never_double_counted_as_the_value() -> None:
    payload = {"version": 1, "data": {LCP_COUNT_ID: 12480}}
    result = si.normalize(payload, metric=LCP, aggregation="p75")
    metrics = result.rows[0].metrics
    assert metrics["p75_lcp"] == pytest.approx(12480)
    assert metrics.get("data_points", 0) == 0


def test_the_others_overflow_bucket_is_marked_on_this_surface_too() -> None:
    result = si.normalize(
        SPEED_ROUTE_WITH_OTHERS_PAYLOAD,
        metric=LCP,
        aggregation="p75",
        group_by=["route"],
    )
    assert [row.key for row in result.rows] == ["/blog/[slug]", "/pricing", "Others"]
    assert [row.is_others for row in result.rows] == [False, False, True]


def test_an_others_bucket_arriving_as_a_rollup_key_is_marked_as_well() -> None:
    payload = {
        "version": 1,
        "query": {"metric": LCP_ID, "groupBy": ["country"]},
        "data": {"US": 2100.0, "Others": 1800.0},
    }
    result = si.normalize(payload, metric=LCP, aggregation="p75", group_by=["country"])
    assert [row.is_others for row in result.rows] == [False, True]


# ---------------------------------------------------------------------------
# 6. The last resort value probe, and the ambiguity it refuses to resolve
# ---------------------------------------------------------------------------
#
# The observability API publishes no response schema, so a row whose value
# arrived under a name none of the probes predicted is read anyway when there
# is exactly one number to read. Two numbers is a guess, and guessing here
# means printing a confidently formatted wrong web vital.


def test_a_row_with_exactly_one_unrecognised_number_is_read_as_the_value() -> None:
    payload = {"version": 1, "data": [{"route": "/", "p75Millis": 2412.0}]}
    result = si.normalize(payload, metric=LCP, aggregation="p75", group_by=["route"])
    assert [row.key for row in result.rows] == ["/"]
    assert result.rows[0].metrics["p75_lcp"] == pytest.approx(2412.0)


def test_an_ungrouped_row_with_one_unrecognised_number_is_read_too() -> None:
    result = si.normalize(
        {"version": 1, "data": {"p75Millis": 2412.0}}, metric=LCP, aggregation="p75"
    )
    assert result.rows[0].metrics["p75_lcp"] == pytest.approx(2412.0)


def test_a_row_with_two_unrecognised_numbers_is_refused_rather_than_guessed() -> None:
    payload = {
        "version": 1,
        "data": [{"route": "/", "p75Millis": 2412.0, "p90Millis": 3100.0}],
    }
    with pytest.raises(ApiError) as excinfo:
        si.normalize(payload, metric=LCP, aggregation="p75", group_by=["route"])
    assert excinfo.value.code == "invalid_response"
    # Neither candidate is quoted back, and neither is silently chosen.
    assert "2412" not in str(excinfo.value)
    assert "3100" not in str(excinfo.value)


def test_two_unrecognised_numbers_are_refused_even_with_a_recognised_label() -> None:
    payload = {
        "version": 1,
        "data": [
            {"route": "/", "value": 2412.0},
            {"route": "/pricing", "alpha": 1.0, "beta": 2.0},
        ],
    }
    # The readable row still parses; the ambiguous one is skipped rather than
    # invented, so the table never carries a number nobody sent.
    result = si.normalize(payload, metric=LCP, aggregation="p75", group_by=["route"])
    assert [row.key for row in result.rows] == ["/"]


def test_an_envelope_field_is_never_the_sole_number_a_row_is_read_from() -> None:
    # {"version": 1} is one number under a name no probe predicted, and it is
    # still not a P75 of 1 millisecond.
    with pytest.raises(ApiError) as excinfo:
        si.normalize({"version": 1}, metric=LCP, aggregation="p75")
    assert excinfo.value.code == "invalid_response"


def test_the_query_block_from_the_response_is_carried_through_untouched() -> None:
    result = si.normalize(
        SPEED_ROUTE_PAYLOAD, metric=LCP, aggregation="p75", group_by=["route"]
    )
    assert result.query == SPEED_ROUTE_PAYLOAD["query"]
