from __future__ import annotations

from .common import *
from .usage_loader import max_optional, max_optional_float, merge_dates

def empty_community_record() -> dict[str, object]:
    return {
        "rating": None,
        "stars": None,
        "downloads": None,
        "installs_current": None,
        "installs_all_time": None,
        "trending_7d": None,
        "comments_count": None,
        "last_updated": None,
    }


def normalize_rating(value) -> float | None:
    rating = coerce_float(value)
    if rating is None:
        return None
    if 0.0 <= rating <= 1.0:
        rating = rating * 5.0
    return rating


def community_record_from_mapping(mapping: dict, hint_name: str | None = None) -> tuple[str, dict[str, object]] | None:
    identity = extract_record_identity(mapping, hint_name=hint_name)
    lookup_key = record_lookup_key(identity)
    if not lookup_key:
        return None

    lowered = lowered_mapping(mapping)
    record = {
        "rating": normalize_rating(first_present(mapping, COMMUNITY_RATING_KEYS, lowered)),
        "stars": coerce_int(first_present(mapping, COMMUNITY_STARS_KEYS, lowered)),
        "downloads": coerce_int(first_present(mapping, COMMUNITY_DOWNLOADS_KEYS, lowered)),
        "installs_current": coerce_int(first_present(mapping, COMMUNITY_INSTALLS_CURRENT_KEYS, lowered)),
        "installs_all_time": coerce_int(first_present(mapping, COMMUNITY_INSTALLS_ALL_TIME_KEYS, lowered)),
        "trending_7d": coerce_int(first_present(mapping, COMMUNITY_TRENDING_KEYS, lowered)),
        "comments_count": coerce_int(first_present(mapping, COMMUNITY_COMMENTS_KEYS, lowered)),
        "last_updated": normalize_dateish(first_present(mapping, COMMUNITY_UPDATED_KEYS, lowered)),
    }
    if not any(value is not None for value in record.values()):
        return None
    return lookup_key, record


def merge_community_record(store: dict[str, dict[str, object]], name: str, incoming: dict[str, object]) -> None:
    target = store.setdefault(name, empty_community_record())
    for key in ("stars", "downloads", "installs_current", "installs_all_time", "trending_7d", "comments_count"):
        target[key] = max_optional(coerce_int(target.get(key)), coerce_int(incoming.get(key)))
    target["rating"] = max_optional_float(
        normalize_rating(target.get("rating")),
        normalize_rating(incoming.get("rating")),
    )
    target["last_updated"] = merge_dates(
        target.get("last_updated"),  # type: ignore[arg-type]
        incoming.get("last_updated"),  # type: ignore[arg-type]
        "max",
    )


def consume_community_node(node, community: dict[str, dict[str, object]], hint_name: str | None = None) -> None:
    if isinstance(node, list):
        for item in node:
            consume_community_node(item, community, hint_name=hint_name)
        return

    if isinstance(node, dict):
        record = community_record_from_mapping(node, hint_name=hint_name)
        if record:
            name, payload = record
            merge_community_record(community, name, payload)
            return

        for key, value in node.items():
            key_text = str(key)
            key_norm = normalize_name(key_text)
            child_hint = None
            if key_text not in COLLECTION_KEYS and key_norm not in COLLECTION_KEYS and isinstance(value, dict):
                child_hint = key_text
            consume_community_node(value, community, hint_name=child_hint)


def load_community_csv(path: Path) -> dict[str, dict[str, object]]:
    community: dict[str, dict[str, object]] = {}
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        for row in reader:
            record = community_record_from_mapping(row)
            if record is None:
                continue
            name, payload = record
            merge_community_record(community, name, payload)
    return community


def load_community_json(path: Path) -> dict[str, dict[str, object]]:
    community: dict[str, dict[str, object]] = {}
    payload = load_json_or_jsonl(path)
    consume_community_node(payload, community)
    return community


def load_community(paths: list[Path]) -> dict[str, dict[str, object]]:
    community: dict[str, dict[str, object]] = {}
    for path in paths:
        if not path.exists():
            continue
        if path.suffix.lower() in {".csv", ".tsv"}:
            parsed = load_community_csv(path)
        else:
            parsed = load_community_json(path)
        for key, value in parsed.items():
            merge_community_record(community, key, value)
    return community


def community_prior_score(entry: dict[str, object] | None) -> tuple[float | None, float | None, dict[str, float]]:
    if not entry:
        return None, None, {}

    score = 0.0
    confidence = 0.0
    breakdown: dict[str, float] = {}
    rating = coerce_float(entry.get("rating"))
    if rating is not None:
        component = clamp(rating / 5.0, 0.0, 1.0) * 0.30
        score += component
        confidence += 0.15
        breakdown["rating"] = round(component, 3)

    volume = coerce_int(entry.get("installs_current"))
    if volume is None:
        volume = coerce_int(entry.get("downloads"))
    if volume is not None:
        component = clamp(math.log1p(volume) / math.log1p(5000), 0.0, 1.0) * 0.20
        score += component
        confidence += 0.15
        breakdown["current_installs_or_downloads"] = round(component, 3)

    installs_all_time = coerce_int(entry.get("installs_all_time"))
    if installs_all_time is not None:
        component = clamp(math.log1p(installs_all_time) / math.log1p(20000), 0.0, 1.0) * 0.10
        score += component
        confidence += 0.10
        breakdown["installs_all_time"] = round(component, 3)

    trending = coerce_int(entry.get("trending_7d"))
    if trending is not None:
        component = clamp(math.log1p(trending) / math.log1p(250), 0.0, 1.0) * 0.15
        score += component
        confidence += 0.15
        breakdown["trending_7d"] = round(component, 3)

    stars = coerce_int(entry.get("stars"))
    if stars is not None:
        component = clamp(math.log1p(stars) / math.log1p(250), 0.0, 1.0) * 0.10
        score += component
        confidence += 0.10
        breakdown["stars"] = round(component, 3)

    comments_count = coerce_int(entry.get("comments_count"))
    if comments_count is not None:
        component = clamp(math.log1p(comments_count) / math.log1p(100), 0.0, 1.0) * 0.05
        score += component
        confidence += 0.10
        breakdown["comments_count"] = round(component, 3)

    last_updated_days = days_since(entry.get("last_updated"))
    if last_updated_days is not None:
        if last_updated_days <= 180:
            maintenance = 1.0
        elif last_updated_days <= 365:
            maintenance = 0.7
        elif last_updated_days <= 730:
            maintenance = 0.4
        else:
            maintenance = 0.1
        component = maintenance * 0.10
        score += component
        confidence += 0.15
        breakdown["maintenance"] = round(component, 3)

    return round(clamp(score, 0.0, 1.0), 2), round(clamp(confidence, 0.0, 1.0), 2), breakdown
