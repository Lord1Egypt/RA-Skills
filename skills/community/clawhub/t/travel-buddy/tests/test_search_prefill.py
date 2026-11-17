#!/usr/bin/env python3
"""A search button carries what it declares -- for families, date-times, stations and cars.

The prefill rule compares every field a button declares prefilled with its URL, and counts a value
only when it is a discrete part of it. Four shapes a real trip produces broke it, found by pushing
a synthetic English self-drive family trip through the whole pipeline on 2026-09-24:

* A family of 2 adults and 2 children. Providers state a party as adults plus children --
  Booking's group_adults=2&group_children=2 -- and never as the total, so `guests: 4` could not be
  satisfied; dropping `guests` fails the renderer's hotel rule instead. The only way through was a
  URL searching for four adults, which hides family rooms.
* A `4` found inside `14:30` was reported as "only inside a free-text parameter".
* An ISO date-time (2026-10-17T08:00:00) was refused as free text.
* Rail cards were compared against origin_airport/destination_airport, which they do not carry,
  so their stations were never compared at all; rental-car searches were never compared either.

Run:  python tests/test_search_prefill.py
      python -m pytest tests/test_search_prefill.py
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_plan_consistency as cpc  # noqa: E402

FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def family_plan() -> dict:
    plan = json.loads(FIXTURE.read_text(encoding="utf-8"))
    plan["trip"]["traveler_count"] = 4
    # Only the hotel whose search each case rewrites books the family room; the other keeps its
    # own two-guest search, which stays correct and out of every assertion below.
    plan["booking_options"]["accommodations"][0]["guest_count"] = 4
    return plan


def findings(plan: dict, needle: str) -> list[str]:
    errors: list[str] = []
    cpc.check_booking_identity(plan, errors, [])
    return [e for e in errors if needle in e]


def with_hotel_search(url: str) -> dict:
    plan = family_plan()
    search = plan["booking_options"]["accommodations"][0]["comparison_searches"][0]
    search["search_url"] = url
    search["prefilled_fields"] = ["destination", "check_in", "check_out", "guests", "rooms"]
    return plan


def with_flight(url: str, fields: list[str]) -> dict:
    plan = family_plan()
    plan["booking_options"]["flights"] = [{
        "id": "flight-1", "provider": "KLM", "review_url": "https://www.klm.com/",
        "origin_airport": "AMS", "destination_airport": "EDI",
        "outbound_date": "2026-10-17", "return_date": "2026-10-20",
        "round_trip_search_url": url, "round_trip_prefilled_fields": fields}]
    return plan


def with_ground(url: str, fields: list[str], **over) -> dict:
    plan = family_plan()
    card = {"id": "rail-1", "provider": "LNER", "review_url": "https://www.lner.co.uk/",
            "origin_station": "Montreux", "destination_station": "Bern",
            "outbound_date": "2026-10-17", "return_date": "2026-10-20",
            "round_trip_search_url": url, "round_trip_prefilled_fields": fields}
    card.update(over)
    plan["booking_options"]["ground_transport"] = [card]
    return plan


def with_car(url: str) -> dict:
    plan = family_plan()
    plan["booking_options"]["rental_cars"] = [{
        "id": "car-1", "provider": "Hertz", "review_url": url,
        "pickup_location": "Edinburgh Waverley", "dropoff_location": "Edinburgh Waverley",
        "pickup_time": "2026-10-17 10:00", "dropoff_time": "2026-10-20 17:00",
        "rental_search_prefilled_fields": ["pickup_location", "dropoff_location", "pickup_time",
                                           "dropoff_time"]}]
    return plan


def main() -> int:
    # Families, however the provider spells a party.
    for provider, url in (
            ("Booking", "https://www.booking.com/searchresults.html?ss=Fixture+Hotel+A"
                        "&checkin=2026-09-28&checkout=2026-09-29&group_adults=2&group_children=2"
                        "&age=7&age=10&no_rooms=1"),
            ("Airbnb", "https://www.airbnb.com/s/Fixture/homes?checkin=2026-09-28"
                       "&checkout=2026-09-29&adults=2&children=2"),
            ("Expedia", "https://www.expedia.com/Hotel-Search?destination=Fixture"
                        "&startDate=2026-09-28&endDate=2026-09-29&adults=2&children=1_7%2C1_10"
                        "&rooms=1")):
        found = [e for e in findings(with_hotel_search(url), "'guests'") if "Hotel A" in e]
        check(f"a {provider} family search carries its party of four", not found, found)
    for provider, url in (
            ("Skyscanner", "https://www.skyscanner.net/transport/flights/ams/edi/261017/261020/"
                           "?adultsv2=2&childrenv2=7%7C10"),
            ("KAYAK", "https://www.kayak.com/flights/AMS-EDI/2026-10-17/2026-10-20/2adults/"
                      "children-7-10")):
        found = findings(with_flight(url, ["origin", "destination", "outbound_date", "return_date",
                                           "travellers"]), "'travellers'")
        check(f"a {provider} family flight search carries its party of four", not found, found)
    # A party that really is missing is still refused -- and not for being "free text" because a 4
    # happens to sit inside a date.
    found = [e for e in findings(with_hotel_search(
        "https://www.booking.com/searchresults.html?ss=Fixture&checkin=2026-10-14"
        "&checkout=2026-10-15&no_rooms=1"), "'guests'") if "Hotel A" in e]
    check("a search with no party is refused as not carrying it",
          found and "does not carry 4 at all" in found[0], found)
    found = [e for e in findings(with_hotel_search(
        "https://www.booking.com/searchresults.html?ss=Fixture&checkin=2026-09-28"
        "&checkout=2026-09-29&group_adults=2&no_rooms=1"), "'guests'") if "Hotel A" in e]
    check("two adults are not a party of four", found, "a partial party passed")
    # One party stated twice is still one party. A Booking link copied from the results carries the
    # party in two families -- group_* and req_* -- and summing every adult and child key counted a
    # family of four as eight, refusing the correct link. Expedia's multi-room list (adults=2,2) is
    # two rooms of two, which the digit test used to read as no party at all.
    for provider, url in (
            ("Booking, two parameter families", "https://www.booking.com/searchresults.html"
             "?ss=Fixture+Hotel+A&checkin=2026-09-28&checkout=2026-09-29&group_adults=2"
             "&group_children=2&age=7&age=10&no_rooms=1&req_adults=2&req_children=2&req_age=7"
             "&req_age=10"),
            ("Expedia, two rooms", "https://www.expedia.com/Hotel-Search?destination=Fixture"
             "&startDate=2026-09-28&endDate=2026-09-29&adults=2%2C2&rooms=2")):
        found = [e for e in findings(with_hotel_search(url), "'guests'") if "Hotel A" in e]
        check(f"{provider}: the party of four is read once", not found, found)
    found = [e for e in findings(with_hotel_search(
        "https://www.booking.com/searchresults.html?ss=Fixture&checkin=2026-09-28"
        "&checkout=2026-09-29&group_adults=2&req_adults=2&no_rooms=1"), "'guests'") if "Hotel A" in e]
    check("two families each saying two adults are not a party of four", found,
          "the two statements were added together")
    # A count and an age list are one statement of the same children, and rooms numbered 1, 2, ...
    # split one party. Probed 2026-09-24 on twelve providers' own formats: a link giving both the
    # number of children and their ages (Agoda children=2&childages=7,10; Qunar childNum with
    # childAge) read a family of four as six, and per-room parameters (Hilton's room1NumAdults /
    # room2NumAdults) read as two parties of two. Both refused a link that was right.
    for provider, url in (
            ("Agoda, count and ages", "https://www.agoda.com/search?city=1&checkIn=2026-09-28"
             "&los=1&rooms=1&adults=2&children=2&childages=7%2C10&textToSearch=Fixture+Hotel+A"),
            ("Agoda, camelCase ages", "https://www.agoda.com/search?city=1&checkIn=2026-09-28"
             "&los=1&rooms=1&adults=2&children=2&childAges=7%2C10&textToSearch=Fixture+Hotel+A"),
            ("Qunar, count and ages", "https://hotel.qunar.com/cn/fixture?fromDate=2026-09-28"
             "&toDate=2026-09-29&adultNum=2&childNum=2&childAge=7%2C10&q=Fixture+Hotel+A"),
            ("Hilton, one party in numbered rooms", "https://www.hilton.com/en/book/reservation/"
             "rooms/?ctyhocn=FIXHA&arrivalDate=2026-09-28&departureDate=2026-09-29"
             "&room1NumAdults=1&room1NumChildren=1&room2NumAdults=1&room2NumChildren=1"
             "&query=Fixture+Hotel+A"),
            ("Airbnb, an infant is one more guest", "https://www.airbnb.com/s/Fixture-Hotel-A/"
             "homes?checkin=2026-09-28&checkout=2026-09-29&adults=2&children=1&infants=1")):
        found = [e for e in findings(with_hotel_search(url), "'guests'") if "Hotel A" in e]
        check(f"{provider}: the party of four is read as four", not found, found)
    # From the fresh review: Skyscanner's childrenv2 is a list of ages even when it holds one
    # (childrenv2=7 is one child of seven, not seven children), and age lists kept per room
    # (childages1 / childages2) are different children, so they add up.
    for url, party in (("https://www.skyscanner.net/transport/flights/ams/edi/261017/?adultsv2=2"
                        "&childrenv2=7", 3),
                       ("https://hotel.example/search?adults1=2&adults2=2&childages1=7"
                        "&childages2=10", 6)):
        check(f"{url[:48]}... reads a party of {party}", party in cpc._party_sizes_in_url(url),
              cpc._party_sizes_in_url(url))

    # ISO date-times are one field.
    url = ("https://www.thetrainline.com/book/results?origin=Montreux&destination=Bern"
           "&outwardDate=2026-10-17T08%3A00%3A00&inwardDate=2026-10-20T17%3A00%3A00")
    found = findings(with_ground(url, ["origin", "destination", "outbound_date", "return_date"]),
                     "ground_transport 'LNER'")
    check("an ISO date-time counts as the date it starts with", not found, found)

    # Stations, by name or by the provider's own id.
    # One-way cards (return_date None), so each case is about its stations and nothing else.
    found = [e for e in findings(with_ground("https://www.sbb.ch/en?nach=Bern&datum=2026-10-17",
                                             ["origin", "destination", "outbound_date"],
                                             return_date=None), "ground_transport 'LNER'")
             if "'origin'" in e]
    check("a rail search without its origin station is refused", found, "origin never compared")
    found = findings(with_ground("https://www.sbb.ch/en?von=Z%C3%BCrich+HB&nach=Bern"
                                 "&datum=2026-10-17", ["origin", "destination", "outbound_date"],
                                 origin_station="Zürich HB", return_date=None),
                     "ground_transport 'LNER'")
    check("a multi-word station that is a whole query value is carried", not found, found)
    trainline = ("https://www.thetrainline.com/book/results?origin=urn%3Atrainline%3Ageneric%3A"
                 "loc%3A6386&destination=urn%3Atrainline%3Ageneric%3Aloc%3A5456"
                 "&outwardDate=2026-10-17T08%3A00%3A00")
    found = findings(with_ground(trainline, ["origin", "destination", "outbound_date"],
                                 origin_station="London Kings Cross",
                                 destination_station="Edinburgh Waverley", return_date=None),
                     "ground_transport 'LNER'")
    check("an id-keyed provider without declared ids is refused",
          any("'origin'" in e for e in found) and any("'destination'" in e for e in found), found)
    found = findings(with_ground(trainline, ["origin", "destination", "outbound_date"],
                                 origin_station="London Kings Cross",
                                 destination_station="Edinburgh Waverley",
                                 origin_station_id="urn:trainline:generic:loc:6386",
                                 destination_station_id="urn:trainline:generic:loc:5456",
                                 return_date=None),
                     "ground_transport 'LNER'")
    check("an id-keyed provider is carried by the ids the card declares", not found, found)

    # Rental cars.
    found = findings(with_car("https://www.hertz.com/"), "rental car")
    check("a rental search that is a bare home page is refused", found, "home page passed")
    found = findings(with_car("https://www.rentalcars.com/SearchResults.do?locationId=123"
                              "&puDay=17&puMonth=10&puYear=2026&doDay=20&doMonth=10&doYear=2026"),
                     "rental car")
    check("a rental search carrying split day/month/year passes", not found, found)
    found = findings(with_car("https://www.kayak.com/cars/Edinburgh-c123/2026-10-17-10h/"
                              "2026-10-20-17h"), "rental car")
    check("a rental search carrying both dates in its path passes", not found, found)
    found = findings(with_car("https://www.kayak.com/cars/Edinburgh-c123/2026-10-17-10h"),
                     "rental car")
    check("a rental search missing its return date is refused",
          any("dropoff_time" in e for e in found), found)

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("search prefill cases passed")
    return 0


def test_search_prefill() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
