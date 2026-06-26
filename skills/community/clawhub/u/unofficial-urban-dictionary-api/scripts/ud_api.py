#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.parse
import urllib.request

BASE = "https://unofficialurbandictionaryapi.com/api"


def bool_str(v):
    if v is None:
        return None
    return "true" if v else "false"


def get_json(path, params):
    query = {k: v for k, v in params.items() if v is not None}
    url = f"{BASE}{path}?{urllib.parse.urlencode(query)}"
    req = urllib.request.Request(url, headers={"User-Agent": "openclaw-ud-skill/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def parse_args():
    p = argparse.ArgumentParser(description="Unofficial Urban Dictionary API helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--limit", type=int)
    common.add_argument("--page", type=int)
    common.add_argument("--multi-page")

    s = sub.add_parser("search", parents=[common])
    s.add_argument("--term", required=True)
    s.add_argument("--strict", action="store_true")
    s.add_argument("--match-case", action="store_true")

    r = sub.add_parser("random", parents=[common])
    r.add_argument("--term")

    b = sub.add_parser("browse", parents=[common])
    b.add_argument("--character", required=True)
    b.add_argument("--term")

    a = sub.add_parser("author", parents=[common])
    a.add_argument("--term", required=True)

    d = sub.add_parser("date", parents=[common])
    d.add_argument("--term", required=True, help="Date string expected by API")

    return p.parse_args()


def main():
    args = parse_args()

    params = {
        "term": getattr(args, "term", None),
        "limit": args.limit,
        "page": args.page,
        "multiPage": args.multi_page,
    }

    if args.cmd == "search":
        path = "/search"
        params["strict"] = bool_str(args.strict)
        params["matchCase"] = bool_str(args.match_case)
    elif args.cmd == "random":
        path = "/random"
    elif args.cmd == "browse":
        path = "/browse"
        params["character"] = args.character
    elif args.cmd == "author":
        path = "/author"
    elif args.cmd == "date":
        path = "/date"
    else:
        print("Unknown command", file=sys.stderr)
        return 2

    try:
        data = get_json(path, params)
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, indent=2))
        return 1

    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
