"""Shared fakes, payloads and helpers for the suite.

Nothing here touches the network. Every HTTP interaction goes through a fake
session object, and every retry test injects its own sleep and jitter callables
so the suite is instant and deterministic. A test that reaches the real network
or the real ``time.sleep`` is a bug in the test.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlsplit

import pytest

from vercel_insights import cli as vi_cli
from vercel_insights import http as vi_http
from vercel_insights.http import PreparedRequest
from vercel_insights.logs import build_request as build_logs_request
from vercel_insights.speedinsights import build_request as build_speed_request
from vercel_insights.speedinsights import validate_metric
from vercel_insights.webanalytics import build_request

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = REPO_ROOT / "vercel_insights"
TESTS_DIR = REPO_ROOT / "tests"

#: The Web Analytics endpoint prefix, written out rather than composed from
#: the package constants: a test that builds the URL the same way the code does
#: cannot notice the code building the wrong one.
WEB_ANALYTICS_BASE = "https://api.vercel.com/v1/query/web-analytics"

#: The observability query endpoint, likewise written out by hand from
#: docs/api-notes.md rather than read back from ``OPERATIONS``.
SPEED_QUERY_URL = "https://api.vercel.com/v2/observability/query"

#: The request-logs endpoint, written out by hand from docs/api-notes.md rather
#: than read back from OPERATIONS.
LOGS_URL = "https://vercel.com/api/logs/request-logs"

TOKEN = "vercel-token-that-must-never-be-printed"
PROJECT = "prj_demo"
#: A Speed Insights scope requires an ownerId. Supplying it here keeps the CLI
#: tests to the one request under test: without it a personal-account run spends
#: its first request resolving the owner from /v2/user, which every queued fake
#: response would then be off by one against.
OWNER = "own_demo"

BASE_ENV = {
    "VERCEL_TOKEN": TOKEN,
    "VERCEL_PROJECT_ID": PROJECT,
    "VERCEL_OWNER_ID": OWNER,
}
DRY_RUN_ENV = {"VERCEL_PROJECT_ID": PROJECT, "VERCEL_OWNER_ID": OWNER}

NOW = datetime(2026, 8, 14, 12, 30, 45, tzinfo=timezone.utc)


def package_sources() -> list[Path]:
    """Every Python file in the package, for the source level invariants."""
    return sorted(PACKAGE_DIR.glob("*.py"))


def package_source_text() -> str:
    """The whole package as one string, for the source level invariants."""
    return "\n".join(path.read_text(encoding="utf-8") for path in package_sources())


def utc(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
) -> datetime:
    """Build an aware UTC datetime, for readable expectations."""
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)


class FakeResponse:
    """The slice of a requests response that the module actually reads."""

    def __init__(
        self,
        status_code: int,
        body: Any = None,
        headers: dict[str, str] | None = None,
        *,
        text: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.headers = headers or {}
        if text is not None:
            self.text = text
        else:
            self.text = json.dumps(body if body is not None else {})


class FakeSession:
    """A session that returns queued responses and records every call.

    Queue entries may be ``FakeResponse`` objects or exception instances; an
    exception is raised instead of returned, which is how the network failure
    paths are exercised. ``get`` and ``post`` share one queue and one call log,
    and each entry records the verb, so a test can assert which one was used.
    """

    def __init__(self, *responses: FakeResponse | BaseException) -> None:
        self.queue: list[FakeResponse | BaseException] = list(responses)
        self.calls: list[dict[str, Any]] = []
        self.closed = False

    def _serve(self, call: dict[str, Any]) -> FakeResponse:
        self.calls.append(call)
        if not self.queue:
            raise AssertionError(f"unexpected extra request to {call['url']}")
        item = self.queue.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item

    def get(
        self,
        url: str,
        *,
        params: Any = None,
        headers: Any = None,
        timeout: Any = None,
        allow_redirects: Any = True,
    ) -> FakeResponse:
        return self._serve(
            {
                "method": "GET",
                "url": url,
                "params": params,
                "headers": headers,
                "timeout": timeout,
                "allow_redirects": allow_redirects,
            }
        )

    def post(
        self,
        url: str,
        *,
        params: Any = None,
        headers: Any = None,
        json: Any = None,
        timeout: Any = None,
        allow_redirects: Any = True,
    ) -> FakeResponse:
        return self._serve(
            {
                "method": "POST",
                "url": url,
                "params": params,
                "headers": headers,
                "json": json,
                "timeout": timeout,
                "allow_redirects": allow_redirects,
            }
        )

    def close(self) -> None:
        self.closed = True


class ForbiddenSession:
    """A session that fails the test if anything ever calls it."""

    def __init__(self) -> None:
        self.calls: list[Any] = []

    def get(self, *args: Any, **kwargs: Any) -> Any:
        self.calls.append((args, kwargs))
        raise AssertionError("this code path must not issue a request")

    def post(self, *args: Any, **kwargs: Any) -> Any:
        self.calls.append((args, kwargs))
        raise AssertionError("this code path must not issue a request")

    def close(self) -> None:
        raise AssertionError("this code path must not construct a session")


class Recorder:
    """Records the exact delays handed to ``sleep``."""

    def __init__(self) -> None:
        self.delays: list[float] = []

    def __call__(self, delay: float) -> None:
        self.delays.append(delay)


def no_jitter() -> float:
    return 0.0


def prepared(**overrides: Any) -> PreparedRequest:
    """A prepared request with sensible defaults, for the HTTP level tests."""
    kwargs: dict[str, Any] = {
        "dataset": "visits",
        "project": PROJECT,
        "since": utc(2026, 8, 7),
        "until": utc(2026, 8, 14),
        "group_by": ["requestPath"],
        "limit": 10,
        "token": TOKEN,
    }
    kwargs.update(overrides)
    return build_request(**kwargs)


def speed_request(**overrides: Any) -> PreparedRequest:
    """A prepared Speed Insights request, for the HTTP and security tests."""
    kwargs: dict[str, Any] = {
        "metric": validate_metric("lcp"),
        "project": PROJECT,
        "owner_id": OWNER,
        "since": utc(2026, 8, 7),
        "until": utc(2026, 8, 14),
        "token": TOKEN,
    }
    kwargs.update(overrides)
    return build_speed_request(**kwargs)


def logs_request(**overrides: Any) -> PreparedRequest:
    """A prepared request-logs request, for the HTTP and security tests."""
    kwargs: dict[str, Any] = {
        "project": PROJECT,
        "owner_id": OWNER,
        "since": utc(2026, 8, 17, 10, 6, 8),
        "until": utc(2026, 8, 17, 11, 6, 8),
        "token": TOKEN,
    }
    kwargs.update(overrides)
    return build_logs_request(**kwargs)


def dry_run_calls(out: str) -> list[tuple[str, list[tuple[str, str]]]]:
    """Parse a ``--dry-run`` dump into ``(endpoint, query parameter pairs)``.

    One entry per request, so the three request overview parses too, as do the
    two calls an errors preset makes. On Web Analytics the endpoint is the tail
    of the path after that surface's own prefix, for example
    ``visits/aggregate``; any other surface is named by its last path segment,
    so a request-logs call yields ``request-logs``.
    """
    calls: list[tuple[str, list[tuple[str, str]]]] = []
    lines = out.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("Encoded URL"):
            continue
        split = urlsplit(lines[index + 1].strip())
        marker = "/web-analytics/"
        if marker in split.path:
            endpoint = split.path.split(marker, 1)[1]
        else:
            endpoint = split.path.rsplit("/", 1)[-1]
        calls.append((endpoint, parse_qsl(split.query, keep_blank_values=True)))
    return calls


def dry_run_values(out: str, name: str, call: int = 0) -> list[str]:
    """Every value sent for one query parameter, in order, from one request."""
    return [value for key, value in dry_run_calls(out)[call][1] if key == name]


def dry_run_bodies(out: str) -> list[dict[str, Any]]:
    """Every JSON body a ``--dry-run`` dump printed, parsed back, in order.

    The dump is what the tool promises it would have sent, so parsing it back
    is how a test asserts on the body of a request that was never issued.
    """
    bodies: list[dict[str, Any]] = []
    lines = out.splitlines()
    index = 0
    while index < len(lines):
        if lines[index].strip() != "JSON body:":
            index += 1
            continue
        index += 1
        block: list[str] = []
        while index < len(lines) and lines[index].startswith("  "):
            block.append(lines[index][2:])
            index += 1
        parsed = json.loads("\n".join(block))
        assert isinstance(parsed, dict), f"a dry run printed a non object body: {parsed}"
        bodies.append(parsed)
    return bodies


def patch_retry_sleep(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    """Make ``main()`` retry without ever really sleeping.

    ``execute`` takes its ``sleep`` and ``jitter`` as injected callables, but
    ``main()`` does not thread them through, so this wraps the dispatcher the
    CLI actually calls and supplies both. The real retry logic still runs; the
    only thing replaced is the blocking wait.

    Returns:
        The list every delay is appended to, in order.
    """
    delays: list[float] = []
    real = vi_http.execute

    def wrapper(
        request: PreparedRequest, session: Any, *args: Any, **kwargs: Any
    ) -> dict[str, Any] | list[Any]:
        kwargs.setdefault("sleep", delays.append)
        kwargs.setdefault("jitter", no_jitter)
        return real(request, session, *args, **kwargs)

    monkeypatch.setattr(vi_cli, "execute", wrapper)
    return delays


def error_payload(code: str, message: str, **extra: Any) -> dict[str, Any]:
    """The documented Vercel error envelope."""
    error: dict[str, Any] = {"code": code, "message": message}
    error.update(extra)
    return {"error": error}


# Payload fixtures. Every shape below is copied from docs/api-notes.md.

VISITS_COUNT_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"filter": "requestPath eq '/blog/my-post'"},
    "data": {"pageviews": 1250, "visitors": 980},
}

EVENTS_COUNT_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"since": "2024-10-01", "until": "2024-10-07"},
    "data": {"count": 42, "visitors": 36},
}

DAILY_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {
        "since": "2024-10-01",
        "until": "2024-10-07",
        "groupBy": ["day"],
        "filter": "requestPath eq '/blog/my-post'",
    },
    "data": [
        {"timestamp": "2024-10-01T00:00:00.000Z", "pageviews": 220, "visitors": 180},
        {"timestamp": "2024-10-02T00:00:00.000Z", "pageviews": 245, "visitors": 201},
    ],
}

COUNTRY_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"since": "2024-10-01", "until": "2024-10-07", "groupBy": ["country"]},
    "data": [
        {"country": "US", "pageviews": 640, "visitors": 510},
        {"country": "DE", "pageviews": 180, "visitors": 150},
    ],
}

COUNTRY_WITH_OTHERS_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"since": "2024-10-01", "until": "2024-10-07", "groupBy": ["country"]},
    "data": [
        {"country": "US", "pageviews": 640, "visitors": 510},
        {"country": "DE", "pageviews": 180, "visitors": 150},
        {"country": "Others", "pageviews": 80, "visitors": 60},
    ],
}

EVENT_DATA_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"groupBy": ["eventData/plan"]},
    "data": [
        {"eventData": "pro", "count": 42, "visitors": 36},
        {"eventData": "enterprise", "count": 12, "visitors": 10},
    ],
}

FLAGS_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"groupBy": ["flags/beta_banner"]},
    "data": [
        {"flags": True, "pageviews": 90, "visitors": 70},
        {"flags": "false", "pageviews": 30, "visitors": 25},
    ],
}

TOP_PAGES_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {
        "since": "2026-08-07",
        "until": "2026-08-14",
        "groupBy": ["requestPath"],
        "limit": 10,
    },
    "data": [
        {"requestPath": "/pricing", "pageviews": 640, "visitors": 510},
        {"requestPath": "/blog/my-post", "pageviews": 180, "visitors": 150},
    ],
}

REFERRERS_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"groupBy": ["referrerHostname"], "limit": 5},
    "data": [
        {"referrerHostname": "news.ycombinator.com", "pageviews": 300, "visitors": 260},
        {"referrerHostname": "google.com", "pageviews": 120, "visitors": 110},
    ],
}

EMPTY_AGGREGATE_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"since": "2026-08-07", "until": "2026-08-14", "groupBy": ["requestPath"]},
    "data": [],
}

TWO_DIMENSION_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"groupBy": ["eventName", "eventData/plan"], "limit": 10},
    "data": [
        {"eventName": "signup", "eventData": "free", "count": 30, "visitors": 28},
        {"eventName": "signup", "eventData": "pro", "count": 12, "visitors": 11},
        {"eventName": "purchase", "eventData": "pro", "count": 3, "visitors": 3},
    ],
}
TWO_DIMENSIONS = ["eventName", "eventData/plan"]

# A response derived label is remote input in the strongest sense: a UTM
# campaign is whatever a visitor typed into a query string. These two carry an
# ANSI colour sequence, a carriage return that would rewrite the line already
# printed, a NUL, a DEL and a C1 introducer, and the escaped forms below are
# what every output format must show instead.
ANSI_CAMPAIGN = "\x1b[31mRED\x1b[0m\rHIDDEN"
ESCAPED_ANSI_CAMPAIGN = "\\x1b[31mRED\\x1b[0m\\x0dHIDDEN"
C1_CAMPAIGN = "ok\x07\x00\x7f\x9b]0;pwned\x07"
ESCAPED_C1_CAMPAIGN = "ok\\x07\\x00\\x7f\\x9b]0;pwned\\x07"

#: Printable Unicode a sanitizer must leave exactly as the API sent it.
UNICODE_CAMPAIGN = "sommerfest-2026 éè 中文 \U0001f680"

CONTROL_CHARACTER_CAMPAIGN_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"groupBy": ["utmCampaign"], "limit": 10},
    "data": [
        {"utmCampaign": ANSI_CAMPAIGN, "pageviews": 5, "visitors": 4},
        {"utmCampaign": C1_CAMPAIGN, "pageviews": 2, "visitors": 2},
        {"utmCampaign": UNICODE_CAMPAIGN, "pageviews": 1, "visitors": 1},
    ],
}

TIME_ONLY_OTHERS_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"groupBy": ["day"], "limit": 2},
    "data": [
        {"timestamp": "2026-08-01T00:00:00.000Z", "pageviews": 10, "visitors": 8},
        {"timestamp": "2026-08-02T00:00:00.000Z", "pageviews": 5, "visitors": 4},
        {"timestamp": "Others", "pageviews": 6, "visitors": 5},
    ],
}

# Speed Insights payload fixtures.
#
# The observability API publishes no response schema, so unlike the Web
# Analytics fixtures above these are plausible shapes rather than transcribed
# ones. Each one is named for the shape it exercises, and the parser is
# expected to read all of them and to refuse anything it cannot read rather
# than to guess.

#: Metric ids, copied character by character out of docs/api-notes.md. They are
#: written out here, never composed from METRICS, so a typo in the package
#: fails a test instead of being mirrored by it.
LCP_ID = "vercel.speed_insights.lcp_ms"
INP_ID = "vercel.speed_insights.inp_ms"
CLS_ID = "vercel.speed_insights.cls"
FCP_ID = "vercel.speed_insights.fcp_ms"
TTFB_ID = "vercel.speed_insights.ttfb_ms"
LCP_COUNT_ID = "vercel.speed_insights.lcp_count"
INP_COUNT_ID = "vercel.speed_insights.inp_count"
CLS_COUNT_ID = "vercel.speed_insights.cls_count"
FCP_COUNT_ID = "vercel.speed_insights.fcp_count"
TTFB_COUNT_ID = "vercel.speed_insights.ttfb_count"


def speed_value_payload(
    metric_id: str, value: float, points: float | None = None, count_id: str = ""
) -> dict[str, Any]:
    """One ungrouped metric value, the shape the vitals preset expects back."""
    data: dict[str, Any] = {"value": value}
    if points is not None:
        data[count_id or "dataPoints"] = points
    return {"version": 1, "query": {"metric": metric_id}, "data": data}


#: One payload per vital, in the order the vitals preset queries them. TTFB is
#: deliberately over its 800 ms target while the other four meet theirs, so a
#: verdict column that always says the same thing fails.
SPEED_VITALS_PAYLOADS: list[dict[str, Any]] = [
    speed_value_payload(LCP_ID, 2412.0, 12480, LCP_COUNT_ID),
    speed_value_payload(INP_ID, 168.0, 12480, INP_COUNT_ID),
    speed_value_payload(CLS_ID, 0.0834, 12480, CLS_COUNT_ID),
    speed_value_payload(FCP_ID, 812.0, 12480, FCP_COUNT_ID),
    speed_value_payload(TTFB_ID, 934.0, 12480, TTFB_COUNT_ID),
]

#: Grouped rows: the plausible shape for slowest-pages and friends.
SPEED_ROUTE_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"metric": LCP_ID, "groupBy": ["route"], "limit": 10},
    "data": [
        {"route": "/blog/[slug]", "value": 4120.0, LCP_COUNT_ID: 1830},
        {"route": "/pricing", "value": 2980.0, LCP_COUNT_ID: 640},
        {"route": "/", "value": 1240.0, LCP_COUNT_ID: 8800},
    ],
}

#: Time buckets: the plausible shape for vitals-trend.
SPEED_TREND_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"metric": LCP_ID, "granularity": {"interval": "1d"}},
    "data": [
        {"timestamp": "2026-08-10T00:00:00.000Z", "value": 2100.0, "dataPoints": 1800},
        {"timestamp": "2026-08-11T00:00:00.000Z", "value": 2450.0, "dataPoints": 1750},
    ],
}

#: A rollup keyed by dimension value rather than a list of rows.
SPEED_ROLLUP_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"metric": LCP_ID, "groupBy": ["country"]},
    "data": {"US": 2100.0, "DE": {"value": 1800.0, "dataPoints": 430}},
}

#: Time buckets carrying their grouped rows inside them.
SPEED_NESTED_BUCKET_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"metric": LCP_ID, "groupBy": ["country"]},
    "data": [
        {
            "timestamp": "2026-08-10T00:00:00.000Z",
            "rows": [
                {"country": "US", "value": 2100.0},
                {"country": "DE", "value": 1800.0},
            ],
        }
    ],
}

#: Data point counts, which do add up and so keep a totals row.
SPEED_DATA_POINTS_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"metric": LCP_COUNT_ID, "groupBy": ["route"], "limit": 10},
    "data": [
        {"route": "/", "value": 8800},
        {"route": "/blog/[slug]", "value": 1830},
    ],
}

#: Grouped rows whose limit overflowed, so the API collapsed the rest into the
#: documented Others bucket. Speed Insights collapses exactly as Web Analytics
#: does, and the row has to be labelled and annotated on this surface too.
SPEED_ROUTE_WITH_OTHERS_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"metric": LCP_ID, "groupBy": ["route"], "limit": 2},
    "data": [
        {"route": "/blog/[slug]", "value": 4120.0, LCP_COUNT_ID: 1830},
        {"route": "/pricing", "value": 2980.0, LCP_COUNT_ID: 640},
        {"route": "Others", "value": 1240.0, LCP_COUNT_ID: 8800},
    ],
}

#: A route label and a bucket label carrying terminal control sequences. Both
#: are remote input rendered into the same table cells as any other label.
ANSI_ROUTE = "/\x1b[2Jwiped"
ESCAPED_ANSI_ROUTE = "/\\x1b[2Jwiped"
ANSI_BUCKET = "2026-08-10T00:00:00Z\x1b[2J"
ESCAPED_ANSI_BUCKET = "2026-08-10T00:00:00Z\\x1b[2J"

SPEED_EMPTY_PAYLOAD: dict[str, Any] = {
    "version": 1,
    "query": {"metric": LCP_ID},
    "data": [],
}

#: Shapes this client must refuse outright. Reading a number out of any of them
#: would mean printing a confidently formatted wrong figure, which is worse
#: than an error naming the shape.
SPEED_MALFORMED_PAYLOADS: list[tuple[str, dict[str, Any]]] = [
    ("data-is-a-string", {"version": 1, "query": {}, "data": "2412 ms"}),
    ("data-is-a-status-object", {"version": 1, "data": {"status": "ok"}}),
    ("data-is-a-list-of-strings", {"version": 1, "data": ["/pricing", "/"]}),
    ("envelope-with-no-data", {"version": 1, "query": {"metric": LCP_ID}}),
    ("data-is-null", {"version": 1, "query": {}, "data": None}),
    ("rows-carry-no-number", {"version": 1, "data": [{"route": "/", "value": "fast"}]}),
]

# Request logs payload fixtures.
#
# These rows are copied from docs/api-notes.md, which in turn holds the real
# probed rows. Their shape is real; their identifiers are fictional, replaced
# in both places at the same time so the fixture and the record still agree.


def logs_row(**overrides: Any) -> dict[str, Any]:
    """One request-logs row, shaped exactly as the live API returns them."""
    row: dict[str, Any] = {
        "requestId": "abcde-1786964768933-0123456789ab",
        "timestamp": "2026-08-17T11:06:08.933Z",
        "deploymentId": "dpl_ExampleDeploymentId000000000",
        "environment": "production",
        "deploymentDomain": "demo.vercel.app",
        "branch": "main",
        "domain": "demo.vercel.app",
        "requestMethod": "GET",
        "requestPath": "/api/me",
        "statusCode": 401,
        "errorCode": "",
        "route": "/api/me",
        "cache": "MISS",
        "wafAction": "",
        "traceId": "",
        "logs": [],
        "requestDurationMs": 54,
        "clientRegion": "fra1",
        "hasFunctionCrashed": False,
        "events": [{"source": "serverless", "httpStatus": 401, "region": "fra1"}],
        "requestTags": ["ssr", "rsc"],
    }
    row.update(overrides)
    return row


#: A page of ordinary traffic: no 5xx, no log lines. This is what a healthy
#: project really returns, and it is the shape that makes --level answer with
#: zero rows.
LOGS_PAGE: dict[str, Any] = {"rows": [logs_row()], "hasMoreRows": False}

#: A page carrying the two kinds of error: a 500 that logged a stack trace, and
#: a 502 that logged nothing at all.
LOGS_ERROR_PAGE: dict[str, Any] = {
    "rows": [
        logs_row(
            requestId="err-1",
            timestamp="2026-08-17T11:04:52.100Z",
            requestMethod="POST",
            requestPath="/api/checkout",
            route="/api/checkout",
            statusCode=500,
            logs=[
                {
                    "level": "error",
                    "message": "TypeError: Cannot read properties of undefined",
                    "messageTruncated": False,
                }
            ],
        ),
        logs_row(
            requestId="err-2",
            timestamp="2026-08-17T10:58:03.000Z",
            requestPath="/api/documents/summer",
            route="/api/documents/[slug]",
            statusCode=502,
            logs=[],
        ),
    ],
    "hasMoreRows": False,
}

LOGS_EMPTY_PAGE: dict[str, Any] = {"rows": [], "hasMoreRows": False}

SECRET = "sk_SUPERSECRETVALUE"
