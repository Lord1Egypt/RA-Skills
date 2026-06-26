"""Run-scoped candidate persistence and canonicalization for scout sessions."""

from __future__ import annotations

import datetime
import json
import re
from pathlib import Path
from typing import Any, Callable


SESSION_FILE_SUFFIX = ".candidates.json"
SESSION_RETENTION_DAYS = 14
CONFIDENCE_RANK = {
    "unverified": 0,
    "possible": 0,
    "likely": 1,
    "confirmed": 2,
}
STRONG_OVERRIDE_FIELDS: tuple[str, ...] = (
    "event_name",
    "start_date",
    "end_date",
    "time_info",
    "location_name",
    "lat",
    "lon",
    "source_url",
    "source_name",
    "description",
    "category",
    "free_entry",
    "country",
)
NAME_STOPWORDS: frozenset[str] = frozenset(
    {
        "the",
        "and",
        "for",
        "der",
        "die",
        "das",
        "dem",
        "den",
        "des",
        "und",
        "mit",
        "von",
        "vom",
        "auf",
        "am",
        "im",
        "in",
        "an",
        "bei",
        "zum",
        "zur",
        "de",
        "del",
        "la",
        "le",
        "les",
        "los",
        "las",
        "da",
        "di",
        "do",
        "dos",
        "das",
        "na",
    }
)


def _cache_dir(config: dict[str, Any]) -> Path:
    """Return the active cache directory, respecting test overrides."""
    if "_cache_dir" in config:
        return Path(config["_cache_dir"])
    from weekend_scout.config import get_cache_dir

    return get_cache_dir(config)


def get_runs_dir(config: dict[str, Any]) -> Path:
    """Return the directory that stores run-scoped candidate session files."""
    return _cache_dir(config) / "runs"


def get_session_path(config: dict[str, Any], run_id: str) -> Path:
    """Return the path to one run's candidate session file."""
    return get_runs_dir(config) / f"{run_id}{SESSION_FILE_SUFFIX}"


def cleanup_stale_sessions(
    config: dict[str, Any], *, days: int = SESSION_RETENTION_DAYS
) -> list[str]:
    """Delete stale candidate session files and return removed filenames."""
    runs_dir = get_runs_dir(config)
    try:
        items = list(runs_dir.iterdir())
    except OSError:
        return []

    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    removed: list[str] = []
    for path in items:
        if not path.is_file() or not path.name.endswith(SESSION_FILE_SUFFIX):
            continue
        try:
            modified = datetime.datetime.fromtimestamp(path.stat().st_mtime)
        except OSError:
            continue
        if modified >= cutoff:
            continue
        try:
            path.unlink(missing_ok=True)
            removed.append(path.name)
        except OSError:
            continue
    return removed


def _default_state(run_id: str, target_weekend: str) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "target_weekend": target_weekend,
        "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "candidates": [],
    }


def _write_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def load_session_state(
    config: dict[str, Any],
    run_id: str,
    *,
    target_weekend: str | None = None,
    create: bool = False,
) -> dict[str, Any] | None:
    """Load one run's session state, optionally creating an empty file."""
    path = get_session_path(config, run_id)
    if not path.exists():
        if not create:
            return None
        if target_weekend is None:
            raise ValueError("target_weekend is required when creating a session file")
        state = _default_state(run_id, target_weekend)
        _write_state(path, state)
        return state

    state = json.loads(path.read_text(encoding="utf-8"))
    if "candidates" not in state or not isinstance(state["candidates"], list):
        state["candidates"] = []
    if not state.get("run_id"):
        state["run_id"] = run_id
    if target_weekend and not state.get("target_weekend"):
        state["target_weekend"] = target_weekend
        _write_state(path, state)
    return state


def export_session_candidates(config: dict[str, Any], run_id: str) -> list[dict[str, Any]]:
    """Return all canonical candidates currently stored for one run."""
    finalized = finalize_session_candidates(config, run_id)
    return _sorted_candidates(finalized["candidates"])


def query_session_candidates(config: dict[str, Any], run_id: str) -> list[dict[str, Any]]:
    """Return candidates for one run that overlap the run's target weekend."""
    finalized = finalize_session_candidates(config, run_id)
    candidates = finalized["candidates"]
    if not candidates:
        state = load_session_state(config, run_id)
        if state is None:
            return []
        saturday = state.get("target_weekend")
    else:
        state = load_session_state(config, run_id)
        saturday = state.get("target_weekend") if state is not None else None
    if not isinstance(saturday, str) or not saturday:
        return []
    return _sorted_candidates(
        [
            candidate for candidate in candidates if _overlaps_weekend(candidate, saturday)
        ]
    )


def get_session_covered_cities(config: dict[str, Any], run_id: str) -> list[str]:
    """Return covered city names from one run's session candidates for the target weekend."""
    return sorted(
        {
            str(candidate.get("city"))
            for candidate in query_session_candidates(config, run_id)
            if candidate.get("city")
        }
    )


def get_session_candidate_count(config: dict[str, Any], run_id: str) -> int:
    """Return the total canonical candidate count for one run."""
    return len(export_session_candidates(config, run_id))


def upsert_session_candidates(
    config: dict[str, Any],
    run_id: str,
    target_weekend: str,
    candidates: list[dict[str, Any]],
) -> dict[str, int]:
    """Upsert candidates into the run-scoped session file."""
    state = load_session_state(config, run_id, target_weekend=target_weekend, create=True)
    if state is None:
        raise RuntimeError("Failed to create session state")

    before = canonicalize_candidates(config, target_weekend, state.get("candidates", []))
    after = canonicalize_candidates(
        config,
        target_weekend,
        before["candidates"] + [dict(candidate) for candidate in candidates],
    )
    state["candidates"] = after["candidates"]
    _write_state(get_session_path(config, run_id), state)

    added = max(0, len(after["candidates"]) - len(before["candidates"]))
    merged = max(0, len(candidates) - added)
    updated = merged if after["candidates"] != before["candidates"] else 0
    return {
        "added": added,
        "updated": updated,
        "duplicates_merged": merged,
        "events_discovered": added,
        "candidate_count": len(after["candidates"]),
    }


def finalize_session_candidates(config: dict[str, Any], run_id: str) -> dict[str, Any]:
    """Canonicalize one run session in place and return the final candidate list."""
    state = load_session_state(config, run_id)
    if state is None:
        return {
            "candidates": [],
            "candidate_count": 0,
            "duplicates_merged": 0,
        }

    target_weekend = str(state.get("target_weekend") or "")
    canonical = canonicalize_candidates(config, target_weekend, state.get("candidates", []))
    original_candidates = _sorted_candidates(state.get("candidates", []))
    state["candidates"] = canonical["candidates"]
    if canonical["candidates"] != original_candidates:
        _write_state(get_session_path(config, run_id), state)
    return {
        "candidates": canonical["candidates"],
        "candidate_count": len(canonical["candidates"]),
        "duplicates_merged": canonical["duplicates_collapsed"],
    }


def canonicalize_candidates(
    config: dict[str, Any],
    target_weekend: str,
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return canonicalized candidates plus summary statistics."""
    resolve_country = _build_country_resolver(config)
    canonical: list[dict[str, Any]] = []
    duplicates_collapsed = 0
    countries_enriched = 0

    for candidate in candidates:
        normalized = _normalize_candidate(candidate)
        if not normalized:
            continue
        if not _has_value(normalized.get("country")):
            country = resolve_country(str(normalized.get("city", "")))
            if country:
                normalized["country"] = country
                countries_enriched += 1

        match_idx = _find_match_index(canonical, normalized, target_weekend)
        if match_idx is None:
            canonical.append(normalized)
            continue

        merged = merge_candidate_data(canonical[match_idx], normalized)
        canonical[match_idx] = merged
        duplicates_collapsed += 1

    return {
        "candidates": _sorted_candidates(canonical),
        "duplicates_collapsed": duplicates_collapsed,
        "countries_enriched": countries_enriched,
    }


def merge_candidate_data(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    """Merge candidate/event fields, keeping the stronger richer version."""
    merged = dict(existing)
    existing_rank = _confidence_rank(existing.get("confidence"))
    incoming_rank = _confidence_rank(incoming.get("confidence"))

    existing_name = str(existing.get("event_name", ""))
    incoming_name = str(incoming.get("event_name", ""))
    if _has_value(incoming_name):
        if not _has_value(existing_name):
            merged["event_name"] = incoming_name
        elif incoming_rank > existing_rank and _is_more_specific_name(incoming_name, existing_name):
            merged["event_name"] = incoming_name
        elif incoming_rank == existing_rank and _is_more_specific_name(incoming_name, existing_name):
            merged["event_name"] = incoming_name

    for key, value in incoming.items():
        if key in {"city", "event_name"}:
            continue
        if not _has_value(value):
            continue
        if not _has_value(merged.get(key)):
            merged[key] = value
            continue
        if incoming_rank > existing_rank and key in STRONG_OVERRIDE_FIELDS:
            merged[key] = value

    if incoming_rank > existing_rank and _has_value(incoming.get("confidence")):
        merged["confidence"] = incoming["confidence"]
    elif not _has_value(merged.get("confidence")) and _has_value(incoming.get("confidence")):
        merged["confidence"] = incoming["confidence"]

    return merged


def _normalize_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in candidate.items():
        if isinstance(value, str):
            stripped = value.strip()
            if stripped:
                normalized[key] = stripped
        elif value is not None:
            normalized[key] = value
    if not normalized:
        return {}
    _validate_candidate(normalized)
    return normalized


def _validate_candidate(candidate: dict[str, Any]) -> None:
    for key in ("event_name", "city", "start_date"):
        value = candidate.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"candidate missing required field {key!r}")


def _normalize_text(value: str) -> str:
    return re.sub(r"[^\w_]", "", re.sub(r"\s+", "_", value.strip().lower()))


def _meaningful_tokens(value: str) -> set[str]:
    tokens = {
        token
        for token in re.findall(r"\w+", value.lower())
        if len(token) >= 3 and token not in NAME_STOPWORDS
    }
    return tokens


def _name_alias_match(existing_name: str, incoming_name: str) -> bool:
    existing_norm = _normalize_text(existing_name)
    incoming_norm = _normalize_text(incoming_name)
    if existing_norm == incoming_norm:
        return True

    shorter, longer = sorted((existing_norm, incoming_norm), key=len)
    if len(shorter) >= 12 and shorter in longer:
        return True

    existing_tokens = _meaningful_tokens(existing_name)
    incoming_tokens = _meaningful_tokens(incoming_name)
    if min(len(existing_tokens), len(incoming_tokens)) < 2:
        return False
    smaller, larger = sorted((existing_tokens, incoming_tokens), key=len)
    return smaller.issubset(larger)


def _is_more_specific_name(candidate_name: str, current_name: str) -> bool:
    if _normalize_text(candidate_name) == _normalize_text(current_name):
        return False
    candidate_tokens = _meaningful_tokens(candidate_name)
    current_tokens = _meaningful_tokens(current_name)
    if candidate_tokens and current_tokens and current_tokens.issubset(candidate_tokens):
        return True
    return len(candidate_name) > len(current_name) + 4


def _confidence_rank(value: Any) -> int:
    if not isinstance(value, str):
        return 0
    return CONFIDENCE_RANK.get(value.strip().lower(), 0)


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    return True


def _sorted_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        (dict(candidate) for candidate in candidates),
        key=lambda candidate: (
            str(candidate.get("start_date", "")),
            str(candidate.get("city", "")).lower(),
            str(candidate.get("event_name", "")).lower(),
        ),
    )


def _event_end_date(candidate: dict[str, Any]) -> str | None:
    end_date = candidate.get("end_date")
    if isinstance(end_date, str) and end_date:
        return end_date
    start_date = candidate.get("start_date")
    if isinstance(start_date, str) and start_date:
        return start_date
    return None


def _overlaps_weekend(candidate: dict[str, Any], saturday: str) -> bool:
    try:
        sunday = (
            datetime.date.fromisoformat(saturday) + datetime.timedelta(days=1)
        ).isoformat()
    except ValueError:
        return False

    start_date = candidate.get("start_date")
    end_date = _event_end_date(candidate)
    if not isinstance(start_date, str) or not start_date or end_date is None:
        return False
    return start_date <= sunday and end_date >= saturday


def _find_match_index(
    candidates: list[dict[str, Any]],
    incoming: dict[str, Any],
    target_weekend: str,
) -> int | None:
    incoming_name = _normalize_text(incoming["event_name"])
    incoming_city = _normalize_text(incoming["city"])
    incoming_start = incoming["start_date"]

    for idx, candidate in enumerate(candidates):
        if (
            _normalize_text(str(candidate.get("event_name", ""))) == incoming_name
            and _normalize_text(str(candidate.get("city", ""))) == incoming_city
            and candidate.get("start_date") == incoming_start
        ):
            return idx

    if not _overlaps_weekend(incoming, target_weekend):
        return None

    for idx, candidate in enumerate(candidates):
        if _normalize_text(str(candidate.get("city", ""))) != incoming_city:
            continue
        if not _overlaps_weekend(candidate, target_weekend):
            continue
        existing_name = str(candidate.get("event_name", ""))
        if _normalize_text(existing_name) == incoming_name:
            return idx
        if _name_alias_match(existing_name, incoming["event_name"]):
            return idx
    return None


def _build_country_resolver(config: dict[str, Any]) -> Callable[[str], str | None]:
    from weekend_scout.config import COUNTRY_CODE_MAP
    from weekend_scout.cities import find_city_candidates, get_city_list

    resolved: dict[str, str] = {}
    lookup_cache: dict[str, str | None] = {}

    home_city = str(config.get("home_city") or "")
    home_country = str(config.get("home_country") or "")
    if home_city and home_country:
        resolved[_normalize_text(home_city)] = home_country

    coords = config.get("home_coordinates", {})
    coords_valid = isinstance(coords, dict) and not (
        coords.get("lat", 0.0) == 0.0 and coords.get("lon", 0.0) == 0.0
    )

    if coords_valid:
        try:
            cities = get_city_list(config)
        except Exception:
            cities = {"tier1": [], "tier2": [], "tier3": []}
    else:
        cities = {"tier1": [], "tier2": [], "tier3": []}

    for entries in cities.values():
        for entry in entries:
            if "|" not in entry:
                continue
            city_name, country_code = entry.rsplit("|", 1)
            country_name = COUNTRY_CODE_MAP.get(country_code, "")
            if country_name:
                resolved.setdefault(_normalize_text(city_name), country_name)

    geonames_path = _cache_dir(config) / "geonames" / "cities15000.txt"

    def resolve(city_name: str) -> str | None:
        normalized = _normalize_text(city_name)
        if not normalized:
            return None
        if normalized in resolved:
            return resolved[normalized]
        if normalized in lookup_cache:
            return lookup_cache[normalized]

        result: str | None = None
        if geonames_path.exists():
            matches = find_city_candidates(city_name, geonames_path)
            if len(matches) == 1:
                result = str(matches[0].get("country_name") or "") or None

        lookup_cache[normalized] = result
        return result

    return resolve
