"""Listing the projects an account holds, and naming them.

One Vercel account holds many projects, so the first question anyone has is
"which one, and does it even have data". That question is not specific to either
query surface, which is why it lives in its own module.

It also carries the fix for a real inconsistency. The Web Analytics endpoints
accept "the project identifier or the project name", but Speed Insights scopes
by ``projectIds`` and wants identifiers, so a project name worked on one surface
and silently returned nothing on the other. Resolving a name to its id here
makes both behave the same.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from . import ApiError, ConfigError, sanitize_label
from .http import PreparedRequest, default_headers, operation_url

#: Operation keys into ``http.OPERATIONS``. Never a method, never a host.
LIST_OPERATION = "projects"
ONE_OPERATION = "project"

#: Vercel project identifiers start with this. A value that does not is a name,
#: which is legal input and simply needs resolving before the Speed Insights
#: surface can use it.
PROJECT_ID_PREFIX = "prj_"

#: How many projects to ask for. Generous enough that almost no account pages,
#: and bounded so a very large team cannot produce an unreadable wall.
LIST_LIMIT = 100


def looks_like_project_id(value: str | None) -> bool:
    """True when ``value`` is already an identifier rather than a name."""
    return bool(value) and str(value).startswith(PROJECT_ID_PREFIX)


def build_list_request(
    *,
    team: str | None = None,
    team_slug: str | None = None,
    token: str | None = None,
    limit: int = LIST_LIMIT,
) -> PreparedRequest:
    """Build the request that lists the account's projects."""
    params: list[tuple[str, str]] = [("limit", str(limit))]
    if team:
        params.append(("teamId", team))
    elif team_slug:
        params.append(("slug", team_slug))
    return PreparedRequest(
        operation=LIST_OPERATION,
        url=operation_url(LIST_OPERATION),
        params=params,
        headers=default_headers(token),
    )


def build_one_request(
    project: str,
    *,
    team: str | None = None,
    team_slug: str | None = None,
    token: str | None = None,
) -> PreparedRequest:
    """Build the request that reads one project by identifier or by name."""
    params: list[tuple[str, str]] = []
    if team:
        params.append(("teamId", team))
    elif team_slug:
        params.append(("slug", team_slug))
    return PreparedRequest(
        operation=ONE_OPERATION,
        url=operation_url(ONE_OPERATION, project=project),
        params=params,
        headers=default_headers(token),
    )


def _feature_state(entry: Mapping[str, Any], key: str) -> str:
    """Whether one analytics feature is off, on, or actually holding data.

    A project record carries ``webAnalytics`` and ``speedInsights`` objects with
    ``enabledAt`` and ``hasData``. The distinction is worth showing: "enabled
    but empty" and "not enabled" look identical when a query comes back with
    nothing, and they need different fixes.
    """
    feature = entry.get(key)
    if not isinstance(feature, Mapping):
        return "off"
    if feature.get("disabledAt"):
        return "off"
    if not feature.get("enabledAt"):
        return "off"
    return "data" if feature.get("hasData") else "empty"


def extract_projects(payload: Any) -> list[dict[str, str]]:
    """Pull the project list out of a response, defensively.

    The list endpoint's response shape is not published in usable detail, so
    this accepts a bare list or the documented ``projects`` wrapper, and reads
    only the fields it needs from each entry.
    """
    entries: Any = payload
    if isinstance(payload, Mapping):
        for key in ("projects", "data", "result"):
            candidate = payload.get(key)
            if isinstance(candidate, list):
                entries = candidate
                break
    if not isinstance(entries, list):
        return []
    projects: list[dict[str, str]] = []
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        name = entry.get("name")
        identifier = entry.get("id")
        if not isinstance(identifier, str) or not identifier:
            continue
        projects.append(
            {
                "name": sanitize_label(str(name)) if name else "(unnamed)",
                "id": sanitize_label(identifier),
                "analytics": _feature_state(entry, "webAnalytics"),
                "speed": _feature_state(entry, "speedInsights"),
            }
        )
    return projects


def format_projects(projects: Sequence[Mapping[str, str]]) -> str:
    """Render the project list as an aligned table.

    Every project is shown, including those with nothing collected. A project
    missing from this list would read as "does not exist" when it may only have
    analytics switched off, and that is exactly the confusion worth avoiding.
    """
    if not projects:
        return (
            "no projects found for this account. If the token is scoped to a "
            "single project, it cannot list the others; an account or team "
            "scoped token can"
        )
    headers = ("name", "project id", "traffic", "speed")
    rows = [
        (p.get("name", ""), p.get("id", ""), p.get("analytics", ""), p.get("speed", ""))
        for p in projects
    ]
    widths = [
        max(len(headers[i]), max(len(row[i]) for row in rows)) for i in range(len(headers))
    ]
    lines = [
        "  ".join(headers[i].ljust(widths[i]) for i in range(len(headers))).rstrip(),
        "  ".join("-" * widths[i] for i in range(len(headers))),
    ]
    for row in rows:
        lines.append(
            "  ".join(row[i].ljust(widths[i]) for i in range(len(headers))).rstrip()
        )
    lines.append("")
    lines.append(
        "traffic and speed are Web Analytics and Speed Insights: 'data' means "
        "collected, 'empty' means enabled but nothing yet, 'off' means not enabled."
    )
    lines.append("Query one with --project, using either the name or the project id.")
    return "\n".join(lines)


def resolve_project_id(payload: Any, requested: str) -> str:
    """The canonical project id from a project record.

    Args:
        payload: The decoded ``GET /v9/projects/{idOrName}`` response.
        requested: What the user asked for, for the error message.

    Raises:
        ConfigError: When the record carries no usable id.
    """
    if isinstance(payload, Mapping):
        identifier = payload.get("id")
        if isinstance(identifier, str) and identifier:
            return identifier
    raise ConfigError(
        f"the record for project {requested!r} carried no id, so it could not "
        "be resolved; pass the prj_ identifier directly, which --list-projects "
        "will show"
    )


def owner_from_project(payload: Any) -> str | None:
    """The owning account id from a project record, when it carries one."""
    if isinstance(payload, Mapping):
        account = payload.get("accountId")
        if isinstance(account, str) and account:
            return account
    return None


def missing_project_error(projects: Sequence[Mapping[str, str]] | None) -> ConfigError:
    """The "which project" error, listing the choices when they are known."""
    base = (
        "no project configured; pass --project with a project id or name, or "
        "set VERCEL_PROJECT_ID in the environment"
    )
    if not projects:
        return ConfigError(f"{base}. Run --list-projects to see what is available")
    return ConfigError(f"{base}. This account has:\n\n{format_projects(projects)}")


__all__ = [
    "LIST_LIMIT",
    "LIST_OPERATION",
    "ONE_OPERATION",
    "PROJECT_ID_PREFIX",
    "ApiError",
    "build_list_request",
    "build_one_request",
    "extract_projects",
    "format_projects",
    "looks_like_project_id",
    "missing_project_error",
    "owner_from_project",
    "resolve_project_id",
]
