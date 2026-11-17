"""Tests for vercel_insights/cli.py: validation rules, main() and wiring."""

from __future__ import annotations

import csv
import io
import json
import re
from typing import Any

import pytest
import requests
from conftest import Cli
from helpers import (
    BASE_ENV,
    DAILY_PAYLOAD,
    DRY_RUN_ENV,
    EMPTY_AGGREGATE_PAYLOAD,
    EVENT_DATA_PAYLOAD,
    PROJECT,
    REFERRERS_PAYLOAD,
    REPO_ROOT,
    TOKEN,
    TOP_PAGES_PAYLOAD,
    VISITS_COUNT_PAYLOAD,
    WEB_ANALYTICS_BASE,
    FakeResponse,
    FakeSession,
    dry_run_calls,
    dry_run_values,
    error_payload,
    prepared,
)

from vercel_insights import VERSION
from vercel_insights import cli as vi_cli
from vercel_insights.http import DEFAULT_TIMEOUT
from vercel_insights.timerange import TIME_GRANULARITIES

# ---------------------------------------------------------------------------
# 1. Validation rules from docs/cli-contract.md
# ---------------------------------------------------------------------------

CONFIG_ERROR_CASES: list[tuple[str, list[str], dict[str, str], list[str]]] = [
    (
        "rule1-missing-project",
        ["top-pages"],
        {"VERCEL_TOKEN": TOKEN},
        ["--project", "VERCEL_PROJECT_ID"],
    ),
    (
        "rule2-missing-token",
        ["top-pages"],
        {"VERCEL_PROJECT_ID": PROJECT},
        ["--token", "VERCEL_TOKEN", "--dry-run", "vercel.com/docs"],
    ),
    (
        "rule3-team-and-team-slug",
        ["top-pages", "--team", "team_abc", "--team-slug", "acme"],
        dict(BASE_ENV),
        ["--team", "--team-slug", "mutually", "team_abc", "acme"],
    ),
    (
        "rule4-more-than-two-group-by",
        [
            "top-pages",
            "--group-by",
            "country",
            "--group-by",
            "deviceType",
            "--group-by",
            "browserName",
        ],
        dict(BASE_ENV),
        ["maximum of 2", "drop"],
    ),
    (
        "rule5-two-time-granularities",
        ["trend", "--group-by", "day", "--group-by", "week"],
        dict(BASE_ENV),
        ["at most one time granularity", "hour, day, week, month, year"],
    ),
    (
        "rule6-unknown-dimension",
        ["top-pages", "--group-by", "countries"],
        dict(BASE_ENV),
        ["unknown dimension", "'countries'", "Valid dimensions", "requestPath"],
    ),
    (
        "rule7-event-data-grouping-on-visits",
        ["top-pages", "--group-by", "eventData/plan"],
        dict(BASE_ENV),
        ["eventData/plan", "--dataset events"],
    ),
    (
        "rule7-event-property-on-visits",
        ["top-pages", "--event-property", "plan"],
        dict(BASE_ENV),
        ["--dataset events"],
    ),
    (
        "rule7-event-name-on-visits",
        ["top-pages", "--event-name", "signup"],
        dict(BASE_ENV),
        ["--event-name", "--dataset events"],
    ),
    (
        "rule8-limit-zero",
        ["top-pages", "--limit", "0"],
        dict(BASE_ENV),
        ["--limit 0", "1 to 100", "Others"],
    ),
    (
        "rule8-limit-101",
        ["top-pages", "--limit", "101"],
        dict(BASE_ENV),
        ["--limit 101", "1 to 100", "Others"],
    ),
    (
        "rule9-preview-environment-on-a-count-query",
        ["total", "--environment", "preview"],
        dict(BASE_ENV),
        ["--environment preview", "production", "--group-by day"],
    ),
    (
        "rule10-json-with-csv",
        ["top-pages", "--json", "--csv"],
        dict(BASE_ENV),
        ["--json", "--csv", "mutually exclusive"],
    ),
    (
        "rule11-since-not-before-until",
        ["top-pages", "--since", "now", "--until", "7d"],
        dict(BASE_ENV),
        ["--since must be strictly earlier than --until"],
    ),
    (
        # An empty value is a value: it has to reach the time parser and be
        # refused there. Quietly reading it as "nobody asked" would report the
        # default window as though the user had chosen it.
        "empty-since",
        ["top-pages", "--since", ""],
        dict(BASE_ENV),
        ["empty time value"],
    ),
    (
        "empty-until",
        ["top-pages", "--until", ""],
        dict(BASE_ENV),
        ["empty time value"],
    ),
    (
        "rule13-flag-without-equals",
        ["top-pages", "--flag", "beta_banner"],
        dict(BASE_ENV),
        ["--flag", "NAME=VALUE", "beta_banner=true"],
    ),
]


@pytest.mark.parametrize(
    ("argv", "env", "fragments"),
    [case[1:] for case in CONFIG_ERROR_CASES],
    ids=[case[0] for case in CONFIG_ERROR_CASES],
)
def test_config_errors_exit_two_and_name_the_fix(
    cli: Cli, argv: list[str], env: dict[str, str], fragments: list[str]
) -> None:
    code, out, err = cli.run(argv, env=env)
    assert code == 2
    assert out == ""
    assert err.startswith("error: ")
    assert "Traceback" not in err
    for fragment in fragments:
        assert fragment in err, f"{fragment!r} missing from {err!r}"


def test_rule12_an_old_since_warns_on_stderr_and_still_succeeds(cli: Cli) -> None:
    code, out, err = cli.run(
        ["top-pages", "--since", "2000-01-01", "--dry-run"],
        env={"VERCEL_PROJECT_ID": PROJECT},
    )
    assert code == 0
    assert "warning:" in err
    assert "reporting window" in err
    assert "2000-01-01T00:00:00Z" in out


def test_overview_rejects_csv_and_an_overridden_grouping(cli: Cli) -> None:
    code, _, err = cli.run(["overview", "--csv"], env=dict(BASE_ENV))
    assert code == 2
    assert "overview" in err and "--csv" in err

    code, _, err = cli.run(["overview", "--group-by", "country"], env=dict(BASE_ENV))
    assert code == 2
    assert "--group-by" in err


def test_an_out_of_range_since_exits_two_without_a_traceback(cli: Cli) -> None:
    code, out, err = cli.run(
        ["top-pages", "--since", "99999999999999999", "--dry-run"],
        env=dict(DRY_RUN_ENV),
    )
    assert code == 2
    assert out == ""
    assert "Traceback" not in err
    assert "representable range" in err


@pytest.mark.parametrize("value", ["0", "-1", "-0.5", "1e400", "nan", "0.0"])
def test_a_bad_timeout_is_a_config_error_rather_than_a_traceback(
    cli: Cli, value: str
) -> None:
    code, out, err = cli.run(
        ["top-pages", "--timeout", value, "--dry-run"], env=dict(DRY_RUN_ENV)
    )
    assert code == 2
    assert out == ""
    assert "Traceback" not in err
    assert "--timeout" in err


# ---------------------------------------------------------------------------
# 2. main() end to end
# ---------------------------------------------------------------------------


def test_main_runs_top_pages_and_prints_a_table(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, TOP_PAGES_PAYLOAD))
    code, out, err = cli.run(
        ["top-pages", "--since", "7d", "--limit", "10"],
        env=dict(BASE_ENV),
        session=session,
    )
    assert code == 0
    assert err == ""
    assert len(session.calls) == 1
    assert session.calls[0]["method"] == "GET"
    assert session.calls[0]["url"] == f"{WEB_ANALYTICS_BASE}/visits/aggregate"
    assert ("by", "requestPath") in session.calls[0]["params"]
    assert ("limit", "10") in session.calls[0]["params"]
    assert session.calls[0]["headers"]["Authorization"] == f"Bearer {TOKEN}"
    assert "/pricing" in out and "640" in out
    assert "TOTAL" in out and "820" in out
    assert session.closed is True


def test_main_top_pages_as_csv_parses_back(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, TOP_PAGES_PAYLOAD))
    code, out, _ = cli.run(["top-pages", "--csv"], env=dict(BASE_ENV), session=session)
    assert code == 0
    assert list(csv.reader(io.StringIO(out))) == [
        ["requestPath", "pageviews", "visitors"],
        ["/pricing", "640", "510"],
        ["/blog/my-post", "180", "150"],
    ]


def test_main_top_pages_as_json_includes_the_raw_payload(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, TOP_PAGES_PAYLOAD))
    code, out, _ = cli.run(["top-pages", "--json"], env=dict(BASE_ENV), session=session)
    assert code == 0
    document = json.loads(out)
    assert document["raw"] == TOP_PAGES_PAYLOAD
    assert document["totals"]["pageviews"] == 820


def test_main_total_preset_uses_the_count_endpoint(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, VISITS_COUNT_PAYLOAD))
    code, out, _ = cli.run(["total"], env=dict(BASE_ENV), session=session)
    assert code == 0
    assert session.calls[0]["url"] == f"{WEB_ANALYTICS_BASE}/visits/count"
    assert all(name != "by" for name, _ in session.calls[0]["params"])
    assert "1,250" in out


def test_main_overview_issues_exactly_three_get_requests(cli: Cli) -> None:
    session = FakeSession(
        FakeResponse(200, DAILY_PAYLOAD),
        FakeResponse(200, TOP_PAGES_PAYLOAD),
        FakeResponse(200, REFERRERS_PAYLOAD),
    )
    code, out, err = cli.run([], env=dict(BASE_ENV), session=session)
    assert code == 0
    assert err == ""
    assert len(session.calls) == 3
    assert all(call["method"] == "GET" for call in session.calls)
    grouped = [
        [value for name, value in call["params"] if name == "by"]
        for call in session.calls
    ]
    assert grouped == [["day"], ["requestPath"], ["referrerHostname"]]
    assert all(
        call["url"] == f"{WEB_ANALYTICS_BASE}/visits/aggregate"
        for call in session.calls
    )
    assert f"Vercel Web Analytics: {PROJECT}" in out
    assert "By day" in out
    assert "Top pages" in out and "Top referrers" in out


def test_main_overview_as_json_has_the_three_named_sections(cli: Cli) -> None:
    session = FakeSession(
        FakeResponse(200, DAILY_PAYLOAD),
        FakeResponse(200, TOP_PAGES_PAYLOAD),
        FakeResponse(200, REFERRERS_PAYLOAD),
    )
    code, out, _ = cli.run(["overview", "--json"], env=dict(BASE_ENV), session=session)
    assert code == 0
    document = json.loads(out)
    assert set(document["sections"]) == {"byGranularity", "topPages", "topReferrers"}
    assert document["sections"]["topPages"]["rows"][0]["key"] == "/pricing"


def test_main_exits_zero_on_an_empty_result(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, EMPTY_AGGREGATE_PAYLOAD))
    code, out, err = cli.run(["top-pages"], env=dict(BASE_ENV), session=session)
    assert code == 0
    assert err == ""
    assert "No visits data" in out
    assert "TOTAL" not in out


def test_the_empty_result_message_names_the_range_and_the_filter(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, EMPTY_AGGREGATE_PAYLOAD))
    code, out, err = cli.run(
        [
            "top-pages",
            "--since",
            "2026-08-01",
            "--until",
            "2026-08-08",
            "--country",
            "US",
        ],
        env=dict(BASE_ENV),
        session=session,
    )
    assert code == 0
    assert err == ""
    assert "No visits data for project prj_demo" in out
    assert "grouped by requestPath" in out
    assert "2026-08-01T00:00:00Z" in out and "2026-08-08T00:00:00Z" in out
    assert "country eq 'US'" in out
    assert "Try a wider --since" in out


def test_main_exits_one_on_an_api_error_and_repeats_the_message(cli: Cli) -> None:
    session = FakeSession(
        FakeResponse(
            403,
            error_payload("forbidden", "You do not have permission for this project"),
        )
    )
    code, out, err = cli.run(
        ["top-pages", "--max-retries", "0"], env=dict(BASE_ENV), session=session
    )
    assert code == 1
    assert out == ""
    assert "You do not have permission for this project" in err
    assert "HTTP 403" in err
    assert TOKEN not in err


def test_main_exits_one_on_a_rate_limit_with_a_hint(cli: Cli) -> None:
    body = error_payload(
        "rate_limited", "The rate limit of 6 exceeded", limit={"total": 6, "reset": 1}
    )
    session = FakeSession(FakeResponse(429, body))
    code, _, err = cli.run(
        ["top-pages", "--max-retries", "0"], env=dict(BASE_ENV), session=session
    )
    assert code == 1
    assert "The rate limit of 6 exceeded" in err
    assert "rate limits are per endpoint" in err


def test_main_exits_two_on_a_configuration_error(cli: Cli) -> None:
    code, out, err = cli.run(["top-pages"], env={"VERCEL_TOKEN": TOKEN})
    assert code == 2
    assert out == ""
    assert "--project" in err


def test_main_list_presets_prints_the_table_without_touching_the_network(
    cli: Cli,
) -> None:
    # The row contents are checked against hard-coded literals in
    # test_presets.py, deliberately not against PRESETS: a test that iterates
    # the same dict the renderer iterates cannot detect a wrong value in it.
    code, out, err = cli.run(["--list-presets"], env={})
    assert code == 0
    assert err == ""
    assert "overview" in out and "3 x aggregate" in out


def test_main_version_prints_the_version_and_exits_zero(cli: Cli) -> None:
    code, out, _ = cli.run(["--version"], env={})
    assert code == 0
    assert VERSION in out


def test_main_applies_filter_flags_to_the_query(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, TOP_PAGES_PAYLOAD))
    code, _, _ = cli.run(
        [
            "top-pages",
            "--country",
            "US,DE",
            "--path",
            "/pricing",
            "--flag",
            "beta=true",
        ],
        env=dict(BASE_ENV),
        session=session,
    )
    assert code == 0
    filters = [value for name, value in session.calls[0]["params"] if name == "filter"]
    assert filters == [
        "requestPath eq '/pricing' and country in ('US', 'DE') and flags/beta eq 'true'"
    ]


def test_main_events_preset_breaks_out_an_event_property(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, EVENT_DATA_PAYLOAD))
    code, out, _ = cli.run(
        ["events", "--event-property", "plan"], env=dict(BASE_ENV), session=session
    )
    assert code == 0
    grouped = [value for name, value in session.calls[0]["params"] if name == "by"]
    assert grouped == ["eventName", "eventData/plan"]
    assert session.calls[0]["url"] == f"{WEB_ANALYTICS_BASE}/events/aggregate"
    assert "pro" in out and "42" in out


def test_main_team_slug_is_sent_as_slug(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, TOP_PAGES_PAYLOAD))
    env = dict(BASE_ENV, VERCEL_TEAM_SLUG="acme")
    code, _, _ = cli.run(["top-pages"], env=env, session=session)
    assert code == 0
    assert ("slug", "acme") in session.calls[0]["params"]
    assert all(name != "teamId" for name, _ in session.calls[0]["params"])


def test_a_malformed_payload_exits_one_rather_than_rendering_something(
    cli: Cli,
) -> None:
    session = FakeSession(FakeResponse(200, text="<html>gateway timeout</html>"))
    code, out, err = cli.run(
        ["top-pages", "--max-retries", "0"], env=dict(BASE_ENV), session=session
    )
    assert code == 1
    assert out == ""
    assert "Traceback" not in err


@pytest.mark.parametrize("literal", ["NaN", "Infinity", "-Infinity"])
def test_a_body_carrying_a_non_standard_json_literal_exits_one_cleanly(
    cli: Cli, literal: str
) -> None:
    # json.loads would have read any of the three as a float, and a nan reaching
    # the renderer prints as "nan" and compares false against every target.
    body = f'{{"version": 1, "data": {{"pageviews": {literal}, "visitors": 3}}}}'
    session = FakeSession(FakeResponse(200, text=body))
    code, out, err = cli.run(
        ["total", "--max-retries", "0"], env=dict(BASE_ENV), session=session
    )
    assert code == 1
    assert out == ""
    assert "invalid_response" in err
    assert "NaN" in err
    assert "Traceback" not in err
    assert "nan" not in out


def test_an_aggregate_body_shaped_like_a_count_exits_one_instead_of_rendering(
    cli: Cli,
) -> None:
    payload = {"version": 1, "query": {}, "data": {"pageviews": 1250, "visitors": 980}}
    session = FakeSession(FakeResponse(200, payload))
    code, out, err = cli.run(
        ["top-pages", "--max-retries", "0"], env=dict(BASE_ENV), session=session
    )
    assert code == 1
    assert out == ""
    assert "invalid_response" in err
    assert "1,250" not in out
    assert "Traceback" not in err


def test_a_count_body_shaped_like_an_aggregate_exits_one(cli: Cli) -> None:
    payload = {"version": 1, "query": {}, "data": [{"pageviews": 5, "visitors": 4}]}
    session = FakeSession(FakeResponse(200, payload))
    code, out, err = cli.run(["total"], env=dict(BASE_ENV), session=session)
    assert code == 1
    assert out == ""
    assert "invalid_response" in err


# ---------------------------------------------------------------------------
# 3. Filter shorthands, one row per documented flag
# ---------------------------------------------------------------------------
#
# Everything below drives the real CLI with --dry-run and reads the request
# back out of the printed encoded URL, which is the string the tool promises is
# what would go on the wire. Asserting the whole parameter value means a flag
# wired to the wrong dimension (--browser building an osName clause, say) fails
# here instead of returning a confidently formatted wrong number.

# (flag, argv, the exact OData clause it must produce). Every row of the flag
# table in docs/cli-contract.md appears here.
FILTER_SHORTHAND_CASES: list[tuple[str, list[str], str]] = [
    ("--path", ["top-pages", "--path", "/pricing"], "requestPath eq '/pricing'"),
    ("--route", ["top-routes", "--route", "/blog/[slug]"], "route eq '/blog/[slug]'"),
    ("--country", ["countries", "--country", "US"], "country eq 'US'"),
    ("--device", ["devices", "--device", "mobile"], "deviceType eq 'mobile'"),
    ("--browser", ["browsers", "--browser", "Chrome"], "browserName eq 'Chrome'"),
    ("--os", ["operating-systems", "--os", "macOS"], "osName eq 'macOS'"),
    (
        "--referrer",
        ["referrers", "--referrer", "news.ycombinator.com"],
        "referrerHostname eq 'news.ycombinator.com'",
    ),
    (
        "--utm-source",
        ["campaigns", "--utm-source", "newsletter"],
        "utmSource eq 'newsletter'",
    ),
    ("--utm-medium", ["campaigns", "--utm-medium", "email"], "utmMedium eq 'email'"),
    (
        "--utm-campaign",
        ["campaigns", "--utm-campaign", "launch"],
        "utmCampaign eq 'launch'",
    ),
    ("--event-name", ["events", "--event-name", "signup"], "eventName eq 'signup'"),
    (
        "--flag",
        ["top-pages", "--flag", "beta_banner=true"],
        "flags/beta_banner eq 'true'",
    ),
    (
        "--environment",
        ["top-pages", "--environment", "preview"],
        "environment eq 'preview'",
    ),
    (
        "--filter",
        ["top-pages", "--filter", "startswith(requestPath, '/docs')"],
        "startswith(requestPath, '/docs')",
    ),
]


@pytest.mark.parametrize(
    ("argv", "expected"),
    [case[1:] for case in FILTER_SHORTHAND_CASES],
    ids=[case[0] for case in FILTER_SHORTHAND_CASES],
)
def test_every_filter_shorthand_builds_exactly_its_documented_clause(
    cli: Cli, argv: list[str], expected: str
) -> None:
    code, out, err = cli.run([*argv, "--dry-run"], env=dict(DRY_RUN_ENV))
    assert code == 0, err
    assert dry_run_values(out, "filter") == [expected]


def test_two_filter_shorthands_are_joined_with_and(cli: Cli) -> None:
    code, out, err = cli.run(
        ["top-pages", "--country", "US", "--browser", "Chrome", "--dry-run"],
        env=dict(DRY_RUN_ENV),
    )
    assert code == 0, err
    assert dry_run_values(out, "filter") == [
        "country eq 'US' and browserName eq 'Chrome'"
    ]


def test_a_comma_separated_shorthand_value_becomes_an_in_clause(cli: Cli) -> None:
    code, out, err = cli.run(
        ["countries", "--country", "US,DE,FR", "--dry-run"], env=dict(DRY_RUN_ENV)
    )
    assert code == 0, err
    assert dry_run_values(out, "filter") == ["country in ('US', 'DE', 'FR')"]


def test_repeating_flag_and_filter_appends_a_clause_each_time(cli: Cli) -> None:
    code, out, err = cli.run(
        [
            "top-pages",
            "--flag",
            "beta_banner=true",
            "--flag",
            "new_nav=false",
            "--filter",
            "not (deviceType eq 'bot')",
            "--dry-run",
        ],
        env=dict(DRY_RUN_ENV),
    )
    assert code == 0, err
    assert dry_run_values(out, "filter") == [
        "flags/beta_banner eq 'true' and flags/new_nav eq 'false' "
        "and not (deviceType eq 'bot')"
    ]


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("plan", "eventData/plan"),
        ("beta_2", "eventData/beta_2"),
        ("sign-up", "eventData/'sign-up'"),
        ("'sign-up'", "eventData/'sign-up'"),
        ("'it''s'", "eventData/'it''s'"),
        ("a/b", "eventData/a/b"),
    ],
)
def test_a_legal_event_property_reaches_by_exactly_as_documented(
    cli: Cli, key: str, expected: str
) -> None:
    code, out, err = cli.run(
        ["events", "--event-property", key, "--dry-run"], env=dict(DRY_RUN_ENV)
    )
    assert code == 0, err
    assert dry_run_values(out, "by") == ["eventName", expected]


# ---------------------------------------------------------------------------
# 4. --granularity
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("granularity", list(TIME_GRANULARITIES))
def test_granularity_replaces_the_presets_time_bucket(
    cli: Cli, granularity: str
) -> None:
    # The preset supplies "day". Appending rather than replacing would send two
    # time granularities, which the API forbids and rule 5 rejects, so this
    # covers both the wiring and the replacement.
    code, out, err = cli.run(
        ["trend", "--granularity", granularity, "--dry-run"], env=dict(DRY_RUN_ENV)
    )
    assert code == 0, err
    assert dry_run_values(out, "by") == [granularity]


def test_granularity_is_appended_to_an_explicit_grouping(cli: Cli) -> None:
    code, out, err = cli.run(
        ["top-pages", "--group-by", "country", "--granularity", "day", "--dry-run"],
        env=dict(DRY_RUN_ENV),
    )
    assert code == 0, err
    assert dry_run_values(out, "by") == ["country", "day"]


def test_granularity_on_top_of_an_explicit_time_dimension_is_a_config_error(
    cli: Cli,
) -> None:
    code, _, err = cli.run(
        ["trend", "--group-by", "day", "--granularity", "week"], env=dict(BASE_ENV)
    )
    assert code == 2
    assert "at most one time granularity" in err


def test_granularity_rebuckets_the_overview_trend_section(cli: Cli) -> None:
    code, out, err = cli.run(
        ["overview", "--granularity", "week", "--dry-run"], env=dict(DRY_RUN_ENV)
    )
    assert code == 0, err
    assert dry_run_values(out, "by", call=0) == ["week"]


# Both vocabularies are accepted from the user, and Web Analytics understands
# only one of them. The alias has to be translated on the way to `by=`, which is
# a separate code path in the overview because that preset picks its own
# grouping rather than passing --group-by through.
GRANULARITY_ON_THE_WIRE: list[tuple[str, str]] = [
    ("hour", "hour"),
    ("1h", "hour"),
    ("day", "day"),
    ("1d", "day"),
    ("week", "week"),
    ("month", "month"),
    ("1mo", "month"),
    ("year", "year"),
]

#: Spellings that exist only in the Speed Insights vocabulary. None of them is
#: a legal Web Analytics `by` value, so none may ever reach one.
SPEED_ONLY_SPELLINGS = ["1h", "1d", "1mo"]


@pytest.mark.parametrize(
    ("value", "expected"),
    GRANULARITY_ON_THE_WIRE,
    ids=[case[0] for case in GRANULARITY_ON_THE_WIRE],
)
def test_the_overview_translates_either_granularity_vocabulary_for_its_trend(
    cli: Cli, value: str, expected: str
) -> None:
    code, out, err = cli.run(
        ["overview", "--granularity", value, "--dry-run"], env=dict(DRY_RUN_ENV)
    )
    assert code == 0, err
    calls = dry_run_calls(out)
    assert len(calls) == 3
    assert dry_run_values(out, "by", call=0) == [expected]
    # The other two overview sections are dimension grouped and unaffected.
    assert dry_run_values(out, "by", call=1) == ["requestPath"]
    assert dry_run_values(out, "by", call=2) == ["referrerHostname"]


@pytest.mark.parametrize(
    ("value", "expected"),
    GRANULARITY_ON_THE_WIRE,
    ids=[case[0] for case in GRANULARITY_ON_THE_WIRE],
)
def test_a_single_query_preset_translates_the_same_way_the_overview_does(
    cli: Cli, value: str, expected: str
) -> None:
    code, out, err = cli.run(
        ["trend", "--granularity", value, "--dry-run"], env=dict(DRY_RUN_ENV)
    )
    assert code == 0, err
    assert dry_run_values(out, "by") == [expected]


WEB_PRESETS_TAKING_A_GRANULARITY = [
    "overview",
    "trend",
    "top-pages",
    "top-routes",
    "referrers",
    "countries",
    "devices",
    "browsers",
    "operating-systems",
    "campaigns",
    "events",
    "total",
]


@pytest.mark.parametrize("preset", WEB_PRESETS_TAKING_A_GRANULARITY)
@pytest.mark.parametrize("value", SPEED_ONLY_SPELLINGS)
def test_no_speed_insights_spelling_ever_reaches_a_web_analytics_by_parameter(
    cli: Cli, preset: str, value: str
) -> None:
    # Every Web Analytics preset, every alias spelling, every request the run
    # plans: `by` may only ever carry a name Web Analytics itself documents.
    code, out, err = cli.run(
        [preset, "--granularity", value, "--dry-run"], env=dict(DRY_RUN_ENV)
    )
    assert code == 0, err
    sent = [
        item for _endpoint, params in dry_run_calls(out) for item in params
        if item[0] == "by"
    ]
    assert sent, f"{preset} sent no by parameter at all"
    for _name, dimension in sent:
        assert dimension not in SPEED_ONLY_SPELLINGS
        if dimension in ("hour", "day", "week", "month", "year"):
            assert dimension in TIME_GRANULARITIES


def test_the_overview_heading_reads_the_translated_bucket_not_the_alias(
    cli: Cli,
) -> None:
    daily = {
        "version": 1,
        "query": {"groupBy": ["day"]},
        "data": [
            {"timestamp": "2026-08-10T00:00:00.000Z", "pageviews": 9, "visitors": 7}
        ],
    }
    session = FakeSession(
        FakeResponse(200, daily),
        FakeResponse(200, TOP_PAGES_PAYLOAD),
        FakeResponse(200, REFERRERS_PAYLOAD),
    )
    code, out, err = cli.run(
        ["overview", "--granularity", "1d"], env=dict(BASE_ENV), session=session
    )
    assert code == 0, err
    assert "By day" in out
    assert "By 1d" not in out


def test_granularity_relabels_the_overview_trend_heading(cli: Cli) -> None:
    weekly = {
        "version": 1,
        "query": {"groupBy": ["week"]},
        "data": [
            {"timestamp": "2026-08-03T00:00:00.000Z", "pageviews": 9, "visitors": 7}
        ],
    }
    session = FakeSession(
        FakeResponse(200, weekly),
        FakeResponse(200, TOP_PAGES_PAYLOAD),
        FakeResponse(200, REFERRERS_PAYLOAD),
    )
    code, out, _ = cli.run(
        ["overview", "--granularity", "week"], env=dict(BASE_ENV), session=session
    )
    assert code == 0
    assert "By week" in out


# ---------------------------------------------------------------------------
# 5. Interruption
# ---------------------------------------------------------------------------


def test_a_keyboard_interrupt_exits_one_hundred_and_thirty(cli: Cli) -> None:
    session = FakeSession(KeyboardInterrupt())
    code, out, err = cli.run(["top-pages"], env=dict(BASE_ENV), session=session)
    assert code == 130
    assert out == ""
    assert "interrupted" in err
    assert "Traceback" not in err
    assert session.closed is True


def test_a_keyboard_interrupt_between_overview_requests_still_exits_one_thirty(
    cli: Cli,
) -> None:
    session = FakeSession(FakeResponse(200, DAILY_PAYLOAD), KeyboardInterrupt())
    code, _, err = cli.run([], env=dict(BASE_ENV), session=session)
    assert code == 130
    assert "interrupted" in err


# ---------------------------------------------------------------------------
# 6. --timeout, --no-color and NO_COLOR wiring
# ---------------------------------------------------------------------------


class TtyStream(io.StringIO):
    """A stdout that claims to be a terminal, so the colour path activates."""

    def isatty(self) -> bool:
        return True


ANSI = "\033["


@pytest.mark.parametrize("value", ["12.5", "0.25", "90"])
def test_the_cli_forwards_its_parsed_timeout_to_the_request(
    cli: Cli, value: str
) -> None:
    session = FakeSession(FakeResponse(200, TOP_PAGES_PAYLOAD))
    code, _, _ = cli.run(
        ["top-pages", "--timeout", value], env=dict(BASE_ENV), session=session
    )
    assert code == 0
    assert session.calls[0]["timeout"] == float(value)


def test_the_default_timeout_is_forwarded_when_the_flag_is_absent(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, TOP_PAGES_PAYLOAD))
    code, _, _ = cli.run(["top-pages"], env=dict(BASE_ENV), session=session)
    assert code == 0
    assert session.calls[0]["timeout"] == DEFAULT_TIMEOUT


def test_color_is_used_on_a_tty_with_no_color_unset() -> None:
    out, err = TtyStream(), io.StringIO()
    assert vi_cli.main(["--list-presets"], {}, out=out, err=err) == 0
    assert ANSI in out.getvalue()


@pytest.mark.parametrize(
    ("argv", "env"),
    [
        (["--list-presets", "--no-color"], {}),
        (["--list-presets"], {"NO_COLOR": "1"}),
        (["--list-presets"], {"NO_COLOR": ""}),
    ],
    ids=["--no-color", "NO_COLOR=1", "NO_COLOR-empty"],
)
def test_color_is_suppressed_by_the_flag_and_by_no_color(
    argv: list[str], env: dict[str, str]
) -> None:
    out, err = TtyStream(), io.StringIO()
    assert vi_cli.main(argv, env, out=out, err=err) == 0
    text = out.getvalue()
    if env.get("NO_COLOR") == "":
        # An empty NO_COLOR is falsy, so the TTY still gets colour. Pinning the
        # behaviour here keeps the env check honest either way.
        assert ANSI in text
    else:
        assert ANSI not in text
    assert "Presets" in text


def test_color_is_suppressed_when_stdout_is_not_a_tty() -> None:
    out, err = io.StringIO(), io.StringIO()
    assert vi_cli.main(["--list-presets"], {}, out=out, err=err) == 0
    assert ANSI not in out.getvalue()


def test_a_report_on_a_tty_is_coloured_and_the_same_report_piped_is_not(
    cli: Cli,
) -> None:
    tty_out, err = TtyStream(), io.StringIO()
    session = FakeSession(FakeResponse(200, TOP_PAGES_PAYLOAD))
    cli.monkeypatch.setattr(requests, "Session", lambda: session)
    assert vi_cli.main(["top-pages"], dict(BASE_ENV), out=tty_out, err=err) == 0
    assert ANSI in tty_out.getvalue()

    plain_out = io.StringIO()
    session2 = FakeSession(FakeResponse(200, TOP_PAGES_PAYLOAD))
    cli.monkeypatch.setattr(requests, "Session", lambda: session2)
    assert vi_cli.main(["top-pages"], dict(BASE_ENV), out=plain_out, err=err) == 0
    assert ANSI not in plain_out.getvalue()


# ---------------------------------------------------------------------------
# 7. Version consistency across the repo
# ---------------------------------------------------------------------------


def test_the_version_matches_pyproject_and_the_skill_frontmatter() -> None:
    # pyyaml is not a dependency, so the frontmatter is read with a regex; the
    # pyproject version is parsed properly. This drift has happened before.
    tomllib: Any = pytest.importorskip("tomllib", reason="tomllib needs Python 3.11")
    pyproject = tomllib.loads(
        (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert pyproject["project"]["version"] == VERSION

    skill = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = skill.split("---", 2)[1]
    match = re.search(r"^version:[ \t]*(\S+)[ \t]*$", frontmatter, re.MULTILINE)
    assert match is not None, "SKILL.md frontmatter has no version key"
    assert match.group(1) == VERSION


def test_the_version_is_reported_by_the_flag_and_the_user_agent(cli: Cli) -> None:
    code, out, _ = cli.run(["--version"], env={})
    assert code == 0
    assert out.strip() == f"vercel-insights {VERSION}"
    assert prepared().headers["User-Agent"] == f"vercel-insights-skill/{VERSION}"


# ---------------------------------------------------------------------------
# 8. Entry points
# ---------------------------------------------------------------------------


def test_both_entry_points_exist_and_the_module_form_is_importable() -> None:
    assert (REPO_ROOT / "vercel_insights" / "__main__.py").is_file()
    assert callable(vi_cli.main)


def test_the_parser_prog_is_the_renamed_command(cli: Cli) -> None:
    assert vi_cli.build_parser().prog == "vercel-insights"


def test_the_help_names_every_surface_and_what_a_limit_means_on_each() -> None:
    # The help doubles as the reference docs, so a surface the tool can query
    # but does not mention is a surface nobody finds. --limit is the one flag
    # whose meaning changes between them: groups on the analytics APIs, rows on
    # request logs, with a different ceiling.
    # Whitespace collapsed, because argparse wraps the help to the terminal and
    # a phrase would otherwise be split by a line break rather than missing.
    help_text = " ".join(vi_cli.build_parser().format_help().split())
    for surface in ("Web Analytics", "Speed Insights", "request logs"):
        assert surface in help_text, f"{surface} is queryable but unmentioned"
    assert "counts rows rather than groups, up to 200" in help_text


def test_dry_run_calls_helper_sees_one_entry_per_planned_request(cli: Cli) -> None:
    code, out, err = cli.run(["overview", "--dry-run"], env=dict(DRY_RUN_ENV))
    assert code == 0, err
    assert len(dry_run_calls(out)) == 3
