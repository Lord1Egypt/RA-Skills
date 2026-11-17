#!/usr/bin/env python3
"""Collect a UTC calendar-month CI Tools digest without mutating GitLab."""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import urlencode


PROJECT = "xrow-public/ci-tools"
BASE = "projects/xrow-public%2Fci-tools"
PAGE_SIZE = 100


def instant(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("GitLab timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def utc(value):
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def month_window(month=None, *, now=None, allow_incomplete=False):
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).replace(microsecond=0)
    if month is None:
        end = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start = end.replace(year=end.year - 1, month=12) if end.month == 1 else end.replace(month=end.month - 1)
    else:
        if re.fullmatch(r"[0-9]{4}-(0[1-9]|1[0-2])", month) is None:
            raise ValueError("month must be YYYY-MM")
        start = datetime.strptime(month, "%Y-%m").replace(tzinfo=timezone.utc)
        end = start.replace(year=start.year + 1, month=1) if start.month == 12 else start.replace(month=start.month + 1)
    if start > now:
        raise ValueError("cannot collect a future month")
    if end > now and not allow_incomplete:
        raise ValueError("month is not complete; use --allow-incomplete only for an explicitly labelled preview")
    return start, end, min(now, end), now


def pages(endpoint, params):
    page = 1
    seen = set()
    while True:
        query = urlencode({**params, "per_page": PAGE_SIZE, "page": page})
        result = subprocess.run(
            ["glab", "api", f"{BASE}/{endpoint}?{query}"],
            check=True, capture_output=True, text=True, timeout=30,
        )
        batch = json.loads(result.stdout)
        if not isinstance(batch, list):
            raise ValueError(f"Unexpected GitLab response for {endpoint} page {page}")
        for item in batch:
            if not isinstance(item, dict):
                raise ValueError(f"Invalid GitLab record for {endpoint}")
            identity = item.get("tag_name") if endpoint == "releases" else item.get("iid")
            if identity is None or identity in seen:
                raise ValueError(f"Missing or repeated identity for {endpoint} page {page}")
            seen.add(identity)
        yield from batch
        if len(batch) < PAGE_SIZE:
            return
        page += 1


def collect(month=None, *, now=None, allow_incomplete=False):
    start, end, through, now = month_window(month, now=now, allow_incomplete=allow_incomplete)
    releases = []
    for item in pages("releases", {}):
        # Missing required timestamps fail closed rather than silently lowering counts.
        released_at = instant(item["released_at"])
        if start <= released_at < through:
            releases.append({
                "tag_name": item["tag_name"], "name": item.get("name"),
                "released_at": utc(released_at),
                "web_url": f"https://gitlab.com/{PROJECT}/-/releases/{item['tag_name']}",
            })
    merged = []
    # Do not set updated_before: a later edit must not hide a merge in this month.
    for item in pages("merge_requests", {"state": "merged", "updated_after": utc(start)}):
        merged_at = instant(item["merged_at"])
        if start <= merged_at < through:
            merged.append({
                "iid": item["iid"], "title": item["title"], "web_url": item["web_url"],
                "merged_at": utc(merged_at), "labels": item.get("labels", []),
            })
    # Open work is a separately dated current snapshot, not a historical month count.
    opened = [{
        "iid": item["iid"], "title": item["title"], "web_url": item["web_url"],
        "updated_at": utc(instant(item["updated_at"])), "labels": item.get("labels", []),
    } for item in pages("merge_requests", {"state": "opened"})]
    releases.sort(key=lambda item: item["released_at"])
    merged.sort(key=lambda item: (item["merged_at"], item["iid"]))
    opened.sort(key=lambda item: (item["updated_at"], item["iid"]), reverse=True)
    month = start.strftime("%Y-%m")
    return {
        "project": PROJECT, "month": month, "timezone": "UTC",
        "window_start_utc": utc(start), "window_end_utc": utc(end),
        "collected_through_utc": utc(through), "complete": end <= now,
        "output_path": f"docs/digest/digest-{month}.md",
        "suggested_branch": f"docs/digest-{month}",
        "counts": {"releases": len(releases), "merged_merge_requests": len(merged)},
        "releases": releases, "merged_merge_requests": merged,
        "open_merge_requests_as_of_utc": utc(now), "open_merge_requests": opened,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", help="UTC calendar month YYYY-MM; default: previous complete month")
    parser.add_argument("--allow-incomplete", action="store_true", help="allow a clearly marked month-to-date preview")
    args = parser.parse_args()
    try:
        data = collect(args.month, allow_incomplete=args.allow_incomplete)
    except (ValueError, KeyError, TypeError, AttributeError, OSError, subprocess.SubprocessError) as error:
        print(f"Unable to collect complete digest evidence: {error}", file=sys.stderr)
        return 1
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
