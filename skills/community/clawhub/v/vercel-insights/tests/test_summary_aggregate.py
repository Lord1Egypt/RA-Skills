"""The window aggregate comes from the server's summary, never from the rows.

Fixtures here are the shape a live account actually returned, and the numbers
are the ones it actually produced. That matters because this bug was invisible
to every mocked test written before it: the client displayed the first bucket as
though it were the window, reading 6.7 seconds where the true figure was 2.9,
landing the verdict on the wrong side of the published target.

A percentile does not average. The P75 of 168 hourly P75s is not the P75 of the
week, so there is no correct client-side derivation and the server's own summary
is the only honest source.
"""

from __future__ import annotations

import pytest
from helpers import TOKEN, FakeResponse, FakeSession

from vercel_insights import render
from vercel_insights import speedinsights as si

LCP = si.validate_metric("lcp")

#: Hourly buckets plus the window summary, exactly as the API returns them.
LIVE_SHAPE = {
    "query": {"granularity": {"hours": 1}},
    "data": [
        {"timestamp": "2026-08-08T20:00:00.000Z", "vercel_speed_insights_lcp_ms_p75": 6708},
        {"timestamp": "2026-08-09T00:00:00.000Z", "vercel_speed_insights_lcp_ms_p75": 3868},
        {"timestamp": "2026-08-15T19:00:00.000Z", "vercel_speed_insights_lcp_ms_p75": 1948},
    ],
    "summary": [{"vercel_speed_insights_lcp_ms_p75": 2908}],
    "orderBy": "vercel_speed_insights_lcp_ms_p75",
}


def test_the_rollup_key_is_computed_not_guessed() -> None:
    # The metric id with dots as underscores, then the aggregation. Computing it
    # beats probing a row for a lone number, which cannot tell two apart.
    assert si.rollup_key(LCP, "p75") == "vercel_speed_insights_lcp_ms_p75"
    assert si.rollup_key(si.validate_metric("cls"), "p90") == (
        "vercel_speed_insights_cls_p90"
    )


def test_the_summary_is_read_from_the_response() -> None:
    assert si.summary_value(LIVE_SHAPE, LCP, "p75") == pytest.approx(2908.0)


def test_an_ungrouped_result_reports_the_window_not_the_first_bucket() -> None:
    result = si.normalize(LIVE_SHAPE, metric=LCP, aggregation="p75")
    assert len(result.rows) == 1
    value = result.rows[0].metrics["p75_lcp"]
    assert value == pytest.approx(2908.0)
    # The exact regression: 6708 was the first bucket and was shown as the week.
    assert value != pytest.approx(6708.0)


def test_the_verdict_follows_the_window_value() -> None:
    # 6708 is over the 2500 target and 2908 is too, but the margin is the whole
    # point: a wrong headline number produces a wrong conclusion about the site.
    text = render.format_table(si.normalize(LIVE_SHAPE, metric=LCP, aggregation="p75"))
    assert "2.9 s" in text
    assert "6.7 s" not in text


def test_a_requested_granularity_keeps_the_time_series() -> None:
    # vitals-trend asks for buckets on purpose; collapsing them would defeat it.
    result = si.normalize(LIVE_SHAPE, metric=LCP, aggregation="p75", granularity="1d")
    assert len(result.rows) == 3
    assert [row.metrics["p75_lcp"] for row in result.rows] == [6708.0, 3868.0, 1948.0]


def test_a_grouped_result_keeps_its_groups() -> None:
    # A summary alongside grouped rows describes the whole, not each group.
    payload = {
        "data": [
            {"route": "/", "vercel_speed_insights_lcp_ms_p75": 4000},
            {"route": "/pricing", "vercel_speed_insights_lcp_ms_p75": 2000},
        ],
        "summary": [{"vercel_speed_insights_lcp_ms_p75": 2908}],
    }
    result = si.normalize(payload, metric=LCP, aggregation="p75", group_by=["route"])
    assert len(result.rows) == 2
    assert [row.key for row in result.rows] == ["/", "/pricing"]


def test_a_response_with_no_summary_still_works() -> None:
    payload = {"data": [{"vercel_speed_insights_lcp_ms_p75": 1234}]}
    result = si.normalize(payload, metric=LCP, aggregation="p75")
    assert result.rows[0].metrics["p75_lcp"] == pytest.approx(1234.0)


def test_an_ambiguous_summary_is_not_guessed_at() -> None:
    payload = {
        "data": [{"vercel_speed_insights_lcp_ms_p75": 1234}],
        "summary": [{"something": 1.0, "else": 2.0}],
    }
    assert si.summary_value(payload, LCP, "p75") is None


def test_data_point_counts_are_summed_across_buckets() -> None:
    # Counts do add up, unlike the percentile they support.
    payload = {
        "data": [
            {
                "timestamp": "2026-08-08T00:00:00.000Z",
                "vercel_speed_insights_lcp_ms_p75": 1,
                "count": 10,
            },
            {
                "timestamp": "2026-08-09T00:00:00.000Z",
                "vercel_speed_insights_lcp_ms_p75": 2,
                "count": 15,
            },
        ],
        "summary": [{"vercel_speed_insights_lcp_ms_p75": 3}],
    }
    result = si.normalize(payload, metric=LCP, aggregation="p75")
    assert result.rows[0].metrics[render.DATA_POINTS_METRIC] == pytest.approx(25.0)


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
def test_granularity_uses_the_verified_unit_and_count_shape(
    interval: str, expected: dict[str, int]
) -> None:
    # The API refused {"interval": "1d"} outright: a granularity "must divide a
    # day evenly or be a single week, month or year".
    assert si.build_granularity(interval) == expected


def test_vitals_end_to_end_reports_the_window(cli) -> None:  # type: ignore[no-untyped-def]
    session = FakeSession(*[FakeResponse(200, LIVE_SHAPE) for _ in range(5)])
    code, out, err = cli.run(
        ["vitals", "--since", "2026-08-08", "--until", "2026-08-15"],
        env={"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": "prj_x", "VERCEL_OWNER_ID": "own_x"},
        session=session,
    )
    assert code == 0, err
    assert "2.9 s" in out
    assert "6.7 s" not in out
