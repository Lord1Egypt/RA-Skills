"""Tests for vercel_insights/http.py: retries, backoff and error paths."""

from __future__ import annotations

import json

import pytest
import requests
from helpers import (
    COUNTRY_PAYLOAD,
    SPEED_QUERY_URL,
    TOKEN,
    FakeResponse,
    FakeSession,
    Recorder,
    error_payload,
    no_jitter,
    prepared,
    speed_request,
    utc,
)

from vercel_insights import ApiError, ConfigError, RateLimitError
from vercel_insights import http as vi_http
from vercel_insights.http import PreparedRequest

# ---------------------------------------------------------------------------
# Retry and backoff
# ---------------------------------------------------------------------------


def test_retry_delay_prefers_a_numeric_retry_after_header() -> None:
    response = FakeResponse(429, {}, {"Retry-After": "2"})
    assert vi_http.retry_delay(0, response, None, 1000.0) == 2.0


def test_retry_delay_understands_an_http_date_retry_after() -> None:
    when = utc(2015, 10, 21, 7, 28)
    header = {"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"}
    delay = vi_http.retry_delay(
        0, FakeResponse(429, {}, header), None, when.timestamp() - 5
    )
    assert delay == pytest.approx(5.0)


def test_retry_delay_falls_back_to_reset_ms_then_reset_then_backoff() -> None:
    body_ms = error_payload("rate_limited", "slow down", limit={"resetMs": 1003500})
    assert vi_http.retry_delay(0, FakeResponse(429, body_ms), body_ms, 1000.0) == 3.5

    body_s = error_payload("rate_limited", "slow down", limit={"reset": 1004})
    assert vi_http.retry_delay(0, FakeResponse(429, body_s), body_s, 1000.0) == 4.0

    assert vi_http.retry_delay(0, FakeResponse(500, {}), None, 1000.0) == 0.5


@pytest.mark.parametrize(
    ("attempt", "expected"), [(0, 0.5), (1, 1.0), (2, 2.0), (3, 4.0), (10, 60.0)]
)
def test_retry_delay_backoff_doubles_and_is_capped(
    attempt: int, expected: float
) -> None:
    assert vi_http.retry_delay(attempt, None, None, 1000.0) == expected


def test_a_rate_limited_response_honors_retry_after_then_succeeds() -> None:
    sleeps = Recorder()
    session = FakeSession(
        FakeResponse(
            429,
            error_payload("rate_limited", "The rate limit of 6 exceeded"),
            {"Retry-After": "2"},
        ),
        FakeResponse(200, COUNTRY_PAYLOAD),
    )
    payload = vi_http.execute(
        prepared(),
        session,
        sleep=sleeps,
        jitter=no_jitter,
        max_retries=3,
        now=lambda: 1000.0,
    )
    assert payload == COUNTRY_PAYLOAD
    assert sleeps.delays == [2.0]
    assert len(session.calls) == 2


def test_a_rate_limited_response_honors_reset_ms_when_there_is_no_header() -> None:
    sleeps = Recorder()
    body = error_payload(
        "rate_limited",
        "The rate limit of 6 exceeded",
        limit={"remaining": 0, "reset": 1004, "resetMs": 1003500, "total": 6},
    )
    session = FakeSession(FakeResponse(429, body), FakeResponse(200, COUNTRY_PAYLOAD))
    payload = vi_http.execute(
        prepared(),
        session,
        sleep=sleeps,
        jitter=no_jitter,
        max_retries=3,
        now=lambda: 1000.0,
    )
    assert payload == COUNTRY_PAYLOAD
    assert sleeps.delays == [3.5]


def test_a_server_error_is_retried_with_exponential_backoff() -> None:
    sleeps = Recorder()
    session = FakeSession(
        FakeResponse(500, error_payload("internal_server_error", "boom")),
        FakeResponse(200, COUNTRY_PAYLOAD),
    )
    payload = vi_http.execute(
        prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=3
    )
    assert payload == COUNTRY_PAYLOAD
    assert sleeps.delays == [0.5]


def test_a_408_request_timeout_is_retried() -> None:
    # 408 is on the retryable list because the observability query API
    # documents it: a query can time out server side and is worth another go.
    sleeps = Recorder()
    session = FakeSession(
        FakeResponse(408, error_payload("request_timeout", "the query timed out")),
        FakeResponse(200, COUNTRY_PAYLOAD),
    )
    payload = vi_http.execute(
        prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=3
    )
    assert payload == COUNTRY_PAYLOAD
    assert sleeps.delays == [0.5]
    assert len(session.calls) == 2


def test_408_is_on_the_retryable_status_list() -> None:
    assert 408 in vi_http.RETRYABLE_STATUSES


# 507 Insufficient Storage, 508 Loop Detected, 599 and friends are not on the
# named list, and none of them ever will be: the rule is "any other 5xx is
# retried too", and these are what hold that clause in place.
UNLISTED_SERVER_ERRORS = [501, 505, 507, 508, 599]


@pytest.mark.parametrize("status", UNLISTED_SERVER_ERRORS)
def test_a_five_hundred_status_not_on_the_named_list_is_retried_anyway(
    status: int,
) -> None:
    assert status not in vi_http.RETRYABLE_STATUSES, (
        f"{status} is now named explicitly, so this test no longer covers the "
        "'any other 5xx' rule; pick another unlisted status"
    )
    sleeps = Recorder()
    session = FakeSession(
        FakeResponse(status, error_payload("server_error", "something gave way")),
        FakeResponse(200, COUNTRY_PAYLOAD),
    )
    payload = vi_http.execute(
        prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=3
    )
    assert payload == COUNTRY_PAYLOAD
    assert sleeps.delays == [0.5]
    assert len(session.calls) == 2


@pytest.mark.parametrize("status", UNLISTED_SERVER_ERRORS)
def test_an_unlisted_five_hundred_that_never_clears_reports_every_attempt(
    status: int,
) -> None:
    sleeps = Recorder()
    session = FakeSession(
        *[
            FakeResponse(status, error_payload("server_error", "still down"))
            for _ in range(3)
        ]
    )
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=2
        )
    assert "gave up after 3 attempts" in str(excinfo.value)
    assert sleeps.delays == [0.5, 1.0]


@pytest.mark.parametrize("status", [402, 404, 409, 418, 451])
def test_a_four_hundred_status_off_the_list_is_still_never_retried(
    status: int,
) -> None:
    sleeps = Recorder()
    session = FakeSession(
        FakeResponse(status, error_payload("nope", "no")),
        FakeResponse(200, COUNTRY_PAYLOAD),
    )
    with pytest.raises(ApiError):
        vi_http.execute(
            prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=3
        )
    assert sleeps.delays == []
    assert len(session.calls) == 1


# ---------------------------------------------------------------------------
# Rate limits, recognised by status and by error code
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("status", [400, 403, 500, 503])
def test_the_documented_rate_limited_code_is_a_rate_limit_at_any_status(
    status: int,
) -> None:
    # docs/api-notes.md documents the code, not only the status: "Rate limiting
    # returns code rate_limited and carries a limit object". A body that says so
    # is a rate limit whatever status carried it, so the reset time is read and
    # the CLI prints its rate limit hint rather than a bare error.
    assert status != 429
    limit = {"remaining": 0, "reset": 1571432075, "resetMs": 1571432075563, "total": 6}
    body = error_payload(
        "rate_limited", "The rate limit of 6 exceeded. Try again in 7 days", limit=limit
    )
    session = FakeSession(FakeResponse(status, body))
    with pytest.raises(RateLimitError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    error = excinfo.value
    assert error.status == status
    assert error.code == "rate_limited"
    assert error.limit == limit
    assert "Try again in 7 days" in str(error)


def test_a_429_is_a_rate_limit_even_when_the_body_names_another_code() -> None:
    # The other half of the same rule: the status alone is enough.
    session = FakeSession(
        FakeResponse(429, error_payload("too_many_requests", "slow down"))
    )
    with pytest.raises(RateLimitError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    assert excinfo.value.status == 429
    assert excinfo.value.code == "too_many_requests"


def test_a_429_carrying_no_body_at_all_is_still_a_rate_limit() -> None:
    session = FakeSession(FakeResponse(429, text=""))
    with pytest.raises(RateLimitError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    assert excinfo.value.code == "rate_limited"


def test_an_ordinary_error_is_not_dressed_up_as_a_rate_limit() -> None:
    session = FakeSession(FakeResponse(403, error_payload("forbidden", "no")))
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    assert not isinstance(excinfo.value, RateLimitError)


# ---------------------------------------------------------------------------
# Non-standard JSON literals
# ---------------------------------------------------------------------------
#
# json.loads reads NaN, Infinity and -Infinity as floats by default even though
# none of the three is JSON. A nan that got that far would compare false against
# every target, format as "nan", and read as a measurement.

NON_STANDARD_LITERALS = ["NaN", "Infinity", "-Infinity"]


@pytest.mark.parametrize("literal", NON_STANDARD_LITERALS)
def test_the_json_module_really_would_have_accepted_the_literal(literal: str) -> None:
    # The premise of the guard below: without it, this is what would be parsed.
    accepted = json.loads(f'{{"data": {{"pageviews": {literal}}}}}')
    assert isinstance(accepted["data"]["pageviews"], float)


@pytest.mark.parametrize("literal", NON_STANDARD_LITERALS)
def test_a_success_body_carrying_a_non_standard_literal_is_refused(
    literal: str,
) -> None:
    body = f'{{"version": 1, "data": {{"pageviews": {literal}, "visitors": 3}}}}'
    session = FakeSession(FakeResponse(200, text=body))
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    error = excinfo.value
    assert error.code == "invalid_response"
    assert error.status == 200
    assert "NaN" in str(error) and "Infinity" in str(error)
    # The refusal names the class of literal, never the field it sat on.
    assert "pageviews" not in str(error)
    assert not isinstance(error, json.JSONDecodeError)


@pytest.mark.parametrize("literal", NON_STANDARD_LITERALS)
def test_a_non_standard_literal_anywhere_in_the_body_is_refused(
    literal: str,
) -> None:
    # Nested inside an array, and as the whole document, not only as one field.
    for body in (
        f'{{"version": 1, "data": [{{"country": "US", "pageviews": {literal}}}]}}',
        f'{{"data": {literal}}}',
        literal,
    ):
        session = FakeSession(FakeResponse(200, text=body))
        with pytest.raises(ApiError) as excinfo:
            vi_http.execute(
                prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
            )
        assert excinfo.value.code == "invalid_response"


def test_an_ordinary_float_body_is_still_parsed_normally() -> None:
    session = FakeSession(FakeResponse(200, text='{"version": 1, "data": {"cls": 0.0}}'))
    payload = vi_http.execute(
        prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
    )
    assert payload == {"version": 1, "data": {"cls": 0.0}}


# ---------------------------------------------------------------------------
# Redirects: reported, never followed
# ---------------------------------------------------------------------------
#
# The token travels in the Authorization header, so following a redirect would
# hand it to whatever host the Location names. Not following one is what makes
# the operation allowlist bind every hop rather than only the first.

REDIRECT_STATUSES = [300, 301, 302, 303, 305, 307, 308, 399]


@pytest.mark.parametrize("status", REDIRECT_STATUSES)
def test_a_redirect_is_reported_rather_than_followed(status: int) -> None:
    sleeps = Recorder()
    session = FakeSession(
        FakeResponse(status, {}, {"Location": "https://evil.example/steal"}),
        FakeResponse(200, COUNTRY_PAYLOAD),
    )
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=3
        )
    error = excinfo.value
    assert error.status == status
    assert error.code == "unexpected_redirect"
    assert "https://evil.example/steal" in str(error)
    assert "does not follow" in str(error)
    # One attempt only: a redirect is neither retried nor chased.
    assert len(session.calls) == 1
    assert sleeps.delays == []


@pytest.mark.parametrize("status", REDIRECT_STATUSES)
def test_a_redirect_reaches_no_second_host(status: int) -> None:
    session = FakeSession(
        FakeResponse(status, {}, {"Location": "https://evil.example/steal"})
    )
    with pytest.raises(ApiError):
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    hosts = {call["url"] for call in session.calls}
    assert hosts == {
        "https://api.vercel.com/v1/query/web-analytics/visits/aggregate"
    }
    assert all("evil.example" not in call["url"] for call in session.calls)


def test_a_redirect_with_a_lowercase_location_header_is_named_too() -> None:
    session = FakeSession(
        FakeResponse(302, {}, {"location": "https://proxy.internal/vercel"})
    )
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    assert "https://proxy.internal/vercel" in str(excinfo.value)


def test_a_redirect_without_a_location_header_still_reports_cleanly() -> None:
    session = FakeSession(FakeResponse(302, {}))
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    assert excinfo.value.code == "unexpected_redirect"
    assert "no Location header" in str(excinfo.value)


def test_a_redirect_location_echoing_the_token_is_scrubbed() -> None:
    session = FakeSession(
        FakeResponse(302, {}, {"Location": f"https://evil.example/?t={TOKEN}"})
    )
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    assert TOKEN not in str(excinfo.value)
    assert "<redacted>" in str(excinfo.value)


def test_a_redirect_on_the_post_operation_is_refused_the_same_way() -> None:
    session = FakeSession(
        FakeResponse(307, {}, {"Location": "https://evil.example/steal"})
    )
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            speed_request(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    assert excinfo.value.code == "unexpected_redirect"
    assert len(session.calls) == 1
    assert session.calls[0]["url"] == SPEED_QUERY_URL


def test_neither_call_site_ever_asks_the_session_to_follow_a_redirect() -> None:
    # The guarantee is structural: allow_redirects=False is passed at both call
    # sites, so it holds for a real requests.Session too, not only for a 3xx a
    # test happens to queue up.
    get_session = FakeSession(FakeResponse(200, COUNTRY_PAYLOAD))
    vi_http.execute(prepared(), get_session, sleep=Recorder(), jitter=no_jitter)
    assert get_session.calls[0]["method"] == "GET"
    assert get_session.calls[0]["allow_redirects"] is False

    post_session = FakeSession(FakeResponse(200, {"data": {"value": 2412}}))
    vi_http.execute(speed_request(), post_session, sleep=Recorder(), jitter=no_jitter)
    assert post_session.calls[0]["method"] == "POST"
    assert post_session.calls[0]["allow_redirects"] is False


def test_every_attempt_of_a_retried_request_also_refuses_redirects() -> None:
    session = FakeSession(
        FakeResponse(500, error_payload("internal_server_error", "boom")),
        FakeResponse(200, COUNTRY_PAYLOAD),
    )
    vi_http.execute(
        prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=2
    )
    assert [call["allow_redirects"] for call in session.calls] == [False, False]


def test_injected_jitter_is_added_to_every_delay() -> None:
    sleeps = Recorder()
    session = FakeSession(
        FakeResponse(500, error_payload("internal_server_error", "boom")),
        FakeResponse(503, error_payload("service_unavailable", "boom")),
        FakeResponse(200, COUNTRY_PAYLOAD),
    )
    vi_http.execute(
        prepared(), session, sleep=sleeps, jitter=lambda: 0.25, max_retries=3
    )
    assert sleeps.delays == [0.75, 1.25]


def test_exhausting_max_retries_reports_the_attempt_count() -> None:
    sleeps = Recorder()
    session = FakeSession(
        *[
            FakeResponse(500, error_payload("internal_server_error", "boom"))
            for _ in range(3)
        ]
    )
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=2
        )
    assert "gave up after 3 attempts" in str(excinfo.value)
    assert "boom" in str(excinfo.value)
    assert sleeps.delays == [0.5, 1.0]
    assert len(session.calls) == 3


def test_exhausting_max_retries_on_a_rate_limit_raises_rate_limit_error() -> None:
    sleeps = Recorder()
    body = error_payload("rate_limited", "Try again in 7 days", limit={"total": 6})
    session = FakeSession(FakeResponse(429, body), FakeResponse(429, body))
    with pytest.raises(RateLimitError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=1
        )
    assert excinfo.value.limit == {"total": 6}
    assert "Try again in 7 days" in str(excinfo.value)
    assert sleeps.delays == [0.5]


def test_a_client_error_is_never_retried() -> None:
    sleeps = Recorder()
    session = FakeSession(
        FakeResponse(400, error_payload("bad_request", "Invalid value for by")),
        FakeResponse(200, COUNTRY_PAYLOAD),
    )
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=3
        )
    assert excinfo.value.status == 400
    assert sleeps.delays == []
    assert len(session.calls) == 1


def test_a_timeout_is_retried_and_then_succeeds() -> None:
    sleeps = Recorder()
    session = FakeSession(
        requests.Timeout("timed out"), FakeResponse(200, COUNTRY_PAYLOAD)
    )
    payload = vi_http.execute(
        prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=2
    )
    assert payload == COUNTRY_PAYLOAD
    assert sleeps.delays == [0.5]


def test_repeated_network_failures_surface_as_an_api_error_with_attempts() -> None:
    sleeps = Recorder()
    session = FakeSession(
        requests.ConnectionError("no route"), requests.Timeout("timed out")
    )
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=1
        )
    assert excinfo.value.status is None
    assert "could not reach" in str(excinfo.value)
    assert "gave up after 2 attempts" in str(excinfo.value)
    assert sleeps.delays == [0.5]


def test_max_retries_zero_makes_exactly_one_attempt() -> None:
    sleeps = Recorder()
    session = FakeSession(FakeResponse(503, error_payload("unavailable", "down")))
    with pytest.raises(ApiError):
        vi_http.execute(
            prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=0
        )
    assert sleeps.delays == []
    assert len(session.calls) == 1


def test_execute_sends_a_get_with_the_prepared_parameters_and_timeout() -> None:
    session = FakeSession(FakeResponse(200, COUNTRY_PAYLOAD))
    request = prepared()
    vi_http.execute(request, session, sleep=Recorder(), jitter=no_jitter, timeout=12.5)
    call = session.calls[0]
    assert call["method"] == "GET"
    assert call["url"] == request.url
    assert call["params"] == request.params
    assert call["headers"] == request.headers
    assert call["timeout"] == 12.5


def test_execute_sends_a_post_with_its_json_body_for_a_post_operation() -> None:
    # The dispatcher reads the verb out of OPERATIONS, so an operation the
    # table marks POST is issued as a POST and carries its body.
    body = {"metric": "vercel.speed_insights.lcp_ms", "scope": {"projectId": "prj"}}
    request = PreparedRequest(
        operation="observability_query",
        url="https://api.vercel.com/v2/observability/query",
        params=[],
        headers={"Accept": "application/json"},
        json_body=body,
    )
    session = FakeSession(FakeResponse(200, {"data": []}))
    vi_http.execute(request, session, sleep=Recorder(), jitter=no_jitter, timeout=9.0)
    call = session.calls[0]
    assert call["method"] == "POST"
    assert call["url"] == "https://api.vercel.com/v2/observability/query"
    assert call["json"] == body
    assert call["timeout"] == 9.0


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("status", "code", "message"),
    [
        (400, "bad_request", "An english description of the error that just occurred"),
        (401, "forbidden", "Not authorized"),
        (403, "forbidden", "You do not have permission to access this resource"),
        (410, "gone", "The resource is gone"),
    ],
)
def test_an_api_error_surfaces_vercels_message_verbatim(
    status: int, code: str, message: str
) -> None:
    session = FakeSession(FakeResponse(status, error_payload(code, message)))
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    error = excinfo.value
    assert error.status == status
    assert error.code == code
    assert error.message == message
    assert message in str(error)
    assert f"HTTP {status}" in str(error)


def test_a_non_json_success_body_becomes_a_clean_error() -> None:
    session = FakeSession(FakeResponse(200, text="<html>gateway</html>"))
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    assert "not a JSON object" in str(excinfo.value)
    assert not isinstance(excinfo.value, json.JSONDecodeError)


def test_a_non_json_error_body_falls_back_to_a_trimmed_snippet() -> None:
    session = FakeSession(FakeResponse(502, text="<html>\nbad gateway\n</html>"))
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    rendered = str(excinfo.value)
    assert "bad gateway" in rendered
    assert "\n" not in rendered


def test_an_error_body_without_a_message_still_renders() -> None:
    session = FakeSession(FakeResponse(400, {"error": {"code": "bad_request"}}))
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    assert "HTTP 400" in str(excinfo.value)
    assert "bad_request" in str(excinfo.value)


def test_an_unexpected_request_exception_is_not_retried() -> None:
    sleeps = Recorder()
    session = FakeSession(requests.TooManyRedirects("looping"))
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=sleeps, jitter=no_jitter, max_retries=3
        )
    assert excinfo.value.code == "request_failed"
    assert sleeps.delays == []


@pytest.mark.parametrize("body", ['"a string"', "42", "true", "null"], ids=str)
def test_a_json_body_that_is_neither_object_nor_array_is_a_clean_error(
    body: str,
) -> None:
    # An object or an array is accepted at this layer: query endpoints answer
    # with an object and the schema endpoint answers with a top level array.
    # Anything else is not a response this client has a use for.
    session = FakeSession(FakeResponse(200, text=body))
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    assert excinfo.value.code == "invalid_response"
    assert "not a JSON object or array" in str(excinfo.value)


def test_a_top_level_array_is_accepted_because_the_schema_endpoint_returns_one() -> None:
    session = FakeSession(FakeResponse(200, text='[{"id": "a"}]'))
    answer = vi_http.execute(
        prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
    )
    assert answer == [{"id": "a"}]


def test_an_empty_response_body_is_a_clean_error() -> None:
    session = FakeSession(FakeResponse(200, text=""))
    with pytest.raises(ApiError) as excinfo:
        vi_http.execute(
            prepared(), session, sleep=Recorder(), jitter=no_jitter, max_retries=0
        )
    assert "not a JSON object" in str(excinfo.value)


# ---------------------------------------------------------------------------
# --timeout validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value", [0.0, -1.0, float("inf"), float("-inf"), float("nan")]
)
def test_validate_timeout_rejects_every_unusable_value(value: float) -> None:
    with pytest.raises(ConfigError):
        vi_http.validate_timeout(value)


@pytest.mark.parametrize("value", [0.25, 1.0, 30.0, 600.0])
def test_validate_timeout_accepts_a_finite_positive_value(value: float) -> None:
    assert vi_http.validate_timeout(value) == value
