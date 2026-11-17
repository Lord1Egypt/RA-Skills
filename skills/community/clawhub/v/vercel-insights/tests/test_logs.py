"""Tests for vercel_insights/logs.py: the request logs surface.

The API validates almost nothing: an unknown level or source comes back as 200
with zero rows, which would read as "your site is fine". So the vocabularies are
checked here, before a request exists, and these tests are what hold that line.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest
from helpers import (
    LOGS_EMPTY_PAGE,
    LOGS_ERROR_PAGE,
    LOGS_PAGE,
    LOGS_URL,
    OWNER,
    PROJECT,
    TOKEN,
    logs_request,
    logs_row,
)

from vercel_insights import ApiError, ConfigError
from vercel_insights import logs as vi_logs


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("error", "error"),
        ("ERROR", "error"),
        (" error , fatal ", "error,fatal"),
        ("error,fatal,warning,info", "error,fatal,warning,info"),
    ],
)
def test_validate_levels_normalizes_a_valid_list(value: str, expected: str) -> None:
    assert vi_logs.validate_levels(value) == expected


@pytest.mark.parametrize("value", ["erro", "errors", "critical", "", ","])
def test_validate_levels_refuses_anything_the_api_would_silently_ignore(
    value: str,
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        vi_logs.validate_levels(value)
    message = str(excinfo.value)
    # The message has to name the four accepted values and say why a typo is
    # dangerous here rather than merely wrong.
    for level in vi_logs.LEVELS:
        assert level in message
    assert "zero rows" in message


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("serverless", "serverless"),
        ("edge-function,static", "edge-function,static"),
        (" EDGE-MIDDLEWARE ", "edge-middleware"),
    ],
)
def test_validate_sources_normalizes_a_valid_list(value: str, expected: str) -> None:
    assert vi_logs.validate_sources(value) == expected


@pytest.mark.parametrize("value", ["lambda", "edge", "function", ""])
def test_validate_sources_refuses_an_unknown_source(value: str) -> None:
    with pytest.raises(ConfigError) as excinfo:
        vi_logs.validate_sources(value)
    message = str(excinfo.value)
    # Same message builder as validate_levels, so it owes the same two checks:
    # every accepted value named, and the zero-rows danger explained.
    for source in vi_logs.SOURCES:
        assert source in message
    assert "zero rows" in message
    # The row table can print a value that is not itself a filter spelling, so
    # the refusal message has to point at the mapping, not just the raw list.
    assert "serverless-middleware" in message
    assert "edge-middleware" in message


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("serverless-middleware", "edge-middleware"),
        ("SERVERLESS-MIDDLEWARE", "edge-middleware"),
        ("serverless,serverless-middleware", "serverless,edge-middleware"),
        (" Serverless-Middleware , static ", "edge-middleware,static"),
    ],
)
def test_validate_sources_resolves_the_display_alias_to_its_filter_spelling(
    value: str, expected: str
) -> None:
    # The row table's source column can print serverless-middleware, which is
    # not itself an accepted filter value; edge-middleware is what matches
    # those rows on the live API (verified 2026-08-17), so the displayed
    # spelling has to resolve to it rather than being refused.
    assert vi_logs.validate_sources(value) == expected


def test_validate_sources_still_refuses_an_unrelated_unknown_value_beside_the_alias() -> (
    None
):
    with pytest.raises(ConfigError) as excinfo:
        vi_logs.validate_sources("serverless-middleware,lambda")
    message = str(excinfo.value)
    assert "'lambda'" in message
    for source in vi_logs.SOURCES:
        assert source in message


def test_the_alias_note_is_composed_from_the_alias_table() -> None:
    # The sentence is a probed API fact, and it used to be hand-written in two
    # places: this refusal and --source's help text. Composing it from the table
    # means a new alias reaches both, and neither can drift from the mapping the
    # code actually applies.
    for display, resolved in vi_logs.SOURCE_ALIASES.items():
        assert display in vi_logs.SOURCE_ALIAS_NOTE
        assert resolved in vi_logs.SOURCE_ALIAS_NOTE
    with pytest.raises(ConfigError) as excinfo:
        vi_logs.validate_sources("lambda")
    assert vi_logs.SOURCE_ALIAS_NOTE in str(excinfo.value)


def test_source_aliases_only_resolve_to_values_the_api_accepts() -> None:
    # An alias that pointed outside SOURCES would mean this client refuses,
    # or worse silently mis-filters, on its own alias table rather than on
    # anything the API actually rejected.
    for resolved in vi_logs.SOURCE_ALIASES.values():
        assert resolved in vi_logs.SOURCES


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("500", "500"),
        ("5xx", "5xx"),
        ("4xx,5xx", "4xx,5xx"),
        ("401,4xx", "401,4xx"),
        ("40x", "40x"),
        ("5XX", "5xx"),
        ("none", "None"),
        (" 500 , 502 ", "500,502"),
    ],
)
def test_validate_status_code_accepts_what_the_api_accepts(
    value: str, expected: str
) -> None:
    # Verified live: comma separated integers, classes like 4xx or 5xx, or the
    # literal None. See docs/api-notes.md.
    assert vi_logs.validate_status_code(value) == expected


@pytest.mark.parametrize("value", [">=500", "xxx", "5**", "", "1234", "-1"])
def test_validate_status_code_refuses_what_the_api_rejects(value: str) -> None:
    with pytest.raises(ConfigError) as excinfo:
        vi_logs.validate_status_code(value)
    assert "4xx" in str(excinfo.value)


@pytest.mark.parametrize("limit", [1, 50, 200])
def test_validate_limit_accepts_the_documented_range(limit: int) -> None:
    assert vi_logs.validate_limit(limit) == limit


@pytest.mark.parametrize("limit", [0, -1, 201, 1000])
def test_validate_limit_refuses_a_limit_outside_the_range(limit: int) -> None:
    with pytest.raises(ConfigError) as excinfo:
        vi_logs.validate_limit(limit)
    assert "200" in str(excinfo.value)


def test_the_level_vocabulary_matches_the_severity_table() -> None:
    # The names are validated here and ranked in render.py, where LogEntry needs
    # them. Two spellings of the same vocabulary would drift, so the invariant is
    # asserted instead.
    from vercel_insights.render import ERROR_LEVELS, LOG_LEVEL_SEVERITY

    assert set(vi_logs.LEVELS) == set(LOG_LEVEL_SEVERITY)
    assert set(ERROR_LEVELS) <= set(vi_logs.LEVELS)
    assert ERROR_LEVELS == ("error", "fatal")


def test_build_request_targets_the_allowlisted_operation() -> None:
    request = logs_request()
    assert request.operation == "request_logs"
    assert request.url == LOGS_URL
    assert request.method == "GET"


def test_build_request_sends_the_five_required_parameters_first() -> None:
    request = logs_request()
    assert request.params[:5] == [
        ("projectId", PROJECT),
        ("ownerId", OWNER),
        ("page", "0"),
        ("startDate", "1786961168000"),
        ("endDate", "1786964768000"),
    ]


def test_build_request_puts_the_token_only_in_the_header() -> None:
    request = logs_request()
    assert request.headers["Authorization"] == f"Bearer {TOKEN}"
    assert TOKEN not in request.url
    assert all(TOKEN not in value for _name, value in request.params)


def test_build_request_emits_filters_in_a_fixed_order() -> None:
    request = logs_request(
        filters={
            "search": "boom",
            "level": "error,fatal",
            "statusCode": "5xx",
            "requestPath": "/api/checkout",
        }
    )
    names = [name for name, _value in request.params]
    assert names == [
        "projectId",
        "ownerId",
        "page",
        "startDate",
        "endDate",
        "level",
        "statusCode",
        "requestPath",
        "search",
    ]


def test_build_request_pages() -> None:
    assert ("page", "3") in logs_request(page=3).params


def test_build_request_refuses_a_parameter_that_is_not_on_the_allowlist() -> None:
    # The filters mapping reaches this function from the CLI, so it is the last
    # place an arbitrary query parameter could be introduced.
    with pytest.raises(ConfigError) as excinfo:
        logs_request(filters={"callback": "javascript:alert(1)"})
    assert "callback" in str(excinfo.value)


def test_build_request_drops_an_empty_filter_value() -> None:
    assert ("search", "") not in logs_request(filters={"search": ""}).params


def test_build_request_sends_no_team_parameter() -> None:
    # Verified live: teamId is not accepted here, and ownerId is what scopes the
    # call. Sending teamId as well would be cargo cult.
    names = [name for name, _value in logs_request().params]
    assert "teamId" not in names and "slug" not in names


def test_normalize_reads_the_fields_the_table_shows() -> None:
    entries, has_more = vi_logs.normalize(LOGS_PAGE)
    assert has_more is False
    entry = entries[0]
    assert entry.request_id == "abcde-1786964768933-0123456789ab"
    assert entry.status == 401
    assert entry.method == "GET"
    assert entry.path == "/api/me"
    assert entry.route == "/api/me"
    assert entry.source == "serverless"
    assert entry.region == "fra1"
    assert entry.duration_ms == 54
    assert entry.timestamp is not None
    assert entry.timestamp.isoformat() == "2026-08-17T11:06:08.933000+00:00"


def test_normalize_reads_an_empty_page() -> None:
    entries, has_more = vi_logs.normalize(LOGS_EMPTY_PAGE)
    assert entries == [] and has_more is False


def test_a_row_with_no_log_lines_has_no_level_and_no_headline() -> None:
    entry = vi_logs.normalize(LOGS_PAGE)[0][0]
    assert entry.lines == ()
    assert entry.worst_level is None
    assert entry.headline == ""


@pytest.mark.parametrize("spelling", ["ERROR", "Error", " error "])
def test_a_level_is_lower_cased_on_the_way_in(spelling: str) -> None:
    # Not cosmetic: worst_line ranks levels by an exact lower-case key in
    # LOG_LEVEL_SEVERITY, so an un-normalized "ERROR" would score below "info",
    # lose the ranking to any other line, and leave is_error returning False for
    # a request that logged a stack trace.
    payload = {
        "rows": [
            logs_row(
                statusCode=200,
                logs=[
                    {"level": "info", "message": "starting"},
                    {"level": spelling, "message": "boom"},
                ],
            )
        ]
    }
    entry = vi_logs.normalize(payload)[0][0]
    assert entry.worst_level == "error"
    assert entry.headline == "boom"
    assert entry.is_error is True


def test_the_worst_line_wins_the_level_and_the_headline() -> None:
    payload = {
        "rows": [
            logs_row(
                logs=[
                    {"level": "info", "message": "starting"},
                    {"level": "fatal", "message": "connection pool exhausted"},
                    {"level": "warning", "message": "slow"},
                ]
            )
        ]
    }
    entry = vi_logs.normalize(payload)[0][0]
    assert entry.worst_level == "fatal"
    assert entry.headline == "connection pool exhausted"


def test_a_5xx_is_an_error_even_with_no_log_line() -> None:
    entries, _ = vi_logs.normalize(LOGS_ERROR_PAGE)
    assert [entry.is_error for entry in entries] == [True, True]


def test_a_4xx_is_not_an_error() -> None:
    # A 401 on /api/me is the application working. Counting it would drown the
    # answer in noise and misreport a healthy site as broken.
    assert vi_logs.normalize(LOGS_PAGE)[0][0].is_error is False


def test_a_logged_error_on_a_200_is_an_error() -> None:
    payload = {
        "rows": [logs_row(statusCode=200, logs=[{"level": "error", "message": "boom"}])]
    }
    assert vi_logs.normalize(payload)[0][0].is_error is True


def test_a_crashed_function_is_an_error() -> None:
    payload = {"rows": [logs_row(statusCode=200, hasFunctionCrashed=True)]}
    assert vi_logs.normalize(payload)[0][0].is_error is True


def test_normalize_survives_a_row_that_is_missing_everything() -> None:
    # Real rows carry 30-odd fields and Vercel adds more over time. A row that
    # arrives short must degrade, not raise.
    entries, _ = vi_logs.normalize({"rows": [{}]})
    entry = entries[0]
    assert entry.request_id == ""
    assert entry.status is None
    assert entry.timestamp is None
    assert entry.label == "(unknown)"
    assert entry.is_error is False


def test_normalize_falls_back_to_the_path_when_the_route_is_empty() -> None:
    entry = vi_logs.normalize({"rows": [logs_row(route="")]})[0][0]
    assert entry.label == "/api/me"


def test_normalize_reports_an_unusable_payload_rather_than_raising() -> None:
    for payload in ({"rows": "nope"}, {"rows": [["not", "a", "row"]]}):
        with pytest.raises(ApiError) as excinfo:
            vi_logs.normalize(payload)
        assert excinfo.value.code == "invalid_response"


def test_normalize_keeps_the_raw_row_for_json_output() -> None:
    entry = vi_logs.normalize(LOGS_PAGE)[0][0]
    assert entry.raw["cache"] == "MISS"
    assert entry.raw["requestTags"] == ["ssr", "rsc"]


# ---------------------------------------------------------------------------
# Paging, merging and error presets
# ---------------------------------------------------------------------------


def _page(count: int, has_more: bool, first_id: int = 0) -> dict[str, Any]:
    return {
        "rows": [logs_row(requestId=f"r{first_id + index}") for index in range(count)],
        "hasMoreRows": has_more,
    }


def test_collect_stops_after_one_page_when_there_is_no_more() -> None:
    calls: list[int] = []

    def call(page: int) -> Mapping[str, Any]:
        calls.append(page)
        return _page(3, False)

    entries, truncated, pages = vi_logs.collect(call, limit=50)
    assert calls == [0]
    assert len(entries) == 3
    assert truncated is False and pages == 1


def test_collect_keeps_paging_until_the_budget_is_met() -> None:
    calls: list[int] = []

    def call(page: int) -> Mapping[str, Any]:
        calls.append(page)
        return _page(vi_logs.PAGE_SIZE, True, first_id=page * vi_logs.PAGE_SIZE)

    entries, truncated, pages = vi_logs.collect(call, limit=120)
    assert calls == [0, 1, 2]
    assert len(entries) == 120
    # More rows existed than were asked for, so this is a truncated answer.
    assert truncated is True and pages == 3


def test_collect_never_reads_more_than_the_page_cap() -> None:
    def call(page: int) -> Mapping[str, Any]:
        return _page(vi_logs.PAGE_SIZE, True, first_id=page * vi_logs.PAGE_SIZE)

    entries, truncated, pages = vi_logs.collect(call, limit=vi_logs.MAX_LIMIT)
    assert pages == vi_logs.MAX_PAGES
    assert len(entries) == vi_logs.MAX_LIMIT
    assert truncated is True


def test_collect_stops_on_a_short_page_even_when_the_api_claims_more() -> None:
    # Defensive: a short page means the server has nothing else for this query,
    # whatever hasMoreRows says. Trusting the flag alone would loop to the cap.
    def call(page: int) -> Mapping[str, Any]:
        return _page(2, True)

    entries, truncated, pages = vi_logs.collect(call, limit=50)
    assert pages == 1 and len(entries) == 2


def test_collect_does_not_trust_has_more_rows_off_a_short_page_that_meets_the_budget() -> None:
    # Regression: a short page means nothing else exists for this query,
    # whatever hasMoreRows claims, even when that same short page happens to
    # exactly fill the requested limit. A version that checks the budget
    # before the short-page rule (and lets hasMoreRows leak into that branch)
    # would report a truncated answer here even though there is truly nothing
    # left to fetch.
    def call(page: int) -> Mapping[str, Any]:
        return _page(2, True)

    entries, truncated, pages = vi_logs.collect(call, limit=2)
    assert pages == 1
    assert len(entries) == 2
    assert truncated is False


def test_collect_stops_at_an_explicit_max_pages_ceiling_and_reports_truncation() -> None:
    # The ceiling is its own stop condition, not merely a side effect of
    # MAX_LIMIT and MAX_PAGES lining up by construction: this pins it with an
    # explicit override, well short of the row budget, so the only reason
    # paging stops is the ceiling. Every remaining request past it would be
    # spent on data this call never even asks for.
    def call(page: int) -> Mapping[str, Any]:
        return _page(vi_logs.PAGE_SIZE, True, first_id=page * vi_logs.PAGE_SIZE)

    entries, truncated, pages = vi_logs.collect(call, limit=1000, max_pages=2)
    assert pages == 2
    assert len(entries) == 2 * vi_logs.PAGE_SIZE
    assert truncated is True


def test_merge_deduplicates_by_request_id() -> None:
    # A 500 that also logged an error comes back from both calls of the errors
    # preset. It is one request and must be reported once.
    shared = vi_logs.normalize(LOGS_ERROR_PAGE)[0]
    entries, _truncated = vi_logs.merge([shared, shared], limit=50)
    assert len(entries) == 2
    assert [entry.request_id for entry in entries] == ["err-1", "err-2"]


def test_merge_prefers_the_copy_that_carries_log_lines() -> None:
    bare = vi_logs.normalize({"rows": [logs_row(requestId="x", logs=[])]})[0]
    logged = vi_logs.normalize(
        {"rows": [logs_row(requestId="x", logs=[{"level": "error", "message": "boom"}])]}
    )[0]
    entries, _ = vi_logs.merge([bare, logged], limit=50)
    assert len(entries) == 1
    assert entries[0].headline == "boom"


def test_merge_sorts_newest_first() -> None:
    older = vi_logs.normalize(
        {"rows": [logs_row(requestId="old", timestamp="2026-08-17T10:00:00.000Z")]}
    )[0]
    newer = vi_logs.normalize(
        {"rows": [logs_row(requestId="new", timestamp="2026-08-17T11:00:00.000Z")]}
    )[0]
    entries, _ = vi_logs.merge([older, newer], limit=50)
    assert [entry.request_id for entry in entries] == ["new", "old"]


def test_merge_puts_a_row_with_no_timestamp_last_and_stays_deterministic() -> None:
    undated = vi_logs.normalize({"rows": [logs_row(requestId="b", timestamp="")]})[0]
    dated = vi_logs.normalize(
        {"rows": [logs_row(requestId="a", timestamp="2026-08-17T11:00:00.000Z")]}
    )[0]
    entries, _ = vi_logs.merge([undated, dated], limit=50)
    assert [entry.request_id for entry in entries] == ["a", "b"]


def test_merge_reports_truncation_when_it_drops_rows() -> None:
    many = vi_logs.normalize(_page(10, False))[0]
    entries, truncated = vi_logs.merge([many], limit=4)
    assert len(entries) == 4 and truncated is True


def test_error_filter_sets_queries_both_kinds_of_error() -> None:
    # Verified live: level matches log lines only, so a 500 that printed nothing
    # is invisible to level=error, and a 200 that logged a stack trace is
    # invisible to statusCode=5xx. Neither filter alone answers the question.
    assert vi_logs.error_filter_sets({}) == [
        {"statusCode": "5xx"},
        {"level": "error,fatal"},
    ]


def test_error_filter_sets_keeps_the_users_own_filters_on_both_calls() -> None:
    sets = vi_logs.error_filter_sets({"requestPath": "/api/checkout"})
    assert all(item["requestPath"] == "/api/checkout" for item in sets)


@pytest.mark.parametrize("override", [{"statusCode": "500"}, {"level": "warning"}])
def test_an_explicit_filter_collapses_the_errors_preset_to_one_call(
    override: dict[str, str],
) -> None:
    assert vi_logs.error_filter_sets(override) == [override]


def test_summarize_counts_by_status_worst_first() -> None:
    entries = vi_logs.normalize(
        {
            "rows": [
                logs_row(requestId="a", statusCode=500),
                logs_row(requestId="b", statusCode=500),
                logs_row(requestId="c", statusCode=502),
            ]
        }
    )[0]
    summary = vi_logs.summarize(entries)
    assert summary.total == 3
    assert summary.by_status == (("500", 2), ("502", 1))


def test_summarize_groups_routes_with_their_worst_status_and_window() -> None:
    entries = vi_logs.normalize(
        {
            "rows": [
                logs_row(
                    requestId="a",
                    route="/api/checkout",
                    statusCode=500,
                    timestamp="2026-08-17T10:00:00.000Z",
                ),
                logs_row(
                    requestId="b",
                    route="/api/checkout",
                    statusCode=502,
                    timestamp="2026-08-17T11:00:00.000Z",
                ),
            ]
        }
    )[0]
    tally = vi_logs.summarize(entries).by_route[0]
    assert tally.route == "/api/checkout"
    assert tally.count == 2
    assert tally.worst_status == 502
    assert tally.first_seen is not None and tally.first_seen.hour == 10
    assert tally.last_seen is not None and tally.last_seen.hour == 11


def test_summarize_groups_messages_by_exact_text() -> None:
    # Grouping by a guessed pattern would merge two different bugs into one row.
    entries = vi_logs.normalize(
        {
            "rows": [
                logs_row(requestId="a", logs=[{"level": "error", "message": "boom 1"}]),
                logs_row(requestId="b", logs=[{"level": "error", "message": "boom 1"}]),
                logs_row(requestId="c", logs=[{"level": "error", "message": "boom 2"}]),
            ]
        }
    )[0]
    summary = vi_logs.summarize(entries)
    assert [(item.message, item.count) for item in summary.by_message] == [
        ("boom 1", 2),
        ("boom 2", 1),
    ]


def test_summarize_gives_requests_that_logged_nothing_their_own_group() -> None:
    entries = vi_logs.normalize(LOGS_ERROR_PAGE)[0]
    summary = vi_logs.summarize(entries)
    assert (vi_logs.NO_LOG_LINE, 1) in [
        (item.message, item.count) for item in summary.by_message
    ]


def test_summarize_counts_the_errors_that_are_only_errors_because_they_logged() -> None:
    entries = vi_logs.normalize(
        {
            "rows": [
                logs_row(requestId="a", statusCode=500),
                logs_row(
                    requestId="b",
                    statusCode=200,
                    logs=[{"level": "fatal", "message": "pool exhausted"}],
                ),
            ]
        }
    )[0]
    # The status table groups by status alone, so this count is what keeps a 200
    # in that table from reading as a rendering bug.
    assert vi_logs.summarize(entries).logged_only == 1


#: Rows that are not 5xx and did not crash, and whose log lines do not make them
#: errors either. Every one of them was counted as "an error only because it
#: logged an error or fatal line" while that count looked at the status alone,
#: which made the output claim a log line its own message table denied.
NOT_LOGGED_ERRORS: list[tuple[str, dict[str, Any]]] = [
    ("a-401-that-logged-nothing", {"statusCode": 401, "logs": []}),
    ("a-404-that-logged-nothing", {"statusCode": 404, "logs": []}),
    (
        "a-200-that-only-warned",
        {"statusCode": 200, "logs": [{"level": "warning", "message": "slow"}]},
    ),
    (
        "a-200-that-only-noted",
        {"statusCode": 200, "logs": [{"level": "info", "message": "served"}]},
    ),
    ("a-row-with-no-status-at-all", {"statusCode": None, "logs": []}),
]


@pytest.mark.parametrize(
    "row", [row for _name, row in NOT_LOGGED_ERRORS], ids=[n for n, _r in NOT_LOGGED_ERRORS]
)
def test_summarize_does_not_count_a_row_that_logged_no_error_line(
    row: dict[str, Any],
) -> None:
    # The sentence built from this count says the row "logged an error or fatal
    # line", so a row that logged nothing, or logged only a warning, must not be
    # in it. Only the positive case was covered before, which is why an errors
    # run narrowed with --status-code 4xx printed that sentence over a table
    # whose every message cell read "(no log line)".
    entries = vi_logs.normalize({"rows": [logs_row(requestId="x", **row)]})[0]
    assert vi_logs.summarize(entries).logged_only == 0


def test_summarize_counts_a_logged_error_even_on_a_set_nobody_filtered() -> None:
    # The count is about the row, not about how the row was found: on a plain
    # logs run a 200 that logged a stack trace is still an error only because it
    # logged one, and the two ordinary rows beside it are not.
    entries = vi_logs.normalize(
        {
            "rows": [
                logs_row(requestId="a", statusCode=200),
                logs_row(requestId="b", statusCode=401),
                logs_row(
                    requestId="c",
                    statusCode=200,
                    logs=[{"level": "error", "message": "boom"}],
                ),
            ]
        }
    )[0]
    assert vi_logs.summarize(entries).logged_only == 1


def test_summarize_does_not_count_a_crashed_function_as_logging_its_way_in() -> None:
    # A crash is its own reason to be an error, so "only because it logged" is
    # false of it even when it did also log.
    entries = vi_logs.normalize(
        {
            "rows": [
                logs_row(
                    requestId="a",
                    statusCode=200,
                    hasFunctionCrashed=True,
                    logs=[{"level": "fatal", "message": "boom"}],
                )
            ]
        }
    )[0]
    assert vi_logs.summarize(entries).logged_only == 0


def test_summarize_of_nothing_is_empty_rather_than_an_error() -> None:
    summary = vi_logs.summarize([])
    assert summary.total == 0
    assert summary.by_status == () and summary.by_route == ()
