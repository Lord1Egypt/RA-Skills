"""Import X/Twitter cookies from browser export (Cookie-Editor format)."""

import json
import sys
from pathlib import Path

COOKIES_PATH = Path.home() / ".openclaw" / "credentials" / "x-cookies.json"


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: x_login.py <path-to-exported-cookies.json>\n\n"
            "Export cookies from your browser using Cookie-Editor extension\n"
            "while logged into x.com, then pass the file here.",
            file=sys.stderr,
        )
        sys.exit(1)

    source = Path(sys.argv[1])
    if not source.exists():
        print(f"File not found: {source}", file=sys.stderr)
        sys.exit(1)

    with open(source, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert Cookie-Editor array format to {name: value} dict
    if isinstance(data, list):
        cookies = {item["name"]: item["value"] for item in data}
    elif isinstance(data, dict):
        cookies = data
    else:
        print("Unrecognized cookie format.", file=sys.stderr)
        sys.exit(1)

    COOKIES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(COOKIES_PATH, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)

    print(f"Saved {len(cookies)} cookies to {COOKIES_PATH}")


if __name__ == "__main__":
    main()
