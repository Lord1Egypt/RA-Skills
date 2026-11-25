#!/usr/bin/env python3
"""LinkDigest daily brief (每日稿) from the command line. Standard library only.

add / list / run / pause / resume / delete manage watches (POST/GET/PATCH/DELETE
/api/v1/watch); draft searches a topic once and writes a post from it
(/api/v1/search with digest + draft); checkup reads your own notes into a page
with a draft of the next one (/api/v1/digest/batch with synthesis + draft).
Needs LINKDIGEST_API_KEY. Prints JSON for the agent; the post as text.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("LINKDIGEST_BASE_URL", "https://linkdigest.dev").rstrip("/")
UA = "linkdigest-openclaw-skill-daily-draft/1.0.0"


def key() -> str:
    k = os.environ.get("LINKDIGEST_API_KEY", "").strip()
    if not k.startswith("ld_live_"):
        sys.exit("Set LINKDIGEST_API_KEY (ld_live_...). Create one at https://linkdigest.dev/signin?ref=skill-xiaohongshu-daily-draft&next=/app/keys")
    return k


def call(method: str, path: str, body: dict | None = None, timeout: int = 170) -> tuple[int, dict]:
    data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={
        "Authorization": "Bearer " + key(), "Content-Type": "application/json", "User-Agent": UA,
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except Exception:  # noqa: BLE001
            return e.code, {"error": str(e)}


def show(status: int, body: dict) -> None:
    print(json.dumps(body, ensure_ascii=False, indent=2))
    if status >= 400:
        if body.get("offer_zh"):
            print("\n" + body["offer_zh"], file=sys.stderr)
        sys.exit(1)


def wait_batch(batch_id: str) -> dict:
    for _ in range(60):
        status, b = call("GET", f"/api/v1/digest/batch/{batch_id}")
        if status >= 400:
            show(status, b)
        if b.get("status") == "done":
            return b
        time.sleep(10)
    sys.exit("the batch is still running; GET /api/v1/digest/batch/" + batch_id)


def print_post(b: dict) -> None:
    d = b.get("draft")
    print(f"\n[{b.get('done')} read, {b.get('failed')} failed, {b.get('skipped') or 0} replaced, {b.get('credits_total')} credits]")
    for r in b.get("ranked") or []:
        print(f"  {r['rank']}. 热度 {r['heat']} · 赞 {r['likes']} 收藏 {r['collects']} 评论 {r['comments']} · {r['title']}")
    if not d:
        print("\n(no draft on this batch)")
        return
    print(f"\n=== 成稿 (made_by: {d.get('made_by')}, cut: {d.get('cut')}) ===")
    for i, t in enumerate(d.get("titles") or [], 1):
        print(f"标题 {i}: {t}")
    print()
    print(d.get("body", ""))
    print()
    print(" ".join("#" + t for t in d.get("hashtags") or []))
    if d.get("cover_text"):
        print(f"封面文字: {d['cover_text']}")
    print("\n发布由你自己点。")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="watch a topic")
    a.add_argument("query")
    a.add_argument("--platform", choices=["xiaohongshu", "douyin"], default="xiaohongshu")
    a.add_argument("--voice", default=None, help="a note or two of your own writing; the post matches its tone")
    a.add_argument("--hour-utc", type=int, default=None, help="delivery hour, UTC (1 = 09:00 Beijing)")
    a.add_argument("--reads", type=int, default=None, help="posts one run reads, 1-20 (default 5; more posts, more credits)")
    sub.add_parser("list", help="the account's watches")
    for name in ("run", "pause", "resume", "delete"):
        s = sub.add_parser(name)
        s.add_argument("watch_id")
    d = sub.add_parser("draft", help="search a topic once and write a post from it")
    d.add_argument("query")
    d.add_argument("--platform", choices=["xiaohongshu", "douyin"], default="xiaohongshu")
    d.add_argument("--voice", default=None)
    d.add_argument("--limit", type=int, default=5)
    c = sub.add_parser("checkup", help="read your own notes into a page with a draft of the next one")
    c.add_argument("urls", nargs="+")
    c.add_argument("--voice", default=None)
    args = p.parse_args()

    if args.cmd == "add":
        body = {"query": args.query, "platform": args.platform, "draft_platform": args.platform}
        if args.voice:
            body["voice"] = args.voice
        if args.hour_utc is not None:
            body["hour_utc"] = args.hour_utc
        if args.reads is not None:
            body["reads"] = max(1, min(20, args.reads))
        show(*call("POST", "/api/v1/watch", body))
    elif args.cmd == "list":
        show(*call("GET", "/api/v1/watch"))
    elif args.cmd in ("run", "pause", "resume"):
        patch = {"run_now": True} if args.cmd == "run" else {"status": "paused" if args.cmd == "pause" else "active"}
        show(*call("PATCH", f"/api/v1/watch/{args.watch_id}", patch))
    elif args.cmd == "delete":
        show(*call("DELETE", f"/api/v1/watch/{args.watch_id}"))
    elif args.cmd == "draft":
        body = {"query": args.query, "platform": args.platform, "limit": max(1, min(10, args.limit)), "digest": True, "draft": True}
        if args.voice:
            body["voice"] = args.voice
        status, r = call("POST", "/api/v1/search", body)
        if status >= 400 or not r.get("batch_id"):
            show(status, r)
        print(f"search: {len(r.get('results') or [])} posts, {r.get('credits')} credits; batch {r['batch_id']}")
        print_post(wait_batch(r["batch_id"]))
    elif args.cmd == "checkup":
        body = {"urls": args.urls[:5], "synthesis": True, "draft": True, "platform": "xiaohongshu", "partial_ok": True, "label": "账号体检"}
        if args.voice:
            body["voice"] = args.voice
        status, r = call("POST", "/api/v1/digest/batch", body)
        if status >= 400 or not r.get("batch_id"):
            show(status, r)
        print(f"batch {r['batch_id']}")
        print_post(wait_batch(r["batch_id"]))


if __name__ == "__main__":
    main()
