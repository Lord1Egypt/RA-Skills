#!/usr/bin/env python3
# Copyright (c) 2025-2026 西安悟跃创想文化创意有限公司. All rights reserved.
# Proprietary software — see LICENSE at repo root.

"""List wutrix projects.

Usage:
    list_projects.py
    list_projects.py --universe awakening_uni
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
    parser = argparse.ArgumentParser(description="List wutrix projects")
    parser.add_argument("--universe", default=None,
                        help="Optional universe slug filter")
    args = parser.parse_args()

    base_url = os.environ.get("INSPIRESTUDIO_URL")
    api_key = os.environ.get("INSPIRESTUDIO_API_KEY")
    if not base_url or not api_key:
        print(json.dumps({"ok": False, "error": "env not set"}, ensure_ascii=False))
        sys.exit(1)

    url = base_url.rstrip("/") + "/api/projects"
    if args.universe:
        url += "?" + urlencode({"universe": args.universe})

    req = Request(url)
    req.add_header("X-API-Key", api_key)
    try:
        data = json.loads(urlopen(req, timeout=10).read())
        print(json.dumps({"ok": True, "projects": data}, ensure_ascii=False))
    except HTTPError as e:
        print(json.dumps({
            "ok": False,
            "status": e.code,
            "error": e.reason,
        }, ensure_ascii=False))
        sys.exit(2)


if __name__ == "__main__":
    main()
