"""Tests for the request logs renderers."""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Mapping
from typing import Any

import pytest
from helpers import LOGS_EMPTY_PAGE, LOGS_ERROR_PAGE, logs_row, utc

from vercel_insights import logs as vi_logs
from vercel_insights.render import (
    LogReport,
    format_logs_csv,
    format_logs_json,
    render_error_summary,
    render_logs,
)

WINDOW = (utc(2026, 8, 17, 10, 36), utc(2026, 8, 17, 11, 6))


def _report(payload: Mapping[str, Any], **overrides: object) -> LogReport:
    entries, _more = vi_logs.normalize(payload)
    kwargs: dict[str, object] = {
        "time_range": WINDOW,
        "project_label": "acme-docs",
        "preset": "errors",
        "filters": {},
        "truncated": False,
        "pages_fetched": 1,
        "requested_limit": 50,
        "counts_errors": True,
    }
    kwargs.update(overrides)
    return vi_logs.build_report(entries, **kwargs)  # type: ignore[arg-type]


def test_the_table_shows_one_row_per_request() -> None:
    text = render_logs(_report(LOGS_ERROR_PAGE))
    assert "Vercel request logs: acme-docs (errors" in text
    assert "Range: 2026-08-17T10:36:00Z to 2026-08-17T11:06:00Z (UTC)" in text
    assert "/api/checkout" in text
    # The fixture message is 46 characters, wider than LOG_MESSAGE_WIDTH (34),
    # so the compact table truncates it; the untruncated form is covered by
    # test_expand_prints_the_whole_message_under_the_row instead.
    assert "TypeError: Cannot read properties" in text
    assert "500" in text and "502" in text


def test_the_header_says_what_counts_as_an_error() -> None:
    text = render_logs(_report(LOGS_ERROR_PAGE))
    assert vi_logs.ERROR_DEFINITION in text


@pytest.mark.parametrize(
    ("filters", "expected"),
    [
        ({"statusCode": "4xx"}, "statusCode 4xx"),
        ({"level": "warning"}, "level warning"),
        ({"level": "error", "statusCode": "5xx"}, "level error and statusCode 5xx"),
    ],
    ids=["status", "level", "both"],
)
def test_an_explicit_filter_replaces_the_error_definition_with_what_ran(
    filters: dict[str, str], expected: str
) -> None:
    # An explicit --level or --status-code collapses the errors preset to one
    # call carrying that filter, so the rows are whatever it matched. Printing
    # the error definition there would describe a query that never ran.
    text = render_logs(_report(LOGS_ERROR_PAGE, filters=filters))
    assert vi_logs.ERROR_DEFINITION not in text
    assert f"These rows are what {expected} matched" in text


def test_a_narrowed_run_does_not_call_its_rows_errors() -> None:
    # Same reason: --status-code 4xx asks for 401s, and a 401 is not an error by
    # any definition this tool holds, so the count sentence must not say it is.
    text = render_logs(_report(LOGS_ERROR_PAGE, filters={"statusCode": "4xx"}))
    assert "2 requests in 30 minutes" in text
    assert "2 errors" not in text


def test_a_plain_logs_report_still_carries_no_header_note() -> None:
    # counts_errors is False there, so there is no definition to state and no
    # filter to explain away: the table speaks for itself.
    report = _report(LOGS_ERROR_PAGE, preset="logs", counts_errors=False)
    assert report.header_note is None
    assert "2 requests in 30 minutes" in render_logs(report)


def test_a_request_that_logged_nothing_says_so_rather_than_showing_a_blank() -> None:
    text = render_logs(_report(LOGS_ERROR_PAGE))
    assert "(no log line" in text


def test_a_row_with_no_level_shows_a_dash() -> None:
    lines = render_logs(_report(LOGS_ERROR_PAGE)).splitlines()
    row = next(line for line in lines if "/api/documents/[slug]" in line)
    assert " -  " in row or row.split()[1] == "-"


def test_expand_prints_the_whole_message_under_the_row() -> None:
    long_message = "Error: " + "x" * 200
    payload = {
        "rows": [
            {
                "requestId": "a",
                "timestamp": "2026-08-17T11:00:00.000Z",
                "statusCode": 500,
                "requestPath": "/api/checkout",
                "logs": [{"level": "error", "message": long_message}],
            }
        ]
    }
    compact = render_logs(_report(payload))
    expanded = render_logs(_report(payload), expand=True)
    assert long_message not in compact
    assert long_message in expanded


def test_an_empty_result_names_the_window_and_the_retention_limits() -> None:
    # Six hours is longer than the shortest retention any plan has, so an empty
    # answer here genuinely might be aged-out logs rather than a healthy site.
    text = render_logs(
        _report(
            LOGS_EMPTY_PAGE,
            time_range=(utc(2026, 8, 17, 5, 6), utc(2026, 8, 17, 11, 6)),
        )
    )
    assert "No request logs" in text
    assert "1 hour on Hobby" in text


def test_a_thirty_minute_window_does_not_lecture_about_retention() -> None:
    # Inside the shortest retention window there is nothing to warn about, and a
    # warning on every empty answer trains the reader to ignore it. WINDOW is 30
    # minutes.
    text = render_logs(_report(LOGS_EMPTY_PAGE))
    assert "No request logs" in text
    assert "1 hour on Hobby" not in text


def test_truncation_is_stated_rather_than_implied() -> None:
    text = render_logs(_report(LOGS_ERROR_PAGE, truncated=True, requested_limit=2))
    assert "more" in text.lower()
    # Two rows out of a possible 200, so there is room to ask for more.
    assert f"Raise --limit (up to {vi_logs.MAX_LIMIT})" in text


def test_a_truncated_report_counts_the_rows_shown_not_the_window() -> None:
    # There were not 2 errors in 30 minutes: there were more, and these are the
    # 2 most recent of them. The sentence has to say which it is describing.
    text = render_logs(_report(LOGS_ERROR_PAGE, truncated=True, requested_limit=2))
    assert "Showing the most recent 2 of more errors that matched in 30 minutes" in text
    assert "2 errors in 30 minutes" not in text


def test_a_truncated_report_scopes_its_ranking_to_the_rows_shown() -> None:
    # A most-affected route computed over the most recent N is a fact about
    # those N rows, not about the window, and reading it as a ranking of the
    # window is exactly the mistake an unqualified line invites.
    payload = {
        "rows": [
            *LOGS_ERROR_PAGE["rows"],
            {
                "requestId": "err-3",
                "timestamp": "2026-08-17T11:01:00.000Z",
                "statusCode": 500,
                "requestPath": "/api/checkout",
                "route": "/api/checkout",
            },
        ]
    }
    truncated = render_logs(_report(payload, truncated=True, requested_limit=3))
    assert "Most affected route among the rows shown: /api/checkout (2)." in truncated
    whole = render_logs(_report(payload))
    assert "Most affected route: /api/checkout (2)." in whole


def test_a_tie_at_the_top_is_not_reported_as_a_most_affected_route() -> None:
    # LOGS_ERROR_PAGE holds one row on each of two routes, so the leader is
    # whichever sorted first alphabetically. Printing that as "most affected"
    # reports the tiebreak as a finding.
    text = render_logs(_report(LOGS_ERROR_PAGE))
    assert "Most affected route" not in text


def test_one_route_alone_is_not_reported_as_most_affected_either() -> None:
    payload = {"rows": [logs_row(requestId="a", statusCode=500)]}
    assert "Most affected route" not in render_logs(_report(payload))


def test_a_truncation_at_the_ceiling_does_not_advise_raising_the_limit() -> None:
    # The error-summary preset already asks for MAX_LIMIT, so "raise --limit (up
    # to 200)" would be telling a reader who is at 200 to go to 200. Advice that
    # cannot be followed is worse than none, so the remedy offered is the one
    # that is left.
    text = render_logs(
        _report(LOGS_ERROR_PAGE, truncated=True, requested_limit=vi_logs.MAX_LIMIT)
    )
    assert "more" in text.lower()
    assert "Raise --limit" not in text
    assert "narrow the window" in text


def test_a_two_call_truncation_says_it_is_the_most_recent_of_each_kind() -> None:
    # No explicit level or statusCode filter, so the errors preset ran its two
    # calls and merged them: what was cut is per kind, not a global top N, and
    # the footer must say so rather than let the generic sentence imply less.
    text = render_logs(_report(LOGS_ERROR_PAGE, truncated=True, requested_limit=2))
    assert "the most recent 2 of each kind rather than a global top 2" in text


def test_a_single_call_truncation_does_not_claim_a_merge_that_did_not_happen() -> None:
    # An explicit --level (or --status-code) collapses the errors preset to one
    # call, so there was no per-kind merge, and the sharper sentence would be a
    # lie here: it must not appear.
    text = render_logs(
        _report(
            LOGS_ERROR_PAGE,
            truncated=True,
            requested_limit=2,
            filters={"level": "error"},
        )
    )
    assert "of each kind" not in text


def test_the_footer_counts_the_errors_by_status() -> None:
    text = render_logs(_report(LOGS_ERROR_PAGE))
    assert "2 errors" in text


def test_expand_keeps_a_multiline_message_indented_under_its_row() -> None:
    # sanitize_message indents continuation lines by two spaces so nothing a
    # server sends can reach column zero; render_logs must add its own indent
    # on top of that on every line, not only the first, or a stack trace steps
    # backwards under --expand instead of staying nested under its row.
    payload = {
        "rows": [
            {
                "requestId": "trace-1",
                "timestamp": "2026-08-17T11:00:00.000Z",
                "statusCode": 500,
                "requestPath": "/api/checkout",
                "logs": [
                    {
                        "level": "error",
                        "message": "Error: boom\nat foo (a.js:1)\nat bar (b.js:2)",
                    }
                ],
            }
        ]
    }
    text = render_logs(_report(payload), expand=True)
    lines = [
        line
        for line in text.splitlines()
        if line.startswith(" ")
        and ("boom" in line or "at foo" in line or "at bar" in line)
    ]
    assert len(lines) == 3
    indents = [len(line) - len(line.lstrip(" ")) for line in lines]
    assert all(indent >= indents[0] for indent in indents)


def test_a_row_with_no_timestamp_says_so_rather_than_leaving_a_blank() -> None:
    payload = {
        "rows": [
            {
                "requestId": "no-time",
                "statusCode": 500,
                "requestPath": "/api/checkout",
            }
        ]
    }
    text = render_logs(_report(payload))
    assert "(no time)" in text


def test_a_window_over_a_day_shows_the_date_in_the_time_column() -> None:
    text = render_logs(
        _report(
            LOGS_ERROR_PAGE,
            time_range=(utc(2026, 8, 15, 11, 6), utc(2026, 8, 17, 11, 6)),
        )
    )
    assert "08-17 11:04:52" in text


# ---------------------------------------------------------------------------
# render_error_summary
# ---------------------------------------------------------------------------


def test_the_summary_prints_three_tables() -> None:
    report = _report(LOGS_ERROR_PAGE, preset="error-summary")
    text = render_error_summary(report, vi_logs.summarize(report.entries))
    assert "status" in text and "route" in text and "message" in text
    assert "TOTAL" in text
    assert "100.0%" in text


def test_the_summary_explains_a_non_5xx_row_in_the_status_table() -> None:
    payload = {
        "rows": [
            {
                "requestId": "a",
                "statusCode": 200,
                "timestamp": "2026-08-17T11:00:00.000Z",
                "logs": [{"level": "fatal", "message": "pool exhausted"}],
            }
        ]
    }
    report = _report(payload, preset="error-summary")
    text = render_error_summary(report, vi_logs.summarize(report.entries))
    assert "logged" in text
    # The "logged" word above is satisfied by the trailing note no matter what
    # the status table renders, so the property this test actually owns (a
    # level never leaks into the status column) needs its own assertion,
    # scoped to the status table itself: "fatal" legitimately appears in the
    # note's prose ("... error or fatal line"), so a whole-text search for it
    # would be a false positive there.
    lines = text.splitlines()
    start = next(
        index for index, line in enumerate(lines) if line.split()[:1] == ["status"]
    )
    status_table = lines[start : lines.index("", start)]
    assert any(line.split()[0] == "200" for line in status_table)
    assert not any("fatal" in line for line in status_table)


def test_the_summary_names_the_filter_that_produced_its_tables() -> None:
    # This renderer prints no header note, so without this line a narrowed run
    # showed three tables and a count of matching rows with nothing on screen
    # saying what they had been narrowed to.
    report = _report(
        LOGS_ERROR_PAGE, preset="error-summary", filters={"statusCode": "4xx"}
    )
    text = render_error_summary(report, vi_logs.summarize(report.entries))
    assert "Filter: statusCode 4xx" in text
    assert "2 requests in 30 minutes" in text
    assert "2 errors" not in text


def test_the_summary_names_the_window_rather_than_printing_empty_tables() -> None:
    # render_error_summary's empty branch is not in the brief and no test
    # called it; this pins the behaviour the reviewer confirmed by hand.
    report = _report(
        LOGS_EMPTY_PAGE,
        preset="error-summary",
        time_range=(utc(2026, 8, 17, 5, 6), utc(2026, 8, 17, 11, 6)),
    )
    text = render_error_summary(report, vi_logs.summarize(report.entries))
    assert "No request logs" in text
    assert "TOTAL" not in text
    # Six hours is over the shortest retention, so the retention note, composed
    # in build_report rather than by this renderer, should still surface after
    # the empty-tables message.
    assert "1 hour on Hobby" in text


def test_json_output_keeps_every_field_the_api_sent() -> None:
    report = _report(LOGS_ERROR_PAGE)
    parsed = json.loads(format_logs_json(report))
    assert parsed["truncated"] is False
    assert parsed["pagesFetched"] == 1
    first = parsed["entries"][0]
    assert first["requestId"] == "err-1"
    assert first["status"] == 500
    assert first["lines"][0]["level"] == "error"
    # Nothing probed is thrown away: the whole row is still there.
    assert first["raw"]["cache"] == "MISS"


def test_json_output_refuses_a_non_finite_number_rather_than_emit_one() -> None:
    # http.py's response parser already walks every real response body and
    # refuses a NaN, Infinity or -Infinity with an invalid_response error, so
    # this can never actually reach `raw` from a live API call. allow_nan=False
    # is a second line of defence: if a non-finite float ever did get here some
    # other way, this must refuse to write it out as something jq would
    # reject, rather than silently emit a bare NaN token.
    payload = {"rows": [{"requestId": "a", "cacheReason": float("nan")}]}
    with pytest.raises(ValueError):
        format_logs_json(_report(payload))


def test_json_output_escapes_a_control_character_in_the_raw_row() -> None:
    # raw is the one field kept verbatim, so this is what makes that safe: it
    # only ever leaves through json.dumps, which escapes the escape.
    payload = {"rows": [{"requestId": "a", "cacheReason": "\x1b[2Jgone"}]}
    text = format_logs_json(_report(payload))
    assert "\x1b" not in text
    assert "\\u001b" in text


def test_csv_output_has_one_row_per_request() -> None:
    text = format_logs_csv(_report(LOGS_ERROR_PAGE))
    rows = list(csv.reader(io.StringIO(text)))
    assert rows[0] == [
        "time",
        "level",
        "status",
        "method",
        "route",
        "path",
        "source",
        "requestId",
        "message",
    ]
    assert len(rows) == 3


def test_csv_keeps_a_hostile_message_inside_one_cell() -> None:
    payload = {
        "rows": [
            {
                "requestId": "a",
                "statusCode": 500,
                "logs": [{"level": "error", "message": "a\r\nerror: fine"}],
            }
        ]
    }
    rows = list(csv.reader(io.StringIO(format_logs_csv(_report(payload)))))
    assert len(rows) == 2
