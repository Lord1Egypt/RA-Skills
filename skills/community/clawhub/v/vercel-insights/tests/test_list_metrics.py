"""`--list-metrics` asks the API which metrics an account can actually query.

Vercel documents the schema endpoint as the source of truth for the metrics,
dimensions and aggregations available to an account, which makes it the right
thing to consult when a query is refused: it answers "does this metric exist for
me" outright rather than by inference. Its response shape is not published, so
the renderer reads defensively and says so when it cannot interpret one.
"""

from __future__ import annotations

import json

import pytest
from conftest import Cli
from helpers import TOKEN, FakeResponse, FakeSession

ENV = {"VERCEL_TOKEN": TOKEN}

LIST_SHAPE = [
    {
        "id": "vercel.speed_insights.lcp_ms",
        "description": "Largest Contentful Paint",
        "unit": "ms",
        "aggregations": ["p75", "p90", "p95", "p99"],
        "defaultAggregation": "p75",
        "dimensions": [{"name": "route", "label": "Route"}, {"name": "country"}],
    },
    {"id": "vercel.edge_requests.count", "unit": "count", "aggregations": ["sum"]},
]


def test_it_reaches_the_schema_endpoint_with_a_get(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, LIST_SHAPE))
    code, out, err = cli.run(["--list-metrics"], env=ENV, session=session)
    assert code == 0, err
    assert len(session.calls) == 1
    call = session.calls[0]
    assert call["method"] == "GET"
    assert call["url"] == "https://api.vercel.com/v2/observability/schema"
    assert "vercel.speed_insights.lcp_ms" in out


def test_it_needs_no_project_and_no_owner(cli: Cli) -> None:
    # The whole point is that it works when a query cannot even be built.
    session = FakeSession(FakeResponse(200, LIST_SHAPE))
    code, _out, err = cli.run(["--list-metrics"], env=ENV, session=session)
    assert code == 0, err


def test_a_prefix_filters_the_listing(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, LIST_SHAPE))
    code, out, err = cli.run(
        ["--list-metrics", "vercel.speed_insights"], env=ENV, session=session
    )
    assert code == 0, err
    assert "vercel.speed_insights.lcp_ms" in out
    assert "vercel.edge_requests.count" not in out


def test_it_renders_units_aggregations_and_dimensions(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, LIST_SHAPE))
    code, out, err = cli.run(["--list-metrics"], env=ENV, session=session)
    assert code == 0, err
    assert "p75" in out and "p99" in out
    assert "route" in out and "country" in out
    assert "ms" in out


@pytest.mark.parametrize(
    "payload",
    [
        {"metrics": LIST_SHAPE},
        {"data": LIST_SHAPE},
        {"vercel.speed_insights.lcp_ms": {"unit": "ms", "aggregations": ["p75"]}},
    ],
    ids=["metrics-key", "data-key", "keyed-by-id"],
)
def test_it_reads_the_plausible_unpublished_shapes(cli: Cli, payload: object) -> None:
    session = FakeSession(FakeResponse(200, payload))
    code, out, err = cli.run(["--list-metrics"], env=ENV, session=session)
    assert code == 0, err
    assert "vercel.speed_insights.lcp_ms" in out


def test_an_unrecognisable_shape_says_so_rather_than_guessing(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, {"unexpected": "totally"}))
    code, out, err = cli.run(["--list-metrics"], env=ENV, session=session)
    assert code == 0, err
    assert "not in a shape this client recognises" in out
    assert "--json" in out


def test_an_empty_listing_explains_what_that_means(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, []))
    code, out, err = cli.run(["--list-metrics"], env=ENV, session=session)
    assert code == 0, err
    assert "no queryable metrics" in out
    assert "Speed Insights is enabled" in out


def test_json_prints_the_untouched_payload(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, LIST_SHAPE))
    code, out, err = cli.run(["--list-metrics", "--json"], env=ENV, session=session)
    assert code == 0, err
    assert json.loads(out) == LIST_SHAPE


def test_a_dry_run_sends_nothing_and_needs_no_token(cli: Cli) -> None:
    code, out, err = cli.run(["--list-metrics", "--dry-run"], env={}, session=None)
    assert code == 0, err
    assert "/v2/observability/schema" in out
    assert TOKEN not in out


def test_an_api_error_surfaces_verbatim_and_exits_one(cli: Cli) -> None:
    body = {"error": {"code": "forbidden", "message": "Not authorized"}}
    session = FakeSession(FakeResponse(403, body))
    code, _out, err = cli.run(["--list-metrics"], env=ENV, session=session)
    assert code == 1
    assert "Not authorized" in err


def test_the_token_never_reaches_the_listing(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, LIST_SHAPE))
    code, out, err = cli.run(["--list-metrics"], env=ENV, session=session)
    assert code == 0
    assert TOKEN not in out and TOKEN not in err
