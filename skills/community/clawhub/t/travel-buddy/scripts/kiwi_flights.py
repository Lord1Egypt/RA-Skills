#!/usr/bin/env python3
"""Fill a round-trip plan's flight cards from Kiwi.com's public flight search.

Airline sites and the usual comparison platforms answer this skill's research with bot challenges,
so flight facts were the ones a plan most often shipped unverified. Kiwi.com runs a public MCP
endpoint for AI assistants -- https://mcp.kiwi.com, no account, no key -- and this script asks it
directly, over HTTP, so it needs no setup on any host. It only ever calls the read-only
`search-flight` tool; Kiwi's other tool writes feedback to its developers and is never touched.

What it does with the answer, and why each step exists, is in the functions below. The short
version: protected connections only unless the traveller accepted self-transfer in their own
words; party totals turned into the card's per-person basis; flight numbers, local times, duration
and baggage onto the existing card fields; a dated Kiwi search page verified by its title; and
`TODO:` for what Kiwi cannot know, so the existing placeholder refusals make the author finish it.
Kiwi's own booking link is never used: it resolves to an affiliate checkout page, which the
booking-link rules forbid (references/booking-html-output.md#booking-links).

No published terms for the endpoint were found (2026-10-11). It is public and built for assistants;
this client names itself and makes one search per flight query, two when self-transfer is accepted.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import math
import os
import re
import sys
import tempfile
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_plan_consistency as cpc  # noqa: E402 - the prefilled-field rule this script asks
import trip_zones  # noqa: E402 - the plan's zones for the round trip's two ends

ENDPOINT = "https://mcp.kiwi.com"
SEARCH_TOOL = "search-flight"
PROTOCOL_VERSION = "2025-06-18"


class KiwiUnavailable(RuntimeError):
    """The endpoint could not be asked, or answered in a shape this script does not understand."""


def skill_version() -> str:
    """The plugin's version, read at runtime so there is no fifth copy of it to keep in step."""
    try:
        manifest = Path(__file__).resolve().parents[1] / ".claude-plugin" / "plugin.json"
        return str(json.loads(manifest.read_text(encoding="utf-8"))["version"])
    except (OSError, ValueError, KeyError):
        return "unknown"


def http_post(url: str, body: dict, headers: dict, timeout: float) -> tuple[str, dict]:
    request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                     headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace"), dict(response.headers)


def parse_messages(raw: str) -> list[dict]:
    """JSON-RPC messages from a Streamable HTTP body: SSE `data:` lines, or one plain JSON object."""
    messages = []
    for line in raw.splitlines():
        if line.startswith("data:"):
            try:
                messages.append(json.loads(line[5:].strip()))
            except ValueError:
                continue
    if not messages and raw.strip():
        messages.append(json.loads(raw))  # raises ValueError on a non-JSON body
    return messages


def result_problems(payload: object) -> list[str]:
    """What is wrong with the result envelope. Individual itineraries are judged when mapped."""
    if not isinstance(payload, dict):
        return [f"result is {type(payload).__name__}, not an object"]
    problems = []
    if payload.get("error"):
        problems.append(f"endpoint error: {str(payload['error'])[:200]}")
    if not isinstance(payload.get("itineraries"), list):
        problems.append("itineraries is not a list")
    return problems


class KiwiClient:
    def __init__(self, transport=http_post, endpoint: str = ENDPOINT, timeout: float = 90.0):
        self.transport = transport
        self.endpoint = endpoint
        self.timeout = timeout
        self.session_id: str | None = None
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": f"travel-buddy/{skill_version()} (+https://github.com/dong845/travel-buddy)",
        }

    def _send(self, body: dict) -> list[dict]:
        headers = dict(self.headers)
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        try:
            raw, response_headers = self.transport(self.endpoint, body, headers, self.timeout)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            raise KiwiUnavailable(f"{type(exc).__name__}: {exc}") from exc
        for key, value in response_headers.items():
            if key.lower() == "mcp-session-id":
                self.session_id = value
        try:
            return parse_messages(raw)
        except ValueError as exc:
            raise KiwiUnavailable(f"the endpoint answered with something that is not JSON ({exc})") from exc

    def search(self, arguments: dict) -> dict:
        self._send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": PROTOCOL_VERSION, "capabilities": {},
                               "clientInfo": {"name": "travel-buddy", "version": skill_version()}}})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        messages = self._send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                               "params": {"name": SEARCH_TOOL, "arguments": arguments}})
        result = next((m["result"] for m in messages if isinstance(m, dict) and "result" in m), None)
        if result is None:
            error = next((m.get("error") for m in messages if isinstance(m, dict) and m.get("error")), None)
            raise KiwiUnavailable("no result in the response"
                                  + (f": {json.dumps(error)[:200]}" if error else ""))
        payload = result.get("structuredContent")
        if payload is None:
            for item in result.get("content") or []:
                if isinstance(item, dict) and item.get("type") == "text":
                    try:
                        payload = json.loads(item["text"])
                        break
                    except ValueError:
                        continue
        problems = result_problems(payload)
        if problems:
            raise KiwiUnavailable("unexpected result: " + "; ".join(problems))
        return payload


SAFE_CONNECTIONS = {"allow_self_transfer": False, "allow_diff_airport_connection": False,
                    "allow_overnight_stopovers": False}
CABINS = {"M": ("economy", "经济舱"), "W": ("premium economy", "超级经济舱"),
          "C": ("business", "商务舱"), "F": ("first", "头等舱")}
CABIN_WORDS_ZH = {v[0]: v[1] for v in CABINS.values()}


def search_arguments(request: dict, permissive: bool = False) -> dict:
    """The search as Kiwi takes it, with protected connections unless asked otherwise.

    Measured on 2026-10-11: with Kiwi's defaults the cheapest Amsterdam–Edinburgh return for a
    family was easyJet to Belfast plus Ryanair on to Edinburgh on separate tickets, and a single
    traveller's was "land at Luton, leave from Stansted". Excluding self-transfer, airport changes
    and overnight layovers made the cheapest the direct easyJet flight, five euros dearer.
    """
    def ddmmyyyy(iso: str) -> str:
        return dt.date.fromisoformat(iso).strftime("%d/%m/%Y")
    arguments = {"flyFrom": request["origin"], "flyTo": request["destination"],
                 "departureDate": ddmmyyyy(request["depart"]), "returnDate": ddmmyyyy(request["return"]),
                 "adults": request["adults"], "children": request["children"], "infants": request["infants"],
                 "currency": request["currency"], "locale": "en", "sort": "price"}
    if request.get("cabin"):
        arguments["cabinClass"] = request["cabin"]
    arguments.update({key: permissive for key in SAFE_CONNECTIONS})
    return arguments


def _legs(itinerary: dict) -> list[tuple[str, dict]]:
    return [(name, itinerary[name]) for name in ("outbound", "inbound") if isinstance(itinerary.get(name), dict)]


def itinerary_problems(itinerary: object) -> list[str]:
    if not isinstance(itinerary, dict):
        return ["not an object"]
    problems = []
    if not isinstance(itinerary.get("price"), (int, float)) or isinstance(itinerary.get("price"), bool) \
            or itinerary["price"] <= 0:
        problems.append("no price")
    if not isinstance(itinerary.get("outbound"), dict) or not isinstance(itinerary.get("inbound"), dict):
        problems.append("not a round trip")
    for name, leg in _legs(itinerary):
        segments = leg.get("segments")
        if not isinstance(segments, list) or not segments:
            problems.append(f"{name} has no segments")
            continue
        for segment in segments:
            for key in ("carrier", "flightNumber", "from", "to", "departureTime", "arrivalTime"):
                if not isinstance(segment, dict) or not isinstance(segment.get(key), str) or not segment[key]:
                    problems.append(f"{name} segment without {key}")
                    break
    return problems


def segment_signature(itinerary: dict) -> tuple:
    """What makes two results the same flights: carrier, number and departure minute per segment."""
    return tuple((s["carrier"], s["flightNumber"], s["departureTime"][:16])
                 for _, leg in _legs(itinerary) for s in leg["segments"])


def usable_itineraries(payload: dict, lines: list[str]) -> list[dict]:
    """Well-formed results, cheapest first, one per segment signature (a codeshare is one option)."""
    valid = []
    for index, itinerary in enumerate(payload.get("itineraries") or []):
        problems = itinerary_problems(itinerary)
        if problems:
            lines.append(f"SKIPPED itinerary {index + 1}: {'; '.join(problems)}")
            continue
        valid.append(itinerary)
    # Sorted BEFORE deduplicating, so the copy kept of a codeshare is its cheapest fare.
    seen: set[tuple] = set()
    usable = []
    for itinerary in sorted(valid, key=lambda i: i["price"]):
        signature = segment_signature(itinerary)
        if signature in seen:
            continue
        seen.add(signature)
        usable.append(itinerary)
    return usable


def mark_self_transfer(safe: list[dict], permissive: list[dict]) -> list[dict]:
    """Kiwi marks no itinerary as self-transfer, so let its own filter decide.

    Anything the protected search returned is protected; anything only the permissive search
    returned needed one of the excluded connection kinds.
    """
    protected = {segment_signature(i) for i in safe}
    merged = {segment_signature(i): i for i in safe}
    for itinerary in permissive:
        signature = segment_signature(itinerary)
        if signature not in protected:
            merged[signature] = dict(itinerary, _self_transfer=True)
    return sorted(merged.values(), key=lambda i: i["price"])


def _departure(itinerary: dict) -> dt.datetime:
    return dt.datetime.fromisoformat(itinerary["outbound"]["segments"][0]["departureTime"][:19])


def _carriers(itinerary: dict) -> frozenset:
    return frozenset(s["carrier"] for _, leg in _legs(itinerary) for s in leg["segments"])


def pick_candidates(itineraries: list[dict]) -> list[dict]:
    """The cheapest, and the cheapest that is a real alternative: another airline, or a departure
    at least two hours away. Two fares on the same flights are not a comparison."""
    if not itineraries:
        return []
    first = itineraries[0]
    for other in itineraries[1:]:
        if _carriers(other) != _carriers(first) or \
                abs((_departure(other) - _departure(first)).total_seconds()) >= 2 * 3600:
            return [first, other]
    return [first]


def _clock(iso: str) -> str:
    return iso[:16].replace("T", " ")


def _minutes(seconds: object) -> int | None:
    return round(seconds / 60) if isinstance(seconds, (int, float)) and not isinstance(seconds, bool) else None


def _layover(a: dict, b: dict) -> str:
    gap = dt.datetime.fromisoformat(b["departureTime"][:19]) - dt.datetime.fromisoformat(a["arrivalTime"][:19])
    minutes = int(gap.total_seconds() // 60)
    return f"{minutes // 60}h{minutes % 60:02d}"


def _leg_note(leg: dict, zh: bool) -> str:
    segments = leg["segments"]
    route = " → ".join([segments[0]["from"]] + [s["to"] for s in segments])
    if len(segments) == 1:
        # The renderer prints the stop count itself ("non-stop" / 直飞); repeating it here read
        # "直飞 · 直飞，AMS → EDI" on a real card.
        return route
    changes = []
    for a, b in zip(segments, segments[1:]):
        where = a["to"] if a["to"] == b["from"] else f"{a['to']} → {b['from']}"
        changes.append((f"在 {where} 转机（停留 {_layover(a, b)}）") if zh
                       else f"change at {where} ({_layover(a, b)} layover)")
    return f"{route}；" + "；".join(changes) if zh else f"{route}; " + "; ".join(changes)


def _connection_summary(itinerary: dict, zh: bool) -> str:
    """Both directions in one phrase, for the card's detail line: direct, or how many changes."""
    def part(leg: dict, en_name: str, zh_name: str) -> str:
        changes = len(leg["segments"]) - 1
        if zh:
            return f"{zh_name}直飞" if not changes else f"{zh_name}转机 {changes} 次"
        return f"{en_name}: direct" if not changes else f"{en_name}: {changes} change{'s' if changes > 1 else ''}"
    outbound, inbound = itinerary["outbound"], itinerary["inbound"]
    if len(outbound["segments"]) == 1 and len(inbound["segments"]) == 1:
        return "往返均为直飞" if zh else "Direct both ways"
    return ("；" if zh else "; ").join((part(outbound, "Outbound", "去程"), part(inbound, "return", "回程")))


def _amount(value: float) -> str:
    """A total as a person reads it: 1,250,000 -- never 1.25e+06, which `:g` printed for a JPY party."""
    return f"{int(value):,}" if float(value).is_integer() else f"{value:,.2f}"


def _mixed_carriers(itinerary: dict) -> tuple[list[str], list[str]] | None:
    """The airlines of each direction when the two share none: a round trip sold as two tickets."""
    def names(leg: dict) -> list[str]:
        return list(dict.fromkeys(s.get("carrierName") or s["carrier"] for s in leg["segments"]))
    out = {s["carrier"] for s in itinerary["outbound"]["segments"]}
    back = {s["carrier"] for s in itinerary["inbound"]["segments"]}
    return None if out & back else (names(itinerary["outbound"]), names(itinerary["inbound"]))


def _party_words(request: dict, zh: bool) -> str:
    parts = []
    for key, en, cn in (("adults", "adult", "位成人"), ("children", "child", "位儿童"), ("infants", "infant", "位婴儿")):
        count = request[key]
        if count:
            parts.append(f"{count} {cn}" if zh else f"{count} {en if count == 1 else en + ('ren' if en == 'child' else 's')}")
    return " + ".join(parts)


def itinerary_to_card(itinerary: dict, request: dict, index: int, checked_at: str, single: bool) -> dict:
    """One Kiwi itinerary as one flight card of templates/final-trip-plan.json.

    Every value Kiwi gives goes into the field the renderer already prints; every value it cannot
    know is a `TODO:` the existing placeholder refusals make the author answer.
    """
    zh = request["language"] == "zh"
    travellers = request["adults"] + request["children"] + request["infants"]
    total = itinerary["price"]
    per_person = math.ceil(total / travellers)
    marked = bool(itinerary.get("_self_transfer"))

    def leg_card(leg: dict) -> dict:
        segments = leg["segments"]
        entry = {"service_identifier": " + ".join(s["flightNumber"] for s in segments),
                 "departure_local": _clock(segments[0]["departureTime"]),
                 "arrival_local": _clock(segments[-1]["arrivalTime"]),
                 "duration_minutes": _minutes(leg.get("durationSeconds")),
                 "stops": len(segments) - 1,
                 "connection_or_terminal_note": _leg_note(leg, zh),
                 "service_identifier_status": "researched",
                 "service_identifier_unresearched_reason": None}
        if marked and len(segments) > 1:
            entry["self_transfer"] = True
        return entry

    carriers = list(dict.fromkeys(s.get("carrierName") or s["carrier"]
                                  for _, leg in _legs(itinerary) for s in leg["segments"]))
    cabin_code = request.get("cabin")
    cabin = (CABINS[cabin_code][1 if zh else 0] if cabin_code in CABINS
             else itinerary["outbound"].get("cabinClass") or "economy")
    if zh:
        # Kiwi writes "Economy"; the table is keyed lower-case.
        cabin = CABIN_WORDS_ZH.get(str(cabin).casefold(), cabin)
    bags = itinerary.get("baggage") or {}
    baggage = (f"全团已含：{bags.get('personalItem', 0)} 件随身小件、{bags.get('cabinBag', 0)} 件登机箱、"
               f"{bags.get('checkedBag', 0)} 件托运行李" if zh else
               f"Included for the party: {bags.get('personalItem', 0)} personal items, "
               f"{bags.get('cabinBag', 0)} cabin bags, {bags.get('checkedBag', 0)} checked bags")
    outbound, inbound = itinerary["outbound"], itinerary["inbound"]
    todo = "TODO: "
    card = {
        "id": f"fl-kiwi-{index + 1}",
        "leg_group_id": f"flight-{request['origin']}-{request['destination']}".lower(),
        "provider": " + ".join(carriers),
        "comparison_platform": "Kiwi.com",
        "comparison_checked_at": checked_at,
        "direct_provider": todo + "the operating airline, or delete both direct_* fields if it has no route page",
        "direct_review_url": todo + "the airline's own page for this route, or delete both direct_* fields",
        "source_type": "comparison_platform",
        "checked_at": checked_at,
        "review_url": todo + "the operating airline's own site (HTTPS) for this route",
        "round_trip_search_provider": "Kiwi.com",
        "round_trip_search_checked_at": checked_at,
        "round_trip_search_url": todo + "a dated comparison search; the Kiwi page did not verify",
        "round_trip_prefilled_fields": [],
        "origin_airport": outbound["segments"][0]["from"],
        "destination_airport": outbound["segments"][-1]["to"],
        "outbound_date": request["depart"],
        "return_date": request["return"],
        "outbound_itinerary": leg_card(outbound),
        "return_itinerary": leg_card(inbound),
        "cabin": cabin,
        "baggage_assumption": baggage,
        "connection_summary": _connection_summary(itinerary, zh),
        "fare_currency": request["currency"],
        "fare_low": per_person,
        "fare_high": per_person,
        "price_basis": "per_person_round_trip",
        "price_status": "researched_current",
        "material_conditions": todo + "change and refund terms of this fare",
        "availability_status": "available",
        "price_checked_at": checked_at,
        "airport_transfer_note": todo + "how the traveller gets from the arrival airport into town",
    }
    notes = []
    if request["children"] or request["infants"]:
        notes.append(f"全团合计 {_amount(total)} {request['currency']}（{_party_words(request, True)}），此处为人均平均值。"
                     if zh else
                     f"Party total {_amount(total)} {request['currency']} for {_party_words(request, False)}; "
                     f"shown as an average per person.")
    # Disjoint airlines out and back (KLM out, easyJet back: 9 of 15 recorded Amsterdam-Edinburgh
    # results) are two tickets. Neither airline sells the pair, and each leg changes and refunds on
    # its own terms -- which a card headed "round trip" would otherwise hide.
    mixed = _mixed_carriers(itinerary)
    if mixed:
        out_names, back_names = ("、".join(mixed[0]), "、".join(mixed[1])) if zh else \
            (", ".join(mixed[0]), ", ".join(mixed[1]))
        notes.append(f"去程（{out_names}）和回程（{back_names}）是不同航司的两张票，各自预订、改签和退款，条款不同。"
                     if zh else
                     f"Outbound ({out_names}) and return ({back_names}) are separate tickets with different "
                     f"airlines: each is booked, changed and refunded on its own terms.")
    if notes:
        card["price_note"] = (" " if not zh else "").join(notes)
    if single:
        card["single_option_reason"] = ("Kiwi.com 在这些日期没有返回航司不同或出发时间相差两小时以上的第二个方案。"
                                        if zh else
                                        "Kiwi.com returned no second itinerary with another airline or a departure "
                                        "at least two hours apart for these dates.")
    return card


SEARCH_PAGE = "https://www.kiwi.com/en/search/results"
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
ALL_PREFILL = ["origin", "destination", "outbound_date", "return_date", "travellers"]


def _fold(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").casefold().strip()


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", _fold(text)).strip("-")


def place_slugs(itinerary: dict) -> tuple[str, str]:
    """Kiwi's keys for the two ends of the outbound leg: `city-country`, accent-folded."""
    first = itinerary["outbound"]["segments"][0]
    last = itinerary["outbound"]["segments"][-1]
    return (f"{slugify(first.get('fromCity', ''))}-{slugify(first.get('fromCountry', ''))}",
            f"{slugify(last.get('toCity', ''))}-{slugify(last.get('toCountry', ''))}")


def search_page_url(itinerary: dict, request: dict) -> str:
    """Kiwi's search-results page in the only form that prefills its cities: `city-country` slugs.

    The IATA form (/AMS/EDI/...) loads with the dates and party filled in and BOTH places empty --
    a 200 that delivers nothing (checked in Chrome, 2026-10-11).
    """
    origin, destination = place_slugs(itinerary)
    query = {"adults": request["adults"]}
    if request["children"]:
        query["children"] = request["children"]
    if request["infants"]:
        query["infants"] = request["infants"]
    return (f"{SEARCH_PAGE}/{origin}/{destination}/{request['depart']}/{request['return']}"
            f"?{urllib.parse.urlencode(query)}")


def fetch_title(url: str, opener=urllib.request.urlopen, timeout: float = 30.0) -> str | None:
    try:
        with opener(urllib.request.Request(url, headers={"User-Agent": BROWSER_UA, "Accept-Language": "en"}),
                    timeout=timeout) as response:
            body = response.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return None
    match = re.search(r"<title>(.*?)</title>", body, re.DOTALL | re.IGNORECASE)
    return html.unescape(match.group(1)) if match else None


def title_confirms(title: str | None, origin_city: str, destination_city: str) -> bool:
    """The server-rendered title names both cities only when both slugs resolved.

    Valid: "Amsterdam – Edinburgh trips". Invalid slugs give "–  trips" or Kiwi's generic home-page
    title. Names are compared accent-folded: slug `zurich` renders as "Zürich".
    """
    if not title:
        return False
    match = re.fullmatch(r"\s*(.+?)\s+[–-]\s+(.+?)\s+trips\s*", title.replace("‎", ""))
    if not match:
        return False
    return _fold(match.group(1)) == _fold(origin_city) and _fold(match.group(2)) == _fold(destination_city)


def prefilled_fields(url: str, card: dict, request: dict) -> list[str]:
    """Only the fields the gate itself confirms in this URL -- asked, never assumed.

    Kiwi's `infants` parameter was never checked on a rendered page, so a party with infants does
    not declare `travellers` even when the number is in the URL.
    """
    wanted = {"origin": card["origin_airport"], "destination": card["destination_airport"],
              "outbound_date": card["outbound_date"], "return_date": card["return_date"],
              "travellers": request["adults"] + request["children"] + request["infants"]}
    ids = {"origin": card.get("origin_place_id"), "destination": card.get("destination_place_id")}
    missing = {field for field, _, _ in cpc.undelivered_prefill_fields(url, ALL_PREFILL, wanted, ids)}
    fields = [field for field in ALL_PREFILL if field not in missing]
    if request["infants"]:
        fields = [field for field in fields if field != "travellers"]
    return fields


def attach_search_link(cards: list[dict], itinerary: dict, request: dict, lines: list[str],
                       opener=urllib.request.urlopen) -> None:
    if request["infants"]:
        # The page gate requires `travellers` on every flight search button, and Kiwi's `infants`
        # parameter was never checked on a rendered page, so `travellers` cannot be declared: a
        # verified Kiwi link would only leave the author stuck behind a refusal they cannot fix.
        for card in cards:
            card["round_trip_search_url"] = ("TODO: a dated round-trip search that carries the whole party, "
                                             "infants included -- Kiwi's infants parameter is unverified, so "
                                             "its page is not used")
        lines.append("LINK NOT USED: the party includes infants, and Kiwi's search page was never checked to "
                     "carry them; find a dated search on another platform that does")
        return
    url = search_page_url(itinerary, request)
    first = itinerary["outbound"]["segments"][0]
    last = itinerary["outbound"]["segments"][-1]
    if title_confirms(fetch_title(url, opener=opener), first.get("fromCity", ""), last.get("toCity", "")):
        # The first card only. Two options that open the same page are one option shown twice
        # (check_plan_consistency.check_booking_identity), and the Kiwi page lists both, so a
        # second card needs a dated search of its own on another comparison platform.
        card = cards[0]
        card["origin_place_id"], card["destination_place_id"] = place_slugs(itinerary)
        card["round_trip_search_url"] = url
        card["round_trip_prefilled_fields"] = prefilled_fields(url, card, request)
        for other in cards[1:]:
            other["round_trip_search_url"] = ("TODO: a dated round-trip search on another comparison "
                                              "platform -- the Kiwi page is the first card's, and two "
                                              "options may not open the same page")
        lines.append(f"LINK VERIFIED {url} (first card; the others need another platform)")
    else:
        lines.append(f"LINK NOT VERIFIED {url} -- its title did not name both cities; find another "
                     f"dated comparison search for round_trip_search_url")


def echo_problems(payload: dict, request: dict) -> list[str]:
    """Where the reply says it priced something other than what was asked.

    Every recorded reply echoes `currency` and `passengers`. A reply in another currency would put
    EUR figures under a CNY label; one for another party would be divided by the wrong head count.
    """
    problems = []
    currency = payload.get("currency")
    if isinstance(currency, str) and currency.strip() and currency.strip().upper() != request["currency"].upper():
        problems.append(f"the reply is priced in currency {currency}, not {request['currency']}")
    passengers = payload.get("passengers")
    if isinstance(passengers, dict):
        asked = {key: request[key] for key in ("adults", "children", "infants")}
        echoed = {key: passengers.get(key) for key in asked if key in passengers}
        if any(echoed[key] != asked[key] for key in echoed):
            problems.append(f"the reply's passengers are {echoed}, not {asked}")
    return problems


def _is_filled_card(card: object) -> bool:
    """A flight card someone answered: a real provider or a priced fare, not the skeleton's TODOs."""
    if not isinstance(card, dict):
        return False
    provider = card.get("provider")
    fare = card.get("fare_low")
    return (isinstance(provider, str) and provider.strip() and not provider.strip().upper().startswith("TODO")) \
        or (isinstance(fare, (int, float)) and not isinstance(fare, bool))


def _refuse(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def stamp_zones(plan: dict, cards: list[dict]) -> bool:
    """The round trip's two ends from the plan's own zones, when it names them.

    A Kiwi search here is the round trip between trip.origin and the destination on the trip's own
    dates (main() refuses other dates), so its outbound leaves the origin zone and lands in the
    first day's zone, and the return is the reverse. Without the plan's zones nothing is written:
    the gate then asks for them by name, rather than this script guessing from airport codes.
    """
    trip = plan.get("trip") if isinstance(plan.get("trip"), dict) else {}
    days = [d for d in plan.get("days") or [] if isinstance(d, dict)]
    origin = str(trip.get("origin_timezone") or "")
    first = trip_zones.day_zone(plan, days[0]) if days else trip_zones.zone_on(plan, dt.date.min)
    last = trip_zones.day_zone(plan, days[-1]) if days else first
    if not (trip_zones.zone(origin) and first and last):
        return False
    for card in cards:
        for leg, departure, arrival in (("outbound_itinerary", origin, first), ("return_itinerary", last, origin)):
            if isinstance(card.get(leg), dict) and card[leg].get("departure_local"):
                card[leg]["departure_timezone"], card[leg]["arrival_timezone"] = departure, arrival
    return True


def main(argv: list[str] | None = None, client: KiwiClient | None = None,
         opener=urllib.request.urlopen, today: dt.date | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--from", dest="origin", required=True, help="Origin airport or city code (IATA)")
    parser.add_argument("--to", dest="destination", required=True, help="Destination airport or city code (IATA)")
    parser.add_argument("--depart", required=True, help="Outbound date, YYYY-MM-DD")
    parser.add_argument("--return", dest="ret", required=True, help="Return date, YYYY-MM-DD")
    parser.add_argument("--adults", type=int, default=1)
    parser.add_argument("--children", type=int, default=0, help="Aged 2-11")
    parser.add_argument("--infants", type=int, default=0, help="Under 2")
    parser.add_argument("--cabin", choices=sorted(CABINS), default=None, help="M economy, W premium, C business, F first")
    parser.add_argument("--currency", default=None, help="Defaults to the plan's trip.currency, else EUR")
    parser.add_argument("--language", choices=("en", "zh"), default=None, help="Card text language without --into")
    parser.add_argument("--accept-self-transfer", action="store_true",
                        help="Also allow separate-ticket connections; needs --into and the traveller's own words "
                             "in trip.traveler_preferences.accepts_self_transfer")
    parser.add_argument("--into", default=None, help="Plan JSON whose booking_options.flights to replace")
    parser.add_argument("--replace", action="store_true", help="Replace flight cards that are already filled")
    parser.add_argument("--today", default=None, help="Treat this date as today (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    try:
        now = dt.date.fromisoformat(args.today) if args.today else (today or dt.date.today())
        depart = dt.date.fromisoformat(args.depart)
        ret = dt.date.fromisoformat(args.ret)
    except ValueError as exc:
        return _refuse(f"dates are YYYY-MM-DD ({exc})")
    if depart < now:
        return _refuse(f"--depart {depart} is before today ({now})")
    if ret < depart:
        return _refuse(f"--return {ret} is before --depart {depart}")
    if args.adults < 1 or args.children < 0 or args.infants < 0:
        return _refuse("a search needs at least one adult and no negative counts")
    if args.infants > args.adults:
        return _refuse("each infant travels on an adult's lap: --infants cannot exceed --adults")
    if args.accept_self_transfer and not args.into:
        return _refuse("--accept-self-transfer needs --into, so the traveller's consent can be read from the plan")

    plan = None
    language = args.language or "en"
    currency = (args.currency or "EUR").upper()
    if args.into:
        try:
            plan = json.loads(Path(args.into).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            return _refuse(f"cannot read {args.into}: {exc}")
        trip = plan.get("trip") if isinstance(plan, dict) else None
        if not isinstance(trip, dict):
            return _refuse(f"{args.into} has no trip object")
        party = args.adults + args.children + args.infants
        if trip.get("traveler_count") != party:
            return _refuse(f"the search is for {party} travellers but trip.traveler_count is "
                           f"{trip.get('traveler_count')!r}; the cards must price the plan's own party")
        plan_currency = trip.get("currency")
        if args.currency and plan_currency and args.currency.upper() != str(plan_currency).upper():
            return _refuse(f"--currency {args.currency} differs from trip.currency {plan_currency}; "
                           f"cards are priced in the plan's currency")
        currency = plan_currency or currency
        # render_final_trip_html.validate_plan refuses a flight whose dates are not the trip's
        # first and last day, so cards for other dates could never be saved.
        start, end = str(trip.get("start_date") or "")[:10], str(trip.get("end_date") or "")[:10]
        if start and end and (depart.isoformat() != start or ret.isoformat() != end):
            return _refuse(f"the search is {depart} to {ret} but the trip runs {start} to {end}; a flight "
                           f"card's dates must be the trip's first and last day (trip.start_date / "
                           f"trip.end_date)")
        language = "zh" if str(trip.get("language") or "").casefold().startswith("zh") else "en"
        consent = (trip.get("traveler_preferences") or {}).get("accepts_self_transfer")
        if args.accept_self_transfer and not (isinstance(consent, str) and consent.strip()
                                              and not consent.strip().upper().startswith("TODO")):
            return _refuse("--accept-self-transfer needs the traveller's own words in "
                           "trip.traveler_preferences.accepts_self_transfer")
        existing = ((plan.get("booking_options") or {}).get("flights") or [])
        if any(_is_filled_card(card) for card in existing) and not args.replace:
            return _refuse(f"{args.into} already has filled flight cards; pass --replace to overwrite them")

    request = {"origin": args.origin.upper(), "destination": args.destination.upper(),
               "depart": depart.isoformat(), "return": ret.isoformat(), "adults": args.adults,
               "children": args.children, "infants": args.infants, "cabin": args.cabin,
               "currency": currency, "language": language}
    client = client or KiwiClient()
    lines: list[str] = []
    try:
        def search(permissive: bool) -> dict:
            payload = client.search(search_arguments(request, permissive=permissive))
            problems = echo_problems(payload, request)
            if problems:
                raise KiwiUnavailable("; ".join(problems))
            return payload
        safe = usable_itineraries(search(False), lines)
        itineraries = safe
        if args.accept_self_transfer:
            permissive = usable_itineraries(search(True), lines)
            itineraries = mark_self_transfer(safe, permissive)
    except KiwiUnavailable as exc:
        print(f"KIWI UNAVAILABLE: {exc}. Research flights as before and say so in the hand-off.", file=sys.stderr)
        return 2
    for line in lines:
        print(line)
    candidates = pick_candidates(itineraries)
    if not candidates:
        print("KIWI NO RESULTS for these dates and this party. Research flights as before and say so.",
              file=sys.stderr)
        return 3
    checked_at = now.isoformat()
    cards = [itinerary_to_card(c, request, n, checked_at, single=len(candidates) == 1)
             for n, c in enumerate(candidates)]
    if plan is not None and stamp_zones(plan, cards):
        print("ZONES: each card's two ends carry the plan's trip.origin_timezone and destination zone.")
    attach_search_link(cards, candidates[0], request, lines, opener=opener)
    for line in lines[-1:]:
        print(line)
    for candidate, card in zip(candidates, cards):
        flag = " (self-transfer)" if candidate.get("_self_transfer") else ""
        print(f"CANDIDATE {card['id']}: {card['provider']} {card['fare_low']} {currency} per person{flag}")
        mixed = _mixed_carriers(candidate)
        if mixed:
            print(f"MIXED CARRIERS {card['id']}: outbound {', '.join(mixed[0])}, return {', '.join(mixed[1])} -- "
                  f"two tickets; the card's price note says so")

    if plan is None:
        print(json.dumps(cards, ensure_ascii=False, indent=1))
        print("NEXT: put these cards in booking_options.flights (or rerun with --into <plan.json>), "
              "then fill every TODO: field.")
        return 0

    plan.setdefault("booking_options", {})["flights"] = cards
    source_url = next((c["round_trip_search_url"] for c in cards
                       if not str(c["round_trip_search_url"]).startswith("TODO")), "https://www.kiwi.com/")
    sources = plan.setdefault("sources", [])
    if not any(isinstance(s, dict) and s.get("name") == "Kiwi.com flight search" and s.get("url") == source_url
               for s in sources):
        sources.append({"name": "Kiwi.com flight search", "url": source_url, "source_type": "comparison_platform",
                        "accessed_at": checked_at,
                        "claim_or_decision_supported": "flight prices, flight numbers, times and baggage",
                        "confidence": "researched"})
    target = Path(args.into)
    fd, temp = tempfile.mkstemp(dir=str(target.parent), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(plan, handle, ensure_ascii=False, indent=2)
    os.replace(temp, target)
    print(f"WROTE {len(cards)} flight card(s) into {target}")
    todo_fields = "review_url, material_conditions, airport_transfer_note, direct_*"
    if len(cards) > 1 or any(str(c["round_trip_search_url"]).startswith("TODO") for c in cards):
        todo_fields += ", and round_trip_search_url wherever it is still TODO (a dated search on another platform)"
    print(f"NEXT: fill the TODO: fields on the new flight cards ({todo_fields}), then "
          f"python scripts/check_plan_contract.py {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
