#!/usr/bin/env python3
"""Find out what evidence this machine can actually read, before concluding it cannot.

Usage: python probe_sources.py [--market <name>] [--json]

WHY THIS EXISTS. Twice in one delivered plan the author concluded a whole class of evidence was
unavailable, wrote that into the artifact, and was wrong both times:

  * "restaurant ratings and hours cannot be obtained" — after probing an OpenRice *listing* page,
    which shows review counts and price bands and no hours. The *detail* page carries opening
    hours per day, the full address and the walking time from the nearest station. The half that
    was reachable is the half that matters: a wrong rating is a disappointment, a wrong opening
    time is a traveller standing at a closed door.
  * "accommodation prices and guest scores cannot be obtained" — after probing Booking.com, which
    answers automated requests with a challenge page. hk.trip.com had already been probed as
    reachable in the same session and was never asked for content; its detail pages carry the
    guest score with its scale, the review count, the nightly rate with its currency, the distance
    to the nearest station, and the text of recent negative reviews.

Both conclusions reached the traveller as "this environment cannot do it". Neither was a property
of the environment. The cost is not embarrassment: an agent that gives up early ships an
intermediate artifact where a booking-ready plan was possible, and the traveller cannot tell the
difference between "nobody could" and "nobody tried the second URL".

WHAT THIS DOES NOT DO. It reports reachability, not extractability, and the difference is the whole
lesson above. A 200 means the host answered this machine; it does not mean the page yields the
field you need, because most travel sites render their content with JavaScript that nothing here
executes. So every row is a candidate to try, never a promise -- and a class is only "unavailable"
after a DETAIL page for a real item has been read and come back without the field.

The list is deliberately small and deliberately incomplete. Availability differs by machine,
network and day; the point is to make probing cheap and repeatable, not to publish a provider
table that goes stale.
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

TIMEOUT = 12
UA = "travel-buddy-source-probe/1.0 (local planning environment)"

# (market, class, label, url, what a DETAIL page on this source is worth asking for)
CANDIDATES: list[tuple[str, str, str, str, str]] = [
    ("any", "encyclopaedia", "Wikipedia (zh)", "https://zh.wikipedia.org/wiki/香港",
     "coordinates, the article title a lookup needs, a lead image"),
    ("any", "encyclopaedia", "Wikipedia (en)", "https://en.wikipedia.org/wiki/Hong_Kong",
     "coordinates, Latin titles for image search"),
    ("any", "rates", "ECB reference rates", "https://open.er-api.com/v6/latest/HKD",
     "a dated FX rate, so money is converted rather than guessed"),
    ("hong_kong", "official", "HK Immigration", "https://www.immd.gov.hk/eng/index.html",
     "entry rules by nationality and residence status"),
    ("hong_kong", "official", "GovHK holidays", "https://www.gov.hk/en/about/abouthk/holiday/2027.htm",
     "public holidays, which change museum closure rules and crowding"),
    ("hong_kong", "official", "LCSD museums", "https://www.lcsd.gov.hk/en/index.html",
     "opening hours and the weekly closure day"),
    ("hong_kong", "operator", "MTR", "https://www.mtr.com.hk/en/customer/main/index.html",
     "lines, interchanges, fares"),
    ("hong_kong", "operator", "Star Ferry", "https://www.starferry.com.hk/en/service",
     "sailing hours, frequency by weekday, adult fare"),
    ("hong_kong", "dining", "OpenRice detail page", "https://www.openrice.com/en/hongkong",
     "PER-WEEKDAY opening hours, address, station walk, price band — try a DETAIL page, "
     "a listing page carries none of it"),
    ("hong_kong", "lodging", "Trip.com HK", "https://hk.trip.com/",
     "guest score WITH its scale, review count, nightly rate with currency, station distance, "
     "and the text of recent negative reviews — try a DETAIL page"),
    ("any", "lodging", "Booking.com", "https://www.booking.com/",
     "often answers automated requests with a challenge page: HTTP 200 or 202 with no content"),
    ("any", "reviews", "TripAdvisor", "https://www.tripadvisor.com/",
     "commonly refuses automated requests outright"),
    ("mainland_china", "maps", "Amap", "https://www.amap.com/",
     "the map provider this skill mandates for mainland routes"),
    ("mainland_china", "lodging", "Ctrip", "https://www.ctrip.com/", "rates and guest scores"),
    ("mainland_china", "rail", "12306", "https://www.12306.cn/index/", "rail services and fares"),
]


def probe(url: str) -> tuple[str, str]:
    """(status, note). Never raises: a probe that dies tells you less than one that reports."""
    # Two failures this probe reported about itself on its first run, both of which would have
    # been read as "the source is down" -- the exact mistake the file exists to prevent:
    #   * a non-ASCII path (zh.wikipedia.org/wiki/香港) raised UnicodeEncodeError before any
    #     request left the machine;
    #   * a host that closes the connection on a bare urllib handshake answered curl normally,
    #     so the honest report is "this probe could not, curl could", not "unreachable".
    safe = urllib.parse.urlsplit(url)
    url = urllib.parse.urlunsplit((
        safe.scheme, safe.netloc.encode("idna").decode("ascii"),
        urllib.parse.quote(safe.path), urllib.parse.quote(safe.query, safe="=&"), ""))
    request = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        "Accept-Language": "en,zh;q=0.9",
    })
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT,
                                    context=ssl.create_default_context()) as response:
            body = response.read(4096)
            code = response.getcode()
            if code == 200 and len(body) < 512:
                return str(code), "answered but returned almost nothing — likely a challenge page"
            return str(code), ""
    except urllib.error.HTTPError as exc:
        return str(exc.code), "refused this request" if exc.code in (401, 403, 429) else ""
    except Exception as exc:  # noqa: BLE001 - every failure shape is a result here
        # Named, not collapsed to "unreachable": a refused handshake, a DNS failure and a timeout
        # need different next moves, and one of them (a host that only rejects THIS client) is not
        # a statement about the source at all.
        return "unreachable", (f"{type(exc).__name__} from this client — try curl before "
                               f"concluding the source is down")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--market", default=None,
                        help="Only probe this market's sources plus the universal ones")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    rows = [c for c in CANDIDATES
            if args.market is None or c[0] in ("any", args.market)]
    results = []
    for market, kind, label, url, worth in rows:
        status, note = probe(url)
        reachable = status.isdigit() and status.startswith("2")
        results.append({"market": market, "class": kind, "source": label, "url": url,
                        "status": status, "reachable": reachable, "note": note,
                        "worth_asking_for": worth})

    if args.json:
        print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    else:
        for r in results:
            mark = "ok " if r["reachable"] else "-- "
            print(f"  {mark} {r['status']:>11}  {r['class']:<14} {r['source']}")
            if r["note"]:
                print(f"                    {r['note']}")
        classes = sorted({r["class"] for r in results if r["reachable"]})
        print(f"\n{sum(1 for r in results if r['reachable'])} of {len(results)} answered. "
              f"Classes with at least one reachable source: {', '.join(classes) or 'none'}.")

    print("\nA 200 is a candidate, not an answer. Before writing that a class of evidence is "
          "unavailable, open a DETAIL page for one real item on a reachable source and say which "
          "field came back empty. 'The listing page had no ratings' is not that sentence, and "
          "twice it has been written as though it were.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
