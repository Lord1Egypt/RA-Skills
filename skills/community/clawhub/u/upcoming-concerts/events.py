#!/usr/bin/env python3
"""Query upcoming concerts/events from the Ticketmaster Discovery API."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

API_BASE = "https://app.ticketmaster.com/discovery/v2/events.json"


def fetch_events(params: dict) -> list[dict]:
    query = urllib.parse.urlencode(params)
    url = f"{API_BASE}?{query}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    if "_embedded" not in data:
        return []

    results = []
    seen = set()
    for event in data["_embedded"]["events"]:
        venues = event.get("_embedded", {}).get("venues", [])
        venue = venues[0] if venues else {}
        artists = [
            a["name"]
            for a in event.get("_embedded", {}).get("attractions", [])
        ]

        date = event.get("dates", {}).get("start", {}).get("localDate", "")
        name = event.get("name", "")
        venue_name = venue.get("name", "")

        dedup_key = (date, name, venue_name)
        if dedup_key in seen:
            continue
        seen.add(dedup_key)

        classifications = event.get("classifications", [{}])
        genre_info = classifications[0] if classifications else {}

        results.append({
            "date": date,
            "name": name,
            "artists": artists,
            "venue": venue_name,
            "city": venue.get("city", {}).get("name", ""),
            "country": venue.get("country", {}).get("countryCode", ""),
            "genre": genre_info.get("genre", {}).get("name", ""),
            "url": event.get("url", ""),
        })

    results.sort(key=lambda e: e["date"])
    return results


def main():
    parser = argparse.ArgumentParser(description="Search upcoming events")
    parser.add_argument("--city", help="City name")
    parser.add_argument("--country", help="ISO country code (e.g. ES, US, GB)")
    parser.add_argument("--artist", help="Artist or keyword filter")
    parser.add_argument("--genre", help="Genre (e.g. Metal, Rock, Jazz)")
    parser.add_argument("--from", dest="date_from", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="date_to", help="End date (YYYY-MM-DD)")
    parser.add_argument("--size", type=int, default=50, help="Max results (default 50)")
    args = parser.parse_args()

    api_key = os.environ.get("TICKETMASTER_API_KEY")
    if not api_key:
        print("Error: TICKETMASTER_API_KEY environment variable not set.", file=sys.stderr)
        print("Get a free key at https://developer.ticketmaster.com/", file=sys.stderr)
        sys.exit(1)

    date_from = args.date_from or datetime.now().strftime("%Y-%m-%d")
    date_to = args.date_to or (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")

    params = {
        "apikey": api_key,
        "classificationName": "music",
        "startDateTime": f"{date_from}T00:00:00Z",
        "endDateTime": f"{date_to}T23:59:59Z",
        "size": min(args.size, 200),
        "sort": "date,asc",
    }

    if args.city:
        params["city"] = args.city
    if args.country:
        params["countryCode"] = args.country
    if args.artist:
        params["keyword"] = args.artist
    if args.genre:
        params["classificationName"] = args.genre

    try:
        results = fetch_events(params)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Error: API returned {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

    json.dump(results, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
