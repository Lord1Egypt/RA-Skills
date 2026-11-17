"""Web Analytics request building and response normalization.

Everything specific to ``GET /v1/query/web-analytics/{dataset}/{endpoint}``
lives here: the dataset vocabulary, its dimension names, its metric names, and
the shape of the rows it returns. The modules underneath (``http``, ``odata``,
``timerange``, ``render``) know none of it, so a second surface can reuse them
without modification.
"""

from __future__ import annotations

import difflib
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, TypeGuard

from . import OTHERS_LABEL, ApiError, ConfigError, sanitize_label
from .http import PreparedRequest, default_headers, operation_url
from .odata import validate_key_segments
from .render import Result, Row
from .render import stringify_label as _stringify
from .timerange import TIME_GRANULARITIES, to_api_timestamp

#: The operation key this surface uses. It is a key into ``http.OPERATIONS``,
#: never a method and never a host.
OPERATION = "web_analytics"

#: The two datasets this API exposes.
DATASETS: tuple[str, ...] = ("visits", "events")

#: Plain dimensions accepted by both datasets.
PLAIN_DIMENSIONS: tuple[str, ...] = (
    "country",
    "deviceType",
    "environment",
    "requestPath",
    "referrerHostname",
    "osName",
    "browserName",
    "route",
    "utmSource",
    "utmMedium",
    "utmCampaign",
    "utmContent",
    "utmTerm",
)

#: JSON dimensions, mapped to the datasets that accept them. Used bare they
#: group by key name; used as ``base/key`` they group by that key's value.
JSON_DIMENSIONS: dict[str, tuple[str, ...]] = {
    "flags": ("visits", "events"),
    "eventData": ("events",),
}

VISIT_DIMENSIONS: tuple[str, ...] = TIME_GRANULARITIES + PLAIN_DIMENSIONS + ("flags",)

EVENT_DIMENSIONS: tuple[str, ...] = (
    TIME_GRANULARITIES + PLAIN_DIMENSIONS + ("eventName", "flags", "eventData")
)

#: Metric keys each dataset returns, primary metric first.
DATASET_METRICS: dict[str, tuple[str, ...]] = {
    "visits": ("pageviews", "visitors"),
    "events": ("count", "visitors"),
}

#: Every metric key this client recognises while parsing rows.
KNOWN_METRICS: frozenset[str] = frozenset(
    name for names in DATASET_METRICS.values() for name in names
)

#: Speed Insights spellings, mapped to the Web Analytics name for the same
#: thing. That API is snake_case and this one is camelCase, so a dimension
#: name is not portable between them and the fix is worth naming outright.
#: Written here rather than imported so this module stays free of a dependency
#: on the other surface.
SPEED_INSIGHTS_DIMENSIONS: dict[str, str | None] = {
    "request_path": "requestPath",
    "device_type": "deviceType",
    "project_id": None,
}

MIN_LIMIT = 1
MAX_LIMIT = 100
DEFAULT_LIMIT = 10
MAX_GROUP_BY = 2


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def dimensions_for(dataset: str) -> tuple[str, ...]:
    """Every grouping dimension name valid on ``dataset``."""
    return EVENT_DIMENSIONS if dataset == "events" else VISIT_DIMENSIONS


def validate_dimension(dimension: str, dataset: str) -> str:
    """Validate one grouping dimension against a dataset.

    Handles the JSON dimensions (``flags``, ``eventData``) including their
    ``base/key`` form and the quoting rule for keys with punctuation.

    Args:
        dimension: The dimension as the user wrote it.
        dataset: Either ``visits`` or ``events``.

    Returns:
        The dimension, unchanged, when it is valid.

    Raises:
        ConfigError: With the offending value and the fix.
    """
    name = dimension.strip()
    if not name:
        raise ConfigError(
            "empty grouping dimension; pass a name such as --group-by requestPath"
        )

    if "/" in name:
        base, _, key = name.partition("/")
        if base not in JSON_DIMENSIONS:
            raise ConfigError(
                f"unknown JSON dimension {base!r} in {name!r}; the JSON dimensions "
                f"are {', '.join(sorted(JSON_DIMENSIONS))}"
            )
        if dataset not in JSON_DIMENSIONS[base]:
            raise ConfigError(
                f"{name!r} is only available on the events dataset; add "
                "--dataset events (or use the events preset)"
            )
        if not key:
            raise ConfigError(
                f"{name!r} is missing a key; use {base}/<key>, for example "
                f"{base}/plan, or drop the slash to group by key name"
            )
        validate_key_segments(base, name, key)
        return name

    valid = dimensions_for(dataset)
    if name in valid:
        return name

    if name in SPEED_INSIGHTS_DIMENSIONS:
        equivalent = SPEED_INSIGHTS_DIMENSIONS[name]
        if equivalent is not None:
            raise ConfigError(
                f"{name!r} is the Speed Insights spelling; the Web Analytics API "
                f"uses camelCase, so group by {equivalent!r} instead"
            )
        raise ConfigError(
            f"{name!r} is a Speed Insights dimension and has no Web Analytics "
            "equivalent; a Web Analytics query already names its project, so "
            "there is nothing to group by there"
        )

    other = EVENT_DIMENSIONS if dataset == "visits" else VISIT_DIMENSIONS
    if name in other:
        raise ConfigError(
            f"{name!r} is only available on the events dataset; add --dataset "
            "events (or use the events preset)"
        )

    suggestions = difflib.get_close_matches(name, valid, n=1, cutoff=0.6)
    hint = f" Did you mean {suggestions[0]!r}?" if suggestions else ""
    raise ConfigError(
        f"unknown dimension {name!r} for the {dataset} dataset.{hint} "
        f"Valid dimensions: {', '.join(valid)}, plus flags/<name>"
        + (", eventData/<property>" if dataset == "events" else "")
    )


def validate_group_by(dimensions: Sequence[str], dataset: str) -> list[str]:
    """Validate a whole grouping: each dimension, the count, and the time rule.

    Args:
        dimensions: The grouping in request order.
        dataset: Either ``visits`` or ``events``.

    Returns:
        The validated grouping as a list.

    Raises:
        ConfigError: On an unknown dimension, a repeat, more than one time
            granularity, or more than :data:`MAX_GROUP_BY` dimensions.
    """
    validated = [validate_dimension(dimension, dataset) for dimension in dimensions]

    seen: set[str] = set()
    for dimension in validated:
        if dimension in seen:
            raise ConfigError(
                f"dimension {dimension!r} is grouped by twice; remove the repeat "
                "(--granularity also adds a time dimension)"
            )
        seen.add(dimension)

    granularities = [dim for dim in validated if dim in TIME_GRANULARITIES]
    if len(granularities) > 1:
        raise ConfigError(
            "a query may use at most one time granularity, but this one uses "
            f"{', '.join(granularities)}; the granularities are "
            f"{', '.join(TIME_GRANULARITIES)}, so keep one of them"
        )

    if len(validated) > MAX_GROUP_BY:
        raise ConfigError(
            f"grouping by {len(validated)} dimensions ({', '.join(validated)}) "
            f"exceeds the API maximum of {MAX_GROUP_BY}; drop "
            f"{len(validated) - MAX_GROUP_BY} of them"
        )

    return validated


def select_endpoint(group_by: Sequence[str]) -> str:
    """Pick the endpoint for a grouping: ``aggregate`` when there is one."""
    return "aggregate" if list(group_by) else "count"


def validate_limit(limit: int) -> int:
    """Check ``--limit`` against the API bounds.

    Raises:
        ConfigError: When outside ``1..100``, explaining the overflow bucket.
    """
    if limit < MIN_LIMIT or limit > MAX_LIMIT:
        raise ConfigError(
            f"--limit {limit} is outside the API bounds of {MIN_LIMIT} to "
            f"{MAX_LIMIT}; pick a value in that range, and note that groups past "
            f"the limit are not dropped, they roll into a single {OTHERS_LABEL!r} row"
        )
    return limit


# ---------------------------------------------------------------------------
# Request building
# ---------------------------------------------------------------------------


def build_request(
    *,
    dataset: str,
    project: str,
    since: datetime,
    until: datetime,
    group_by: Sequence[str] = (),
    limit: int | None = None,
    filter_expr: str | None = None,
    team: str | None = None,
    team_slug: str | None = None,
    token: str | None = None,
) -> PreparedRequest:
    """Build the request that answers one query. Pure: it performs no I/O.

    The URL comes from the ``web_analytics`` entry of the operation allowlist,
    so neither the method nor the host is written down here. The token, when
    supplied, goes into the ``Authorization`` header and nowhere else. ``limit``
    is only meaningful on the aggregate endpoints, so it is dropped for count
    queries rather than silently sent and ignored.

    Args:
        dataset: ``visits`` or ``events``.
        project: Project id or project name.
        since: Start of the window, aware.
        until: End of the window, aware.
        group_by: Validated grouping; empty selects the count endpoint.
        limit: Maximum number of groups, aggregate only.
        filter_expr: A combined OData expression, or ``None``.
        team: Team id, mutually exclusive with ``team_slug``.
        team_slug: Team slug, sent as ``slug``.
        token: Access token for the ``Authorization`` header.

    Returns:
        The :class:`PreparedRequest` describing exactly one allowlisted call.
    """
    dimensions = list(group_by)
    endpoint = select_endpoint(dimensions)
    url = operation_url(OPERATION, dataset=dataset, endpoint=endpoint)

    params: list[tuple[str, str]] = [("projectId", project)]
    for dimension in dimensions:
        params.append(("by", dimension))
    params.append(("since", to_api_timestamp(since)))
    params.append(("until", to_api_timestamp(until)))
    if endpoint == "aggregate" and limit is not None:
        params.append(("limit", str(limit)))
    if filter_expr:
        params.append(("filter", filter_expr))
    if team:
        params.append(("teamId", team))
    if team_slug:
        params.append(("slug", team_slug))

    return PreparedRequest(
        operation=OPERATION,
        url=url,
        params=params,
        headers=default_headers(token),
    )


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------


def _is_number(value: Any) -> TypeGuard[float]:
    """True for a real JSON number. Booleans are not numbers for our purposes."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def normalize(
    payload: Mapping[str, Any],
    dataset: str,
    group_by: Sequence[str],
    *,
    status: int = 200,
) -> Result:
    """Turn a raw response into a :class:`Result`.

    Parsing is deliberately permissive. The published JSON Schema marks roughly
    300 row fields as required, which is a generation artifact of a shared
    internal row type rather than a description of real responses, so this
    reads the metric keys it knows, treats the remaining string valued key as
    the group label, and requires nothing else.

    Grouping by a JSON dimension is the one trap that needs care: asking for
    ``eventData/plan`` returns rows keyed ``eventData``, and ``flags/x`` returns
    rows keyed ``flags``, so the base key is mapped back onto the dimension the
    caller actually asked for. That remap runs for every grouped dimension, so
    a two dimension grouping keeps both labels.

    Only the top level shape is strict. Which endpoint answered is decided by
    the requested grouping alone, never by the shape that came back, so a body
    that does not match its endpoint is an error rather than something quietly
    reinterpreted as a different kind of result.

    Args:
        payload: The decoded response body.
        dataset: ``visits`` or ``events``, which decides the metric names.
        group_by: The grouping that was requested.
        status: The HTTP status the body arrived with, used in the error when
            the shape is wrong. Only 2xx bodies ever reach this function.

    Returns:
        A :class:`Result` ready to format.

    Raises:
        ApiError: When ``data`` is not the shape the chosen endpoint must
            return: a mapping for count, a list of rows for aggregate.
    """
    dimensions = list(group_by)
    query = payload.get("query")
    query_block: dict[str, Any] = dict(query) if isinstance(query, Mapping) else {}
    data = payload.get("data")

    preferred = DATASET_METRICS.get(dataset, DATASET_METRICS["visits"])
    label_dimensions = [dim for dim in dimensions if dim not in TIME_GRANULARITIES]

    if select_endpoint(dimensions) == "count":
        if not isinstance(data, Mapping):
            raise ApiError(status, "invalid_response", _shape_error("count", data))
        metrics, names = _extract_metrics(data, preferred, skip=set())
        return Result(
            rows=[Row(metrics=metrics)],
            is_count=True,
            dataset=dataset,
            group_by=dimensions,
            query=query_block,
            metric_names=names,
            fallback_metrics=preferred,
        )

    if not isinstance(data, list):
        raise ApiError(status, "invalid_response", _shape_error("aggregate", data))

    rows: list[Row] = []
    metric_names: list[str] = []
    for entry in data:
        if not isinstance(entry, Mapping):
            continue
        row, names = _normalize_row(entry, preferred, label_dimensions)
        rows.append(row)
        for name in names:
            if name not in metric_names:
                metric_names.append(name)

    if not metric_names:
        metric_names = list(preferred)

    return Result(
        rows=rows,
        is_count=False,
        dataset=dataset,
        group_by=dimensions,
        query=query_block,
        metric_names=metric_names,
        fallback_metrics=preferred,
    )


def _shape_error(endpoint: str, data: Any) -> str:
    """Describe a top level ``data`` that is not what the endpoint must return.

    Only the shape is named, never the content, so nothing from the response
    body is echoed back out.
    """
    expected = (
        "a JSON object of metrics"
        if endpoint == "count"
        else "a JSON array of grouped rows"
    )
    if data is None:
        found = "it was missing or null"
    else:
        found = f"it was a {type(data).__name__}"
    return (
        f"the {endpoint} response should carry {expected} under 'data', but "
        f"{found}; the request succeeded, so this is a response the client "
        "cannot interpret rather than an empty result"
    )


def _fallback_label_key(entry: Mapping[str, Any], consumed: set[str]) -> str | None:
    """The first unclaimed string valued field that is not a metric.

    Defensive only: it labels a row whose grouping key came back under a name
    this client did not ask for, which the docs warn can happen.
    """
    for name, value in entry.items():
        if name == "timestamp" or name in KNOWN_METRICS or name in consumed:
            continue
        if isinstance(value, str):
            return name
    return None


def _normalize_row(
    entry: Mapping[str, Any],
    preferred: Sequence[str],
    label_dimensions: Sequence[str],
) -> tuple[Row, list[str]]:
    """Turn one raw row into a :class:`Row` plus the metric names it carried.

    One label cell is produced per grouped dimension. Each dimension claims the
    field named after it, or after its JSON base (``eventData/plan`` arrives as
    ``eventData``); whatever is still unlabelled afterwards falls back to any
    remaining string field, so nothing is silently dropped.
    """
    raw_timestamp = entry.get("timestamp")
    # A bucket label is remote input like any other, and it is rendered in the
    # same table cell, so it goes through the same sanitizer.
    timestamp = sanitize_label(raw_timestamp) if isinstance(raw_timestamp, str) else None

    consumed: set[str] = set()
    claimed: list[str | None] = []
    for dimension in label_dimensions:
        chosen: str | None = None
        for candidate in (dimension, dimension.split("/", 1)[0]):
            if candidate in entry and candidate not in consumed:
                chosen = candidate
                break
        if chosen is not None:
            consumed.add(chosen)
        claimed.append(chosen)

    for index, chosen in enumerate(claimed):
        if chosen is not None:
            continue
        fallback = _fallback_label_key(entry, consumed)
        if fallback is not None:
            consumed.add(fallback)
        claimed[index] = fallback

    labels = tuple(
        _stringify(entry[name]) if name is not None else None for name in claimed
    )

    metrics, names = _extract_metrics(entry, preferred, skip={"timestamp"} | consumed)
    is_others = OTHERS_LABEL in labels or timestamp == OTHERS_LABEL
    return (
        Row(labels=labels, metrics=metrics, timestamp=timestamp, is_others=is_others),
        names,
    )


def _extract_metrics(
    entry: Mapping[str, Any],
    preferred: Sequence[str],
    skip: set[str],
) -> tuple[dict[str, float], list[str]]:
    """Pull numeric metrics out of a row, known names first, extras after.

    An extra name is whatever key the response happened to carry, and it becomes
    a table column header and a CSV header cell, so it is sanitized for the same
    reason a label is. The preferred names are our own constants and need no
    such treatment, but they go through the same call so no future edit can
    reintroduce the gap by reordering these loops.
    """
    metrics: dict[str, float] = {}
    names: list[str] = []
    for name in preferred:
        value = entry.get(name)
        if _is_number(value):
            metrics[name] = value
            names.append(name)
    for name, value in entry.items():
        if name in skip or name in metrics or not _is_number(value):
            continue
        safe_name = sanitize_label(name)
        metrics[safe_name] = value
        names.append(safe_name)
    return metrics, names
