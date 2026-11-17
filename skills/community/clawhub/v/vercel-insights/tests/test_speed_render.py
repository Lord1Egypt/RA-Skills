"""Rendering a Speed Insights result: units, targets, verdicts and legends.

The verdict is two tier by design. Vercel publishes one "good" target per web
vital and no boundary above it, and the dashboard's good / needs improvement /
poor bands describe a derived 0 to 100 score rather than a raw millisecond
figure. Several tests below exist only to keep that third tier from creeping
into the output.
"""

from __future__ import annotations

import csv
import io
import json
from typing import Any

import pytest
from helpers import (
    ANSI_BUCKET,
    ANSI_ROUTE,
    CLS_ID,
    ESCAPED_ANSI_BUCKET,
    ESCAPED_ANSI_ROUTE,
    INP_ID,
    LCP_COUNT_ID,
    LCP_ID,
    PROJECT,
    SPEED_DATA_POINTS_PAYLOAD,
    SPEED_ROUTE_PAYLOAD,
    SPEED_ROUTE_WITH_OTHERS_PAYLOAD,
    SPEED_TREND_PAYLOAD,
    SPEED_VITALS_PAYLOADS,
    speed_value_payload,
    utc,
)

from vercel_insights import speedinsights as si
from vercel_insights.render import (
    UNIT_COUNT,
    UNIT_MS,
    UNIT_SCORE,
    VERDICT_MEETS,
    VERDICT_OVER,
    VERDICT_UNKNOWN,
    Result,
    format_csv,
    format_json,
    format_table,
    format_value,
    render_vitals,
    verdict,
)

TIME_RANGE = (utc(2026, 8, 7), utc(2026, 8, 14))

#: Wording that would claim a three tier rating Vercel does not publish.
THREE_TIER_WORDING = [
    "needs improvement",
    "needs-improvement",
    "needsimprovement",
    "poor",
]


def vitals_results(*payloads: dict[str, Any]) -> list[Result]:
    """Normalize one ungrouped payload per vital, in display order."""
    return [
        si.normalize(payload, metric=si.validate_metric(short), aggregation="p75")
        for short, payload in zip(si.VITAL_ORDER, payloads)
    ]


# ---------------------------------------------------------------------------
# 1. format_value at the boundaries
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0.0, "0 ms"),
        (1.0, "1 ms"),
        (168.0, "168 ms"),
        (799.0, "799 ms"),
        (998.4, "998 ms"),
        (999.0, "999 ms"),
        (999.9, "1000 ms"),
        (1000.0, "1.0 s"),
        (1000.1, "1.0 s"),
        (1449.0, "1.4 s"),
        (1450.0, "1.4 s"),
        (1800.0, "1.8 s"),
        (2500.0, "2.5 s"),
        (4120.0, "4.1 s"),
        (12345.0, "12.3 s"),
    ],
)
def test_a_millisecond_value_switches_to_seconds_at_one_thousand(
    value: float, expected: str
) -> None:
    assert format_value(value, UNIT_MS) == expected


def test_the_millisecond_boundary_is_exactly_where_it_is_documented() -> None:
    # 999 ms stays milliseconds; 1000 ms reads as 1.0 s.
    assert format_value(999.0, UNIT_MS).endswith(" ms")
    assert format_value(1000.0, UNIT_MS) == "1.0 s"


@pytest.mark.parametrize(
    ("value", "expected"),
    [(0.0, "0.000"), (0.083, "0.083"), (0.0834, "0.083"), (0.1, "0.100"), (0.25, "0.250")],
)
def test_a_layout_shift_score_keeps_three_decimals_and_no_unit(
    value: float, expected: str
) -> None:
    rendered = format_value(value, UNIT_SCORE)
    assert rendered == expected
    assert "ms" not in rendered
    assert "s" not in rendered


@pytest.mark.parametrize(
    ("value", "expected"), [(0.0, "0"), (1830.0, "1,830"), (12480.0, "12,480")]
)
def test_a_data_point_count_is_a_thousands_separated_plain_number(
    value: float, expected: str
) -> None:
    assert format_value(value, UNIT_COUNT) == expected


# ---------------------------------------------------------------------------
# 2. The verdict, at and around each published target
# ---------------------------------------------------------------------------

# (metric, published target). Transcribed from docs/api-notes.md.
PUBLISHED_TARGETS: list[tuple[str, float]] = [
    ("lcp", 2500.0),
    ("inp", 200.0),
    ("cls", 0.1),
    ("fcp", 1800.0),
    ("ttfb", 800.0),
]


@pytest.mark.parametrize(
    ("short", "target"), PUBLISHED_TARGETS, ids=[case[0] for case in PUBLISHED_TARGETS]
)
def test_a_value_exactly_on_the_target_meets_it_and_a_hair_over_does_not(
    short: str, target: float
) -> None:
    step = 0.001 if short == "cls" else 1.0
    assert verdict(target, target) == VERDICT_MEETS
    assert verdict(target - step, target) == VERDICT_MEETS
    assert verdict(target + step, target) == VERDICT_OVER


def test_2500_milliseconds_meets_the_lcp_target_and_2501_does_not() -> None:
    # Vercel states the LCP target as "2.5 seconds or less", so the boundary
    # itself is inside the target.
    assert verdict(2500.0, 2500.0) == VERDICT_MEETS
    assert verdict(2501.0, 2500.0) == VERDICT_OVER


def test_a_metric_with_no_published_target_gets_no_verdict() -> None:
    assert verdict(12480.0, None) == VERDICT_UNKNOWN
    assert verdict(None, 2500.0) == VERDICT_UNKNOWN


def test_the_verdict_vocabulary_has_exactly_two_tiers() -> None:
    values = {verdict(value, 2500.0) for value in (0.0, 2499.0, 2500.0, 2501.0, 9999.0)}
    assert values == {VERDICT_MEETS, VERDICT_OVER}
    for wording in THREE_TIER_WORDING:
        assert wording not in " ".join(values).lower()


# ---------------------------------------------------------------------------
# 3. render_vitals
# ---------------------------------------------------------------------------


def test_the_vitals_table_names_each_metric_its_value_target_and_verdict() -> None:
    text = render_vitals(
        vitals_results(*SPEED_VITALS_PAYLOADS),
        project=PROJECT,
        time_range=TIME_RANGE,
    )
    assert f"Vercel Speed Insights: {PROJECT}" in text
    assert "Range: 2026-08-07T00:00:00Z to 2026-08-14T00:00:00Z (UTC)" in text

    lines = text.splitlines()
    assert lines[3].split() == ["metric", "p75", "target", "verdict", "data", "points"]

    body = {line.split("  ")[0].strip(): line for line in lines[5:10]}
    assert "2.4 s" in body["Largest Contentful Paint"]
    assert "2.5 s" in body["Largest Contentful Paint"]
    assert VERDICT_MEETS in body["Largest Contentful Paint"]
    assert "168 ms" in body["Interaction to Next Paint"]
    assert "200 ms" in body["Interaction to Next Paint"]
    assert "0.083" in body["Cumulative Layout Shift"]
    assert "0.100" in body["Cumulative Layout Shift"]
    assert "812 ms" in body["First Contentful Paint"]
    assert "1.8 s" in body["First Contentful Paint"]
    # TTFB is over its 800 ms target in the fixture, so the verdict column has
    # to actually vary rather than always agreeing.
    assert "934 ms" in body["Time to First Byte"]
    assert VERDICT_OVER in body["Time to First Byte"]
    assert "12,480" in body["Time to First Byte"]


def test_the_vitals_table_reports_both_verdicts_and_never_a_third_tier() -> None:
    text = render_vitals(
        vitals_results(*SPEED_VITALS_PAYLOADS),
        project=PROJECT,
        time_range=TIME_RANGE,
    )
    assert VERDICT_MEETS in text
    assert VERDICT_OVER in text
    lowered = text.lower()
    for wording in THREE_TIER_WORDING:
        assert wording not in lowered, f"{wording!r} is a tier Vercel does not publish"


def test_the_vitals_legend_says_lower_is_better_and_why_the_counts_matter() -> None:
    text = render_vitals(
        vitals_results(*SPEED_VITALS_PAYLOADS),
        project=PROJECT,
        time_range=TIME_RANGE,
    )
    assert "Lower is better for all five metrics." in text
    assert "two tier" in text
    assert "few data points is not comparable" in text
    assert "Real Experience Score is not queryable" in text
    assert "dashboard" in text


def test_a_metric_that_came_back_empty_reads_as_no_data_rather_than_zero() -> None:
    payloads = [
        speed_value_payload(LCP_ID, 2412.0, 12480),
        {"version": 1, "query": {}, "data": []},
        speed_value_payload(CLS_ID, 0.083, 12480),
    ]
    text = render_vitals(
        vitals_results(*payloads), project=PROJECT, time_range=TIME_RANGE
    )
    line = next(
        row for row in text.splitlines() if row.startswith("Interaction to Next Paint")
    )
    cells = [cell.strip() for cell in line.split("  ") if cell.strip()]
    # The value and the verdict both say so; neither reads as a measured zero.
    assert cells == ["Interaction to Next Paint", "no data", "200 ms", "no data", "n/a"]


def test_the_vitals_table_uses_the_aggregation_it_was_given_as_its_column_head() -> None:
    text = render_vitals(
        vitals_results(*SPEED_VITALS_PAYLOADS),
        project=PROJECT,
        time_range=TIME_RANGE,
        aggregation="p95",
    )
    assert "p95" in text.splitlines()[3]


def test_a_vitals_table_of_data_point_counts_swaps_the_legend_and_drops_targets() -> (
    None
):
    results = [
        si.normalize(
            speed_value_payload(LCP_COUNT_ID, 12480),
            metric=si.metric_for(short, data_points=True),
            aggregation="sum",
        )
        for short in si.VITAL_ORDER
    ]
    text = render_vitals(results, project=PROJECT, time_range=TIME_RANGE)
    assert "12,480" in text
    assert "one data point is one measurement" in text
    assert "target" not in text.splitlines()[3]
    assert VERDICT_MEETS not in text
    assert VERDICT_OVER not in text


# ---------------------------------------------------------------------------
# 4. format_table on a Speed Insights result
# ---------------------------------------------------------------------------


def grouped_result() -> Result:
    return si.normalize(
        SPEED_ROUTE_PAYLOAD,
        metric=si.validate_metric("lcp"),
        aggregation="p75",
        group_by=["route"],
    )


def test_a_grouped_percentile_table_has_no_totals_row_and_no_share_column() -> None:
    # Summing the P75 of three routes would be meaningless, and a share of that
    # sum doubly so.
    text = format_table(grouped_result(), time_range=TIME_RANGE)
    assert "TOTAL" not in text
    assert "%" not in text
    assert "8340" not in text


def test_a_grouped_percentile_table_formats_the_metric_in_its_own_unit() -> None:
    text = format_table(grouped_result(), time_range=TIME_RANGE)
    lines = text.splitlines()
    assert lines[2].split() == ["route", "p75_lcp", "data_points"]
    assert "4.1 s" in text and "3.0 s" in text and "1.2 s" in text
    # The count column beside it is a plain number, not a duration.
    assert "1,830" in text and "8,800" in text
    assert "1.8 s" not in text


def test_a_grouped_table_names_the_metric_and_its_target_underneath() -> None:
    text = format_table(grouped_result(), time_range=TIME_RANGE)
    assert f"Metric: {LCP_ID} (Largest Contentful Paint)" in text
    assert "Target: 2.5 s or less" in text
    assert "Lower is better for all five metrics." in text
    lowered = text.lower()
    for wording in THREE_TIER_WORDING:
        assert wording not in lowered


def test_a_data_point_table_keeps_its_totals_row_because_counts_do_add_up() -> None:
    result = si.normalize(
        SPEED_DATA_POINTS_PAYLOAD,
        metric=si.metric_for("lcp", data_points=True),
        aggregation="sum",
        group_by=["route"],
    )
    text = format_table(result, time_range=TIME_RANGE)
    assert "TOTAL" in text
    assert "10,630" in text
    assert "% sum_lcp_count" in text
    assert "one data point is one measurement" in text
    # A count has no published target, so nothing is compared against one.
    assert "Target:" not in text


def test_a_time_bucketed_table_labels_its_rows_with_the_bucket_start() -> None:
    result = si.normalize(
        SPEED_TREND_PAYLOAD,
        metric=si.validate_metric("lcp"),
        aggregation="p75",
        granularity="1d",
    )
    text = format_table(result, time_range=TIME_RANGE)
    # The header is the human spelling, so vitals-trend and the Web Analytics
    # trend head this column identically; the machine spelling "1d" stays in the
    # request body and in JSON output, where a consumer needs the real value.
    assert text.splitlines()[2].split()[0] == "day"
    assert result.granularity == "1d"
    assert "2026-08-10" in text and "2026-08-11" in text
    assert "T00:00:00.000Z" not in text
    assert "2.1 s" in text and "2.5 s" in text


def test_an_ungrouped_speed_result_renders_as_a_labelled_block_in_its_unit() -> None:
    result = si.normalize(
        speed_value_payload(INP_ID, 168.0, 900),
        metric=si.validate_metric("inp"),
        aggregation="p75",
    )
    text = format_table(result, time_range=TIME_RANGE)
    assert "p75_inp" in text
    assert "168 ms" in text
    assert "900" in text
    assert "TOTAL" not in text


def test_csv_of_a_speed_result_writes_raw_numbers_not_formatted_ones() -> None:
    rows = list(csv.reader(io.StringIO(format_csv(grouped_result()))))
    assert rows[0] == ["route", "p75_lcp", "data_points"]
    assert rows[1] == ["/blog/[slug]", "4120.0", "1830.0"]
    assert all("s" not in cell for cell in rows[1][1:])


# ---------------------------------------------------------------------------
# 5. The Others overflow bucket, on this surface too
# ---------------------------------------------------------------------------


def others_result() -> Result:
    return si.normalize(
        SPEED_ROUTE_WITH_OTHERS_PAYLOAD,
        metric=si.validate_metric("lcp"),
        aggregation="p75",
        group_by=["route"],
    )


def test_a_speed_table_labels_the_overflow_bucket_and_explains_it() -> None:
    text = format_table(others_result(), time_range=TIME_RANGE, limit=2)
    lines = text.splitlines()
    assert lines[2].split() == ["route", "p75_lcp", "data_points"]
    assert [line.split()[0] for line in lines[4:7]] == [
        "/blog/[slug]",
        "/pricing",
        "Others",
    ]
    assert "Others is not a real value" in text
    assert "--limit 2" in text
    assert "collapsed by the API into one bucket" in text


def test_a_speed_table_without_an_overflow_bucket_prints_no_such_note() -> None:
    text = format_table(grouped_result(), time_range=TIME_RANGE, limit=10)
    assert "Others" not in text
    assert "is not a real value" not in text


def test_the_speed_overflow_bucket_survives_csv_and_json_as_a_labelled_row() -> None:
    rows = list(csv.reader(io.StringIO(format_csv(others_result()))))
    assert rows[3] == ["Others", "1240.0", "8800.0"]
    document = json.loads(format_json(others_result(), SPEED_ROUTE_WITH_OTHERS_PAYLOAD))
    assert [row["key"] for row in document["rows"]] == [
        "/blog/[slug]",
        "/pricing",
        "Others",
    ]


# ---------------------------------------------------------------------------
# 6. A vitals table of mixed metric kinds
# ---------------------------------------------------------------------------
#
# render_vitals decides two things per table rather than per row: whether to
# show the target and verdict columns at all, and which legend to print. A run
# of all values and a run of all data point counts agree about both, so only a
# mixed list tells the two rules apart.


def mixed_results() -> list[Result]:
    """One value metric and one data point count metric, in that order."""
    return [
        si.normalize(
            speed_value_payload(LCP_ID, 2412.0, 12480),
            metric=si.validate_metric("lcp"),
            aggregation="p75",
        ),
        si.normalize(
            speed_value_payload(LCP_COUNT_ID, 12480),
            metric=si.metric_for("lcp", data_points=True),
            aggregation="sum",
        ),
    ]


def test_a_mixed_vitals_table_keeps_the_target_columns_for_the_metric_that_has_one() -> (
    None
):
    # One published target among the results is enough to earn the columns: the
    # metric that has none reads "n/a" rather than costing the other its verdict.
    text = render_vitals(mixed_results(), project=PROJECT, time_range=TIME_RANGE)
    header = text.splitlines()[3]
    assert "target" in header
    assert "verdict" in header
    lines = {line.split("  ")[0].strip(): line for line in text.splitlines()[5:7]}
    assert VERDICT_MEETS in lines["Largest Contentful Paint"]
    assert "2.5 s" in lines["Largest Contentful Paint"]
    assert VERDICT_UNKNOWN in lines["Largest Contentful Paint data points"]
    assert "n/a" in lines["Largest Contentful Paint data points"]


def test_a_mixed_vitals_table_keeps_the_web_vital_legend_not_the_count_one() -> None:
    # The data point legend replaces the vitals one only when there is no metric
    # value in the table at all; one value metric present means the reader still
    # needs "lower is better" and the two tier verdict explained.
    text = render_vitals(mixed_results(), project=PROJECT, time_range=TIME_RANGE)
    assert "Lower is better for all five metrics." in text
    assert "two tier" in text
    assert "one data point is one measurement" not in text


def test_a_vitals_table_of_only_counts_still_swaps_both_rules_together() -> None:
    # The control for the two tests above: all counts, so no targets and the
    # data point legend.
    results = [mixed_results()[1]]
    text = render_vitals(results, project=PROJECT, time_range=TIME_RANGE)
    assert "target" not in text.splitlines()[3]
    assert "verdict" not in text.splitlines()[3]
    assert "one data point is one measurement" in text
    assert "Lower is better for all five metrics." not in text


# ---------------------------------------------------------------------------
# 7. Control characters in a response derived label
# ---------------------------------------------------------------------------


def control_character_result() -> Result:
    payload = {
        "version": 1,
        "query": {"metric": LCP_ID, "groupBy": ["route"]},
        "data": [{"route": ANSI_ROUTE, "value": 1200.0}],
    }
    return si.normalize(
        payload,
        metric=si.validate_metric("lcp"),
        aggregation="p75",
        group_by=["route"],
    )


def test_a_route_label_carrying_an_escape_sequence_is_neutralised() -> None:
    result = control_character_result()
    assert result.rows[0].key == ESCAPED_ANSI_ROUTE
    text = format_table(result, time_range=TIME_RANGE)
    assert ESCAPED_ANSI_ROUTE in text
    assert "\x1b[2J" not in text
    rows = list(csv.reader(io.StringIO(format_csv(result))))
    assert rows[1][0] == ESCAPED_ANSI_ROUTE


def test_a_bucket_label_carrying_an_escape_sequence_is_neutralised_too() -> None:
    # A timestamp is remote input rendered into the same cell as any label, and
    # an unparseable one is printed through rather than dropped.
    payload = {
        "version": 1,
        "query": {"metric": LCP_ID},
        "data": [{"timestamp": ANSI_BUCKET, "value": 1200.0}],
    }
    result = si.normalize(
        payload, metric=si.validate_metric("lcp"), aggregation="p75", granularity="1d"
    )
    assert result.rows[0].timestamp == ESCAPED_ANSI_BUCKET
    text = format_table(result, time_range=TIME_RANGE)
    assert ESCAPED_ANSI_BUCKET in text
    assert "\x1b" not in text
