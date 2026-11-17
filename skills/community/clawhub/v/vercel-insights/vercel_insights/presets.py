"""The preset table: named bundles of defaults, and how to print them.

A preset also decides which API a run talks to. That is the one thing about it
that no flag overrides: ``--metric`` chooses which web vital a Speed Insights
preset reports, it does not turn a Web Analytics preset into a Speed Insights
one.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import OTHERS_LABEL
from .logs import DEFAULT_LIMIT as LOGS_DEFAULT_LIMIT
from .logs import MAX_LIMIT as LOGS_MAX_LIMIT
from .render import (
    OVERVIEW_TABLE_LIMIT,
    PLAIN_STYLE,
    Style,
    render_grid,
)
from .speedinsights import COUNT_AGGREGATION
from .speedinsights import DEFAULT_LIMIT as SPEED_DEFAULT_LIMIT
from .timerange import LOGS, SPEED_INSIGHTS, WEB_ANALYTICS
from .webanalytics import DEFAULT_LIMIT, MAX_LIMIT, select_endpoint

#: What the ``dataset`` column shows for a Speed Insights preset, which has no
#: dataset in the Web Analytics sense: it queries one metric at a time.
SPEED_DATASET = "speed"

#: What the ``dataset`` column shows for a request logs preset, which has no
#: dataset in the Web Analytics sense either: it queries rows, not groups.
LOGS_DATASET = "logs"

#: The metric a Speed Insights preset reports when the user names none.
DEFAULT_METRIC = "lcp"


@dataclass(frozen=True)
class Preset:
    """A named bundle of defaults. Any explicit flag overrides a preset value."""

    name: str
    dataset: str
    group_by: tuple[str, ...]
    limit: int | None
    description: str
    calls: int = 1
    #: Which API this preset queries.
    surface: str = WEB_ANALYTICS
    #: Speed Insights only. ``None`` means ``--metric`` decides, defaulting to
    #: :data:`DEFAULT_METRIC`; ``"*"`` means every vital, one query each.
    metric: str | None = None
    #: Speed Insights only, overriding the percentile default.
    aggregation: str | None = None
    order_by: str | None = None
    order: str | None = None
    #: Speed Insights only, already spelled the way that surface spells it.
    granularity: str | None = None
    #: Speed Insights only: query the ``*_count`` metric instead of the value.
    data_points: bool = False
    #: A per-surface window default, overriding the global one. Only the logs
    #: presets set it: runtime logs are retained for an hour on Hobby, so a 7
    #: day default there would report nothing and read as a healthy site.
    default_since: str | None = None

    @property
    def is_speed(self) -> bool:
        """True when this preset queries the Speed Insights surface."""
        return self.surface == SPEED_INSIGHTS

    @property
    def is_logs(self) -> bool:
        """True when this preset queries the request logs surface."""
        return self.surface == LOGS

    @property
    def endpoint(self) -> str:
        """The endpoint this preset hits, for display purposes."""
        if self.is_logs:
            endpoint = "request-logs"
        elif self.is_speed:
            endpoint = "query"
        else:
            endpoint = select_endpoint(list(self.group_by))
        if self.calls > 1:
            return f"{self.calls} x {endpoint}"
        return endpoint


PRESETS: dict[str, Preset] = {
    "overview": Preset(
        name="overview",
        dataset="visits",
        group_by=("day",),
        limit=OVERVIEW_TABLE_LIMIT,
        description="Totals, a daily trend, top pages and top referrers",
        calls=3,
    ),
    "trend": Preset(
        name="trend",
        dataset="visits",
        group_by=("day",),
        limit=MAX_LIMIT,
        description="Page views over time (change buckets with --granularity)",
    ),
    "top-pages": Preset(
        name="top-pages",
        dataset="visits",
        group_by=("requestPath",),
        limit=DEFAULT_LIMIT,
        description="Most viewed URL paths",
    ),
    "top-routes": Preset(
        name="top-routes",
        dataset="visits",
        group_by=("route",),
        limit=DEFAULT_LIMIT,
        description="Most viewed framework routes, for example /blog/[slug]",
    ),
    "referrers": Preset(
        name="referrers",
        dataset="visits",
        group_by=("referrerHostname",),
        limit=DEFAULT_LIMIT,
        description="Where the traffic came from",
    ),
    "countries": Preset(
        name="countries",
        dataset="visits",
        group_by=("country",),
        limit=DEFAULT_LIMIT,
        description="Traffic by country",
    ),
    "devices": Preset(
        name="devices",
        dataset="visits",
        group_by=("deviceType",),
        limit=DEFAULT_LIMIT,
        description="Traffic by device type",
    ),
    "browsers": Preset(
        name="browsers",
        dataset="visits",
        group_by=("browserName",),
        limit=DEFAULT_LIMIT,
        description="Traffic by browser",
    ),
    "operating-systems": Preset(
        name="operating-systems",
        dataset="visits",
        group_by=("osName",),
        limit=DEFAULT_LIMIT,
        description="Traffic by operating system",
    ),
    "campaigns": Preset(
        name="campaigns",
        dataset="visits",
        group_by=("utmCampaign",),
        limit=DEFAULT_LIMIT,
        description="Traffic by utm_campaign (needs Web Analytics Plus)",
    ),
    "events": Preset(
        name="events",
        dataset="events",
        group_by=("eventName",),
        limit=DEFAULT_LIMIT,
        description="Custom events, plus --event-property NAME to break one out",
    ),
    "total": Preset(
        name="total",
        dataset="visits",
        group_by=(),
        limit=None,
        description="One ungrouped total from the count endpoint",
    ),
    "vitals": Preset(
        name="vitals",
        dataset=SPEED_DATASET,
        group_by=(),
        limit=None,
        description="P75 of all five web vitals against their targets",
        calls=5,
        surface=SPEED_INSIGHTS,
        metric="*",
    ),
    "slowest-pages": Preset(
        name="slowest-pages",
        dataset=SPEED_DATASET,
        group_by=("route",),
        limit=SPEED_DEFAULT_LIMIT,
        description="Routes with the worst P75 LCP, worst first",
        surface=SPEED_INSIGHTS,
        metric="lcp",
        order_by="value",
        order="desc",
    ),
    "fastest-pages": Preset(
        name="fastest-pages",
        dataset=SPEED_DATASET,
        group_by=("route",),
        limit=SPEED_DEFAULT_LIMIT,
        description="Routes with the best P75 LCP, best first",
        surface=SPEED_INSIGHTS,
        metric="lcp",
        order_by="value",
        order="asc",
    ),
    "vitals-by-country": Preset(
        name="vitals-by-country",
        dataset=SPEED_DATASET,
        group_by=("country",),
        limit=SPEED_DEFAULT_LIMIT,
        description=f"P75 of --metric (default {DEFAULT_METRIC}) by country",
        surface=SPEED_INSIGHTS,
    ),
    "vitals-by-device": Preset(
        name="vitals-by-device",
        dataset=SPEED_DATASET,
        group_by=("device_type",),
        limit=SPEED_DEFAULT_LIMIT,
        description=f"P75 of --metric (default {DEFAULT_METRIC}) by device type",
        surface=SPEED_INSIGHTS,
    ),
    "vitals-trend": Preset(
        name="vitals-trend",
        dataset=SPEED_DATASET,
        group_by=(),
        limit=None,
        description=f"P75 of --metric (default {DEFAULT_METRIC}) over time",
        surface=SPEED_INSIGHTS,
        granularity="1d",
    ),
    "metric": Preset(
        name="metric",
        dataset=SPEED_DATASET,
        group_by=(),
        limit=SPEED_DEFAULT_LIMIT,
        description="Any metric by id, for example --metric vercel.request.count",
        surface=SPEED_INSIGHTS,
    ),
    "data-points": Preset(
        name="data-points",
        dataset=SPEED_DATASET,
        group_by=("route",),
        limit=SPEED_DEFAULT_LIMIT,
        description="How many measurements each route contributed",
        surface=SPEED_INSIGHTS,
        aggregation=COUNT_AGGREGATION,
        data_points=True,
    ),
    "logs": Preset(
        name="logs",
        dataset=LOGS_DATASET,
        group_by=(),
        limit=LOGS_DEFAULT_LIMIT,
        description="Recent requests, newest first, whatever their status",
        surface=LOGS,
        default_since="1h",
    ),
    "errors": Preset(
        name="errors",
        dataset=LOGS_DATASET,
        group_by=(),
        limit=LOGS_DEFAULT_LIMIT,
        description="Failing requests: 5xx responses and logged error lines",
        calls=2,
        surface=LOGS,
        default_since="1h",
    ),
    "error-summary": Preset(
        name="error-summary",
        dataset=LOGS_DATASET,
        group_by=(),
        limit=LOGS_MAX_LIMIT,
        description="The same errors grouped by status, route and message",
        calls=2,
        surface=LOGS,
        default_since="6h",
    ),
}

DEFAULT_PRESET = "overview"


def format_presets(style: Style = PLAIN_STYLE) -> str:
    """Render the preset table for ``--list-presets``."""
    headers = ["preset", "dataset", "endpoint", "grouping", "limit", "what it shows"]
    aligns = ["left", "left", "left", "left", "right", "left"]
    body: list[list[str]] = []
    for preset in PRESETS.values():
        name = preset.name + (" (default)" if preset.name == DEFAULT_PRESET else "")
        grouping = ", ".join(preset.group_by) if preset.group_by else "none"
        if preset.granularity:
            grouping = ", ".join([*preset.group_by, preset.granularity])
        if preset.name == "overview":
            grouping = "day, requestPath, referrerHostname"
        if preset.name == "events":
            grouping = "eventName [+ eventData/<property>]"
        body.append(
            [
                name,
                preset.dataset,
                preset.endpoint,
                grouping,
                str(preset.limit) if preset.limit is not None else "n/a",
                preset.description,
            ]
        )
    lines = [style.bold("Presets"), ""]
    lines.extend(render_grid(headers, aligns, body, None, style))
    lines.append("")
    lines.append(
        style.dim(
            "Any explicit flag overrides a preset value. Groups beyond the limit "
            f"roll into a single {OTHERS_LABEL!r} row rather than being dropped."
        )
    )
    lines.append(
        style.dim(
            f"A {SPEED_DATASET!r} preset queries Speed Insights, which reports one "
            "metric per request: pick it with --metric, and note that this API "
            "spells its dimensions in snake_case (request_path, device_type)."
        )
    )
    lines.append(
        style.dim(
            f"A {LOGS_DATASET!r} preset queries request logs, which has no groups: "
            "its limit counts requests, not groups, and it takes no --group-by "
            "and no --granularity."
        )
    )
    return "\n".join(lines)
