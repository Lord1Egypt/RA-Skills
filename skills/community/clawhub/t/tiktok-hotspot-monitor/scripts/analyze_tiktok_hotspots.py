from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNAPSHOT_GLOB = "data/tiktok_hotspots*/snapshots/*.jsonl"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "tiktok_hotspot_analysis"
TEXT_TERM_PATTERN = re.compile(r"(?<![#＠@])\b([a-zA-Z][a-zA-Z0-9_&'-]{2,}(?:\s+[a-zA-Z][a-zA-Z0-9_&'-]{2,}){0,3})")
STOP_TERMS = {
    "and",
    "are",
    "but",
    "for",
    "from",
    "get",
    "got",
    "how",
    "not",
    "the",
    "this",
    "that",
    "with",
    "you",
    "your",
    "tiktok",
    "video",
    "videos",
    "fyp",
    "viral",
    "follow",
    "like",
    "comment",
    "share",
    "show",
    "girl",
    "girls",
    "woman",
    "women",
    "fashion",
}

RECENT_VIDEO_BUCKETS = [
    {"key": "within_1d", "label": "近一天", "min_hours": 0, "max_hours": 24},
    {"key": "within_3d", "label": "近三天", "min_hours": 24, "max_hours": 72},
    {"key": "within_7d", "label": "近七天", "min_hours": 72, "max_hours": 168},
    {"key": "within_14d", "label": "近两周", "min_hours": 168, "max_hours": 336},
]
RECENT_TERM_BUCKETS = [
    *RECENT_VIDEO_BUCKETS,
    {"key": "within_30d", "label": "近一个月", "min_hours": 336, "max_hours": 720},
]
RECENT_TERM_MAX_HOURS = 720
ESTABLISHED_ACTIVE_RATIO = 0.1  # 7d内视频占比 >= 10%才算扩散


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze TikTok hotspot metadata snapshots.")
    parser.add_argument("--snapshot", type=Path, default=None, help="JSONL snapshot to analyze. Defaults to latest non-empty snapshot.")
    parser.add_argument("--previous-snapshot", type=Path, default=None, help="Earlier JSONL snapshot for growth comparison. Defaults to latest non-empty snapshot before --snapshot.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--top", type=int, default=10, help="Number of ranked items per section.")
    parser.add_argument("--download", action="store_true", help="Download videos after analysis.")
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else PROJECT_ROOT / path


def non_empty_snapshots() -> list[Path]:
    return [path for path in PROJECT_ROOT.glob(DEFAULT_SNAPSHOT_GLOB) if path.stat().st_size > 0]


def has_video_records(path: Path) -> bool:
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(item, dict) and item.get("video_id"):
                return True
    return False


def valid_snapshots() -> list[Path]:
    return [path for path in non_empty_snapshots() if has_video_records(path)]


def latest_snapshot() -> Path:
    paths = sorted(valid_snapshots(), key=lambda path: path.stat().st_mtime, reverse=True)
    if paths:
        return paths[0]
    raise ValueError("No non-empty TikTok hotspot snapshot found")


def previous_snapshot_for(snapshot_path: Path) -> Path | None:
    current = snapshot_path.resolve()
    candidates = [path for path in valid_snapshots() if path.resolve() != current and path.stat().st_mtime < snapshot_path.stat().st_mtime]
    if not candidates:
        return None
    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)[0]


def crawl_log_for_snapshot(snapshot_path: Path) -> Path | None:
    output_base = snapshot_path.parent.parent
    log_path = output_base / "logs" / snapshot_path.name
    return log_path if log_path.exists() else None


def load_crawl_metrics(snapshot_path: Path) -> dict[str, Any] | None:
    log_path = crawl_log_for_snapshot(snapshot_path)
    if not log_path:
        return None
    summary = None
    window_counts: dict[str, dict[str, Any]] = {}
    with log_path.open("r", encoding="utf-8") as file:
        for line in file:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(item, dict):
                continue
            if item.get("event") == "crawl_round_summary":
                summary = item
                continue
            window = str(item.get("crawl_window") or "default")
            bucket = window_counts.setdefault(
                window,
                {
                    "label": item.get("crawl_window_label") or window,
                    "planned_run_count": 0,
                    "completed_run_count": 0,
                    "failed_run_count": 0,
                    "requested_limit": 0,
                    "raw_record_count": 0,
                },
            )
            bucket["planned_run_count"] += 1
            bucket["requested_limit"] += int(number(item.get("crawl_window_limit")))
            bucket["raw_record_count"] += int(number(item.get("record_count")))
            bucket["failed_run_count" if item.get("status") == "failed" else "completed_run_count"] += 1
    if summary:
        summary.setdefault("windows", window_counts)
        summary["log_path"] = str(log_path)
        return summary
    if not window_counts:
        return None
    raw_count = sum(item["raw_record_count"] for item in window_counts.values())
    return {
        "log_path": str(log_path),
        "enabled_source_count": None,
        "crawl_window_count": len(window_counts),
        "planned_run_count": sum(item["planned_run_count"] for item in window_counts.values()),
        "completed_run_count": sum(item["completed_run_count"] for item in window_counts.values()),
        "failed_run_count": sum(item["failed_run_count"] for item in window_counts.values()),
        "requested_total_limit": sum(item["requested_limit"] for item in window_counts.values()),
        "raw_record_count": raw_count,
        "windows": window_counts,
        "cost_model_note": "Apify cost depends on Actor pricing, planned runs, returned results, compute duration, memory, proxy usage, retries, add-ons, and account plan; verify exact cost in the Apify usage dashboard.",
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                item = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            if isinstance(item, dict) and item.get("video_id"):
                rows.append(item)
    if not rows:
        raise ValueError(f"Snapshot has no video records: {path}")
    return rows


def number(value: Any) -> float:
    if isinstance(value, bool) or value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.replace(",", ""))
        except ValueError:
            return 0.0
    return 0.0


def parse_datetime(value: Any) -> datetime | None:
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    for fmt in ["%Y%m%dT%H%M%SZ", "%Y%m%dT%H%M%S%z"]:
        try:
            parsed = datetime.strptime(text, fmt)
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def snapshot_time(records: list[dict[str, Any]], path: Path) -> datetime:
    times = [parsed for record in records if (parsed := parse_datetime(record.get("crawl_timestamp")))]
    if times:
        return max(times)
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def hours_between(start: datetime | None, end: datetime | None) -> float | None:
    if not start or not end:
        return None
    return max((end - start).total_seconds() / 3600, 0.0)


def hot_score(record: dict[str, Any]) -> float:
    views = number(record.get("view_count"))
    likes = number(record.get("like_count"))
    comments = number(record.get("comment_count"))
    shares = number(record.get("share_count", record.get("repost_count")))
    collects = number(record.get("collect_count"))
    return views + likes * 10 + comments * 25 + shares * 35 + collects * 20


def engagement_rate(record: dict[str, Any]) -> float | None:
    views = number(record.get("view_count"))
    if views <= 0:
        return None
    interactions = (
        number(record.get("like_count"))
        + number(record.get("comment_count"))
        + number(record.get("share_count", record.get("repost_count")))
        + number(record.get("collect_count"))
    )
    return interactions / views


def growth_metrics(record: dict[str, Any], previous: dict[str, Any] | None, current_time: datetime, previous_time: datetime | None) -> dict[str, Any]:
    upload_time = parse_datetime(record.get("upload_date") or record.get("timestamp"))
    video_age_hours = hours_between(upload_time, current_time)
    freshness_score = None if video_age_hours is None else round(max(0.0, 1.0 - video_age_hours / (14 * 24)), 4)
    interval_hours = hours_between(previous_time, current_time)
    age_bucket = age_bucket_for(video_age_hours, RECENT_VIDEO_BUCKETS)

    metrics: dict[str, Any] = {
        "previous_seen": previous is not None,
        "video_age_hours": None if video_age_hours is None else round(video_age_hours, 2),
        "age_bucket": age_bucket,
        "age_bucket_label": age_bucket_label(age_bucket, RECENT_VIDEO_BUCKETS),
        "freshness_score": freshness_score,
        "interval_hours": None if interval_hours is None else round(interval_hours, 2),
        "views_delta": None,
        "likes_delta": None,
        "comments_delta": None,
        "shares_delta": None,
        "collects_delta": None,
        "growth_score": None,
        "growth_score_per_hour": None,
        "trend_score": None,
        "timeliness_label": "age_unknown" if video_age_hours is None else (age_bucket or "older_than_14d"),
    }
    if previous is None or not interval_hours or interval_hours <= 0:
        return metrics

    views_delta = number(record.get("view_count")) - number(previous.get("view_count"))
    likes_delta = number(record.get("like_count")) - number(previous.get("like_count"))
    comments_delta = number(record.get("comment_count")) - number(previous.get("comment_count"))
    shares_delta = number(record.get("share_count", record.get("repost_count"))) - number(previous.get("share_count", previous.get("repost_count")))
    collects_delta = number(record.get("collect_count")) - number(previous.get("collect_count"))
    score = views_delta + likes_delta * 10 + comments_delta * 25 + shares_delta * 35 + collects_delta * 20
    score_per_hour = score / interval_hours
    trend_score = score_per_hour * (1 + (freshness_score or 0.0))

    metrics.update(
        {
            "views_delta": int(views_delta),
            "likes_delta": int(likes_delta),
            "comments_delta": int(comments_delta),
            "shares_delta": int(shares_delta),
            "collects_delta": int(collects_delta),
            "growth_score": round(score, 2),
            "growth_score_per_hour": round(score_per_hour, 2),
            "trend_score": round(trend_score, 2),
        }
    )
    return metrics



def age_bucket_for(age_hours: float | None, buckets: list[dict[str, Any]]) -> str | None:
    if age_hours is None:
        return None
    for bucket in buckets:
        if float(bucket["min_hours"]) <= age_hours <= float(bucket["max_hours"]):
            return str(bucket["key"])
    return None


def age_bucket_label(key: str | None, buckets: list[dict[str, Any]]) -> str | None:
    for bucket in buckets:
        if bucket["key"] == key:
            return str(bucket["label"])
    return None


def video_age_hours(record: dict[str, Any], current_time: datetime) -> float | None:
    return hours_between(parse_datetime(record.get("upload_date") or record.get("timestamp")), current_time)


def rank_recent_videos_by_age(records: list[dict[str, Any]], previous_by_id: dict[str, dict[str, Any]], current_time: datetime, previous_time: datetime | None, limit: int = 10) -> list[dict[str, Any]]:
    grouped: list[dict[str, Any]] = []
    for bucket in RECENT_VIDEO_BUCKETS:
        bucket_records = [
            record
            for record in records
            if (age := video_age_hours(record, current_time)) is not None
            and float(bucket["min_hours"]) <= age <= float(bucket["max_hours"])
        ]
        top_records = sorted(bucket_records, key=hot_score, reverse=True)[:limit]
        grouped.append(
            {
                "key": bucket["key"],
                "label": bucket["label"],
                "min_hours": bucket["min_hours"],
                "max_hours": bucket["max_hours"],
                "items": [short_video(record, previous_by_id.get(str(record.get("video_id"))), current_time, previous_time) for record in top_records],
            }
        )
    return grouped


def short_video(record: dict[str, Any], previous: dict[str, Any] | None, current_time: datetime, previous_time: datetime | None) -> dict[str, Any]:
    return {
        "video_id": record.get("video_id"),
        "url": record.get("webpage_url"),
        "title": record.get("title"),
        "creator": record.get("uploader"),
        "source_type": record.get("source_type"),
        "source_value": record.get("source_value"),
        "upload_date": record.get("upload_date"),
        "view_count": int(number(record.get("view_count"))),
        "like_count": int(number(record.get("like_count"))),
        "comment_count": int(number(record.get("comment_count"))),
        "share_count": int(number(record.get("share_count", record.get("repost_count")))),
        "collect_count": int(number(record.get("collect_count"))),
        "engagement_rate": engagement_rate(record),
        "hot_score": round(hot_score(record), 2),
        "growth": growth_metrics(record, previous, current_time, previous_time),
        "hashtags": record.get("hashtags") or [],
        "music": record.get("music") or {},
    }


def analyze(records: list[dict[str, Any]], snapshot_path: Path, top: int, previous_records: list[dict[str, Any]] | None = None, previous_snapshot_path: Path | None = None) -> dict[str, Any]:
    unique_records = dedupe_records(records)
    previous_unique_records = dedupe_records(previous_records or [])
    previous_by_id = {str(record.get("video_id")): record for record in previous_unique_records}
    current_time = snapshot_time(records, snapshot_path)
    previous_time = snapshot_time(previous_records, previous_snapshot_path) if previous_records and previous_snapshot_path else None
    crawl_metrics = load_crawl_metrics(snapshot_path) or {}
    duplicate_rate = 0.0 if not records else round(1 - len(unique_records) / len(records), 4)
    crawl_metrics["raw_record_count"] = int(crawl_metrics.get("raw_record_count") or len(records))
    crawl_metrics["unique_video_count"] = len(unique_records)
    crawl_metrics["duplicate_rate"] = duplicate_rate
    if crawl_metrics.get("requested_total_limit"):
        crawl_metrics["effective_unique_yield"] = round(len(unique_records) / float(crawl_metrics["requested_total_limit"]), 4)
    rising_candidates = [record for record in unique_records if previous_by_id.get(str(record.get("video_id")))]
    top_videos = sorted(unique_records, key=hot_score, reverse=True)[:top]
    top_rising_videos = sorted(
        rising_candidates,
        key=lambda record: growth_metrics(record, previous_by_id.get(str(record.get("video_id"))), current_time, previous_time).get("trend_score") or 0,
        reverse=True,
    )[:top]
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_path": str(snapshot_path),
        "previous_snapshot_path": str(previous_snapshot_path) if previous_snapshot_path else None,
        "analysis_window": {
            "current_snapshot_time": current_time.isoformat(),
            "previous_snapshot_time": previous_time.isoformat() if previous_time else None,
            "interval_hours": hours_between(previous_time, current_time),
            "matched_previous_video_count": len(rising_candidates),
        },
        "record_count": len(records),
        "unique_video_count": len(unique_records),
        "source_counts": dict(Counter(record.get("source_type") for record in unique_records)),
        "top_videos": [short_video(record, previous_by_id.get(str(record.get("video_id"))), current_time, previous_time) for record in top_videos],
        "recent_videos_by_age": rank_recent_videos_by_age(unique_records, previous_by_id, current_time, previous_time, limit=top),
        "top_rising_videos": [short_video(record, previous_by_id.get(str(record.get("video_id"))), current_time, previous_time) for record in top_rising_videos],
        "top_hashtags": rank_hashtags(unique_records, previous_unique_records, current_time, top),
        "recent_signals_by_age": rank_recent_signals_by_age(unique_records, current_time, limit=top),
        "recent_terms_by_age": rank_recent_terms_by_age(unique_records, current_time),
        "recent_hashtags_by_age": rank_recent_hashtags_by_age(unique_records, current_time),
        "established_terms": rank_established_terms(unique_records, current_time, top),
        "established_hashtags": rank_established_hashtags(unique_records, current_time, top),
        "top_music": rank_music(unique_records, top),
        "top_creators": rank_creators(unique_records, top),
        "candidate_signals": build_candidate_signals(top_videos[:5]),
        "crawl_metrics": crawl_metrics,
    }
    return report


def dedupe_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for record in records:
        video_id = str(record.get("video_id") or "")
        existing = by_id.get(video_id)
        if not existing or hot_score(record) > hot_score(existing):
            by_id[video_id] = record
    return list(by_id.values())


def normalize_term(value: Any) -> str:
    term = str(value or "").lower().strip().lstrip("#@＠")
    term = re.sub(r"\s+", " ", term)
    return term.strip(" .,;:!?()[]{}\"'")


def extract_hashtag_terms(record: dict[str, Any]) -> set[str]:
    terms: set[str] = set()
    for hashtag in record.get("hashtags") or []:
        term = normalize_term(hashtag)
        if is_useful_term(term):
            terms.add(term)
    return terms


def extract_content_terms(record: dict[str, Any]) -> set[str]:
    terms: set[str] = set()
    for field in ["title", "description"]:
        value = record.get(field)
        if not isinstance(value, str):
            continue
        for match in TEXT_TERM_PATTERN.finditer(value):
            term = normalize_term(match.group(1))
            if is_useful_term(term):
                terms.add(term)
    return terms


def extract_terms(record: dict[str, Any]) -> set[str]:
    return extract_content_terms(record) | extract_hashtag_terms(record)


def is_useful_term(term: str) -> bool:
    if len(term) < 3 or term in STOP_TERMS:
        return False
    words = term.split()
    if len(words) > 4:
        return False
    if all(word in STOP_TERMS for word in words):
        return False
    if re.fullmatch(r"u[a-f0-9]{3,}", term, re.IGNORECASE):
        return False
    if all(re.fullmatch(r"u[a-f0-9]{3,}", w, re.IGNORECASE) for w in words if len(w) > 2):
        return False
    return True


def rank_hashtags(records: list[dict[str, Any]], previous_records: list[dict[str, Any]], current_time: datetime, top: int) -> list[dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = defaultdict(lambda: {"video_count": 0, "views": 0.0, "likes": 0.0, "comments": 0.0, "shares": 0.0, "score": 0.0, "example_urls": [], "newest_video_age_hours": None, "oldest_video_age_hours": None})
    previous_hashtags = set()
    for record in previous_records:
        for hashtag in record.get("hashtags") or []:
            key = normalize_term(hashtag)
            if key:
                previous_hashtags.add(key)

    for record in records:
        upload_time = parse_datetime(record.get("upload_date") or record.get("timestamp"))
        video_age_hours = hours_between(upload_time, current_time)
        for hashtag in record.get("hashtags") or []:
            key = normalize_term(hashtag)
            if not key:
                continue
            add_aggregate(stats[key], record)
            if video_age_hours is not None:
                newest = stats[key]["newest_video_age_hours"]
                oldest = stats[key]["oldest_video_age_hours"]
                stats[key]["newest_video_age_hours"] = video_age_hours if newest is None else min(newest, video_age_hours)
                stats[key]["oldest_video_age_hours"] = video_age_hours if oldest is None else max(oldest, video_age_hours)

    ranked = []
    for item in finalize_ranked(stats, len(stats)):
        oldest_age = item.get("oldest_video_age_hours")
        if oldest_age is not None and float(oldest_age) <= RECENT_TERM_MAX_HOURS:
            continue
        item["previous_seen"] = item["name"] in previous_hashtags
        item["timeliness_label"] = "established_still_hot" if item["previous_seen"] else "established_first_seen"
        for field in ["newest_video_age_hours", "oldest_video_age_hours"]:
            if item.get(field) is not None:
                item[field] = round(float(item[field]), 2)
        ranked.append(item)
    return ranked[:top]



def hashtag_timeliness_label(item: dict[str, Any], previous_seen: bool) -> str:
    oldest_age = item.get("oldest_video_age_hours")
    if previous_seen:
        return "established_still_hot"
    if oldest_age is None:
        return "new_without_upload_time"
    if oldest_age <= 24:
        return "new_within_1d"
    if oldest_age <= 72:
        return "new_within_3d"
    if oldest_age <= 168:
        return "new_within_7d"
    return "established_first_seen"


def empty_term_bucket() -> dict[str, Any]:
    return {"video_count": 0, "views": 0.0, "likes": 0.0, "comments": 0.0, "shares": 0.0, "score": 0.0, "example_urls": [], "newest_video_age_hours": None, "oldest_video_age_hours": None, "video_ids": set(), "video_ages_by_id": {}}


def term_stats(records: list[dict[str, Any]], current_time: datetime | None = None, extractor: Any = extract_terms) -> dict[str, dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = defaultdict(empty_term_bucket)
    for record in records:
        video_id = str(record.get("video_id") or "")
        upload_time = parse_datetime(record.get("upload_date") or record.get("timestamp"))
        video_age_hours = hours_between(upload_time, current_time) if current_time else None
        for term in extractor(record):
            add_aggregate(stats[term], record)
            if video_id:
                stats[term]["video_ids"].add(video_id)
                if video_age_hours is not None:
                    stats[term]["video_ages_by_id"][video_id] = video_age_hours
            if video_age_hours is not None:
                newest = stats[term]["newest_video_age_hours"]
                oldest = stats[term]["oldest_video_age_hours"]
                stats[term]["newest_video_age_hours"] = video_age_hours if newest is None else min(newest, video_age_hours)
                stats[term]["oldest_video_age_hours"] = video_age_hours if oldest is None else max(oldest, video_age_hours)
    return stats


def recent_delta_counts(current: dict[str, Any], previous: dict[str, Any] | None) -> dict[str, int]:
    previous_video_ids = previous.get("video_ids", set()) if previous else set()
    current_video_ids = current.get("video_ids", set())
    new_video_ids = current_video_ids - previous_video_ids
    ages_by_id = current.get("video_ages_by_id") if isinstance(current.get("video_ages_by_id"), dict) else {}
    recent_24h = 0
    recent_7d = 0
    for video_id in new_video_ids:
        age = ages_by_id.get(video_id)
        if age is None:
            continue
        if float(age) <= 24:
            recent_24h += 1
        if float(age) <= 168:
            recent_7d += 1
    return {"sample_delta": len(new_video_ids), "recent_24h_delta": recent_24h, "recent_7d_delta": recent_7d}


def term_item(name: str, current: dict[str, Any], previous: dict[str, Any] | None = None) -> dict[str, Any]:
    previous_video_count = int(previous["video_count"]) if previous else 0
    previous_views = float(previous["views"]) if previous else 0.0
    previous_score = float(previous["score"]) if previous else 0.0
    video_count_delta = int(current["video_count"] - previous_video_count)
    views_delta = float(current["views"] - previous_views)
    score_delta = float(current["score"] - previous_score)
    deltas = recent_delta_counts(current, previous)
    sample_video_delta = deltas["sample_delta"]
    recent_24h_video_delta = deltas["recent_24h_delta"]
    recent_7d_video_delta = deltas["recent_7d_delta"]
    if previous is None:
        status = "new_emerging" if current["video_count"] >= 2 else "single_signal"
    elif score_delta > 0 and recent_7d_video_delta > 0:
        status = "spreading"
    else:
        status = "mature_or_flat"
    emergence_score = max(score_delta, 0.0) + max(recent_7d_video_delta, 0) * 100_000 + (0 if previous else current["score"] * 0.25)
    avg_spv = current["score"] / max(int(current["video_count"]), 1)
    coverage_score = int(current["video_count"]) * math.log1p(avg_spv)
    return {
        "name": name,
        "status": status,
        "video_count": int(current["video_count"]),
        "previous_video_count": previous_video_count,
        "video_count_delta": video_count_delta,
        "sample_video_delta": sample_video_delta,
        "recent_24h_video_delta": recent_24h_video_delta,
        "recent_7d_video_delta": recent_7d_video_delta,
        "views": round(current["views"], 2),
        "previous_views": round(previous_views, 2),
        "views_delta": round(views_delta, 2),
        "score": round(current["score"], 2),
        "coverage_score": round(coverage_score, 2),
        "score_delta": round(score_delta, 2),
        "emergence_score": round(emergence_score, 2),
        "newest_video_age_hours": None if current.get("newest_video_age_hours") is None else round(float(current["newest_video_age_hours"]), 2),
        "oldest_video_age_hours": None if current.get("oldest_video_age_hours") is None else round(float(current["oldest_video_age_hours"]), 2),
        "example_urls": current["example_urls"],
    }


def aggregate_terms_by_age(records: list[dict[str, Any]], current_time: datetime, extractor: Any, limit: int) -> list[dict[str, Any]]:
    bucket_stats_list: list[dict[str, dict[str, Any]]] = []
    for _bucket in RECENT_TERM_BUCKETS:
        bucket_stats_list.append(
            defaultdict(lambda: {"video_count": 0, "views": 0.0, "likes": 0.0, "comments": 0.0, "shares": 0.0, "score": 0.0, "example_urls": [], "newest_video_age_hours": None, "oldest_video_age_hours": None})
        )

    for record in records:
        age = video_age_hours(record, current_time)
        if age is None:
            continue
        for idx, bucket in enumerate(RECENT_TERM_BUCKETS):
            if age < float(bucket["min_hours"]) or age > float(bucket["max_hours"]):
                continue
            for term in extractor(record):
                stats = bucket_stats_list[idx][term]
                add_aggregate(stats, record)
                newest = stats["newest_video_age_hours"]
                oldest = stats["oldest_video_age_hours"]
                stats["newest_video_age_hours"] = age if newest is None else min(newest, age)
                stats["oldest_video_age_hours"] = age if oldest is None else max(oldest, age)

    bucket_term_names: list[set[str]] = [set(stats.keys()) for stats in bucket_stats_list]

    grouped: list[dict[str, Any]] = []
    for idx, bucket in enumerate(RECENT_TERM_BUCKETS):
        older_term_names: set[str] = set()
        for j in range(idx + 1, len(bucket_term_names)):
            older_term_names |= bucket_term_names[j]

        items = [term_item(name, values) for name, values in bucket_stats_list[idx].items()]
        for item in items:
            item["novelty"] = "first_seen" if item["name"] not in older_term_names else "seen_in_older_buckets"
        heat_ranked = sorted(items, key=lambda item: (item["score"], item["video_count"]), reverse=True)[:limit]
        coverage_ranked = sorted(items, key=lambda item: (item.get("coverage_score", 0), item["video_count"]), reverse=True)[:limit]
        grouped.append(
            {
                "key": bucket["key"],
                "label": bucket["label"],
                "min_hours": bucket["min_hours"],
                "max_hours": bucket["max_hours"],
                "items": heat_ranked,
                "coverage_items": coverage_ranked,
            }
        )
    return grouped


def rank_recent_signals_by_age(records: list[dict[str, Any]], current_time: datetime, limit: int = 10) -> list[dict[str, Any]]:
    content_groups = aggregate_terms_by_age(records, current_time, extract_content_terms, limit)
    hashtag_groups = aggregate_terms_by_age(records, current_time, extract_hashtag_terms, limit)
    groups: list[dict[str, Any]] = []
    for content_group, hashtag_group in zip(content_groups, hashtag_groups):
        groups.append(
            {
                "key": content_group["key"],
                "label": content_group["label"],
                "min_hours": content_group["min_hours"],
                "max_hours": content_group["max_hours"],
                "content_terms": content_group["items"],
                "content_terms_coverage": content_group["coverage_items"],
                "hashtags": hashtag_group["items"],
                "hashtags_coverage": hashtag_group["coverage_items"],
            }
        )
    return groups


def rank_recent_terms_by_age(records: list[dict[str, Any]], current_time: datetime, limit: int = 5) -> list[dict[str, Any]]:
    return aggregate_terms_by_age(records, current_time, extract_content_terms, limit)


def rank_recent_hashtags_by_age(records: list[dict[str, Any]], current_time: datetime, limit: int = 5) -> list[dict[str, Any]]:
    return aggregate_terms_by_age(records, current_time, extract_hashtag_terms, limit)


def rank_established_terms(records: list[dict[str, Any]], current_time: datetime, top: int) -> list[dict[str, Any]]:
    current_stats = term_stats(records, current_time, extract_content_terms)
    ranked = []
    for name, current in current_stats.items():
        ages = [float(a) for a in (current.get("video_ages_by_id") or {}).values() if a is not None]
        if not ages:
            continue
        oldest = max(ages)
        newest = min(ages)
        if oldest <= RECENT_TERM_MAX_HOURS:
            continue
        recent_24h = sum(1 for a in ages if a <= 24)
        recent_7d = sum(1 for a in ages if a <= 168)
        vc = int(current["video_count"])
        status = "cooling"
        if newest <= 168 and (recent_7d / max(vc, 1)) >= ESTABLISHED_ACTIVE_RATIO:
            status = "spreading"
        elif newest <= 720:
            status = "mature_or_flat"
        avg_spv = current["score"] / max(vc, 1)
        coverage_score = int(current["video_count"]) * math.log1p(avg_spv)
        ranked.append({
            "name": name, "status": status,
            "video_count": int(current["video_count"]),
            "sample_video_delta": int(current["video_count"]),
            "recent_24h_video_delta": recent_24h, "recent_7d_video_delta": recent_7d,
            "score": round(current["score"], 2), "score_delta": round(current["score"], 2),
            "coverage_score": round(coverage_score, 2),
            "oldest_video_age_hours": round(oldest, 2), "newest_video_age_hours": round(newest, 2),
            "example_urls": current["example_urls"],
        })
    return sorted(ranked, key=lambda item: (item["score_delta"], item["score"], item["video_count"]), reverse=True)[:top]


def rank_established_hashtags(records: list[dict[str, Any]], current_time: datetime, top: int) -> list[dict[str, Any]]:
    current_stats = term_stats(records, current_time, extract_hashtag_terms)
    ranked = []
    for name, current in current_stats.items():
        ages = [float(a) for a in (current.get("video_ages_by_id") or {}).values() if a is not None]
        if not ages:
            continue
        oldest = max(ages)
        newest = min(ages)
        if oldest <= RECENT_TERM_MAX_HOURS:
            continue
        recent_24h = sum(1 for a in ages if a <= 24)
        recent_7d = sum(1 for a in ages if a <= 168)
        vc = int(current["video_count"])
        status = "cooling"
        if newest <= 168 and (recent_7d / max(vc, 1)) >= ESTABLISHED_ACTIVE_RATIO:
            status = "spreading"
        elif newest <= 720:
            status = "mature_or_flat"
        avg_spv = current["score"] / max(vc, 1)
        coverage_score = int(current["video_count"]) * math.log1p(avg_spv)
        ranked.append({
            "name": name, "status": status,
            "video_count": int(current["video_count"]),
            "sample_video_delta": int(current["video_count"]),
            "recent_24h_video_delta": recent_24h, "recent_7d_video_delta": recent_7d,
            "score": round(current["score"], 2), "score_delta": round(current["score"], 2),
            "coverage_score": round(coverage_score, 2),
            "oldest_video_age_hours": round(oldest, 2), "newest_video_age_hours": round(newest, 2),
            "example_urls": current["example_urls"],
        })
    return sorted(ranked, key=lambda item: (item["score_delta"], item["score"], item["video_count"]), reverse=True)[:top]

def rank_music(records: list[dict[str, Any]], top: int) -> list[dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = defaultdict(lambda: {"video_count": 0, "views": 0.0, "likes": 0.0, "comments": 0.0, "shares": 0.0, "score": 0.0, "example_urls": [], "artist": None, "music_id": None})
    for record in records:
        music = record.get("music") if isinstance(record.get("music"), dict) else {}
        track = music.get("track") or music.get("id")
        if not track:
            continue
        key = str(track)
        add_aggregate(stats[key], record)
        stats[key]["artist"] = stats[key]["artist"] or music.get("artist")
        stats[key]["music_id"] = stats[key]["music_id"] or music.get("id")
    return finalize_ranked(stats, top)


def rank_creators(records: list[dict[str, Any]], top: int) -> list[dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = defaultdict(lambda: {"video_count": 0, "views": 0.0, "likes": 0.0, "comments": 0.0, "shares": 0.0, "score": 0.0, "example_urls": [], "follower_count": None})
    for record in records:
        creator = record.get("uploader")
        if not creator:
            continue
        key = str(creator)
        add_aggregate(stats[key], record)
        stats[key]["follower_count"] = stats[key]["follower_count"] or record.get("uploader_follower_count")
    return finalize_ranked(stats, top)


def add_aggregate(bucket: dict[str, Any], record: dict[str, Any]) -> None:
    bucket["video_count"] += 1
    bucket["views"] += number(record.get("view_count"))
    bucket["likes"] += number(record.get("like_count"))
    bucket["comments"] += number(record.get("comment_count"))
    bucket["shares"] += number(record.get("share_count", record.get("repost_count")))
    bucket["score"] += hot_score(record)
    if record.get("webpage_url") and len(bucket["example_urls"]) < 3:
        bucket["example_urls"].append(record.get("webpage_url"))


def finalize_ranked(stats: dict[str, dict[str, Any]], top: int) -> list[dict[str, Any]]:
    ranked = []
    for name, values in stats.items():
        item = {"name": name, **values}
        for field in ["views", "likes", "comments", "shares", "score"]:
            item[field] = round(item[field], 2)
        vc = max(item.get("video_count", 0), 1)
        item["avg_score_per_video"] = round(item["score"] / vc, 2)
        item["coverage_score"] = round(vc * math.log1p(item["avg_score_per_video"]), 2)
        ranked.append(item)
    return sorted(ranked, key=lambda item: (item["score"], item["video_count"]), reverse=True)[:top]


def build_candidate_signals(records: list[dict[str, Any]]) -> list[str]:
    signals = []
    for record in records:
        title = str(record.get("title") or "").strip()
        creator = record.get("uploader") or "unknown"
        views = int(number(record.get("view_count")))
        likes = int(number(record.get("like_count")))
        url = record.get("webpage_url")
        if title:
            title = title[:120] + ("..." if len(title) > 120 else "")
        signals.append(f"{creator}: {views:,} views, {likes:,} likes — {title} ({url})")
    return signals


def write_report(report: dict[str, Any], output_dir: Path) -> Path:
    output_dir = output_dir if output_dir.is_absolute() else PROJECT_ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"tiktok_hotspot_analysis_{utc_timestamp()}.json"
    with path.open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)
        file.write("\n")
    return path


def print_summary(report: dict[str, Any], output_path: Path) -> None:
    print(f"report: {output_path}")
    print(f"snapshot: {report['snapshot_path']}")
    print(f"previous_snapshot: {report['previous_snapshot_path']}")
    print(f"records: {report['record_count']} unique_videos: {report['unique_video_count']}")
    print(f"matched_previous_videos: {report['analysis_window']['matched_previous_video_count']}")
    print("\nTop videos by cumulative heat:")
    for index, item in enumerate(report["top_videos"][:5], start=1):
        label = item["growth"]["timeliness_label"]
        age = item["growth"]["video_age_hours"]
        print(f"{index}. {item['creator']} | views={item['view_count']:,} likes={item['like_count']:,} score={item['hot_score']:,.0f} age_hours={age} label={label}")
        print(f"   {item['url']}")
    print("\nTop rising videos:")
    if not report["top_rising_videos"]:
        print("No overlapping videos found in the previous snapshot; run the same monitored sources again to compute growth.")
    for index, item in enumerate(report["top_rising_videos"][:5], start=1):
        growth = item["growth"]
        print(f"{index}. {item['creator']} | views_delta={growth['views_delta']:,} trend_score={growth['trend_score']:,.0f} label={growth['timeliness_label']}")
        print(f"   {item['url']}")
    print("\nTop hashtags:")
    for index, item in enumerate(report["top_hashtags"][:5], start=1):
        print(f"{index}. #{item['name']} | videos={item['video_count']} views={int(item['views']):,} score={item['score']:,.0f}")
    print("\nRecent terms by age:")
    for group in report["recent_terms_by_age"]:
        print(f"{group['label']}:")
        for index, item in enumerate(group["items"][:5], start=1):
            print(f"  {index}. {item['name']} | videos={item['video_count']} views={int(item['views']):,} score={item['score']:,.0f}")
    print("\nEstablished terms:")
    for index, item in enumerate(report["established_terms"][:5], start=1):
        print(f"{index}. {item['name']} | status={item['status']} videos={item['video_count']} delta={item['video_count_delta']} views_delta={int(item['views_delta']):,} score={item['score']:,.0f}")


def main() -> int:
    args = parse_args()
    try:
        snapshot_path = resolve_path(args.snapshot) if args.snapshot else latest_snapshot()
        records = load_jsonl(snapshot_path)
        previous_snapshot_path = resolve_path(args.previous_snapshot) if args.previous_snapshot else previous_snapshot_for(snapshot_path)
        previous_records = load_jsonl(previous_snapshot_path) if previous_snapshot_path else None
        report = analyze(records, snapshot_path, args.top, previous_records, previous_snapshot_path)
        output_path = write_report(report, args.output_dir)
    except ValueError as exc:
        print(f"analysis error: {exc}")
        return 2
    print_summary(report, output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
