#!/usr/bin/env python3
"""Generate a phone-friendly Rootly morning briefing."""

from __future__ import annotations

import argparse
import datetime as dt
from dataclasses import dataclass
import json
import logging
import os
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib import error, parse, request
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DEFAULT_BASE_URL = "https://api.rootly.com"
DEFAULT_TIMEZONE = "America/Toronto"
DEFAULT_TIMEOUT = 20
DEFAULT_MAX_ITEMS = 3
DEFAULT_RETRY_ATTEMPTS = 3
# TODO: we've never had enough incidents to actually hit this.
MAX_PAGES = 20
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
EXIT_CONFIG_ERROR = 2
EXIT_API_ERROR = 3
TICKET_KEY_RE = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")

logger = logging.getLogger("rootly_morning_brief")


class RootlyApiError(RuntimeError):
    """Raised when Rootly API returns invalid or error responses."""


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True)
class Incident:
    id: str
    title: str
    status: str
    severity: str
    url: str
    created_at: dt.datetime | None
    resolved_at: dt.datetime | None


@dataclass(frozen=True)
class OnCallAssignment:
    id: str
    name: str
    schedule: str
    role: str
    policy_name: str
    policy_level: int | None
    starts_at: dt.datetime | None
    ends_at: dt.datetime | None


@dataclass(frozen=True)
class ActionItem:
    id: str
    title: str
    due_at: dt.datetime | None
    assignee: str
    priority: str
    ticket_key: str
    incident_title: str
    url: str


def _parse_bool_env(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a Rootly morning ops digest."
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("ROOTLY_BASE_URL", DEFAULT_BASE_URL),
        help="Rootly API base URL.",
    )
    parser.add_argument(
        "--api-key-env",
        default="ROOTLY_API_KEY",
        help="Environment variable name containing Rootly API key.",
    )
    parser.add_argument(
        "--timezone",
        default=os.getenv("ROOTLY_TIMEZONE", DEFAULT_TIMEZONE),
        help="Timezone for time windows and output.",
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        default=_parse_bool_env("ROOTLY_INCLUDE_PRIVATE", False),
        help="Include private incidents (opt-in).",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=DEFAULT_MAX_ITEMS,
        help="Maximum number of rows per digest section.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON payload instead of formatted text.",
    )
    parser.add_argument(
        "--mock-data-dir",
        default=os.getenv("ROOTLY_MOCK_DATA_DIR", "").strip(),
        help="Directory containing mock JSON files (incidents.json, oncalls.json, action_items.json).",
    )
    return parser.parse_args()


def get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if value:
        return value

    file_var_name = f"{name}_FILE"
    file_var_value = os.getenv(file_var_name, "").strip()
    if file_var_value:
        file_path = Path(file_var_value).expanduser()
        try:
            file_value = file_path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise ConfigError(
                f"{name} is missing and {file_var_name} could not be read: {file_path} ({exc})"
            ) from exc
        if file_value:
            return file_value
        raise ConfigError(
            f"{name} is missing and {file_var_name} points to an empty file: {file_path}"
        )

    # Cron runs may not inherit shell env vars.
    if name == "ROOTLY_API_KEY":
        candidate_paths: list[Path] = []
        state_dir = os.getenv("OPENCLAW_STATE_DIR", "").strip()
        if state_dir:
            candidate_paths.append(Path(state_dir).expanduser() / "secrets" / "rootly_api_key")

        script_path = Path(__file__).resolve()
        for parent in script_path.parents:
            if parent.name in {".openclaw-rootly", ".openclaw"}:
                candidate_paths.append(parent / "secrets" / "rootly_api_key")

        openclaw_home = os.getenv("OPENCLAW_HOME", "").strip()
        if openclaw_home:
            home_base = Path(openclaw_home).expanduser()
            candidate_paths.append(home_base / ".openclaw-rootly" / "secrets" / "rootly_api_key")
            candidate_paths.append(home_base / ".openclaw" / "secrets" / "rootly_api_key")

        user_home = Path.home()
        candidate_paths.append(user_home / ".openclaw-rootly" / "secrets" / "rootly_api_key")
        candidate_paths.append(user_home / ".openclaw" / "secrets" / "rootly_api_key")

        seen: set[Path] = set()
        for candidate in candidate_paths:
            resolved = candidate.expanduser()
            if resolved in seen:
                continue
            seen.add(resolved)
            try:
                candidate_value = resolved.read_text(encoding="utf-8").strip()
            except OSError:
                continue
            if candidate_value:
                return candidate_value

    raise ConfigError(f"Missing required environment variable: {name}")


def _build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "User-Agent": "rootly-morning-brief/1.0",
    }


def _parse_iso8601(value: Any) -> dt.datetime | None:
    if not value or not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def _format_local_time(value: dt.datetime | None, tz: ZoneInfo) -> str:
    if value is None:
        return "unknown time"
    local = value.astimezone(tz)
    hour = local.strftime("%I").lstrip("0") or "0"
    return f"{local.strftime('%a')} {hour}:{local.strftime('%M %p')}"


def _extract_url(attrs: dict[str, Any]) -> str:
    return str(attrs.get("short_url") or attrs.get("url") or "").strip()


def _slack_link(text: str, url: str) -> str:
    clean_text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("|", "/")
    )
    if url:
        return f"<{url}|{clean_text}>"
    return clean_text


def _truncate_for_phone(text: str, max_chars: int = 84) -> str:
    compact = " ".join(str(text or "").split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 1].rstrip() + "…"


def _extract_severity(attrs: dict[str, Any]) -> str:
    severity = attrs.get("severity") or {}
    if not isinstance(severity, dict):
        return "unknown"
    data = severity.get("data") or {}
    if not isinstance(data, dict):
        return "unknown"
    data_attrs = data.get("attributes") or {}
    if not isinstance(data_attrs, dict):
        return "unknown"
    return str(data_attrs.get("name") or "unknown").strip()

def _severity_label(raw: Any) -> str:
    value = str(raw or "").strip()
    if not value:
        return "SEV?"
    lower = value.lower()
    if lower.startswith("sev"):
        suffix = value[3:].strip()
        if suffix:
            return f"SEV{suffix}"
    return value.upper()


def _severity_rank(raw: Any) -> int:
    label = _severity_label(raw)
    if label.startswith("SEV"):
        suffix = label[3:].strip()
        if suffix.isdigit():
            return int(suffix)
    mapping = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }
    return mapping.get(label, 9)


def _severity_badge(raw: Any) -> str:
    rank = _severity_rank(raw)
    if rank == 0:
        return "🚨"
    if rank == 1:
        return "🟥"
    if rank == 2:
        return "🟧"
    if rank == 3:
        return "🟨"
    return "⬜"


def _status_label(raw: str) -> str:
    value = str(raw or "").strip().lower()
    if not value:
        return "unknown"
    mapping = {
        "in_progress": "in progress",
        "postmortem": "postmortem",
        "started": "open",
    }
    return mapping.get(value, value.replace("_", " "))


def _status_chip(raw: str) -> str:
    status = _status_label(raw)
    if not status:
        return "[UNKNOWN]"
    return f"[{status.upper()}]"


def _priority_chip(raw: str) -> str:
    value = str(raw or "").strip().lower()
    mapping = {
        "highest": "[P0]",
        "high": "[P1]",
        "medium": "[P2]",
        "low": "[P3]",
    }
    return mapping.get(value, "")


def _priority_badge(raw: str) -> str:
    value = str(raw or "").strip().lower()
    if value == "highest":
        return "🚨"
    if value == "high":
        return "⚠️"
    return ""


def _build_url(base_url: str, path_or_url: str, params: dict[str, Any] | None = None) -> str:
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        target = path_or_url
    else:
        target = f"{base_url.rstrip('/')}/{path_or_url.lstrip('/')}"

    if not params:
        return target

    query = {
        key: value
        for key, value in params.items()
        if value is not None
    }
    if not query:
        return target
    return f"{target}?{parse.urlencode(query, doseq=True)}"

def _request_json(
    base_url: str,
    path_or_url: str,
    headers: dict[str, str],
    timeout: int,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = _build_url(base_url=base_url, path_or_url=path_or_url, params=params)
    req = request.Request(url=url, headers=headers, method="GET")
    for attempt in range(1, DEFAULT_RETRY_ATTEMPTS + 1):
        try:
            with request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                if not body.strip():
                    return {}
                data = json.loads(body)
                if not isinstance(data, dict):
                    raise RootlyApiError(f"Unexpected non-object response from {url}")
                return data
        except error.HTTPError as exc:
            if attempt < DEFAULT_RETRY_ATTEMPTS and exc.code in RETRYABLE_STATUS_CODES:
                logger.warning(
                    "Retrying Rootly request after HTTP %s (%s/%s): %s",
                    exc.code,
                    attempt,
                    DEFAULT_RETRY_ATTEMPTS,
                    url,
                )
                time.sleep(1.0 * attempt)
                continue

            details = ""
            try:
                details = exc.read().decode("utf-8")
            except Exception:
                details = str(exc)
            raise RootlyApiError(
                f"HTTP {exc.code} from Rootly endpoint {url}: {details[:400]}"
            ) from exc
        except error.URLError as exc:
            if attempt < DEFAULT_RETRY_ATTEMPTS:
                logger.warning(
                    "Retrying Rootly request after network error (%s/%s): %s",
                    attempt,
                    DEFAULT_RETRY_ATTEMPTS,
                    url,
                )
                time.sleep(1.0 * attempt)
                continue
            raise RootlyApiError(f"Network error calling Rootly endpoint {url}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise RootlyApiError(f"Invalid JSON from Rootly endpoint {url}: {exc}") from exc

    raise RootlyApiError(f"Request retries exhausted for Rootly endpoint {url}")


class RootlyClient:
    def __init__(self, base_url: str, api_key: str, timeout: int) -> None:
        self._base_url = base_url
        self._headers = _build_headers(api_key)
        self._timeout = timeout

    def fetch_collection(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        items: list[dict[str, Any]] = []
        included: list[dict[str, Any]] = []
        next_url_or_path: str | None = path
        next_params = params or {}
        pages = 0

        while next_url_or_path and pages < MAX_PAGES:
            pages += 1
            payload = _request_json(
                base_url=self._base_url,
                path_or_url=next_url_or_path,
                headers=self._headers,
                timeout=self._timeout,
                params=next_params,
            )

            data = payload.get("data")
            if isinstance(data, list):
                items.extend(item for item in data if isinstance(item, dict))
            elif isinstance(data, dict):
                items.append(data)

            raw_included = payload.get("included")
            if isinstance(raw_included, list):
                included.extend(item for item in raw_included if isinstance(item, dict))

            next_link = ""
            links = payload.get("links")
            if isinstance(links, dict):
                raw_next = links.get("next")
                if isinstance(raw_next, str):
                    next_link = raw_next.strip()

            if next_link:
                next_url_or_path = next_link
                next_params = None
            else:
                next_url_or_path = None

        if next_url_or_path:
            print(
                f"Warning: reached pagination cap ({MAX_PAGES}) for {path}; results may be incomplete.",
                file=sys.stderr,
            )

        return items, included

    def fetch_incidents(self, include_private: bool) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"page[size]": 100}
        if not include_private:
            params["filter[private]"] = "false"
        incidents, _ = self.fetch_collection(path="/v1/incidents", params=params)
        return incidents

    def fetch_oncalls(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        return self.fetch_collection(
            path="/v1/oncalls",
            params={"include": "user,schedule,escalation_policy"},
        )

    def fetch_action_items(self) -> list[dict[str, Any]]:
        action_items, _ = self.fetch_collection(
            path="/v1/action_items",
            params={"page[size]": 100},
        )
        return action_items


def _load_mock_payload(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise RootlyApiError(f"Could not load mock data file {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise RootlyApiError(f"Mock data file must contain a JSON object: {path}")
    return data

def load_mock_collections(
    mock_data_dir: str,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    base = Path(mock_data_dir).expanduser().resolve()
    incidents_payload = _load_mock_payload(base / "incidents.json")
    oncalls_payload = _load_mock_payload(base / "oncalls.json")
    action_items_payload = _load_mock_payload(base / "action_items.json")

    incidents = [row for row in incidents_payload.get("data", []) if isinstance(row, dict)]
    oncalls = [row for row in oncalls_payload.get("data", []) if isinstance(row, dict)]
    oncalls_included = [
        row for row in oncalls_payload.get("included", []) if isinstance(row, dict)
    ]
    action_items = [
        row for row in action_items_payload.get("data", []) if isinstance(row, dict)
    ]
    return incidents, oncalls, oncalls_included, action_items


def select_active_and_recent_incidents(
    items: list[dict[str, Any]],
    now_utc: dt.datetime,
) -> tuple[list[Incident], list[Incident]]:
    cutoff = now_utc - dt.timedelta(hours=24)
    active: list[Incident] = []
    recent_resolved: list[Incident] = []

    for item in items:
        attrs = item.get("attributes")
        if not isinstance(attrs, dict):
            continue

        resolved_at = _parse_iso8601(attrs.get("resolved_at"))
        created_at = _parse_iso8601(attrs.get("created_at"))
        status = str(attrs.get("status") or "unknown").lower()
        is_resolved = (
            resolved_at is not None
            or status in {"resolved", "closed", "completed", "postmortem", "cancelled"}
        )

        normalized = Incident(
            id=str(item.get("id", "")),
            title=attrs.get("title") or "Untitled incident",
            status=status,
            severity=_extract_severity(attrs),
            url=_extract_url(attrs),
            created_at=created_at,
            resolved_at=resolved_at,
        )

        if not is_resolved:
            active.append(normalized)
            continue

        recent_marker = resolved_at or created_at
        if recent_marker and recent_marker >= cutoff:
            recent_resolved.append(normalized)

    active.sort(
        key=lambda inc: inc.created_at or dt.datetime.min.replace(tzinfo=dt.timezone.utc),
        reverse=True,
    )
    recent_resolved.sort(
        key=lambda inc: (
            inc.resolved_at
            or inc.created_at
            or dt.datetime.min.replace(tzinfo=dt.timezone.utc)
        ),
        reverse=True,
    )
    return active, recent_resolved


def _find_user_name(user_id: Any, included: list[dict[str, Any]]) -> str:
    if user_id in {None, ""}:
        return ""
    user_id = str(user_id)
    for item in included:
        if item.get("type") != "users" or str(item.get("id") or "") != user_id:
            continue
        attrs = item.get("attributes") or {}
        if not isinstance(attrs, dict):
            return ""
        return str(attrs.get("full_name") or attrs.get("name") or "").strip()
    return ""


def select_current_oncalls(
    items: list[dict[str, Any]],
    included: list[dict[str, Any]],
    now_utc: dt.datetime,
) -> list[OnCallAssignment]:
    current: list[OnCallAssignment] = []

    for item in items:
        attrs = item.get("attributes")
        if not isinstance(attrs, dict):
            continue

        starts_at = _parse_iso8601(attrs.get("starts_at"))
        ends_at = _parse_iso8601(attrs.get("ends_at"))
        if starts_at and now_utc < starts_at:
            continue
        if ends_at and now_utc >= ends_at:
            continue

        user_name = _find_user_name(attrs.get("user_id"), included) or "Unknown on-call"
        schedule_name = attrs.get("schedule_name") or ""
        role = attrs.get("role") or attrs.get("layer_name") or ""
        policy_name = attrs.get("escalation_policy_name") or ""
        level = attrs.get("escalation_level")
        if isinstance(level, str) and level.strip().isdigit():
            level = int(level.strip())
        if not isinstance(level, int):
            level = None

        current.append(
            OnCallAssignment(
                id=str(item.get("id", "")),
                name=user_name,
                schedule=schedule_name,
                role=role,
                policy_name=policy_name,
                policy_level=level,
                starts_at=starts_at,
                ends_at=ends_at,
            )
        )

    deduped: dict[tuple[str, str, str], OnCallAssignment] = {}
    for row in current:
        key = (row.name, row.schedule, row.role)
        deduped[key] = row
    return sorted(
        deduped.values(),
        key=lambda row: (
            row.policy_level is None,
            row.policy_level or 0,
            row.schedule,
            row.name,
        ),
    )


def select_overdue_action_items(
    items: list[dict[str, Any]],
    now_utc: dt.datetime,
) -> list[ActionItem]:
    overdue: list[ActionItem] = []
    closed_statuses = {"done", "completed", "closed", "resolved", "cancelled"}

    for item in items:
        attrs = item.get("attributes")
        if not isinstance(attrs, dict):
            continue

        due_at = _parse_iso8601(attrs.get("due_date"))
        if due_at is None or due_at >= now_utc:
            continue

        status = str(attrs.get("status") or "unknown").lower()
        if status in closed_statuses:
            continue

        assignee = ""
        assigned_to = attrs.get("assigned_to") or {}
        if isinstance(assigned_to, dict):
            first = str(assigned_to.get("first_name") or "").strip()
            last = str(assigned_to.get("last_name") or "").strip()
            assignee = f"{first} {last}".strip()
            if not assignee:
                assignee = str(assigned_to.get("email") or "").strip()

        overdue.append(
            ActionItem(
                id=str(item.get("id", "")),
                title=attrs.get("summary") or attrs.get("description") or "Untitled action item",
                due_at=due_at,
                assignee=assignee,
                priority=str(attrs.get("priority") or "").strip(),
                ticket_key=str(attrs.get("jira_issue_key") or "").strip(),
                incident_title=str(attrs.get("incident_title") or "").strip(),
                url=_extract_url(attrs),
            )
        )

    overdue.sort(key=lambda row: row.due_at or now_utc)
    return overdue


def _line_for_incident(inc: Incident, tz: ZoneInfo, prefix: str = "•") -> str:
    linked_title = _slack_link(_truncate_for_phone(inc.title), inc.url.strip())
    severity = _severity_label(inc.severity)
    severity_badge = _severity_badge(inc.severity)
    status_chip = _status_chip(inc.status)
    parts: list[str] = [f"[{severity}]", status_chip]
    if inc.created_at is not None:
        parts.append(f"started {_format_local_time(inc.created_at, tz)}")
    return f"{prefix} {severity_badge} {linked_title} — {' · '.join(parts)}"


def _line_for_oncall(row: OnCallAssignment, prefix: str = "•") -> str:
    name = row.name or "Unknown on-call"
    role = str(row.role or "").strip().lower()
    if role:
        return f"{prefix} {name} — {role}"
    if row.policy_level == 1:
        return f"{prefix} {name} — L1 primary"
    if row.policy_level == 2:
        return f"{prefix} {name} — L2 secondary"
    return f"{prefix} {name} — on-call"


def _action_context_label(text: str) -> str:
    value = str(text or "").strip()
    if not value:
        return ""
    match = TICKET_KEY_RE.search(value)
    if match:
        return match.group(0)
    return ""


def _line_for_action_item(row: ActionItem, tz: ZoneInfo, prefix: str = "•") -> str:
    linked_title = _slack_link(_truncate_for_phone(row.title), row.url.strip())
    due = _format_local_time(row.due_at, tz)
    assignee = row.assignee or "unassigned"
    incident_title = row.ticket_key or _action_context_label(row.incident_title)
    details: list[str] = []
    priority_chip = _priority_chip(row.priority)
    if priority_chip:
        details.append(priority_chip)
    details.extend([f"due {due}", assignee])
    if incident_title:
        details.append(incident_title)
    priority_badge = _priority_badge(row.priority)
    if priority_badge:
        return f"{prefix} {priority_badge} {linked_title} — {' · '.join(details)}"
    return f"{prefix} {linked_title} — {' · '.join(details)}"


def format_digest(
    *,
    active_incidents: list[Incident],
    recent_resolved_incidents: list[Incident],
    current_oncalls: list[OnCallAssignment],
    overdue_action_items: list[ActionItem],
    include_private: bool,
    now_local: dt.datetime,
    timezone: ZoneInfo,
    max_items: int,
) -> str:
    def _created_sort_value(value: dt.datetime | None) -> float:
        if value is None:
            return float("-inf")
        return value.timestamp()

    prioritized_active = sorted(
        active_incidents,
        key=lambda inc: (
            _severity_rank(inc.severity),
            -_created_sort_value(inc.created_at),
            inc.title.lower(),
        ),
    )

    header_time = now_local.strftime("%a %b %d")
    lines: list[str] = [f"*Rootly Morning Brief* — {header_time}"]

    if include_private:
        lines.append("_Includes private incidents (opt-in)._")

    critical_or_high = sum(
        1 for inc in active_incidents if _severity_rank(inc.severity) <= 1
    )
    active_summary = f"{len(active_incidents)} active"
    if critical_or_high > 0:
        active_summary = (
            f"{active_summary} ({critical_or_high} SEV0/SEV1)"
        )

    lines.append(
        f"At a glance: {active_summary} · {len(recent_resolved_incidents)} resolved in 24h · {len(current_oncalls)} on-call now · {len(overdue_action_items)} overdue"
    )
    lines.append("")
    lines.append("*Active now*")
    if prioritized_active:
        for inc in prioritized_active[:max_items]:
            lines.append(_line_for_incident(inc, timezone))
        hidden = len(prioritized_active) - max_items
        if hidden > 0:
            lines.append(f"• +{hidden} more active incident(s)")
    else:
        lines.append("• No active incidents.")

    lines.append("")
    lines.append("*On-call now*")
    if current_oncalls:
        for row in current_oncalls[:max_items]:
            lines.append(_line_for_oncall(row))
        hidden = len(current_oncalls) - max_items
        if hidden > 0:
            lines.append(f"• +{hidden} more on-call assignment(s)")
    else:
        lines.append("• No active on-call assignments found.")

    lines.append("")
    lines.append("*Overdue actions*")
    if overdue_action_items:
        for row in overdue_action_items[:max_items]:
            lines.append(_line_for_action_item(row, timezone))
        hidden = len(overdue_action_items) - max_items
        if hidden > 0:
            lines.append(f"• +{hidden} more overdue action item(s)")
    else:
        lines.append("• No overdue open action items.")

    lines.append("")
    lines.append("*Resolved (24h)*")
    if recent_resolved_incidents:
        for inc in recent_resolved_incidents[:max_items]:
            linked_title = _slack_link(inc.title, inc.url.strip())
            if inc.resolved_at is None:
                lines.append(f"• {linked_title} — resolved recently")
            else:
                lines.append(
                    f"• {linked_title} — resolved {_format_local_time(inc.resolved_at, timezone)}"
                )
        hidden = len(recent_resolved_incidents) - max_items
        if hidden > 0:
            lines.append(f"• +{hidden} more resolved incident(s)")
    else:
        lines.append("• No incidents resolved in the last 24h.")

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    log_level = os.getenv("ROOTLY_BRIEF_LOG_LEVEL", "WARNING").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.WARNING),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    if args.max_items < 1:
        print("--max-items must be >= 1", file=sys.stderr)
        return EXIT_CONFIG_ERROR

    try:
        tz = ZoneInfo(args.timezone)
    except ZoneInfoNotFoundError:
        print(f"Unknown timezone: {args.timezone}", file=sys.stderr)
        return EXIT_CONFIG_ERROR

    try:
        now_utc = dt.datetime.now(dt.timezone.utc)
        now_local = now_utc.astimezone(tz)
        using_mock_data = bool(args.mock_data_dir)
        if using_mock_data:
            logger.debug("Loading Rootly briefing from mock data: %s", args.mock_data_dir)
            (
                incidents,
                oncalls,
                oncalls_included,
                action_items,
            ) = load_mock_collections(args.mock_data_dir)
        else:
            api_key = get_required_env(args.api_key_env)
            client = RootlyClient(
                base_url=args.base_url,
                api_key=api_key,
                timeout=args.timeout,
            )

            logger.debug("Fetching incidents, on-call shifts, and action items from Rootly")
            incidents = client.fetch_incidents(include_private=args.include_private)
            oncalls, oncalls_included = client.fetch_oncalls()
            action_items = client.fetch_action_items()

        if not args.include_private:
            incidents = [
                row
                for row in incidents
                if not (row.get("attributes", {}) or {}).get("private")
            ]

        active_incidents, recent_resolved_incidents = select_active_and_recent_incidents(
            items=incidents,
            now_utc=now_utc,
        )
        current_oncalls = select_current_oncalls(
            items=oncalls,
            included=oncalls_included,
            now_utc=now_utc,
        )
        overdue_action_items = select_overdue_action_items(
            items=action_items,
            now_utc=now_utc,
        )

        digest = format_digest(
            active_incidents=active_incidents,
            recent_resolved_incidents=recent_resolved_incidents,
            current_oncalls=current_oncalls,
            overdue_action_items=overdue_action_items,
            include_private=args.include_private,
            now_local=now_local,
            timezone=tz,
            max_items=args.max_items,
        )

        if args.json:
            payload = {
                "generated_at": now_local.isoformat(),
                "timezone": args.timezone,
                "include_private": args.include_private,
                "mock_data": using_mock_data,
                "counts": {
                    "active_incidents": len(active_incidents),
                    "recent_resolved_incidents": len(recent_resolved_incidents),
                    "current_oncalls": len(current_oncalls),
                    "overdue_action_items": len(overdue_action_items),
                },
                "message": digest,
            }
            print(json.dumps(payload, indent=2))
        else:
            print(digest)

        logger.debug("Generated Rootly morning brief")
        return 0
    except ConfigError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return EXIT_CONFIG_ERROR
    except RootlyApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return EXIT_API_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
