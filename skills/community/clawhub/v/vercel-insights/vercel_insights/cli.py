"""Argument parsing, settings resolution and ``main()``.

Usage
-----
    export VERCEL_TOKEN=...          # a Vercel access token
    export VERCEL_PROJECT_ID=prj_... # project id or project name

    python3 -m vercel_insights                        # 7 day overview
    python3 -m vercel_insights top-pages --since 30d  # a single table
    python3 -m vercel_insights events --event-property plan --json
    python3 -m vercel_insights vitals                 # the five web vitals

Run ``--list-presets`` for the full preset table and ``--help`` for every flag.
Add ``--dry-run`` to print the exact request that would be sent without sending
anything; it works even with no token configured.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, TextIO

import requests

from . import (
    DOCS_TOKEN_URL,
    OTHERS_LABEL,
    VERSION,
    ApiError,
    ConfigError,
    RateLimitError,
)
from .budgets import BUDGET_EXCEEDED, any_failed, evaluate, parse_budgets
from .http import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    PreparedRequest,
    execute,
    format_dry_run,
    redact_headers,
    scrub_credentials,
    validate_timeout,
    validate_token,
)
from .logs import DEFAULT_LIMIT as LOGS_DEFAULT_LIMIT
from .logs import LEVELS as LOG_LEVELS
from .logs import MAX_LIMIT as LOGS_MAX_LIMIT
from .logs import OPERATION as REQUEST_LOGS_QUERY
from .logs import (
    SOURCE_ALIAS_NOTE,
    error_filter_sets,
    method_warning,
    normalize_method,
    summarize,
    validate_levels,
    validate_sources,
    validate_status_code,
)
from .logs import SOURCES as LOG_SOURCES
from .logs import build_report as build_log_report
from .logs import build_request as build_logs_request
from .logs import collect as collect_logs
from .logs import merge as merge_logs
from .logs import validate_limit as validate_logs_limit
from .odata import build_clause, combine_filters, json_dimension
from .presets import DEFAULT_METRIC, DEFAULT_PRESET, PRESETS, Preset, format_presets
from .projects import (
    build_list_request as build_projects_request,
)
from .projects import (
    build_one_request as build_project_request,
)
from .projects import (
    extract_projects,
    format_projects,
    looks_like_project_id,
    owner_from_project,
    resolve_project_id,
)
from .render import (
    DATA_POINTS_METRIC,
    OVERVIEW_TABLE_LIMIT,
    LogEntry,
    LogReport,
    Result,
    Style,
    _result_document,
    format_csv,
    format_json,
    format_logs_csv,
    format_logs_json,
    format_table,
    format_value,
    render_error_summary,
    render_logs,
    render_overview,
    render_vitals,
)
from .speedinsights import (
    COUNT_AGGREGATION,
    DEFAULT_AGGREGATION,
    KNOWN_AGGREGATIONS,
    METRIC_HELP,
    ORDER_BY_VALUES,
    ORDER_DIRECTIONS,
    PERCENTILES,
    SPEED_DIMENSIONS,
    VITAL_ORDER,
    Metric,
    build_schema_request,
    format_schema,
    metric_for,
    validate_aggregation,
    validate_metric,
    validate_percentile,
    warn_if_not_project_id,
)
from .speedinsights import DATASET as SPEED_INSIGHTS_DATASET
from .speedinsights import (
    METRICS as KNOWN_METRICS,
)
from .speedinsights import OPERATION as OBSERVABILITY_QUERY
from .speedinsights import build_request as build_speed_request
from .speedinsights import normalize as normalize_speed
from .speedinsights import validate_group_by as validate_speed_group_by
from .speedinsights import validate_limit as validate_speed_limit
from .timerange import (
    ACCEPTED_GRANULARITIES,
    LOGS,
    SPEED_INSIGHTS,
    SURFACE_LABELS,
    SURFACES,
    TIME_GRANULARITIES,
    TIME_HELP,
    WEB_ANALYTICS,
    granularity_meaning,
    normalize_granularity,
    reporting_window_warning,
    resolve_range,
    to_api_timestamp,
)
from .webanalytics import (
    DATASETS,
    DEFAULT_LIMIT,
    MAX_LIMIT,
    MIN_LIMIT,
    VISIT_DIMENSIONS,
    build_request,
    normalize,
    select_endpoint,
    validate_group_by,
    validate_limit,
)

PROG = "vercel-insights"

DEFAULT_SINCE = "7d"
DEFAULT_UNTIL = "now"

EPILOG = f"""\
examples:
  # Last 7 days at a glance for the configured project
  {PROG}

  # Top 20 pages over the last 30 days, US traffic only
  {PROG} top-pages --limit 20 --since 30d --country US

  # Daily page view trend for one framework route, as CSV
  {PROG} trend --route '/blog/[slug]' --since 4w --csv

  # Custom events broken down by the "plan" event property
  {PROG} events --event-property plan --since 30d --json

  # Show exactly what would be requested, and send nothing
  {PROG} referrers --since 2026-01-01 --until 2026-02-01 --dry-run

  # The five web vitals at P75, against Vercel's published targets
  {PROG} vitals --since 7d

  # The slowest routes by P75 LCP, on mobile only
  {PROG} slowest-pages --device mobile --limit 20

  # Daily P75 INP for one route, production traffic only
  {PROG} vitals-trend --metric inp --route '/blog/[slug]' --environment production

environment:
  VERCEL_TOKEN       access token, used only in the Authorization header
  VERCEL_PROJECT_ID  project id or project name
  VERCEL_TEAM_ID     team id, for team owned projects
  VERCEL_TEAM_SLUG   team slug, an alternative to the team id
  VERCEL_OWNER_ID    account id owning the project (Speed Insights scope)
  NO_COLOR           set to any value to disable colour

exit codes:
  0 success, including an empty result set
  1 the API returned an error, or the network failed after retries
  2 configuration or usage error
  130 interrupted
"""


def _preset_window_phrase() -> str:
    """Name every preset that owns a window default, as ``--since``'s help says it.

    Composed from :data:`PRESETS` rather than written out, because the two used
    to be separate strings with nothing keeping them in step: the help said "1h
    on the logs and errors presets and 6h on error-summary" while the preset
    table was free to move underneath it.

    Returns:
        A phrase such as ``1h on logs and errors, 6h on error-summary``, in the
        order the preset table lists them, or ``""`` when no preset owns one.
    """
    grouped: dict[str, list[str]] = {}
    for name, preset in PRESETS.items():
        if preset.default_since:
            grouped.setdefault(preset.default_since, []).append(name)
    parts: list[str] = []
    for since, names in grouped.items():
        if len(names) > 1:
            listed = f"{', '.join(names[:-1])} and {names[-1]}"
        else:
            listed = names[0]
        parts.append(f"{since} on {listed}")
    return ", ".join(parts)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser. The help text doubles as the reference docs."""
    parser = argparse.ArgumentParser(
        prog=PROG,
        description=(
            "Query the Vercel Web Analytics, Speed Insights and request logs "
            "APIs from the command line. Read only: every request comes from a "
            "fixed operation allowlist, and the access token is sent only in "
            "the Authorization header."
        ),
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "preset",
        nargs="?",
        choices=sorted(PRESETS),
        default=None,
        help=(
            f"what to report; defaults to {DEFAULT_PRESET}. "
            "Run --list-presets for the full table"
        ),
    )

    config = parser.add_argument_group("configuration")
    config.add_argument(
        "--token",
        metavar="TOKEN",
        help="Vercel access token; defaults to $VERCEL_TOKEN. Not needed for --dry-run",
    )
    config.add_argument(
        "--project",
        metavar="ID_OR_NAME",
        help="project id or project name; defaults to $VERCEL_PROJECT_ID",
    )
    config.add_argument(
        "--team",
        metavar="TEAM_ID",
        help="team id for a team owned project; defaults to $VERCEL_TEAM_ID",
    )
    config.add_argument(
        "--team-slug",
        metavar="SLUG",
        help="team slug instead of a team id; defaults to $VERCEL_TEAM_SLUG",
    )
    config.add_argument(
        "--budget",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help=(
            "fail with exit code 3 when a web vital exceeds VALUE, for example "
            "--budget lcp=2500 or --budget cls=0.1; repeatable, and intended "
            "for CI. A metric with no data does not fail"
        ),
    )
    config.add_argument(
        "--list-projects",
        action="store_true",
        help=(
            "list the account's projects with their ids, and whether each has "
            "Web Analytics and Speed Insights data; use it to find what to "
            "pass to --project"
        ),
    )
    config.add_argument(
        "--list-metrics",
        nargs="?",
        const="",
        metavar="PREFIX",
        help=(
            "ask the API which metrics this account can actually query, "
            "optionally filtered by a prefix such as vercel.speed_insights; "
            "this is the source of truth when a query is refused"
        ),
    )
    config.add_argument(
        "--owner-id",
        metavar="ID",
        help=(
            "account that owns the project, required by a Speed Insights scope; "
            "defaults to $VERCEL_OWNER_ID, then to the team, then to the "
            "personal account read from the API"
        ),
    )

    shape = parser.add_argument_group("query shape")
    shape.add_argument(
        "--dataset",
        choices=DATASETS,
        default=None,
        help="which dataset to query; the preset picks one by default",
    )
    shape.add_argument(
        "--group-by",
        "--dimension",
        dest="group_by",
        metavar="DIMENSION",
        action="append",
        help=(
            "group rows by a dimension; repeatable up to 2. Visits accept: "
            + ", ".join(VISIT_DIMENSIONS)
            + ". Events also accept eventName and eventData/<property>. "
            "flags/<name> works on both. Speed Insights spells its dimensions "
            "in snake_case and accepts: " + ", ".join(SPEED_DIMENSIONS)
        ),
    )
    shape.add_argument(
        "--granularity",
        choices=ACCEPTED_GRANULARITIES,
        default=None,
        metavar="BUCKET",
        help=(
            "time bucket, replacing the preset's own: "
            + ", ".join(ACCEPTED_GRANULARITIES)
            + ". Both vocabularies are accepted and translated per API; week "
            "and year exist on Web Analytics only"
        ),
    )
    shape.add_argument(
        "--since",
        metavar="WHEN",
        # No default here: a preset may own one, and only an unset value can
        # tell "the user asked for 7d" apart from "nobody asked for anything".
        default=None,
        help=(
            f"start of the window (default: {DEFAULT_SINCE}, or "
            f"{_preset_window_phrase()}); {TIME_HELP}"
        ),
    )
    shape.add_argument(
        "--until",
        metavar="WHEN",
        default=DEFAULT_UNTIL,
        help=f"end of the window (default: {DEFAULT_UNTIL}); same forms as --since",
    )
    shape.add_argument(
        "--limit",
        metavar="N",
        type=int,
        default=None,
        help=(
            f"maximum number of groups, {MIN_LIMIT} to {MAX_LIMIT} "
            f"(preset default, usually {DEFAULT_LIMIT}); the rest roll into "
            f"one {OTHERS_LABEL!r} row. On a logs preset it counts rows rather "
            f"than groups, up to {LOGS_MAX_LIMIT}, and nothing rolls up"
        ),
    )
    shape.add_argument(
        "--event-property",
        metavar="NAME",
        default=None,
        help="break custom events down by this event property (events dataset)",
    )

    speed = parser.add_argument_group(
        "speed insights",
        "Only meaningful with a Speed Insights preset (vitals, slowest-pages, "
        "fastest-pages, vitals-by-country, vitals-by-device, vitals-trend, "
        "data-points). That API answers for one metric per request.",
    )
    speed.add_argument(
        "--metric",
        metavar="NAME",
        default=None,
        help=(
            f"which web vital to report: {METRIC_HELP}. Real Experience Score "
            "is not queryable through any API; read it on the dashboard"
        ),
    )
    speed.add_argument(
        "--percentile",
        metavar="N",
        type=int,
        default=None,
        help=(
            "percentile to report, one of "
            + ", ".join(str(value) for value in PERCENTILES)
            + f" (default {DEFAULT_AGGREGATION[1:]}, as on the dashboard)"
        ),
    )
    speed.add_argument(
        "--aggregation",
        metavar="NAME",
        default=None,
        help=(
            "aggregation to request instead of a percentile, for example "
            + ", ".join(KNOWN_AGGREGATIONS)
        ),
    )
    speed.add_argument(
        "--order-by",
        dest="order_by",
        metavar="COLUMN",
        default=None,
        help=(
            "rollup column to order grouped results by: "
            + ", ".join(ORDER_BY_VALUES)
            + " (default count, so a group with few data points does not lead)"
        ),
    )
    speed.add_argument(
        "--order",
        metavar="DIRECTION",
        default=None,
        help="order grouped results " + " or ".join(ORDER_DIRECTIONS) + " (default desc)",
    )
    speed.add_argument(
        "--bucket-timezone",
        dest="bucket_timezone",
        metavar="IANA",
        default=None,
        help=(
            "IANA zone aligning daily and monthly buckets, for example "
            "Europe/Paris; timestamps stay UTC and sub-daily buckets ignore it"
        ),
    )
    speed.add_argument(
        "--all",
        dest="all_projects",
        action="store_true",
        help="query every project in the team; mutually exclusive with --project",
    )
    speed.add_argument(
        "--data-points",
        dest="data_points",
        action="store_true",
        help=(
            "report how many measurements were collected instead of the metric "
            "value; a percentile over few data points is not comparable to one "
            "over many"
        ),
    )

    logs = parser.add_argument_group(
        "request logs",
        "Only meaningful with a logs preset (logs, errors, error-summary). This "
        "API returns rows of text rather than aggregated numbers, and filters "
        "with query parameters rather than OData.",
    )
    logs.add_argument(
        "--level",
        metavar="LEVEL",
        default=None,
        help=(
            "only requests that logged a line at one of these levels: "
            + ", ".join(LOG_LEVELS)
            + ", comma separated. Note that this matches application log lines "
            "only, so a 5xx that printed nothing does not match"
        ),
    )
    logs.add_argument(
        "--status-code",
        dest="status_code",
        metavar="CODE",
        default=None,
        help=(
            "only responses with this status: an integer such as 500, a class "
            "such as 5xx, None for requests with no status recorded, or a comma "
            "separated mix"
        ),
    )
    logs.add_argument(
        "--source",
        metavar="SOURCE",
        default=None,
        help=(
            "only requests served by: "
            + ", ".join(LOG_SOURCES)
            # Composed in logs.py from the alias table itself, so this help and
            # the refusal that quotes the same fact cannot drift from it.
            + f", comma separated. {SOURCE_ALIAS_NOTE}"
        ),
    )
    logs.add_argument(
        "--method",
        metavar="METHOD",
        default=None,
        help="only this HTTP method, for example POST",
    )
    logs.add_argument(
        "--search",
        metavar="TEXT",
        default=None,
        help=(
            "only requests whose path or log text contains this; free text and "
            "nothing more, not a query syntax, so do not expect 'status:500' to "
            "filter by status: use --status-code for that"
        ),
    )
    logs.add_argument(
        "--request-id",
        dest="request_id",
        metavar="ID",
        default=None,
        help="one request, by the id shown in the table",
    )
    logs.add_argument(
        "--branch",
        metavar="NAME",
        default=None,
        help="only deployments built from this git branch",
    )
    logs.add_argument(
        "--deployment",
        metavar="ID",
        default=None,
        help="only this deployment, by its dpl_ id",
    )
    logs.add_argument(
        "--expand",
        action="store_true",
        help="print each full log message under its row instead of truncating it",
    )

    filters = parser.add_argument_group(
        "filters",
        "Each flag adds one OData clause; all clauses are joined with 'and'. "
        "A comma separated value becomes an 'in (...)' set. A logs preset has "
        "only --path, --route and --environment, which become exact match query "
        "parameters there; --search is the substring tool on that surface.",
    )
    filters.add_argument("--path", metavar="PATH", help="requestPath, exact URL path")
    filters.add_argument("--route", metavar="ROUTE", help="route, framework pattern")
    filters.add_argument("--country", metavar="CODE", help="country, ISO code")
    filters.add_argument("--device", metavar="TYPE", help="deviceType")
    filters.add_argument("--browser", metavar="NAME", help="browserName")
    filters.add_argument("--os", metavar="NAME", dest="os_name", help="osName")
    filters.add_argument("--referrer", metavar="HOST", help="referrerHostname")
    filters.add_argument("--utm-source", metavar="VALUE", help="utmSource")
    filters.add_argument("--utm-medium", metavar="VALUE", help="utmMedium")
    filters.add_argument("--utm-campaign", metavar="VALUE", help="utmCampaign")
    filters.add_argument(
        "--event-name", metavar="NAME", help="eventName (events dataset only)"
    )
    filters.add_argument(
        "--flag",
        metavar="NAME=VALUE",
        action="append",
        help="feature flag clause, for example --flag beta_banner=true; repeatable",
    )
    filters.add_argument(
        "--environment",
        choices=("production", "preview"),
        default=None,
        help="environment; aggregate queries default to production",
    )
    filters.add_argument(
        "--filter",
        metavar="ODATA",
        action="append",
        dest="raw_filters",
        help="raw OData clause, appended verbatim; repeatable",
    )

    output = parser.add_argument_group("output and behaviour")
    output.add_argument(
        "--json", action="store_true", help="machine readable JSON output"
    )
    output.add_argument("--csv", action="store_true", help="CSV output")
    output.add_argument(
        "--dry-run",
        action="store_true",
        help="print the request that would be sent and send nothing; needs no token",
    )
    output.add_argument(
        "--timeout",
        metavar="SECONDS",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"per request timeout (default: {DEFAULT_TIMEOUT})",
    )
    output.add_argument(
        "--max-retries",
        metavar="N",
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help=(
            f"retries after the first attempt (default: {DEFAULT_MAX_RETRIES}); "
            "only 408, 429 and 5xx responses and network failures are retried"
        ),
    )
    output.add_argument(
        "--no-color", action="store_true", help="disable colour; NO_COLOR works too"
    )
    output.add_argument(
        "--verbose", action="store_true", help="diagnostics on stderr, never the token"
    )
    output.add_argument(
        "--list-presets", action="store_true", help="print the preset table and exit"
    )
    output.add_argument(
        "--version", action="store_true", help="print the version and exit"
    )
    return parser


@dataclass
class Settings:
    """Everything one run needs, after flags, env and preset have been merged."""

    preset: Preset
    dataset: str
    project: str
    token: str | None
    team: str | None
    team_slug: str | None
    group_by: list[str]
    limit: int | None
    filter_expr: str | None
    time_range: tuple[datetime, datetime]
    timeout: float = DEFAULT_TIMEOUT
    warnings: list[str] = field(default_factory=list)
    #: Which API this run talks to, decided by the preset.
    surface: str = WEB_ANALYTICS
    #: Speed Insights only: the metrics to query, one request each. The vitals
    #: preset holds five; every other Speed Insights preset holds one.
    metrics: tuple[Metric, ...] = ()
    #: ``None`` for a metric outside the web vitals, where the server's own
    #: default is better than any guess this client could make.
    aggregation: str | None = DEFAULT_AGGREGATION
    all_projects: bool = False
    order_by: str | None = None
    order_direction: str | None = None
    granularity: str | None = None
    bucket_timezone: str | None = None
    #: Speed Insights and request logs. A scope requires an ownerId, and for a
    #: team the team id IS the owner. For a personal account it is read once
    #: from the project's own record at run time, because nothing else knows it.
    owner_id: str | None = None
    #: Request logs only: wire-named filter values, keyed by
    #: :data:`logs.FILTER_PARAMS`. Empty on the other two surfaces, which filter
    #: with an OData expression in :attr:`filter_expr` instead.
    log_filters: dict[str, str] = field(default_factory=dict)

    @property
    def aggregation_label(self) -> str:
        """What to call the value column when no aggregation was requested.

        The request omits the field so the server applies the metric's own
        default, but a column still needs a name, and "value" is honest where a
        specific aggregation was never asked for.
        """
        return self.aggregation or "value"

    @property
    def is_speed(self) -> bool:
        """True when this run queries the Speed Insights surface."""
        return self.surface == SPEED_INSIGHTS

    @property
    def is_logs(self) -> bool:
        """True when this run queries the request logs surface."""
        return self.surface == LOGS

    @property
    def project_label(self) -> str:
        """How to name what was queried, in a heading or an empty result line."""
        return self.project or "every project in the team"


def _env_value(env: Mapping[str, str], name: str) -> str | None:
    value = env.get(name)
    return value.strip() or None if value else None


#: Every filter shorthand, in the order its clause is emitted, with the name it
#: compiles to on each surface: the flag, then Web Analytics, Speed Insights and
#: request logs in that order. The three APIs name the same thing differently,
#: so the spelling follows the surface the query is going to, and ``None`` marks
#: a shorthand that surface has no dimension for at all. On the logs surface
#: these names are query parameters rather than OData dimensions.
FILTER_SHORTHANDS: tuple[tuple[str, str, str | None, str | None], ...] = (
    ("--path", "requestPath", "request_path", "requestPath"),
    ("--route", "route", "route", "route"),
    ("--country", "country", "country", None),
    ("--device", "deviceType", "device_type", None),
    ("--browser", "browserName", None, None),
    ("--os", "osName", None, None),
    ("--referrer", "referrerHostname", None, None),
    ("--utm-source", "utmSource", None, None),
    ("--utm-medium", "utmMedium", None, None),
    ("--utm-campaign", "utmCampaign", None, None),
    ("--environment", "environment", "environment", "environment"),
)

#: What the request logs surface can filter on, named as the user writes it.
#: The wire parameter names live in :data:`logs.FILTER_PARAMS`; these are the
#: flags that reach them, which is what a refusal should tell the reader to use.
LOGS_FILTER_FLAGS: tuple[str, ...] = (
    "--path",
    "--route",
    "--environment",
    "--level",
    "--status-code",
    "--source",
    "--method",
    "--branch",
    "--deployment",
    "--request-id",
    "--search",
)

#: For each surface that lacks some shorthand's dimension: how that surface is
#: named in the refusal, and what it does filter on instead. Web Analytics is
#: absent because every shorthand compiles there, so the refusal cannot arise
#: for it.
_NO_DIMENSION_HELP: dict[str, tuple[str, tuple[str, ...]]] = {
    SPEED_INSIGHTS: ("Speed Insights", SPEED_DIMENSIONS),
    LOGS: ("the request logs API", LOGS_FILTER_FLAGS),
}


def _shorthand_values(args: argparse.Namespace) -> dict[str, str | None]:
    """What the user passed for each shorthand, keyed by the flag itself."""
    return {
        "--path": args.path,
        "--route": args.route,
        "--country": args.country,
        "--device": args.device,
        "--browser": args.browser,
        "--os": args.os_name,
        "--referrer": args.referrer,
        "--utm-source": args.utm_source,
        "--utm-medium": args.utm_medium,
        "--utm-campaign": args.utm_campaign,
        "--environment": args.environment,
    }


def _resolve_filters(
    args: argparse.Namespace, dataset: str, surface: str = WEB_ANALYTICS
) -> str | None:
    """Turn every filter flag into one combined OData expression.

    A shorthand compiles to the dimension name of the surface the query is
    actually going to, and a shorthand the active surface has no dimension for
    is a configuration error naming why, never a clause the API would reject.
    """
    values = _shorthand_values(args)

    clauses: list[str] = []
    for flag, web_name, speed_name, logs_name in FILTER_SHORTHANDS:
        value = values[flag]
        if not value:
            continue
        if surface == SPEED_INSIGHTS:
            dimension = speed_name
        elif surface == LOGS:
            dimension = logs_name
        else:
            dimension = web_name
        if dimension is None:
            # Looked up rather than indexed: a future shorthand with no Web
            # Analytics dimension would reach a surface this table has no entry
            # for, and a KeyError traceback is a worse answer than a ConfigError
            # that names one thing less.
            subject, filterable = _NO_DIMENSION_HELP.get(
                surface, (SURFACE_LABELS[surface], ())
            )
            alternatives = (
                f"That surface filters on {', '.join(filterable)}. "
                if filterable
                else ""
            )
            raise ConfigError(
                f"{flag} {value!r} is a Web Analytics filter: {subject} "
                f"collects no {web_name} dimension, so it cannot filter on one. "
                f"{alternatives}Drop the flag, or run a Web Analytics preset instead"
            )
        clauses.append(build_clause(dimension, value))

    if args.event_name:
        if dataset != "events":
            raise ConfigError(
                f"--event-name {args.event_name!r} only exists on the events "
                "dataset; add --dataset events (or use the events preset)"
            )
        clauses.append(build_clause("eventName", args.event_name))

    for raw_flag in args.flag or []:
        name, separator, value = str(raw_flag).partition("=")
        if not separator or not name.strip():
            raise ConfigError(
                f"--flag {raw_flag!r} is not in NAME=VALUE form; write it as "
                "--flag beta_banner=true"
            )
        clauses.append(build_clause(json_dimension("flags", name), value.strip()))

    for raw in args.raw_filters or []:
        text = str(raw).strip()
        if text:
            clauses.append(text)

    return combine_filters(clauses)


def _resolve_log_filters(
    args: argparse.Namespace, warnings: list[str]
) -> dict[str, str]:
    """Turn every logs filter flag into the query parameters the API takes.

    This is the one place a flag becomes a wire parameter on this surface, and
    each value goes through its validator here, before a request exists, because
    the API answers an unknown level or source with HTTP 200 and zero rows: an
    unchecked typo would read as a healthy site.

    ``--method`` is the one vocabulary warned about rather than refused: a custom
    HTTP method is legal, so refusing an unknown one would remove capability,
    while saying nothing would leave the same zero-rows trap unmarked.

    Args:
        args: The parsed arguments.
        warnings: Collector for anything worth saying on stderr without failing
            the run, the same list :class:`Settings` carries.

    Returns:
        Wire-named filters, keyed by :data:`logs.FILTER_PARAMS`.

    Raises:
        ConfigError: From any validator, naming the flag and the accepted set.
    """
    filters: dict[str, str] = {}
    if args.level:
        filters["level"] = validate_levels(args.level)
    if args.status_code:
        filters["statusCode"] = validate_status_code(args.status_code)
    if args.source:
        filters["source"] = validate_sources(args.source)
    if args.method:
        # The API records the method in upper case, and matches it exactly.
        method = normalize_method(str(args.method))
        filters["requestMethod"] = method
        warning = method_warning(method)
        if warning:
            warnings.append(warning)
    if args.path:
        filters["requestPath"] = args.path
    if args.route:
        filters["route"] = args.route
    if args.environment:
        filters["environment"] = args.environment
    if args.branch:
        filters["branch"] = args.branch
    if args.deployment:
        filters["deploymentId"] = args.deployment
    if args.request_id:
        filters["requestId"] = args.request_id
    if args.search:
        filters["search"] = args.search
    return filters


def _resolve_group_by(args: argparse.Namespace, preset: Preset) -> list[str]:
    """Merge the preset grouping with --group-by, --granularity and the sugar."""
    explicit = [dim for dim in (args.group_by or []) if dim]
    if explicit:
        group_by = list(explicit)
    else:
        group_by = list(preset.group_by)

    if args.granularity:
        if not explicit:
            group_by = [dim for dim in group_by if dim not in TIME_GRANULARITIES]
        group_by.append(normalize_granularity(args.granularity, WEB_ANALYTICS))

    if args.event_property:
        group_by.append(json_dimension("eventData", args.event_property))

    return group_by


#: Every option that is not meaningful on every surface: the argparse attribute,
#: the flag as the user writes it, the surfaces it does mean something on, and
#: the reason it means nothing elsewhere. One table rather than one per surface,
#: because with three surfaces the pairwise version stops being readable. The
#: filter shorthands are absent: :data:`FILTER_SHORTHANDS` already knows which
#: surface has which dimension, and refuses the rest there.
SURFACE_OPTIONS: tuple[tuple[str, str, frozenset[str], str], ...] = (
    # Speed Insights only.
    ("metric", "--metric", frozenset({SPEED_INSIGHTS}),
     "only Speed Insights reports a metric per request"),
    ("percentile", "--percentile", frozenset({SPEED_INSIGHTS}),
     "a percentile only means something over a distribution of measurements"),
    ("aggregation", "--aggregation", frozenset({SPEED_INSIGHTS}),
     "an aggregation combines a distribution of measurements, and only Speed "
     "Insights collects one"),
    ("order_by", "--order-by", frozenset({SPEED_INSIGHTS}),
     "only Speed Insights returns the rollup columns this orders by"),
    ("order", "--order", frozenset({SPEED_INSIGHTS}),
     "only Speed Insights takes an order for its grouped rows"),
    ("bucket_timezone", "--bucket-timezone", frozenset({SPEED_INSIGHTS}),
     "only Speed Insights aligns its time buckets to a zone"),
    ("all_projects", "--all", frozenset({SPEED_INSIGHTS}),
     "only Speed Insights can answer for every project in one request"),
    ("data_points", "--data-points", frozenset({SPEED_INSIGHTS}),
     "only Speed Insights counts the measurements behind a value"),
    ("budget", "--budget", frozenset({SPEED_INSIGHTS}),
     "a budget compares a measured value against a threshold, and only Speed "
     "Insights reports one"),
    # Web Analytics only. Each reason has to hold on both of the other two
    # surfaces, since either can be the one refusing.
    ("dataset", "--dataset", frozenset({WEB_ANALYTICS}),
     "neither Speed Insights nor request logs has datasets; Speed Insights "
     "queries one metric at a time, chosen with --metric, and request logs "
     "answer with rows"),
    ("event_name", "--event-name", frozenset({WEB_ANALYTICS}),
     "neither Speed Insights nor request logs collect custom events"),
    ("event_property", "--event-property", frozenset({WEB_ANALYTICS}),
     "neither Speed Insights nor request logs collect custom events, so "
     "neither has event properties to break out"),
    ("flag", "--flag", frozenset({WEB_ANALYTICS}),
     "neither Speed Insights nor request logs collect feature flag values"),
    # Request logs only.
    ("level", "--level", frozenset({LOGS}),
     "only the request logs API records a log level"),
    ("status_code", "--status-code", frozenset({LOGS}),
     "only the request logs API reports a response status per request"),
    ("source", "--source", frozenset({LOGS}),
     "only the request logs API says what served a request"),
    # These two are claims about what this client's analytics surfaces filter
    # on, not about what the APIs behind them could do: the observability API
    # publishes an HTTP method and a deployment among a metric's dimensions, and
    # a future change here could reach them. Overstating that would be a fact
    # this table cannot support.
    ("method", "--method", frozenset({LOGS}),
     "neither analytics surface here filters by HTTP method"),
    ("search", "--search", frozenset({LOGS}),
     "there is no log text to search on an analytics surface"),
    ("request_id", "--request-id", frozenset({LOGS}),
     "an analytics row is an aggregate, not one request"),
    ("branch", "--branch", frozenset({LOGS}),
     "neither analytics API records the git branch"),
    ("deployment", "--deployment", frozenset({LOGS}),
     "neither analytics surface here filters by deployment"),
    ("expand", "--expand", frozenset({LOGS}),
     "there is no log message to expand"),
    # Both analytics surfaces, but not request logs.
    ("group_by", "--group-by", frozenset({WEB_ANALYTICS, SPEED_INSIGHTS}),
     "request logs are rows rather than buckets, so there is nothing to group; "
     "use the error-summary preset, which groups by status, route and message"),
    ("granularity", "--granularity", frozenset({WEB_ANALYTICS, SPEED_INSIGHTS}),
     "request logs are rows rather than time buckets"),
    ("raw_filters", "--filter", frozenset({WEB_ANALYTICS, SPEED_INSIGHTS}),
     "the request logs API takes no OData; filter with "
     + ", ".join(LOGS_FILTER_FLAGS)),
)


def _surface_phrase(surfaces: frozenset[str]) -> str:
    """Name the surfaces in prose, for example ``Speed Insights surface``.

    Args:
        surfaces: The surfaces an option means something on.

    Returns:
        The labels in a fixed order, singular or plural as the count needs.
    """
    labels = [SURFACE_LABELS[name] for name in SURFACES if name in surfaces]
    if len(labels) == 1:
        return f"{labels[0]} surface"
    return f"{' and '.join(labels)} surfaces"


def _preset_names(surfaces: frozenset[str]) -> str:
    """The presets that query any of ``surfaces``, comma separated.

    Every refusal names where the flag does work, because a message that only
    says "not here" leaves the reader with nothing to try next.

    Args:
        surfaces: The surfaces an option means something on.

    Returns:
        The preset names in the order the preset table lists them.
    """
    return ", ".join(
        name for name, preset in PRESETS.items() if preset.surface in surfaces
    )


#: A bucket timezone is an IANA zone name such as ``Europe/Paris`` or ``UTC``.
_TIMEZONE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+_-]*(/[A-Za-z0-9+_.-]+){0,2}$")


def _reject_cross_surface_options(args: argparse.Namespace, preset: Preset) -> None:
    """Rules 14, 15 and 22: an option used on the surface it does not belong to.

    Walks :data:`SURFACE_OPTIONS` once, in all three directions: the preset
    decides the surface, and an option not meaningful there is refused with the
    reason and the presets it does work on. An option that is silently ignored
    instead is the failure this exists to prevent, because a flag that promises
    something and does nothing is worse than a flag that is refused.

    Rule 14 goes first, because ``--dataset`` with ``--metric`` names a conflict
    between two options rather than between an option and a preset, and that
    is the more specific complaint.

    Args:
        args: The parsed arguments.
        preset: The preset this run uses, which names the active surface.

    Raises:
        ConfigError: Naming the flag, the surface the preset queries, why the
            flag means nothing there, and the presets it does work on.
    """
    if args.dataset and args.metric:
        raise ConfigError(
            f"--dataset {args.dataset!r} and --metric {args.metric!r} select "
            "different APIs and are mutually exclusive: --dataset queries Web "
            "Analytics page views or custom events, --metric queries a Speed "
            "Insights web vital. Keep one, and pick a preset for that surface"
        )

    for attribute, flag, surfaces, reason in SURFACE_OPTIONS:
        value = getattr(args, attribute)
        # An appending option defaults to [] or None, and a store_true to
        # False, so "was it passed" is not the same question as "is it truthy".
        if value is None or value is False or value == []:
            continue
        if preset.surface in surfaces:
            continue
        if isinstance(value, bool):
            shown = ""
        elif isinstance(value, list):
            # An appending flag holds a list, and printing the list itself would
            # quote Python syntax back at a user who never typed any.
            shown = f" {', '.join(str(item) for item in value)!r}"
        else:
            shown = f" {value!r}"
        raise ConfigError(
            f"{flag}{shown} only applies to the {_surface_phrase(surfaces)}, "
            f"but the {preset.name} preset queries "
            f"{SURFACE_LABELS[preset.surface]}: {reason}. Run one of "
            f"{_preset_names(surfaces)}, or drop the flag"
        )


def _resolve_aggregation(
    args: argparse.Namespace, preset: Preset, metrics: Sequence[Metric]
) -> str | None:
    """Resolve the aggregation from --aggregation, --percentile or the preset.

    A data point count is a count, so when the user asked for one without
    naming an aggregation it is summed rather than run through the percentile
    default: the 75th percentile of a number of measurements answers nothing.
    """
    if args.aggregation and args.percentile is not None:
        raise ConfigError(
            f"--aggregation {args.aggregation!r} and --percentile "
            f"{args.percentile} both set the aggregation; --percentile "
            f"{args.percentile} is shorthand for --aggregation p{args.percentile}, "
            "so pass one of them"
        )
    if args.aggregation:
        return validate_aggregation(args.aggregation)
    if args.percentile is not None:
        return validate_percentile(args.percentile)
    if preset.aggregation:
        return preset.aggregation
    if metrics and all(metric.is_count for metric in metrics):
        return COUNT_AGGREGATION
    if metrics and any(metric.id not in KNOWN_METRICS for metric in metrics):
        # Outside the web vitals this client does not know what the metric
        # measures, and the 75th percentile of a request count answers nothing.
        # Omitting the field lets the server apply the metric's own default,
        # which the schema publishes and this client would only be copying.
        return None
    return DEFAULT_AGGREGATION


def _resolve_metrics(args: argparse.Namespace, preset: Preset) -> tuple[Metric, ...]:
    """Which metric or metrics this run queries, one request each."""
    if preset.metric == "*":
        return tuple(
            metric_for(short, data_points=args.data_points) for short in VITAL_ORDER
        )
    name = args.metric or preset.metric or DEFAULT_METRIC
    return (metric_for(name, data_points=args.data_points or preset.data_points),)


def _resolve_speed_ordering(
    args: argparse.Namespace, preset: Preset, group_by: Sequence[str]
) -> tuple[str | None, str | None]:
    """Rule 20: ordering applies to grouped results, so refuse it without one."""
    if (args.order_by or args.order) and not group_by:
        flags = " and ".join(
            flag
            for flag, value in (("--order-by", args.order_by), ("--order", args.order))
            if value
        )
        raise ConfigError(
            f"{flags} orders the rows of a grouped query, but this one is not "
            "grouped, so there is nothing to order. Add --group-by "
            f"{SPEED_DIMENSIONS[0]} (or run slowest-pages, vitals-by-country or "
            "another grouped preset), or drop the flag"
        )

    order_by = args.order_by or preset.order_by
    if order_by is not None and order_by not in ORDER_BY_VALUES:
        raise ConfigError(
            f"--order-by {order_by!r} is not a rollup column; the columns are "
            f"{', '.join(ORDER_BY_VALUES)}, where count is the number of data "
            "points behind each group and value is the metric itself"
        )

    order = args.order or preset.order
    if order is not None and order not in ORDER_DIRECTIONS:
        raise ConfigError(
            f"--order {order!r} is not a direction; pass "
            f"{' or '.join(ORDER_DIRECTIONS)}"
        )
    return order_by, order


def _resolve_bucket_timezone(
    args: argparse.Namespace, granularity: str | None, warnings: list[str]
) -> str | None:
    """Rule 21: a sub-daily bucket ignores the zone, so warn rather than refuse."""
    zone: str | None = args.bucket_timezone
    if not zone:
        return None
    if not _TIMEZONE_RE.match(zone):
        raise ConfigError(
            f"--bucket-timezone {zone!r} is not an IANA zone name; pass one such "
            "as Europe/Paris, America/New_York or UTC"
        )
    if granularity is not None and granularity_meaning(granularity) == "hour":
        warnings.append(
            f"--bucket-timezone {zone} aligns calendar buckets only, so it has "
            f"no effect at --granularity {args.granularity}; it is still sent, "
            "and the API ignores it. Use a daily or monthly bucket to see it work"
        )
    return zone


def _resolve_settings(args: argparse.Namespace, env: Mapping[str, str]) -> Settings:
    """Apply every validation rule, in order, before anything touches the network."""
    preset_name = args.preset
    if preset_name is None and args.metric:
        # Naming a metric is unambiguous about intent, and the default preset
        # reports traffic, which is a different API entirely. Without this the
        # only way to query one of the other 90-odd metrics would be to pick an
        # unrelated speed preset first, which reads like a workaround because
        # it is one.
        preset_name = "metric"
    preset = PRESETS[preset_name or DEFAULT_PRESET]

    if args.json and args.csv:
        raise ConfigError(
            "--json and --csv are mutually exclusive; pick one output format"
        )

    _reject_cross_surface_options(args, preset)
    speed = preset.is_speed
    dataset = args.dataset or preset.dataset

    if args.all_projects and args.project:
        raise ConfigError(
            f"--all and --project {args.project!r} are mutually exclusive: --all "
            "queries every project in the team, --project queries one. Keep one "
            "of them"
        )

    project = args.project or _env_value(env, "VERCEL_PROJECT_ID")
    if args.all_projects:
        project = None
    if not project and not args.all_projects:
        # Raised as its own type so main() can answer the question the user
        # actually has ("which projects do I have?") instead of only telling
        # them a flag is missing. One account holds many projects, so that
        # list is the whole answer.
        raise MissingProject(
            "no project configured; pass --project with a project id or name, "
            "or set VERCEL_PROJECT_ID in the environment"
            + (", or pass --all to query every project in the team" if speed else "")
        )

    token = args.token or _env_value(env, "VERCEL_TOKEN")
    if not token and not args.dry_run:
        raise ConfigError(
            "no access token configured; pass --token or set VERCEL_TOKEN "
            f"(create one at {DOCS_TOKEN_URL}). Use --dry-run to build the "
            "request without a token"
        )
    if token:
        token = validate_token(token)

    timeout = validate_timeout(args.timeout)

    team = args.team or _env_value(env, "VERCEL_TEAM_ID")
    team_slug = args.team_slug or _env_value(env, "VERCEL_TEAM_SLUG")
    # A team is its own owner, so a team id doubles as the ownerId a Speed
    # Insights scope requires. Only a personal account needs the lookup.
    # VERCEL_ORG_ID is Vercel's own name for the owning account, set by `vercel
    # link` and used across their tooling, so it is read before falling back to
    # the team. VERCEL_OWNER_ID is accepted too because it names what the API
    # field is actually called.
    owner_id = (
        args.owner_id
        or _env_value(env, "VERCEL_OWNER_ID")
        or _env_value(env, "VERCEL_ORG_ID")
        or team
    )
    if preset.surface in (SPEED_INSIGHTS, LOGS) and team_slug and not owner_id:
        # Both of these surfaces scope by an owning account: Speed Insights
        # through scope.ownerId and request logs through the ownerId parameter.
        # A slug names a team but is not an account id, so falling through to
        # the personal account lookup here would silently answer for the wrong
        # account rather than failing, which is the worst outcome available.
        raise ConfigError(
            f"--team-slug {team_slug!r} cannot scope a "
            f"{SURFACE_LABELS[preset.surface]} query on its own: that surface "
            "needs the account id, and a slug is a name. Pass --team with the "
            "team id (Team Settings, General), or --owner-id. A slug still "
            "works for Web Analytics presets"
        )
    if team and team_slug:
        raise ConfigError(
            f"--team ({team}) and --team-slug ({team_slug}) are mutually "
            "exclusive; keep one of them, and check VERCEL_TEAM_ID and "
            "VERCEL_TEAM_SLUG in case the environment supplies the other"
        )

    if preset.name == "overview" and (args.group_by or args.event_property):
        raise ConfigError(
            "the overview preset issues its own three queries, so --group-by and "
            "--event-property have no meaning there; use trend, top-pages, "
            "referrers or another preset to control the grouping"
        )

    if preset.name == "overview" and args.csv:
        raise ConfigError(
            "--csv needs a single table, but the overview preset issues three "
            "queries; use trend, top-pages or referrers with --csv instead"
        )

    if preset.name == "error-summary" and args.csv:
        raise ConfigError(
            "--csv needs a single table, but the error-summary preset tallies "
            "the same errors three ways; use the errors preset with --csv "
            "instead, which is one row per request"
        )

    if preset.metric == "*" and args.group_by:
        raise ConfigError(
            f"the {preset.name} preset issues one query per web vital, so "
            "--group-by has no meaning there; use vitals-by-country, "
            "vitals-by-device or --group-by with another Speed Insights preset"
        )

    if preset.metric == "*" and args.csv:
        raise ConfigError(
            f"--csv needs a single table, but the {preset.name} preset issues one "
            "query per web vital; use vitals-trend, slowest-pages or another "
            "single query preset with --csv instead"
        )

    if preset.metric == "*" and args.metric:
        # Validate the name first, so that naming something unqueryable gets
        # the specific answer rather than the generic one: --metric res must
        # say that Real Experience Score cannot be queried at all, which is
        # true of every preset, before this says that this preset reports all
        # five anyway.
        validate_metric(args.metric)
        raise ConfigError(
            f"--metric {args.metric!r} has no meaning on the {preset.name} "
            f"preset: {preset.name} reports all five web vitals, one query "
            "each. Use vitals-trend, vitals-by-country, vitals-by-device or "
            "slowest-pages for a single metric"
        )

    warnings: list[str] = []
    metrics: tuple[Metric, ...] = ()
    aggregation: str | None = DEFAULT_AGGREGATION
    granularity: str | None = None
    order_by: str | None = None
    order_direction: str | None = None
    bucket_timezone: str | None = None
    log_filters: dict[str, str] = {}

    if speed:
        metrics = _resolve_metrics(args, preset)
        aggregation = _resolve_aggregation(args, preset, metrics)
        known = all(metric.id in KNOWN_METRICS for metric in metrics)
        group_by = validate_speed_group_by(
            [dim for dim in (args.group_by or []) if dim] or list(preset.group_by),
            known_metric=known,
        )
        granularity = (
            normalize_granularity(args.granularity, SPEED_INSIGHTS)
            if args.granularity
            else preset.granularity
        )
        order_by, order_direction = _resolve_speed_ordering(args, preset, group_by)
        bucket_timezone = _resolve_bucket_timezone(args, granularity, warnings)
        limit = args.limit if args.limit is not None else preset.limit
        if limit is not None:
            limit = validate_speed_limit(limit)
        if not group_by:
            # The limit bounds grouped results per bucket, so an ungrouped
            # query has nothing to bound and the field is left out entirely.
            limit = None
    elif preset.is_logs:
        # This surface returns rows rather than groups, so there is nothing to
        # group by, the limit counts requests, and the filters are query
        # parameters rather than one OData expression.
        group_by = []
        limit = args.limit if args.limit is not None else preset.limit
        limit = validate_logs_limit(limit if limit is not None else LOGS_DEFAULT_LIMIT)
        log_filters = _resolve_log_filters(args, warnings)
    else:
        group_by = validate_group_by(_resolve_group_by(args, preset), dataset)
        limit = args.limit if args.limit is not None else preset.limit
        if limit is not None:
            limit = validate_limit(limit)
        if args.environment == "preview" and select_endpoint(group_by) == "count":
            # Web Analytics only, which is what this branch is. A logs preset is
            # ungrouped too, but it refuses --group-by outright, so the advice
            # below would send its reader to a flag that surface does not take.
            raise ConfigError(
                "--environment preview cannot be used with a count query: the "
                "count endpoints report production traffic only. Add --group-by "
                "day (or any other dimension) so the aggregate endpoint is used "
                "instead"
            )

    # This runs on every surface, because it is what refuses a shorthand the
    # active surface has no dimension for (--country on request logs, say).
    filter_expr = _resolve_filters(args, dataset, preset.surface)
    if preset.is_logs:
        # Request logs take no OData at all: their filters are already query
        # parameters in log_filters, and leaving this empty is what keeps the
        # header line from claiming a filter that was never sent.
        filter_expr = None

    now = datetime.now(timezone.utc)
    # A preset may own a window default, and an explicit --since still wins:
    # runtime logs are retained for an hour on Hobby and a day on Pro, so the
    # global 7 day default would report nothing there and read as a healthy site.
    # Tested against None rather than for truthiness, so --since "" still reaches
    # the time parser and is still refused: silently substituting a default for
    # an empty value would report a window nobody asked for as though they had.
    since = args.since
    if since is None:
        since = preset.default_since or DEFAULT_SINCE
    time_range = resolve_range(since, args.until, now)

    warning = reporting_window_warning(time_range[0], now)
    if warning:
        warnings.append(warning)

    if preset.surface == SPEED_INSIGHTS and not args.all_projects:
        # This surface scopes by projectIds, so a project name is likely to come
        # back empty rather than as an error, which is the worst kind of wrong.
        id_warning = warn_if_not_project_id(project or None)
        if id_warning:
            warnings.append(id_warning)

    return Settings(
        preset=preset,
        dataset=dataset,
        project=project or "",
        token=token,
        team=team,
        team_slug=team_slug,
        owner_id=owner_id,
        group_by=group_by,
        limit=limit,
        filter_expr=filter_expr,
        log_filters=log_filters,
        time_range=time_range,
        timeout=timeout,
        warnings=warnings,
        surface=preset.surface,
        metrics=metrics,
        aggregation=aggregation,
        all_projects=bool(args.all_projects),
        order_by=order_by,
        order_direction=order_direction,
        granularity=granularity,
        bucket_timezone=bucket_timezone,
    )


def _plan_speed_requests(settings: Settings) -> list[PreparedRequest]:
    """One Speed Insights request per metric: that API answers for one at a time."""
    common: dict[str, Any] = {
        "since": settings.time_range[0],
        "until": settings.time_range[1],
        "project": settings.project or None,
        "all_projects": settings.all_projects,
        "aggregation": settings.aggregation,
        "group_by": settings.group_by,
        "filter_expr": settings.filter_expr,
        "limit": settings.limit,
        "order_by": settings.order_by,
        "order_direction": settings.order_direction,
        "granularity": settings.granularity,
        "bucket_timezone": settings.bucket_timezone,
        "team": settings.team,
        "team_slug": settings.team_slug,
        "owner_id": settings.owner_id,
        "token": settings.token,
    }
    return [build_speed_request(metric=metric, **common) for metric in settings.metrics]


def _plan_log_requests(settings: Settings, page: int = 0) -> list[PreparedRequest]:
    """One request logs call per filter set, all for the same page.

    An errors preset needs two: ``level`` matches application log lines and
    ``statusCode`` matches responses, so a 5xx that printed nothing is invisible
    to the first and a 200 that logged a stack trace is invisible to the second.
    An explicit ``--level`` or ``--status-code`` collapses that to one call.

    It takes a page rather than looping over pages, because ``--dry-run`` prints
    exactly what one page would ask for.

    Args:
        settings: The resolved settings for this run.
        page: Zero based page index, the same for every filter set.

    Returns:
        One prepared request per filter set, in the order they are queried.
    """
    filter_sets = (
        error_filter_sets(settings.log_filters)
        if settings.preset.calls > 1
        else [dict(settings.log_filters)]
    )
    return [
        build_logs_request(
            project=settings.project,
            owner_id=settings.owner_id or "",
            since=settings.time_range[0],
            until=settings.time_range[1],
            page=page,
            filters=filters,
            token=settings.token,
        )
        for filters in filter_sets
    ]


#: Shown in a dry run when the owner is not known without asking the API. A dry
#: run must send nothing, including the one GET that would resolve this.
OWNER_PLACEHOLDER = "<read from the project at run time>"


#: Where a token is created in the dashboard, which is what both scope refusals
#: below tell the reader to go and do. Named here rather than in the package root
#: (where :data:`DOCS_TOKEN_URL`, the documentation anchor, lives) because this
#: module is the only one that needs it, and written once so a moved Vercel page
#: cannot leave one of the two hints stale.
DASHBOARD_TOKEN_URL = "https://vercel.com/account/tokens"


#: Appended to a 404 from the observability API. That surface scopes by account
#: (``scope.ownerId``), so a token bound to a single project has no account to
#: resolve and is refused. Web Analytics takes a ``projectId`` instead, which is
#: why a project scoped token can read traffic but not web vitals, and why the
#: bare API message is so misleading here.
OBSERVABILITY_SCOPE_HINT = (
    "This usually means the access token is scoped to a single project. "
    "Speed Insights is served by Vercel's observability API, which scopes by "
    "account rather than by project, so it needs a token with account (or "
    "team) scope. Web Analytics presets keep working with a project scoped "
    f"token. Create an account scoped token at {DASHBOARD_TOKEN_URL}, or "
    "confirm the scope of the current one with: npx vercel@latest metrics schema"
)


#: Appended to a Web Analytics 403 or 404 when no team was configured. Vercel's
#: own documentation is explicit: "For team projects, find the team's teamId or
#: slug and include one in each request. For projects owned by your personal
#: account, omit teamId and slug." So a team owned project queried without one
#: is refused, and the refusal does not say which of the two situations applies.
MISSING_TEAM_HINT = (
    "If this project belongs to a team rather than to your personal account, "
    "the request needs the team as well: pass --team with the team id (Team "
    "Settings, General) or set VERCEL_TEAM_ID. Vercel requires it on every "
    "request for a team owned project, and omitting it looks the same as not "
    "having access. Run --list-projects to see which projects this token can "
    "reach."
)


def _explain_missing_team(exc: ApiError, settings: Settings) -> ApiError:
    """Add the team hint to a Web Analytics refusal when no team was given.

    Only for 403 and 404, and only when nothing supplied a team. A refusal that
    might mean "wrong account" and might mean "no such project" is worth one
    sentence naming the commonest cause, but guessing at it when a team was
    already configured would send the reader the wrong way.
    """
    if exc.status not in (403, 404) or settings.team or settings.team_slug:
        return exc
    return ApiError(
        exc.status,
        exc.code,
        f"{exc.message}\n{MISSING_TEAM_HINT}",
        attempts=exc.attempts,
    )


def _explain_observability_404(exc: ApiError) -> ApiError:
    """Turn a bare observability 404 into something a user can act on.

    Vercel answers ``404 Observability Data not found.`` when a credential
    cannot reach that surface at all, which reads as "your project has no data"
    when it usually means "this token cannot ask". The distinction costs real
    debugging time, so it is spelled out rather than left to the API's wording.
    """
    if exc.status != 404:
        return exc
    return ApiError(
        exc.status,
        exc.code,
        f"{exc.message}\n{OBSERVABILITY_SCOPE_HINT}",
        attempts=exc.attempts,
    )


#: Appended to a 403 from the request logs endpoint. That endpoint is scoped by
#: the owning account, through an ``ownerId`` query parameter it requires and
#: cannot infer, so the commonest cause is a token that has no account to scope
#: to. It accepts no ``teamId`` at all, which is why the Web Analytics team hint
#: above would send the reader to a parameter this surface does not have.
REQUEST_LOGS_SCOPE_HINT = (
    "Request logs are scoped by the owning account (the ownerId parameter), so "
    "a token scoped to a single project cannot read them: it cannot act for the "
    "account that owns the project. Create an account or team scoped token at "
    f"{DASHBOARD_TOKEN_URL}, and set VERCEL_TEAM_ID for a team owned project, "
    "since a team is its own owner."
)


def _explain_request_logs_403(exc: ApiError) -> ApiError:
    """Turn a 403 from the logs endpoint into the answer, not just the status.

    ASSUMPTION: only a team scoped token was available to verify this against,
    so the project scoped case is reasoned from the ``ownerId`` requirement
    (omitting it is a 400, and a value the token cannot reach is a 403) rather
    than observed. See docs/api-notes.md.

    Args:
        exc: The failure as the API reported it.

    Returns:
        A new :class:`ApiError` carrying Vercel's own message and then the
        scope explanation, or ``exc`` unchanged for any other status.
    """
    if exc.status != 403:
        return exc
    return ApiError(
        exc.status,
        exc.code,
        f"{exc.message}\n{REQUEST_LOGS_SCOPE_HINT}",
        attempts=exc.attempts,
    )


def _explain_failure(exc: ApiError, operation: str, settings: Settings) -> ApiError:
    """Add whatever explanation the failing operation's own scoping rules call for.

    One dispatch point for all three surfaces, so a refusal can only ever
    collect advice that fits the endpoint that refused: the Web Analytics team
    hint on a request logs 403 would point at ``--team``, which that endpoint
    does not accept, and would say nothing about the ``ownerId`` it does need.

    Args:
        exc: The failure as the API reported it.
        operation: The operation key of the request that failed.
        settings: The resolved settings, which decide whether the Web Analytics
            team hint applies at all.

    Returns:
        Either a new :class:`ApiError` carrying the explanation, or ``exc``
        unchanged when this status on this operation explains itself.
    """
    if operation == OBSERVABILITY_QUERY:
        return _explain_observability_404(exc)
    if operation == REQUEST_LOGS_QUERY:
        return _explain_request_logs_403(exc)
    return _explain_missing_team(exc, settings)


class MissingProject(ConfigError):
    """No project was named, and one account may hold many.

    Its own type only so the entry point can turn it into something useful: a
    list of the projects available, which is the answer to the question behind
    the error rather than a restatement of the error.
    """


def _with_project_list(
    exc: MissingProject, args: argparse.Namespace, env: Mapping[str, str]
) -> str:
    """The missing-project message, with the account's projects appended.

    Best effort by design: if the projects cannot be listed, for any reason,
    the original message stands. An error path is the worst place to raise a
    second error, and the first message is already correct on its own.
    """
    if args.dry_run:
        return str(exc)
    try:
        token, team, team_slug = _credentials(args, env)
        session = requests.Session()
        try:
            projects = _fetch_projects(
                session,
                token,
                team,
                team_slug,
                args.max_retries,
                validate_timeout(args.timeout),
            )
        finally:
            session.close()
    except Exception:
        return str(exc)
    if not projects:
        return str(exc)
    return f"{exc}\n\nThis account has:\n\n{format_projects(projects)}"


def _credentials(
    args: argparse.Namespace, env: Mapping[str, str]
) -> tuple[str | None, str | None, str | None]:
    """Token, team and team slug, from flags then environment."""
    token = args.token or _env_value(env, "VERCEL_TOKEN")
    if not token and not args.dry_run:
        raise ConfigError(
            "no access token configured; pass --token or set VERCEL_TOKEN "
            f"(create one at {DOCS_TOKEN_URL}). Use --dry-run to build the "
            "request without a token"
        )
    if token:
        token = validate_token(token)
    return (
        token,
        args.team or _env_value(env, "VERCEL_TEAM_ID"),
        args.team_slug or _env_value(env, "VERCEL_TEAM_SLUG"),
    )


def _fetch_projects(
    session: Any,
    token: str | None,
    team: str | None,
    team_slug: str | None,
    max_retries: int,
    timeout: float,
) -> list[dict[str, str]]:
    """Every project the account holds, or an empty list if it cannot be read."""
    prepared = build_projects_request(team=team, team_slug=team_slug, token=token)
    payload = execute(
        prepared, session, max_retries=max_retries, timeout=timeout
    )
    return extract_projects(payload)


def _run_list_projects(
    args: argparse.Namespace,
    env: Mapping[str, str],
    style: Style,
    out: TextIO,
    err: TextIO,
) -> int:
    """List the account's projects, so picking one does not need the dashboard.

    One account holds many projects and a query has to name exactly one, so
    this is the discovery step that everything else depends on. Every project
    is shown, including those collecting nothing: "enabled but empty" and "not
    enabled" both produce an empty query, and they need different fixes, so the
    difference is worth seeing.
    """
    token, team, team_slug = _credentials(args, env)
    prepared = build_projects_request(team=team, team_slug=team_slug, token=token)

    if args.dry_run:
        print(format_dry_run(prepared), file=out)
        return 0

    def on_retry(reason: str) -> None:
        if args.verbose:
            print(f"verbose: {reason}", file=err)

    session = requests.Session()
    try:
        payload = execute(
            prepared,
            session,
            max_retries=args.max_retries,
            timeout=validate_timeout(args.timeout),
            on_retry=on_retry,
        )
    finally:
        session.close()

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True), file=out)
        return 0
    print(style.bold("Projects"), file=out)
    print(file=out)
    print(format_projects(extract_projects(payload)), file=out)
    return 0


def _run_list_metrics(
    args: argparse.Namespace,
    env: Mapping[str, str],
    style: Style,
    out: TextIO,
    err: TextIO,
) -> int:
    """Ask the API which metrics this account can actually query.

    Vercel documents the schema as the source of truth for the metrics,
    dimensions and aggregations available to an account, which makes it the
    right thing to consult when a query is refused: it answers "does this metric
    exist for me" outright instead of by inference. It needs no project and no
    owner, only a token, so it works even when a query cannot be built at all.
    """
    token = args.token or _env_value(env, "VERCEL_TOKEN")
    team = args.team or _env_value(env, "VERCEL_TEAM_ID")
    team_slug = args.team_slug or _env_value(env, "VERCEL_TEAM_SLUG")
    if not token and not args.dry_run:
        raise ConfigError(
            "no access token configured; pass --token or set VERCEL_TOKEN "
            f"(create one at {DOCS_TOKEN_URL}). Use --dry-run to build the "
            "request without a token"
        )
    if token:
        token = validate_token(token)
    prepared = build_schema_request(team=team, team_slug=team_slug, token=token)

    if args.dry_run:
        print(format_dry_run(prepared), file=out)
        return 0

    def on_retry(reason: str) -> None:
        if args.verbose:
            print(f"verbose: {reason}", file=err)

    session = requests.Session()
    try:
        payload = execute(
            prepared,
            session,
            max_retries=args.max_retries,
            timeout=validate_timeout(args.timeout),
            on_retry=on_retry,
        )
    except ApiError as exc:
        raise _explain_observability_404(exc) from None
    finally:
        session.close()

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True), file=out)
        return 0
    prefix = args.list_metrics or None
    print(style.bold("Queryable metrics"), file=out)
    print(file=out)
    print(format_schema(payload, prefix), file=out)
    return 0


def _resolve_project_record(
    session: Any,
    settings: Settings,
    max_retries: int,
    on_retry: Callable[[str], None],
) -> tuple[str | None, str | None]:
    """Read one project record, returning its canonical id and owning account.

    Called for the two surfaces that scope by an owning account, whenever
    something they need is missing. Two things come from the one request, which
    is why they resolve together:

    * The **owner**, because both surfaces require one (Speed Insights as
      ``scope.ownerId``, request logs as the ``ownerId`` parameter) and only the
      API knows it for a personal account. The account endpoint is not
      equivalent: a team scoped token has no personal user and it answers 404
      "User not found."
    * The **canonical project id**, because Speed Insights scopes by
      ``projectIds`` and wants identifiers, while Web Analytics happily accepts
      a project name. Resolving the name here is what stops ``--project
      my-site`` working for traffic and silently returning nothing for speed.
      Request logs take a name or an id, so that surface never needs this on
      its own.

    Returns:
        ``(project_id, owner_id)``, either of which may be ``None`` when the
        record did not carry it.

    Raises:
        ConfigError: When there is no project to ask about.
    """
    if not settings.project:
        raise ConfigError(
            "--all needs an owner named explicitly, because there is no single "
            "project to read one from; pass --owner-id, or --team (a team is "
            "its own owner), or set VERCEL_OWNER_ID"
        )
    prepared = build_project_request(
        settings.project,
        team=settings.team,
        team_slug=settings.team_slug,
        token=settings.token,
    )
    payload = execute(
        prepared,
        session,
        max_retries=max_retries,
        timeout=settings.timeout,
        on_retry=on_retry,
    )
    if not isinstance(payload, Mapping):
        raise ConfigError(
            f"the record for project {settings.project!r} was not a JSON "
            "object, so neither its id nor its owning account could be read; "
            "pass --owner-id and a prj_ identifier explicitly"
        )
    return resolve_project_id(payload, settings.project), owner_from_project(payload)


def _needs_owner_lookup(settings: Settings) -> bool:
    """Whether this run must read the project record before it can query.

    Both scoped surfaces need the owning account, and for a personal account
    only the project's own record knows it. What each surface needs beyond that
    differs:

    * **Speed Insights** scopes by ``scope.ownerId`` and ``scope.projectIds``,
      so it needs the owner and a real project id. A project name is legal input
      and works as-is on Web Analytics, so it is resolved here rather than handed
      to a field that cannot match it.
    * **Request logs** require ``ownerId`` too: omitting it is a 400 and a value
      the token cannot reach is a 403. That endpoint takes a project name as
      happily as an id, so only a missing owner is worth the extra request.

    Args:
        settings: The resolved settings for this run.

    Returns:
        True when one extra GET is needed before the query can be built.
    """
    if settings.is_logs:
        return not settings.owner_id
    return settings.is_speed and (
        not settings.owner_id
        or not (settings.all_projects or looks_like_project_id(settings.project))
    )


def _overview_granularity(settings: Settings) -> str:
    """The time bucket the overview's trend query groups by.

    Read off the resolved settings rather than off the raw flag, because the
    two vocabularies do not agree with the wire: ``--granularity 1d`` is a
    legal input that Web Analytics would reject verbatim, and by the time it
    reaches the settings it has already been translated to ``day`` and
    validated. The overview rejects ``--group-by``, so its grouping is exactly
    one time dimension and there is nothing else here to find.
    """
    for dimension in settings.group_by:
        if dimension in TIME_GRANULARITIES:
            return dimension
    return "day"


def _plan_requests(settings: Settings) -> list[PreparedRequest]:
    """Build every request a run needs.

    One for most presets, two for an errors preset (one per filter set), three
    for the overview and five for vitals. On the request logs surface these are
    the first page only, which is what a dry run shows.
    """
    if settings.is_speed:
        return _plan_speed_requests(settings)
    if settings.is_logs:
        return _plan_log_requests(settings)

    common: dict[str, Any] = {
        "dataset": settings.dataset,
        "project": settings.project,
        "since": settings.time_range[0],
        "until": settings.time_range[1],
        "filter_expr": settings.filter_expr,
        "team": settings.team,
        "team_slug": settings.team_slug,
        "token": settings.token,
    }

    if settings.preset.name != "overview":
        return [
            build_request(group_by=settings.group_by, limit=settings.limit, **common)
        ]

    table_limit = settings.limit if settings.limit is not None else OVERVIEW_TABLE_LIMIT
    granularity = _overview_granularity(settings)
    return [
        build_request(group_by=[granularity], limit=MAX_LIMIT, **common),
        build_request(group_by=["requestPath"], limit=table_limit, **common),
        build_request(group_by=["referrerHostname"], limit=table_limit, **common),
    ]


def _is_empty(result: Result) -> bool:
    """True when there is nothing worth tabulating.

    No rows is empty on either surface. An ungrouped row needs the two surfaces
    told apart, because zero means opposite things on them:

    * Web Analytics counts. Zero page views by zero visitors is genuinely no
      data, and printing a table of zeroes says less than one line of prose.
    * Speed Insights values. A Cumulative Layout Shift of exactly ``0.0`` is a
      perfect score and a real measurement, and calling it "no data" would hide
      the best result the metric can have. So presence decides here, never
      truthiness: the value key is either in the row or it is not, and a data
      point count settles it when the value arrived under a name the parser
      recognised but the caller did not ask for.
    """
    if not result.rows:
        return True
    if not result.is_count:
        return False
    row = result.rows[0]
    if result.dataset == SPEED_INSIGHTS_DATASET:
        return not (
            result.primary_metric in row.metrics or DATA_POINTS_METRIC in row.metrics
        )
    return not any(value for value in row.metrics.values())


def _empty_message(settings: Settings, group_by: Sequence[str]) -> str:
    """The single line printed instead of an empty table."""
    since, until = settings.time_range
    grouping = f"grouped by {', '.join(group_by)}" if group_by else "ungrouped"
    filter_text = settings.filter_expr or "no filter"
    subject = settings.dataset
    if settings.is_speed and settings.metrics:
        subject = settings.metrics[0].id
    return (
        f"No {subject} data for project {settings.project_label} "
        f"({grouping}) between {to_api_timestamp(since)} and "
        f"{to_api_timestamp(until)} with {filter_text}. "
        "Try a wider --since, or relax the filter."
    )


def _collect_logs(
    settings: Settings,
    args: argparse.Namespace,
    session: Any,
    on_retry: Callable[[str], None],
    err: TextIO,
) -> LogReport:
    """Fetch every filter set, page by page, and build one report from them.

    Each filter set gets its own paging budget, and the sets are then merged and
    deduplicated by request id: one request can arrive from both of an errors
    run's filter sets, because ``level`` matches what a request logged while
    ``statusCode`` matches what it answered.

    Args:
        settings: The resolved settings for this run.
        args: The parsed command line, for ``--verbose`` and ``--max-retries``.
        session: The session every request is issued on.
        on_retry: Called with one line of reason each time a request is retried.
        err: Where the verbose lines go. Passed in rather than taken from
            ``sys.stderr`` so they reach the same stream as the rest of the CLI's
            diagnostics, which is also the stream the tests capture.

    Returns:
        One report covering every filter set, newest first.

    Raises:
        ApiError: On a failure the API reported, carrying the token scope
            explanation when it was a 403; or with code ``invalid_response``
            when a page was not an object carrying ``rows``.
        RateLimitError: When retrying did not clear a rate limit.

    Note:
        This is where the credential scrub is supplied, because this is the
        caller that holds the prepared request and therefore its headers. Rows
        on this surface are free text an application wrote, so a response can
        echo the very token that fetched it; this tool knows exactly one secret
        and must never be the thing that discloses it. The scrub is handed to
        the normalization step, which is the single boundary where a payload
        becomes typed rows, so no renderer and no output format has to remember
        it. It rewrites this client's own credential only: nothing can tell a
        user's own API key from ordinary log text, and pretending otherwise
        would be a promise this tool cannot keep.
    """
    limit = settings.limit or LOGS_DEFAULT_LIMIT
    # Built once, for the filter set count and for the header line below. The
    # rebuild inside the loop is only because a page index has to reach the
    # request, and every page of a set carries the same headers.
    planned = _plan_log_requests(settings)
    groups: list[list[LogEntry]] = []
    truncated = False
    pages = 0

    for index, first_page in enumerate(planned):
        # Bound per filter set from the request that will carry it, rather than
        # rebuilt from the token here: the headers are the authority on what the
        # credential actually is, and every page of a set carries the same ones.
        def scrub(text: str, headers: Mapping[str, str] = first_page.headers) -> str:
            """Rewrite this client's own credential out of a response string."""
            return scrub_credentials(text, headers)

        if args.verbose:
            # Once per filter set rather than once per page, so the output stays
            # proportional to the paging. This is also the line that shows a
            # reader the token is redacted wherever the tool prints a request.
            print(
                f"verbose: headers {redact_headers(first_page.headers)}",
                file=err,
            )

        def call(page: int, index: int = index) -> Mapping[str, Any]:
            """Fetch one page of one filter set. Injected into logs.collect."""
            prepared = _plan_log_requests(settings, page)[index]
            if args.verbose:
                # The params name the page and the filter set's own statusCode or
                # level, which is what tells two interleaved sets apart: without
                # them an errors run reads "page 0, page 1, page 0".
                print(f"verbose: {prepared.method} {prepared.url}", file=err)
                print(f"verbose: params {prepared.params}", file=err)
            try:
                answer = execute(
                    prepared,
                    session,
                    max_retries=args.max_retries,
                    timeout=settings.timeout,
                    on_retry=on_retry,
                )
            except ApiError as exc:
                raise _explain_failure(exc, prepared.operation, settings) from None
            if not isinstance(answer, Mapping):
                raise ApiError(
                    200,
                    "invalid_response",
                    "the request logs response was a JSON array, but this "
                    "endpoint answers with an object carrying 'rows'",
                )
            return answer

        entries, call_truncated, call_pages = collect_logs(
            call, limit=limit, scrub=scrub
        )
        groups.append(entries)
        truncated = truncated or call_truncated
        pages += call_pages

    merged, merge_truncated = merge_logs(groups, limit=limit)
    return build_log_report(
        merged,
        time_range=settings.time_range,
        project_label=settings.project_label,
        preset=settings.preset.name,
        filters=settings.log_filters,
        truncated=truncated or merge_truncated,
        pages_fetched=pages,
        requested_limit=limit,
        counts_errors=settings.preset.name in ("errors", "error-summary"),
    )


def _run(
    args: argparse.Namespace,
    env: Mapping[str, str],
    out: TextIO,
    err: TextIO,
) -> int:
    """Resolve settings, issue the request or requests, and print the report."""
    style = _resolve_style(args, env, out)

    if args.version:
        print(f"{PROG} {VERSION}", file=out)
        return 0
    if args.list_presets:
        print(format_presets(style), file=out)
        return 0

    if args.list_projects:
        return _run_list_projects(args, env, style, out, err)

    if args.list_metrics is not None:
        return _run_list_metrics(args, env, style, out, err)

    settings = _resolve_settings(args, env)
    for warning in settings.warnings:
        print(f"warning: {warning}", file=err)

    needs_lookup = _needs_owner_lookup(settings)

    if args.dry_run:
        # A dry run sends nothing, including the GET that would resolve the
        # owner, so the body shows a placeholder and says where it comes from.
        if needs_lookup and not settings.owner_id:
            settings.owner_id = OWNER_PLACEHOLDER
        for index, prepared in enumerate(_plan_requests(settings)):
            if index:
                print(file=out)
            print(format_dry_run(prepared), file=out)
        if needs_lookup and settings.owner_id == OWNER_PLACEHOLDER:
            # The two surfaces carry the owner differently: Speed Insights posts
            # it inside a scope object, request logs send it as a plain query
            # parameter. Naming a scope object the logs API does not have would
            # send its reader hunting for a field that is not there.
            owner_field = "the ownerId parameter" if settings.is_logs else "scope.ownerId"
            print(
                f"\n{owner_field} shows {OWNER_PLACEHOLDER} because no --team "
                "and no --owner-id were given. A real run reads it once from "
                "the project's own record (its accountId); pass --owner-id to "
                "skip that call.",
                file=out,
            )
        return 0

    def on_retry(reason: str) -> None:
        if args.verbose:
            print(f"verbose: {reason}", file=err)

    payloads: list[dict[str, Any]] = []
    # Declared here, before the session, so this one name has a single type all
    # the way through: the emitter below branches on it having been collected
    # rather than on the surface, which needs neither an assert nor a cast.
    report: LogReport | None = None
    session = requests.Session()
    try:
        if needs_lookup:
            project_id, owner_id = _resolve_project_record(
                session, settings, args.max_retries, on_retry
            )
            if not settings.owner_id and owner_id:
                settings.owner_id = owner_id
            if project_id:
                settings.project = project_id
            if args.verbose:
                print(
                    "verbose: resolved the project record "
                    f"(id={settings.project}, owner={settings.owner_id})",
                    file=err,
                )
            if not settings.owner_id:
                raise ConfigError(
                    f"project {settings.project!r} carried no owning account, "
                    f"so a {SURFACE_LABELS[settings.surface]} query could not "
                    "be scoped; pass --owner-id explicitly, or set "
                    "VERCEL_OWNER_ID"
                )

        if settings.is_logs:
            # This surface pages, so its requests are issued as they are needed
            # rather than all planned up front, and it answers with rows rather
            # than with the grouped payload the loop below collects.
            report = _collect_logs(settings, args, session, on_retry, err)
        else:
            requests_to_send = _plan_requests(settings)

            if args.verbose:
                for prepared in requests_to_send:
                    print(f"verbose: {prepared.method} {prepared.url}", file=err)
                    print(f"verbose: params {prepared.params}", file=err)
                    print(
                        f"verbose: headers {redact_headers(prepared.headers)}",
                        file=err,
                    )

            for prepared in requests_to_send:
                try:
                    answer = execute(
                        prepared,
                        session,
                        max_retries=args.max_retries,
                        timeout=settings.timeout,
                        on_retry=on_retry,
                    )
                except ApiError as exc:
                    raise _explain_failure(exc, prepared.operation, settings) from None
                if not isinstance(answer, Mapping):
                    # Only the schema endpoint answers with a top level array; a
                    # query that does is a response this client cannot interpret.
                    raise ApiError(
                        200,
                        "invalid_response",
                        "the query returned a JSON array, but a query response "
                        "is an object carrying 'data'; run with --json to see it",
                    )
                payloads.append(dict(answer))
    finally:
        session.close()

    if report is not None:
        return _emit_logs(settings, args, report, style, out, err)
    if settings.is_speed:
        return _emit_speed(settings, args, payloads, style, out, err)
    if settings.preset.name == "overview":
        return _emit_overview(settings, args, payloads, style, out)
    return _emit_single(settings, args, payloads[0], style, out)


def _measured(
    results: Sequence[Result], metrics: Sequence[Metric], aggregation: str
) -> dict[str, float | None]:
    """The single value measured for each metric, keyed by its short name."""
    measured: dict[str, float | None] = {}
    for result, metric in zip(results, metrics):
        column = metric.column(aggregation)
        value: float | None = None
        for row in result.rows:
            if column in row.metrics:
                value = row.metrics[column]
                break
        measured[metric.short] = value
    return measured


def _emit_budgets(
    settings: Settings,
    args: argparse.Namespace,
    results: Sequence[Result],
    style: Style,
    out: TextIO,
    err: TextIO,
) -> int:
    """Report each budget and return the exit code the run should use.

    The report goes to stderr whenever the real output is machine readable, so
    a ``--json`` run stays parseable while a human still sees why the build
    failed.
    """
    if not args.budget:
        return 0
    if settings.group_by:
        raise ConfigError(
            "--budget compares one number against a limit, but this query is "
            "grouped, so there is a number per group. Drop --group-by, or use "
            "the vitals preset"
        )
    budgets = parse_budgets(args.budget, VITAL_ORDER)
    outcomes = evaluate(budgets, _measured(results, settings.metrics, settings.aggregation_label))

    stream = err if (args.json or args.csv) else out
    print(file=stream)
    print(style.bold("Budgets"), file=stream)
    for budget, value, verdict in outcomes:
        metric = metric_for(budget.metric)
        shown = format_value(value, metric.unit) if value is not None else "no data"
        limit = format_value(budget.limit, metric.unit)
        print(
            f"  {verdict:<7} {metric.label:<26} {shown:>8} against {limit}",
            file=stream,
        )
    if any_failed(outcomes):
        print(
            "at least one budget was exceeded, so this run exits "
            f"{BUDGET_EXCEEDED}",
            file=stream,
        )
        return BUDGET_EXCEEDED
    return 0


def _emit_speed(
    settings: Settings,
    args: argparse.Namespace,
    payloads: Sequence[dict[str, Any]],
    style: Style,
    out: TextIO,
    err: TextIO,
) -> int:
    """Render one Speed Insights result, or compose five into the vitals table."""
    results = [
        normalize_speed(
            payload,
            metric=metric,
            aggregation=settings.aggregation_label,
            group_by=settings.group_by,
            granularity=settings.granularity,
        )
        for payload, metric in zip(payloads, settings.metrics)
    ]

    if len(results) > 1:
        if args.json:
            document = {
                "range": {
                    "since": to_api_timestamp(settings.time_range[0]),
                    "until": to_api_timestamp(settings.time_range[1]),
                },
                "aggregation": settings.aggregation,
                "metrics": {
                    result.metric or metric.id: _result_document(
                        result, payload, settings.time_range
                    )
                    for result, payload, metric in zip(
                        results, payloads, settings.metrics
                    )
                },
            }
            print(json.dumps(document, indent=2), file=out)
            return _emit_budgets(settings, args, results, style, out, err)
        if all(_is_empty(result) for result in results):
            print(_empty_message(settings, settings.group_by), file=out)
            return _emit_budgets(settings, args, results, style, out, err)
        print(
            render_vitals(
                results,
                project=settings.project_label,
                time_range=settings.time_range,
                aggregation=settings.aggregation_label,
                filter_expr=settings.filter_expr,
                style=style,
            ),
            file=out,
        )
        return _emit_budgets(settings, args, results, style, out, err)

    result = results[0]
    if args.json:
        print(
            format_json(result, payloads[0], time_range=settings.time_range), file=out
        )
        return _emit_budgets(settings, args, results, style, out, err)
    if args.csv:
        print(format_csv(result), end="", file=out)
        return _emit_budgets(settings, args, results, style, out, err)
    if _is_empty(result):
        print(_empty_message(settings, settings.group_by), file=out)
        return _emit_budgets(settings, args, results, style, out, err)

    title = (
        f"Vercel Speed Insights: {settings.project_label} "
        f"({settings.preset.name}, {settings.aggregation})"
    )
    print(
        format_table(
            result,
            time_range=settings.time_range,
            filter_expr=settings.filter_expr,
            limit=settings.limit,
            style=style,
            title=title,
        ),
        file=out,
    )
    return _emit_budgets(settings, args, results, style, out, err)


def _emit_single(
    settings: Settings,
    args: argparse.Namespace,
    payload: dict[str, Any],
    style: Style,
    out: TextIO,
) -> int:
    """Render one result in the requested format."""
    result = normalize(payload, settings.dataset, settings.group_by)

    if args.json:
        print(format_json(result, payload, time_range=settings.time_range), file=out)
        return 0
    if args.csv:
        print(format_csv(result), end="", file=out)
        return 0

    if _is_empty(result):
        print(_empty_message(settings, settings.group_by), file=out)
        return 0

    title = f"Vercel Web Analytics: {settings.project} ({settings.preset.name})"
    print(
        format_table(
            result,
            time_range=settings.time_range,
            filter_expr=settings.filter_expr,
            limit=settings.limit,
            style=style,
            title=title,
        ),
        file=out,
    )
    return 0


def _emit_overview(
    settings: Settings,
    args: argparse.Namespace,
    payloads: Sequence[dict[str, Any]],
    style: Style,
    out: TextIO,
) -> int:
    """Render the three overview results as one report, or as JSON."""
    granularity = _overview_granularity(settings)
    groupings = [[granularity], ["requestPath"], ["referrerHostname"]]
    results = [
        normalize(payload, settings.dataset, grouping)
        for payload, grouping in zip(payloads, groupings)
    ]

    if args.json:
        document = {
            "range": {
                "since": to_api_timestamp(settings.time_range[0]),
                "until": to_api_timestamp(settings.time_range[1]),
            },
            "sections": {
                name: _result_document(result, payload, settings.time_range)
                for name, result, payload in zip(
                    ("byGranularity", "topPages", "topReferrers"), results, payloads
                )
            },
        }
        print(json.dumps(document, indent=2), file=out)
        return 0

    if all(_is_empty(result) for result in results):
        print(_empty_message(settings, [granularity]), file=out)
        return 0

    print(
        render_overview(
            results,
            project=settings.project,
            time_range=settings.time_range,
            filter_expr=settings.filter_expr,
            limit=(
                settings.limit if settings.limit is not None else OVERVIEW_TABLE_LIMIT
            ),
            style=style,
        ),
        file=out,
    )
    return 0


def _emit_logs(
    settings: Settings,
    args: argparse.Namespace,
    report: LogReport,
    style: Style,
    out: TextIO,
    err: TextIO,
) -> int:
    """Print a logs report in whichever format was asked for.

    Args:
        settings: The resolved settings, for the preset that decides the layout.
        args: The parsed command line, for the output format and ``--expand``.
        report: The collected report.
        style: Colour and glyph settings.
        out: Stream for the report.
        err: Stream for the report's notes when the report itself is machine
            readable, the same way ``_emit_budgets`` moves its verdict aside for
            ``--json`` and ``--csv``.

    Returns:
        0, always. An empty window is a complete answer to "what broke", and
        exiting non-zero for it would fail a caller's pipeline over good news.
    """
    if args.json:
        # The notes are a field of the document here, so they need no second
        # copy: a consumer reads them out of it.
        print(format_logs_json(report), file=out)
        return 0
    if args.csv:
        print(format_logs_csv(report), end="", file=out)
        # CSV has nowhere to carry a caveat, so the caveats go to the other
        # stream rather than nowhere: without this, a table cut at its limit is
        # indistinguishable from a complete one, and an empty window from a
        # healthy site, to exactly the caller who cannot tell otherwise.
        for note in report.notes:
            print(f"note: {note}", file=err)
        return 0
    if settings.preset.name == "error-summary":
        # Tallied from the merged entries, and by this one caller, so the tables
        # can only ever count the rows the report itself carries.
        print(
            render_error_summary(report, summarize(report.entries), style=style),
            file=out,
        )
        return 0
    print(render_logs(report, style=style, expand=args.expand), file=out)
    return 0


def _resolve_style(
    args: argparse.Namespace, env: Mapping[str, str], out: TextIO
) -> Style:
    """Colour only on a TTY, with NO_COLOR unset and --no-color not passed."""
    color = True
    if args.no_color or env.get("NO_COLOR"):
        color = False
    else:
        isatty = getattr(out, "isatty", None)
        color = bool(isatty()) if callable(isatty) else False
    encoding = (getattr(out, "encoding", None) or "utf-8").lower()
    unicode_safe = "utf" in encoding
    return Style(color=color, unicode=unicode_safe)


def main(
    argv: Sequence[str] | None = None,
    env: Mapping[str, str] | None = None,
    *,
    out: TextIO | None = None,
    err: TextIO | None = None,
) -> int:
    """Entry point. Returns the process exit code and never raises for the user.

    Args:
        argv: Command line arguments without the program name.
        env: Environment mapping; defaults to :data:`os.environ`.
        out: Stream for report output; defaults to stdout.
        err: Stream for warnings and errors; defaults to stderr.

    Returns:
        0 on success (including an empty result set), 1 for an API or network
        failure, 2 for a configuration or usage error, 130 when interrupted.
    """
    stdout = out if out is not None else sys.stdout
    stderr = err if err is not None else sys.stderr
    environment = env if env is not None else os.environ

    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        return _run(args, environment, stdout, stderr)
    except MissingProject as exc:
        # Answer the question behind the error. Listing costs one request and
        # only happens on this path, so a normal run pays nothing for it.
        print(f"error: {_with_project_list(exc, args, environment)}", file=stderr)
        return 2
    except ConfigError as exc:
        print(f"error: {exc}", file=stderr)
        return 2
    except RateLimitError as exc:
        print(f"error: {exc}", file=stderr)
        print(
            "hint: rate limits are per endpoint; wait for the reset above or "
            "raise --max-retries so the client waits for you",
            file=stderr,
        )
        return 1
    except ApiError as exc:
        print(f"error: {exc}", file=stderr)
        return 1
    except KeyboardInterrupt:
        print("interrupted", file=stderr)
        return 130
