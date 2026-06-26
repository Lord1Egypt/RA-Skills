#!/usr/bin/env python3
"""Collect public ClawHub skill portfolio data for one publisher handle."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONVEX_QUERY_URL = "https://wry-manatee-359.convex.cloud/api/query"
SKILL_DETAIL_URL = "https://clawhub.ai/api/v1/skills/{slug}"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ms_to_iso(value: Any) -> str:
    if value in (None, ""):
        return ""
    try:
        return datetime.fromtimestamp(float(value) / 1000, timezone.utc).replace(microsecond=0).isoformat()
    except Exception:
        return ""


def request_json(
    url: str,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
    user_agent: str,
    retries: int = 3,
    timeout: int = 30,
) -> dict[str, Any]:
    data = None
    headers = {"User-Agent": user_agent, "Accept": "application/json"}
    if body is not None:
        data = json.dumps(body, separators=(",", ":")).encode("utf-8")
        headers["Content-Type"] = "application/json"
        headers["Convex-Client"] = "npm-1.40.0"

    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                payload = response.read().decode("utf-8")
            return json.loads(payload)
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code in {429, 500, 502, 503, 504} and attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
                continue
            try:
                detail = exc.read().decode("utf-8")
            except Exception:
                detail = ""
            raise RuntimeError(f"HTTP {exc.code} for {url}: {detail[:300]}") from exc
        except Exception as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
    raise RuntimeError(f"Request failed for {url}: {last_error}")


def convex_query(path: str, args: list[Any], *, user_agent: str) -> Any:
    response = request_json(
        CONVEX_QUERY_URL,
        method="POST",
        body={"path": path, "format": "convex_encoded_json", "args": args},
        user_agent=user_agent,
    )
    if response.get("status") != "success":
        raise RuntimeError(f"Convex query failed for {path}: {response}")
    return response.get("value")


def fetch_profile(handle: str, *, user_agent: str) -> dict[str, Any]:
    value = convex_query("publishers:getProfileByHandle", [{"handle": handle}], user_agent=user_agent)
    if not isinstance(value, dict):
        raise RuntimeError(f"Unexpected profile response: {value!r}")
    return value


def fetch_skill_list(handle: str, *, page_size: int, user_agent: str) -> list[dict[str, Any]]:
    skills: list[dict[str, Any]] = []
    cursor: str | None = None
    page_number = 0

    while True:
        page_number += 1
        args = {
            "handle": handle,
            "kind": "skill",
            "sort": "downloads",
            "paginationOpts": {"cursor": cursor, "numItems": page_size},
        }
        value = convex_query("publishers:listPublishedPage", [args], user_agent=user_agent)
        if not isinstance(value, dict):
            raise RuntimeError(f"Unexpected published page response: {value!r}")
        page = value.get("page") or []
        if not isinstance(page, list):
            raise RuntimeError(f"Unexpected page payload: {page!r}")
        skills.extend(page)
        print(f"Fetched page {page_number}: {len(page)} skills, total {len(skills)}", flush=True)
        if value.get("isDone"):
            break
        cursor = value.get("continueCursor")
        if cursor in (None, ""):
            raise RuntimeError(f"Pagination did not finish but no cursor was returned: {value}")
    return skills


def fetch_skill_detail(slug: str, *, user_agent: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(slug, safe="")
    return request_json(SKILL_DETAIL_URL.format(slug=encoded), user_agent=user_agent)


def fetch_skill_details(
    slugs: list[str],
    *,
    concurrency: int,
    user_agent: str,
) -> dict[str, dict[str, Any]]:
    details: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {executor.submit(fetch_skill_detail, slug, user_agent=user_agent): slug for slug in slugs}
        for index, future in enumerate(as_completed(futures), start=1):
            slug = futures[future]
            try:
                details[slug] = {"ok": True, "data": future.result()}
            except Exception as exc:
                details[slug] = {"ok": False, "error": str(exc)}
            if index % 50 == 0 or index == len(slugs):
                print(f"Fetched details: {index}/{len(slugs)}", flush=True)
    return details


def first_value(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return ""


def nested(data: dict[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return ""
        current = current.get(key)
    return current if current is not None else ""


def tags_to_text(tags: Any) -> tuple[int, str]:
    if isinstance(tags, dict):
        names = [str(key) for key, value in tags.items() if value is not False and value is not None]
    elif isinstance(tags, list):
        names = [str(item) for item in tags]
    elif isinstance(tags, str) and tags:
        names = [tags]
    else:
        names = []
    names = sorted({name.strip() for name in names if name.strip()})
    return len(names), "|".join(names)


def normalize_rows(
    handle: str,
    list_items: list[dict[str, Any]],
    detail_map: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in list_items:
        slug = str(first_value(item.get("slug"), item.get("name"), item.get("id"))).strip()
        wrapper = detail_map.get(slug, {})
        detail = wrapper.get("data") if wrapper.get("ok") else {}
        if not isinstance(detail, dict):
            detail = {}
        skill = detail.get("skill") if isinstance(detail.get("skill"), dict) else {}
        latest_version = detail.get("latestVersion") if isinstance(detail.get("latestVersion"), dict) else {}
        owner = detail.get("owner") if isinstance(detail.get("owner"), dict) else {}

        list_stats = item.get("stats") if isinstance(item.get("stats"), dict) else {}
        detail_stats = skill.get("stats") if isinstance(skill.get("stats"), dict) else {}
        stats = {**list_stats, **detail_stats}

        tag_count, tag_text = tags_to_text(first_value(skill.get("tags"), item.get("tags")))
        source = item.get("source") if isinstance(item.get("source"), dict) else {}

        row = {
            "handle": handle,
            "slug": slug,
            "display_name": first_value(skill.get("displayName"), item.get("displayName"), item.get("title"), slug),
            "summary": first_value(skill.get("summary"), item.get("summary")),
            "href": first_value(item.get("href"), f"/{handle}/{slug}" if slug else ""),
            "downloads": int(first_value(stats.get("downloads"), 0) or 0),
            "installs_all_time": int(first_value(stats.get("installsAllTime"), stats.get("installs"), 0) or 0),
            "installs_current": int(first_value(stats.get("installsCurrent"), 0) or 0),
            "stars": int(first_value(stats.get("stars"), 0) or 0),
            "comments": int(first_value(stats.get("comments"), 0) or 0),
            "versions": int(first_value(stats.get("versions"), 0) or 0),
            "created_at_ms": first_value(skill.get("createdAt"), item.get("createdAt")),
            "created_at_utc": ms_to_iso(first_value(skill.get("createdAt"), item.get("createdAt"))),
            "updated_at_ms": first_value(skill.get("updatedAt"), item.get("updatedAt")),
            "updated_at_utc": ms_to_iso(first_value(skill.get("updatedAt"), item.get("updatedAt"))),
            "latest_version": first_value(latest_version.get("version"), nested(item, "latestPublishedVersion", "version")),
            "latest_version_created_at_ms": first_value(
                latest_version.get("createdAt"), nested(item, "latestPublishedVersion", "createdAt")
            ),
            "latest_version_created_at_utc": ms_to_iso(
                first_value(latest_version.get("createdAt"), nested(item, "latestPublishedVersion", "createdAt"))
            ),
            "latest_changelog": first_value(latest_version.get("changelog"), nested(item, "latestPublishedVersion", "changelog")),
            "license": first_value(latest_version.get("license"), nested(item, "latestPublishedVersion", "license")),
            "tag_count": tag_count,
            "tags": tag_text,
            "source_repo": first_value(source.get("repo"), source.get("repository"), item.get("repo")),
            "source_path": first_value(source.get("path"), item.get("path")),
            "source_id": first_value(source.get("id"), item.get("sourceId")),
            "owner_handle": first_value(owner.get("handle"), handle),
            "detail_ok": bool(wrapper.get("ok")),
            "detail_error": "" if wrapper.get("ok") else wrapper.get("error", ""),
        }
        rows.append(row)
    return rows


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handle", default="harrylabsj")
    parser.add_argument("--out-dir", default="data")
    parser.add_argument("--page-size", type=int, default=200)
    parser.add_argument("--detail-concurrency", type=int, default=8)
    parser.add_argument("--skip-details", action="store_true")
    parser.add_argument("--user-agent", default="codex-clawhub-skill-maintainer/0.1")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    raw_dir = out_dir / "raw"
    processed_dir = out_dir / "processed"

    started_at = utc_now_iso()
    profile = fetch_profile(args.handle, user_agent=args.user_agent)
    skills = fetch_skill_list(args.handle, page_size=args.page_size, user_agent=args.user_agent)
    slugs = [str(first_value(item.get("slug"), item.get("name"), item.get("id"))).strip() for item in skills]
    slugs = [slug for slug in slugs if slug]

    if args.skip_details:
        detail_map = {}
    else:
        detail_map = fetch_skill_details(slugs, concurrency=args.detail_concurrency, user_agent=args.user_agent)

    rows = normalize_rows(args.handle, skills, detail_map)
    ended_at = utc_now_iso()
    collection_summary = {
        "handle": args.handle,
        "started_at_utc": started_at,
        "ended_at_utc": ended_at,
        "profile_skill_count": nested(profile, "stats", "skills"),
        "collected_skill_count": len(rows),
        "detail_success_count": sum(1 for value in detail_map.values() if value.get("ok")),
        "detail_error_count": sum(1 for value in detail_map.values() if not value.get("ok")),
    }

    write_json(raw_dir / f"{args.handle}_profile.json", profile)
    write_json(raw_dir / f"{args.handle}_skill_list.json", skills)
    write_json(raw_dir / f"{args.handle}_skill_details.json", detail_map)
    write_json(raw_dir / f"{args.handle}_collection_summary.json", collection_summary)
    write_csv(processed_dir / f"{args.handle}_skills.csv", rows)

    print(json.dumps(collection_summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
