#!/usr/bin/env python3
# Copyright (c) 2025-2026 西安悟跃创想文化创意有限公司. All rights reserved.
# Proprietary software — see LICENSE at repo root.

"""Save an idea to wutrix inbox.

Usage:
    save_idea.py --text "灵感内容"
    save_idea.py --text "灵感内容" --source feishu

向后兼容策略：
- 优先调新版 /api/inbox/add（返回 JSON，不 redirect，2026-05 wutrix
  v1.5.1+ 提供）
- 404 时 fallback 到旧版 /inbox/add（form-urlencoded，会 303 redirect
  到 /inbox 浏览页）—— fallback 时禁用 redirect 不让 urllib 跟到那里
  撞 LoginMiddleware

这样无论客户 wutrix 升级到 v1.5.1+ 与否，skill 都能工作。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import (
    HTTPRedirectHandler,
    Request,
    build_opener,
    urlopen,
)


class _NoRedirect(HTTPRedirectHandler):
    """Block urllib auto-following 303 → /inbox（撞登录页就完了）。
    303 会被当作 HTTPError 上抛，调用方按 status code 判断成功。"""
    def redirect_request(self, *args, **kwargs):
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Save an idea to wutrix inbox")
    parser.add_argument("--text", required=True, help="Idea content (raw)")
    parser.add_argument("--source", default="feishu",
                        help="Origin tag (default: feishu)")
    args = parser.parse_args()

    base_url = os.environ.get("INSPIRESTUDIO_URL")
    api_key = os.environ.get("INSPIRESTUDIO_API_KEY")
    if not base_url or not api_key:
        print(json.dumps({
            "ok": False,
            "error": "env INSPIRESTUDIO_URL or INSPIRESTUDIO_API_KEY missing"
        }, ensure_ascii=False))
        sys.exit(1)

    base = base_url.rstrip("/")

    # ── 路径 1：先试新 endpoint /api/inbox/add（JSON, no redirect）─────────
    try:
        body_json = json.dumps({"source": args.source, "raw_text": args.text}).encode("utf-8")
        req = Request(base + "/api/inbox/add", data=body_json, method="POST")
        req.add_header("X-API-Key", api_key)
        req.add_header("Content-Type", "application/json")
        resp = urlopen(req, timeout=10)
        payload = json.loads(resp.read().decode("utf-8", "replace"))
        print(json.dumps({
            "ok": True,
            "status": resp.status,
            "id": payload.get("id"),
            "message": payload.get("message") or "已记入灵感箱",
        }, ensure_ascii=False))
        return
    except HTTPError as e:
        if e.code != 404:
            # 真错（401 / 500 / 等），不 fallback —— 让用户看到具体错
            print(json.dumps({
                "ok": False, "status": e.code, "error": e.reason,
                "body": e.read().decode("utf-8", "replace")[:500],
            }, ensure_ascii=False))
            sys.exit(2)
        # 404 = 老 wutrix backend 没这路由，fallback 旧路径
    except URLError as e:
        print(json.dumps({"ok": False, "error": str(e.reason)}, ensure_ascii=False))
        sys.exit(3)

    # ── 路径 2：fallback 旧 endpoint /inbox/add（form, 303 redirect）─────
    try:
        body_form = urlencode({"source": args.source, "raw_text": args.text}).encode()
        req = Request(base + "/inbox/add", data=body_form, method="POST")
        req.add_header("X-API-Key", api_key)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        opener = build_opener(_NoRedirect())
        opener.open(req, timeout=10)
        # urllib 不会到这里 —— 旧路由 303 会被 _NoRedirect 转成 HTTPError
        print(json.dumps({
            "ok": True, "status": 200,
            "message": "已记入灵感箱（legacy /inbox/add）",
        }, ensure_ascii=False))
    except HTTPError as e:
        if e.code in (200, 303):
            # 303 是旧路由的成功信号（redirect 到 /inbox 浏览页）
            print(json.dumps({
                "ok": True, "status": e.code,
                "message": "已记入灵感箱（legacy /inbox/add）",
            }, ensure_ascii=False))
        else:
            print(json.dumps({
                "ok": False, "status": e.code, "error": e.reason,
                "body": e.read().decode("utf-8", "replace")[:500],
            }, ensure_ascii=False))
            sys.exit(2)
    except URLError as e:
        print(json.dumps({"ok": False, "error": str(e.reason)}, ensure_ascii=False))
        sys.exit(3)


if __name__ == "__main__":
    main()
