#!/usr/bin/env python3
"""Query public X profiles, circles, followers, recaps, posts, and threads via https://xcircle.me."""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

BASE_URL = "https://xcircle.me"
MAX_BYTES = 4 * 1024 * 1024
HANDLE_RE = re.compile(r"^[A-Za-z0-9_]{1,15}$")
POST_ID_RE = re.compile(r"^[0-9]{1,24}$")


def parse_handle(raw: str) -> str:
    value = raw.strip().lstrip("@＠")
    if "://" in value or value.lower().startswith(("x.com/", "twitter.com/", "www.x.com/", "www.twitter.com/")):
        if "://" not in value:
            value = "https://" + value
        parsed = urlsplit(value)
        parts = [p for p in parsed.path.split("/") if p]
        value = parts[0].lstrip("@＠") if parts else ""
    if not HANDLE_RE.match(value):
        raise ValueError("Invalid public X handle. Expected 1-15 letters, digits, or underscores.")
    return value.lower()


def parse_post_ref(raw: str):
    value = raw.strip()
    if POST_ID_RE.match(value):
        return value, None
    if "://" not in value:
        value = "https://" + value
    parsed = urlsplit(value)
    host = (parsed.hostname or "").lower()
    if host not in ("x.com", "www.x.com", "mobile.x.com", "twitter.com", "www.twitter.com", "mobile.twitter.com"):
        raise ValueError("Provide a valid numeric status ID or x.com / twitter.com status URL.")
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) >= 3 and parts[1].lower() == "status" and POST_ID_RE.match(parts[2]):
        handle = parts[0] if HANDLE_RE.match(parts[0]) and parts[0].lower() != "i" else None
        return parts[2], handle
    if len(parts) >= 3 and parts[0].lower() == "i" and parts[1].lower() in ("status", "web") and POST_ID_RE.match(parts[-1]):
        return parts[-1], None
    raise ValueError("Could not extract status ID from URL.")


def call_api(path: str, payload: dict, timeout: int = 45) -> dict:
    req = Request(
        BASE_URL + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "XCircleSkill/1.0 (+https://xcircle.me/skill)",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read(MAX_BYTES + 1)
    except HTTPError as err:
        if err.code == 429:
            wait = err.headers.get("Retry-After", "10")
            raise RuntimeError(f"Rate limited by XCircle. Retry after {wait}s.") from err
        try:
            msg = json.loads(err.read(4096)).get("message", "request_failed")
        except Exception:
            msg = "request_failed"
        raise RuntimeError(f"XCircle HTTP {err.code}: {msg}") from err
    except URLError as err:
        raise RuntimeError(f"Network error contacting XCircle: {err.reason}") from err

    if len(raw) > MAX_BYTES:
        raise RuntimeError("Response exceeded safety size limit.")
    envelope = json.loads(raw)
    if not isinstance(envelope, dict) or envelope.get("code") != 0:
        raise RuntimeError(f"XCircle error: {envelope.get('message', 'unknown_error')}")
    return envelope.get("data") or {}


def main():
    parser = argparse.ArgumentParser(description="XCircle public X data helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_prof = sub.add_parser("profile", help="Lookup public X profile")
    p_prof.add_argument("handle")
    p_prof.add_argument("--json", action="store_true")

    p_circ = sub.add_parser("circle", help="Generate ranked interaction circle")
    p_circ.add_argument("handle")
    p_circ.add_argument("--count", type=int, choices=[8, 24, 50], default=24)
    p_circ.add_argument("--json", action="store_true")

    p_foll = sub.add_parser("followers", help="Read public followers or following")
    p_foll.add_argument("handle")
    p_foll.add_argument("--kind", choices=["followers", "following"], default="followers")
    p_foll.add_argument("--limit", type=int, default=100)
    p_foll.add_argument("--json", action="store_true")

    p_rec = sub.add_parser("recap", help="Generate 3-day or 7-day activity recap")
    p_rec.add_argument("handle")
    p_rec.add_argument("--days", type=int, choices=[3, 7], default=7)
    p_rec.add_argument("--json", action="store_true")

    p_post = sub.add_parser("post", help="Lookup a single public X post")
    p_post.add_argument("post")
    p_post.add_argument("--json", action="store_true")

    p_thr = sub.add_parser("thread", help="Export a connected public X thread")
    p_thr.add_argument("post")
    p_thr.add_argument("--markdown", action="store_true")
    p_thr.add_argument("--json", action="store_true")

    args = parser.parse_args()
    try:
        if args.cmd == "profile":
            data = call_api("/api/header/profile", {"handle": parse_handle(args.handle)}, timeout=20)
            if args.json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(f"@{data.get('handle')} ({data.get('name')})")
                print(f"Followers: {data.get('followers')} | Following: {data.get('following')}")
                if data.get("bio"):
                    print(f"Bio: {data.get('bio')}")
                if data.get("avatar"):
                    print(f"Avatar: {data.get('avatar')}")
        elif args.cmd == "circle":
            handle = parse_handle(args.handle)
            data = call_api("/api/circle", {"handle": handle}, timeout=50)
            people = (data.get("people") or [])[: args.count]
            if args.json:
                data["people"] = people
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                owner = data.get("owner") or {}
                print(f"Interaction Circle for @{owner.get('handle', handle)} ({len(people)} shown):")
                for idx, person in enumerate(people, 1):
                    print(f"  {idx:2d}. @{person.get('handle')} ({person.get('name')}) — score {person.get('score')}")
                print(f"Visual studio: {BASE_URL}/?handle={handle}")
        elif args.cmd == "followers":
            handle = parse_handle(args.handle)
            limit = max(1, min(400, args.limit))
            data = call_api("/api/followers-header", {"handle": handle, "kind": args.kind}, timeout=45)
            people = (data.get("people") or [])[:limit]
            if args.json:
                data["people"] = people
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                owner = data.get("owner") or {}
                print(f"Public {args.kind} for @{owner.get('handle', handle)} ({len(people)} of {data.get('totalCollected')}):")
                for idx, person in enumerate(people, 1):
                    print(f"  {idx:3d}. @{person.get('handle')} ({person.get('name')})")
                print(f"Header & MP4 studio: {BASE_URL}/x-followers-header?handle={handle}&kind={args.kind}")
        elif args.cmd == "recap":
            handle = parse_handle(args.handle)
            data = call_api("/api/recap", {"handle": handle, "days": args.days}, timeout=50)
            if args.json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                owner = data.get("owner") or {}
                summary = data.get("summary") or {}
                print(f"{args.days}-day X Recap for @{owner.get('handle', handle)}:")
                print(json.dumps(summary, indent=2, ensure_ascii=False))
                print(f"Recap studio: {BASE_URL}/x-recap?handle={owner.get('handle', handle)}")
        elif args.cmd == "post":
            post_id, handle = parse_post_ref(args.post)
            body = {"id": post_id}
            if handle:
                body["handle"] = handle
            data = call_api("/api/x-post/lookup", body, timeout=25)
            if args.json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                ts = datetime.fromtimestamp((data.get("createdAt") or 0) / 1000, tz=timezone.utc).isoformat()
                print(f"@{data.get('handle')} ({data.get('name')}) · {ts}")
                print(data.get("text", ""))
        elif args.cmd == "thread":
            post_id, _ = parse_post_ref(args.post)
            data = call_api("/api/x-thread", {"id": post_id}, timeout=30)
            if args.json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                posts = data.get("posts") or []
                print(f"# Thread by @{data.get('handle')} ({data.get('name')})\n")
                for idx, item in enumerate(posts, 1):
                    ts = datetime.fromtimestamp((item.get("createdAt") or 0) / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
                    print(f"## {idx}/{len(posts)} · {ts}\n\n{item.get('text', '')}\n")
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
