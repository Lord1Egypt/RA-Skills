"""Fetch X bookmarks via twikit and output JSON to stdout."""

import asyncio
import json
import sys
from pathlib import Path

from twikit import Client

COOKIES_PATH = Path.home() / ".openclaw" / "credentials" / "x-cookies.json"
PUSHED_PATH = Path.home() / ".openclaw" / "data" / "x-bookmarks-pushed.json"


def load_cookies(path: Path) -> dict:
    """Load cookies, converting Cookie-Editor format if needed."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return {item["name"]: item["value"] for item in data}
    return data


def load_pushed_ids() -> set:
    """Load IDs of previously pushed bookmarks."""
    if not PUSHED_PATH.exists():
        return set()
    with open(PUSHED_PATH, "r", encoding="utf-8") as f:
        return set(json.load(f))


async def main():
    show_all = "--all" in sys.argv
    folder_id = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--folder-id" and i + 1 < len(args):
            folder_id = args[i + 1]
            i += 2
        else:
            i += 1

    if not COOKIES_PATH.exists():
        print(
            f"X cookies not found. Export cookies from your browser to {COOKIES_PATH}",
            file=sys.stderr,
        )
        sys.exit(1)

    client = Client(language="en-US")
    client.set_cookies(load_cookies(COOKIES_PATH))

    bookmarks = await client.get_bookmarks(count=20, folder_id=folder_id)
    pushed_ids = load_pushed_ids()

    results = []
    for tweet in bookmarks:
        entry = {
            "id": tweet.id,
            "author": tweet.user.screen_name,
            "author_name": tweet.user.name,
            "text": tweet.full_text[:120],
            "url": f"https://x.com/{tweet.user.screen_name}/status/{tweet.id}",
        }
        if show_all:
            entry["already_pushed"] = tweet.id in pushed_ids
            results.append(entry)
        elif tweet.id not in pushed_ids:
            results.append(entry)

    json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    asyncio.run(main())
