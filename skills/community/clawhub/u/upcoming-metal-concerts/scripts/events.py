#!/usr/bin/env python3
"""Scrape upcoming metal concerts from concerts-metal.com and accumulate to data/concerts.json."""

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

BROADCAST_URL = (
    "https://broadcast.concerts-metal.com/"
    "ie-998_000000_FF0000_b_ces__{country}.html"
)

COUNTRIES = {
    "AR": "Argentina", "AU": "Australia", "AT": "Austria", "BE": "Belgium",
    "BR": "Brazil", "BG": "Bulgaria", "CA": "Canada", "CL": "Chile",
    "CN": "China", "CO": "Colombia", "HR": "Croatia", "CZ": "Czech-Republic",
    "DK": "Denmark", "EE": "Estonia", "FI": "Finland", "FR": "France",
    "DE": "Germany", "GR": "Greece", "HU": "Hungary", "IS": "Iceland",
    "IN": "India", "ID": "Indonesia", "IE": "Ireland", "IL": "Israel",
    "IT": "Italy", "JP": "Japan", "LV": "Latvia", "LT": "Lithuania",
    "LU": "Luxembourg", "MY": "Malaysia", "MX": "Mexico", "NL": "Netherlands",
    "NZ": "New-Zealand", "NO": "Norway", "PE": "Peru", "PH": "Philippines",
    "PL": "Poland", "PT": "Portugal", "RO": "Romania", "RU": "Russia",
    "RS": "Serbia", "SG": "Singapore", "SK": "Slovakia", "SI": "Slovenia",
    "ZA": "South-Africa", "KR": "South-Korea", "ES": "Spain", "SE": "Sweden",
    "CH": "Switzerland", "TW": "Taiwan", "TH": "Thailand", "TR": "Turkey",
    "UA": "Ukraine", "GB": "United-Kingdom", "US": "United-States",
    "UY": "Uruguay", "VE": "Venezuela",
}

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONCERTS_FILE = DATA_DIR / "concerts.json"
CONFIG_FILE = BASE_DIR / "skill-config.json"

DEFAULT_CONFIG = {
    "country": "ES",
    "concert_days": 200,
}


def load_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return dict(DEFAULT_CONFIG)


def init_config() -> dict:
    """Create skill-config.json with defaults if it doesn't exist."""
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
            f.write("\n")
    return load_config()


def fetch_html(country_name: str) -> str:
    url = BROADCAST_URL.format(country=country_name)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    })
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


def parse_events(html: str) -> list[dict]:
    events = []
    blocks = html.split("row align-items-center")[1:]

    for block in blocks:
        # Event name
        title_match = re.search(r'itemprop="url" title="([^"]+)"', block)
        name = title_match.group(1) if title_match else ""

        # Event URL
        url_match = re.search(
            r'href="(https://en\.concerts-metal\.com/concert_[^"]+)"', block
        )
        url = url_match.group(1).replace("?i=1", "") if url_match else ""

        # Date and venue/city
        date_match = re.search(
            r'(\d{2}/\d{2}/\d{4}) @ (.+?)<br', block, re.DOTALL
        )
        if not date_match:
            continue

        raw_date = date_match.group(1)
        # Convert DD/MM/YYYY to YYYY-MM-DD
        day, month, year = raw_date.split("/")
        date = f"{year}-{month}-{day}"

        venue_city_raw = date_match.group(2)
        # Extract venue name (may be a link or plain text)
        venue_link = re.search(r'>([^<]+)</a>', venue_city_raw)
        # City is after the last >, or after comma
        city_match = re.search(r',\s*(.+)$', venue_city_raw)
        city = city_match.group(1).strip() if city_match else ""
        city = re.sub(r'<[^>]+>', '', city).strip()

        if venue_link:
            venue = venue_link.group(1).strip()
        else:
            # No link — venue might be plain text before comma
            plain = re.sub(r'<[^>]+>', '', venue_city_raw)
            parts = plain.split(",", 1)
            venue = parts[0].strip() if len(parts) > 1 else ""

        # Artists from <li> entries
        artists = []
        for li_match in re.finditer(
            r'<li>.*?<a\s+title="([^"]+)"[^>]*>[^<]*</a>\s*(.*?)</li>',
            block, re.DOTALL,
        ):
            artists.append(li_match.group(1).strip())

        events.append({
            "date": date,
            "artists": artists,
            "venue": venue,
            "city": city,
            "url": url,
        })

    return events


def load_existing() -> dict[str, dict]:
    """Load existing concerts keyed by URL for dedup."""
    if CONCERTS_FILE.exists():
        with open(CONCERTS_FILE) as f:
            return {c["url"]: c for c in json.load(f)}
    return {}


def save_concerts(concerts: dict[str, dict]) -> None:
    """Write merged concerts to data/concerts.json."""
    DATA_DIR.mkdir(exist_ok=True)
    with open(CONCERTS_FILE, "w") as f:
        json.dump(list(concerts.values()), f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    config = init_config()

    parser = argparse.ArgumentParser(
        description="Collect upcoming metal concerts from concerts-metal.com"
    )
    parser.add_argument(
        "--country", default=config["country"],
        help=f"ISO country code (e.g. ES, DE, US, GB). Default from config: {config['country']}",
    )
    parser.add_argument(
        "--list-countries", action="store_true",
        help="List supported country codes and exit",
    )
    args = parser.parse_args()

    if args.list_countries:
        for code, name in sorted(COUNTRIES.items()):
            print(f"  {code}  {name}")
        return

    code = args.country.upper()
    country_name = COUNTRIES.get(code)
    if not country_name:
        print(f"Error: Unknown country code '{code}'.", file=sys.stderr)
        print("Use --list-countries to see supported codes.", file=sys.stderr)
        sys.exit(1)

    days = config["concert_days"]
    cutoff = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        html = fetch_html(country_name)
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} fetching {country_name} page.", file=sys.stderr)
        sys.exit(1)

    scraped = parse_events(html)

    # Filter to events within the lookahead window
    scraped = [e for e in scraped if today <= e["date"] <= cutoff]

    # Merge with existing data (dedup by URL) and detect cancellations
    existing = load_existing()
    now = datetime.now().isoformat()
    scraped_urls = {e["url"] for e in scraped}

    # Check existing concerts for cancellations or reappearances
    cancelled_count = 0
    for concert in existing.values():
        if concert["url"] in scraped_urls:
            concert["status"] = "active"
        elif today <= concert["date"] <= cutoff:
            if concert.get("status") != "cancelled":
                cancelled_count += 1
            concert["status"] = "cancelled"

    # Add newly-scraped concerts
    for event in scraped:
        if event["url"] not in existing:
            event["discovered_at"] = now
            event["status"] = "active"
            existing[event["url"]] = event

    save_concerts(existing)
    print(f"Saved {len(existing)} concerts to {CONCERTS_FILE}")
    if cancelled_count:
        print(f"Flagged {cancelled_count} concert(s) as potentially cancelled")


if __name__ == "__main__":
    main()
