#!/usr/bin/env python3
# Copyright (c) 2025-2026 西安悟跃创想文化创意有限公司. All rights reserved.
# Proprietary software — see LICENSE at repo root.

"""List scenes of a wutrix project.

Usage:
    list_scenes.py --project 觉醒之战
    list_scenes.py --project 觉醒之战 --act 1
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


def main() -> None:
    parser = argparse.ArgumentParser(description="List scenes of a project")
    parser.add_argument("--project", required=True, help="Project name (中文 OK)")
    parser.add_argument("--act", default=None, help="Filter by act, e.g. '1'")
    parser.add_argument("--universe", default=None)
    args = parser.parse_args()

    base_url = os.environ.get("INSPIRESTUDIO_URL")
    api_key = os.environ.get("INSPIRESTUDIO_API_KEY")
    if not base_url or not api_key:
        print(json.dumps({"ok": False, "error": "env not set"}, ensure_ascii=False))
        sys.exit(1)

    url = base_url.rstrip("/") + f"/api/project/{quote(args.project)}/scenes"
    params = {}
    if args.act:
        params["act"] = args.act
    if args.universe:
        params["universe"] = args.universe
    if params:
        url += "?" + urlencode(params)

    req = Request(url)
    req.add_header("X-API-Key", api_key)
    try:
        data = json.loads(urlopen(req, timeout=10).read())
        print(json.dumps({"ok": True, "scenes": data}, ensure_ascii=False))
    except HTTPError as e:
        print(json.dumps({
            "ok": False,
            "status": e.code,
            "error": e.reason,
        }, ensure_ascii=False))
        sys.exit(2)


if __name__ == "__main__":
    main()
