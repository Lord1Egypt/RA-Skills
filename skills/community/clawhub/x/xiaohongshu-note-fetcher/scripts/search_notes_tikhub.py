#!/usr/bin/env python3
"""Call TikHub Xiaohongshu search_notes endpoint safely."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen


APP_V2_API_URL = "https://api.tikhub.io/api/v1/xiaohongshu/app_v2/search_notes"
WEB_API_URL = "https://api.tikhub.io/api/v1/xiaohongshu/web/search_notes"

SORT_TYPES = {
    "general",
    "time_descending",
    "popularity_descending",
    "comment_descending",
    "collect_descending",
    "english_preferred",
}

NOTE_TYPE_MAP = {
    "all": "不限",
    "video": "视频笔记",
    "image": "普通笔记",
    "live": "直播笔记",
    "不限": "不限",
    "视频笔记": "视频笔记",
    "普通笔记": "普通笔记",
    "直播笔记": "直播笔记",
}

TIME_FILTER_MAP = {
    "all": "不限",
    "day": "一天内",
    "week": "一周内",
    "half_year": "半年内",
    "不限": "不限",
    "一天内": "一天内",
    "一周内": "一周内",
    "半年内": "半年内",
}


def normalize_note_type(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    key = value.strip()
    if not key:
        return None
    return NOTE_TYPE_MAP.get(key, key)


def normalize_time_filter(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    key = value.strip()
    if not key:
        return None
    return TIME_FILTER_MAP.get(key, key)


def build_params(args: argparse.Namespace) -> Dict[str, str]:
    params: Dict[str, str] = {"keyword": args.keyword, "page": str(args.page)}

    # For first page requests, keep params minimal by default.
    first_page = args.page == 1 and not args.search_id and not args.search_session_id
    if first_page and not args.force_all_params:
        if args.sort_type and args.sort_type != "general":
            params["sort_type"] = args.sort_type
        if args.note_type:
            note_type = normalize_note_type(args.note_type)
            if note_type and note_type != "不限":
                params["note_type"] = note_type
        if args.time_filter:
            time_filter = normalize_time_filter(args.time_filter)
            if time_filter and time_filter != "不限":
                params["time_filter"] = time_filter
        if args.source and args.source != "explore_feed":
            params["source"] = args.source
        if args.ai_mode is not None and args.ai_mode != 0:
            params["ai_mode"] = str(args.ai_mode)
        return params

    # Pagination or force-all mode.
    if args.sort_type:
        params["sort_type"] = args.sort_type
    if args.note_type:
        params["note_type"] = normalize_note_type(args.note_type) or "不限"
    if args.time_filter:
        params["time_filter"] = normalize_time_filter(args.time_filter) or "不限"
    if args.search_id:
        params["search_id"] = args.search_id
    if args.search_session_id:
        params["search_session_id"] = args.search_session_id
    if args.source:
        params["source"] = args.source
    if args.ai_mode is not None:
        params["ai_mode"] = str(args.ai_mode)
    return params


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Xiaohongshu notes via TikHub API.")
    parser.add_argument("--token", help="TikHub bearer token. Can be omitted when --token-file is provided.")
    parser.add_argument("--token-file", help="File containing TikHub bearer token.")
    parser.add_argument("--keyword", required=True, help="Search keyword.")
    parser.add_argument("--page", type=int, default=1, help="Page number, start from 1.")
    parser.add_argument("--sort-type", default="general", choices=sorted(SORT_TYPES))
    parser.add_argument("--note-type", default="不限", help="all/video/image/live or Chinese enum.")
    parser.add_argument("--time-filter", default="不限", help="all/day/week/half_year or Chinese enum.")
    parser.add_argument("--search-id", default="", help="search_id from first response for pagination.")
    parser.add_argument("--search-session-id", default="", help="search_session_id from first response.")
    parser.add_argument("--source", default="explore_feed")
    parser.add_argument("--ai-mode", type=int, choices=[0, 1], default=0)
    parser.add_argument("--endpoint", choices=["app_v2", "web"], default="app_v2", help="TikHub endpoint family.")
    parser.add_argument(
        "--auth-mode",
        choices=["bearer", "apikey"],
        default="bearer",
        help="Use Authorization: Bearer <token> or custom API key header.",
    )
    parser.add_argument(
        "--auth-header",
        default="X-API-KEY",
        help="Header name used when --auth-mode apikey, default X-API-KEY.",
    )
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds.")
    parser.add_argument("--force-all-params", action="store_true", help="Always send all query params.")
    parser.add_argument("--output", default="", help="Optional path to save full JSON response.")
    args = parser.parse_args()

    if args.page < 1:
        parser.error("--page must be >= 1")

    token = args.token
    if args.token_file:
        token = Path(args.token_file).read_text(encoding="utf-8").strip()
    if not token:
        parser.error("Provide --token or --token-file")

    params = build_params(args)
    base_url = APP_V2_API_URL if args.endpoint == "app_v2" else WEB_API_URL
    # web endpoint expects sort/noteType; app_v2 expects sort_type/note_type.
    if args.endpoint == "web":
        if "sort_type" in params:
            params["sort"] = params.pop("sort_type")
        if "note_type" in params:
            params["noteType"] = params.pop("note_type")

    url = f"{base_url}?{urlencode(params)}"
    if args.auth_mode == "bearer":
        headers = {"Authorization": f"Bearer {token}"}
    else:
        headers = {args.auth_header: token}
    req = Request(url, headers=headers, method="GET")

    with urlopen(req, timeout=args.timeout) as resp:
        payload = resp.read().decode("utf-8", errors="replace")

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print(payload)
        return 0

    if args.output:
        Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
