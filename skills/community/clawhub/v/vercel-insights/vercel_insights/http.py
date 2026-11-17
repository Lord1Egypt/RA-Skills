"""The operation allowlist, request preparation, redaction and retries.

Surface agnostic: nothing here knows about page views or web vitals. It knows
which operations exist, how to render one safely, and how to perform one.

The allowlist
-------------
:data:`OPERATIONS` is the whole of this client's reachable API surface. It maps
an operation key to a fixed ``(method, url_template)`` pair, and it is the only
place either value is written down. :func:`execute` takes a
:class:`PreparedRequest`, which carries an operation *key*, never a method and
never a host, so no user input can select, extend or override an entry. There
are exactly two HTTP call sites in this package, ``session.get`` and
``session.post``, and both are inside :func:`execute`. Neither follows
redirects, so the allowlist binds every hop of a request rather than only its
first: a 3xx is reported as an error naming the location it wanted to send the
``Authorization`` header to.

One of the six operations is a POST. That is still a read: Vercel exposes no
GET equivalent for an observability query, so the query travels in the body.
Nothing is created or mutated, and the toggle endpoints that would enable or
disable a feature are deliberately absent from the table.

The allowlist spans two hosts: ``api.vercel.com`` for five operations and
``vercel.com`` for request logs, the one entry documented elsewhere. A
redirect is still refused at both call sites, so the allowlist binds every
hop regardless of which of the two hosts a request started on.
"""

from __future__ import annotations

import json
import math
import random
import re
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import timezone
from email.utils import parsedate_to_datetime
from typing import Any, Protocol
from urllib.parse import urlencode

import requests

from . import (
    BASE_URL,
    DOCS_TOKEN_URL,
    LOGS_BASE_URL,
    VERSION,
    ApiError,
    ConfigError,
    RateLimitError,
    sanitize_label,
    sanitize_message,
)

#: Every operation this client can perform, and nothing else. The key is what
#: callers pass around; the method and the URL template are read from here and
#: are never accepted from a caller.
OPERATIONS: dict[str, tuple[str, str]] = {
    "web_analytics": ("GET", BASE_URL + "/v1/query/web-analytics/{dataset}/{endpoint}"),
    "observability_query": ("POST", BASE_URL + "/v2/observability/query"),
    "observability_schema": ("GET", BASE_URL + "/v2/observability/schema"),
    # Read-only, and needed because a Speed Insights scope requires an ownerId.
    # The project's own record carries it as accountId, which is a better
    # source than the account endpoint: it works for a team owned and a
    # personal project alike, and it reads a resource the token must already be
    # able to see, since that is the project being queried. Consulted at most
    # once per run, and only on the Speed Insights surface.
    "project": ("GET", BASE_URL + "/v9/projects/{project}"),
    # Read-only. One Vercel account holds many projects, and picking the right
    # one is the first thing anybody has to do, so listing them is part of the
    # job rather than a convenience.
    "projects": ("GET", BASE_URL + "/v10/projects"),
    # Read-only. Runtime request logs. The one entry that is not on
    # api.vercel.com and not in Vercel's published OpenAPI document: its ground
    # truth is the official CLI plus the live probes recorded in
    # docs/api-notes.md, so it can change without notice. Nothing is created or
    # mutated; the whole query travels in the query string.
    "request_logs": ("GET", LOGS_BASE_URL + "/api/logs/request-logs"),
}

DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3

#: Statuses worth retrying. Any other 5xx is retried too; no other 4xx ever is.
#: 408 is here because the observability query API documents it: a query can
#: time out server side, and that is worth another attempt.
RETRYABLE_STATUSES: frozenset[int] = frozenset({408, 429, 500, 502, 503, 504})

BACKOFF_BASE_SECONDS = 0.5
MAX_SLEEP_SECONDS = 60.0

REDACTED_BEARER = "Bearer <redacted>"
REDACTED = "<redacted>"
_SENSITIVE_HEADERS = frozenset({"authorization", "proxy-authorization", "cookie"})

#: Shortest bare credential that is substring matched when scrubbing text. A
#: real Vercel token is far longer; anything shorter is not a credential and
#: matching it would corrupt every message it appears inside.
MIN_SCRUBBABLE_CREDENTIAL = 8

#: A path segment substituted into a URL template. No slash, no scheme, no
#: host, so a template can only ever be filled in with a single path segment.
_PATH_SEGMENT_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

USER_AGENT = f"vercel-insights-skill/{VERSION}"


# ---------------------------------------------------------------------------
# The allowlist
# ---------------------------------------------------------------------------


def _static_prefix(template: str) -> str:
    """The part of a URL template before its first placeholder."""
    prefix, separator, _rest = template.partition("{")
    return prefix if separator else template


def _is_path_segment(value: str) -> bool:
    """True for a value that can only ever be one literal path segment.

    No slash, no scheme, no host, and neither of the relative names, so a
    substituted value cannot climb out of the path the template pins down.
    """
    if value in (".", ".."):
        return False
    return _PATH_SEGMENT_RE.match(value) is not None


def operation_url(operation: str, **values: str) -> str:
    """Build the URL for one allowlisted operation.

    This is the only way a URL is ever produced. The operation key selects a
    template from :data:`OPERATIONS`, and each substituted value must be a
    single path segment, so no value can introduce a host, a scheme, a query
    string or a parent directory traversal.

    Raises:
        ConfigError: When the operation is not on the allowlist, or a value is
            not a usable path segment.
    """
    entry = OPERATIONS.get(operation)
    if entry is None:
        raise ConfigError(
            f"unknown operation {operation!r}; this client can only perform "
            f"{', '.join(sorted(OPERATIONS))}"
        )
    for name, value in values.items():
        if not _is_path_segment(value):
            raise ConfigError(
                f"{name} {value!r} is not a usable path segment for the "
                f"{operation} operation"
            )
    return entry[1].format(**values)


def url_is_allowed(operation: str, url: str) -> bool:
    """True when ``url`` can only have come from ``operation``'s template.

    A template with no placeholder must match exactly. A template with
    placeholders must match its literal prefix and then exactly as many plain
    path segments as it has placeholders.
    """
    entry = OPERATIONS.get(operation)
    if entry is None:
        return False
    template = entry[1]
    prefix = _static_prefix(template)
    if prefix == template:
        return url == template
    if not url.startswith(prefix):
        return False
    remainder = url[len(prefix) :]
    wanted = template[len(prefix) :].split("/")
    segments = remainder.split("/")
    if len(segments) != len(wanted):
        return False
    return all(_is_path_segment(segment) for segment in segments)


# ---------------------------------------------------------------------------
# The prepared request
# ---------------------------------------------------------------------------


@dataclass(frozen=True, repr=False)
class PreparedRequest:
    """Everything needed to issue one allowlisted request, and nothing else.

    ``operation`` is a key into :data:`OPERATIONS`, not a method and not a
    host: :meth:`method` is read back out of the table, so it cannot diverge
    from the allowlist, and ``__post_init__`` refuses a URL that the operation's
    template could not have produced.

    ``params`` is an ordered list of pairs rather than a mapping because ``by``
    may legitimately appear twice. ``json_body`` is populated only for a POST
    operation and carries the query itself, never a credential. ``headers`` is
    the only place a credential ever lives, and the generated ``repr`` is
    suppressed so that printing one of these cannot leak it: :meth:`__repr__`
    renders headers through :func:`redact_headers`, which makes the guarantee
    structural rather than a promise that no caller ever prints the object.
    """

    operation: str
    url: str
    params: list[tuple[str, str]]
    headers: dict[str, str]
    json_body: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.operation not in OPERATIONS:
            raise ConfigError(
                f"unknown operation {self.operation!r}; this client can only "
                f"perform {', '.join(sorted(OPERATIONS))}"
            )
        if not url_is_allowed(self.operation, self.url):
            raise ConfigError(
                f"the {self.operation} operation cannot address {self.url!r}"
            )

    @property
    def method(self) -> str:
        """The HTTP method, read from the allowlist rather than stored."""
        return OPERATIONS[self.operation][0]

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(operation={self.operation!r}, "
            f"method={self.method!r}, url={self.url!r}, params={self.params!r}, "
            f"headers={redact_headers(self.headers)!r}, "
            f"json_body={self.json_body!r})"
        )


def default_headers(token: str | None) -> dict[str, str]:
    """The headers every request carries, with the token in one place only."""
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


# ---------------------------------------------------------------------------
# Credential handling
# ---------------------------------------------------------------------------


def redact_headers(headers: Mapping[str, str]) -> dict[str, str]:
    """Copy headers with every credential replaced by a fixed placeholder.

    This is the only way headers are ever rendered, in dry runs, verbose
    diagnostics and error paths alike.
    """
    safe: dict[str, str] = {}
    for name, value in headers.items():
        if name.lower() in _SENSITIVE_HEADERS:
            safe[name] = REDACTED_BEARER if value.startswith("Bearer ") else REDACTED
        else:
            safe[name] = value
    return safe


def _credential_values(headers: Mapping[str, str]) -> list[str]:
    """Every secret string present in ``headers``, longest first.

    Both the whole header value and the bare bearer credential are returned, so
    a message that quotes either form is scrubbed. Longest first matters: it
    keeps ``Bearer <token>`` from being partially replaced.
    """
    values: set[str] = set()
    for name, value in headers.items():
        if name.lower() not in _SENSITIVE_HEADERS or not value:
            continue
        values.add(value)
        if value.startswith("Bearer "):
            bearer = value[len("Bearer ") :].strip()
            # A bare credential is replaced wherever it appears, which is only
            # safe while it is long enough to be a credential. A one or two
            # character value would match ordinary letters everywhere and turn
            # every message into unreadable confetti, for example a token of
            # "t" rewriting "https" as "h<redacted><redacted>ps". The whole
            # header value is always scrubbed regardless of length, so nothing
            # is exposed by declining to substring match a value this short:
            # such a value is rejected as a token by validate_token anyway.
            if len(bearer) >= MIN_SCRUBBABLE_CREDENTIAL:
                values.add(bearer)
    return sorted(values, key=len, reverse=True)


def scrub_credentials(text: str, headers: Mapping[str, str]) -> str:
    """Replace every credential from ``headers`` with a fixed placeholder.

    :func:`redact_headers` protects headers that this module renders itself.
    This protects the other direction: text produced elsewhere, above all an
    exception message from ``requests``. ``InvalidHeader``, for one, embeds the
    offending header value verbatim, so any message on its way into an
    :class:`ApiError` goes through here first. Structuring it this way means a
    future exception type cannot reinstate the leak.
    """
    scrubbed = text
    for secret in _credential_values(headers):
        scrubbed = scrubbed.replace(secret, REDACTED)
    return scrubbed


def _bad_token_reason(token: str) -> str | None:
    """Describe why ``token`` cannot be an HTTP header value, or ``None``.

    The description never contains any part of the token itself: only its
    length, the offending position, and the class of character found there.
    """
    if token != token.strip(" "):
        side = "leading" if token[:1] == " " else "trailing"
        return f"a {side} space"
    for index, char in enumerate(token, start=1):
        code = ord(char)
        if char in "\r\n":
            name = "a carriage return" if char == "\r" else "a line feed"
            return f"{name} at position {index}"
        if code < 0x20 or code == 0x7F:
            return f"a control character (U+{code:04X}) at position {index}"
        if code > 0x7F:
            return f"a non-ASCII character (U+{code:04X}) at position {index}"
    return None


def validate_token(token: str) -> str:
    """Reject a credential that cannot safely become a header value.

    A token carrying a carriage return or line feed is a header injection
    vector, and the exception ``requests`` raises for one embeds the offending
    value, which would print the credential to stderr. Catching it here, before
    a request object exists, means that exception can never be raised.

    The error names the length and the character class only, never the value.

    Raises:
        ConfigError: When the token is empty or not printable ASCII.
    """
    if not token:
        raise ConfigError(
            "the access token is empty; pass --token or set VERCEL_TOKEN "
            f"(create one at {DOCS_TOKEN_URL})"
        )
    reason = _bad_token_reason(token)
    if reason is not None:
        raise ConfigError(
            f"the access token is not usable as an HTTP header value: the "
            f"{len(token)} character value contains {reason}. A Vercel token is "
            "printable ASCII with no spaces, so re-copy it (a stray newline from "
            f"a shell here-doc or a copy and paste is the usual cause; create a "
            f"fresh one at {DOCS_TOKEN_URL}). The token itself is not shown."
        )
    return token


def validate_timeout(timeout: float) -> float:
    """Check ``--timeout`` before it reaches the socket layer.

    ``argparse`` happily accepts ``0``, a negative number, ``nan`` and ``inf``
    (``1e400`` parses to ``inf``), each of which makes urllib3 raise deep inside
    the request. They are caught here instead, as a plain configuration error.

    Raises:
        ConfigError: When the value is not a finite number above zero.
    """
    value = float(timeout)
    if math.isnan(value) or math.isinf(value):
        raise ConfigError(
            f"--timeout {timeout!r} is not a finite number of seconds; pass a "
            f"real value such as --timeout {DEFAULT_TIMEOUT}"
        )
    if value <= 0:
        raise ConfigError(
            f"--timeout {value:g} must be greater than 0 seconds, since a "
            "zero or negative timeout can never allow a request to finish; "
            f"pass a value such as --timeout {DEFAULT_TIMEOUT}"
        )
    return value


def format_dry_run(request: PreparedRequest) -> str:
    """Render a request for ``--dry-run``: complete, readable, credential free.

    A POST operation prints the full JSON body it would have sent, so a dry run
    shows the whole query and not just its envelope.
    """
    safe_headers = redact_headers(request.headers)
    safe_headers.setdefault("Authorization", REDACTED_BEARER)

    lines: list[str] = [f"{request.method} {request.url}", "", "Query parameters:"]
    if request.params:
        width = max(len(name) for name, _ in request.params)
        for name, value in request.params:
            lines.append(f"  {name.ljust(width)}  {value}")
    else:
        lines.append("  (none)")

    lines.extend(["", "Headers:"])
    header_width = max(len(name) for name in safe_headers)
    for name in sorted(safe_headers):
        lines.append(f"  {name.ljust(header_width)}  {safe_headers[name]}")

    if request.json_body is not None:
        lines.extend(["", "JSON body:"])
        lines.extend(
            f"  {line}" for line in json.dumps(request.json_body, indent=2).splitlines()
        )

    query = urlencode(request.params)
    lines.extend(
        [
            "",
            "Encoded URL (never contains the token):",
            f"  {request.url}?{query}" if query else f"  {request.url}",
            "",
            "Nothing was sent. No credential is printed above.",
        ]
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Performing a request
# ---------------------------------------------------------------------------


class ResponseLike(Protocol):
    """The slice of a response this module reads."""

    @property
    def status_code(self) -> int: ...

    @property
    def headers(self) -> Mapping[str, str]: ...

    @property
    def text(self) -> str: ...


class SessionLike(Protocol):
    """The two HTTP capabilities this module needs, both injectable."""

    def get(
        self,
        url: str,
        *,
        params: list[tuple[str, str]] | None = ...,
        headers: dict[str, str] | None = ...,
        timeout: float | None = ...,
        allow_redirects: bool = ...,
    ) -> Any: ...

    def post(
        self,
        url: str,
        *,
        params: list[tuple[str, str]] | None = ...,
        headers: dict[str, str] | None = ...,
        json: dict[str, Any] | None = ...,
        timeout: float | None = ...,
        allow_redirects: bool = ...,
    ) -> Any: ...


def _default_jitter() -> float:
    """Randomised padding added to a computed retry delay."""
    return random.uniform(0.0, 0.25)


def retry_delay(
    attempt: int,
    response: ResponseLike | None,
    body: Mapping[str, Any] | None,
    now: float,
) -> float:
    """Decide how long to wait before retry number ``attempt`` (0 based).

    Preference order: the ``Retry-After`` header, then ``error.limit.resetMs``,
    then ``error.limit.reset``, then exponential backoff from
    :data:`BACKOFF_BASE_SECONDS`, doubling each attempt. Any single wait is
    capped at :data:`MAX_SLEEP_SECONDS`. Jitter is added by :func:`execute` so
    that this function stays pure and testable.

    Args:
        attempt: Zero based index of the attempt that just failed.
        response: The failed response, or ``None`` for a network level failure.
        body: The parsed error envelope, when there was one.
        now: Current Unix time in seconds, injected for determinism.

    Returns:
        Seconds to sleep, never negative and never above the cap.
    """
    if response is not None:
        header = response.headers.get("Retry-After")
        seconds = _parse_retry_after(header, now)
        if seconds is not None and seconds > 0:
            return min(seconds, MAX_SLEEP_SECONDS)

    limit = _error_field(body, "limit")
    if isinstance(limit, Mapping):
        reset_ms = limit.get("resetMs")
        if isinstance(reset_ms, (int, float)) and not isinstance(reset_ms, bool):
            delay = float(reset_ms) / 1000.0 - now
            if delay > 0:
                return min(delay, MAX_SLEEP_SECONDS)
        reset = limit.get("reset")
        if isinstance(reset, (int, float)) and not isinstance(reset, bool):
            delay = float(reset) - now
            if delay > 0:
                return min(delay, MAX_SLEEP_SECONDS)

    backoff = BACKOFF_BASE_SECONDS * float(2**attempt)
    return min(backoff, MAX_SLEEP_SECONDS)


def _parse_retry_after(header: str | None, now: float) -> float | None:
    """Read a ``Retry-After`` header in either delay-seconds or HTTP-date form."""
    if not header:
        return None
    text = header.strip()
    try:
        return float(text)
    except ValueError:
        pass
    try:
        when = parsedate_to_datetime(text)
    except (TypeError, ValueError):
        return None
    if when is None:
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return when.timestamp() - now


def _error_field(body: Mapping[str, Any] | None, name: str) -> Any:
    """Read one field out of the ``{"error": {...}}`` envelope, defensively."""
    if not isinstance(body, Mapping):
        return None
    error = body.get("error")
    if not isinstance(error, Mapping):
        return None
    return error.get(name)


def _reject_json_constant(name: str) -> float:
    """Refuse the three non-standard literals ``json`` accepts by default.

    ``json.loads`` reads ``NaN``, ``Infinity`` and ``-Infinity`` as floats even
    though none of them is JSON, and a ``nan`` that gets that far propagates
    silently: it compares false against every target, formats as ``nan``, and
    can surface as a raw traceback instead of a message. Rejecting them at the
    parse boundary turns the whole class of problem into one clean
    ``invalid_response`` error.

    Raises:
        ValueError: Always, which :func:`_parse_body` turns into "not JSON".
    """
    raise ValueError(f"{name} is not valid JSON")


def _reject_non_finite(value: Any) -> None:
    """Walk a parsed body and refuse any float that is not finite.

    :func:`_reject_json_constant` only sees the three bare literal tokens, so it
    misses a number that overflows on the way in: ``1e999`` is well formed JSON
    and ``json.loads`` reads it as ``inf`` without ever calling ``parse_constant``.
    An ``inf`` that gets through renders as ``inf`` in a table and, worse, comes
    back out of ``--json`` as a bare ``Infinity``, which is not JSON and which a
    strict consumer such as ``jq`` refuses. Since this client's own README sells
    piping ``--json`` into ``jq``, that has to be caught here rather than papered
    over at the dump site.

    Raises:
        ValueError: On the first non-finite float found.
    """
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("a non-finite number is not valid JSON")
        return
    if isinstance(value, Mapping):
        for item in value.values():
            _reject_non_finite(item)
        return
    if isinstance(value, (list, tuple)):
        for item in value:
            _reject_non_finite(item)


def _parse_body(text: str) -> dict[str, Any] | list[Any] | None:
    """Parse a response body, returning ``None`` when it is not JSON we accept.

    A JSON object or a JSON array is accepted: the schema endpoint answers with
    a top level array, while every query endpoint answers with an object, and
    both are legitimate. Anything else, a bare string or number for instance, is
    not a response this client has any use for.

    ``None`` also covers a body that is syntactically JSON but carries a
    non-standard literal or a non-finite number; see
    :func:`_reject_json_constant` and :func:`_reject_non_finite`.
    """
    if not text:
        return None
    try:
        parsed = json.loads(text, parse_constant=_reject_json_constant)
        _reject_non_finite(parsed)
    except ValueError:
        return None
    if isinstance(parsed, (dict, list)):
        return parsed
    return None


def _api_error(
    status: int,
    body: Mapping[str, Any] | None,
    text: str,
    attempts: int,
    scrub: Callable[[str], str],
) -> ApiError:
    """Build the exception for a failed response, keeping Vercel's wording."""
    code = _error_field(body, "code")
    message = _error_field(body, "message")
    code_text = code if isinstance(code, str) else None
    if isinstance(message, str) and message:
        message_text = message
    else:
        snippet = text.strip().replace("\n", " ")[:300]
        message_text = snippet or "the API returned no error message"
    # The message is quoted verbatim from the response, so it is remote input:
    # an error body carrying an ANSI escape could blank the screen and forge a
    # convincing second line ("error: everything fine") under our own prefix.
    # Newlines survive, indented, because these bodies are often pretty-printed
    # JSON and escaping them makes the one thing worth reading unreadable.
    message_text = sanitize_message(scrub(message_text))
    if status == 429 or code_text == "rate_limited":
        limit = _error_field(body, "limit")
        return RateLimitError(
            status,
            code_text or "rate_limited",
            message_text,
            attempts=attempts,
            limit=limit if isinstance(limit, Mapping) else None,
        )
    return ApiError(status, code_text, message_text, attempts=attempts)


def _redirect_error(
    status: int,
    response: ResponseLike,
    request: PreparedRequest,
    scrub: Callable[[str], str],
    attempts: int,
) -> ApiError:
    """Refuse a redirect rather than carrying the credential to its target.

    Redirects are not followed, so the operation allowlist binds every hop
    rather than only the first: a 3xx from any of the allowlisted URLs could
    otherwise send the ``Authorization`` header to whatever host the ``Location``
    names, including off the two hosts the table spans. None of the six
    operations is documented to redirect, so one is a change worth reporting
    rather than a step to take silently.

    The location is named because it is the whole diagnostic. It is a response
    header, so it is remote input: it goes through :func:`sanitize_label` as well
    as the credential scrub, or a crafted ``Location`` could paint whatever it
    liked on the terminal of whoever ran the command.
    """
    location = response.headers.get("Location") or response.headers.get("location")
    target = (
        f" to {sanitize_label(scrub(location))}" if location else " (no Location header)"
    )
    return ApiError(
        status,
        "unexpected_redirect",
        scrub(
            f"{request.url} answered with a redirect{target}, which this client "
            "does not follow: the token travels in the Authorization header, and "
            "following a redirect would hand it to whatever host the redirect "
            "names. The six endpoints this client may call are fixed, and none "
            "of them is documented to redirect, so check for a proxy or a "
            "captive network between you and Vercel"
        ),
        attempts=attempts,
    )


def _is_retryable(status: int) -> bool:
    """Retry 408, 429 and any 5xx. Never any other 4xx."""
    return status in RETRYABLE_STATUSES or status >= 500


def execute(
    request: PreparedRequest,
    session: SessionLike,
    sleep: Callable[[float], None] = time.sleep,
    jitter: Callable[[], float] = _default_jitter,
    max_retries: int = DEFAULT_MAX_RETRIES,
    timeout: float = DEFAULT_TIMEOUT,
    *,
    now: Callable[[], float] = time.time,
    on_retry: Callable[[str], None] | None = None,
) -> dict[str, Any] | list[Any]:
    """Perform the request, retrying only what is safe to retry.

    This is the one and only dispatcher, and the only place in the package
    where an HTTP call is made. It reads the method out of :data:`OPERATIONS`
    using the request's operation key, so the set of reachable methods and
    hosts is fixed by that table and by nothing else. ``sleep``, ``jitter`` and
    ``now`` are injected so retry behaviour is deterministic under test.

    Args:
        request: The prepared request, carrying an allowlisted operation key.
        session: Anything exposing a compatible ``get`` and ``post``.
        sleep: Blocking sleep, injected.
        jitter: Returns extra seconds to add to each delay, injected.
        max_retries: Retries after the first attempt; 0 disables retrying.
        timeout: Per attempt timeout in seconds.
        now: Returns current Unix time in seconds, injected.
        on_retry: Optional callback receiving a one line reason per retry.

    Returns:
        The parsed JSON response object.

    Raises:
        ApiError: On a non-retryable failure, or once retries are exhausted.
        RateLimitError: When the failure is a rate limit.
    """
    method = OPERATIONS[request.operation][0]
    attempts = max(0, max_retries) + 1

    def safe(text: str) -> str:
        """Every string that reaches an ApiError from here passes through this."""
        return scrub_credentials(text, request.headers)

    for attempt in range(attempts):
        is_last = attempt == attempts - 1
        response: Any = None
        try:
            if method == "GET":
                response = session.get(
                    request.url,
                    params=request.params,
                    headers=request.headers,
                    timeout=timeout,
                    allow_redirects=False,
                )
            else:
                response = session.post(
                    request.url,
                    params=request.params,
                    headers=request.headers,
                    json=request.json_body,
                    timeout=timeout,
                    allow_redirects=False,
                )
        except (requests.Timeout, requests.ConnectionError) as exc:
            reason = safe(f"{type(exc).__name__}: {exc}")
            if is_last:
                raise ApiError(
                    None,
                    "network_error",
                    f"could not reach {request.url}: {reason}",
                    attempts=attempts,
                ) from exc
            delay = _delay_with_jitter(retry_delay(attempt, None, None, now()), jitter)
            if on_retry:
                on_retry(f"{reason}; retrying in {delay:.2f}s")
            sleep(delay)
            continue
        except requests.RequestException as exc:
            raise ApiError(
                None,
                "request_failed",
                safe(f"request to {request.url} failed: {type(exc).__name__}: {exc}"),
                attempts=attempt + 1,
            ) from exc

        status = int(response.status_code)
        text = str(response.text)
        body = _parse_body(text)
        # Only an object can carry an error envelope or a rate limit block;
        # a top level array (the schema endpoint) carries neither.
        envelope = body if isinstance(body, Mapping) else None

        if 300 <= status < 400:
            raise _redirect_error(status, response, request, safe, attempt + 1)

        if 200 <= status < 300:
            if body is None:
                raise ApiError(
                    status,
                    "invalid_response",
                    safe(
                        "the response was not a JSON object or array (a body "
                        "carrying NaN, Infinity or -Infinity is refused here "
                        "too: none of the three is JSON)"
                    ),
                    attempts=attempt + 1,
                )
            return body

        if _is_retryable(status) and not is_last:
            delay = _delay_with_jitter(
                retry_delay(attempt, response, envelope, now()), jitter
            )
            if on_retry:
                on_retry(f"HTTP {status}; retrying in {delay:.2f}s")
            sleep(delay)
            continue

        raise _api_error(
            status,
            envelope,
            text,
            attempt + 1 if not is_last else attempts,
            safe,
        )

    raise ApiError(None, "no_attempt", "no request was attempted", attempts=attempts)


def _delay_with_jitter(delay: float, jitter: Callable[[], float]) -> float:
    """Add injected jitter to a delay and keep it inside the sleep cap."""
    return max(0.0, min(delay + jitter(), MAX_SLEEP_SECONDS))
