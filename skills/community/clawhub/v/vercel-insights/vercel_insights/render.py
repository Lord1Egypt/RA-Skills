"""Rows, results and every output format: table, JSON, CSV, overview and vitals.

Surface agnostic: a :class:`Result` carries everything the renderers need, so
nothing here has to know which API produced it. In particular a result names
its own metrics, its own fallback metric names, and, when it came from Speed
Insights, its metric id, human label, unit and published target, rather than
looking any of that up in a per-surface table. That is what keeps this module
free of an import back into a surface module.

Two conventions differ between the surfaces, and a :class:`Result` says which
one applies rather than the renderer guessing:

* ``additive``. Page views add up, so a Web Analytics table carries a totals
  row and a share of total column. A percentile does not add up: summing the
  P75 of six countries is meaningless, so a Speed Insights table has neither.
* ``unit``. A page view count is a bare number. A web vital is milliseconds or
  a unitless score, and is rendered accordingly.
"""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from . import OTHERS_LABEL, sanitize_label
from .timerange import (
    GRANULARITY_ALIASES,
    TIME_GRANULARITIES,
    format_timestamp,
    to_api_timestamp,
)

#: Number of table rows the overview preset shows per section.
OVERVIEW_TABLE_LIMIT = 5

#: Units a metric value can carry. ``ms`` is milliseconds, ``score`` is the
#: unitless layout shift score, ``count`` is a number of collected data points.
UNIT_MS = "ms"
UNIT_SCORE = "score"
UNIT_COUNT = "count"

#: The metric key under which a result carries its data point count, when the
#: response supplied one.
DATA_POINTS_METRIC = "data_points"

#: Below this many milliseconds a value reads better in milliseconds; at or
#: above it, seconds with one decimal.
MS_TO_SECONDS_THRESHOLD = 1000.0

VERDICT_MEETS = "meets target"
VERDICT_OVER = "over target"
VERDICT_UNKNOWN = "no published target"

#: Printed under every Speed Insights table. Vercel publishes one "good"
#: target per metric and no upper bound above it, so the verdict is two tier;
#: the dashboard's three colour bands describe derived 0 to 100 scores, not
#: raw values, and are deliberately not reproduced here.
DATA_POINTS_LEGEND: tuple[str, ...] = (
    "These are data point counts, not metric values: one data point is one "
    "measurement of one web vital during one visit, and a visit produces up to "
    "six.",
    "They are what makes a percentile trustworthy, so a group with few of them "
    "is not comparable to one with many.",
)

#: Printed under every Speed Insights table. Vercel publishes one "good"
#: target per metric and no upper bound above it, so the verdict is two tier;
#: the dashboard's three colour bands describe derived 0 to 100 scores, not
#: raw values, and are deliberately not reproduced here.
VITALS_LEGEND: tuple[str, ...] = (
    "Lower is better for all five metrics.",
    "The target is Vercel's published 'good' threshold, so the verdict is two "
    "tier: meets target or over target.",
)

#: Printed only when a data point count is actually shown. Explaining a column
#: that is not on screen sends the reader looking for something that is not
#: there, so this is appended rather than always included.
DATA_POINTS_NOTE = (
    "A percentile over few data points is not comparable to one over many, so "
    "read the value next to its data point count."
)

#: Log levels ordered by severity, so the worst line on a request can be picked
#: without a surface module having to rank them. The names are validated in
#: logs.py; tests/test_logs.py asserts the two agree.
LOG_LEVEL_SEVERITY: dict[str, int] = {
    "info": 0,
    "warning": 1,
    "error": 2,
    "fatal": 3,
}

#: The levels that make a request an error rather than a note, in the order they
#: are sent as a filter. Defined here because LogEntry.is_error needs them and
#: this module must not import a surface module; a later task has logs.py
#: import them from here, so there will be one definition rather than two that
#: can drift.
ERROR_LEVELS: tuple[str, ...] = ("error", "fatal")


# ---------------------------------------------------------------------------
# The untrusted-input boundary
# ---------------------------------------------------------------------------

# ``sanitize_label`` lives in the package root so that every layer can reach it,
# including :mod:`vercel_insights.http`, which has to scrub a ``Location`` header
# and a server supplied error message before either reaches a terminal. It is
# re-exported here because this module is where labels are rendered.


def stringify_label(value: Any) -> str:
    """Render a group label that may be a string, number, bool or null.

    This is the single boundary at which a response value becomes a label:
    both surfaces normalize through it, so the table, CSV, JSON, overview and
    vitals renderers all inherit :func:`sanitize_label` without repeating it.
    """
    if value is None:
        return "(none)"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return sanitize_label(value) or "(empty)"
    return sanitize_label(str(value))


# ---------------------------------------------------------------------------
# Result containers, shared by both analytics surfaces
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Row:
    """One result row: its group labels, its metrics, and an optional bucket.

    ``labels`` holds one cell per non-time grouping dimension, in the order the
    dimensions were requested, so a two dimension grouping keeps both values.
    ``key`` is the convenience accessor for the common single label case.
    """

    labels: tuple[str | None, ...] = ()
    metrics: dict[str, float] = field(default_factory=dict)
    timestamp: str | None = None
    #: True for the bucket the API uses to collapse limit overflow. This is a
    #: field rather than a comparison against ``key`` because a time-only
    #: grouping carries the overflow marker on the timestamp instead.
    is_others: bool = False

    @property
    def key(self) -> str | None:
        """The first group label, or ``None`` when the row carries none."""
        return self.labels[0] if self.labels else None


@dataclass(frozen=True)
class Result:
    """A parsed response: rows plus the context needed to render them."""

    rows: list[Row]
    is_count: bool
    dataset: str
    group_by: list[str]
    query: dict[str, Any]
    metric_names: list[str]
    #: The metric names to fall back on when a response carried none, supplied
    #: by whichever surface parsed it. Keeping it on the result is what lets
    #: this module render any surface without importing one.
    fallback_metrics: tuple[str, ...] = ()
    #: The queried metric id, for a surface that queries one metric at a time.
    metric: str | None = None
    #: That metric's human label, for example ``Largest Contentful Paint``.
    metric_label: str | None = None
    #: :data:`UNIT_MS`, :data:`UNIT_SCORE` or :data:`UNIT_COUNT`; ``None`` for
    #: a plain count that needs no unit.
    unit: str | None = None
    #: The published target for the metric, in its own unit, when there is one.
    target: float | None = None
    #: The time bucket label as its own surface spells it, for a surface whose
    #: buckets are not part of the grouping (``1d`` rather than ``day``).
    time_bucket: str | None = None
    #: False when the rows do not add up, which is true of every percentile.
    #: A non additive result gets no totals row and no share of total column.
    additive: bool = True

    @property
    def primary_metric(self) -> str:
        """The metric used for sorting context and share-of-total percentages."""
        if self.metric_names:
            return self.metric_names[0]
        if self.fallback_metrics:
            return self.fallback_metrics[0]
        return ""

    @property
    def group_dimensions(self) -> list[str]:
        """Every non-time dimension the rows are labelled by, in request order.

        There is one label cell per entry here on every row, so a grouping such
        as ``eventName`` plus ``eventData/plan`` keeps both values instead of
        collapsing onto the first one.
        """
        return [dim for dim in self.group_by if dim not in TIME_GRANULARITIES]

    @property
    def group_dimension(self) -> str | None:
        """The first non-time dimension, if there is one."""
        dimensions = self.group_dimensions
        return dimensions[0] if dimensions else None

    @property
    def granularity(self) -> str | None:
        """The time bucket for these rows, if they are bucketed at all.

        A surface that carries its buckets outside the grouping sets
        ``time_bucket`` instead, and that spelling wins because it is the one
        that surface actually used. This is the machine spelling: it is what
        goes into JSON output and what timestamps are formatted against. For
        something to print as a column header, use :attr:`granularity_label`.
        """
        if self.time_bucket:
            return self.time_bucket
        for dimension in self.group_by:
            if dimension in TIME_GRANULARITIES:
                return dimension
        return None

    @property
    def granularity_label(self) -> str | None:
        """The time bucket as a human reads it, for a column header.

        The two surfaces spell buckets differently (``1d`` against ``day``), and
        a bare ``1d`` at the top of a column reads like a value rather than a
        heading. Sibling presets should not disagree about what to call the same
        thing, so ``trend`` and ``vitals-trend`` both head that column ``day``.
        An unrecognised spelling is passed through rather than guessed at.
        """
        granularity = self.granularity
        if granularity is None:
            return None
        return GRANULARITY_ALIASES.get(granularity, granularity)

    def totals(self) -> dict[str, float]:
        """Sum every metric across every row, including the ``Others`` bucket."""
        totals: dict[str, float] = {name: 0 for name in self.metric_names}
        for row in self.rows:
            for name in self.metric_names:
                totals[name] += row.metrics.get(name, 0)
        return totals


# ---------------------------------------------------------------------------
# Request logs containers, and the widths their tables use
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LogLine:
    """One application log line attached to a request.

    ``message`` is already sanitized: the surface module escapes it once, on
    the way in, so nothing downstream has to remember to.
    """

    level: str
    message: str
    truncated: bool = False


@dataclass(frozen=True)
class LogEntry:
    """One request, as the request logs surface reports it.

    Every string field arrives sanitized. ``raw`` is the exception: it keeps the
    row as it arrived, unescaped, so ``--json`` can hand back everything the API
    sent rather than only the columns this tool tabulates. That is safe because
    ``raw`` is only ever emitted through ``json.dumps``, which escapes control
    characters, so no escape sequence in it can reach a terminal. It must never
    be printed directly, and tests/test_logs_render.py holds that line.

    One rewrite does reach ``raw``: this client's own credential is replaced
    wherever it appears in a row, since a log line is free text an application
    wrote and can echo the token that fetched it. That happens in
    ``logs.normalize``, before this container exists.
    """

    request_id: str = ""
    timestamp: datetime | None = None
    status: int | None = None
    method: str = ""
    path: str = ""
    route: str = ""
    source: str = ""
    environment: str = ""
    deployment_id: str = ""
    duration_ms: float | None = None
    region: str = ""
    error_code: str = ""
    branch: str = ""
    domain: str = ""
    trace_id: str = ""
    crashed: bool = False
    lines: tuple[LogLine, ...] = ()
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def worst_line(self) -> LogLine | None:
        """The most severe log line on this request, if it logged anything.

        ``max`` is stable in Python, so among lines tied for the worst level
        the first one wins, which is the earliest one logged.
        """
        if not self.lines:
            return None
        return max(
            self.lines,
            key=lambda line: LOG_LEVEL_SEVERITY.get(line.level, -1),
        )

    @property
    def worst_level(self) -> str | None:
        """The level of :attr:`worst_line`, or ``None`` when nothing was logged."""
        line = self.worst_line
        return line.level if line is not None else None

    @property
    def headline(self) -> str:
        """The message worth showing on one row, empty when nothing was logged."""
        line = self.worst_line
        return line.message if line is not None else ""

    @property
    def is_error(self) -> bool:
        """True when this request is something to worry about.

        Three ways to qualify: the response was a 5xx, the function crashed, or
        the request logged an error or fatal line. A 4xx does not qualify: a
        401 on a login route is the application working.
        """
        if self.status is not None and self.status >= 500:
            return True
        if self.crashed:
            return True
        return self.worst_level in ERROR_LEVELS

    @property
    def label(self) -> str:
        """What to show in the route column: the route, or the path, or a mark."""
        return self.route or self.path or "(unknown)"


@dataclass(frozen=True)
class RouteTally:
    """How many requests hit one route, at what worst status, and when."""

    route: str
    count: int
    worst_status: int | None
    first_seen: datetime | None
    last_seen: datetime | None


@dataclass(frozen=True)
class MessageTally:
    """How many requests logged one exact message, and when."""

    message: str
    count: int
    first_seen: datetime | None
    last_seen: datetime | None


@dataclass(frozen=True)
class LogSummary:
    """A merged list of entries, tallied by status, by route and by message."""

    total: int
    by_status: tuple[tuple[str, int], ...]
    by_route: tuple[RouteTally, ...]
    by_message: tuple[MessageTally, ...]
    #: Entries that are errors only because they logged an error or fatal
    #: line: a non-5xx status that did not crash but did carry such a line.
    #: All three conditions are checked, so this is safe to compute on any
    #: set of entries, not just one already filtered to errors.
    logged_only: int


@dataclass(frozen=True)
class LogReport:
    """Everything :func:`render_logs` needs, already decided by ``logs.py``.

    ``render.py`` lays this out without knowing any API fact: every sentence
    beyond the table itself, including whether one is owed at all, is decided
    by :func:`vercel_insights.logs.build_report` and carried here as data.
    """

    entries: list[LogEntry]
    time_range: tuple[datetime, datetime]
    project_label: str
    preset: str
    #: The window as a person says it, for example "30 minutes". Composed in
    #: logs.py so it cannot disagree with the range line.
    window_label: str = ""
    filters: dict[str, str] = field(default_factory=dict)
    truncated: bool = False
    pages_fetched: int = 0
    requested_limit: int = 0
    header_note: str | None = None
    notes: tuple[str, ...] = ()
    #: The "try this next" line, dropped when --expand already did it.
    hint: str | None = None


#: Column widths for the request logs table, wide enough for a route or a
#: one-line message excerpt without either dominating the row.
LOG_MESSAGE_WIDTH = 34
LOG_ROUTE_WIDTH = 32

#: Message width for the error-summary's message table, wider than the row
#: table's since that table has no route or status column competing for
#: space.
LOG_SUMMARY_MESSAGE_WIDTH = 48

#: Printed in the message column for an error that logged nothing, so a blank
#: cell there reads as the fact that the response failed before any handler
#: printed rather than as a rendering fault.
NO_LINE_ERROR = "(no log line: the response failed)"


# ---------------------------------------------------------------------------
# Decoration, value formatting and the grid every table is built on
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Style:
    """How output is decorated: colour, and whether non-ASCII glyphs are safe."""

    color: bool = False
    unicode: bool = True

    def bold(self, text: str) -> str:
        return f"\033[1m{text}\033[0m" if self.color else text

    def dim(self, text: str) -> str:
        return f"\033[2m{text}\033[0m" if self.color else text

    def accent(self, text: str) -> str:
        return f"\033[36m{text}\033[0m" if self.color else text

    @property
    def ellipsis(self) -> str:
        return "…" if self.unicode else "..."

    @property
    def bar(self) -> str:
        return "█" if self.unicode else "#"


PLAIN_STYLE = Style()


def _format_number(value: float) -> str:
    """Thousands separated, with decimals only when the value really has them."""
    if isinstance(value, int) or float(value).is_integer():
        return f"{int(value):,}"
    return f"{value:,.2f}"


def format_value(value: float, unit: str | None = None) -> str:
    """Render one metric value in its own unit.

    Milliseconds read as milliseconds below one second and as seconds with one
    decimal above it, which is how Vercel writes them (``2.5 s``, not
    ``2500 ms``). The layout shift score is unitless and small, so it keeps
    three decimals. Anything else is a plain number.
    """
    if unit == UNIT_MS:
        if abs(value) < MS_TO_SECONDS_THRESHOLD:
            return f"{value:.0f} ms"
        return f"{value / 1000.0:.1f} s"
    if unit == UNIT_SCORE:
        return f"{value:.3f}"
    return _format_number(value)


def verdict(value: float | None, target: float | None) -> str:
    """Compare a value against its published target. Two tier by design.

    Vercel publishes one "good" target per web vital and no boundary above it,
    so there is no honest third tier to report. The dashboard's good, needs
    improvement and poor bands describe a 0 to 100 score derived from a log
    normal distribution of HTTP Archive data, not the raw millisecond or score
    value this function is given, so they are not applicable here.

    Lower is better for every metric that has a target, so meeting it means
    being at or below it.
    """
    if target is None or value is None:
        return VERDICT_UNKNOWN
    return VERDICT_MEETS if value <= target else VERDICT_OVER


def _truncate(text: str, width: int, style: Style) -> str:
    """Shorten a label to ``width`` characters, marking the cut."""
    if width <= 0 or len(text) <= width:
        return text
    marker = style.ellipsis
    if width <= len(marker):
        return text[:width]
    return text[: width - len(marker)] + marker


def _pad(text: str, width: int, align: str) -> str:
    return text.rjust(width) if align == "right" else text.ljust(width)


def render_grid(
    headers: Sequence[str],
    aligns: Sequence[str],
    body: Sequence[Sequence[str]],
    footer: Sequence[str] | None,
    style: Style,
) -> list[str]:
    """Lay out an aligned text grid with a rule under the head and the footer."""
    widths = [len(head) for head in headers]
    for row in list(body) + ([list(footer)] if footer else []):
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def line(cells: Sequence[str]) -> str:
        return "  ".join(
            _pad(cell, widths[index], aligns[index]) for index, cell in enumerate(cells)
        ).rstrip()

    rule = "  ".join("-" * width for width in widths)
    lines = [style.bold(line(headers)), style.dim(rule)]
    lines.extend(line(row) for row in body)
    if footer:
        lines.append(style.dim(rule))
        lines.append(style.bold(line(footer)))
    return lines


def _label_headers(result: Result, has_time: bool) -> list[str]:
    """One column heading per grouped dimension, named as it was requested.

    A grouping with no non-time dimension needs no label column at all when the
    timestamp already identifies the row; without a timestamp column there is
    still one generic column so the rows are not left anonymous.
    """
    dimensions = result.group_dimensions
    if dimensions:
        return list(dimensions)
    return [] if has_time else ["group"]


def _label_cells(row: Row, count: int) -> list[str]:
    """The label cells for one row, padded to ``count`` columns.

    A missing label reads as ``(none)``, except on the overflow bucket, which
    always says so: it must never render as a blank cell.
    """
    cells: list[str] = []
    for index in range(count):
        label = row.labels[index] if index < len(row.labels) else None
        if label is None:
            label = OTHERS_LABEL if row.is_others else "(none)"
        cells.append(label)
    return cells


def _range_line(time_range: tuple[datetime, datetime]) -> str:
    since, until = time_range
    return f"Range: {to_api_timestamp(since)} to {to_api_timestamp(until)} (UTC)"


# ---------------------------------------------------------------------------
# The analytics table, and its JSON and CSV forms
# ---------------------------------------------------------------------------


def format_table(
    result: Result,
    *,
    time_range: tuple[datetime, datetime] | None = None,
    filter_expr: str | None = None,
    limit: int | None = None,
    style: Style = PLAIN_STYLE,
    max_label_width: int = 48,
    title: str | None = None,
    show_context: bool = True,
) -> str:
    """Render a result as aligned text.

    Grouped results get one row per group, metric columns right aligned with
    thousands separators, a share of total column for the primary metric, and a
    totals row. Count results get a small labelled block instead, since there is
    nothing to group. An ``Others`` row is annotated below the table so it reads
    as the limit overflow bucket rather than a real group value.

    Args:
        result: The parsed result.
        time_range: The resolved window, shown as context.
        filter_expr: The active OData filter, shown as context.
        limit: The limit that was sent, used in the ``Others`` note.
        style: Colour and glyph settings.
        max_label_width: Longer labels are truncated with an ellipsis.
        title: Optional heading, used by the overview report.
        show_context: Print the range and filter lines above the table.

    Returns:
        The rendered block, without a trailing newline.
    """
    lines: list[str] = []
    if title:
        lines.append(style.bold(title))
    if show_context:
        if time_range:
            lines.append(style.dim(_range_line(time_range)))
        if filter_expr:
            lines.append(style.dim(f"Filter: {filter_expr}"))
        if lines:
            lines.append("")

    if result.is_count:
        lines.extend(_format_count_block(result, style))
        lines.extend(_vitals_notes(result, style))
        return "\n".join(lines)

    totals = result.totals()
    primary = result.primary_metric
    primary_total = totals.get(primary, 0)

    granularity = result.granularity
    has_time = granularity is not None and any(row.timestamp for row in result.rows)
    label_headers = _label_headers(result, has_time)

    headers: list[str] = []
    aligns: list[str] = []
    if has_time:
        headers.append(result.granularity_label or "time")
        aligns.append("left")
    headers.extend(label_headers)
    aligns.extend("left" for _ in label_headers)
    for name in result.metric_names:
        headers.append(name)
        aligns.append("right")
    if result.additive:
        headers.append(f"% {primary}")
        aligns.append("right")

    body: list[list[str]] = []
    has_others = any(row.is_others for row in result.rows)
    for row in result.rows:
        cells: list[str] = []
        if has_time:
            cells.append(format_timestamp(row.timestamp or "", granularity))
        cells.extend(
            _truncate(label, max_label_width, style)
            for label in _label_cells(row, len(label_headers))
        )
        for name in result.metric_names:
            cells.append(_format_metric(result, name, row.metrics.get(name, 0)))
        if result.additive:
            share = (
                (row.metrics.get(primary, 0) / primary_total * 100)
                if primary_total
                else 0.0
            )
            cells.append(f"{share:.1f}%")
        body.append(cells)

    footer: list[str] | None = None
    if result.additive:
        footer = ["TOTAL"]
        footer.extend("" for _ in range(len(label_headers) + (1 if has_time else 0) - 1))
        for name in result.metric_names:
            footer.append(_format_number(totals.get(name, 0)))
        footer.append("100.0%" if primary_total else "0.0%")

    lines.extend(render_grid(headers, aligns, body, footer, style))

    if has_others:
        bound = f"--limit {limit}" if limit is not None else "the limit"
        lines.append("")
        lines.append(
            style.dim(
                f"{OTHERS_LABEL} is not a real value: it is every group beyond "
                f"{bound}, collapsed by the API into one bucket."
            )
        )
    lines.extend(_vitals_notes(result, style))
    return "\n".join(lines)


def _vitals_notes(result: Result, style: Style) -> list[str]:
    """The legend under a Speed Insights table, and nothing under any other."""
    if result.unit is None:
        return []
    lines = [""]
    if result.metric:
        label = f" ({result.metric_label})" if result.metric_label else ""
        lines.append(style.dim(f"Metric: {result.metric}{label}"))
        if result.target is not None:
            lines.append(
                style.dim(
                    f"Target: {format_value(result.target, result.unit)} or less"
                )
            )
    legend = list(
        DATA_POINTS_LEGEND if result.unit == UNIT_COUNT else VITALS_LEGEND
    )
    if result.unit != UNIT_COUNT and DATA_POINTS_METRIC in result.metric_names:
        legend.append(DATA_POINTS_NOTE)
    lines.extend(style.dim(note) for note in legend)
    return lines


def _metric_names(result: Result) -> list[str]:
    """The metric names to render, falling back to what the surface supplied."""
    return result.metric_names or list(result.fallback_metrics)


def _format_metric(result: Result, name: str, value: float) -> str:
    """Render one metric cell, in the result's unit for the primary metric.

    Only the primary metric carries the unit: the columns beside it are data
    point counts, which are plain numbers whatever the metric is measured in.
    """
    if result.unit is not None and name == result.primary_metric:
        return format_value(value, result.unit)
    return _format_number(value)


def _format_count_block(result: Result, style: Style) -> list[str]:
    """Render an ungrouped result as a small labelled block."""
    row = result.rows[0] if result.rows else Row()
    names = _metric_names(result)
    if not names:
        return []
    width = max(len(name) for name in names)
    values = [
        _format_metric(result, name, row.metrics.get(name, 0)) for name in names
    ]
    value_width = max(len(value) for value in values)
    return [
        f"  {name.ljust(width)}  {value.rjust(value_width)}"
        for name, value in zip(names, values)
    ]


def _result_document(
    result: Result,
    payload: Mapping[str, Any] | None,
    time_range: tuple[datetime, datetime] | None,
) -> dict[str, Any]:
    """Build the JSON document for one result."""
    document: dict[str, Any] = {
        "query": result.query,
        "range": (
            {
                "since": to_api_timestamp(time_range[0]),
                "until": to_api_timestamp(time_range[1]),
            }
            if time_range
            else None
        ),
        "dataset": result.dataset,
        "groupBy": result.group_by,
        "isCount": result.is_count,
        "metrics": result.metric_names,
        **(
            {
                "metric": result.metric,
                "metricLabel": result.metric_label,
                "unit": result.unit,
                "target": result.target,
                "granularity": result.time_bucket,
            }
            if result.metric
            else {}
        ),
        "rows": [
            {
                "key": row.key,
                "groups": dict(zip(result.group_dimensions, row.labels)),
                "timestamp": row.timestamp,
                "metrics": row.metrics,
            }
            for row in result.rows
        ],
        # A percentile does not add up, so a non additive result reports no
        # totals rather than a sum that would read as a real figure.
        "totals": result.totals() if result.additive else None,
    }
    document["raw"] = payload
    return document


def format_json(
    result: Result,
    payload: Mapping[str, Any] | None = None,
    *,
    time_range: tuple[datetime, datetime] | None = None,
) -> str:
    """Render a result as JSON, with the untouched API payload under ``raw``."""
    return json.dumps(_result_document(result, payload, time_range), indent=2)


def format_csv(result: Result) -> str:
    """Render a result as CSV, quoted by :mod:`csv` so labels stay safe."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    names = result.metric_names

    if result.is_count:
        writer.writerow(names)
        row = result.rows[0] if result.rows else Row()
        writer.writerow([row.metrics.get(name, 0) for name in names])
        return buffer.getvalue()

    granularity = result.granularity
    has_time = granularity is not None and any(row.timestamp for row in result.rows)
    label_headers = _label_headers(result, has_time)

    header: list[str] = []
    if has_time:
        header.append(result.granularity_label or "time")
    header.extend(label_headers)
    header.extend(names)
    writer.writerow(header)

    for row in result.rows:
        cells: list[Any] = []
        if has_time:
            cells.append(format_timestamp(row.timestamp or "", granularity))
        cells.extend(_label_cells(row, len(label_headers)))
        cells.extend(row.metrics.get(name, 0) for name in names)
        writer.writerow(cells)
    return buffer.getvalue()


def _sparkline_rows(result: Result, style: Style, width: int = 24) -> list[str]:
    """A compact per bucket breakdown for the overview report."""
    primary = result.primary_metric
    values = [row.metrics.get(primary, 0) for row in result.rows]
    peak = max(values) if values else 0
    label_width = max(
        (
            len(format_timestamp(row.timestamp or "", result.granularity))
            for row in result.rows
        ),
        default=0,
    )
    value_width = max((len(_format_number(value)) for value in values), default=0)
    lines: list[str] = []
    for row, value in zip(result.rows, values):
        label = format_timestamp(row.timestamp or "", result.granularity)
        filled = round((value / peak) * width) if peak else 0
        bar = style.bar * filled
        lines.append(
            f"  {label.ljust(label_width)}  {_format_number(value).rjust(value_width)}"
            f"  {style.accent(bar)}"
        )
    return lines


# ---------------------------------------------------------------------------
# The composed analytics reports: overview and vitals
# ---------------------------------------------------------------------------


def render_overview(
    results: Sequence[Result],
    *,
    project: str,
    time_range: tuple[datetime, datetime],
    filter_expr: str | None = None,
    limit: int = OVERVIEW_TABLE_LIMIT,
    style: Style = PLAIN_STYLE,
) -> str:
    """Compose the three overview results into one immediately useful report.

    Args:
        results: The daily result, the top pages result and the top referrers
            result, in that order.
        project: Project id or name, shown in the heading.
        time_range: The resolved window.
        filter_expr: The active OData filter, if any.
        limit: The row limit used for the two tables.
        style: Colour and glyph settings.

    Returns:
        The rendered report, without a trailing newline.
    """
    daily, pages, referrers = results[0], results[1], results[2]

    lines = [
        style.bold(f"Vercel Web Analytics: {project}"),
        style.dim(_range_line(time_range)),
    ]
    if filter_expr:
        lines.append(style.dim(f"Filter: {filter_expr}"))
    lines.append("")

    totals = daily.totals()
    names = _metric_names(daily)
    width = max(len(name) for name in names)
    values = [_format_number(totals.get(name, 0)) for name in names]
    value_width = max(len(value) for value in values)
    for name, value in zip(names, values):
        lines.append(f"  {style.bold(name.ljust(width))}  {value.rjust(value_width)}")
    if "visitors" in names:
        lines.append(
            style.dim(
                "  visitors is a sum of the buckets below, so someone who came on "
                "two days counts twice;"
            )
        )
        lines.append(
            style.dim("  run the total preset for distinct visitors over the window")
        )

    lines.append("")
    lines.append(style.bold(f"By {daily.granularity_label or 'day'}"))
    if daily.rows:
        lines.extend(_sparkline_rows(daily, style))
    else:
        lines.append(style.dim("  no data in this window"))

    for title, result in (("Top pages", pages), ("Top referrers", referrers)):
        lines.append("")
        if result.rows:
            lines.append(
                format_table(
                    result,
                    limit=limit,
                    style=style,
                    title=f"{title} (top {limit})",
                    show_context=False,
                    max_label_width=56,
                )
            )
        else:
            lines.append(style.bold(title))
            lines.append(style.dim("  no data in this window"))

    return "\n".join(lines)


def _single_value(result: Result) -> float | None:
    """The one value an ungrouped result carries, or ``None`` when it has none."""
    if not result.rows:
        return None
    value = result.rows[0].metrics.get(result.primary_metric)
    return float(value) if isinstance(value, (int, float)) else None


def _data_point_count(result: Result) -> float | None:
    """The data point count behind an ungrouped value, when one came back."""
    if not result.rows:
        return None
    value = result.rows[0].metrics.get(DATA_POINTS_METRIC)
    return float(value) if isinstance(value, (int, float)) else None


def render_vitals(
    results: Sequence[Result],
    *,
    project: str,
    time_range: tuple[datetime, datetime],
    aggregation: str = "p75",
    filter_expr: str | None = None,
    style: Style = PLAIN_STYLE,
) -> str:
    """Compose one ungrouped result per web vital into a single table.

    The Speed Insights query API answers for one metric per request, so the
    vitals preset issues one query per metric and this is where the five
    answers become one report: metric, the percentile that was asked for,
    Vercel's published target, and whether the value meets it.

    The verdict is two tier on purpose. See :func:`verdict`.

    Args:
        results: One ungrouped result per metric, in display order.
        project: Project id or name, shown in the heading.
        time_range: The resolved window.
        aggregation: The aggregation every query used, used as a column head.
        filter_expr: The active OData filter, if any.
        style: Colour and glyph settings.

    Returns:
        The rendered report, without a trailing newline.
    """
    lines = [
        style.bold(f"Vercel Speed Insights: {project}"),
        style.dim(_range_line(time_range)),
    ]
    if filter_expr:
        lines.append(style.dim(f"Filter: {filter_expr}"))
    lines.append("")

    show_points = any(_data_point_count(result) is not None for result in results)
    # Data point counts have no published target, and no target means there is
    # nothing to render a verdict against.
    show_targets = any(result.target is not None for result in results)
    counts_only = bool(results) and all(
        result.unit == UNIT_COUNT for result in results
    )

    headers = ["metric", aggregation]
    aligns = ["left", "right"]
    if show_targets:
        headers.extend(["target", "verdict"])
        aligns.extend(["right", "left"])
    if show_points:
        headers.append("data points")
        aligns.append("right")

    body: list[list[str]] = []
    for result in results:
        value = _single_value(result)
        cells = [
            result.metric_label or result.metric or "",
            format_value(value, result.unit) if value is not None else "no data",
        ]
        if show_targets:
            cells.append(
                format_value(result.target, result.unit)
                if result.target is not None
                else "n/a"
            )
            cells.append(
                verdict(value, result.target) if value is not None else "no data"
            )
        if show_points:
            points = _data_point_count(result)
            cells.append(_format_number(points) if points is not None else "n/a")
        body.append(cells)

    lines.extend(render_grid(headers, aligns, body, None, style))
    lines.append("")
    legend = list(DATA_POINTS_LEGEND if counts_only else VITALS_LEGEND)
    if not counts_only and any(
        DATA_POINTS_METRIC in result.metric_names for result in results
    ):
        legend.append(DATA_POINTS_NOTE)
    lines.extend(style.dim(note) for note in legend)
    lines.append(
        style.dim(
            "Real Experience Score is not queryable through this API; read it "
            "on the Speed Insights dashboard."
        )
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Request logs rendering: rows, the three tallies, JSON and CSV
# ---------------------------------------------------------------------------


def _clock_pattern(time_range: tuple[datetime, datetime]) -> str:
    """The strftime pattern a clock in this report should use.

    ``HH:MM:SS`` is enough to tell rows apart inside one day; a window
    spanning more than a day needs the date too, or two rows a day apart would
    print identical times. Shared by :func:`_log_time` and the error-summary's
    per tally "first seen" and "last seen" columns, so both read the same
    window the same way.
    """
    span = time_range[1] - time_range[0]
    return "%H:%M:%S" if span <= timedelta(hours=24) else "%m-%d %H:%M:%S"


def _log_time(entry: LogEntry, time_range: tuple[datetime, datetime]) -> str:
    """The row's clock, at a precision the window justifies."""
    if entry.timestamp is None:
        return "(no time)"
    return entry.timestamp.strftime(_clock_pattern(time_range))


def _seen_cell(timestamp: datetime | None, time_range: tuple[datetime, datetime]) -> str:
    """A tally's ``first seen`` or ``last seen`` cell, or a mark when it has none.

    A route or message group can end up with no timestamped member (a row can
    arrive with no ``timestamp`` at all), and a blank cell there would read as
    a rendering fault rather than as the fact that nothing was recorded.
    """
    if timestamp is None:
        return "(no time)"
    return timestamp.strftime(_clock_pattern(time_range))


def _log_message_cell(entry: LogEntry, style: Style) -> str:
    """The one line of message that fits in the table.

    An error that logged nothing says so: an empty cell there reads as a
    rendering fault rather than as the fact that the response failed before any
    handler printed anything.
    """
    message = entry.headline
    if not message:
        return NO_LINE_ERROR if entry.is_error else ""
    return _truncate(message.splitlines()[0], LOG_MESSAGE_WIDTH, style)


def _expanded_lines(entry: LogEntry, style: Style) -> list[str]:
    """Every log line of one request, worst first, indented under its row.

    A message may itself be several lines: ``sanitize_message`` indents its
    continuations, so they stay visibly quoted rather than reaching column
    zero. This adds its own indent on top of that on every line, rather than
    only on the first, so a continuation never renders less indented than the
    line above it: a stack trace must not step backwards under ``--expand``.
    """
    ordered = sorted(
        entry.lines,
        key=lambda line: LOG_LEVEL_SEVERITY.get(line.level, -1),
        reverse=True,
    )
    out: list[str] = []
    for line in ordered:
        label = f"{line.level}: " if line.level else ""
        suffix = " [truncated by Vercel]" if line.truncated else ""
        rows = line.message.split("\n")
        rows[0] = f"{label}{rows[0]}"
        rows[-1] = f"{rows[-1]}{suffix}"
        out.append(style.dim("\n".join(f"    {row}" for row in rows)))
    if entry.request_id:
        out.append(style.dim(f"    request {entry.request_id}"))
    return out


def render_logs(
    report: LogReport, *, style: Style = PLAIN_STYLE, expand: bool = False
) -> str:
    """Render a logs report as aligned text.

    One row per request, newest first. An empty report prints one line naming
    what was asked rather than a table head with nothing under it.

    Args:
        report: The report to print.
        style: Colour and glyph settings.
        expand: Print every full log message under its row.

    Returns:
        The report as text, with no trailing newline.
    """
    title = (
        f"Vercel request logs: {report.project_label} "
        f"({report.preset}, last {report.window_label})"
    )
    parts: list[str] = [style.bold(title), _range_line(report.time_range)]
    if report.filters:
        shown = ", ".join(f"{name} {value}" for name, value in report.filters.items())
        parts.append(f"Filter: {shown}")
    if report.header_note:
        parts.append(style.dim(report.header_note))
    parts.append("")

    if not report.entries:
        since, until = report.time_range
        parts.append(
            f"No request logs for project {report.project_label} between "
            f"{to_api_timestamp(since)} and {to_api_timestamp(until)}."
        )
    else:
        headers = ["time", "level", "status", "method", "route", "source", "message"]
        aligns = ["left", "left", "right", "left", "left", "left", "left"]
        body = [
            [
                _log_time(entry, report.time_range),
                entry.worst_level or "-",
                str(entry.status) if entry.status is not None else "(none)",
                entry.method or "-",
                _truncate(entry.label, LOG_ROUTE_WIDTH, style),
                entry.source or "-",
                _log_message_cell(entry, style),
            ]
            for entry in report.entries
        ]
        grid = render_grid(headers, aligns, body, None, style)
        # render_grid emits the head, the rule, then one line per body row in
        # order, which is what lets the expansions be spliced under their rows.
        parts.extend(grid[:2])
        for index, entry in enumerate(report.entries):
            parts.append(grid[2 + index])
            if expand:
                parts.extend(_expanded_lines(entry, style))

    if report.notes:
        parts.append("")
        parts.extend(style.dim(note) for note in report.notes)
    if report.hint and not expand:
        parts.append(style.dim(report.hint))
    return "\n".join(parts)


def _share(count: int, total: int) -> str:
    """A share of ``total``, formatted like ``format_table``'s share column."""
    share = (count / total * 100) if total else 0.0
    return f"{share:.1f}%"


def _status_table(summary: LogSummary, style: Style) -> list[str]:
    """The status breakdown: grouped by HTTP status alone.

    A request that is an error only because it logged an error or fatal line
    still appears under its real status here rather than under a level name:
    mixing a level into this column would read as though ``fatal`` were a
    status code. ``report.notes`` is what explains how many rows qualify that
    way; this table only counts.
    """
    headers = ["status", "count", "share"]
    aligns = ["left", "right", "right"]
    body = [
        [status, str(count), _share(count, summary.total)]
        for status, count in summary.by_status
    ]
    footer = ["TOTAL", str(summary.total), _share(summary.total, summary.total)]
    return render_grid(headers, aligns, body, footer, style)


def _route_table(
    summary: LogSummary, time_range: tuple[datetime, datetime], style: Style
) -> list[str]:
    """The per route breakdown. No totals row: a worst status does not add up."""
    headers = ["route", "count", "worst status", "first seen", "last seen"]
    aligns = ["left", "right", "right", "left", "left"]
    body = [
        [
            tally.route,
            str(tally.count),
            str(tally.worst_status) if tally.worst_status is not None else "(none)",
            _seen_cell(tally.first_seen, time_range),
            _seen_cell(tally.last_seen, time_range),
        ]
        for tally in summary.by_route
    ]
    return render_grid(headers, aligns, body, None, style)


def _message_table(
    summary: LogSummary, time_range: tuple[datetime, datetime], style: Style
) -> list[str]:
    """The per exact message breakdown. No totals row, for the same reason as routes."""
    headers = ["message", "count", "first seen", "last seen"]
    aligns = ["left", "right", "left", "left"]
    body = [
        [
            _truncate(tally.message, LOG_SUMMARY_MESSAGE_WIDTH, style),
            str(tally.count),
            _seen_cell(tally.first_seen, time_range),
            _seen_cell(tally.last_seen, time_range),
        ]
        for tally in summary.by_message
    ]
    return render_grid(headers, aligns, body, None, style)


def render_error_summary(
    report: LogReport, summary: LogSummary, *, style: Style = PLAIN_STYLE
) -> str:
    """Render a logs report as three grouped tables: status, route and message.

    Unlike :func:`render_logs`, which prints one row per request, this groups
    the same entries three ways so "what is breaking" reads off a handful of
    rows instead of scrolling a table of individual requests. ``summary`` is
    supplied rather than recomputed here so a caller building both the report
    and its summary controls exactly which entries were tallied.

    The report's notes are printed verbatim and are the only prose this
    function adds: ``build_report`` already composes the sentence explaining
    a non-5xx row in the status table (the ``logged_only`` count), so this
    renderer must not print a second copy of it.

    Args:
        report: The report to print.
        summary: The same report's entries, tallied by status, route and
            message.
        style: Colour and glyph settings.

    Returns:
        The report as text, with no trailing newline.
    """
    title = (
        f"Vercel request logs: {report.project_label} "
        f"({report.preset}, last {report.window_label})"
    )
    parts: list[str] = [style.bold(title), _range_line(report.time_range)]
    if report.filters:
        # Same line as render_logs, for the same reason: this report's footer
        # counts the rows that matched, and a count of matching rows read
        # without the filter beside it reads as a count of everything.
        shown = ", ".join(f"{name} {value}" for name, value in report.filters.items())
        parts.append(f"Filter: {shown}")

    if not report.entries:
        since, until = report.time_range
        parts.append("")
        parts.append(
            f"No request logs for project {report.project_label} between "
            f"{to_api_timestamp(since)} and {to_api_timestamp(until)}."
        )
    else:
        parts.append("")
        parts.extend(_status_table(summary, style))
        parts.append("")
        parts.extend(_route_table(summary, report.time_range, style))
        parts.append("")
        parts.extend(_message_table(summary, report.time_range, style))

    if report.notes:
        parts.append("")
        parts.extend(style.dim(note) for note in report.notes)
    return "\n".join(parts)


def _log_entry_json(entry: LogEntry) -> dict[str, Any]:
    """One entry as a JSON object, keeping the whole row alongside the columns.

    Args:
        entry: The entry to render.

    Returns:
        A JSON-safe mapping. ``raw`` is included as the row arrived, save for
        the credential rewrite ``logs.normalize`` applied to it: this
        function's result must only ever be handed to :func:`json.dumps`, never
        printed directly, because ``raw`` is not escaped.
    """
    return {
        "requestId": entry.request_id,
        "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
        "status": entry.status,
        "method": entry.method,
        "path": entry.path,
        "route": entry.route,
        "source": entry.source,
        "environment": entry.environment,
        "deploymentId": entry.deployment_id,
        "durationMs": entry.duration_ms,
        "region": entry.region,
        "errorCode": entry.error_code,
        "branch": entry.branch,
        "domain": entry.domain,
        "traceId": entry.trace_id,
        "crashed": entry.crashed,
        "isError": entry.is_error,
        "level": entry.worst_level,
        "message": entry.headline,
        "lines": [
            {
                "level": line.level,
                "message": line.message,
                "truncated": line.truncated,
            }
            for line in entry.lines
        ],
        "raw": entry.raw,
    }


def format_logs_json(report: LogReport) -> str:
    """Render a logs report as JSON, keeping every field the API sent.

    ``raw`` carries the unescaped row, which is safe here and only here: this
    is the one output path that escapes control characters on the way out. It is
    not entirely untouched, since ``logs.normalize`` rewrote this client's own
    credential out of it, but nothing else in it was altered.

    Args:
        report: The report to render.

    Returns:
        The report as an indented JSON document, with strict JSON semantics:
        ``NaN`` and ``Infinity`` are refused rather than emitted, since the
        README sells piping ``--json`` into ``jq``.

    Raises:
        ValueError: If a value in ``report`` is a non-finite float, since
            ``json.dumps`` is called with ``allow_nan=False``.
    """
    # allow_nan=False is a second line of defence, not the first: http.py's
    # response parser already walks every parsed body and refuses a NaN,
    # Infinity or -Infinity with an invalid_response error, so one of those
    # cannot reach `raw` from a real API response. This still refuses to
    # write one out rather than propagate it, in case a value ever reached
    # here some other way.
    since, until = report.time_range
    document = {
        "query": {
            "project": report.project_label,
            "preset": report.preset,
            "since": to_api_timestamp(since),
            "until": to_api_timestamp(until),
            "filters": report.filters,
            "limit": report.requested_limit,
        },
        "entries": [_log_entry_json(entry) for entry in report.entries],
        "truncated": report.truncated,
        "pagesFetched": report.pages_fetched,
        "notes": list(report.notes),
    }
    return json.dumps(document, indent=2, allow_nan=False)


#: The CSV columns, in order. Kept next to the writer so the header and the
#: row cannot drift apart.
LOG_CSV_COLUMNS: tuple[str, ...] = (
    "time",
    "level",
    "status",
    "method",
    "route",
    "path",
    "source",
    "requestId",
    "message",
)


def format_logs_csv(report: LogReport) -> str:
    """Render a logs report as CSV, one row per request.

    A message can contain a literal newline: ``sanitize_message`` deliberately
    keeps them, because a stack trace's line structure is the one place a
    newline carries meaning (``sanitize_label``, used for every other string
    field here, is the one that escapes them). What keeps that newline from
    breaking a row open is :mod:`csv` itself: ``csv.writer`` quotes any field
    that contains its line terminator, so the message stays inside one cell
    rather than starting a new record.

    Args:
        report: The report to render.

    Returns:
        The report as CSV text, header first, with the columns named in
        :data:`LOG_CSV_COLUMNS`.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(LOG_CSV_COLUMNS)
    for entry in report.entries:
        writer.writerow(
            [
                entry.timestamp.isoformat() if entry.timestamp else "",
                entry.worst_level or "",
                entry.status if entry.status is not None else "",
                entry.method,
                entry.route,
                entry.path,
                entry.source,
                entry.request_id,
                entry.headline,
            ]
        )
    return buffer.getvalue()
