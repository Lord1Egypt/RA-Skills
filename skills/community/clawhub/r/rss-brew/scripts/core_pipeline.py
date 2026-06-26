#!/usr/bin/env python3
"""RSS-Brew core pipeline: fetch feeds, extract clean text, deduplicate.

Outputs a JSON payload of ONLY new, pure-text articles.
Also emits structured run stats and maintains separated dedup + metadata stores.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import feedparser
import trafilatura
import yaml
from pydantic import BaseModel, ValidationError

TRACKING_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "segmentid",
}


class Source(BaseModel):
    name: str
    url: str
    deepset_eligible: bool = True


class SourcesConfig(BaseModel):
    sources: List[Source]


def load_sources(path: Path) -> List[Source]:
    if not path.exists():
        raise FileNotFoundError(f"sources.yaml not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    try:
        config = SourcesConfig(**data)
    except ValidationError as exc:
        raise ValueError(f"Invalid sources.yaml: {exc}") from exc
    return config.sources


def hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def _is_sha256_hex(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", value or ""))


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url)
    scheme = (parts.scheme or "https").lower()

    netloc = parts.netloc
    host = (parts.hostname or "").lower()
    port = parts.port
    if host:
        if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
            netloc = f"{host}:{port}"
        else:
            netloc = host

    query_pairs = parse_qsl(parts.query, keep_blank_values=False)
    filtered_pairs = []
    for k, v in query_pairs:
        key = k.lower()
        if key.startswith("utm_"):
            continue
        if key in TRACKING_KEYS:
            continue
        filtered_pairs.append((k, v))

    query = urlencode(filtered_pairs, doseq=True)
    return urlunsplit((scheme, netloc, parts.path, query, ""))


def normalize_title(title: str) -> str:
    lowered = title.lower().strip()
    lowered = re.sub(r"[^\w\s]", " ", lowered)
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered


def _extract_url_from_legacy_entry(key: str, value: Any) -> Optional[str]:
    if isinstance(key, str) and key.startswith(("http://", "https://")):
        return key

    if isinstance(value, str) and value.startswith(("http://", "https://")):
        return value

    if isinstance(value, dict):
        nested_url = value.get("url")
        if isinstance(nested_url, str) and nested_url.startswith(("http://", "https://")):
            return nested_url

    return None


def _metadata_subset(record: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key in ("title", "source", "published", "category", "score"):
        value = record.get(key)
        if value is not None:
            out[key] = value
    return out


def _normalize_score(score: Any) -> Tuple[Optional[int], bool]:
    if score is None:
        return None, False
    try:
        value = int(score)
    except (TypeError, ValueError):
        return 0, True
    clamped = max(0, min(5, value))
    return clamped, clamped != value


def _normalize_category(category: Any) -> Tuple[Optional[str], bool]:
    if category is None:
        return None, False
    if not isinstance(category, str):
        return "other", True
    value = category.strip().lower()
    if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        return value, False
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        return "other", True
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        return "other", True
    return value, True


def normalize_dedup_and_metadata(raw_dedup: Any, raw_metadata: Any) -> Tuple[Dict[str, str], Dict[str, Dict[str, Any]], Dict[str, int]]:
    index: Dict[str, str] = {}
    metadata: Dict[str, Dict[str, Any]] = {}
    migration_stats = {
        "legacy_index_entries": 0,
        "legacy_metadata_entries": 0,
        "canonicalized_existing_urls": 0,
    }

    # load existing metadata first
    if isinstance(raw_metadata, dict):
        for key, value in raw_metadata.items():
            if _is_sha256_hex(str(key)) and isinstance(value, dict):
                metadata[str(key)] = _metadata_subset(value)

    if not isinstance(raw_dedup, dict):
        return index, metadata, migration_stats

    for key, value in raw_dedup.items():
        key_str = key.strip() if isinstance(key, str) else ""
        candidate_url: Optional[str] = None
        meta_candidate: Dict[str, Any] = {}

        if _is_sha256_hex(key_str):
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                candidate_url = value
            elif isinstance(value, dict):
                nested_url = value.get("url")
                if isinstance(nested_url, str) and nested_url.startswith(("http://", "https://")):
                    candidate_url = nested_url
                meta_candidate = _metadata_subset(value)
                if meta_candidate:
                    migration_stats["legacy_metadata_entries"] += 1
        else:
            candidate_url = _extract_url_from_legacy_entry(key_str, value)
            if candidate_url:
                migration_stats["legacy_index_entries"] += 1
            if isinstance(value, dict):
                meta_candidate = _metadata_subset(value)
                if meta_candidate:
                    migration_stats["legacy_metadata_entries"] += 1

        if not candidate_url:
            continue

        canonical_url = canonicalize_url(candidate_url)
        if canonical_url != candidate_url:
            migration_stats["canonicalized_existing_urls"] += 1
        url_hash = hash_url(canonical_url)
        index[url_hash] = canonical_url

        if meta_candidate:
            metadata[url_hash] = {**metadata.get(url_hash, {}), **meta_candidate}

    return index, metadata, migration_stats


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_json_locked(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_suffix(path.suffix + ".lock")
    tmp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}")

    with open(lock_path, "a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            with open(tmp_path, "w", encoding="utf-8") as tmp_file:
                json.dump(payload, tmp_file, indent=2, ensure_ascii=False)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
            os.replace(tmp_path, path)
        finally:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)


def entry_datetime(entry) -> Optional[datetime]:
    # feedparser provides published_parsed / updated_parsed as time.struct_time
    struct_time = entry.get("published_parsed") or entry.get("updated_parsed")
    if not struct_time:
        return None
    return datetime.fromtimestamp(time.mktime(struct_time), tz=timezone.utc)


def extract_text(url: str, retries: int = 2, retry_delay: float = 0.6) -> Optional[str]:
    for attempt in range(retries + 1):
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=False,
                include_images=False,
                favor_recall=False,
            )
            if text:
                return text.strip()
        if attempt < retries:
            time.sleep(retry_delay)
    return None


def extract_feed_summary(entry) -> Optional[str]:
    """Fallback when full-text extraction fails: use feed summary/content text."""
    candidates: List[str] = []

    summary = entry.get("summary") or entry.get("description")
    if summary:
        candidates.append(summary)

    content = entry.get("content")
    if isinstance(content, list):
        for item in content:
            value = item.get("value") if isinstance(item, dict) else None
            if value:
                candidates.append(value)

    for raw in candidates:
        # Strip HTML tags and normalize whitespace
        cleaned = re.sub(r"<[^>]+>", " ", raw)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        if cleaned and len(cleaned) >= 80:
            return cleaned
    return None


def should_skip_entry(source_name: str, url: str) -> bool:
    """Drop low-signal Bloomberg multimedia links that often fail text extraction."""
    if "bloomberg" in source_name.lower():
        if "/news/videos/" in url or "/news/audio/" in url:
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="RSS-Brew core pipeline")
    parser.add_argument(
        "--sources",
        default="/root/workplace/2 Areas/rss-brew-data/sources.yaml",
        help="Path to sources.yaml",
    )
    parser.add_argument(
        "--dedup",
        default="/root/workplace/2 Areas/rss-brew-data/processed-index.json",
        help="Path to dedup index JSON",
    )
    parser.add_argument(
        "--metadata",
        default="/root/workplace/2 Areas/rss-brew-data/metadata.json",
        help="Path to metadata JSON",
    )
    parser.add_argument(
        "--output",
        default="/root/workplace/2 Areas/rss-brew-data/new-articles.json",
        help="Path to output JSON",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=48,
        help="Lookback window in hours",
    )
    parser.add_argument(
        "--run-stats-dir",
        default="/root/workplace/2 Areas/rss-brew-data/run-stats",
        help="Path to run-stats output directory",
    )
    args = parser.parse_args()

    sources_path = Path(args.sources)
    dedup_path = Path(args.dedup)
    metadata_path = Path(args.metadata)
    output_path = Path(args.output)

    sources = load_sources(sources_path)

    raw_dedup = load_json(dedup_path)
    raw_metadata = load_json(metadata_path)
    dedup_index, metadata_index, migration_stats = normalize_dedup_and_metadata(raw_dedup, raw_metadata)

    cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)

    new_articles = []
    updated_index = dict(dedup_index)
    updated_metadata = dict(metadata_index)

    stats: Dict[str, Any] = {
        "total_entries": 0,
        "invalid": 0,
        "old": 0,
        "dedup": 0,
        "title_dedup": 0,
        "skipped_multimedia": 0,
        "extract_fail": 0,
        "fallback_used": 0,
        "new": 0,
        "category_fixed": 0,
        "score_fixed": 0,
        "canonicalized_in_run": 0,
        "migration": migration_stats,
    }

    source_stats: Dict[str, Dict[str, int]] = {
        source.name: {
            "recent": 0,
            "dedup": 0,
            "skipped": 0,
            "extract_fail": 0,
            "fallback_used": 0,
            "new": 0,
            "title_dedup": 0,
        }
        for source in sources
    }

    canonicalization_examples: List[Dict[str, str]] = []
    seen_titles: set[str] = set()

    for source in sources:
        feed = feedparser.parse(source.url)
        source_stat = source_stats[source.name]

        for entry in feed.entries:
            stats["total_entries"] += 1
            url = entry.get("link")
            title = entry.get("title")
            if not url or not title:
                stats["invalid"] += 1
                continue

            published_dt = entry_datetime(entry)
            if not published_dt or published_dt < cutoff:
                stats["old"] += 1
                continue

            source_stat["recent"] += 1

            canonical_url = canonicalize_url(url)
            if canonical_url != url:
                stats["canonicalized_in_run"] += 1
                if len(canonicalization_examples) < 5:
                    canonicalization_examples.append({"original": url, "canonical": canonical_url})

            if should_skip_entry(source.name, canonical_url):
                stats["skipped_multimedia"] += 1
                source_stat["skipped"] += 1
                continue

            url_hash = hash_url(canonical_url)
            if url_hash in updated_index:
                stats["dedup"] += 1
                source_stat["dedup"] += 1
                continue

            normalized_title = normalize_title(title)
            if normalized_title in seen_titles:
                stats["title_dedup"] += 1
                source_stat["title_dedup"] += 1
                continue

            # Always keep a short feed-level summary for cheap Phase-A scoring.
            feed_summary = extract_feed_summary(entry)

            text = extract_text(canonical_url)
            if not text:
                # Fallback to feed summary when full-text extraction fails.
                if feed_summary:
                    text = feed_summary
                    stats["fallback_used"] += 1
                    source_stat["fallback_used"] += 1
                else:
                    stats["extract_fail"] += 1
                    source_stat["extract_fail"] += 1
                    continue

            article = {
                "source": source.name,
                "source_url": source.url,
                "title": title,
                "url": canonical_url,
                "published": published_dt.isoformat(),
                "summary": feed_summary or "",
                "text": text,
            }

            category, category_fixed = _normalize_category(article.get("category"))
            if category is not None:
                article["category"] = category
            if category_fixed:
                stats["category_fixed"] += 1

            score, score_fixed = _normalize_score(article.get("score"))
            if score is not None:
                article["score"] = score
            if score_fixed:
                stats["score_fixed"] += 1

            new_articles.append(article)
            seen_titles.add(normalized_title)
            updated_index[url_hash] = canonical_url
            updated_metadata[url_hash] = {
                **updated_metadata.get(url_hash, {}),
                **_metadata_subset(article),
            }
            stats["new"] += 1
            source_stat["new"] += 1

    generated_at = datetime.now(timezone.utc)
    payload = {
        "generated_at": generated_at.isoformat(),
        "article_count": len(new_articles),
        "articles": new_articles,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    save_json_locked(dedup_path, updated_index)
    save_json_locked(metadata_path, updated_metadata)

    run_stats_dir = Path(args.run_stats_dir)
    run_stats_dir.mkdir(parents=True, exist_ok=True)
    run_stats_path = run_stats_dir / f"run-stats-{generated_at.strftime('%Y-%m-%dT%H%M%SZ')}.json"

    run_stats_payload = {
        "generated_at": generated_at.isoformat(),
        "article_count": len(new_articles),
        "by_source": source_stats,
        "global": stats,
        "canonicalization_examples": canonicalization_examples,
    }
    run_stats_path.write_text(json.dumps(run_stats_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print("RSS-Brew stats:", json.dumps(run_stats_payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
