"""List X bookmark folders and output JSON to stdout."""

import asyncio
import json
import sys
from pathlib import Path

from twikit import Client

COOKIES_PATH = Path.home() / ".openclaw" / "credentials" / "x-cookies.json"


def load_cookies(path: Path) -> dict:
    """Load cookies, converting Cookie-Editor format if needed."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return {item["name"]: item["value"] for item in data}
    return data


async def main():
    if not COOKIES_PATH.exists():
        print(
            f"X cookies not found. Export cookies from your browser to {COOKIES_PATH}",
            file=sys.stderr,
        )
        sys.exit(1)

    client = Client(language="en-US")
    client.set_cookies(load_cookies(COOKIES_PATH))

    folders = await client.get_bookmark_folders()

    results = [{"id": folder.id, "name": folder.name} for folder in folders]

    json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    asyncio.run(main())
