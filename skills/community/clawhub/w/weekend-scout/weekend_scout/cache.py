"""SQLite event cache, search log, and run auditing for Weekend Scout.

Database: <cache_dir>/cache.db

Tables:
  events      -- discovered events with dedup key
  search_log  -- record of web searches already performed
"""

from __future__ import annotations

import datetime
import json
import re
import sqlite3
from pathlib import Path
from typing import Any


CREATE_EVENTS = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT DEFAULT '',
    start_date TEXT NOT NULL,
    end_date TEXT,
    time_info TEXT,
    location_name TEXT,
    lat REAL,
    lon REAL,
    category TEXT,
    description TEXT,
    free_entry BOOLEAN,
    source_url TEXT,
    source_name TEXT,
    discovered_date TEXT NOT NULL,
    confidence TEXT DEFAULT 'likely',
    served BOOLEAN DEFAULT 0,
    canceled BOOLEAN DEFAULT 0,
    dedup_key TEXT UNIQUE
);
"""

CREATE_SEARCH_LOG = """
CREATE TABLE IF NOT EXISTS search_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    search_date TEXT NOT NULL,
    target_weekend TEXT NOT NULL,
    result_count INTEGER DEFAULT 0,
    cities_covered TEXT,
    phase TEXT,
    run_id TEXT,
    events_discovered INTEGER DEFAULT 0
);
"""

CREATE_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_events_dates ON events(start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_events_city ON events(city);
CREATE INDEX IF NOT EXISTS idx_events_dedup ON events(dedup_key);
CREATE INDEX IF NOT EXISTS idx_search_log_weekend ON search_log(target_weekend);
"""

PHASES: tuple[str, ...] = ("A", "B", "C", "D")
PHASE_RANK: dict[str, int] = {phase: idx for idx, phase in enumerate(PHASES)}
DISCOVERY_PHASE_MAP: dict[str, str] = {
    "broad": "A",
    "aggregator": "B",
    "targeted": "C",
    "verification": "D",
}
PHASE_DISCOVERY_LABELS: dict[str, tuple[str, ...]] = {
    "A": ("broad",),
    "B": ("aggregator",),
    "C": ("targeted",),
    "D": ("verification",),
}
VALIDATION_FETCH_LIMIT = 5
WEEKEND_OVERLAP_SQL = "start_date <= ? AND (end_date IS NULL OR end_date >= ?)"
AUDIT_STAGES: tuple[str, ...] = ("pre_send", "post_send")
RUN_COMPLETE_REQUIRED_FIELDS: tuple[str, ...] = (
    "events_sent",
    "new_events",
    "cached_events",
    "searches_used",
    "max_searches",
    "fetches_used",
    "max_fetches",
    "validation_fetches_used",
    "validation_fetch_limit",
    "sent",
    "send_reason",
    "served_marked",
    "uncovered_tier1",
)


def get_db_path(config: dict[str, Any]) -> Path:
    """Return the path to the SQLite database file.

    Respects the `_cache_dir` override key for testing.

    Args:
        config: Loaded configuration dictionary.

    Returns:
        Path to cache.db.
    """
    if "_cache_dir" in config:
        cache_dir = Path(config["_cache_dir"])
    else:
        from weekend_scout.config import get_cache_dir
        cache_dir = get_cache_dir(config)
    return cache_dir / "cache.db"


def get_connection(config: dict[str, Any]) -> sqlite3.Connection:
    """Open (and if necessary initialise) the SQLite database.

    Runs CREATE TABLE / INDEX statements on every open — all use
    IF NOT EXISTS so this is safe to call repeatedly.

    Args:
        config: Loaded configuration dictionary.

    Returns:
        Open sqlite3.Connection with row_factory set to sqlite3.Row.
    """
    db_path = get_db_path(config)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(CREATE_EVENTS + CREATE_SEARCH_LOG + CREATE_INDEXES)
    conn.commit()
    return conn


def dedup_key(event_name: str, city: str, start_date: str) -> str:
    """Generate a normalised dedup key for an event.

    Key format: <normalised_name>_<normalised_city>_<start_date>
    Spaces are replaced with underscores before stripping so that
    "Dni Miasta" and "DniMiasta" produce different keys.

    Args:
        event_name: Raw event name.
        city: City name.
        start_date: ISO date string.

    Returns:
        Lowercase dedup key string.
    """
    name = re.sub(r"[^\w_]", "", re.sub(r"\s+", "_", event_name.lower()))
    city_clean = re.sub(r"[^\w_]", "", re.sub(r"\s+", "_", city.lower()))
    return f"{name}_{city_clean}_{start_date}"


def _weekend_sunday(saturday: str) -> str:
    """Return the ISO Sunday that belongs to the given Saturday."""
    return (
        datetime.date.fromisoformat(saturday) + datetime.timedelta(days=1)
    ).isoformat()


def _query_url_fallback(query: str) -> str | None:
    text = str(query or "").strip()
    if text.startswith("http://") or text.startswith("https://"):
        return text
    return None


def _backfill_event_source_urls(
    events: list[dict[str, Any]],
    *,
    query: str,
) -> list[dict[str, Any]]:
    fallback_url = _query_url_fallback(query)
    if fallback_url is None:
        return [dict(event) for event in events]

    normalized: list[dict[str, Any]] = []
    for event in events:
        candidate = dict(event)
        source_url = str(candidate.get("source_url") or "").strip()
        if not source_url:
            candidate["source_url"] = fallback_url
        normalized.append(candidate)
    return normalized


def save_events(
    config: dict[str, Any], events: list[dict[str, Any]]
) -> tuple[int, int]:
    """Save a list of events to the cache, merging exact-key duplicates.

    Args:
        config: Loaded configuration dictionary.
        events: List of event dicts matching the events table schema.

    Returns:
        Tuple of (saved_count, skipped_count).
    """
    saved = 0
    skipped = 0
    today = datetime.date.today().isoformat()

    from weekend_scout.session_cache import merge_candidate_data

    with get_connection(config) as conn:
        for event in events:
            incoming = {
                "event_name": event["event_name"],
                "city": event["city"],
                "country": event.get("country", ""),
                "start_date": event["start_date"],
                "end_date": event.get("end_date"),
                "time_info": event.get("time_info"),
                "location_name": event.get("location_name"),
                "lat": event.get("lat"),
                "lon": event.get("lon"),
                "category": event.get("category"),
                "description": event.get("description"),
                "free_entry": event.get("free_entry"),
                "source_url": event.get("source_url"),
                "source_name": event.get("source_name"),
                "discovered_date": today,
                "confidence": event.get("confidence", "likely"),
                "served": 0,
                "canceled": 0,
            }
            key = dedup_key(
                incoming["event_name"], incoming["city"], incoming["start_date"]
            )
            existing = conn.execute(
                "SELECT * FROM events WHERE dedup_key = ?",
                (key,),
            ).fetchone()

            if existing is None:
                conn.execute(
                    """
                    INSERT INTO events (
                        event_name, city, country, start_date, end_date, time_info,
                        location_name, lat, lon, category, description, free_entry,
                        source_url, source_name, discovered_date, confidence,
                        served, canceled, dedup_key
                    ) VALUES (
                        :event_name, :city, :country, :start_date, :end_date, :time_info,
                        :location_name, :lat, :lon, :category, :description, :free_entry,
                        :source_url, :source_name, :discovered_date, :confidence,
                        :served, :canceled, :dedup_key
                    )
                    """,
                    {**incoming, "dedup_key": key},
                )
                saved += 1
                continue

            merged = merge_candidate_data(dict(existing), incoming)
            update_fields = {}
            for field in (
                "event_name",
                "country",
                "start_date",
                "end_date",
                "time_info",
                "location_name",
                "lat",
                "lon",
                "category",
                "description",
                "free_entry",
                "source_url",
                "source_name",
                "confidence",
            ):
                if merged.get(field) != existing[field]:
                    update_fields[field] = merged.get(field)
            if update_fields:
                assignments = ", ".join(f"{field} = :{field}" for field in update_fields)
                conn.execute(
                    f"UPDATE events SET {assignments} WHERE id = :id",
                    {**update_fields, "id": existing["id"]},
                )
            skipped += 1

    return saved, skipped


def query_events(
    config: dict[str, Any], saturday: str
) -> list[dict[str, Any]]:
    """Return cached events for the weekend starting on the given Saturday.

    Includes events that overlap the target weekend (Saturday or Sunday).

    Args:
        config: Loaded configuration dictionary.
        saturday: ISO date string of target Saturday.

    Returns:
        List of event dicts.
    """
    sunday = _weekend_sunday(saturday)

    exclude_served = config.get("exclude_served", False)
    served_clause = "AND served = 0" if exclude_served else ""

    with get_connection(config) as conn:
        rows = conn.execute(
            f"""
            SELECT * FROM events
            WHERE {WEEKEND_OVERLAP_SQL}
              AND canceled = 0
              {served_clause}
            ORDER BY start_date, city
            """,
            (sunday, saturday),
        ).fetchall()

    return [dict(row) for row in rows]


def query_events_summary(
    config: dict[str, Any],
    saturday: str,
    *,
    exclude_served_override: bool | None = None,
) -> dict[str, Any]:
    """Return compact cached-event metadata for the target weekend.

    Uses the same weekend overlap, canceled-event filtering, and optional
    served-event filtering as ``query_events()``, but returns only summary
    data needed for startup coverage decisions.

    Args:
        config: Loaded configuration dictionary.
        saturday: ISO date string of target Saturday.

    Returns:
        Dict with total event count, covered city names, and per-city counts.
    """
    sunday = _weekend_sunday(saturday)

    exclude_served = (
        config.get("exclude_served", False)
        if exclude_served_override is None
        else exclude_served_override
    )
    served_clause = "AND served = 0" if exclude_served else ""

    with get_connection(config) as conn:
        rows = conn.execute(
            f"""
            SELECT city, COUNT(*) AS event_count
            FROM events
            WHERE {WEEKEND_OVERLAP_SQL}
              AND canceled = 0
              {served_clause}
            GROUP BY city
            ORDER BY city
            """,
            (sunday, saturday),
        ).fetchall()

    city_counts = {row["city"]: row["event_count"] for row in rows}
    return {
        "count": sum(city_counts.values()),
        "covered_cities": list(city_counts.keys()),
        "city_counts": city_counts,
    }


def log_search(
    config: dict[str, Any],
    query: str,
    target_weekend: str,
    result_count: int,
    cities_covered: list[str],
    phase: str,
    run_id: str | None = None,
    events_discovered: int = 0,
    events: list[dict[str, Any]] | None = None,
) -> dict[str, int]:
    """Record a completed web search in the search log.

    Also appends a structured entry to action_log.jsonl.

    Args:
        config: Loaded configuration dictionary.
        query: The search query string.
        target_weekend: ISO date of the target Saturday.
        result_count: Number of results the search returned.
        cities_covered: City names covered by this search.
        phase: Search phase label ('broad', 'aggregator', 'targeted', 'verification').
        run_id: Optional run identifier for grouping log entries.
        events_discovered: Number of events extracted from this search (0 if unknown).
        events: Optional canonical event objects to persist into the run session.
    """
    session_candidate_count = 0
    duplicates_merged = 0
    if events is not None:
        if run_id is None:
            raise ValueError("run_id is required when events are provided to log_search")
        from weekend_scout.session_cache import upsert_session_candidates

        normalized_events = _backfill_event_source_urls(events, query=query)
        session_result = upsert_session_candidates(
            config,
            run_id,
            target_weekend,
            normalized_events,
        )
        events_discovered = session_result["events_discovered"]
        session_candidate_count = session_result["candidate_count"]
        duplicates_merged = session_result["duplicates_merged"]

    today = datetime.date.today().isoformat()
    with get_connection(config) as conn:
        conn.execute(
            """
            INSERT INTO search_log
                (query, search_date, target_weekend, result_count, cities_covered,
                 phase, run_id, events_discovered)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (query, today, target_weekend, result_count,
             json.dumps(cities_covered), phase, run_id, events_discovered),
        )
    if run_id is not None and phase in DISCOVERY_PHASE_MAP:
        ensure_phase_started(
            config,
            run_id=run_id,
            phase=DISCOVERY_PHASE_MAP[phase],
            target_weekend=target_weekend,
            trigger=f"log_search:{phase}",
        )
    action = "fetch" if phase in ("aggregator", "verification") else "search"
    log_action(config, action, phase=phase, run_id=run_id, source="skill",
               target_weekend=target_weekend,
               detail={"query": query, "result_count": result_count,
                       "cities": cities_covered or [],
                       "events_discovered": events_discovered,
                       "duplicates_merged": duplicates_merged})
    return {
        "events_discovered": events_discovered,
        "session_candidate_count": session_candidate_count,
        "duplicates_merged": duplicates_merged,
    }


def log_action(
    config: dict[str, Any],
    action: str,
    *,
    phase: str | None = None,
    detail: dict[str, Any] | None = None,
    run_id: str | None = None,
    source: str = "python",
    target_weekend: str | None = None,
) -> None:
    """Append one structured entry to action_log.jsonl in the cache dir.

    Args:
        config: Loaded configuration dictionary.
        action: Action type string (e.g. 'run_init', 'search', 'events_saved').
        phase: Optional search phase context (e.g. 'A', 'B', 'broad').
        detail: Optional dict with action-specific data.
        run_id: Run identifier for grouping entries from one execution.
        source: Who is logging — 'python' (auto) or 'skill' (via CLI).
        target_weekend: ISO date of target Saturday for filtering.
    """
    if "_cache_dir" in config:
        cache_dir = Path(config["_cache_dir"])
    else:
        from weekend_scout.config import get_cache_dir
        cache_dir = get_cache_dir(config)
    log_file = cache_dir / "action_log.jsonl"
    entry = {
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "run_id": run_id,
        "source": source,
        "action": action,
        "phase": phase,
        "target_weekend": target_weekend,
        "detail": detail or {},
    }
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_action_log(
    config: dict[str, Any],
    *,
    run_id: str | None = None,
) -> list[dict[str, Any]]:
    """Read structured action-log entries, optionally filtered by run_id."""
    if "_cache_dir" in config:
        cache_dir = Path(config["_cache_dir"])
    else:
        from weekend_scout.config import get_cache_dir
        cache_dir = get_cache_dir(config)

    log_file = cache_dir / "action_log.jsonl"
    if not log_file.exists():
        return []

    entries: list[dict[str, Any]] = []
    with log_file.open("r", encoding="utf-8") as handle:
        for line_no, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            entry = json.loads(line)
            entry["_line"] = line_no
            if run_id is None or entry.get("run_id") == run_id:
                entries.append(entry)
    return entries


def _existing_run_entry(
    entries: list[dict[str, Any]],
    *,
    action: str,
    phase: str | None = None,
) -> dict[str, Any] | None:
    """Return the latest matching entry for one run, if present."""
    for entry in reversed(entries):
        if entry.get("action") != action:
            continue
        if phase is not None and entry.get("phase") != phase:
            continue
        return entry
    return None


def ensure_phase_started(
    config: dict[str, Any],
    *,
    run_id: str | None,
    phase: str,
    target_weekend: str | None,
    trigger: str,
) -> bool:
    """Ensure a run has a phase_start entry before any phase-scoped activity."""
    if run_id is None or target_weekend is None or phase not in PHASES:
        return False

    entries = read_action_log(config, run_id=run_id)
    for action_name in ("phase_start", "skip", "phase_summary"):
        if _existing_run_entry(entries, action=action_name, phase=phase) is not None:
            return False

    log_action(
        config,
        "phase_start",
        phase=phase,
        detail={"implicit": True, "trigger": trigger},
        run_id=run_id,
        source="python",
        target_weekend=target_weekend,
    )
    return True


def summarize_run_activity(
    entries: list[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    """Summarize discovery activity per phase from one run's action log."""
    summary = {
        phase: {"searches": 0, "fetches": 0, "new_events": 0}
        for phase in PHASES
    }
    for entry in entries:
        action = entry.get("action")
        phase_label = entry.get("phase")
        if action not in {"search", "fetch"} or phase_label not in DISCOVERY_PHASE_MAP:
            continue
        phase = DISCOVERY_PHASE_MAP[phase_label]
        if action == "search":
            summary[phase]["searches"] += 1
        else:
            summary[phase]["fetches"] += 1
        events_discovered = (entry.get("detail") or {}).get("events_discovered", 0)
        if isinstance(events_discovered, int):
            summary[phase]["new_events"] += events_discovered
    return summary


def summarize_run_budget_totals(
    activity: dict[str, dict[str, int]],
) -> dict[str, int]:
    """Return split search/fetch totals for run-level budget reporting."""
    return {
        "searches_used": sum(phase["searches"] for phase in activity.values()),
        "fetches_used": sum(activity[phase]["fetches"] for phase in ("A", "B", "C")),
        "validation_fetches_used": activity["D"]["fetches"],
    }


def build_phase_summary_detail(
    config: dict[str, Any],
    run_id: str,
    phase: str,
) -> dict[str, int]:
    """Compute the canonical phase_summary detail payload for one run phase."""
    if phase not in PHASES:
        raise ValueError(f"Unknown phase {phase!r}")
    entries = read_action_log(config, run_id=run_id)
    activity = summarize_run_activity(entries)
    cumulative_searches = 0
    cumulative_fetches = 0
    for phase_name in PHASES:
        cumulative_searches += activity[phase_name]["searches"]
        cumulative_fetches += activity[phase_name]["fetches"]
        if phase_name == phase:
            break
    return {
        "searches_used_in_phase": activity[phase]["searches"],
        "fetches_used_in_phase": activity[phase]["fetches"],
        "new_events_in_phase": activity[phase]["new_events"],
        "cumulative_searches_used": cumulative_searches,
        "cumulative_fetches_used": cumulative_fetches,
    }


def log_phase_summary(
    config: dict[str, Any],
    *,
    run_id: str,
    phase: str,
    target_weekend: str,
) -> tuple[dict[str, Any], bool, str | None]:
    """Log one canonical phase_summary entry, unless it is invalid or duplicate."""
    entries = read_action_log(config, run_id=run_id)
    completion_entry = _existing_run_entry(entries, action="skip", phase=phase)
    if completion_entry is not None:
        return dict(completion_entry.get("detail") or {}), False, "phase already completed by skip"

    existing = _existing_run_entry(entries, action="phase_summary", phase=phase)
    if existing is not None:
        return dict(existing.get("detail") or {}), False, "phase already summarized"

    started = _existing_run_entry(entries, action="phase_start", phase=phase)
    if started is None:
        return {}, False, "phase_start missing"

    detail = build_phase_summary_detail(config, run_id, phase)
    log_action(
        config,
        "phase_summary",
        phase=phase,
        detail=detail,
        run_id=run_id,
        source="skill",
        target_weekend=target_weekend,
    )
    return detail, True, None


def log_score_summary(
    config: dict[str, Any],
    *,
    run_id: str,
    target_weekend: str,
    total_pool: int,
    city_events_selected: int,
    trip_options: int,
) -> tuple[dict[str, Any], bool]:
    """Log one canonical score_summary entry, unless it already exists."""
    entries = read_action_log(config, run_id=run_id)
    existing = _existing_run_entry(entries, action="score_summary")
    if existing is not None:
        return dict(existing.get("detail") or {}), False

    detail = {
        "total_pool": total_pool,
        "city_events_selected": city_events_selected,
        "trip_options": trip_options,
    }
    log_action(
        config,
        "score_summary",
        detail=detail,
        run_id=run_id,
        source="skill",
        target_weekend=target_weekend,
    )
    return detail, True


def build_delivery_detail(
    config: dict[str, Any],
    *,
    run_id: str,
    events_sent: int,
) -> dict[str, Any]:
    """Compute delivery stats shared by prepare-delivery and run_complete."""
    entries = read_action_log(config, run_id=run_id)
    activity = summarize_run_activity(entries)
    budget_totals = summarize_run_budget_totals(activity)

    events_saved_entry = _existing_run_entry(entries, action="events_saved")
    if events_saved_entry is not None:
        new_events = int((events_saved_entry.get("detail") or {}).get("saved", 0))
    else:
        new_events = sum(phase["new_events"] for phase in activity.values())

    run_init_entry = _existing_run_entry(entries, action="run_init")
    cached_events = int((run_init_entry.get("detail") or {}).get("cached_count", 0)) if run_init_entry else 0
    uncovered_tier1 = _derive_uncovered_tier1(config, run_init_entry, run_id)

    return {
        "events_sent": events_sent,
        "new_events": new_events,
        "cached_events": cached_events,
        "searches_used": budget_totals["searches_used"],
        "max_searches": int(config.get("max_searches", 15)),
        "fetches_used": budget_totals["fetches_used"],
        "max_fetches": int(config.get("max_fetches", 15)),
        "validation_fetches_used": budget_totals["validation_fetches_used"],
        "validation_fetch_limit": VALIDATION_FETCH_LIMIT,
        "uncovered_tier1": uncovered_tier1,
    }


def build_run_complete_detail(
    config: dict[str, Any],
    *,
    run_id: str,
    events_sent: int,
    sent: bool,
    send_reason: str,
    served_marked: bool,
) -> dict[str, Any]:
    """Compute the canonical run_complete detail payload for one run."""
    detail = build_delivery_detail(
        config,
        run_id=run_id,
        events_sent=events_sent,
    )
    detail.update({
        "sent": sent,
        "send_reason": send_reason,
        "served_marked": served_marked,
    })
    return detail


def log_run_complete(
    config: dict[str, Any],
    *,
    run_id: str,
    target_weekend: str,
    events_sent: int,
    sent: bool,
    send_reason: str,
    served_marked: bool,
) -> tuple[dict[str, Any], bool]:
    """Log one canonical run_complete entry, unless it already exists."""
    entries = read_action_log(config, run_id=run_id)
    existing = _existing_run_entry(entries, action="run_complete")
    if existing is not None:
        return dict(existing.get("detail") or {}), False

    detail = build_run_complete_detail(
        config,
        run_id=run_id,
        events_sent=events_sent,
        sent=sent,
        send_reason=send_reason,
        served_marked=served_marked,
    )
    log_action(
        config,
        "run_complete",
        detail=detail,
        run_id=run_id,
        source="skill",
        target_weekend=target_weekend,
    )
    return detail, True


def _derive_uncovered_tier1(
    config: dict[str, Any],
    run_init_entry: dict[str, Any] | None,
    run_id: str,
) -> list[str]:
    """Derive uncovered tier1 cities from run_init data and saved weekend cache."""
    if run_init_entry is None:
        return []

    detail = run_init_entry.get("detail") or {}
    tier1_entries = detail.get("tier1", [])
    if not isinstance(tier1_entries, list):
        return []

    target_weekend = run_init_entry.get("target_weekend")
    if not isinstance(target_weekend, str) or not target_weekend:
        target_weekend = _extract_target_weekend_from_run_id(run_id)
    if target_weekend is None:
        return []

    cached_summary = query_events_summary(
        config,
        target_weekend,
        exclude_served_override=False,
    )
    covered = set(cached_summary.get("covered_cities", []))
    ordered_tier1 = [
        entry.rsplit("|", 1)[0]
        for entry in tier1_entries
        if isinstance(entry, str)
    ]
    return [city for city in ordered_tier1 if city not in covered]


def _extract_target_weekend_from_run_id(run_id: str) -> str | None:
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})_\d{4}", run_id)
    if not match:
        return None
    return match.group(1)


def audit_run(
    config: dict[str, Any],
    run_id: str,
    *,
    stage: str = "post_send",
) -> dict[str, Any]:
    """Validate one scout run from action_log.jsonl entries.

    The audit is intentionally strict about workflow sequencing and accounting,
    so skills can use it as a deterministic final guard before reporting success.
    """
    if stage not in AUDIT_STAGES:
        raise ValueError(f"Unknown audit stage: {stage!r}")
    try:
        entries = read_action_log(config, run_id=run_id)
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "run_id": run_id,
            "stage": stage,
            "errors": [f"action_log.jsonl contains invalid JSON: {exc.msg}"],
            "warnings": [],
            "summary": {},
        }

    errors: list[str] = []
    warnings: list[str] = []

    if not entries:
        return {
            "ok": False,
            "run_id": run_id,
            "stage": stage,
            "errors": [f"No action-log entries found for run_id {run_id!r}"],
            "warnings": [],
            "summary": {},
        }

    phase_state = {phase: "not_seen" for phase in PHASES}
    phase_started_at: dict[str, int] = {}
    phase_completed_at: dict[str, int] = {}
    phase_completed_by: dict[str, str] = {}
    phase_summary_detail: dict[str, dict[str, Any]] = {}
    phase_activity = {
        phase: {"searches": 0, "fetches": 0, "new_events": 0}
        for phase in PHASES
    }
    phase_skip_reasons: dict[str, str | None] = {}
    implicit_phase_starts: set[str] = set()
    prestart_activity_phases: set[str] = set()

    search_bypass_reason: str | None = None
    search_bypass_index: int | None = None
    d_complete_index: int | None = None
    total_searches = 0
    total_discovery_fetches = 0
    total_validation_fetches = 0
    total_new_events = 0

    run_init_entry: dict[str, Any] | None = None
    events_saved_entry: dict[str, Any] | None = None
    score_summary_entry: dict[str, Any] | None = None
    message_formatted_entry: dict[str, Any] | None = None
    telegram_send_entry: dict[str, Any] | None = None
    events_served_entry: dict[str, Any] | None = None
    run_complete_entry: dict[str, Any] | None = None
    command_failed_entries: list[tuple[int, dict[str, Any]]] = []

    current_phase_idx = 0

    for entry_index, entry in enumerate(entries):
        action = entry.get("action")
        phase = entry.get("phase")
        detail = entry.get("detail") or {}

        if action == "run_init" and run_init_entry is None:
            run_init_entry = entry
        elif action == "events_saved":
            events_saved_entry = entry
        elif action == "score_summary":
            score_summary_entry = entry
        elif action == "message_formatted":
            message_formatted_entry = entry
        elif action == "telegram_send":
            # Delivery retries are allowed; the last telegram_send entry is authoritative.
            telegram_send_entry = entry
        elif action == "events_served":
            events_served_entry = entry
        elif action == "run_complete":
            run_complete_entry = entry
        elif action == "command_failed":
            command_failed_entries.append((entry_index, entry))

        if action == "skip" and phase == "search" and search_bypass_index is None:
            search_bypass_index = entry_index
            search_bypass_reason = str(detail.get("reason") or "")

        if action in {"search", "fetch"} and phase in DISCOVERY_PHASE_MAP:
            phase_name = DISCOVERY_PHASE_MAP[phase]
            if d_complete_index is not None and entry_index > d_complete_index:
                errors.append(f"Discovery action {action!r} occurred after Phase D completed")
            if search_bypass_index is not None:
                warnings.append("Search bypass skip was logged, but discovery actions still ran")
            if phase_state[phase_name] == "not_seen" and phase_name not in prestart_activity_phases:
                errors.append(f"Phase {phase_name} has activity before phase_start")
                prestart_activity_phases.add(phase_name)
            if action == "search":
                phase_activity[phase_name]["searches"] += 1
                total_searches += 1
            else:
                phase_activity[phase_name]["fetches"] += 1
                if phase_name == "D":
                    total_validation_fetches += 1
                else:
                    total_discovery_fetches += 1
            events_discovered = detail.get("events_discovered", 0)
            if isinstance(events_discovered, int):
                phase_activity[phase_name]["new_events"] += events_discovered
                total_new_events += events_discovered
            else:
                errors.append(
                    f"{action} entry for phase {phase!r} has non-integer events_discovered"
                )

        if phase not in PHASE_RANK:
            continue

        phase_idx = PHASE_RANK[phase]
        if phase_idx > current_phase_idx:
            errors.append(f"Phase {phase} appeared before earlier phases were completed")
            current_phase_idx = phase_idx
        if phase_idx < current_phase_idx:
            errors.append(f"Phase {phase} was revisited after completion")

        if action == "phase_start":
            if phase_state[phase] != "not_seen":
                errors.append(f"Phase {phase} has multiple phase_start entries")
                continue
            phase_state[phase] = "started"
            phase_started_at[phase] = entry_index
            if detail.get("implicit") is True and phase not in implicit_phase_starts:
                trigger = str(detail.get("trigger") or "unknown")
                warnings.append(
                    f"Phase {phase} phase_start was inserted implicitly by python (trigger: {trigger})"
                )
                implicit_phase_starts.add(phase)
        elif action == "phase_summary":
            if phase_state[phase] != "started":
                errors.append(f"Phase {phase} has phase_summary without a matching phase_start")
            if phase in phase_completed_at:
                errors.append(f"Phase {phase} has multiple completion entries")
                continue
            phase_state[phase] = "completed"
            phase_completed_at[phase] = entry_index
            phase_completed_by[phase] = "phase_summary"
            phase_summary_detail[phase] = detail
            current_phase_idx = min(phase_idx + 1, len(PHASES) - 1)
            if phase == "D":
                d_complete_index = entry_index
        elif action == "skip":
            if phase_state[phase] != "started":
                errors.append(f"Phase {phase} has skip without a matching phase_start")
            if phase in phase_completed_at:
                errors.append(f"Phase {phase} has multiple completion entries")
                continue
            phase_state[phase] = "completed"
            phase_completed_at[phase] = entry_index
            phase_completed_by[phase] = "skip"
            phase_skip_reasons[phase] = str(detail.get("reason") or "")
            current_phase_idx = min(phase_idx + 1, len(PHASES) - 1)
            if phase == "D":
                d_complete_index = entry_index
        elif action == "phase_c_batch_requested" and phase == "C":
            if phase_state["C"] == "not_seen" and "C" not in prestart_activity_phases:
                errors.append("Phase C has activity before phase_start")
                prestart_activity_phases.add("C")

    phase_entries_seen = any(
        entry.get("phase") in PHASE_RANK and entry.get("action") in {"phase_start", "phase_summary", "skip"}
        for entry in entries
    )
    if run_init_entry is None:
        errors.append("Missing run_init entry")

    if not phase_entries_seen and search_bypass_index is None:
        errors.append("No phase lifecycle entries were logged")

    if search_bypass_index is None:
        for phase in PHASES:
            if phase not in phase_completed_at:
                errors.append(f"Missing completion entry for Phase {phase}")
            if phase in phase_started_at and phase not in phase_completed_at:
                errors.append(f"Phase {phase} started but never completed")
    else:
        for phase in PHASES:
            if phase in phase_started_at or phase in phase_completed_at:
                warnings.append(
                    f"Search bypass was logged ({search_bypass_reason or 'no reason'}), "
                    f"but phase {phase} still has lifecycle entries"
                )

    cumulative_searches = 0
    cumulative_fetches = 0
    for phase in PHASES:
        cumulative_searches += phase_activity[phase]["searches"]
        cumulative_fetches += phase_activity[phase]["fetches"]
        detail = phase_summary_detail.get(phase)
        if detail is None:
            continue
        expected = phase_activity[phase]
        if detail.get("searches_used_in_phase") != expected["searches"]:
            errors.append(
                f"Phase {phase} summary searches_used_in_phase does not match actual searches"
            )
        if detail.get("fetches_used_in_phase") != expected["fetches"]:
            errors.append(
                f"Phase {phase} summary fetches_used_in_phase does not match actual fetches"
            )
        if detail.get("new_events_in_phase") != expected["new_events"]:
            errors.append(
                f"Phase {phase} summary new_events_in_phase does not match discovered events"
            )
        if detail.get("cumulative_searches_used") != cumulative_searches:
            errors.append(
                f"Phase {phase} summary cumulative_searches_used does not match actual searches"
            )
        if detail.get("cumulative_fetches_used") != cumulative_fetches:
            errors.append(
                f"Phase {phase} summary cumulative_fetches_used does not match actual fetches"
            )

    if stage == "post_send" and run_complete_entry is None:
        errors.append("Missing run_complete entry")
    elif run_complete_entry is not None:
        detail = run_complete_entry.get("detail") or {}
        if stage == "post_send":
            missing_fields = [
                field for field in RUN_COMPLETE_REQUIRED_FIELDS if field not in detail
            ]
            if missing_fields:
                errors.append(
                    "run_complete detail is missing required fields: "
                    + ", ".join(missing_fields)
                )
            if detail.get("searches_used") != total_searches:
                errors.append("run_complete searches_used does not match logged search actions")
            if detail.get("fetches_used") != total_discovery_fetches:
                errors.append("run_complete fetches_used does not match logged discovery fetch actions")
            if detail.get("validation_fetches_used") != total_validation_fetches:
                errors.append("run_complete validation_fetches_used does not match logged validation fetch actions")

            max_searches = detail.get("max_searches")
            max_fetches = detail.get("max_fetches")
            validation_fetch_limit = detail.get("validation_fetch_limit")
            if isinstance(max_searches, int) and max_searches < total_searches:
                errors.append("run_complete max_searches is below actual searches_used")
            if isinstance(max_fetches, int) and max_fetches < total_discovery_fetches:
                errors.append("run_complete max_fetches is below actual discovery fetches_used")
            if validation_fetch_limit != VALIDATION_FETCH_LIMIT:
                errors.append(
                    f"run_complete validation_fetch_limit must equal {VALIDATION_FETCH_LIMIT}"
                )
            elif total_validation_fetches > VALIDATION_FETCH_LIMIT:
                errors.append("run_complete validation_fetch_limit is below actual validation_fetches_used")

            sent = detail.get("sent")
            send_reason = detail.get("send_reason")
            served_marked = detail.get("served_marked")
            if sent is True and send_reason != "sent":
                errors.append("run_complete send_reason must be 'sent' when sent=true")
            if sent is False and send_reason not in {"telegram_not_configured", "telegram_internal", "send_failed"}:
                errors.append("run_complete send_reason is invalid for sent=false")
            if sent is True and served_marked is not True:
                errors.append("run_complete served_marked must be true when sent=true")
            if sent is False and send_reason == "telegram_internal" and served_marked is not True:
                errors.append("run_complete served_marked must be true when send_reason=telegram_internal")
            if sent is False and send_reason != "telegram_internal" and served_marked is not False:
                errors.append("run_complete served_marked must be false when sent=false")

            uncovered_tier1 = detail.get("uncovered_tier1")
            if not isinstance(uncovered_tier1, list):
                errors.append("run_complete uncovered_tier1 must be a JSON array")
            elif run_init_entry is not None:
                init_tier1 = (run_init_entry.get("detail") or {}).get("tier1", [])
                allowed_tier1 = {
                    city_entry.rsplit("|", 1)[0]
                    for city_entry in init_tier1
                    if isinstance(city_entry, str)
                }
                if allowed_tier1 and any(city not in allowed_tier1 for city in uncovered_tier1):
                    errors.append("run_complete uncovered_tier1 contains unknown tier1 city labels")

    if stage == "post_send" and events_saved_entry is not None and run_complete_entry is not None:
        saved_count = (events_saved_entry.get("detail") or {}).get("saved")
        run_complete_new_events = (run_complete_entry.get("detail") or {}).get("new_events")
        if isinstance(saved_count, int) and run_complete_new_events != saved_count:
            errors.append("run_complete new_events does not match events_saved.saved")

    if stage == "post_send" and run_init_entry is not None and run_complete_entry is not None:
        init_cached_count = (run_init_entry.get("detail") or {}).get("cached_count")
        run_complete_cached = (run_complete_entry.get("detail") or {}).get("cached_events")
        if isinstance(init_cached_count, int) and run_complete_cached != init_cached_count:
            errors.append("run_complete cached_events does not match run_init cached_count")

    if stage == "post_send" and message_formatted_entry is not None and run_complete_entry is not None:
        formatted_detail = message_formatted_entry.get("detail") or {}
        expected_events_sent = formatted_detail.get("city_events", 0) + formatted_detail.get("trips", 0)
        if (run_complete_entry.get("detail") or {}).get("events_sent") != expected_events_sent:
            errors.append("run_complete events_sent does not match message_formatted totals")

    if stage == "post_send" and telegram_send_entry is not None and run_complete_entry is not None:
        run_complete_detail = run_complete_entry.get("detail") or {}
        telegram_send_detail = telegram_send_entry.get("detail") or {}
        sent = run_complete_detail.get("sent")
        logged_send = telegram_send_detail.get("success")
        if sent != logged_send:
            errors.append("run_complete sent does not match telegram_send.success")
        logged_reason = telegram_send_detail.get("reason")
        run_complete_reason = run_complete_detail.get("send_reason")
        if run_complete_reason == "telegram_internal":
            if logged_reason != "telegram_not_configured":
                errors.append(
                    "run_complete send_reason=telegram_internal requires telegram_send.reason=telegram_not_configured"
                )
        elif logged_reason is not None and run_complete_reason != logged_reason:
            errors.append("run_complete send_reason does not match telegram_send.reason")

    if command_failed_entries:
        warnings.append("Run contains command_failed entries; review python_failures.jsonl for details")
        if stage == "post_send" and run_complete_entry is not None:
            run_complete_index = next(
                index for index, entry in enumerate(entries)
                if entry is run_complete_entry
            )
            if any(index < run_complete_index for index, _entry in command_failed_entries):
                warnings.append("command_failed entries were logged before run_complete")

    remediation: dict[str, str] | None = None
    if stage == "post_send" and run_complete_entry is not None:
        run_complete_detail = run_complete_entry.get("detail") or {}
        sent = run_complete_detail.get("sent")
        send_reason = run_complete_detail.get("send_reason")
        target_weekend_for_fix = run_complete_entry.get("target_weekend") or ""
        if sent is True and events_served_entry is None:
            errors.append("sent=true but no events_served entry was logged")
            remediation = {
                "missing_step": "cache-mark-served",
                "command": (
                    f'python -m weekend_scout cache-mark-served'
                    f' --date "{target_weekend_for_fix}" --run-id "{run_id}"'
                ),
                "hint": "Run cache-mark-served, then rerun this audit.",
            }
        if send_reason == "telegram_internal" and events_served_entry is None:
            errors.append("run_complete send_reason=telegram_internal requires an events_served entry")
        if (
            sent is False
            and send_reason != "telegram_internal"
            and events_served_entry is not None
        ):
            errors.append("events_served was logged even though final delivery was not served")

    if score_summary_entry is None:
        if stage == "pre_send":
            errors.append("Missing score_summary entry")
        else:
            warnings.append("Missing score_summary entry")
    else:
        score_detail = score_summary_entry.get("detail") or {}
        for field in ("total_pool", "city_events_selected", "trip_options"):
            if not isinstance(score_detail.get(field), int):
                errors.append(f"score_summary {field} must be an integer")
    if stage == "post_send" and message_formatted_entry is None:
        warnings.append("Missing message_formatted entry")
    if stage == "post_send" and telegram_send_entry is None:
        warnings.append("Missing telegram_send entry")

    completed_phases = [
        phase for phase in PHASES if phase in phase_completed_at
    ]
    skipped_phases = [
        phase for phase in PHASES if phase_completed_by.get(phase) == "skip"
    ]

    result: dict[str, object] = {
        "ok": not errors,
        "run_id": run_id,
        "stage": stage,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "entry_count": len(entries),
            "searches_used": total_searches,
            "fetches_used": total_discovery_fetches,
            "validation_fetches_used": total_validation_fetches,
            "new_events_logged": total_new_events,
            "completed_phases": completed_phases,
            "skipped_phases": skipped_phases,
            "search_bypass_reason": search_bypass_reason,
        },
    }
    if remediation is not None:
        result["remediation"] = remediation
    return result


def get_searches_this_week(
    config: dict[str, Any], saturday: str
) -> list[str]:
    """Return query strings already logged for the target weekend this week.

    Args:
        config: Loaded configuration dictionary.
        saturday: ISO date string of target Saturday.

    Returns:
        List of query strings.
    """
    with get_connection(config) as conn:
        rows = conn.execute(
            "SELECT query FROM search_log WHERE target_weekend = ?",
            (saturday,),
        ).fetchall()
    return [row["query"] for row in rows]


def mark_served(config: dict[str, Any], saturday: str) -> int:
    """Mark all events for the target weekend as served (sent to Telegram).

    Args:
        config: Loaded configuration dictionary.
        saturday: ISO date string of target Saturday.

    Returns:
        Number of rows updated.
    """
    sunday = _weekend_sunday(saturday)

    with get_connection(config) as conn:
        cursor = conn.execute(
            """
            UPDATE events SET served = 1
            WHERE start_date <= ?
              AND (end_date IS NULL OR end_date >= ?)
              AND served = 0
            """,
            (sunday, saturday),
        )
    return cursor.rowcount


def cleanup_old_events(config: dict[str, Any], days: int = 30) -> int:
    """Delete events older than `days` days from the cache.

    Args:
        config: Loaded configuration dictionary.
        days: Age threshold in days (default 30).

    Returns:
        Number of rows deleted.
    """
    cutoff = (
        datetime.date.today() - datetime.timedelta(days=days)
    ).isoformat()

    with get_connection(config) as conn:
        cursor = conn.execute(
            "DELETE FROM events WHERE start_date < ?",
            (cutoff,),
        )
    return cursor.rowcount
