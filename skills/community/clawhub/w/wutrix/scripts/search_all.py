#!/usr/bin/env python3
# Copyright (c) 2025-2026 西安悟跃创想文化创意有限公司. All rights reserved.
# Proprietary software — see LICENSE at repo root.

"""Full-text search across wutrix vault (scenes + characters).

Usage:
    search_all.py --q 追车
    search_all.py --q 反派 --universe awakening_uni
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def main() -> None:
    parser = argparse.ArgumentParser(description="Search wutrix vault")
    parser.add_argument("--q", required=True, help="Query keyword")
    parser.add_argument("--universe", default=None)
    args = parser.parse_args()

    base_url = os.environ.get("INSPIRESTUDIO_URL")
    api_key = os.environ.get("INSPIRESTUDIO_API_KEY")
    if not base_url or not api_key:
        print(json.dumps({"ok": False, "error": "env not set"}, ensure_ascii=False))
        sys.exit(1)

    params = {"q": args.q}
    if args.universe:
        params["universe"] = args.universe

    url = base_url.rstrip("/") + "/api/search?" + urlencode(params)
    req = Request(url)
    req.add_header("X-API-Key", api_key)

    try:
        data = json.loads(urlopen(req, timeout=10).read())
        print(json.dumps({"ok": True, **data}, ensure_ascii=False))
    except HTTPError as e:
        print(json.dumps({
            "ok": False,
            "status": e.code,
            "error": e.reason,
        }, ensure_ascii=False))
        sys.exit(2)


if __name__ == "__main__":
    main()
