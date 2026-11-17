#!/usr/bin/env python3
"""kiwi_flights.py: the Kiwi client, the card mapping, the search link and the CLI.

Kiwi.com's public MCP endpoint (https://mcp.kiwi.com) answers this machine where airline sites and
the usual comparison platforms answer with bot challenges, so it is the default flight source. The
behaviours pinned here were each observed on 2026-10-11: prices are party totals, the cheapest
default results were self-transfers, the booking link is an affiliate checkout page, and a search
page's title says whether its city slugs resolved. Every case runs offline against a stub transport
and tests/kiwi-responses-fixture.json; one live case runs only with TRAVEL_BUDDY_LIVE_KIWI=1.

Run:  python tests/test_kiwi_flights.py
      python -m pytest tests/test_kiwi_flights.py
"""

from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import kiwi_flights as kf  # noqa: E402

FIXTURE = json.loads((ROOT / "tests" / "kiwi-responses-fixture.json").read_text(encoding="utf-8"))

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


class StubTransport:
    """Answers the MCP handshake and replays one recorded tools/call result per call."""

    def __init__(self, results: list[dict] | None = None, fail: Exception | None = None,
                 raw: str | None = None):
        self.results = list(results or [])
        self.fail = fail
        self.raw = raw
        self.calls: list[dict] = []

    def __call__(self, url: str, body: dict, headers: dict, timeout: float) -> tuple[str, dict]:
        self.calls.append({"url": url, "body": body, "headers": headers})
        if self.fail:
            raise self.fail
        method = body.get("method")
        if method == "initialize":
            message = {"jsonrpc": "2.0", "id": body["id"], "result": {"serverInfo": {"name": "stub"}}}
            return "data: " + json.dumps(message) + "\n\n", {"Mcp-Session-Id": "s1"}
        if method == "notifications/initialized":
            return "", {}
        if self.raw is not None:
            return self.raw, {}
        if not self.results:
            # A search nobody recorded a result for: the code under test searched when it should
            # have refused. Raised as a network error so it surfaces as a named failed case
            # (KIWI UNAVAILABLE, exit 2) rather than as a crash inside the stub.
            raise OSError("the stub has no recorded result for this search")
        result = self.results.pop(0)
        return "data: " + json.dumps({"jsonrpc": "2.0", "id": body["id"], "result": result}) + "\n\n", {}


def client_cases() -> None:
    recorded = FIXTURE["ams_edi_2a2c_safe"]["result"]
    stub = StubTransport([recorded])
    payload = kf.KiwiClient(transport=stub).search({"flyFrom": "AMS"})
    check("search returns the structured result", payload.get("itineraries"), list(payload)[:5])
    tools = [c["body"].get("params", {}).get("name") for c in stub.calls if c["body"].get("method") == "tools/call"]
    check("only search-flight is ever called", tools == ["search-flight"], tools)
    check("the session id is carried after initialize",
          stub.calls[-1]["headers"].get("Mcp-Session-Id") == "s1", stub.calls[-1]["headers"])
    check("the client names itself", "travel-buddy/" in stub.calls[0]["headers"]["User-Agent"])
    check("the version comes from plugin.json", kf.skill_version() ==
          json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())["version"])

    # Text-only result (no structuredContent) is read from the text block.
    text_only = {"content": [{"type": "text", "text": json.dumps(recorded["structuredContent"])}]}
    check("a text-only result is parsed",
          kf.KiwiClient(transport=StubTransport([text_only])).search({}).get("itineraries"))

    for label, stub in (
        ("a network error", StubTransport(fail=OSError("unreachable"))),
        ("a non-JSON body", StubTransport(raw="<html>blocked</html>")),
        ("an error result", StubTransport([{"structuredContent": {"error": "rate limited", "itineraries": []}}])),
        ("itineraries not a list", StubTransport([{"structuredContent": {"itineraries": "nope"}}])),
    ):
        try:
            kf.KiwiClient(transport=stub).search({})
            failures.append(f"{label} must raise KiwiUnavailable")
        except kf.KiwiUnavailable as exc:
            check(f"{label} says why", str(exc).strip(), exc)


def seg(carrier, number, frm, to, dep, arr, city_from="Amsterdam", city_to="Edinburgh",
        country_from="Netherlands", country_to="United Kingdom", name="Carrier"):
    return {"carrier": carrier, "carrierName": name, "flightNumber": number, "from": frm, "to": to,
            "fromCity": city_from, "toCity": city_to, "fromCountry": country_from, "toCountry": country_to,
            "departureTime": dep, "arrivalTime": arr, "cabinClass": "economy"}


def itin(price, out_segs, in_segs, out_dur=5400, in_dur=6000, bags=(4, 0, 0)):
    def leg(segs, dur):
        return {"route": [segs[0]["from"]] + [s["to"] for s in segs], "departureTime": segs[0]["departureTime"],
                "arrivalTime": segs[-1]["arrivalTime"], "durationSeconds": dur, "stops": len(segs) - 1,
                "cabinClass": "economy", "segments": segs}
    return {"price": price, "priceFormatted": f"{price} EUR", "totalDurationSeconds": out_dur + in_dur,
            "bookingUrl": "https://kiwi.com/u/REDACTED",
            "baggage": {"personalItem": bags[0], "cabinBag": bags[1], "checkedBag": bags[2]},
            "outbound": leg(out_segs, out_dur), "inbound": leg(in_segs, in_dur)}


REQUEST = {"origin": "AMS", "destination": "EDI", "depart": "2026-11-20", "return": "2026-11-24",
           "adults": 2, "children": 2, "infants": 0, "cabin": None, "currency": "EUR", "language": "en"}
DIRECT = itin(733, [seg("U2", "U23302", "AMS", "EDI", "2026-11-20T21:55:00", "2026-11-20T22:25:00", name="easyJet")],
              [seg("U2", "U23301", "EDI", "AMS", "2026-11-24T07:20:00", "2026-11-24T10:00:00",
                   city_from="Edinburgh", city_to="Amsterdam", country_from="United Kingdom",
                   country_to="Netherlands", name="easyJet")])
KLM = itin(778, [seg("KL", "KL1287", "AMS", "EDI", "2026-11-20T09:10:00", "2026-11-20T09:40:00", name="KLM")],
           [seg("KL", "KL1290", "EDI", "AMS", "2026-11-24T12:05:00", "2026-11-24T14:40:00",
                city_from="Edinburgh", city_to="Amsterdam", country_from="United Kingdom",
                country_to="Netherlands", name="KLM")])
SELF_TRANSFER = itin(728, [seg("U2", "U23052", "AMS", "BFS", "2026-11-20T13:00:00", "2026-11-20T13:40:00", name="easyJet",
                               city_to="Belfast"),
                           seg("RK", "RK178", "BFS", "EDI", "2026-11-20T14:50:00", "2026-11-20T15:45:00", name="Ryanair UK",
                               city_from="Belfast")],
                     DIRECT["inbound"]["segments"], out_dur=13500)


def mapping_cases() -> None:
    safe = kf.search_arguments(REQUEST)
    check("protected connections are the default",
          all(safe.get(k) is False for k in ("allow_self_transfer", "allow_diff_airport_connection",
                                              "allow_overnight_stopovers")), safe)
    check("dates go out as dd/mm/yyyy", safe["departureDate"] == "20/11/2026" and safe["returnDate"] == "24/11/2026", safe)
    check("a permissive search allows them explicitly",
          kf.search_arguments(REQUEST, permissive=True).get("allow_self_transfer") is True)

    lines: list[str] = []
    codeshare = copy.deepcopy(DIRECT)
    codeshare["price"] = 790
    payload = {"itineraries": [codeshare, DIRECT, {"price": None, "outbound": {"segments": []}}, KLM]}
    usable = kf.usable_itineraries(payload, lines)
    check("an identical segment signature is one option, not two", len(usable) == 2, [u["price"] for u in usable])
    check("and the copy kept is the cheapest", usable[0]["price"] == 733, [u["price"] for u in usable])
    check("malformed_itinerary_is_skipped", any(l.startswith("SKIPPED") for l in lines), lines)

    merged = kf.mark_self_transfer([DIRECT, KLM], [SELF_TRANSFER, DIRECT, KLM])
    check("a permissive-only itinerary is marked", merged[0] is not None and merged[0].get("_self_transfer") is True
          and merged[0]["price"] == 728, [(m["price"], m.get("_self_transfer")) for m in merged])
    check("an itinerary the safe search also returned is not marked",
          not [m for m in merged if m["price"] == 733 and m.get("_self_transfer")])

    picked = kf.pick_candidates([DIRECT, KLM])
    check("two candidates: cheapest, then a different airline", [p["price"] for p in picked] == [733, 778])
    same = copy.deepcopy(DIRECT); same["price"] = 740
    check("a near-duplicate departure is not a second candidate", len(kf.pick_candidates([DIRECT, same])) == 1)

    card = kf.itinerary_to_card(DIRECT, REQUEST, 0, "2026-10-11", single=False)
    check("party total becomes a per-person price, rounded up", card["fare_low"] == 184 and card["fare_high"] == 184, card["fare_low"])
    check("the price note says it is an average with children", "733" in card["price_note"] and "children" in card["price_note"])
    out = card["outbound_itinerary"]
    check("flight number as the service identifier", out["service_identifier"] == "U23302", out)
    check("local times carry their date", out["departure_local"] == "2026-11-20 21:55" and out["arrival_local"] == "2026-11-20 22:25", out)
    check("duration in minutes", out["duration_minutes"] == 90, out)
    # The renderer already prints the stop count ("non-stop" / 直飞), so a direct leg's note is just
    # its route; printing "Direct" again read "直飞 · 直飞，AMS → EDI" on a real Chinese card.
    check("a direct leg's note is its route, not a second 'direct'", out["connection_or_terminal_note"] == "AMS → EDI", out)
    check("the card summarises both directions", card["connection_summary"] == "Direct both ways", card["connection_summary"])
    check("airports from the segments", card["origin_airport"] == "AMS" and card["destination_airport"] == "EDI")
    check("Kiwi is the comparison platform", card["comparison_platform"] == "Kiwi.com" and card["round_trip_search_provider"] == "Kiwi.com")
    check("researched now, per person round trip", card["price_status"] == "researched_current"
          and card["price_basis"] == "per_person_round_trip" and card["price_checked_at"] == "2026-10-11")
    check("baggage for the party", "4 personal" in card["baggage_assumption"], card["baggage_assumption"])
    for field in ("review_url", "material_conditions", "airport_transfer_note", "direct_provider", "direct_review_url"):
        check(f"{field} is left for the author", str(card.get(field, "")).startswith("TODO:"), card.get(field))
    check("no Kiwi booking link anywhere on the card", "kiwi.com/u/" not in json.dumps(card))

    risky = kf.itinerary_to_card(dict(SELF_TRANSFER, _self_transfer=True), REQUEST, 0, "2026-10-11", single=False)
    check("the connecting leg of a self-transfer is marked", risky["outbound_itinerary"].get("self_transfer") is True)
    check("its direct return is not", risky["return_itinerary"].get("self_transfer") is not True)
    check("the change is in the note", "BFS" in risky["outbound_itinerary"]["connection_or_terminal_note"])
    check("and in the summary", risky["connection_summary"] == "Outbound: 1 change; return: direct", risky["connection_summary"])

    infants = dict(REQUEST, adults=1, children=0, infants=1)
    baby = kf.itinerary_to_card(DIRECT, infants, 0, "2026-10-11", single=False)
    check("infants count in the per-person division", baby["fare_low"] == 367, baby["fare_low"])
    check("and are named in the price note", "infant" in baby["price_note"], baby["price_note"])
    check("adults only: no average note", "price_note" not in kf.itinerary_to_card(
        DIRECT, dict(REQUEST, adults=2, children=0), 0, "2026-10-11", single=False))

    zh = kf.itinerary_to_card(DIRECT, dict(REQUEST, language="zh"), 0, "2026-10-11", single=True)
    check("Chinese plans get Chinese notes", zh["connection_summary"] == "往返均为直飞"
          and "儿童" in zh["price_note"], zh["connection_summary"])
    check("a lone candidate says why", zh.get("single_option_reason"))
    # Kiwi writes the cabin capitalised ("Economy", every one of 214 recorded legs); a Chinese
    # card printed it in English until the lookup ignored case.
    recorded = FIXTURE["ams_edi_2a2c_safe"]["result"]["structuredContent"]["itineraries"][0]
    zh_recorded = kf.itinerary_to_card(recorded, dict(REQUEST, language="zh"), 0, "2026-10-11", single=False)
    check("Kiwi's capitalised cabin is translated", zh_recorded["cabin"] == "经济舱", zh_recorded["cabin"])

    # The recorded responses map without raising, and every card is per person.
    for key in ("ams_edi_2a2c_safe", "ams_hkg_1a_safe"):
        payload = FIXTURE[key]["result"]["structuredContent"]
        args = FIXTURE[key]["arguments"]
        request = dict(REQUEST, adults=args.get("adults", 1), children=args.get("children", 0))
        cards = [kf.itinerary_to_card(i, request, n, "2026-10-11", single=False)
                 for n, i in enumerate(kf.pick_candidates(kf.usable_itineraries(payload, [])))]
        check(f"the recorded {key} response maps", cards and all(c["fare_low"] > 0 for c in cards), key)


class FakePage:
    def __init__(self, body: str):
        self.body = body.encode("utf-8")

    def read(self) -> bytes:
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def opener_with(title_by_slug: dict[str, str], seen: list[str], headers: list[dict] | None = None):
    def opener(request, timeout=30.0):
        url = request.full_url
        seen.append(url)
        if headers is not None:
            headers.append(dict(request.header_items()))
        for slug, title in title_by_slug.items():
            if slug in url:
                return FakePage(f"<html><head><title>{title}</title></head></html>")
        return FakePage("<html><head><title>Kiwi.com | Find Cheap Flights &amp; Discover New Destinations</title></head></html>")
    return opener


def link_cases() -> None:
    check("slugs fold accents and spaces", kf.slugify("Zürich") == "zurich" and kf.slugify("New York") == "new-york")
    url = kf.search_page_url(DIRECT, REQUEST)
    check("the slug form, the dates, the party",
          url == "https://www.kiwi.com/en/search/results/amsterdam-netherlands/edinburgh-united-kingdom/"
                 "2026-11-20/2026-11-24?adults=2&children=2", url)

    check("a resolved title confirms", kf.title_confirms("Amsterdam‎ – Edinburgh‎ trips", "Amsterdam", "Edinburgh"))
    check("accented_title_verifies", kf.title_confirms("Amsterdam – Zürich trips", "Amsterdam", "Zurich"))
    check("the empty-form title does not", not kf.title_confirms("–  trips", "Amsterdam", "Edinburgh"))
    check("the home-page title does not",
          not kf.title_confirms("Kiwi.com | Find Cheap Flights & Discover New Destinations", "Amsterdam", "Edinburgh"))
    check("another city does not", not kf.title_confirms("Amsterdam – Glasgow trips", "Amsterdam", "Edinburgh"))
    check("no title does not", not kf.title_confirms(None, "Amsterdam", "Edinburgh"))

    cards = [kf.itinerary_to_card(DIRECT, REQUEST, 0, "2026-10-11", single=False),
             kf.itinerary_to_card(KLM, REQUEST, 1, "2026-10-11", single=False)]
    lines: list[str] = []
    seen: list[str] = []
    sent: list[dict] = []
    kf.attach_search_link(cards, DIRECT, REQUEST, lines,
                          opener=opener_with({"edinburgh-united-kingdom": "Amsterdam – Edinburgh trips"}, seen, sent))
    check("a verified page becomes the search button", cards[0]["round_trip_search_url"] == url, cards[0]["round_trip_search_url"])
    check("the page's own place ids make origin and destination checkable",
          cards[0].get("origin_place_id") == "amsterdam-netherlands"
          and cards[0].get("destination_place_id") == "edinburgh-united-kingdom", cards[0])
    check("so all five fields are declared, each confirmed by the gate",
          cards[0]["round_trip_prefilled_fields"] == ["origin", "destination", "outbound_date", "return_date", "travellers"],
          cards[0]["round_trip_prefilled_fields"])
    # Two options that open the same page are one option shown twice
    # (check_plan_consistency.check_booking_identity), so the Kiwi page is the first card's only.
    check("the second card does not reuse the first card's search page",
          cards[1]["round_trip_search_url"] != url and cards[1]["round_trip_search_url"].startswith("TODO:")
          and "another" in cards[1]["round_trip_search_url"], cards[1]["round_trip_search_url"])
    check("the verification is reported", any(l.startswith("LINK VERIFIED") for l in lines), lines)
    check("the browser user agent is used", sent and "Chrome/" in sent[0].get("User-agent", ""), sent)

    cards = [kf.itinerary_to_card(DIRECT, REQUEST, 0, "2026-10-11", single=False)]
    lines = []
    kf.attach_search_link(cards, DIRECT, REQUEST, lines, opener=opener_with({}, []))
    check("an unverified page stays TODO", cards[0]["round_trip_search_url"].startswith("TODO:"), cards[0]["round_trip_search_url"])
    check("and says which URL failed", any(l.startswith("LINK NOT VERIFIED") and "kiwi.com" in l for l in lines), lines)

    def broken(request, timeout=30.0):
        raise OSError("down")
    cards = [kf.itinerary_to_card(DIRECT, REQUEST, 0, "2026-10-11", single=False)]
    kf.attach_search_link(cards, DIRECT, REQUEST, [], opener=broken)
    check("a fetch error leaves TODO", cards[0]["round_trip_search_url"].startswith("TODO:"))

    with_infant = dict(REQUEST, adults=1, children=0, infants=1)
    cards = [kf.itinerary_to_card(DIRECT, with_infant, 0, "2026-10-11", single=False)]
    kf.attach_search_link(cards, DIRECT, with_infant, [],
                          opener=opener_with({"edinburgh-united-kingdom": "Amsterdam – Edinburgh trips"}, []))
    check("with an infant, the party is never declared prefilled",
          "travellers" not in cards[0]["round_trip_prefilled_fields"], cards[0]["round_trip_prefilled_fields"])


import contextlib
import io
import tempfile


def run(argv, results=None, titles=None, today="2026-10-11"):
    stub = StubTransport([{"structuredContent": r} for r in (results or [])])
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = kf.main(argv + ["--today", today], client=kf.KiwiClient(transport=stub),
                       opener=opener_with(titles or {}, []))
    return code, out.getvalue(), stub


ARGS = ["--from", "AMS", "--to", "EDI", "--depart", "2026-11-20", "--return", "2026-11-24",
        "--adults", "2", "--children", "2", "--currency", "EUR"]


def plan_file(tmp: str, **trip) -> Path:
    plan = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))
    plan["trip"].update({"traveler_count": 4, "currency": "EUR", "language": "en",
                         "start_date": "2026-11-20", "end_date": "2026-11-24"}, **trip)
    path = Path(tmp) / "plan.json"
    path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    return path


def cli_cases() -> None:
    code, out, _ = run(ARGS, results=[{"itineraries": [DIRECT, KLM]}],
                       titles={"edinburgh-united-kingdom": "Amsterdam – Edinburgh trips"})
    check("a search prints cards and exits 0", code == 0 and '"fl-kiwi-1"' in out and "NEXT:" in out, out[-500:])

    code, out, stub = run(ARGS, results=[{"itineraries": []}])
    check("no results is exit 3", code == 3 and "KIWI NO RESULTS" in out, out[-300:])

    stub = StubTransport(fail=OSError("down"))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        code = kf.main(ARGS + ["--today", "2026-10-11"], client=kf.KiwiClient(transport=stub), opener=opener_with({}, []))
    check("unavailable is exit 2", code == 2 and "KIWI UNAVAILABLE" in buf.getvalue(), buf.getvalue()[-300:])

    for label, bad in (("depart before today", ["--depart", "2026-10-01"]),
                       ("return before depart", ["--return", "2026-11-19"]),
                       ("not a date", ["--depart", "20/11/2026"]),
                       ("more infants than adults", ["--adults", "1", "--children", "0", "--infants", "2"])):
        argv = list(ARGS)
        for i in range(0, len(bad), 2):
            if bad[i] in argv:
                argv[argv.index(bad[i]) + 1] = bad[i + 1]
            else:
                argv += bad[i:i + 2]
        code, out, stub = run(argv)
        check(f"bad_dates_refused: {label}", code == 1 and "ERROR:" in out and not stub.calls, out[-300:])

    with tempfile.TemporaryDirectory() as tmp:
        path = plan_file(tmp, traveler_count=3)
        before = path.read_text(encoding="utf-8")
        code, out, stub = run(ARGS + ["--into", str(path)])
        check("mismatch_refused_before_network: party", code == 1 and not stub.calls
              and path.read_text(encoding="utf-8") == before, out[-300:])
        path = plan_file(tmp, currency="GBP")
        code, out, stub = run(ARGS + ["--into", str(path)])
        check("mismatch_refused_before_network: currency", code == 1 and not stub.calls, out[-300:])
        # The renderer refuses a flight whose dates are not the trip's first and last day, so the
        # script refuses first, before spending a search on cards that cannot be saved.
        path = plan_file(tmp, start_date="2026-11-21", end_date="2026-11-24")
        code, out, stub = run(ARGS + ["--into", str(path)])
        check("mismatch_refused_before_network: dates", code == 1 and not stub.calls
              and "start_date" in out, out[-300:])

        path = plan_file(tmp)
        before_plan = json.loads(path.read_text(encoding="utf-8"))
        code, out, _ = run(ARGS + ["--into", str(path)], results=[{"itineraries": [DIRECT, KLM]}],
                           titles={"edinburgh-united-kingdom": "Amsterdam – Edinburgh trips"})
        written = json.loads(path.read_text(encoding="utf-8"))
        check("--into writes the flight cards", code == 0 and len(written["booking_options"]["flights"]) == 2, out[-400:])
        check("and a source record", any(s.get("name") == "Kiwi.com flight search" for s in written["sources"]))
        check("and nothing else in the plan moved",
              {k: v for k, v in written.items() if k not in ("booking_options", "sources")} ==
              {k: v for k, v in before_plan.items() if k not in ("booking_options", "sources")})
        check("other booking options are untouched",
              {k: v for k, v in written["booking_options"].items() if k != "flights"} ==
              {k: v for k, v in before_plan["booking_options"].items() if k != "flights"})

        path.write_text(json.dumps(written), encoding="utf-8")
        code, out, stub = run(ARGS + ["--into", str(path)], results=[{"itineraries": [DIRECT]}])
        check("filled cards are not overwritten without --replace", code == 1 and "--replace" in out, out[-300:])

        zh = plan_file(tmp, language="zh-CN")
        code, out, _ = run(ARGS + ["--into", str(zh)], results=[{"itineraries": [DIRECT, KLM]}])
        card = json.loads(zh.read_text(encoding="utf-8"))["booking_options"]["flights"][0]
        check("a Chinese plan gets Chinese card text", card["connection_summary"] == "往返均为直飞", card["connection_summary"])

        zoned = plan_file(tmp, timezone="Europe/London", origin_timezone="Europe/Amsterdam")
        code, out, _ = run(ARGS + ["--into", str(zoned)], results=[{"itineraries": [DIRECT]}])
        card = json.loads(zoned.read_text(encoding="utf-8"))["booking_options"]["flights"][0]
        check("kiwi_zones_from_plan: the round trip's zones come from the plan",
              code == 0 and card["outbound_itinerary"].get("departure_timezone") == "Europe/Amsterdam"
              and card["outbound_itinerary"].get("arrival_timezone") == "Europe/London"
              and card["return_itinerary"].get("departure_timezone") == "Europe/London"
              and card["return_itinerary"].get("arrival_timezone") == "Europe/Amsterdam",
              (out[-300:], card.get("outbound_itinerary"), card.get("return_itinerary")))
        import trip_zones  # noqa: PLC0415
        check("kiwi_zones_from_plan: the stamped zones agree with Kiwi's durations",
              not trip_zones.zone_problems(json.loads(zoned.read_text(encoding="utf-8"))),
              trip_zones.zone_problems(json.loads(zoned.read_text(encoding="utf-8"))))
        bare = plan_file(tmp)
        code, out, _ = run(ARGS + ["--into", str(bare)], results=[{"itineraries": [DIRECT]}])
        card = json.loads(bare.read_text(encoding="utf-8"))["booking_options"]["flights"][0]
        check("kiwi_zones_from_plan: a plan without zones gets none invented",
              "departure_timezone" not in card["outbound_itinerary"], card["outbound_itinerary"])

        path = plan_file(tmp)
        code, out, stub = run(ARGS + ["--into", str(path), "--accept-self-transfer"])
        check("self-transfer without the traveller's words is refused", code == 1 and not stub.calls
              and "accepts_self_transfer" in out, out[-300:])
        path = plan_file(tmp)
        plan = json.loads(path.read_text(encoding="utf-8"))
        plan["trip"]["traveler_preferences"]["accepts_self_transfer"] = "Cheapest is fine, we travel light and can re-check bags."
        path.write_text(json.dumps(plan), encoding="utf-8")
        code, out, stub = run(ARGS + ["--into", str(path), "--accept-self-transfer"],
                              results=[{"itineraries": [DIRECT, KLM]}, {"itineraries": [SELF_TRANSFER, DIRECT, KLM]}])
        flights = json.loads(path.read_text(encoding="utf-8"))["booking_options"]["flights"]
        searches = [c for c in stub.calls if c["body"].get("method") == "tools/call"]
        check("with consent, two searches", len(searches) == 2, len(searches))
        check("and the self-transfer card is marked", flights[0]["outbound_itinerary"].get("self_transfer") is True,
              flights[0]["outbound_itinerary"])
    code, out, _ = run(ARGS + ["--accept-self-transfer"])
    check("--accept-self-transfer needs --into", code == 1 and "--into" in out, out[-300:])


def end_to_end_case() -> None:
    """Cards from the script, TODOs filled as an author would, through every gate."""
    import check_plan_consistency as cpc  # noqa: PLC0415
    import plan_flags  # noqa: PLC0415
    import render_final_trip_html as renderer  # noqa: PLC0415
    import validate_trip_html as htmlgate  # noqa: PLC0415

    # The fixture is a one-day trip on 2026-09-28, so the flights go out in the morning and come
    # back that evening; a renderer-valid plan needs flight dates equal to the trip's.
    day = "2026-09-28"
    morning = itin(733, [seg("U2", "U23302", "AMS", "EDI", f"{day}T06:00:00", f"{day}T06:30:00", name="easyJet")],
                   [seg("U2", "U23301", "EDI", "AMS", f"{day}T20:00:00", f"{day}T22:40:00",
                        city_from="Edinburgh", city_to="Amsterdam", country_from="United Kingdom",
                        country_to="Netherlands", name="easyJet")])
    later = itin(778, [seg("KL", "KL1287", "AMS", "EDI", f"{day}T09:10:00", f"{day}T09:40:00", name="KLM")],
                 [seg("KL", "KL1290", "EDI", "AMS", f"{day}T18:05:00", f"{day}T20:40:00",
                      city_from="Edinburgh", city_to="Amsterdam", country_from="United Kingdom",
                      country_to="Netherlands", name="KLM")])
    argv = ["--from", "AMS", "--to", "EDI", "--depart", day, "--return", day,
            "--adults", "2", "--children", "2", "--currency", "EUR"]
    with tempfile.TemporaryDirectory() as tmp:
        path = plan_file(tmp, arrival_transport_mode="flight", start_date=day, end_date=day)
        code, out, _ = run(argv + ["--into", str(path)], results=[{"itineraries": [morning, later]}],
                           titles={"edinburgh-united-kingdom": "Amsterdam – Edinburgh trips"}, today="2026-09-01")
        check("the script wrote the cards", code == 0, out[-400:])
        plan = json.loads(path.read_text(encoding="utf-8"))
    for card in plan["booking_options"]["flights"]:
        card["review_url"] = "https://www.easyjet.com/en/" if "easyJet" in card["provider"] else "https://www.klm.com/"
        card["material_conditions"] = "Standard fare: changes for a fee, no refund."
        card["airport_transfer_note"] = "Airlink 100 bus to the city centre, about 30 minutes."
        card.pop("direct_provider"); card.pop("direct_review_url")
    # What the script leaves the author beyond the cards' own TODOs, done as an author would:
    # the second card's dated search on another platform (the Kiwi page is the first card's), the
    # booking-access check the page requires for a flight category, and -- fixture housekeeping --
    # the budget rows in the plan's currency, since plan_file switched the trip to EUR.
    second = plan["booking_options"]["flights"][1]
    second["round_trip_search_provider"] = "KAYAK"
    second["round_trip_search_url"] = f"https://www.kayak.com/flights/AMS-EDI/{day}/{day}/4adults"
    second["round_trip_prefilled_fields"] = ["origin", "destination", "outbound_date", "return_date", "travellers"]
    access = plan["regional_service_context"]["booking_access_checks"]
    flight_check = dict(access[0], category="flight", provider_or_channel="Kiwi.com and the airlines' own sites")
    access.append(flight_check)
    for row in plan["budget"].get("breakdown", []):
        row["currency"] = "EUR"
    errors = renderer.validate_plan(plan)
    check("the filled plan passes the renderer's plan check", not errors, errors[:3])
    findings: list[str] = []
    for check_fn in cpc.PLAN_CHECKS:
        check_fn(plan, findings, [])
    flight_findings = [f for f in findings if "flight" in f.lower() or "kiwi" in f.lower()]
    check("no consistency finding about the flight cards", not flight_findings, flight_findings[:3])
    page = renderer.render(plan)
    flags = plan_flags.derive_html_flags(plan)
    page_errors = htmlgate.validate(page, flags.expected_days, set(flags.required_booking_types),
                                    flags.transport_mode, [], require_unverified_banner=flags.require_unverified_banner,
                                    plan=plan)
    check("the page passes", not page_errors, page_errors[:3])
    check("Kiwi's booking link never reaches the page", "kiwi.com/u/" not in page and "/booking/" not in page)


def test_live_endpoint() -> None:
    """One real search, only when asked: TRAVEL_BUDDY_LIVE_KIWI=1."""
    if os.environ.get("TRAVEL_BUDDY_LIVE_KIWI") != "1":
        import pytest  # noqa: PLC0415
        pytest.skip("set TRAVEL_BUDDY_LIVE_KIWI=1 to search Kiwi.com for real")
    import datetime as _dt  # noqa: PLC0415
    depart = _dt.date.today() + _dt.timedelta(days=45)
    payload = kf.KiwiClient().search(kf.search_arguments(dict(REQUEST, depart=depart.isoformat(),
                                                              **{"return": (depart + _dt.timedelta(days=4)).isoformat()})))
    assert kf.usable_itineraries(payload, []), "the live endpoint returned no usable itinerary"


def review_fix_cases() -> None:
    """Four findings of the whole-branch review (2026-10-11), each pinned before its fix."""
    # 1. A round trip whose two directions are flown by disjoint airlines is two tickets: neither
    #    airline sells that fare, and change and refund terms differ per leg.
    mixed = itin(195, [seg("KL", "KL933", "AMS", "EDI", "2026-11-20T09:10:00", "2026-11-20T09:40:00", name="KLM")],
                 DIRECT["inbound"]["segments"])
    adults_only = dict(REQUEST, children=0)
    card = kf.itinerary_to_card(mixed, adults_only, 0, "2026-10-11", single=False)
    check("a mixed-carrier round trip says it is two tickets", "separate" in card.get("price_note", ""),
          card.get("price_note"))
    zh = kf.itinerary_to_card(mixed, dict(adults_only, language="zh"), 0, "2026-10-11", single=False)
    check("in Chinese too", "两张" in zh.get("price_note", ""), zh.get("price_note"))
    check("a single-airline round trip does not", "price_note" not in kf.itinerary_to_card(
        DIRECT, adults_only, 0, "2026-10-11", single=False))
    code, out, _ = run(["--from", "AMS", "--to", "EDI", "--depart", "2026-11-20", "--return", "2026-11-24",
                        "--adults", "2", "--currency", "EUR"], results=[{"itineraries": [mixed, KLM]}])
    check("and the run names it", "MIXED CARRIERS" in out, out[-400:])

    # 2. With an infant, `travellers` cannot be declared (Kiwi's infants parameter is unverified)
    #    and the page gate requires it, so the Kiwi link would leave the author stuck. Not used.
    infant_request = dict(REQUEST, adults=1, children=0, infants=1)
    cards = [kf.itinerary_to_card(DIRECT, infant_request, 0, "2026-10-11", single=False)]
    lines: list[str] = []
    kf.attach_search_link(cards, DIRECT, infant_request, lines,
                          opener=opener_with({"edinburgh-united-kingdom": "Amsterdam – Edinburgh trips"}, []))
    check("with an infant the Kiwi page is not used", cards[0]["round_trip_search_url"].startswith("TODO:")
          and "infant" in cards[0]["round_trip_search_url"], cards[0]["round_trip_search_url"])
    check("and the run says why", any(l.startswith("LINK NOT USED") for l in lines), lines)

    # 3. The endpoint says what it priced; a reply in another currency or for another party is not
    #    this search's answer, and writing it would label EUR figures as CNY.
    echo = {"itineraries": [DIRECT, KLM], "currency": "EUR", "passengers": {"adults": 2, "children": 2, "infants": 0}}
    code, out, _ = run(ARGS, results=[echo])
    check("a matching echo is accepted", code == 0, out[-300:])
    code, out, _ = run([a if a != "EUR" else "CNY" for a in ARGS], results=[echo])
    check("a reply in another currency is refused", code == 2 and "KIWI UNAVAILABLE" in out and "currency" in out, out[-300:])
    code, out, _ = run(ARGS, results=[dict(echo, passengers={"adults": 1, "children": 0, "infants": 0})])
    check("a reply for another party is refused", code == 2 and "passengers" in out, out[-300:])
    code, out, stub = run([a if a != "EUR" else "eur" for a in ARGS], results=[echo])
    sent = [c["body"]["params"]["arguments"].get("currency") for c in stub.calls if c["body"].get("method") == "tools/call"]
    check("--currency is upper-cased", code == 0 and sent == ["EUR"], (code, sent, out[-200:]))

    # 4. Traveller-visible totals print as amounts, never in exponent form.
    yen = dict(REQUEST, currency="JPY")
    big = dict(DIRECT, price=1250000)
    note = kf.itinerary_to_card(big, yen, 0, "2026-10-11", single=False)["price_note"]
    check("a large total prints in full", "1,250,000 JPY" in note and "e+" not in note, note)
    odd = dict(DIRECT, price=123456.7)
    note = kf.itinerary_to_card(odd, yen, 0, "2026-10-11", single=False)["price_note"]
    check("a fractional total keeps its cents", "123,456.70" in note, note)


def main() -> int:
    client_cases()
    mapping_cases()
    link_cases()
    cli_cases()
    end_to_end_case()
    review_fix_cases()
    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("kiwi flight cases passed")
    return 0


def test_kiwi_flights() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
