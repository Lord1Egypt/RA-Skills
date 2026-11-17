"""Everything a response carries is untrusted, including the parts that are not labels.

Row labels were hardened first, because a UTM campaign is literally whatever a
visitor typed into a query string. Review then found three more values from the
same response that reach a terminal without passing that boundary: a ``Location``
header, Vercel's own ``error.message``, and a metric name claimed off a row,
which becomes a table column header and a CSV header cell.

This module pins all of them, plus two adjacent robustness properties found at
the same time: a number that overflows to infinity on the way in, and a bare
credential too short to substring match safely.
"""

from __future__ import annotations

import csv
import io
import json

import pytest
from conftest import Cli
from helpers import PROJECT, TOKEN, FakeResponse, FakeSession, logs_row

from vercel_insights import logs as vi_logs
from vercel_insights.http import MIN_SCRUBBABLE_CREDENTIAL, scrub_credentials

#: An escape that clears the screen, a bell, and a carriage return that would
#: rewrite the line already printed. None of these may reach stdout or stderr.
HOSTILE = "\x1b[2J\x07\rwiped"

ENV = {"VERCEL_TOKEN": TOKEN, "VERCEL_PROJECT_ID": PROJECT}


def _has_raw_control(text: str) -> bool:
    """True when any C0/C1 control character survived into ``text``."""
    return any(ord(ch) < 0x20 and ch != "\n" or 0x7F <= ord(ch) <= 0x9F for ch in text)


# ---------------------------------------------------------------------------
# A Location header is remote input
# ---------------------------------------------------------------------------


def test_a_hostile_location_header_cannot_paint_the_terminal(cli: Cli) -> None:
    session = FakeSession(
        FakeResponse(302, {}, {"Location": f"https://evil.example/{HOSTILE}"})
    )
    code, out, err = cli.run(["top-pages"], env=ENV, session=session)
    assert code == 1
    assert not _has_raw_control(err), "a raw control character reached stderr"
    assert "\\x1b" in err, "the escape should still be visible, not dropped"
    assert not _has_raw_control(out)


# ---------------------------------------------------------------------------
# Vercel's own error message is remote input
# ---------------------------------------------------------------------------


def test_a_hostile_server_error_message_cannot_forge_a_second_line(cli: Cli) -> None:
    # The dangerous shape is a message that blanks the screen and then prints
    # something reassuring under our own "error:" prefix.
    body = {"error": {"code": "bad_request", "message": f"oops{HOSTILE}"}}
    session = FakeSession(FakeResponse(400, body))
    code, _out, err = cli.run(["top-pages"], env=ENV, session=session)
    assert code == 1
    assert not _has_raw_control(err)
    assert "\\x1b" in err
    # The wording Vercel sent is still readable, just neutralised.
    assert "oops" in err


# ---------------------------------------------------------------------------
# A metric name claimed off a row becomes a column header
# ---------------------------------------------------------------------------


def _row_with_hostile_metric_name() -> dict[str, object]:
    return {
        "version": 1,
        "query": {"groupBy": ["requestPath"], "limit": 10},
        "data": [{"requestPath": "/a", "pageviews": 5, f"{HOSTILE}bogus": 7}],
    }


def test_a_hostile_metric_name_cannot_reach_a_table_header(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, _row_with_hostile_metric_name()))
    code, out, err = cli.run(["top-pages"], env=ENV, session=session)
    assert code == 0, err
    assert not _has_raw_control(out), "a raw control character reached a column header"
    assert "\\x1b" in out


def test_a_hostile_metric_name_cannot_break_the_csv_header_row(cli: Cli) -> None:
    session = FakeSession(FakeResponse(200, _row_with_hostile_metric_name()))
    code, out, err = cli.run(["top-pages", "--csv"], env=ENV, session=session)
    assert code == 0, err
    assert not _has_raw_control(out)
    rows = list(csv.reader(io.StringIO(out)))
    # A raw carriage return inside a header cell would split the header in two.
    assert len({len(row) for row in rows if row}) == 1, "the CSV came out ragged"


# ---------------------------------------------------------------------------
# A request-logs row is remote input
# ---------------------------------------------------------------------------


def test_a_log_message_cannot_repaint_the_terminal() -> None:
    entry = vi_logs.normalize(
        {"rows": [logs_row(logs=[{"level": "error", "message": "\x1b[2Jerror: fine"}])]}
    )[0][0]
    assert "\x1b" not in entry.headline
    assert "\\x1b" in entry.headline


def test_a_hostile_request_path_is_escaped() -> None:
    entry = vi_logs.normalize({"rows": [logs_row(requestPath="/a\rerror: fine")]})[0][0]
    assert "\r" not in entry.path
    assert "\\x0d" in entry.path


def test_a_multi_line_log_message_keeps_its_lines_but_is_indented() -> None:
    # A stack trace is the one place newlines carry meaning, so they survive.
    # Every line after the first is indented, so nothing the server sends can
    # reach column zero and forge a line of this tool's own output.
    message = "Error: boom\nat handler (/api/checkout)"
    entry = vi_logs.normalize(
        {"rows": [logs_row(logs=[{"level": "error", "message": message}])]}
    )[0][0]
    assert entry.headline.splitlines()[1].startswith("  ")


# ---------------------------------------------------------------------------
# A number can overflow to infinity without tripping parse_constant
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("literal", ["1e999", "-1e999", "1E400"])
def test_a_number_that_overflows_to_infinity_is_refused(cli: Cli, literal: str) -> None:
    # json.loads reads 1e999 as inf without ever calling parse_constant, so the
    # three bare-token literals are not the whole story.
    text = f'{{"version":1,"query":{{}},"data":{{"pageviews":{literal},"visitors":3}}}}'
    session = FakeSession(FakeResponse(200, text=text))
    code, out, err = cli.run(["total"], env=ENV, session=session)
    assert code == 1
    assert "invalid_response" in err
    assert "inf" not in out.lower()


def test_an_infinity_never_escapes_through_json_output(cli: Cli) -> None:
    # A bare Infinity is not JSON, and the README sells piping --json into jq.
    text = '{"version":1,"query":{},"data":{"pageviews":1e999,"visitors":3}}'
    session = FakeSession(FakeResponse(200, text=text))
    code, out, _err = cli.run(["total", "--json"], env=ENV, session=session)
    assert code == 1
    assert "Infinity" not in out
    if out.strip():
        json.loads(out)  # whatever was printed must be real JSON


# ---------------------------------------------------------------------------
# A redirect reports how many requests actually went out
# ---------------------------------------------------------------------------


def test_a_redirect_after_retries_reports_the_real_attempt_count(cli: Cli) -> None:
    # Reporting one attempt when three requests went out is misleading exactly
    # when a flaky proxy is the suspect, which is what this message is for.
    failure = {"error": {"code": "server_error", "message": "boom"}}
    session = FakeSession(
        FakeResponse(503, failure),
        FakeResponse(503, failure),
        FakeResponse(302, {}, {"Location": "https://elsewhere.example/"}),
    )
    code, _out, err = cli.run(
        ["top-pages", "--max-retries", "3"], env=ENV, session=session
    )
    assert code == 1
    assert len(session.calls) == 3
    assert "3 attempt" in err


# ---------------------------------------------------------------------------
# A credential too short to substring match safely
# ---------------------------------------------------------------------------


def test_a_short_credential_is_not_substring_matched_into_confetti() -> None:
    # A one character token would rewrite "https" as "h<redacted><redacted>ps"
    # and make every message unreadable.
    headers = {"Authorization": "Bearer t"}
    text = "https://api.vercel.com/v1/query/web-analytics/visits/count"
    assert scrub_credentials(text, headers) == text


def test_a_credential_at_the_threshold_is_still_scrubbed() -> None:
    secret = "x" * MIN_SCRUBBABLE_CREDENTIAL
    headers = {"Authorization": f"Bearer {secret}"}
    assert secret not in scrub_credentials(f"leaked {secret} here", headers)


def test_the_whole_header_value_is_scrubbed_however_short_the_token() -> None:
    # Declining to substring match a short bare token exposes nothing: the full
    # header value is still replaced wherever it appears.
    headers = {"Authorization": "Bearer t"}
    assert "Bearer t" not in scrub_credentials("saw Bearer t in the wild", headers)
