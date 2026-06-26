#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

DEFAULT_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0e41994e-9e62-4713-ad69-fddeaaba8e9a"


def build_content(titles):
    lines = ["标题的列表："]
    lines.extend(f"{idx}. {title}" for idx, title in enumerate(titles, start=1))
    return "\n".join(lines)


def collect_titles(args):
    titles = list(args.title or [])
    if args.stdin:
        titles.extend(line.strip() for line in sys.stdin if line.strip())
    titles = [title.strip() for title in titles if title and title.strip()]
    return titles


def post_json(url, payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def main():
    parser = argparse.ArgumentParser(description="Push Baidu result titles to a WeCom webhook.")
    parser.add_argument("--title", action="append", default=[], help="Result title. Can be passed multiple times.")
    parser.add_argument("--stdin", action="store_true", help="Read titles from stdin, one title per line.")
    parser.add_argument("--webhook-url", default=os.environ.get("WECOM_WEBHOOK_URL", DEFAULT_WEBHOOK_URL), help="Override webhook URL.")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without sending.")
    args = parser.parse_args()

    titles = collect_titles(args)
    if not titles:
        print("No titles provided. Use --title or --stdin.", file=sys.stderr)
        return 2

    payload = {
        "msgtype": "text",
        "text": {
            "content": build_content(titles)
        }
    }

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    try:
        response_text = post_json(args.webhook_url, payload)
        print(response_text)
        try:
            response_json = json.loads(response_text)
        except json.JSONDecodeError:
            return 1
        return 0 if response_json.get("errcode") == 0 else 1
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        print(f"HTTPError: {e.code} {e.reason}\n{body}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
