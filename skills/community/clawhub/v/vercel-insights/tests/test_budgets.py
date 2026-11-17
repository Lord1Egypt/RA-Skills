"""Performance budgets: a measurement compared against a limit, for CI.

Reporting a number helps a person reading a terminal. Failing a build helps a
team catch a regression before it ships, and that needs a threshold and an exit
code that means "over it".

The exit code is deliberately distinct from the one an API failure uses. A
failing budget is a successful run reporting bad news, and a CI step usually
wants to tell those apart.
"""

from __future__ import annotations

import json

import pytest
from conftest import Cli
from helpers import TOKEN, FakeResponse, FakeSession

from vercel_insights import ConfigError
from vercel_insights.budgets import BUDGET_EXCEEDED, Budget, parse_budget, parse_budgets
from vercel_insights.speedinsights import VITAL_ORDER

ENV = {"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": "prj_x", "VERCEL_OWNER_ID": "own_x"}
WINDOW = ["--since", "2026-08-07", "--until", "2026-08-14"]

#: One real P75 per vital. INP is just over its usual 200 ms target on purpose.
MEASURED = {
    "lcp_ms": 2412.0,
    "inp_ms": 205.0,
    "cls": 0.051,
    "fcp_ms": 1240.0,
    "ttfb_ms": 720.0,
}


def _responses() -> list[FakeResponse]:
    out = []
    for short in ("lcp_ms", "inp_ms", "cls", "fcp_ms", "ttfb_ms"):
        key = f"vercel_speed_insights_{short}_p75"
        value = MEASURED[short]
        out.append(
            FakeResponse(200, {"data": [{key: value}], "summary": [{key: value}]})
        )
    return out


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def test_a_budget_is_a_metric_and_a_limit() -> None:
    assert parse_budget("lcp=2500", VITAL_ORDER) == Budget(metric="lcp", limit=2500.0)
    assert parse_budget("CLS=0.1", VITAL_ORDER) == Budget(metric="cls", limit=0.1)


@pytest.mark.parametrize(
    ("text", "fragment"),
    [
        ("lcp", "NAME=VALUE"),
        ("=2500", "NAME=VALUE"),
        ("lcp=", "NAME=VALUE"),
        ("nope=1", "unknown metric"),
        ("lcp=fast", "non-numeric"),
        ("lcp=0", "greater than zero"),
        ("lcp=-5", "greater than zero"),
    ],
)
def test_a_bad_budget_says_what_is_wrong_and_what_is_accepted(
    text: str, fragment: str
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        parse_budget(text, VITAL_ORDER)
    assert fragment in str(excinfo.value)


def test_the_same_metric_twice_is_refused() -> None:
    with pytest.raises(ConfigError) as excinfo:
        parse_budgets(["lcp=2500", "lcp=3000"], VITAL_ORDER)
    assert "twice" in str(excinfo.value)


# ---------------------------------------------------------------------------
# End to end
# ---------------------------------------------------------------------------


def test_every_budget_met_exits_zero(cli: Cli) -> None:
    session = FakeSession(*_responses())
    code, out, err = cli.run(
        ["vitals", *WINDOW, "--budget", "lcp=2500", "--budget", "cls=0.1"],
        env=dict(ENV),
        session=session,
    )
    assert code == 0, err
    assert "pass" in out


def test_an_exceeded_budget_exits_three(cli: Cli) -> None:
    # 205 ms against a 200 ms limit. Distinct from exit 1, which means the API
    # failed: this run worked and is reporting bad news.
    session = FakeSession(*_responses())
    code, out, err = cli.run(
        ["vitals", *WINDOW, "--budget", "inp=200"], env=dict(ENV), session=session
    )
    assert code == BUDGET_EXCEEDED
    assert code != 1
    assert "fail" in out


def test_the_report_names_the_value_and_the_limit(cli: Cli) -> None:
    session = FakeSession(*_responses())
    code, out, _err = cli.run(
        ["vitals", *WINDOW, "--budget", "inp=200"], env=dict(ENV), session=session
    )
    assert code == BUDGET_EXCEEDED
    assert "205 ms" in out
    assert "200 ms" in out
    assert "Interaction to Next Paint" in out


@pytest.mark.parametrize(
    ("limit", "expected"),
    [(2412.0, "pass"), (2412.5, "pass"), (2411.9, "fail")],
    ids=["exactly-at-the-limit", "just-under", "just-over"],
)
def test_a_value_exactly_at_the_limit_passes(
    cli: Cli, limit: float, expected: str
) -> None:
    # Vercel phrases its own targets as "2.5 seconds or less", so the boundary
    # belongs to pass. Off by one here would fail builds that are exactly on
    # budget, which is the most annoying possible false alarm.
    session = FakeSession(*_responses())
    code, out, err = cli.run(
        ["vitals", *WINDOW, "--budget", f"lcp={limit}"], env=dict(ENV), session=session
    )
    assert (code == 0) is (expected == "pass"), err
    assert expected in out


def test_a_metric_with_no_data_does_not_fail_the_build(cli: Cli) -> None:
    # An empty window means the measurement is missing, not that the site got
    # slower. Failing on absent data trains people to ignore the check.
    session = FakeSession(*[FakeResponse(200, {"data": []}) for _ in range(5)])
    code, _out, err = cli.run(
        ["vitals", *WINDOW, "--budget", "lcp=2500"], env=dict(ENV), session=session
    )
    assert code == 0, err


def test_machine_output_stays_parseable_while_the_report_goes_to_stderr(
    cli: Cli,
) -> None:
    session = FakeSession(*_responses())
    code, out, err = cli.run(
        ["vitals", *WINDOW, "--json", "--budget", "inp=200"],
        env=dict(ENV),
        session=session,
    )
    assert code == BUDGET_EXCEEDED
    json.loads(out)  # stdout is still valid JSON
    assert "fail" in err


def test_a_grouped_query_refuses_a_budget(cli: Cli) -> None:
    # A budget compares one number against a limit; a grouped query has one per
    # group, so there is no single thing to compare.
    session = FakeSession(FakeResponse(200, {"data": []}))
    code, _out, err = cli.run(
        ["slowest-pages", *WINDOW, "--budget", "lcp=2500"],
        env=dict(ENV),
        session=session,
    )
    assert code == 2
    assert "grouped" in err


def test_no_budget_means_no_report_and_no_change(cli: Cli) -> None:
    session = FakeSession(*_responses())
    code, out, err = cli.run(["vitals", *WINDOW], env=dict(ENV), session=session)
    assert code == 0, err
    assert "Budgets" not in out
