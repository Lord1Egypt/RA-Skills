#!/usr/bin/env python3
"""TwtAPI CLI — access real Twitter/X data from the command line."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://skill.twtapi.com"
SKILL_KEY = os.environ.get("TWTAPI_SKILL_KEY", "")
BASE_URL = os.environ.get("TWTAPI_SKILL_BASE_URL") or DEFAULT_BASE_URL
TIMEOUT = 30
USER_AGENT = "curl/8.7.1"


def _call(tool: str, params: dict | None = None) -> dict:
    if not SKILL_KEY:
        print("Error: TWTAPI_SKILL_KEY is not set. Get it from your TwtAPI dashboard.", file=sys.stderr)
        sys.exit(1)

    url = f"{BASE_URL.rstrip('/')}/api/v1/agent/invoke"
    payload = json.dumps(
        {
            "tool": tool,
            "params": params or {},
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "X-Skill-Key": SKILL_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read())
            if isinstance(data, dict) and "data" in data:
                return data["data"]
            return data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body)
            msg = err.get("msg") or err.get("message") or err.get("error") or body[:500]
        except Exception:
            msg = body[:500]

        hints = {
            401: "Invalid skill key.",
            402: "Insufficient credits.",
            429: "Rate limit exceeded. Wait a moment and retry.",
            502: "Upstream temporarily unavailable.",
        }
        print(f"Error: {hints.get(e.code, f'HTTP {e.code}')} — {msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: cannot connect to TwtAPI skill endpoint — {e.reason}", file=sys.stderr)
        sys.exit(1)


def _call_tools() -> dict:
    if not SKILL_KEY:
        print("Error: TWTAPI_SKILL_KEY is not set. Get it from your TwtAPI dashboard.", file=sys.stderr)
        sys.exit(1)

    url = f"{BASE_URL.rstrip('/')}/api/v1/agent/tools"
    req = urllib.request.Request(
        url,
        headers={
            "X-Skill-Key": SKILL_KEY,
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Error: HTTP {e.code} — {body[:500]}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: cannot connect to TwtAPI skill endpoint — {e.reason}", file=sys.stderr)
        sys.exit(1)


def _out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ── Subcommands ──────────────────────────────────────────────


def cmd_search(args: argparse.Namespace) -> None:
    params: dict = {"query": args.query}
    if args.count:
        params["count"] = args.count
    if args.type:
        params["search_type"] = args.type
    if args.cursor:
        params["cursor"] = args.cursor
    _out(_call("search_tweets", params))


def cmd_user(args: argparse.Namespace) -> None:
    _out(_call("get_user_by_username", {"screen_name": args.username}))


def cmd_user_by_id(args: argparse.Namespace) -> None:
    _out(_call("get_user_by_id", {"user_id": args.user_id}))


def cmd_tweets(args: argparse.Namespace) -> None:
    params: dict = {"user_id": args.user_id}
    if args.count:
        params["count"] = args.count
    if args.cursor:
        params["cursor"] = args.cursor
    _out(_call("get_user_tweets_by_id", params))


def cmd_replies(args: argparse.Namespace) -> None:
    params: dict = {"user_id": args.user_id}
    if args.count:
        params["count"] = args.count
    if args.cursor:
        params["cursor"] = args.cursor
    _out(_call("get_user_replies", params))


def cmd_media(args: argparse.Namespace) -> None:
    params: dict = {"user_id": args.user_id}
    if args.count:
        params["count"] = args.count
    if args.cursor:
        params["cursor"] = args.cursor
    _out(_call("get_user_media_by_id", params))


def cmd_followers(args: argparse.Namespace) -> None:
    params: dict = {"user_id": args.user_id}
    if args.count:
        params["count"] = args.count
    if args.cursor:
        params["cursor"] = args.cursor
    _out(_call("get_followers", params))


def cmd_following(args: argparse.Namespace) -> None:
    params: dict = {"user_id": args.user_id}
    if args.count:
        params["count"] = args.count
    if args.cursor:
        params["cursor"] = args.cursor
    _out(_call("get_following", params))


def cmd_tweet(args: argparse.Namespace) -> None:
    _out(_call("get_tweet_detail", {"tweet_id": args.tweet_id}))


def cmd_trending(args: argparse.Namespace) -> None:
    params: dict = {}
    if args.woeid is not None:
        params["woeid"] = args.woeid
    _out(_call("get_trending", params))


def cmd_tools(_: argparse.Namespace) -> None:
    _out(_call_tools())


# ── CLI ──────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="twtapi",
        description="Access real Twitter/X data. Requires TWTAPI_SKILL_KEY. The hosted TwtAPI skill gateway is built in.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    # tools
    s = sub.add_parser("tools", help="List available skill tools and verify auth/connectivity")
    s.set_defaults(func=cmd_tools)

    # search
    s = sub.add_parser("search", help="Search tweets by keyword or query")
    s.add_argument("query", help="Search query (supports Twitter search operators)")
    s.add_argument("--count", type=int, help="Number of results")
    s.add_argument("--type", choices=["Latest", "Top"], help="Search type (default: Latest)")
    s.add_argument("--cursor", help="Pagination cursor")
    s.set_defaults(func=cmd_search)

    # user
    s = sub.add_parser("user", help="Get user profile by username")
    s.add_argument("username", help="Twitter username (without @)")
    s.set_defaults(func=cmd_user)

    # user-by-id
    s = sub.add_parser("user-by-id", help="Get user profile by numeric ID")
    s.add_argument("user_id", help="Twitter user ID")
    s.set_defaults(func=cmd_user_by_id)

    # tweets
    s = sub.add_parser("tweets", help="Get tweets posted by a user")
    s.add_argument("user_id", help="Twitter user ID")
    s.add_argument("--count", type=int, help="Number of tweets (default: 20)")
    s.add_argument("--cursor", help="Pagination cursor")
    s.set_defaults(func=cmd_tweets)

    # replies
    s = sub.add_parser("replies", help="Get tweets and replies by a user")
    s.add_argument("user_id", help="Twitter user ID")
    s.add_argument("--count", type=int, help="Number of results (default: 20)")
    s.add_argument("--cursor", help="Pagination cursor")
    s.set_defaults(func=cmd_replies)

    # media
    s = sub.add_parser("media", help="Get media tweets from a user")
    s.add_argument("user_id", help="Twitter user ID")
    s.add_argument("--count", type=int, help="Number of results (default: 20)")
    s.add_argument("--cursor", help="Pagination cursor")
    s.set_defaults(func=cmd_media)

    # followers
    s = sub.add_parser("followers", help="Get followers of a user")
    s.add_argument("user_id", help="Twitter user ID")
    s.add_argument("--count", type=int, help="Number of followers (default: 20)")
    s.add_argument("--cursor", help="Pagination cursor")
    s.set_defaults(func=cmd_followers)

    # following
    s = sub.add_parser("following", help="Get accounts a user follows")
    s.add_argument("user_id", help="Twitter user ID")
    s.add_argument("--count", type=int, help="Number of results (default: 20)")
    s.add_argument("--cursor", help="Pagination cursor")
    s.set_defaults(func=cmd_following)

    # tweet
    s = sub.add_parser("tweet", help="Get full details of a single tweet")
    s.add_argument("tweet_id", help="Tweet ID")
    s.set_defaults(func=cmd_tweet)

    # trending
    s = sub.add_parser("trending", help="Get current trending topics")
    s.add_argument("--woeid", type=int, help="Where On Earth ID (default: 1 = Worldwide)")
    s.set_defaults(func=cmd_trending)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
