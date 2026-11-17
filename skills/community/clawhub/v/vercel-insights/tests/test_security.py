"""The security invariants from docs/cli-contract.md, as executable tests.

These are properties of the package as a whole rather than of one module, so
they live together: the operation allowlist, the fact that the token only ever
appears in one header, and the source level bans.
"""

from __future__ import annotations

import json
import re
from typing import Any

import pytest
import requests
from conftest import Cli
from helpers import (
    BASE_ENV,
    CONTROL_CHARACTER_CAMPAIGN_PAYLOAD,
    COUNTRY_PAYLOAD,
    DAILY_PAYLOAD,
    DRY_RUN_ENV,
    ESCAPED_ANSI_CAMPAIGN,
    LOGS_PAGE,
    PROJECT,
    SECRET,
    SPEED_ROUTE_PAYLOAD,
    TESTS_DIR,
    TOKEN,
    TOP_PAGES_PAYLOAD,
    VISITS_COUNT_PAYLOAD,
    FakeResponse,
    FakeSession,
    ForbiddenSession,
    Recorder,
    dry_run_values,
    error_payload,
    logs_request,
    logs_row,
    no_jitter,
    package_source_text,
    package_sources,
    prepared,
    speed_request,
    utc,
)

from vercel_insights import ApiError, ConfigError
from vercel_insights import http as vi_http
from vercel_insights.http import (
    OPERATIONS,
    PreparedRequest,
    execute,
    format_dry_run,
    operation_url,
    redact_headers,
    scrub_credentials,
    validate_token,
)
from vercel_insights.render import format_csv, format_json, format_table
from vercel_insights.speedinsights import normalize as normalize_speed
from vercel_insights.speedinsights import validate_metric
from vercel_insights.webanalytics import normalize

# ---------------------------------------------------------------------------
# 1. The operation allowlist
# ---------------------------------------------------------------------------

# Transcribed by hand from docs/cli-contract.md and docs/api-notes.md, not read
# back from OPERATIONS: a test that iterates the table it is checking cannot
# notice a fourth entry being added to it.
DOCUMENTED_OPERATIONS: dict[str, tuple[str, str]] = {
    "web_analytics": (
        "GET",
        "https://api.vercel.com/v1/query/web-analytics/{dataset}/{endpoint}",
    ),
    "observability_query": ("POST", "https://api.vercel.com/v2/observability/query"),
    "observability_schema": ("GET", "https://api.vercel.com/v2/observability/schema"),
    # Read-only. A Speed Insights scope requires an ownerId, and the project's
    # own record carries it as accountId.
    "project": ("GET", "https://api.vercel.com/v9/projects/{project}"),
    # Read-only. One account holds many projects, and naming the right one is
    # the first thing any query needs.
    "projects": ("GET", "https://api.vercel.com/v10/projects"),
    # Read-only. Runtime request logs, and the only entry not on api.vercel.com:
    # Vercel serves this one from the dashboard host, and it is the endpoint the
    # official `vercel logs` command calls. See docs/api-notes.md.
    "request_logs": ("GET", "https://vercel.com/api/logs/request-logs"),
}


def test_operations_holds_exactly_the_six_documented_entries() -> None:
    assert set(OPERATIONS) == set(DOCUMENTED_OPERATIONS)
    assert len(OPERATIONS) == 6


@pytest.mark.parametrize("operation", sorted(DOCUMENTED_OPERATIONS))
def test_each_operation_has_exactly_its_documented_method_and_url(
    operation: str,
) -> None:
    assert OPERATIONS[operation] == DOCUMENTED_OPERATIONS[operation]


def test_only_one_operation_is_a_post_and_every_other_is_a_get() -> None:
    methods = sorted(method for method, _ in OPERATIONS.values())
    assert methods == ["GET", "GET", "GET", "GET", "GET", "POST"]


#: The only hosts this client may address. Written out by hand rather than read
#: back from OPERATIONS: a test that derives the answer from the table it is
#: checking cannot notice the table naming a host nobody approved.
DOCUMENTED_HOSTS: frozenset[str] = frozenset(
    {"https://api.vercel.com/", "https://vercel.com/api/"}
)


@pytest.mark.parametrize("operation", sorted(DOCUMENTED_OPERATIONS))
def test_every_allowlisted_url_is_on_a_documented_host(operation: str) -> None:
    _method, url = OPERATIONS[operation]
    assert any(url.startswith(host) for host in DOCUMENTED_HOSTS), url


def test_the_write_toggle_endpoints_are_absent_from_the_package() -> None:
    # The same API exposes toggles that enable or disable a feature. They are
    # writes, and nothing here may reference them.
    source = package_source_text()
    assert "/speed-insights/toggle" not in source
    assert "/web/insights/toggle" not in source
    for _method, url in OPERATIONS.values():
        assert "toggle" not in url


def test_operation_url_refuses_an_operation_that_is_not_on_the_allowlist() -> None:
    with pytest.raises(ConfigError) as excinfo:
        operation_url("speed_insights_toggle")
    assert "unknown operation" in str(excinfo.value)


@pytest.mark.parametrize(
    "dataset",
    [
        "../../../v13/deployments",
        "visits/count",
        "",
        "visits?teamId=x",
        "https://evil.example",
        "..",
        ".",
        "visits count",
    ],
)
def test_operation_url_refuses_anything_that_is_not_a_path_segment(
    dataset: str,
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        operation_url("web_analytics", dataset=dataset, endpoint="count")
    assert "path segment" in str(excinfo.value)


def test_operation_url_builds_the_documented_url_for_a_legal_pair() -> None:
    assert operation_url("web_analytics", dataset="visits", endpoint="aggregate") == (
        "https://api.vercel.com/v1/query/web-analytics/visits/aggregate"
    )
    assert operation_url("observability_schema") == (
        "https://api.vercel.com/v2/observability/schema"
    )


def test_a_prepared_request_refuses_an_operation_that_is_not_on_the_allowlist() -> None:
    with pytest.raises(ConfigError) as excinfo:
        PreparedRequest(
            operation="delete_project",
            url="https://api.vercel.com/v9/projects/prj",
            params=[],
            headers={},
        )
    assert "unknown operation" in str(excinfo.value)


@pytest.mark.parametrize(
    "url",
    [
        "https://evil.example/v1/query/web-analytics/visits/count",
        "http://api.vercel.com/v1/query/web-analytics/visits/count",
        "https://api.vercel.com/v13/deployments",
        "https://api.vercel.com/v2/observability/query",
        "https://api.vercel.com/v1/query/web-analytics/visits/count/extra",
        "https://api.vercel.com/v1/query/web-analytics/visits",
        "https://api.vercel.com.evil.example/v1/query/web-analytics/visits/count",
    ],
)
def test_a_prepared_request_refuses_a_url_its_operation_cannot_address(
    url: str,
) -> None:
    with pytest.raises(ConfigError) as excinfo:
        PreparedRequest(operation="web_analytics", url=url, params=[], headers={})
    assert "cannot address" in str(excinfo.value)


def test_a_static_operation_url_has_to_match_the_template_exactly() -> None:
    with pytest.raises(ConfigError):
        PreparedRequest(
            operation="observability_query",
            url="https://api.vercel.com/v2/observability/query/../../v13/deployments",
            params=[],
            headers={},
        )


@pytest.mark.parametrize(
    "url",
    [
        "https://vercel.com/api/logs/request-logs/extra",
        "https://vercel.com/api/logs",
        "http://vercel.com/api/logs/request-logs",
        "https://vercel.com.evil.example/api/logs/request-logs",
        "https://api.vercel.com/api/logs/request-logs",
    ],
)
def test_request_logs_cannot_address_anything_else(url: str) -> None:
    with pytest.raises(ConfigError):
        PreparedRequest(operation="request_logs", url=url, params=[], headers={})


def test_the_method_is_read_from_the_allowlist_and_cannot_be_set() -> None:
    request = prepared()
    assert request.method == OPERATIONS[request.operation][0] == "GET"
    with pytest.raises(AttributeError):
        request.method = "DELETE"  # type: ignore[misc]


def test_the_dispatcher_uses_only_the_verb_its_operation_names() -> None:
    # A session that offers nothing but get and post: any other verb would
    # raise AttributeError here rather than reaching the network.
    class OnlyGetAndPost:
        def __init__(self) -> None:
            self.verbs: list[str] = []

        def get(self, url: str, **kwargs: Any) -> FakeResponse:
            self.verbs.append("GET")
            return FakeResponse(200, COUNTRY_PAYLOAD)

        def post(self, url: str, **kwargs: Any) -> FakeResponse:
            self.verbs.append("POST")
            return FakeResponse(200, COUNTRY_PAYLOAD)

    session = OnlyGetAndPost()
    execute(prepared(), session, sleep=Recorder(), jitter=no_jitter)
    execute(
        PreparedRequest(
            operation="observability_query",
            url="https://api.vercel.com/v2/observability/query",
            params=[],
            headers={},
            json_body={"metric": "vercel.speed_insights.lcp_ms"},
        ),
        session,
        sleep=Recorder(),
        jitter=no_jitter,
    )
    assert session.verbs == ["GET", "POST"]


# ---------------------------------------------------------------------------
# 2. Source level bans
# ---------------------------------------------------------------------------


def test_the_package_has_exactly_one_get_and_one_post_call_site() -> None:
    source = package_source_text()
    assert source.count("session.get(") == 1
    assert source.count("session.post(") == 1


@pytest.mark.parametrize(
    "verb", ["put", "patch", "delete", "head", "options", "request"]
)
def test_no_other_http_verb_appears_anywhere_in_the_package(verb: str) -> None:
    source = package_source_text()
    assert f"session.{verb}(" not in source
    assert f"requests.{verb}(" not in source


def test_the_two_http_call_sites_are_both_inside_http_py() -> None:
    for path in package_sources():
        text = path.read_text(encoding="utf-8")
        if path.name == "http.py":
            assert "session.get(" in text and "session.post(" in text
        else:
            assert "session.get(" not in text
            assert "session.post(" not in text


@pytest.mark.parametrize(
    "pattern",
    [
        r"\beval\s*\(",
        r"\bexec\s*\(",
        r"\bsubprocess\b",
        r"\bos\.system\b",
        r"\bopen\s*\(",
    ],
)
def test_the_package_has_no_dynamic_execution_or_filesystem_writes(
    pattern: str,
) -> None:
    assert re.search(pattern, package_source_text()) is None


def test_neither_the_package_nor_this_suite_uses_an_em_dash() -> None:
    em_dash = "\u2014"  # an escape, so this file stays free of the character
    for path in [*package_sources(), *sorted(TESTS_DIR.glob("*.py"))]:
        assert em_dash not in path.read_text(encoding="utf-8"), path


# ---------------------------------------------------------------------------
# 3. The token lives in exactly one place
# ---------------------------------------------------------------------------


def test_redact_headers_replaces_every_credential() -> None:
    safe = redact_headers(
        {
            "Authorization": f"Bearer {TOKEN}",
            "Cookie": "session=abc",
            "Accept": "application/json",
        }
    )
    assert safe["Authorization"] == "Bearer <redacted>"
    assert safe["Cookie"] == "<redacted>"
    assert safe["Accept"] == "application/json"
    assert TOKEN not in json.dumps(safe)


def test_redact_headers_does_not_mutate_the_original_headers() -> None:
    headers = {"Authorization": f"Bearer {TOKEN}"}
    redact_headers(headers)
    assert headers["Authorization"] == f"Bearer {TOKEN}"


def test_format_dry_run_never_prints_the_token() -> None:
    text = format_dry_run(prepared(filter_expr="country eq 'US'"))
    assert TOKEN not in text
    assert "Bearer <redacted>" in text
    assert "GET https://api.vercel.com/v1/query/web-analytics/visits/aggregate" in text
    assert "Nothing was sent" in text
    assert "projectId" in text and "requestPath" in text


def test_format_dry_run_shows_a_redacted_authorization_even_without_a_token() -> None:
    text = format_dry_run(prepared(token=None))
    assert "Bearer <redacted>" in text


def test_format_dry_run_prints_the_whole_json_body_of_a_post_operation() -> None:
    body = {"metric": "vercel.speed_insights.lcp_ms", "aggregation": "p75"}
    text = format_dry_run(
        PreparedRequest(
            operation="observability_query",
            url="https://api.vercel.com/v2/observability/query",
            params=[],
            headers={"Authorization": f"Bearer {TOKEN}"},
            json_body=body,
        )
    )
    assert "POST https://api.vercel.com/v2/observability/query" in text
    assert "JSON body:" in text
    assert "vercel.speed_insights.lcp_ms" in text
    assert '"aggregation": "p75"' in text
    assert TOKEN not in text


def test_a_get_dry_run_prints_no_json_body_section() -> None:
    assert "JSON body:" not in format_dry_run(prepared())


@pytest.mark.parametrize(
    "payload", [COUNTRY_PAYLOAD, VISITS_COUNT_PAYLOAD, DAILY_PAYLOAD]
)
def test_no_formatter_output_can_contain_the_token(payload: dict[str, Any]) -> None:
    group_by = [] if isinstance(payload["data"], dict) else ["country"]
    result = normalize(payload, "visits", group_by)
    for text in (
        format_table(result, time_range=(utc(2026, 8, 7), utc(2026, 8, 14))),
        format_json(result, payload),
        format_csv(result),
    ):
        assert TOKEN not in text


def test_no_exception_string_can_contain_the_token() -> None:
    session = FakeSession(
        FakeResponse(401, error_payload("forbidden", "Not authorized"))
    )
    with pytest.raises(ApiError) as excinfo:
        execute(prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0)
    assert TOKEN not in str(excinfo.value)
    assert TOKEN not in repr(excinfo.value)

    network = FakeSession(requests.Timeout("timed out"))
    with pytest.raises(ApiError) as excinfo:
        execute(prepared(), network, sleep=Recorder(), jitter=no_jitter, max_retries=0)
    assert TOKEN not in str(excinfo.value)


def test_dry_run_without_a_token_exits_zero_and_never_touches_a_session(
    cli: Cli,
) -> None:
    session = ForbiddenSession()
    code, out, err = cli.run(
        ["top-pages", "--dry-run"],
        env={"VERCEL_PROJECT_ID": PROJECT},
        session=session,
    )
    assert code == 0
    assert err == ""
    assert cli.created == [], "a dry run must not construct a session at all"
    assert session.calls == []
    assert "Nothing was sent" in out
    assert "Bearer <redacted>" in out


#: One verbose run per surface, with the payload its endpoint answers with. All
#: three are here because this is the demonstration that the token stays in the
#: Authorization header wherever this tool prints a request, and a surface left
#: out of it is a surface where that is only a promise.
VERBOSE_RUNS: list[tuple[str, dict[str, Any]]] = [
    ("top-pages", TOP_PAGES_PAYLOAD),
    ("slowest-pages", SPEED_ROUTE_PAYLOAD),
    ("logs", LOGS_PAGE),
]


@pytest.mark.parametrize(
    ("preset", "payload"), VERBOSE_RUNS, ids=[preset for preset, _ in VERBOSE_RUNS]
)
def test_a_verbose_run_prints_redacted_headers_only(
    cli: Cli, preset: str, payload: dict[str, Any]
) -> None:
    session = FakeSession(FakeResponse(200, payload))
    code, out, err = cli.run([preset, "--verbose"], env=dict(BASE_ENV), session=session)
    assert code == 0, err
    # Speed Insights posts its query; the other two get.
    assert "verbose: GET" in err or "verbose: POST" in err
    assert "Bearer <redacted>" in err
    assert TOKEN not in err
    assert TOKEN not in out


BAD_TOKENS: list[tuple[str, str]] = [
    ("line-feed", SECRET + "\nX-Evil: 1"),
    ("carriage-return", SECRET + "\r"),
    ("crlf-injection", SECRET + "\r\nX-Evil: 1"),
    ("null-byte", "\x00" + SECRET),
    ("delete", SECRET + "\x7f"),
    ("tab", SECRET + "\t"),
    ("non-ascii", "café" + SECRET),
    ("leading-space", " " + SECRET),
    ("trailing-space", SECRET + " "),
]


@pytest.mark.parametrize(
    "token", [case[1] for case in BAD_TOKENS], ids=[case[0] for case in BAD_TOKENS]
)
def test_an_unusable_token_is_rejected_before_any_request_and_is_never_printed(
    cli: Cli, token: str
) -> None:
    # session stays None, so constructing one would fail the test outright.
    code, out, err = cli.run(
        ["top-pages", "--token", token], env={"VERCEL_PROJECT_ID": PROJECT}
    )
    assert code == 2
    assert out == ""
    assert cli.created == []
    assert "Traceback" not in err
    assert "access token" in err
    assert "not shown" in err
    assert SECRET not in err
    assert token not in err
    assert "X-Evil" not in err


def test_a_header_injecting_token_from_the_environment_is_rejected_too(
    cli: Cli,
) -> None:
    env = {"VERCEL_TOKEN": f"{SECRET}\nX-Evil: 1", "VERCEL_PROJECT_ID": PROJECT}
    code, out, err = cli.run(["top-pages"], env=env)
    assert code == 2
    assert out == ""
    assert cli.created == []
    assert SECRET not in err
    assert "X-Evil" not in err


def test_surrounding_whitespace_on_an_environment_token_is_trimmed_not_sent(
    cli: Cli,
) -> None:
    # The env reader trims, so a copy and paste with a trailing newline still
    # works; what matters is that the trimmed value is what reaches the header.
    session = FakeSession(FakeResponse(200, TOP_PAGES_PAYLOAD))
    env = {"VERCEL_TOKEN": f"  {TOKEN}\n", "VERCEL_PROJECT_ID": PROJECT}
    code, _, _ = cli.run(["top-pages"], env=env, session=session)
    assert code == 0
    assert session.calls[0]["headers"]["Authorization"] == f"Bearer {TOKEN}"


def test_validate_token_reports_the_position_and_class_but_not_the_value() -> None:
    with pytest.raises(ConfigError) as excinfo:
        validate_token(SECRET + "\n")
    message = str(excinfo.value)
    assert "line feed" in message
    assert f"position {len(SECRET) + 1}" in message
    assert str(len(SECRET) + 1) in message
    assert SECRET not in message


def test_a_usable_token_passes_validation_unchanged() -> None:
    assert validate_token(TOKEN) == TOKEN


def test_an_empty_token_is_rejected_with_the_docs_pointer() -> None:
    with pytest.raises(ConfigError) as excinfo:
        validate_token("")
    assert "VERCEL_TOKEN" in str(excinfo.value)


def test_the_repr_of_a_prepared_request_hides_the_token() -> None:
    request = prepared()
    for text in (repr(request), f"{request!r}", repr([request]), str([request])):
        assert TOKEN not in text
        assert "Bearer <redacted>" in text
    assert "visits/aggregate" in repr(request)


def test_scrub_credentials_removes_both_the_bearer_and_the_bare_token() -> None:
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}
    leaked = f"InvalidHeader: Bearer {TOKEN} and also {TOKEN} on its own"
    scrubbed = scrub_credentials(leaked, headers)
    assert TOKEN not in scrubbed
    assert "<redacted>" in scrubbed


def test_an_exception_message_quoting_the_header_is_scrubbed() -> None:
    session = FakeSession(requests.ConnectionError(f"failed sending Bearer {TOKEN}"))
    with pytest.raises(ApiError) as excinfo:
        execute(prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0)
    assert TOKEN not in str(excinfo.value)


def test_an_error_body_echoing_the_token_is_scrubbed() -> None:
    body = error_payload("bad_request", f"the header Bearer {TOKEN} was rejected")
    session = FakeSession(FakeResponse(400, body))
    with pytest.raises(ApiError) as excinfo:
        execute(prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0)
    assert TOKEN not in str(excinfo.value)


def test_the_user_agent_carries_no_credential() -> None:
    assert TOKEN not in vi_http.USER_AGENT
    assert vi_http.USER_AGENT.startswith("vercel-insights-skill/")


def test_a_logs_request_carries_no_credential_in_its_url_or_params() -> None:
    request = logs_request(token=TOKEN)
    assert TOKEN not in request.url
    assert all(TOKEN not in value for _name, value in request.params)
    assert request.headers["Authorization"] == f"Bearer {TOKEN}"


def test_the_repr_of_a_logs_request_hides_the_token() -> None:
    text = repr(logs_request(token=TOKEN))
    assert TOKEN not in text
    assert "Bearer <redacted>" in text
    assert "request-logs" in text


def test_a_logs_dry_run_prints_no_credential() -> None:
    text = format_dry_run(logs_request(token=TOKEN))
    assert TOKEN not in text
    assert "Bearer <redacted>" in text
    assert "GET https://vercel.com/api/logs/request-logs" in text
    assert "Nothing was sent" in text


def logs_page_echoing_the_token() -> dict[str, Any]:
    """One row quoting the token in both places a response can put it.

    Vercel receives this token on every call, so a response carrying it back is
    not hypothetical, and request log rows are the only output this tool prints
    that some other program wrote: a log message is free text, and a request path
    is whatever a caller sent. Neither goes anywhere near the error paths that
    the rest of section 3 covers, so they need their own tests.

    The credential opens the message rather than closing it, so that an
    unscrubbed run shows part of it even in the table, whose message column
    truncates. A prefix of a credential is still a disclosure, which is why
    :data:`LEAKED_TOKEN_PREFIX` is asserted against as well as the whole value.
    """
    return {
        "rows": [
            logs_row(
                requestId="leak-1",
                statusCode=500,
                requestPath=f"/api/callback?key={TOKEN}",
                logs=[
                    {
                        "level": "error",
                        "message": f"Bearer {TOKEN} was rejected by upstream",
                        "messageTruncated": False,
                    }
                ],
            )
        ],
        "hasMoreRows": False,
    }


#: Enough of the token to be worth protecting on its own. A truncated column
#: cannot print the whole value, so only a prefix check can tell a scrubbed
#: table from one that merely ran out of room.
LEAKED_TOKEN_PREFIX = TOKEN[:16]


@pytest.mark.parametrize(
    "argv",
    [
        ["errors"],
        ["errors", "--expand"],
        ["errors", "--json"],
        ["errors", "--csv"],
        ["error-summary"],
    ],
    ids=["table", "expand", "json", "csv", "summary"],
)
def test_a_response_echoing_the_token_never_reaches_any_logs_output(
    cli: Cli, argv: list[str]
) -> None:
    # The tool holds exactly one secret and must never be the thing that
    # discloses it, whatever a response carries. Every output format is covered
    # because each renders the row differently: the table truncates a message,
    # --expand prints it whole, --csv writes its own columns, --json carries the
    # row verbatim, and error-summary groups by the message text.
    session = FakeSession(
        FakeResponse(200, logs_page_echoing_the_token()),
        FakeResponse(200, {"rows": [], "hasMoreRows": False}),
    )
    code, out, err = cli.run(argv, env=dict(BASE_ENV), session=session)
    assert code == 0, err
    for text in (out, err):
        assert TOKEN not in text
        assert LEAKED_TOKEN_PREFIX not in text


def test_the_token_is_rewritten_in_a_logs_row_rather_than_dropped(cli: Cli) -> None:
    # --json is where this has to be checked: every other format renders chosen
    # fields, while "raw" is the whole row as it arrived, so it is the copy that
    # would leak if the scrub were applied at rendering time instead of at
    # normalization. The placeholder proves the string was rewritten and the
    # surrounding text kept, rather than the field being blanked.
    session = FakeSession(
        FakeResponse(200, logs_page_echoing_the_token()),
        FakeResponse(200, {"rows": [], "hasMoreRows": False}),
    )
    code, out, err = cli.run(["errors", "--json"], env=dict(BASE_ENV), session=session)
    assert code == 0, err
    entry = json.loads(out)["entries"][0]
    # "Bearer <token>" goes as one unit, because the whole header value is a
    # credential in its own right and is replaced ahead of the bare token.
    assert entry["message"] == "<redacted> was rejected by upstream"
    assert entry["path"] == "/api/callback?key=<redacted>"
    assert entry["raw"]["logs"][0]["message"] == "<redacted> was rejected by upstream"
    assert entry["raw"]["requestPath"] == "/api/callback?key=<redacted>"


# ---------------------------------------------------------------------------
# 4. OData injection
# ---------------------------------------------------------------------------

ODATA_INJECTION_KEYS: list[str] = [
    "x' or 1 eq '1",
    "plan' or requestPath eq '/admin",
    "'a' or 1 eq '1'",
    "'unbalanced",
    "a'b",
    "''",
    "'",
]


@pytest.mark.parametrize("key", ODATA_INJECTION_KEYS)
def test_a_crafted_flag_key_cannot_inject_odata_into_the_filter(
    cli: Cli, key: str
) -> None:
    code, out, err = cli.run(
        ["top-pages", "--flag", f"{key}=true", "--dry-run"], env=dict(DRY_RUN_ENV)
    )
    assert code == 2, out
    assert out == ""
    assert "Traceback" not in err


@pytest.mark.parametrize("key", ODATA_INJECTION_KEYS)
def test_a_crafted_grouping_key_cannot_inject_odata_into_by(cli: Cli, key: str) -> None:
    code, out, err = cli.run(
        ["events", "--group-by", f"eventData/{key}", "--dry-run"],
        env=dict(DRY_RUN_ENV),
    )
    assert code == 2, out
    assert out == ""
    assert "Traceback" not in err


@pytest.mark.parametrize("key", ODATA_INJECTION_KEYS)
def test_a_crafted_event_property_cannot_inject_odata_into_by(
    cli: Cli, key: str
) -> None:
    code, out, err = cli.run(
        ["events", "--event-property", key, "--dry-run"], env=dict(DRY_RUN_ENV)
    )
    assert code == 2, out
    assert out == ""
    assert "Traceback" not in err


def test_a_quote_in_a_filter_value_is_doubled_rather_than_escaping_the_clause(
    cli: Cli,
) -> None:
    code, out, err = cli.run(
        ["countries", "--country", "US' or 1 eq '1", "--dry-run"],
        env=dict(DRY_RUN_ENV),
    )
    assert code == 0, err
    assert dry_run_values(out, "filter") == ["country eq 'US'' or 1 eq ''1'"]


# ---------------------------------------------------------------------------
# 5. The one POST operation
# ---------------------------------------------------------------------------
#
# The project's claim is "read only against a three endpoint allowlist", not
# "GET only": an observability query has no GET equivalent, so the query
# travels in a request body. That makes the body a second place a credential
# could leak into, and the tests below are what rule it out.


def test_observability_query_is_the_only_operation_that_posts() -> None:
    posting = [
        operation for operation, (method, _url) in OPERATIONS.items() if method == "POST"
    ]
    assert posting == ["observability_query"]
    assert OPERATIONS["observability_query"][1] == (
        "https://api.vercel.com/v2/observability/query"
    )


def test_the_read_endpoints_that_stay_gets_are_the_documented_ones() -> None:
    getting = sorted(
        operation for operation, (method, _url) in OPERATIONS.items() if method == "GET"
    )
    assert getting == [
        "observability_schema",
        "project",
        "projects",
        "request_logs",
        "web_analytics",
    ]


def test_a_speed_request_body_carries_the_query_and_never_the_token() -> None:
    request = speed_request(token=TOKEN, team="team_abc", team_slug=None)
    assert request.method == "POST"
    assert request.json_body is not None
    assert request.json_body["metric"] == "vercel.speed_insights.lcp_ms"
    assert TOKEN not in json.dumps(request.json_body)
    assert TOKEN not in json.dumps(request.params)
    assert TOKEN not in request.url
    assert request.headers["Authorization"] == f"Bearer {TOKEN}"


def test_the_repr_of_a_speed_request_shows_the_body_and_hides_the_token() -> None:
    text = repr(speed_request(token=TOKEN))
    assert TOKEN not in text
    assert "Bearer <redacted>" in text
    assert "vercel.speed_insights.lcp_ms" in text


def test_a_speed_dry_run_prints_the_whole_body_and_no_credential(cli: Cli) -> None:
    session = ForbiddenSession()
    code, out, err = cli.run(
        ["vitals-by-country", "--dry-run"],
        env={"VERCEL_PROJECT_ID": PROJECT, "VERCEL_TOKEN": TOKEN},
        session=session,
    )
    assert code == 0, err
    assert cli.created == [], "a dry run must not construct a session at all"
    assert session.calls == []
    assert "POST https://api.vercel.com/v2/observability/query" in out
    assert "JSON body:" in out
    assert '"metric": "vercel.speed_insights.lcp_ms"' in out
    assert "Bearer <redacted>" in out
    assert TOKEN not in out
    assert "Nothing was sent" in out


def test_a_speed_dry_run_works_with_no_token_in_the_environment(cli: Cli) -> None:
    session = ForbiddenSession()
    code, out, err = cli.run(
        ["vitals", "--dry-run"], env={"VERCEL_PROJECT_ID": PROJECT}, session=session
    )
    assert code == 0, err
    assert err == ""
    assert cli.created == []
    assert session.calls == []
    assert out.count("Bearer <redacted>") == 5


def test_a_speed_error_response_echoing_the_token_is_scrubbed(cli: Cli) -> None:
    body = error_payload("bad_request", f"the header Bearer {TOKEN} was rejected")
    session = FakeSession(FakeResponse(400, body))
    code, out, err = cli.run(
        ["slowest-pages", "--max-retries", "0"], env=dict(BASE_ENV), session=session
    )
    assert code == 1
    assert out == ""
    assert TOKEN not in err
    assert "<redacted>" in err


def test_a_speed_network_failure_message_carries_no_credential() -> None:
    session = FakeSession(requests.ConnectionError(f"failed sending Bearer {TOKEN}"))
    with pytest.raises(ApiError) as excinfo:
        execute(
            speed_request(token=TOKEN),
            session,
            sleep=Recorder(),
            jitter=no_jitter,
            max_retries=0,
        )
    assert TOKEN not in str(excinfo.value)
    assert TOKEN not in repr(excinfo.value)


def test_the_body_is_handed_to_post_as_json_rather_than_pasted_into_the_url() -> None:
    session = FakeSession(FakeResponse(200, {"data": {"value": 2412}}))
    execute(
        speed_request(token=TOKEN), session, sleep=Recorder(), jitter=no_jitter
    )
    call = session.calls[0]
    assert call["method"] == "POST"
    assert call["url"] == "https://api.vercel.com/v2/observability/query"
    assert call["json"]["metric"] == "vercel.speed_insights.lcp_ms"
    assert call["params"] == []
    assert TOKEN not in call["url"]


# ---------------------------------------------------------------------------
# 6. The allowlist binds every hop, not only the first
# ---------------------------------------------------------------------------
#
# The token travels in the Authorization header. A followed redirect would hand
# it to whatever host the Location names, which would make the three entry
# allowlist a statement about first hops only.


def test_a_redirect_never_carries_the_authorization_header_to_another_host(
    cli: Cli,
) -> None:
    session = FakeSession(
        FakeResponse(302, {}, {"Location": "https://evil.example/steal"})
    )
    code, out, err = cli.run(
        ["top-pages", "--max-retries", "3"], env=dict(BASE_ENV), session=session
    )
    assert code == 1
    assert out == ""
    # Exactly one request was made, to the one allowlisted URL, and the client
    # asked the session not to follow anything.
    assert len(session.calls) == 1
    call = session.calls[0]
    assert call["url"] == (
        "https://api.vercel.com/v1/query/web-analytics/visits/aggregate"
    )
    assert call["allow_redirects"] is False
    assert call["headers"]["Authorization"] == f"Bearer {TOKEN}"
    # The redirect is reported by name so the user can see where it pointed.
    assert "unexpected_redirect" in err
    assert "https://evil.example/steal" in err
    assert TOKEN not in err


def test_a_redirect_on_the_post_operation_is_refused_through_the_cli_too(
    cli: Cli,
) -> None:
    session = FakeSession(
        FakeResponse(308, {}, {"Location": "https://evil.example/steal"})
    )
    code, out, err = cli.run(
        ["slowest-pages", "--max-retries", "3"], env=dict(BASE_ENV), session=session
    )
    assert code == 1
    assert out == ""
    assert len(session.calls) == 1
    assert session.calls[0]["url"] == "https://api.vercel.com/v2/observability/query"
    assert session.calls[0]["allow_redirects"] is False
    assert "unexpected_redirect" in err
    assert TOKEN not in err


def test_a_redirect_pointing_at_a_url_carrying_the_token_is_scrubbed(
    cli: Cli,
) -> None:
    session = FakeSession(
        FakeResponse(302, {}, {"Location": f"https://evil.example/?token={TOKEN}"})
    )
    code, _out, err = cli.run(
        ["top-pages", "--max-retries", "0"], env=dict(BASE_ENV), session=session
    )
    assert code == 1
    assert TOKEN not in err
    assert "<redacted>" in err
    assert "Traceback" not in err


def test_the_source_pins_allow_redirects_false_at_both_call_sites() -> None:
    # A structural check to go with the behavioural ones: the flag is passed at
    # both call sites, so it holds for a real requests.Session as well.
    dispatcher = next(path for path in package_sources() if path.name == "http.py")
    source = dispatcher.read_text(encoding="utf-8")
    assert source.count("allow_redirects=False") == 2
    assert "allow_redirects=True" not in source


# ---------------------------------------------------------------------------
# 7. Response derived labels reaching a terminal
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "argv",
    [["campaigns"], ["campaigns", "--csv"], ["campaigns", "--json"]],
    ids=["table", "csv", "json"],
)
def test_no_control_character_from_a_response_ever_reaches_stdout(
    cli: Cli, argv: list[str]
) -> None:
    # The label here is a UTM campaign, which is whatever a visitor typed into
    # a query string: real untrusted input, arriving on a real preset.
    session = FakeSession(FakeResponse(200, CONTROL_CHARACTER_CAMPAIGN_PAYLOAD))
    code, out, err = cli.run(argv, env=dict(BASE_ENV), session=session)
    assert code == 0, err
    for character in ("\x1b", "\r", "\x00", "\x07", "\x7f", "\x9b"):
        assert character not in out, f"raw {character!r} reached stdout"
    # Escaped, not dropped: the value still reads as what came back.
    if "--json" in argv:
        keys = [row["key"] for row in json.loads(out)["rows"]]
        assert ESCAPED_ANSI_CAMPAIGN in keys
    else:
        assert ESCAPED_ANSI_CAMPAIGN in out


def test_a_control_character_label_cannot_forge_a_totals_row_either(cli: Cli) -> None:
    # A carriage return inside a label would let the response overwrite the
    # line already printed, which is how a table is made to lie about its total.
    session = FakeSession(FakeResponse(200, CONTROL_CHARACTER_CAMPAIGN_PAYLOAD))
    code, out, err = cli.run(["campaigns"], env=dict(BASE_ENV), session=session)
    assert code == 0, err
    lines = [line for line in out.splitlines() if line.strip()]
    assert sum(1 for line in lines if line.startswith("TOTAL")) == 1
    assert "\r" not in out


def test_a_speed_formatter_can_never_print_the_token() -> None:
    result = normalize_speed(
        {"version": 1, "data": [{"route": "/", "value": 2412, "dataPoints": 30}]},
        metric=validate_metric("lcp"),
        aggregation="p75",
        group_by=["route"],
    )
    for text in (
        format_table(result, time_range=(utc(2026, 8, 7), utc(2026, 8, 14))),
        format_json(result, {"data": []}),
        format_csv(result),
    ):
        assert TOKEN not in text
