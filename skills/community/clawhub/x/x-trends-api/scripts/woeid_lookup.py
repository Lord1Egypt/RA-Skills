#!/usr/bin/env python3
"""Look up WOEIDs by place name from the bundled woeid.json."""

import json
import sys
from pathlib import Path

DATA_PATH = Path(__file__).with_name("woeid.json")


def die(msg: str) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def load_places() -> list[dict]:
    try:
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        die(f"Failed to load {DATA_PATH}: {e}")
    if not isinstance(data, list):
        die("woeid.json is not a JSON array.")
    return data


def search(places: list[dict], query: str) -> list[dict]:
    query_lower = query.lower()
    results = []
    for p in places:
        if not isinstance(p, dict):
            continue
        name = p.get("name", "")
        country = p.get("country", "")
        if query_lower in name.lower() or query_lower in country.lower():
            results.append({
                "woeid": p.get("woeid"),
                "name": name,
                "country": country,
                "countryCode": p.get("countryCode"),
                "placeType": p.get("placeType", {}).get("name", ""),
            })
    return results


def main(argv: list[str]) -> None:
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print('Usage: python3 woeid_lookup.py "<place name>"', file=sys.stderr)
        sys.exit(0 if args else 1)

    query = " ".join(args).strip()
    if not query:
        die("No search query provided.")

    places = load_places()
    results = search(places, query)

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv)
