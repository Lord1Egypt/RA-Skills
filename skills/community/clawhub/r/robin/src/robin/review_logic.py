from __future__ import annotations

from datetime import datetime, timedelta, timezone

from robin.models import Entry


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_timestamp(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def pick_best_candidate(index: dict, entries: list[Entry], config: dict) -> tuple[dict, Entry] | None:
    entries_by_id = {entry.entry_id: entry for entry in entries}
    cooldown_days = config.get("review_cooldown_days", 60)
    cutoff = datetime.now(timezone.utc) - timedelta(days=cooldown_days)

    candidates: list[tuple[tuple[int, int, int, str], dict, Entry]] = []
    for entry_id, item in index.get("items", {}).items():
        entry = entries_by_id.get(entry_id)
        if entry is None:
            continue

        last_surfaced = item.get("last_surfaced")
        if last_surfaced and parse_timestamp(last_surfaced) > cutoff:
            continue

        rating = item.get("rating")
        times_surfaced = item.get("times_surfaced", 0)
        score = (
            0 if rating is None else 1,
            rating if rating is not None else 0,
            times_surfaced,
            entry.entry_id,
        )
        candidates.append((score, item, entry))

    if not candidates:
        return None

    _, item, entry = min(candidates, key=lambda candidate: candidate[0])
    return item, entry


def mark_surfaced(index: dict, entry_id: str, *, awaiting_rating: bool = False) -> dict:
    if entry_id not in index.get("items", {}):
        raise KeyError(entry_id)

    item = index["items"][entry_id]
    item["last_surfaced"] = now_iso()
    item["times_surfaced"] = item.get("times_surfaced", 0) + 1
    item["_awaiting_rating"] = awaiting_rating
    return item


def rate_item(index: dict, entry_id: str, rating: int) -> dict:
    if entry_id not in index.get("items", {}):
        raise KeyError(entry_id)
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5.")

    item = index["items"][entry_id]
    item["rating"] = rating
    if not item.get("_awaiting_rating"):
        item["last_surfaced"] = now_iso()
        item["times_surfaced"] = item.get("times_surfaced", 0) + 1
    item["_awaiting_rating"] = False
    return item
