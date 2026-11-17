"""Tests for the request logs paths through cli.py.

Mirrors tests/test_speed_cli.py: one module per surface through the CLI, so a
change to one surface cannot quietly rewrite another's behaviour.
"""

from __future__ import annotations

import csv
import io
import json
import re
from datetime import datetime, timedelta
from typing import Any

import pytest
from conftest import Cli
from helpers import (
    BASE_ENV,
    DRY_RUN_ENV,
    LOGS_EMPTY_PAGE,
    LOGS_ERROR_PAGE,
    LOGS_PAGE,
    LOGS_URL,
    PROJECT,
    TOKEN,
    FakeResponse,
    FakeSession,
    dry_run_calls,
    dry_run_values,
    error_payload,
    logs_row,
)

from vercel_insights import logs as vi_logs
from vercel_insights.cli import OWNER_PLACEHOLDER, build_parser
from vercel_insights.presets import PRESETS

LOGS_ONLY_FLAGS: list[list[str]] = [
    ["--level", "error"],
    ["--status-code", "500"],
    ["--source", "serverless"],
    ["--method", "POST"],
    ["--search", "boom"],
    ["--request-id", "abc"],
    ["--branch", "main"],
    ["--deployment", "dpl_abc"],
    ["--expand"],
]


@pytest.mark.parametrize("flag", LOGS_ONLY_FLAGS, ids=lambda item: item[0])
def test_a_logs_flag_is_refused_on_a_traffic_preset(cli: Cli, flag: list[str]) -> None:
    code, _out, err = cli.run(
        ["top-pages", *flag], dict(DRY_RUN_ENV) | {"VERCEL_TOKEN": "t"}
    )
    assert code == 2
    assert flag[0] in err
    # The message has to name where the flag does work, or the reader is stuck.
    assert "errors" in err or "logs" in err


@pytest.mark.parametrize("flag", LOGS_ONLY_FLAGS, ids=lambda item: item[0])
def test_a_logs_flag_is_refused_on_a_speed_preset(cli: Cli, flag: list[str]) -> None:
    code, _out, err = cli.run(
        ["vitals", *flag], dict(DRY_RUN_ENV) | {"VERCEL_TOKEN": "t"}
    )
    assert code == 2
    assert flag[0] in err


WRONG_ON_LOGS: list[tuple[list[str], str]] = [
    (["--group-by", "route"], "--group-by"),
    (["--granularity", "day"], "--granularity"),
    (["--filter", "route eq '/x'"], "--filter"),
    (["--dataset", "events"], "--dataset"),
    (["--event-name", "signup"], "--event-name"),
    (["--event-property", "plan"], "--event-property"),
    (["--flag", "beta=true"], "--flag"),
    (["--country", "US"], "--country"),
    (["--device", "mobile"], "--device"),
    (["--browser", "Safari"], "--browser"),
    (["--os", "macOS"], "--os"),
    (["--referrer", "example.com"], "--referrer"),
    (["--utm-source", "news"], "--utm-source"),
    (["--metric", "lcp"], "--metric"),
    (["--percentile", "95"], "--percentile"),
    (["--all"], "--all"),
    (["--budget", "lcp=2500"], "--budget"),
]


@pytest.mark.parametrize(
    ("argv", "flag"), WRONG_ON_LOGS, ids=[flag for _argv, flag in WRONG_ON_LOGS]
)
def test_a_flag_from_another_surface_is_refused_on_errors(
    cli: Cli, argv: list[str], flag: str
) -> None:
    code, _out, err = cli.run(
        ["errors", *argv], dict(DRY_RUN_ENV) | {"VERCEL_TOKEN": "t"}
    )
    assert code == 2, err
    assert flag in err
    # Naming the surface the preset does query is what stops the reader trying
    # the same flag on the other two logs presets next.
    assert "request logs" in err


def test_the_odata_rejection_names_what_to_use_instead(cli: Cli) -> None:
    code, _out, err = cli.run(
        ["errors", "--filter", "route eq '/x'"],
        dict(DRY_RUN_ENV) | {"VERCEL_TOKEN": "t"},
    )
    assert code == 2
    assert "--search" in err and "--status-code" in err
    # Every filter this surface has, rather than a hand-copied subset of them:
    # these three were missing while the list was prose.
    assert "--environment" in err and "--deployment" in err and "--request-id" in err


def test_an_appending_flag_is_reported_as_the_user_typed_it(cli: Cli) -> None:
    # --flag appends, so its value is a list, and printing the list itself would
    # quote Python syntax at a user who typed none of it.
    code, _out, err = cli.run(
        ["errors", "--flag", "beta=true"], dict(DRY_RUN_ENV) | {"VERCEL_TOKEN": "t"}
    )
    assert code == 2
    assert "beta=true" in err
    assert "['beta=true']" not in err


def test_csv_is_refused_on_the_multi_table_summary(cli: Cli) -> None:
    code, _out, err = cli.run(
        ["error-summary", "--csv"], dict(DRY_RUN_ENV) | {"VERCEL_TOKEN": "t"}
    )
    assert code == 2
    assert "--csv" in err and "errors" in err


BAD_LOGS_VALUES: list[list[str]] = [
    ["errors", "--level", "erro"],
    ["errors", "--source", "lambda"],
    ["errors", "--status-code", ">=500"],
]


@pytest.mark.parametrize(
    "argv", BAD_LOGS_VALUES, ids=[argv[1] for argv in BAD_LOGS_VALUES]
)
def test_a_bad_logs_value_is_refused_before_any_request(
    cli: Cli, argv: list[str]
) -> None:
    # session=None makes the fixture fail the test if a request is attempted, so
    # this also proves the check happens before the network.
    code, _out, err = cli.run(argv, dict(BASE_ENV))
    assert code == 2 and err.startswith("error:")


def test_an_out_of_range_limit_is_refused_before_any_request(cli: Cli) -> None:
    # session=None again, so this also pins the refusal ahead of the network.
    code, _out, err = cli.run(["errors", "--limit", "500"], dict(BASE_ENV))
    assert code == 2
    assert "--limit 500" in err
    # The ceiling quoted is this surface's own: 200 rows, not the 100 groups the
    # two analytics APIs bound. A logs limit counts requests, not groups.
    assert "200" in err and "rows" in err


@pytest.mark.parametrize(
    ("flag", "parameter"),
    [
        (["--path", "/api/me"], "requestPath"),
        (["--route", "/api/[id]"], "route"),
        (["--environment", "production"], "environment"),
    ],
    ids=["--path", "--route", "--environment"],
)
def test_a_shorthand_this_surface_has_narrows_every_call(
    cli: Cli, flag: list[str], parameter: str
) -> None:
    # These three are the only Web Analytics shorthands the request logs API has
    # a parameter for. The errors preset queries twice, so a narrowing that
    # reached only the first call would quietly report the other kind of error
    # unfiltered.
    code, out, err = cli.run(["errors", *flag, "--dry-run"], dict(DRY_RUN_ENV))
    assert code == 0, err
    assert len(dry_run_calls(out)) == 2
    for call in (0, 1):
        assert dry_run_values(out, parameter, call=call) == [flag[1]]


# ---------------------------------------------------------------------------
# The window default belongs to the surface
# ---------------------------------------------------------------------------

HOUR_MS = 3_600_000

#: A dry run resolves its window from the clock, so the two timestamps are
#: only approximately the requested distance apart.
TOLERANCE_MS = 5_000


def _window_ms(out: str, call: int = 0) -> int:
    """How long a window one request-logs call asked for, in milliseconds."""
    start = int(dry_run_values(out, "startDate", call=call)[0])
    end = int(dry_run_values(out, "endDate", call=call)[0])
    return end - start


def test_a_logs_run_defaults_to_the_last_hour(cli: Cli) -> None:
    # Runtime logs are retained for an hour on Hobby, so the global 7 day
    # default would mostly return nothing and read as "nothing is broken".
    code, out, err = cli.run(["logs", "--dry-run"], dict(DRY_RUN_ENV))
    assert code == 0, err
    assert abs(_window_ms(out) - HOUR_MS) <= TOLERANCE_MS


def test_the_error_summary_preset_defaults_to_six_hours(cli: Cli) -> None:
    # It tallies rather than lists, so it is worth a wider window than errors.
    code, out, err = cli.run(["error-summary", "--dry-run"], dict(DRY_RUN_ENV))
    assert code == 0, err
    assert abs(_window_ms(out) - 6 * HOUR_MS) <= TOLERANCE_MS


def test_an_explicit_since_beats_the_preset_default(cli: Cli) -> None:
    code, out, err = cli.run(["logs", "--since", "30m", "--dry-run"], dict(DRY_RUN_ENV))
    assert code == 0, err
    assert abs(_window_ms(out) - HOUR_MS // 2) <= TOLERANCE_MS


def test_an_empty_since_is_refused_rather_than_read_as_the_preset_default(
    cli: Cli,
) -> None:
    # A preset default answers "nobody asked for a window". An empty --since is
    # somebody asking for nothing, and substituting the default there would
    # report an hour of logs as though it had been chosen.
    code, _out, err = cli.run(["logs", "--since", ""], dict(BASE_ENV))
    assert code == 2
    assert "empty time value" in err


def test_a_traffic_preset_still_defaults_to_seven_days(cli: Cli) -> None:
    # Only a logs preset owns a window default. Moving the default off the
    # parser must leave every other preset asking for exactly what it did.
    code, out, err = cli.run(["top-pages", "--dry-run"], dict(DRY_RUN_ENV))
    assert code == 0, err
    # This surface sends ISO-8601 rather than Unix milliseconds.
    since = datetime.strptime(dry_run_values(out, "since")[0], "%Y-%m-%dT%H:%M:%SZ")
    until = datetime.strptime(dry_run_values(out, "until")[0], "%Y-%m-%dT%H:%M:%SZ")
    assert until - since == timedelta(days=7)


# ---------------------------------------------------------------------------
# Flags become query parameters, and an errors run queries twice
# ---------------------------------------------------------------------------


def test_the_errors_preset_dry_runs_both_calls(cli: Cli) -> None:
    code, out, err = cli.run(["errors", "--dry-run"], dict(DRY_RUN_ENV))
    assert code == 0, err
    calls = dry_run_calls(out)
    assert [endpoint for endpoint, _params in calls] == ["request-logs", "request-logs"]
    sent = [dict(params) for _endpoint, params in calls]
    # statusCode matches responses and level matches application log lines, so
    # neither call alone answers "what broke": a 5xx that printed nothing is
    # invisible to the second, and a 200 that logged a stack trace to the first.
    assert sent[0]["statusCode"] == "5xx"
    assert "level" not in sent[0]
    assert sent[1]["level"] == "error,fatal"
    assert "statusCode" not in sent[1]


def test_an_explicit_status_code_makes_errors_one_call(cli: Cli) -> None:
    code, out, err = cli.run(
        ["errors", "--status-code", "500", "--dry-run"], dict(DRY_RUN_ENV)
    )
    assert code == 0, err
    assert len(dry_run_calls(out)) == 1
    assert dry_run_values(out, "statusCode") == ["500"]


def test_an_explicit_level_makes_errors_one_call_in_the_api_spelling(cli: Cli) -> None:
    code, out, err = cli.run(
        ["errors", "--level", "ERROR,Warning", "--dry-run"], dict(DRY_RUN_ENV)
    )
    assert code == 0, err
    assert len(dry_run_calls(out)) == 1
    # Lower cased on the way out, because the API matches the spelling it
    # publishes and answers anything else with 200 and zero rows.
    assert dry_run_values(out, "level") == ["error,warning"]


def test_the_shorthand_filters_compile_to_query_parameters(cli: Cli) -> None:
    code, out, err = cli.run(
        [
            "logs",
            "--path",
            "/api/me",
            "--route",
            "/api/[id]",
            "--environment",
            "preview",
            "--method",
            "post",
            "--dry-run",
        ],
        dict(DRY_RUN_ENV),
    )
    assert code == 0, err
    sent = dict(dry_run_calls(out)[0][1])
    assert sent["requestPath"] == "/api/me"
    assert sent["route"] == "/api/[id]"
    assert sent["environment"] == "preview"
    # The API matches the method it logs, which is upper case.
    assert sent["requestMethod"] == "POST"
    # This surface takes no OData, so nothing compiles to a filter expression.
    assert "filter" not in sent


#: The filters this surface has and the two analytics surfaces do not, with the
#: parameter each one has to arrive as. Spelled out by hand rather than read from
#: the package, so a rename on either side of the mapping fails a test instead of
#: being mirrored by it.
LOGS_ONLY_MAPPINGS: list[tuple[list[str], str]] = [
    (["--branch", "release/2026-08"], "branch"),
    (["--deployment", "dpl_ExampleDeploymentId000000000"], "deploymentId"),
    (["--request-id", "abcde-1786964768933-0123456789ab"], "requestId"),
    (["--search", "Cannot read properties"], "search"),
]


@pytest.mark.parametrize(
    ("flag", "parameter"),
    LOGS_ONLY_MAPPINGS,
    ids=[flag[0] for flag, _parameter in LOGS_ONLY_MAPPINGS],
)
def test_a_logs_only_filter_arrives_under_its_own_wire_name(
    cli: Cli, flag: list[str], parameter: str
) -> None:
    # Four of the eleven filters this surface takes are spelled differently on
    # the wire than on the command line, and a filter that never arrives narrows
    # nothing while still looking like it did.
    code, out, err = cli.run(["logs", *flag, "--dry-run"], dict(DRY_RUN_ENV))
    assert code == 0, err
    assert dry_run_values(out, parameter) == [flag[1]]


def test_preview_environment_is_accepted_on_a_logs_preset(cli: Cli) -> None:
    # A Web Analytics count query refuses --environment preview and tells the
    # reader to add --group-by day instead. A logs preset has no grouping either,
    # but it refuses --group-by outright, so that advice cannot be followed and
    # the rule belongs to the surface that can offer it.
    code, out, err = cli.run(
        ["logs", "--environment", "preview", "--dry-run"], dict(DRY_RUN_ENV)
    )
    assert code == 0, err
    assert dry_run_values(out, "environment") == ["preview"]


def test_an_unknown_method_warns_on_stderr_and_is_still_sent(cli: Cli) -> None:
    # --method was the one logs vocabulary with no check at all, so --method POTS
    # went out and came back 200 with zero rows: the same trap --level and
    # --source are validated against. A custom method is legal HTTP, though, so
    # this warns rather than refusing, and the request is still made.
    code, out, err = cli.run(["logs", "--method", "POTS", "--dry-run"], dict(DRY_RUN_ENV))
    assert code == 0, err
    assert dry_run_values(out, "requestMethod") == ["POTS"]
    assert "warning: --method POTS" in err
    # The warning has to name the standard set and the zero-rows outcome, or the
    # reader cannot tell a typo from a deliberate custom verb.
    for method in ("GET", "POST", "DELETE"):
        assert method in err
    assert "zero rows" in err


@pytest.mark.parametrize("method", ["get", "POST", " delete "])
def test_a_standard_method_is_upper_cased_without_a_warning(cli: Cli, method: str) -> None:
    code, out, err = cli.run(["logs", "--method", method, "--dry-run"], dict(DRY_RUN_ENV))
    assert code == 0, err
    assert dry_run_values(out, "requestMethod") == [method.strip().upper()]
    assert "warning:" not in err


def test_the_since_help_names_each_logs_preset_window_from_the_preset_table() -> None:
    # The phrase used to be written out beside a preset table free to move under
    # it. Composed from PRESETS, it cannot say 6h while error-summary asks for
    # something else.
    help_text = " ".join(build_parser().format_help().split())
    for name, preset in PRESETS.items():
        if preset.default_since:
            assert f"{preset.default_since} on " in help_text
            assert name in help_text


def test_the_source_help_quotes_the_one_alias_note_rather_than_its_own_copy() -> None:
    # Two hand-written copies of a probed API fact can drift apart, and this one
    # had them: the help text and the refusal message. Both now read the sentence
    # logs.py composes from SOURCE_ALIASES.
    help_text = " ".join(build_parser().format_help().split())
    assert " ".join(vi_logs.SOURCE_ALIAS_NOTE.split()) in help_text


def test_the_search_help_does_not_claim_a_matching_rule_nobody_established(
    cli: Cli,
) -> None:
    # The probes showed that a field:value string does not filter, not how the
    # server treats it: search=path:/api/me came back unfiltered, which literal
    # matching cannot produce. So the help says what to expect, not why.
    help_text = " ".join(build_parser().format_help().split())
    assert "matched literally" not in help_text
    assert "do not expect 'status:500' to filter by status" in help_text


def test_a_logs_run_needs_an_account_id_and_says_so(cli: Cli) -> None:
    # A team slug names a team but is not an account id, and ownerId wants an id.
    # Falling through to the personal account would answer for the wrong account
    # rather than failing, which is the worst outcome available.
    code, _out, err = cli.run(
        ["errors", "--team-slug", "acme"],
        {"VERCEL_TOKEN": "t", "VERCEL_PROJECT_ID": "p"},
    )
    assert code == 2
    assert "--team-slug" in err and "--owner-id" in err
    # Naming the surface that needs the id is what stops the reader concluding
    # a slug never works.
    assert "request logs" in err


# ---------------------------------------------------------------------------
# A real run: every filter set pages, then the sets are merged and printed
# ---------------------------------------------------------------------------

#: A refusal, as this endpoint words one.
FORBIDDEN = error_payload("forbidden", "You don't have permission")


def test_errors_reports_both_kinds_of_failure(cli: Cli) -> None:
    # The statusCode call finds both failures here and the level call finds
    # nothing, so an errors run has to report the union of its two calls: taking
    # only what both returned would report a healthy site.
    session = FakeSession(
        FakeResponse(200, LOGS_ERROR_PAGE),
        FakeResponse(200, LOGS_EMPTY_PAGE),
    )
    code, out, err = cli.run(["errors", "--since", "30m"], BASE_ENV, session)
    assert code == 0, err
    assert "/api/checkout" in out
    assert "TypeError" in out
    assert [call["url"] for call in session.calls] == [LOGS_URL, LOGS_URL]


def test_a_request_that_matched_both_filters_is_reported_once(cli: Cli) -> None:
    # The same 500 comes back from both calls, and only one copy carries the log
    # line, because level matches the request and statusCode matches the
    # response. Reporting it twice would double every count in the summary, and
    # keeping the silent copy would print a blank message for a request that
    # logged a stack trace.
    silent = logs_row(requestId="both", statusCode=500, logs=[])
    logged = logs_row(
        requestId="both",
        statusCode=500,
        logs=[{"level": "error", "message": "TypeError: boom", "messageTruncated": False}],
    )
    session = FakeSession(
        FakeResponse(200, {"rows": [silent], "hasMoreRows": False}),
        FakeResponse(200, {"rows": [logged], "hasMoreRows": False}),
    )
    code, out, err = cli.run(["errors", "--json"], BASE_ENV, session)
    assert code == 0, err
    entries = json.loads(out)["entries"]
    assert len(entries) == 1
    assert entries[0]["message"] == "TypeError: boom"


def test_an_empty_window_is_a_success_not_a_failure(cli: Cli) -> None:
    session = FakeSession(
        FakeResponse(200, LOGS_EMPTY_PAGE), FakeResponse(200, LOGS_EMPTY_PAGE)
    )
    code, out, _err = cli.run(["errors"], BASE_ENV, session)
    assert code == 0
    assert "No request logs" in out


def test_an_empty_answer_over_a_wide_window_says_the_logs_may_have_aged_out(
    cli: Cli,
) -> None:
    # error-summary looks back six hours by default, which is longer than the
    # shortest retention any plan has, so "nothing failed" and "the logs are
    # gone" are both live readings of an empty answer and the output says so.
    session = FakeSession(
        FakeResponse(200, LOGS_EMPTY_PAGE), FakeResponse(200, LOGS_EMPTY_PAGE)
    )
    code, out, err = cli.run(["error-summary"], BASE_ENV, session)
    assert code == 0, err
    assert "retention" in out and "aged out" in out


def test_the_logs_preset_makes_one_call(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, LOGS_ERROR_PAGE))
    code, _out, _err = cli.run(["logs"], BASE_ENV, session)
    assert code == 0
    assert len(session.calls) == 1


def test_paging_stops_at_the_limit(cli: Cli) -> None:
    full = {
        "rows": [logs_row(requestId=f"r{index}") for index in range(50)],
        "hasMoreRows": True,
    }
    session = FakeSession(*[FakeResponse(200, full) for _ in range(4)])
    code, out, _err = cli.run(["logs", "--limit", "120"], BASE_ENV, session)
    assert code == 0
    assert len(session.calls) == 3
    # Each call asks for the next page. Re-requesting page 0 would fill the
    # budget just as fast and report the same 50 requests three times over.
    assert [dict(call["params"])["page"] for call in session.calls] == ["0", "1", "2"]
    assert "more" in out.lower()


def test_error_summary_prints_the_grouped_tables(cli: Cli) -> None:
    session = FakeSession(
        FakeResponse(200, LOGS_ERROR_PAGE), FakeResponse(200, LOGS_EMPTY_PAGE)
    )
    code, out, _err = cli.run(["error-summary"], BASE_ENV, session)
    assert code == 0
    assert "worst status" in out


def test_expand_prints_the_whole_message_under_its_row(cli: Cli) -> None:
    session = FakeSession(
        FakeResponse(200, LOGS_ERROR_PAGE), FakeResponse(200, LOGS_EMPTY_PAGE)
    )
    code, out, err = cli.run(["errors", "--expand"], BASE_ENV, session)
    assert code == 0, err
    # The row itself only has room for 34 characters of message.
    assert "TypeError: Cannot read properties of undefined" in out
    assert "request err-1" in out


def test_json_output_goes_through_the_logs_formatter(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, LOGS_ERROR_PAGE))
    code, out, _err = cli.run(["logs", "--json"], BASE_ENV, session)
    assert code == 0
    assert json.loads(out)["entries"][0]["requestId"] == "err-1"


def test_csv_output_is_one_row_per_request(cli: Cli) -> None:
    session = FakeSession(
        FakeResponse(200, LOGS_ERROR_PAGE), FakeResponse(200, LOGS_EMPTY_PAGE)
    )
    code, out, err = cli.run(["errors", "--csv"], BASE_ENV, session)
    assert code == 0, err
    rows = list(csv.reader(io.StringIO(out)))
    assert rows[0][0] == "time"
    assert [row[7] for row in rows[1:]] == ["err-1", "err-2"]


def test_csv_reports_truncation_on_the_error_stream(cli: Cli) -> None:
    # CSV has no room for a caveat, and dropping it would leave the one consumer
    # who cannot tell a cut table from a complete one with two rows and no
    # signal. The data stream stays machine readable; the caveat goes beside it.
    full = {
        "rows": [logs_row(requestId=f"r{index}") for index in range(50)],
        "hasMoreRows": True,
    }
    session = FakeSession(FakeResponse(200, full))
    code, out, err = cli.run(["logs", "--limit", "2", "--csv"], BASE_ENV, session)
    assert code == 0, err
    rows = list(csv.reader(io.StringIO(out)))
    # Header plus the two rows asked for, and nothing else on the data stream.
    assert len(rows) == 3
    assert all(not line.startswith("note:") for line in out.splitlines())
    assert "note: " in err
    assert "Showing the most recent 2 of more requests that matched" in err
    assert "More rows matched than were shown" in err


def test_csv_over_an_empty_wide_window_still_warns_about_retention(cli: Cli) -> None:
    # A lone header row reads as "nothing failed" unless something says the logs
    # may simply have aged out, and that is the whole reason the note exists.
    session = FakeSession(
        FakeResponse(200, LOGS_EMPTY_PAGE), FakeResponse(200, LOGS_EMPTY_PAGE)
    )
    code, out, err = cli.run(["errors", "--csv", "--since", "24h"], BASE_ENV, session)
    assert code == 0, err
    assert out.splitlines() == ["time,level,status,method,route,path,source,requestId,message"]
    assert "retention" in err and "aged out" in err


def test_json_does_not_repeat_its_notes_on_the_error_stream(cli: Cli) -> None:
    # They are a field of the document there, so a second copy would be noise a
    # caller has to filter rather than a caveat it cannot otherwise see.
    session = FakeSession(FakeResponse(200, LOGS_ERROR_PAGE))
    code, out, err = cli.run(["logs", "--json"], BASE_ENV, session)
    assert code == 0, err
    assert json.loads(out)["notes"]
    assert "note: " not in err


def test_a_403_explains_token_scope(cli: Cli) -> None:
    session = FakeSession(FakeResponse(403, FORBIDDEN))
    code, _out, err = cli.run(["logs"], BASE_ENV, session)
    assert code == 1
    # Vercel's own wording is kept, then explained rather than replaced.
    assert "You don't have permission" in err
    assert "account" in err and "team" in err
    assert "vercel.com/account/tokens" in err
    # The collector raised through the session's try/finally, so the connection
    # is still closed: a failure must not leak one.
    assert session.closed


def test_a_failure_on_the_second_filter_set_reports_nothing_and_fails(cli: Cli) -> None:
    # The first filter set came back with two real errors and the second was
    # refused. A partial answer is not offered: it would read as "these are the
    # errors" while half the question went unanswered, and this surface's whole
    # point is that neither filter alone answers it.
    session = FakeSession(
        FakeResponse(200, LOGS_ERROR_PAGE), FakeResponse(403, FORBIDDEN)
    )
    code, out, err = cli.run(["errors"], BASE_ENV, session)
    assert code == 1
    assert out == ""
    assert "/api/checkout" not in out
    assert "vercel.com/account/tokens" in err
    assert session.closed


def test_a_403_here_does_not_get_the_web_analytics_team_advice(cli: Cli) -> None:
    # Nothing configured a team, which is the condition the Web Analytics hint
    # fires on. That advice is wrong here twice over: this endpoint takes no
    # teamId at all, and a team id only helps here by being the ownerId.
    session = FakeSession(FakeResponse(403, FORBIDDEN))
    code, _out, err = cli.run(["logs"], BASE_ENV, session)
    assert code == 1
    assert "--team with the team id" not in err
    assert "--list-projects" not in err


def test_a_top_level_array_is_refused_rather_than_read_as_no_rows(cli: Cli) -> None:
    # This endpoint answers with an object carrying "rows". A JSON array is a
    # shape this client cannot read, and reporting it as zero requests would
    # read as a quiet hour on the site.
    session = FakeSession(FakeResponse(200, [1, 2]))
    code, _out, err = cli.run(["logs"], BASE_ENV, session)
    assert code == 1
    assert "rows" in err


def test_an_unreadable_second_page_fails_rather_than_stopping_early(cli: Cli) -> None:
    # Page 0 was fine and page 1 is a shape this client cannot read. Treating
    # that as the end of the data would report the first 50 requests as the whole
    # answer, which is the same silence a truncation note exists to prevent.
    full = {
        "rows": [logs_row(requestId=f"r{index}") for index in range(50)],
        "hasMoreRows": True,
    }
    session = FakeSession(
        FakeResponse(200, full), FakeResponse(200, {"rows": "not a list"})
    )
    code, out, err = cli.run(["logs", "--limit", "100"], BASE_ENV, session)
    assert code == 1
    assert out == ""
    assert "not a list" in err or "was not a list" in err
    assert len(session.calls) == 2


def test_the_token_never_reaches_the_output(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, LOGS_ERROR_PAGE))
    code, out, err = cli.run(["logs", "--verbose"], BASE_ENV, session)
    assert code == 0
    # The verbose line is in the captured stream, so this really is the run's
    # own diagnostics being checked rather than a run that printed none: a line
    # sent to the process stderr instead would escape both of these.
    assert "verbose: GET" in err
    assert "Bearer <redacted>" in err
    assert TOKEN not in out and TOKEN not in err


def test_verbose_says_which_filter_set_each_page_belonged_to(cli: Cli) -> None:
    # An errors run interleaves two filter sets, and page numbers restart with
    # each one, so "page 0, page 1, page 0" cannot be read on its own. The params
    # carry the page and the filter that set was querying with, which is what
    # tells the two apart.
    session = FakeSession(
        FakeResponse(200, LOGS_ERROR_PAGE), FakeResponse(200, LOGS_EMPTY_PAGE)
    )
    code, _out, err = cli.run(["errors", "--verbose"], BASE_ENV, session)
    assert code == 0, err
    params = [line for line in err.splitlines() if line.startswith("verbose: params")]
    assert len(params) == 2
    assert "('statusCode', '5xx')" in params[0]
    assert "('level', 'error,fatal')" in params[1]
    # Headers once per filter set rather than once per page, so a run that pages
    # four times deep does not print the same three headers four times over.
    assert err.count("Bearer <redacted>") == 2


# ---------------------------------------------------------------------------
# Every printed sentence has to survive being read next to its own table
# ---------------------------------------------------------------------------

#: The ordinary 4xx: a 401 that printed nothing, which is the application
#: turning an unauthenticated request away.
FOURXX_PAGE = {
    "rows": [logs_row(requestId="unauth", statusCode=401, logs=[])],
    "hasMoreRows": False,
}

#: Two of them, for the summary preset: a 401 and a 404, neither logging.
FOURXX_PAIR_PAGE = {
    "rows": [
        logs_row(requestId="unauth", statusCode=401, logs=[]),
        logs_row(requestId="gone", statusCode=404, requestPath="/missing", route="", logs=[]),
    ],
    "hasMoreRows": False,
}

#: A 200 whose handler logged a warning and nothing worse.
WARNING_PAGE = {
    "rows": [
        logs_row(
            requestId="slow",
            statusCode=200,
            logs=[{"level": "warning", "message": "slow query", "messageTruncated": False}],
        )
    ],
    "hasMoreRows": False,
}

#: A request the API recorded no status for, which --status-code None selects.
NO_STATUS_PAGE = {
    "rows": [logs_row(requestId="nostatus", statusCode=None, logs=[])],
    "hasMoreRows": False,
}

#: The three documented ways to collapse an errors run to a single call, each
#: with a page whose rows this tool would not itself call errors. Every one of
#: them printed the error definition and counted its rows as errors that had
#: "logged an error or fatal line", four lines above a table showing otherwise.
COLLAPSED_RUNS: list[tuple[list[str], dict[str, Any], str]] = [
    (["errors", "--status-code", "4xx"], FOURXX_PAGE, "statusCode 4xx"),
    (["errors", "--level", "warning"], WARNING_PAGE, "level warning"),
    (["errors", "--status-code", "None"], NO_STATUS_PAGE, "statusCode None"),
]

#: The sentence that claims a row was an error only because of what it printed.
LOGGED_CLAIM = "count as errors only because they logged an error or fatal line"

#: Words no sentence may use about a row this tool would not call an error.
ERROR_NOUN = re.compile(r"\berrors?\b")


def _table_rows(out: str) -> list[list[str]]:
    """The row table's body cells, split on whitespace, as printed.

    Parsed out of the rendered output rather than read off the report, because
    what the reader compares a sentence against is the table on screen.
    """
    lines = out.splitlines()
    head = next(
        index for index, line in enumerate(lines) if line.split()[:2] == ["time", "level"]
    )
    rows: list[list[str]] = []
    for line in lines[head + 2 :]:
        if not line.strip():
            break
        rows.append(line.split())
    return rows


def _footer(out: str) -> list[str]:
    """Every line printed after the table, which is where the sentences are."""
    lines = out.splitlines()
    head = next(
        index for index, line in enumerate(lines) if line.split()[:2] == ["time", "level"]
    )
    blank = lines.index("", head)
    return [line for line in lines[blank + 1 :] if line.strip()]


def _row_is_an_error(cells: list[str]) -> bool:
    """Whether the printed row is an error by the definition the tool states."""
    level, status = cells[1], cells[2]
    if status.isdigit() and int(status) >= 500:
        return True
    return level in ("error", "fatal")


@pytest.mark.parametrize(
    ("argv", "page", "filter_shown"),
    COLLAPSED_RUNS,
    ids=[" ".join(argv[1:]) for argv, _page, _shown in COLLAPSED_RUNS],
)
def test_a_collapsed_errors_run_prints_no_sentence_its_table_contradicts(
    cli: Cli, argv: list[str], page: dict[str, Any], filter_shown: str
) -> None:
    session = FakeSession(FakeResponse(200, page))
    code, out, err = cli.run(argv, BASE_ENV, session)
    assert code == 0, err
    # One call, because the explicit filter replaced the preset's own query.
    assert len(session.calls) == 1
    rows = _table_rows(out)
    footer = _footer(out)
    assert rows and footer

    # 1. The header must not state a definition the query did not apply.
    assert vi_logs.ERROR_DEFINITION not in out
    assert f"These rows are what {filter_shown} matched" in out

    # 2. No sentence may call these rows errors while the table shows a row that
    #    is not one by the tool's own definition.
    if any(not _row_is_an_error(cells) for cells in rows):
        offenders = [line for line in footer if ERROR_NOUN.search(line)]
        assert not offenders, offenders

    # 3. The "logged an error or fatal line" claim needs a row that logged one.
    if LOGGED_CLAIM in out:
        assert any(cells[1] in ("error", "fatal") for cells in rows)

    # 4. The count has to be the number of rows on screen.
    assert f"{len(rows)} request" in out


def test_the_summary_footer_does_not_claim_a_log_line_its_table_denies(cli: Cli) -> None:
    # The same defect on the multi-table preset, where the message table is what
    # contradicted it: every group read "(no log line)" while the footer said
    # both rows had logged an error or fatal line.
    session = FakeSession(FakeResponse(200, FOURXX_PAIR_PAGE))
    code, out, err = cli.run(["error-summary", "--status-code", "4xx"], BASE_ENV, session)
    assert code == 0, err
    assert "(no log line)" in out
    assert LOGGED_CLAIM not in out
    assert "Filter: statusCode 4xx" in out
    assert "2 requests in 6 hours" in out
    assert not ERROR_NOUN.search(out.splitlines()[-1])


def test_an_unnarrowed_errors_run_still_states_the_definition_and_counts_errors(
    cli: Cli,
) -> None:
    # The control for the three cases above: with no explicit level or status the
    # preset does apply its own definition, both rows are 5xx, and calling them
    # errors is exactly right. A fix that simply stopped saying "errors" would
    # pass those three and fail this one.
    session = FakeSession(
        FakeResponse(200, LOGS_ERROR_PAGE), FakeResponse(200, LOGS_EMPTY_PAGE)
    )
    code, out, err = cli.run(["errors", "--since", "30m"], BASE_ENV, session)
    assert code == 0, err
    assert vi_logs.ERROR_DEFINITION in out
    assert "2 errors in 30 minutes" in out
    assert LOGGED_CLAIM not in out


def test_a_logged_error_on_a_non_5xx_is_still_reported_as_one(cli: Cli) -> None:
    # The other direction: a 200 that logged a fatal line is an error only
    # because it logged one, and that sentence has to survive the fix, with the
    # row it describes visible in the table.
    page = {
        "rows": [
            logs_row(
                requestId="cron",
                statusCode=200,
                route="/api/cron/sync",
                logs=[
                    {
                        "level": "fatal",
                        "message": "FATAL: connection pool exhausted",
                        "messageTruncated": False,
                    }
                ],
            )
        ],
        "hasMoreRows": False,
    }
    session = FakeSession(FakeResponse(200, LOGS_EMPTY_PAGE), FakeResponse(200, page))
    code, out, err = cli.run(["errors"], BASE_ENV, session)
    assert code == 0, err
    assert f"1 of them returned a non-5xx status and {LOGGED_CLAIM}" in out
    assert [cells[1] for cells in _table_rows(out)] == ["fatal"]


# ---------------------------------------------------------------------------
# ownerId is required, so an unresolved owner is resolved before the query
# ---------------------------------------------------------------------------

#: A project record, as /v9/projects answers it. ``accountId`` is the owning
#: account, and is the only place a personal account's ownerId can be read.
PROJECT_RECORD = {"id": PROJECT, "name": "demo", "accountId": "own_from_api"}


def test_an_unconfigured_owner_is_read_off_the_project_record(cli: Cli) -> None:
    # This endpoint requires ownerId: omitting it is a 400 and a wrong value a
    # 403, so a run with no owner configured has to resolve one first, the same
    # way a Speed Insights run does.
    session = FakeSession(
        FakeResponse(200, PROJECT_RECORD), FakeResponse(200, LOGS_PAGE)
    )
    code, _out, err = cli.run(
        ["logs"], {"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": PROJECT}, session
    )
    assert code == 0, err
    assert session.calls[0]["url"].endswith(f"/v9/projects/{PROJECT}")
    assert ("ownerId", "own_from_api") in session.calls[1]["params"]


def test_a_project_record_with_no_account_id_names_the_flag_to_set(cli: Cli) -> None:
    # Nothing else knows the account, so this is where the run stops. The
    # refusal names the surface that could not be scoped, and this one is not
    # Speed Insights.
    session = FakeSession(FakeResponse(200, {"id": PROJECT, "name": "demo"}))
    code, _out, err = cli.run(
        ["errors"], {"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": PROJECT}, session
    )
    assert code == 2
    assert "--owner-id" in err and "VERCEL_OWNER_ID" in err
    assert "request logs" in err
    assert "Speed Insights" not in err


def test_a_project_name_does_not_force_a_lookup_on_this_surface(cli: Cli) -> None:
    # Unlike Speed Insights, which scopes by projectIds and needs identifiers,
    # this endpoint takes a project name as happily as an id. Only a missing
    # owner is worth an extra request here.
    session = FakeSession(FakeResponse(200, LOGS_PAGE))
    code, _out, err = cli.run(
        ["logs"],
        {"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": "my-site", "VERCEL_OWNER_ID": "own_x"},
        session,
    )
    assert code == 0, err
    assert len(session.calls) == 1
    assert ("projectId", "my-site") in session.calls[0]["params"]


def test_a_dry_run_without_an_owner_names_the_parameter_this_surface_sends(
    cli: Cli,
) -> None:
    # A dry run sends nothing, including the one GET that would resolve the
    # owner, so the placeholder needs explaining. The explanation has to name
    # the plain ownerId parameter: this API has no scope object to look for, and
    # pointing at Speed Insights' one would send the reader hunting for a field
    # that does not exist here.
    code, out, err = cli.run(["logs", "--dry-run"], {"VERCEL_PROJECT_ID": PROJECT})
    assert code == 0, err
    assert dry_run_values(out, "ownerId") == [OWNER_PLACEHOLDER]
    assert "ownerId parameter" in out
    assert "scope.ownerId" not in out
    assert "Speed Insights" not in out
    assert "--owner-id" in out
