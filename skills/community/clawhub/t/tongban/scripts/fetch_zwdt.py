#!/usr/bin/env python3
"""Fetch public Shanghai "一网通办" municipal service item data."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar
from pathlib import Path

BASE = "https://zwdt.sh.gov.cn"
INDEX_URL = f"{BASE}/govPortals/index.do"
LIST_URL = f"{BASE}/govPortals/person.do"
DEFAULT_PAGE_SIZE = 100
USER_AGENT = "shanghai-service-guide/1.0 (+public-data-fetcher)"


def request_text(opener: urllib.request.OpenerDirector, url: str, data: dict[str, str] | None = None, retries: int = 3) -> str:
    body = None
    headers = {"User-Agent": USER_AGENT, "Referer": INDEX_URL}
    if data is not None:
        body = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    req = urllib.request.Request(url, data=body, headers=headers)
    for attempt in range(1, retries + 1):
        try:
            with opener.open(req, timeout=30) as response:
                return response.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == retries:
                raise RuntimeError(f"request failed for {url}: {exc}") from exc
            time.sleep(attempt)
    raise AssertionError("unreachable")


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def parse_departments(index_html: str) -> list[dict[str, str]]:
    departments: dict[str, dict[str, str]] = {}
    for match in re.finditer(
        r"<a(?P<attrs>[^>]+onclick=\"gotoOrganIndex\('(?P<code>[^']+)','(?P<name>[^']+)'\)\"[^>]*)>(?P<short>.*?)</a>",
        index_html,
        flags=re.S,
    ):
        attrs = match.group("attrs")
        code = match.group("code")
        data_code = re.search(r'data-code="([^"]+)"', attrs)
        data_name = re.search(r'data-name="([^"]+)"', attrs)
        if data_code and code != data_code.group(1):
            continue
        departments[code] = {
            "code": code,
            "name": clean_text(data_name.group(1) if data_name else match.group("name")),
            "short_name": clean_text(match.group("short")),
        }
    if not departments:
        raise RuntimeError("no departments found in index page")
    return sorted(departments.values(), key=lambda item: item["code"])


def fetch_items_for(
    opener: urllib.request.OpenerDirector,
    department: dict[str, str],
    role: str,
    page_limit: int | None,
    sleep_seconds: float,
) -> dict[str, object]:
    page = 1
    pages: list[dict[str, object]] = []
    total = None
    while True:
        payload = {
            "pageNumber": str(page),
            "pageSize": str(DEFAULT_PAGE_SIZE),
            "itemType": "",
            "orgCode": department["code"],
            "stRegion": "SH00SH",
            "category": "",
            "gfType": role,
            "stNet": "",
            "nmErrand": "",
            "sort": "",
            "feature": "",
            "stKeyword": "",
            "stIsShow": "Y",
        }
        text = request_text(opener, LIST_URL, payload)
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"invalid JSON for {department['code']} {role} page {page}: {text[:200]}") from exc
        total = int(data.get("count") or 0)
        pages.append(data)
        if page_limit is not None and page >= page_limit:
            break
        if page * DEFAULT_PAGE_SIZE >= total:
            break
        page += 1
        time.sleep(sleep_seconds)
    return {
        "department": department,
        "role": role,
        "total": total,
        "pages": pages,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Output raw JSON path")
    parser.add_argument("--sample", action="store_true", help="Fetch only two common departments")
    parser.add_argument("--page-limit", type=int, default=None, help="Maximum pages per department/role")
    parser.add_argument("--sleep", type=float, default=0.25, help="Seconds between list requests")
    args = parser.parse_args()

    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
    index_html = request_text(opener, INDEX_URL)
    departments = parse_departments(index_html)
    if args.sample:
        preferred = {"SHGASH", "SHGSSH"}
        departments = [dept for dept in departments if dept["code"] in preferred][:2]
    records = []
    for department in departments:
        for role in ("个人", "法人"):
            print(f"fetch {department['code']} {role}", file=sys.stderr)
            records.append(fetch_items_for(opener, department, role, args.page_limit, args.sleep))
            time.sleep(args.sleep)

    output = {
        "source": INDEX_URL,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "departments": departments,
        "records": records,
    }
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
