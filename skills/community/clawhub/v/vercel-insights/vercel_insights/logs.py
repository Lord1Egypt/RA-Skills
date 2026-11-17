"""Request logs request building and response normalization.

Everything specific to ``GET https://vercel.com/api/logs/request-logs`` lives
here: the level, source and status vocabularies, the parameter allowlist, the
shape of the rows it returns, its paging, and the local aggregation that turns
rows into a summary. The modules underneath (``http``, ``timerange``,
``render``) know none of it.

Two things make this surface unlike the other two, and both shape the code:

* **The API validates almost nothing.** An unknown ``level`` or ``source``
  answers ``200`` with zero rows, so a typo would read as "nothing is broken".
  Every vocabulary is therefore checked here, before a request exists.
* **``level`` matches application log lines, not responses.** A ``500`` that
  printed nothing carries no log line and no level, and a ``200`` whose handler
  logged a stack trace is not a ``5xx``. Neither filter alone answers "what
  broke", which is why the errors presets query both and merge.

See docs/api-notes.md for the live probes behind every claim here.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timedelta, timezone
from typing import Any

from . import ApiError, ConfigError, sanitize_label, sanitize_message
from .http import PreparedRequest, default_headers, operation_url
from .render import (
    ERROR_LEVELS,
    LogEntry,
    LogLine,
    LogReport,
    LogSummary,
    MessageTally,
    RouteTally,
)
from .timerange import to_unix_ms

#: The operation key this surface uses. A key into ``http.OPERATIONS``, never a
#: method and never a host.
OPERATION = "request_logs"

#: Log levels the API filters on, in the order the help text lists them.
LEVELS: tuple[str, ...] = ("error", "warning", "info", "fatal")

#: Sources the API filters on.
SOURCES: tuple[str, ...] = (
    "serverless",
    "edge-function",
    "edge-middleware",
    "static",
)

#: Row display values that are not filter values, mapped to the filter spelling
#: that matches them. Verified live on 2026-08-17: the source column of a real
#: row reads ``serverless-middleware``, while the filter that matches those rows
#: is ``edge-middleware`` (every row it returned carried a serverless-middleware
#: event, and ``source=serverless-middleware`` returned nothing). Accepting the
#: displayed spelling means a user can filter by what this tool showed them.
SOURCE_ALIASES: dict[str, str] = {"serverless-middleware": "edge-middleware"}


def _source_alias_note() -> str:
    """Compose the sentence that warns the two source vocabularies differ.

    Returns:
        One sentence naming every display spelling in :data:`SOURCE_ALIASES`
        with the filter spelling it resolves to. Composed rather than written
        out because two places print it, ``--source``'s help text and the
        refusal :func:`validate_sources` raises, and a probed API fact copied
        by hand into two strings is a fact that can drift in one of them.
    """
    pairs = [
        f"{display!r}, which is filtered as {resolved!r}"
        for display, resolved in sorted(SOURCE_ALIASES.items())
    ]
    return "The source column may display " + "; ".join(pairs) + "."


#: The alias warning, for ``--source``'s help and for its refusal message.
SOURCE_ALIAS_NOTE = _source_alias_note()

#: The HTTP methods worth naming when a ``--method`` value looks like a typo.
#: A method outside this set is still sent: a custom verb is legal HTTP and
#: refusing one would remove capability the API may well have. What is not
#: acceptable is silence, because this API answers a method it never recorded
#: with 200 and zero rows, which reads as a healthy site.
METHODS: tuple[str, ...] = (
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
    "TRACE",
    "CONNECT",
)

#: Rows per page. Fixed by the API: the ``limit`` parameter is accepted and
#: ignored, which is why a row limit is enforced in this client instead.
PAGE_SIZE = 50

#: How many pages one call will ever fetch. A page took up to 6 seconds in
#: testing, so four pages is already 24 seconds against a 30 second per request
#: timeout. Raising this trades an answer for a hang.
MAX_PAGES = 4

MIN_LIMIT = 1
MAX_LIMIT = PAGE_SIZE * MAX_PAGES
DEFAULT_LIMIT = PAGE_SIZE

#: One ``statusCode`` item: three characters where the first is a digit and the
#: rest are digits or ``x``, or the literal ``None``. The API's own message
#: names exactly this rule, and is quoted in the error below.
_STATUS_ITEM_RE = re.compile(r"^[1-9][0-9x]{2}$")


def _split(value: str) -> list[str]:
    """Split a comma separated flag value, dropping surrounding whitespace."""
    return [item.strip() for item in value.split(",") if item.strip()]


def _validate_vocabulary(
    flag: str, noun: str, value: str, vocabulary: tuple[str, ...]
) -> str:
    """Validate a comma separated list against a fixed vocabulary.

    Shared by :func:`validate_levels` and :func:`validate_sources`, which
    differ only in the flag, the noun and the vocabulary: both need every
    accepted value named, and the same 200-with-zero-rows danger explained,
    so one message template serves both rather than two that could drift.

    Args:
        flag: The flag name, without its leading dashes, for example
            ``"level"``.
        noun: What one item of this vocabulary is called, for the message,
            for example ``"log level"``.
        value: One or more comma separated names, any case.
        vocabulary: Every value this API accepts for this flag.

    Returns:
        The lower-cased comma separated list to send.

    Raises:
        ConfigError: When the list is empty or names a value outside
            ``vocabulary``. The API answers an unknown value with HTTP 200
            and zero rows rather than an error, so an unchecked typo would
            read as "nothing is broken".
    """
    items = [item.lower() for item in _split(value)]
    unknown = [item for item in items if item not in vocabulary]
    if not items or unknown:
        offending = f"{unknown[0]!r}" if unknown else "an empty list"
        raise ConfigError(
            f"--{flag} {offending} is not a {noun} this API knows; it accepts "
            f"{', '.join(vocabulary)}, comma separated. This is checked here "
            "because the API answers an unknown value with HTTP 200 and zero "
            "rows rather than an error, which would read as 'nothing is broken'"
        )
    return ",".join(items)


def validate_levels(value: str) -> str:
    """Validate a ``--level`` list and return it as the API spells it.

    Args:
        value: One or more comma separated level names, any case.

    Returns:
        The lower-cased comma separated list to send.

    Raises:
        ConfigError: When the list is empty or names a level the API does not
            know. The API answers 200 with zero rows for an unknown level, so
            an unchecked typo would report a healthy site.
    """
    return _validate_vocabulary("level", "log level", value, LEVELS)


def _resolve_source_aliases(value: str) -> str:
    """Rewrite display-only source spellings to their filter spelling.

    The source column can print a value, such as ``serverless-middleware``,
    that the API does not accept back as a filter; :data:`SOURCE_ALIASES`
    records the filter spelling that matches each one. Resolving this before
    :func:`_validate_vocabulary` runs keeps that helper's vocabulary check
    unaware of aliasing, since :func:`validate_levels` has none.

    Args:
        value: The raw, comma separated ``--source`` value, any case.

    Returns:
        The same items, comma separated, with any alias (matched
        case-insensitively) rewritten to its filter spelling. An item with no
        alias passes through unchanged, for :func:`_validate_vocabulary` to
        accept or refuse.
    """
    items = [SOURCE_ALIASES.get(item.lower(), item) for item in _split(value)]
    return ",".join(items)


def validate_sources(value: str) -> str:
    """Validate a ``--source`` list and return it as the API spells it.

    A display-only spelling such as ``serverless-middleware`` (see
    :data:`SOURCE_ALIASES`) is resolved to its filter spelling first, so a
    value copied out of this tool's own source column is accepted rather than
    refused.

    Args:
        value: One or more comma separated source names, any case; may
            include a display alias from :data:`SOURCE_ALIASES`.

    Returns:
        The lower-cased comma separated list to send, aliases resolved.

    Raises:
        ConfigError: When the list is empty or names a source that is neither
            in :data:`SOURCES` nor a key of :data:`SOURCE_ALIASES`. Same
            reasoning as :func:`validate_levels`: an unknown value is answered
            with zero rows. The message additionally names the alias, since
            the source column can display a spelling this filter does not
            accept.
    """
    try:
        return _validate_vocabulary(
            "source", "source", _resolve_source_aliases(value), SOURCES
        )
    except ConfigError as error:
        raise ConfigError(f"{error}. {SOURCE_ALIAS_NOTE}") from error


def validate_status_code(value: str) -> str:
    """Validate a ``--status-code`` expression against the API's own rule.

    Args:
        value: Comma separated status codes, classes such as ``4xx``, or
            ``None`` for requests with no status recorded.

    Returns:
        The expression to send, lower-cased for classes and with ``None``
        spelled the way the API spells it.

    Raises:
        ConfigError: When an item matches neither form. The message quotes the
            API's own validation text, since that is the authority.
    """
    items = _split(value)
    normalized: list[str] = []
    for item in items:
        if item.lower() == "none":
            normalized.append("None")
            continue
        lowered = item.lower()
        if _STATUS_ITEM_RE.match(lowered):
            normalized.append(lowered)
            continue
        raise ConfigError(
            f"--status-code {item!r} is not a status this API accepts. It says: "
            '"statusCode must contain only comma-separated integers, status code '
            'classes like 4xx or 5xx, or \\"None\\"". So --status-code 500, '
            "--status-code 5xx, --status-code 4xx,5xx and --status-code None all "
            "work; a comparison such as >=500 does not"
        )
    if not normalized:
        raise ConfigError(
            "--status-code was empty; pass a status such as 500, a class such as "
            "4xx or 5xx, or None for requests with no status recorded"
        )
    return ",".join(normalized)


def normalize_method(value: str) -> str:
    """Spell a ``--method`` value the way the API records one.

    Args:
        value: The method as the user typed it, with any surrounding space.

    Returns:
        The method upper-cased and stripped, which is how the API records it
        and therefore how it matches.
    """
    return value.strip().upper()


def method_warning(method: str) -> str | None:
    """Say when a method is outside the standard set, without refusing it.

    A custom verb is legal HTTP, so this warns rather than raising: refusing
    would remove capability. Silence is what is not acceptable, because this
    API answers a method it never recorded with HTTP 200 and zero rows, and
    zero rows reads as "nothing is broken" rather than as "nothing matched".

    Args:
        method: The method as :func:`normalize_method` spelled it.

    Returns:
        One line of warning text when ``method`` is not one of
        :data:`METHODS`, and ``None`` when it is.
    """
    if not method or method in METHODS:
        return None
    return (
        f"--method {method} is not one of the standard HTTP methods "
        f"({', '.join(METHODS)}); it is still sent, because a custom method is "
        "legal, but this API answers a method it never recorded with zero rows "
        "rather than with an error, so check the spelling before reading an "
        "empty answer as a quiet window"
    )


def validate_limit(limit: int) -> int:
    """Bound the number of log rows one run will report.

    Args:
        limit: The requested row count.

    Returns:
        The limit, unchanged, when it is in range.

    Raises:
        ConfigError: When it is outside :data:`MIN_LIMIT` to :data:`MAX_LIMIT`.
    """
    if MIN_LIMIT <= limit <= MAX_LIMIT:
        return limit
    raise ConfigError(
        f"--limit {limit} is out of range on a logs preset, which counts rows "
        f"rather than groups: pass {MIN_LIMIT} to {MAX_LIMIT}. The API pages "
        f"{PAGE_SIZE} rows at a time and ignores a limit of its own, so this "
        f"client stops after {MAX_PAGES} pages"
    )


# ---------------------------------------------------------------------------
# Request building
# ---------------------------------------------------------------------------

#: Every filter parameter this surface may send, in the order they are emitted.
#: This is a parameter allowlist as well as an ordering: a key outside it is a
#: ConfigError, so a caller cannot introduce a query parameter of its own.
FILTER_PARAMS: tuple[str, ...] = (
    "level",
    "statusCode",
    "source",
    "requestMethod",
    "requestPath",
    "route",
    "environment",
    "branch",
    "deploymentId",
    "requestId",
    "search",
)


def build_request(
    *,
    project: str,
    owner_id: str,
    since: datetime,
    until: datetime,
    page: int = 0,
    filters: Mapping[str, str] | None = None,
    token: str | None = None,
) -> PreparedRequest:
    """Build the request that fetches one page of request logs. Pure: no I/O.

    The URL comes from the ``request_logs`` entry of the operation allowlist, so
    neither the method nor the host is written down here. The token, when
    supplied, goes into the ``Authorization`` header and nowhere else.

    ``teamId`` is deliberately absent: this endpoint does not accept it, and
    ``ownerId`` is what scopes the call.

    Args:
        project: Project id or project name; both work on this endpoint.
        owner_id: Account that owns the project. Required by the API.
        since: Start of the window, aware.
        until: End of the window, aware.
        page: Zero based page index.
        filters: Wire-named filter values, keyed by :data:`FILTER_PARAMS`.
            Empty values are dropped rather than sent.
        token: Access token for the ``Authorization`` header.

    Returns:
        The :class:`PreparedRequest` describing exactly one allowlisted call.

    Raises:
        ConfigError: When ``filters`` carries a key outside
            :data:`FILTER_PARAMS`.
    """
    supplied = dict(filters or {})
    unknown = sorted(set(supplied) - set(FILTER_PARAMS))
    if unknown:
        raise ConfigError(
            f"{unknown[0]!r} is not a request logs filter; this surface sends "
            f"only {', '.join(FILTER_PARAMS)}"
        )

    params: list[tuple[str, str]] = [
        ("projectId", project),
        ("ownerId", owner_id),
        ("page", str(page)),
        ("startDate", to_unix_ms(since)),
        ("endDate", to_unix_ms(until)),
    ]
    for name in FILTER_PARAMS:
        value = supplied.get(name)
        if value:
            params.append((name, value))

    return PreparedRequest(
        operation=OPERATION,
        url=operation_url(OPERATION),
        params=params,
        headers=default_headers(token),
    )


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------


def _text(row: Mapping[str, Any], name: str) -> str:
    """One sanitized single-line string field, empty when absent."""
    value = row.get(name)
    if value is None or isinstance(value, (Mapping, list)):
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return sanitize_label(str(value))


def _number(row: Mapping[str, Any], name: str) -> float | None:
    """One numeric field, ``None`` when absent, non-numeric or not finite."""
    value = row.get(name)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value) if math.isfinite(float(value)) else None


def _status(row: Mapping[str, Any]) -> int | None:
    """The HTTP status, ``None`` when the API recorded none.

    A missing field and a value of zero or less are both read as absent rather
    than as a status. ``statusCode=None`` selects rows with no status recorded,
    so such rows exist; which of the two ways the API spells one was never
    probed, and reading both the same way cannot be wrong either way. See
    docs/api-notes.md, which marks this inferred rather than verified.
    """
    value = _number(row, "statusCode")
    if value is None or value <= 0:
        return None
    return int(value)


def _timestamp(row: Mapping[str, Any]) -> datetime | None:
    """The row's instant, ``None`` when it is missing or unparseable.

    Values arrive as ISO-8601 with a trailing ``Z``, which
    ``datetime.fromisoformat`` cannot read before Python 3.11, so the offset is
    spelled out first.
    """
    raw = row.get("timestamp")
    if not isinstance(raw, str) or not raw:
        return None
    candidate = raw[:-1] + "+00:00" if raw.endswith(("Z", "z")) else raw
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _lines(row: Mapping[str, Any]) -> tuple[LogLine, ...]:
    """Every application log line on this request, sanitized.

    ASSUMPTION: the item shape is ``{level, message, messageTruncated}``, taken
    from the Vercel CLI's own mapping code. No probe ever saw one populated,
    because neither test project had logged an error, so anything unexpected is
    skipped rather than trusted. See docs/api-notes.md.
    """
    raw = row.get("logs")
    if not isinstance(raw, list):
        return ()
    lines: list[LogLine] = []
    for item in raw:
        if not isinstance(item, Mapping):
            continue
        message = item.get("message")
        level = item.get("level")
        lines.append(
            LogLine(
                # Lower-cased and stripped because render.py ranks a level by an
                # exact key in LOG_LEVEL_SEVERITY: an "ERROR" or a padded
                # " error " that missed the table would score below "info", lose
                # the worst-line ranking, and leave is_error False for a request
                # that logged a stack trace.
                level=sanitize_label(str(level)).strip().lower() if level else "",
                message=sanitize_message(str(message)) if message else "",
                truncated=bool(item.get("messageTruncated")),
            )
        )
    return tuple(lines)


def _source(row: Mapping[str, Any]) -> str:
    """Where the request was served from, off the first event carrying a source.

    Not simply the first event: a real row can carry several, and the leading
    one need not name a source at all. docs/api-notes.md records it the same
    way.
    """
    events = row.get("events")
    if isinstance(events, list):
        for event in events:
            if isinstance(event, Mapping) and event.get("source"):
                return sanitize_label(str(event["source"]))
    return ""


def _region(row: Mapping[str, Any]) -> str:
    """The serving region, off the first event carrying one, else the client's.

    Same rule as :func:`_source`: the first event that actually names a region
    wins rather than the first event outright, and ``clientRegion`` is the
    fallback when no event names one.
    """
    events = row.get("events")
    if isinstance(events, list):
        for event in events:
            if isinstance(event, Mapping) and event.get("region"):
                return sanitize_label(str(event["region"]))
    return _text(row, "clientRegion")


def _entry(row: Mapping[str, Any]) -> LogEntry:
    """Turn one API row into a :class:`LogEntry`, sanitizing every string."""
    return LogEntry(
        request_id=_text(row, "requestId"),
        timestamp=_timestamp(row),
        status=_status(row),
        method=_text(row, "requestMethod"),
        path=_text(row, "requestPath"),
        route=_text(row, "route"),
        source=_source(row),
        environment=_text(row, "environment"),
        deployment_id=_text(row, "deploymentId"),
        duration_ms=_number(row, "requestDurationMs"),
        region=_region(row),
        error_code=_text(row, "errorCode"),
        branch=_text(row, "branch"),
        domain=_text(row, "domain"),
        trace_id=_text(row, "traceId"),
        crashed=bool(row.get("hasFunctionCrashed")),
        lines=_lines(row),
        raw=dict(row),
    )


def _scrub_json(value: Any, scrub: Callable[[str], str]) -> Any:
    """Return ``value`` with ``scrub`` applied to every string inside it.

    This surface is the only one whose rows are free text an application wrote,
    so it is the only one where a response can echo a string the caller never
    meant to publish. ``scrub`` is injected rather than named here: this module
    knows nothing about credentials, only that some strings must be rewritten
    before they become rows.

    Keys are rewritten as well as values, because ``--json`` prints the whole
    row back and a key is exactly as visible there as the string beside it. Two
    keys colliding under rewriting would lose a field rather than disclose one,
    which is the right direction to fail in.

    Args:
        value: Any decoded JSON value: a row, a nested object, a list, a scalar.
        scrub: The rewrite to apply to each string.

    Returns:
        A value of the same shape with every string passed through ``scrub``.
        Non-string scalars are returned unchanged.
    """
    if isinstance(value, str):
        return scrub(value)
    if isinstance(value, Mapping):
        return {
            _scrub_json(key, scrub): _scrub_json(item, scrub)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_scrub_json(item, scrub) for item in value]
    return value


def normalize(
    payload: Mapping[str, Any], *, scrub: Callable[[str], str] | None = None
) -> tuple[list[LogEntry], bool]:
    """Parse one page of request logs.

    Args:
        payload: The decoded response body.
        scrub: Applied to every string in every row before it becomes a
            :class:`LogEntry`, including the untouched copy kept in
            :attr:`LogEntry.raw` that ``--json`` prints. This is the one
            boundary at which it happens, so no renderer has to remember to.
            ``None`` leaves the rows exactly as they arrived.

    Returns:
        The page's entries in the order they arrived, and whether the API said
        more rows exist.

    Raises:
        ApiError: With code ``invalid_response`` when ``rows`` is present but is
            not a list of objects. Nothing is dropped silently: a shape this
            client cannot read is reported, because a quietly shortened list of
            errors is worse than an error message.
    """
    rows = payload.get("rows", [])
    if rows is None:
        rows = []
    if not isinstance(rows, list):
        raise ApiError(
            200,
            "invalid_response",
            "the request logs response carried 'rows' that was not a list; run "
            "with --json to see it",
        )
    entries: list[LogEntry] = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise ApiError(
                200,
                "invalid_response",
                "the request logs response carried a row that was not an "
                "object; run with --json to see it",
            )
        entries.append(_entry(_scrub_json(row, scrub) if scrub else row))
    return entries, bool(payload.get("hasMoreRows"))


# ---------------------------------------------------------------------------
# Paging, merging and error presets
# ---------------------------------------------------------------------------


def collect(
    call: Callable[[int], Mapping[str, Any]],
    *,
    limit: int,
    max_pages: int = MAX_PAGES,
    scrub: Callable[[str], str] | None = None,
) -> tuple[list[LogEntry], bool, int]:
    """Read pages until the row budget is met, and say whether more existed.

    The API pages :data:`PAGE_SIZE` rows at a time and ignores a ``limit`` of
    its own, so the budget is enforced here instead. Paging stops on whichever
    comes first: the budget being met, a page shorter than :data:`PAGE_SIZE`
    (the server has nothing else for this query, whatever ``hasMoreRows``
    claims), ``hasMoreRows`` being false, or ``max_pages`` being reached. The
    fetcher is injected so this loop is testable with no HTTP at all, and so
    this module still performs no I/O of its own.

    Args:
        call: Given a zero based page index, returns that page's payload.
        limit: How many rows the caller wants at most.
        max_pages: Hard ceiling on requests, defaulting to :data:`MAX_PAGES`.
            A page took up to six seconds against a live account, so the
            default is already 24 seconds against a 30 second per request
            timeout.
        scrub: Passed straight to :func:`normalize` for every page, so a caller
            that holds the request's headers can have its own credential
            rewritten out of anything a response echoes back.

    Returns:
        The entries, never more than ``limit``; whether rows were left
        behind; and how many pages were read.

    Raises:
        ApiError: Whatever :func:`normalize` raises for an unreadable page.
    """
    entries: list[LogEntry] = []
    has_more = False
    short_page = False
    pages = 0
    for page in range(max(1, max_pages)):
        payload = call(page)
        pages = page + 1
        page_entries, has_more = normalize(payload, scrub=scrub)
        entries.extend(page_entries)
        short_page = len(page_entries) < PAGE_SIZE
        if len(entries) >= limit or short_page or not has_more:
            break
    # A short page means nothing else exists for this query, whatever
    # hasMoreRows claims, so it never counts toward truncation on its own:
    # only rows already in hand beyond the budget, or a credible hasMoreRows
    # off a full sized page, make this a truncated answer.
    truncated = len(entries) > limit or (has_more and not short_page)
    return entries[:limit], truncated, pages


def merge(
    groups: Sequence[Sequence[LogEntry]], *, limit: int
) -> tuple[list[LogEntry], bool]:
    """Combine the results of several calls into one honest, ordered list.

    One request can arrive from more than one call: the errors preset's two
    filter sets both match a 5xx that also logged a stack trace. Entries are
    therefore deduplicated by request id, and the copy carrying more log
    lines wins, since the other copy would render with an empty message.

    Ordering is applied here rather than trusted from the server, so "newest
    first" is a property of this client. A row with no timestamp sorts last,
    and the request id breaks ties, so the output is deterministic.

    Args:
        groups: One sequence of entries per call.
        limit: How many rows to keep.

    Returns:
        The merged entries, newest first and never more than ``limit``; and
        whether anything was dropped.
    """
    best: dict[str, LogEntry] = {}
    anonymous: list[LogEntry] = []
    for group in groups:
        for entry in group:
            if not entry.request_id:
                # Without an id there is nothing to deduplicate on, and
                # dropping it would hide a request. Keep it.
                anonymous.append(entry)
                continue
            previous = best.get(entry.request_id)
            if previous is None or len(entry.lines) > len(previous.lines):
                best[entry.request_id] = entry

    merged = list(best.values()) + anonymous
    epoch = datetime(1, 1, 1, tzinfo=timezone.utc)
    merged.sort(
        key=lambda entry: (entry.timestamp or epoch, entry.request_id),
        reverse=True,
    )
    return merged[:limit], len(merged) > limit


#: The two filters that, supplied explicitly, replace the errors presets' own
#: definition of an error rather than narrowing it. Either one collapses the two
#: calls to one, and that one call asks the user's question instead of this
#: tool's: what came back is what the filter matched, error or not.
NARROWING_FILTERS: tuple[str, ...] = ("level", "statusCode")


def _narrowed_by(filters: Mapping[str, str]) -> list[str]:
    """Which of :data:`NARROWING_FILTERS` the user supplied, in a fixed order.

    Three decisions read this: whether to issue one call or two, what the header
    line above the table may claim, and whether the rows may be called errors at
    all. Stating the rule once is what keeps those three from disagreeing, which
    is exactly how the output came to print an error definition that did not
    describe the query it ran.

    Args:
        filters: The wire-named filters the user asked for.

    Returns:
        The narrowing filter names present with a non-empty value, in the order
        :data:`NARROWING_FILTERS` lists them; empty when the errors presets are
        free to run their own two-call query.
    """
    return [name for name in NARROWING_FILTERS if filters.get(name)]


def _is_two_call(filters: Mapping[str, str]) -> bool:
    """Whether the errors preset's two-call merge rule applies to ``filters``.

    :func:`error_filter_sets` and :func:`build_report` both need to agree on
    this: the former decides whether to actually issue two calls, and the
    latter decides whether to caveat a truncated answer as "the most recent N
    of each kind" rather than a global top N. Stating the rule once here,
    rather than once in each, is what keeps them from drifting apart.

    Args:
        filters: The wire-named filters the user asked for.

    Returns:
        True when neither ``level`` nor ``statusCode`` was supplied, meaning
        the errors preset queries both and merges the results; false when an
        explicit ``--level`` or ``--status-code`` already narrowed the query
        to one call.
    """
    return not _narrowed_by(filters)


def error_filter_sets(filters: Mapping[str, str]) -> list[dict[str, str]]:
    """The filter sets the errors preset queries with.

    Two calls, because ``level`` matches application log lines and
    ``statusCode`` matches responses, and an error can show up as either: a
    5xx that printed nothing is invisible to ``level``, and a 200 whose
    handler logged a stack trace is invisible to ``statusCode``. An explicit
    ``--level`` or ``--status-code`` collapses this to one call, the same "an
    explicit flag overrides a preset value" rule the rest of this tool
    follows.

    Args:
        filters: The wire-named filters the user asked for.

    Returns:
        One filter mapping when the user already narrowed by level or status;
        otherwise two, each a complete filter set for one call.
    """
    if not _is_two_call(filters):
        return [dict(filters)]
    return [
        {**filters, "statusCode": "5xx"},
        {**filters, "level": ",".join(ERROR_LEVELS)},
    ]


# ---------------------------------------------------------------------------
# Local aggregation
# ---------------------------------------------------------------------------

#: The message group for a request that failed without logging anything.
NO_LOG_LINE = "(no log line)"


def summarize(entries: Sequence[LogEntry]) -> LogSummary:
    """Tally a merged list of entries three ways, for the error-summary preset.

    Grouping is deliberately literal: statuses by their own number, routes by
    their pattern, messages by their exact text. Clustering messages by a
    guessed pattern would merge two different bugs into one row, which is a
    worse answer than three rows.

    Args:
        entries: The merged entries, in any order.

    Returns:
        The tallies, each ordered by count and then by name so the output is
        stable across runs. ``logged_only`` counts entries that are errors
        only because they logged an error or fatal line: a non-5xx response
        that did not crash and did carry such a line. All three conditions are
        checked, so the count means what the sentence built from it says even
        when the entries were never narrowed to errors at all.
    """
    status_counts: dict[str, int] = {}
    routes: dict[str, list[LogEntry]] = {}
    messages: dict[str, list[LogEntry]] = {}
    logged_only = 0

    for entry in entries:
        status = str(entry.status) if entry.status is not None else "(none)"
        status_counts[status] = status_counts.get(status, 0) + 1
        routes.setdefault(entry.label, []).append(entry)
        messages.setdefault(entry.headline or NO_LOG_LINE, []).append(entry)
        # The log line is the point of this count, not an afterthought: a
        # non-5xx that never printed anything is not an error at all, and
        # counting it here made the output claim a log line the message table
        # beside it showed as "(no log line)". Any error or fatal line makes
        # this the worst level, so the worst level is the whole test.
        if (
            (entry.status is None or entry.status < 500)
            and not entry.crashed
            and entry.worst_level in ERROR_LEVELS
        ):
            logged_only += 1

    def seen(group: Sequence[LogEntry]) -> tuple[datetime | None, datetime | None]:
        stamps = sorted(item.timestamp for item in group if item.timestamp is not None)
        return (stamps[0], stamps[-1]) if stamps else (None, None)

    def worst(group: Sequence[LogEntry]) -> int | None:
        found = [item.status for item in group if item.status is not None]
        return max(found) if found else None

    route_tallies: list[RouteTally] = []
    for route, group in sorted(
        routes.items(), key=lambda item: (-len(item[1]), item[0])
    ):
        first_seen, last_seen = seen(group)
        route_tallies.append(
            RouteTally(
                route=route,
                count=len(group),
                worst_status=worst(group),
                first_seen=first_seen,
                last_seen=last_seen,
            )
        )
    by_route = tuple(route_tallies)

    message_tallies: list[MessageTally] = []
    for message, group in sorted(
        messages.items(), key=lambda item: (-len(item[1]), item[0])
    ):
        first_seen, last_seen = seen(group)
        message_tallies.append(
            MessageTally(
                message=message,
                count=len(group),
                first_seen=first_seen,
                last_seen=last_seen,
            )
        )
    by_message = tuple(message_tallies)
    by_status = tuple(
        sorted(status_counts.items(), key=lambda item: (-item[1], item[0]))
    )
    return LogSummary(
        total=len(entries),
        by_status=by_status,
        by_route=by_route,
        by_message=by_message,
        logged_only=logged_only,
    )


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

#: What the errors presets count, stated in the output so the reader is never
#: guessing. Both halves matter: see the module docstring. Printed only when the
#: presets actually got to apply it, which an explicit ``--level`` or
#: ``--status-code`` prevents: see :func:`_header_note`.
ERROR_DEFINITION = (
    "Counted as an error: a 5xx response, a crashed function, or a request "
    "that logged an error or fatal line."
)

#: Read from https://vercel.com/docs/runtime-logs on 2026-08-17. Printed when a
#: query came back empty over a window longer than the shortest retention, so an
#: empty answer is never mistaken for a healthy one.
RETENTION_NOTE = (
    "Runtime log retention is 1 hour on Hobby, 1 day on Pro, 3 days on "
    "Enterprise and 30 days with Observability Plus, so an empty result over a "
    "longer window can mean the logs aged out rather than that nothing failed."
)

#: The shortest retention any plan has. Below this there is nothing to warn
#: about, and a warning on every empty answer trains the reader to ignore it.
SHORTEST_RETENTION = timedelta(hours=1)


def _leading_route(tallies: Sequence[RouteTally]) -> RouteTally | None:
    """The route that actually leads the ranking, or ``None`` when none does.

    Args:
        tallies: The per route tallies, already ordered by count then name.

    Returns:
        The first tally when it outnumbers the second, and ``None`` otherwise.
        One route on its own leads nothing, since there is no ranking to lead,
        and two routes tied at the top mean the ranking has no winner: printing
        the first of them as "most affected" would report the alphabetical
        accident that broke the tie as a finding.
    """
    if len(tallies) < 2:
        return None
    return tallies[0] if tallies[0].count > tallies[1].count else None


def _header_note(*, counts_errors: bool, filters: Mapping[str, str]) -> str | None:
    """The line above the table saying what the rows in it are.

    An errors preset with no ``--level`` and no ``--status-code`` applies its own
    definition of an error, and :data:`ERROR_DEFINITION` states it. An explicit
    one of either replaces that definition rather than narrowing it: the preset
    collapses to a single call carrying the user's filter, so what comes back is
    whatever that filter matched, which may include a 401 this tool would never
    call an error. Printing the definition there would describe a query that did
    not run, and the table underneath would disprove it.

    Args:
        counts_errors: True for the presets that go looking for failures.
        filters: The wire-named filters the user asked for.

    Returns:
        :data:`ERROR_DEFINITION` for an errors preset running its own query, a
        note naming the filter that ran instead when one narrowed it, and
        ``None`` for a preset that never claimed to be counting errors.
    """
    if not counts_errors:
        return None
    narrowed = _narrowed_by(filters)
    if not narrowed:
        return ERROR_DEFINITION
    shown = " and ".join(f"{name} {filters[name]}" for name in narrowed)
    return (
        f"These rows are what {shown} matched: your filter chose them, not "
        "this tool's own error query. An explicit --level or --status-code "
        "replaces the error definition rather than narrowing it."
    )


def _window_prose(time_range: tuple[datetime, datetime]) -> str:
    """The window as a person says it: "30 minutes", "6 hours", "3 days"."""
    span = time_range[1] - time_range[0]
    minutes = int(round(span.total_seconds() / 60))
    if minutes < 60:
        return f"{minutes} minute{'' if minutes == 1 else 's'}"
    hours = span.total_seconds() / 3600
    if hours < 48:
        rounded = int(round(hours))
        return f"{rounded} hour{'' if rounded == 1 else 's'}"
    days = int(round(hours / 24))
    return f"{days} day{'' if days == 1 else 's'}"


def build_report(
    entries: Sequence[LogEntry],
    *,
    time_range: tuple[datetime, datetime],
    project_label: str,
    preset: str,
    filters: Mapping[str, str],
    truncated: bool,
    pages_fetched: int,
    requested_limit: int,
    counts_errors: bool,
) -> LogReport:
    """Wrap entries in everything needed to print them honestly.

    Every sentence the output adds beyond the table is composed here: what
    counted as an error, how many there were, what was left out, and what an
    empty answer does not prove. ``render.py`` only lays out what it is given.

    Args:
        entries: The merged entries, newest first.
        time_range: The resolved window.
        project_label: How to name what was queried.
        preset: The preset name, shown in the title.
        filters: The filters the user asked for, wire-named.
        truncated: Whether any call left rows behind.
        pages_fetched: How many requests were spent.
        requested_limit: The row budget that was in force.
        counts_errors: True for the presets that filter to failures.

    Returns:
        The report, ready to render in any format.
    """
    window = _window_prose(time_range)
    notes: list[str] = []
    hint: str | None = None

    if entries:
        summary = summarize(entries)
        # Only a preset that got to apply its own error definition may call
        # these rows errors. Narrowed by an explicit --level or --status-code,
        # the rows are whatever that filter matched, and a 401 among them is
        # not an error by any definition this tool holds.
        counted_as_errors = counts_errors and _is_two_call(filters)
        noun = "error" if counted_as_errors else "request"
        plural = "" if summary.total == 1 else "s"
        breakdown = ", ".join(
            f"{count} x {status}" for status, count in summary.by_status
        )
        if truncated:
            # A truncated report holds a sample, so the sentence counts what is
            # on screen. "5 requests in 30 minutes" over the 5 most recent of
            # more that matched describes a window nobody queried.
            notes.append(
                f"Showing the most recent {summary.total} of more {noun}s that "
                f"matched in {window}: {breakdown}."
            )
        else:
            notes.append(f"{summary.total} {noun}{plural} in {window}: {breakdown}.")
        leader = _leading_route(summary.by_route)
        if leader is not None:
            # Ranked over the rows shown, which on a truncated report is the most
            # recent N rather than the window: a ranking read off a sample is
            # only about the sample, and saying otherwise invents a finding.
            scope = " among the rows shown" if truncated else ""
            notes.append(
                f"Most affected route{scope}: {leader.route} ({leader.count})."
            )
        if counts_errors and summary.logged_only:
            # summarize checks for the log line itself, so this sentence is
            # about rows that really carry one. It said the opposite for every
            # non-5xx row while that check was missing.
            notes.append(
                f"{summary.logged_only} of them returned a non-5xx status and "
                "count as errors only because they logged an error or fatal line."
            )
        hint = (
            "Add --expand for full messages, or --request-id to pull one request "
            "apart."
        )

    if truncated:
        # The error-summary preset already asks for MAX_LIMIT, so "raise --limit"
        # is advice its reader cannot follow. Only offer it where there is room.
        if requested_limit < MAX_LIMIT:
            remedy = f"Raise --limit (up to {MAX_LIMIT}) or narrow the window."
        else:
            remedy = (
                f"{MAX_LIMIT} rows is all this surface will fetch, so narrow the "
                "window with --since, or filter with --route or --status-code."
            )
        # How many were kept is the count sentence's job now, so this one carries
        # the fact and the remedy rather than repeating the number.
        notes.append(f"More rows matched than were shown. {remedy}")
        if counts_errors and _is_two_call(filters):
            notes.append(
                "Both filters were paging, so this is the most recent "
                f"{requested_limit} of each kind rather than a global top "
                f"{requested_limit}."
            )

    if not entries and time_range[1] - time_range[0] > SHORTEST_RETENTION:
        notes.append(RETENTION_NOTE)

    return LogReport(
        entries=list(entries),
        time_range=time_range,
        project_label=project_label,
        preset=preset,
        window_label=window,
        filters=dict(filters),
        truncated=truncated,
        pages_fetched=pages_fetched,
        requested_limit=requested_limit,
        header_note=_header_note(counts_errors=counts_errors, filters=filters),
        notes=tuple(notes),
        hint=hint,
    )
