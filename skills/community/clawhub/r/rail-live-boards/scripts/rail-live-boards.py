#!/usr/bin/env python3
"""Rail live board helper using the Rail Data API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_TEMPLATE = (
    "https://api1.raildata.org.uk/"
    "1010-live-arrival-and-departure-boards-arr-and-dep1_1/"
    "LDBWS/api/20220120/GetArrDepBoardWithDetails/{crs}"
)

TOKEN = os.environ.get("RAILDATA_API_KEY") or os.environ.get("NATIONAL_RAIL_TOKEN", "")

STATIONS = [
    ("PAD", "London Paddington"),
    ("EUS", "London Euston"),
    ("KGX", "London Kings Cross"),
    ("STP", "London St Pancras International"),
    ("VIC", "London Victoria"),
    ("WAT", "London Waterloo"),
    ("CHX", "London Charing Cross"),
    ("LST", "London Liverpool Street"),
    ("FST", "London Fenchurch Street"),
    ("MYB", "London Marylebone"),
    ("BHM", "Birmingham New Street"),
    ("BHI", "Birmingham International"),
    ("MAN", "Manchester Piccadilly"),
    ("MCV", "Manchester Victoria"),
    ("LDS", "Leeds"),
    ("EDB", "Edinburgh Waverley"),
    ("GLC", "Glasgow Central"),
    ("GLQ", "Glasgow Queen Street"),
    ("BRI", "Bristol Temple Meads"),
    ("BPW", "Bristol Parkway"),
    ("LIV", "Liverpool Lime Street"),
    ("NCL", "Newcastle"),
    ("SHF", "Sheffield"),
    ("NOT", "Nottingham"),
    ("CBG", "Cambridge"),
    ("OXF", "Oxford"),
    ("RDG", "Reading"),
    ("BTN", "Brighton"),
    ("SOU", "Southampton Central"),
    ("PLY", "Plymouth"),
    ("EXD", "Exeter St Davids"),
    ("YRK", "York"),
    ("PBO", "Peterborough"),
    ("DID", "Didcot Parkway"),
    ("SWI", "Swindon"),
    ("CLJ", "Clapham Junction"),
    ("CRE", "Crewe"),
    ("COV", "Coventry"),
    ("WVH", "Wolverhampton"),
    ("LUT", "Luton"),
    ("LTN", "Luton Airport Parkway"),
    ("STN", "Stansted Airport"),
    ("GTW", "Gatwick Airport"),
    ("LGW", "London Gatwick Airport"),
    ("SRA", "Stratford"),
    ("HHE", "Heathrow Airport"),
    ("GDP", "Gidea Park"),
    ("ROM", "Romford"),
]


def fetch_board(crs: str) -> dict:
    if not TOKEN:
        raise SystemExit(
            "Error: RAILDATA_API_KEY not set "
            "(NATIONAL_RAIL_TOKEN also accepted as a fallback)."
        )

    url = API_TEMPLATE.format(crs=urllib.parse.quote(crs.upper()))
    request = urllib.request.Request(
        url,
        headers={
            "x-apikey": TOKEN,
            "Accept": "application/json",
            "User-Agent": "curl/8.5.0",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        raise SystemExit(
            json.dumps(
                {
                    "error": f"HTTP {exc.code}: {exc.reason}",
                    "body": body,
                },
                indent=2,
            )
        ) from exc
    except urllib.error.URLError as exc:
        raise SystemExit(json.dumps({"error": str(exc.reason)}, indent=2)) from exc


def search_stations(query: str) -> list[dict]:
    q = query.lower().strip()
    matches = []
    for crs, name in STATIONS:
        if q in crs.lower() or q in name.lower():
            matches.append({"crsCode": crs, "stationName": name})
    return matches


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Query National Rail live board data via the Rail Data API."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("board", "departures", "arrivals"):
        p = sub.add_parser(name)
        p.add_argument("crs")
        p.add_argument("--rows", type=int, default=None)

    p_search = sub.add_parser("search")
    p_search.add_argument("query", nargs="+")

    args = parser.parse_args()

    if args.command == "search":
        print(json.dumps(search_stations(" ".join(args.query)), indent=2))
        return

    data = fetch_board(args.crs)

    if args.rows is not None and isinstance(data.get("trainServices"), list):
        data["trainServices"] = data["trainServices"][: args.rows]

    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
