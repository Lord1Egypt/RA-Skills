"""Querying metrics beyond the web vitals.

The observability API serves every Vercel metric, not only Speed Insights:
function invocations, edge requests, cache results, firewall actions, AI gateway
usage and so on. This client can query any of them.

Their ids are deliberately not enumerated in the source. The schema endpoint is
the source of truth for what an account can reach, `--list-metrics` prints it,
and a hardcoded copy would go stale the moment Vercel adds one. What the client
carries records for is the five web vitals, because those have published units
and targets that make a verdict possible; everything else is queried honestly as
an unknown quantity.

NOTE ON VERIFICATION. The vitals path is verified end to end against a live
account. The metrics below are not, because they require Observability Plus,
which the account used for testing does not have. The ids here come from a real
`vercel metrics schema` listing, so they are real, but no query using them has
ever been answered.
"""

from __future__ import annotations

import pytest
from conftest import Cli
from helpers import TOKEN, FakeResponse, FakeSession

from vercel_insights.speedinsights import METRICS, validate_metric

ENV = {"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": "prj_x", "VERCEL_OWNER_ID": "own_x"}
DRY = ["--project", "prj_x", "--owner-id", "own_x", "--dry-run"]

#: Real ids, taken from a live `vercel metrics schema` listing.
REAL_IDS = [
    "vercel.function_invocation.count",
    "vercel.function_invocation.function_duration_ms",
    "vercel.request.count",
    "vercel.firewall_action.count",
    "vercel.image_transformation.count",
    "vercel.isr_operation.read_units",
    "vercel.analytics_pageview.count",
]


def _body(out: str) -> dict[str, object]:
    import json

    start = out.find("{", out.find("JSON body"))
    depth, end = 0, start
    for i, ch in enumerate(out[start:], start):
        depth += (ch == "{") - (ch == "}")
        if depth == 0:
            end = i + 1
            break
    return dict(json.loads(out[start:end]))


@pytest.mark.parametrize("metric_id", REAL_IDS)
def test_any_documented_metric_id_is_queryable(cli: Cli, metric_id: str) -> None:
    code, out, err = cli.run(["--metric", metric_id, *DRY], env={}, session=None)
    assert code == 0, err
    assert _body(out)["metric"] == metric_id


def test_naming_a_metric_needs_no_preset(cli: Cli) -> None:
    # The default preset reports traffic, a different API entirely. Requiring an
    # unrelated speed preset first would read like a workaround, because it is.
    code, out, err = cli.run(["--metric", "vercel.request.count", *DRY], env={}, session=None)
    assert code == 0, err
    assert _body(out)["metric"] == "vercel.request.count"


def test_no_aggregation_is_guessed_for_an_unknown_metric(cli: Cli) -> None:
    # The 75th percentile of a request count answers nothing. Omitting the field
    # lets the server apply the metric's own default, which the schema publishes
    # and this client would only be copying.
    code, out, err = cli.run(["--metric", "vercel.request.count", *DRY], env={}, session=None)
    assert code == 0, err
    assert "aggregation" not in _body(out)


def test_an_explicit_aggregation_is_still_sent(cli: Cli) -> None:
    code, out, err = cli.run(
        ["--metric", "vercel.request.count", "--aggregation", "sum", *DRY],
        env={},
        session=None,
    )
    assert code == 0, err
    assert _body(out)["aggregation"] == "sum"


def test_a_web_vital_still_defaults_to_p75(cli: Cli) -> None:
    code, out, err = cli.run(["--metric", "lcp", *DRY], env={}, session=None)
    assert code == 0, err
    assert _body(out)["aggregation"] == "p75"


def test_an_unknown_metric_accepts_a_dimension_this_client_cannot_check(
    cli: Cli,
) -> None:
    # There is no dimension list for a metric this client has no record of, and
    # inventing one would reject grouping the API supports. A wrong name comes
    # back as the API's own 400 rather than a guess made locally.
    code, out, err = cli.run(
        ["--metric", "vercel.request.count", "--group-by", "http_status", *DRY],
        env={},
        session=None,
    )
    assert code == 0, err
    assert _body(out)["groupBy"] == ["http_status"]


def test_a_web_vital_still_has_its_dimensions_checked(cli: Cli) -> None:
    # Where a list exists it is still enforced, so a typo is caught locally.
    code, _out, err = cli.run(
        ["--metric", "lcp", "--group-by", "http_status", *DRY], env={}, session=None
    )
    assert code == 2
    assert "unknown Speed Insights dimension" in err


def test_a_typo_in_a_short_name_is_still_caught(cli: Cli) -> None:
    # "lcpp" is not a metric id, so it goes down the suggestion path rather than
    # being passed to the API verbatim.
    code, _out, err = cli.run(["--metric", "lcpp", *DRY], env={}, session=None)
    assert code == 2
    assert "Did you mean 'lcp'?" in err


@pytest.mark.parametrize(
    "bad", ["vercel.request", "notvercel.request.count", "vercel..count", "vercel.a.b.c"]
)
def test_something_that_is_not_a_metric_id_is_refused(cli: Cli, bad: str) -> None:
    code, _out, err = cli.run(["--metric", bad, *DRY], env={}, session=None)
    assert code == 2
    assert "unknown metric" in err


def test_real_experience_score_is_still_refused(cli: Cli) -> None:
    code, _out, err = cli.run(["--metric", "res", *DRY], env={}, session=None)
    assert code == 2
    assert "not queryable" in err


def test_an_unknown_metric_carries_no_target_and_no_unit() -> None:
    # Nothing is invented: no published target means no verdict, and an unknown
    # unit means the value renders as a plain number rather than as seconds.
    metric = validate_metric("vercel.request.count")
    assert metric.target is None
    assert metric.unit is None
    assert metric.id not in METRICS


def test_an_unknown_metric_renders_without_a_verdict(cli: Cli) -> None:
    key = "vercel_request_count_sum"
    session = FakeSession(
        FakeResponse(200, {"data": [{key: 4821}], "summary": [{key: 4821}]})
    )
    code, out, err = cli.run(
        ["--metric", "vercel.request.count", "--aggregation", "sum"],
        env=dict(ENV),
        session=session,
    )
    assert code == 0, err
    assert "4,821" in out or "4821" in out
    assert "meets target" not in out
    assert "over target" not in out
