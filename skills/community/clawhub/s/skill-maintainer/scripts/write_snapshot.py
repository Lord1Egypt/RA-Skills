#!/usr/bin/env python3
"""Write a portfolio stats snapshot and latest growth deltas."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


METRIC_KEYS = ("downloads", "installs_all_time", "installs_current", "stars", "comments", "versions")


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def utc_now_iso() -> str:
    return utc_now().isoformat()


def to_int(value: Any) -> int:
    try:
        if value in (None, ""):
            return 0
        return int(float(value))
    except Exception:
        return 0


def to_float(value: Any) -> float:
    try:
        if value in (None, ""):
            return 0.0
        return float(value)
    except Exception:
        return 0.0


def parse_iso(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def snapshot_id_from(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def unique_snapshot_path(snapshot_dir: Path, snapshot_id: str) -> tuple[str, Path]:
    candidate_id = snapshot_id
    candidate = snapshot_dir / f"{candidate_id}.json"
    suffix = 2
    while candidate.exists():
        candidate_id = f"{snapshot_id}-{suffix}"
        candidate = snapshot_dir / f"{candidate_id}.json"
        suffix += 1
    return candidate_id, candidate


def unique_archive_dir(snapshot_dir: Path, archive_id: str) -> Path:
    archive_root = snapshot_dir / "archive"
    candidate = archive_root / archive_id
    suffix = 2
    while candidate.exists():
        candidate = archive_root / f"{archive_id}-{suffix}"
        suffix += 1
    return candidate


def snapshot_files(snapshot_dir: Path) -> list[Path]:
    if not snapshot_dir.exists():
        return []
    return sorted(path for path in snapshot_dir.glob("*.json") if path.name != "latest.json")


def archive_active_snapshots(snapshot_dir: Path, archive_id: str) -> Path | None:
    active = snapshot_files(snapshot_dir)
    latest = snapshot_dir / "latest.json"
    if latest.exists():
        active.append(latest)
    if not active:
        return None
    archive_dir = unique_archive_dir(snapshot_dir, archive_id)
    archive_dir.mkdir(parents=True, exist_ok=True)
    for path in active:
        path.replace(archive_dir / path.name)
    return archive_dir


def snapshot_sort_key(path: Path) -> tuple[str, str]:
    data = read_json(path)
    return str(data.get("generated_at_utc") or data.get("snapshot_id") or path.stem), path.name


def skill_snapshot_row(row: dict[str, str]) -> dict[str, Any]:
    return {
        "slug": row.get("slug", ""),
        "display_name": row.get("display_name", ""),
        "summary": row.get("summary", ""),
        "downloads": to_int(row.get("downloads")),
        "installs_all_time": to_int(row.get("installs_all_time")),
        "installs_current": to_int(row.get("installs_current")),
        "stars": to_int(row.get("stars")),
        "comments": to_int(row.get("comments")),
        "versions": to_int(row.get("versions")),
        "meaning_score": to_float(row.get("meaning_score")),
        "meaningfulness": row.get("meaningfulness", ""),
        "portfolio_decision": row.get("portfolio_decision", ""),
        "category": row.get("category", "Other"),
        "updated_at_utc": row.get("updated_at_utc", ""),
    }


def build_snapshot(
    handle: str,
    rows: list[dict[str, str]],
    *,
    generated_at_utc: str,
    snapshot_id: str,
    collection_summary: dict[str, Any],
) -> dict[str, Any]:
    skills = [skill_snapshot_row(row) for row in rows]
    return {
        "schema_version": 1,
        "handle": handle,
        "snapshot_id": snapshot_id,
        "generated_at_utc": generated_at_utc,
        "source": {
            "collection_started_at_utc": collection_summary.get("started_at_utc", ""),
            "collection_ended_at_utc": collection_summary.get("ended_at_utc", ""),
            "collected_skill_count": collection_summary.get("collected_skill_count", ""),
            "detail_success_count": collection_summary.get("detail_success_count", ""),
            "detail_error_count": collection_summary.get("detail_error_count", ""),
        },
        "skill_count": len(skills),
        "totals": {key: sum(to_int(row.get(key)) for row in skills) for key in METRIC_KEYS},
        "skills": skills,
    }


def index_by_slug(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    skills = snapshot.get("skills") if isinstance(snapshot.get("skills"), list) else []
    return {str(row.get("slug", "")): row for row in skills if row.get("slug")}


def growth_rows(current: dict[str, Any], previous: dict[str, Any] | None) -> list[dict[str, Any]]:
    current_rows = index_by_slug(current)
    previous_rows = index_by_slug(previous or {})
    has_previous = bool(previous)
    rows: list[dict[str, Any]] = []
    for slug, current_row in current_rows.items():
        previous_row = previous_rows.get(slug, {})
        is_new_skill = has_previous and slug not in previous_rows
        download_delta = to_int(current_row.get("downloads")) - to_int(previous_row.get("downloads"))
        install_delta = to_int(current_row.get("installs_all_time")) - to_int(previous_row.get("installs_all_time"))
        row = {
            "snapshot_id": current.get("snapshot_id", ""),
            "previous_snapshot_id": (previous or {}).get("snapshot_id", ""),
            "slug": slug,
            "display_name": current_row.get("display_name", ""),
            "category": current_row.get("category", "Other"),
            "meaning_score": current_row.get("meaning_score", 0),
            "meaningfulness": current_row.get("meaningfulness", ""),
            "portfolio_decision": current_row.get("portfolio_decision", ""),
            "downloads": to_int(current_row.get("downloads")),
            "previous_downloads": to_int(previous_row.get("downloads")) if has_previous else "",
            "download_delta": download_delta if has_previous else 0,
            "new_downloads": max(0, download_delta) if has_previous else 0,
            "installs_all_time": to_int(current_row.get("installs_all_time")),
            "previous_installs_all_time": to_int(previous_row.get("installs_all_time")) if has_previous else "",
            "install_delta": install_delta if has_previous else 0,
            "new_installs": max(0, install_delta) if has_previous else 0,
            "stars": to_int(current_row.get("stars")),
            "previous_stars": to_int(previous_row.get("stars")) if has_previous else "",
            "star_delta": to_int(current_row.get("stars")) - to_int(previous_row.get("stars")) if has_previous else 0,
            "comments": to_int(current_row.get("comments")),
            "previous_comments": to_int(previous_row.get("comments")) if has_previous else "",
            "comment_delta": to_int(current_row.get("comments")) - to_int(previous_row.get("comments")) if has_previous else 0,
            "versions": to_int(current_row.get("versions")),
            "previous_versions": to_int(previous_row.get("versions")) if has_previous else "",
            "version_delta": to_int(current_row.get("versions")) - to_int(previous_row.get("versions")) if has_previous else 0,
            "is_new_skill": is_new_skill,
        }
        rows.append(row)
    rows.sort(key=lambda row: (-to_int(row.get("new_downloads")), -to_int(row.get("new_installs")), row.get("slug", "")))
    return rows


def slim_growth_rows(rows: list[dict[str, Any]], metric: str, limit: int = 20) -> list[dict[str, Any]]:
    ranked = [row for row in rows if to_int(row.get(metric)) > 0]
    ranked.sort(key=lambda row: (-to_int(row.get(metric)), -to_int(row.get("downloads")), row.get("slug", "")))
    keys = [
        "slug",
        "display_name",
        "category",
        "meaning_score",
        "portfolio_decision",
        "downloads",
        "new_downloads",
        "installs_all_time",
        "new_installs",
        "stars",
        "comments",
        "is_new_skill",
    ]
    return [{key: row.get(key, "") for key in keys} for row in ranked[:limit]]


def build_trend_summary(
    handle: str,
    current: dict[str, Any],
    previous: dict[str, Any] | None,
    rows: list[dict[str, Any]],
    *,
    snapshot_count: int,
) -> dict[str, Any]:
    latest_at = str(current.get("generated_at_utc", ""))
    previous_at = str((previous or {}).get("generated_at_utc", ""))
    latest_dt = parse_iso(latest_at)
    previous_dt = parse_iso(previous_at)
    window_hours = None
    if latest_dt and previous_dt:
        window_hours = round((latest_dt - previous_dt).total_seconds() / 3600, 2)

    return {
        "handle": handle,
        "generated_at_utc": utc_now_iso(),
        "has_previous": previous is not None,
        "snapshot_count": snapshot_count,
        "latest_snapshot_id": current.get("snapshot_id", ""),
        "previous_snapshot_id": (previous or {}).get("snapshot_id", ""),
        "latest_at_utc": latest_at,
        "previous_at_utc": previous_at,
        "window_hours": window_hours,
        "skill_count": current.get("skill_count", 0),
        "deltas": {
            "new_downloads": sum(to_int(row.get("new_downloads")) for row in rows),
            "new_installs": sum(to_int(row.get("new_installs")) for row in rows),
            "star_delta": sum(to_int(row.get("star_delta")) for row in rows),
            "comment_delta": sum(to_int(row.get("comment_delta")) for row in rows),
            "new_skill_count": sum(1 for row in rows if row.get("is_new_skill")),
        },
        "top_new_downloads": slim_growth_rows(rows, "new_downloads"),
        "top_new_installs": slim_growth_rows(rows, "new_installs"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handle", default="harrylabsj")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--baseline", action="store_true", help="Archive active snapshots and treat this run as a new baseline.")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    processed_dir = data_dir / "processed"
    analysis_path = processed_dir / f"{args.handle}_skill_analysis.csv"
    if not analysis_path.exists():
        analysis_path = processed_dir / f"{args.handle}_skills.csv"
    rows = read_csv(analysis_path)
    if not rows:
        raise RuntimeError(f"No rows found in {analysis_path}")

    collection_summary = read_json(data_dir / "raw" / f"{args.handle}_collection_summary.json")
    snapshot_dir = data_dir / "snapshots" / args.handle
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    baseline_id = snapshot_id_from(utc_now())
    archive_dir = archive_active_snapshots(snapshot_dir, f"baseline-reset-{baseline_id}") if args.baseline else None
    existing_paths = sorted(snapshot_files(snapshot_dir), key=snapshot_sort_key)
    previous = read_json(existing_paths[-1]) if existing_paths else None

    generated_at = utc_now_iso()
    snapshot_id, snapshot_path = unique_snapshot_path(snapshot_dir, snapshot_id_from(parse_iso(generated_at) or utc_now()))
    snapshot = build_snapshot(
        args.handle,
        rows,
        generated_at_utc=generated_at,
        snapshot_id=snapshot_id,
        collection_summary=collection_summary,
    )
    write_json(snapshot_path, snapshot)
    write_json(snapshot_dir / "latest.json", snapshot)

    growth = growth_rows(snapshot, previous)
    write_csv(processed_dir / f"{args.handle}_skill_growth.csv", growth)
    trend_summary = build_trend_summary(args.handle, snapshot, previous, growth, snapshot_count=len(existing_paths) + 1)
    trend_summary["baseline_reset"] = bool(args.baseline)
    trend_summary["archived_snapshot_dir"] = str(archive_dir) if archive_dir else ""
    write_json(processed_dir / f"{args.handle}_trend_summary.json", trend_summary)
    print(
        json.dumps(
            {
                "snapshot": str(snapshot_path),
                "has_previous": previous is not None,
                "baseline_reset": bool(args.baseline),
                "archived_snapshot_dir": str(archive_dir) if archive_dir else "",
                "deltas": trend_summary["deltas"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
