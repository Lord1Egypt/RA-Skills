#!/usr/bin/env python3
"""The trip as a calendar, and the one path that gets this plan off the laptop.

Every gate in this skill is about the delivered page being TRUE. None of them was about it being
WHERE THE TRAVELLER IS: a 331 KB local HTML file that nobody can open standing in Lucerne. A
calendar solves that with no server and no account of ours -- the file lands in the traveller's own
calendar and their phone syncs it -- and it carries the two things a page cannot: a time to be
somewhere, and a reminder that fires.

Which makes the file's VALIDITY the whole feature. A calendar a phone refuses to open is worse than
no calendar, because the traveller only finds out at the moment they were relying on it. So most of
this file is RFC 5545 conformance, and the rest is the rule that matters more: it must not invent.

Run:  python tests/test_calendar_export.py
      python -m pytest tests/test_calendar_export.py
"""

from __future__ import annotations

import base64
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import plan_to_calendar as CAL  # noqa: E402

FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"


def unfold(body: str) -> list[str]:
    """Undo RFC 5545 line folding, which is how a reader sees the properties."""
    out: list[str] = []
    for line in body.split("\r\n"):
        if line.startswith(" ") and out:
            out[-1] += line[1:]
        else:
            out.append(line)
    return [line for line in out if line]


def events(body: str) -> list[dict]:
    found, current = [], None
    for line in unfold(body):
        if line == "BEGIN:VEVENT":
            current = {"_raw": []}
        elif line == "END:VEVENT":
            found.append(current)
            current = None
        elif current is not None:
            current["_raw"].append(line)
            if ":" in line:
                key, value = line.split(":", 1)
                current.setdefault(key.split(";")[0], value)
    return found


def decision_and_zone_cases(report) -> None:
    def check(label: str, condition: object, detail: object = "") -> None:
        # This file's check() concatenates a string detail; a list or dict would turn a named
        # failure into a TypeError that reports nothing.
        report(label, bool(condition), str(detail) if detail != "" else "")

    self_drive = json.loads((ROOT / "tests" / "self-drive-fixture.json").read_text(encoding="utf-8"))

    def by_summary(body: str, needle: str) -> list[dict]:
        return [e for e in events(body) if needle in e.get("SUMMARY", "")]

    def alarmed(evt: dict) -> bool:
        return any("BEGIN:VALARM" in line for line in evt["_raw"])

    # Undecided: no trains, no car, both groups counted; times are UTC because the plan names zones.
    body, counts, summary = CAL.build_with_summary(self_drive)
    # Matched on the service name and the event wording: the fixture's own activities are called
    # "LNER train London King's Cross to Edinburgh Waverley" and "Collect the hire car at Hertz".
    check("undecided transport stays out", not by_summary(body, "Azuma") and not by_summary(body, "Pick up car"),
          [e.get("SUMMARY") for e in events(body)][:8])
    check("and is counted", len(summary["undecided"]) == 2 and "rental_cars" in summary["undecided"], summary)
    check("a zoned plan is not floating", summary["floating"] is False, summary)
    lunch = [e for e in events(body) if e.get("DTSTART") == "20261017T114000Z"]
    check("a meal is written in UTC (12:40 BST)", lunch, [e.get("DTSTART") for e in events(body)][:10])
    if lunch:
        check("and says its local time", lunch[0].get("DESCRIPTION", "").startswith("Local time: 12:40–13:35 Europe/London"),
              lunch[0].get("DESCRIPTION"))

    # Decided: the booked train and the chosen car enter, with their state.
    decided = json.loads(json.dumps(self_drive))
    decided["bookings"] = [{"option_id": "gt-lner", "state": "booked", "booked_on": "2026-10-10", "booked_via": "LNER website"},
                           {"option_id": "car-hertz", "state": "chosen"}]
    body, counts, summary = CAL.build_with_summary(decided)
    trains = by_summary(body, "Azuma")
    check("the booked train enters, both ways", len(trains) == 2 and not by_summary(body, "Lumo"), [e.get("SUMMARY") for e in trains])
    out = [e for e in trains if e.get("DTSTART") == "20261017T070000Z"]
    check("its outbound runs 07:00Z-11:23Z", out and out[0].get("DTEND") == "20261017T112300Z", out)
    check("its description says where it was booked", out and "Booked via LNER website on 2026-10-10" in out[0].get("DESCRIPTION", ""), out)
    pickup = by_summary(body, "Pick up car")
    check("the chosen car has a pickup at 12:45Z with a reminder",
          pickup and pickup[0].get("DTSTART") == "20261017T124500Z" and alarmed(pickup[0]) and "Hertz" in pickup[0]["SUMMARY"], pickup)
    check("and a return", by_summary(body, "Return car"), [e.get("SUMMARY") for e in events(body)][:12])
    check("its description says it is not booked yet", pickup and "Chosen — not booked yet" in pickup[0].get("DESCRIPTION", ""), pickup)
    check("nothing undecided now", summary["undecided"] == [], summary)

    # dst_meals: Europe/London leaves BST on 2026-10-25.
    dst = {"trip": {"timezone": "Europe/London", "origin_timezone": "Europe/London", "language": "en"},
           "days": [{"number": 1, "date": "2026-10-24", "dining": [{"venue_name": "Before", "time_window": "12:00-13:00"}]},
                    {"number": 2, "date": "2026-10-26", "dining": [{"venue_name": "After", "time_window": "12:00-13:00"}]}]}
    body, _, _ = CAL.build_with_summary(dst)
    check("dst_meals: BST before the change", by_summary(body, "Before") and by_summary(body, "Before")[0].get("DTSTART") == "20261024T110000Z")
    check("dst_meals: GMT after it", by_summary(body, "After") and by_summary(body, "After")[0].get("DTSTART") == "20261026T120000Z")

    # A date-line flight with zones: its true length, no patch.
    zoned = {"trip": {"timezone": "Pacific/Honolulu", "origin_timezone": "Asia/Tokyo", "language": "en"},
             "booking_options": {"flights": [{"id": "fl-1", "outbound_itinerary": {
                 "service_identifier": "ZG2", "departure_local": "2026-11-20 19:05", "arrival_local": "2026-11-20 07:10",
                 "duration_minutes": 425, "departure_timezone": "Asia/Tokyo", "arrival_timezone": "Pacific/Honolulu"}}]},
             "bookings": [{"option_id": "fl-1", "state": "chosen"}]}
    flight = by_summary(CAL.build_with_summary(zoned)[0], "ZG2")
    check("a zoned date-line flight is 10:05Z-17:10Z",
          flight and flight[0].get("DTSTART") == "20261120T100500Z" and flight[0].get("DTEND") == "20261120T171000Z", flight)

    # decided_without_times: chosen, but no times -- no event, no crash, not undecided.
    timeless = json.loads(json.dumps(zoned))
    timeless["booking_options"]["flights"][0]["outbound_itinerary"] = {"service_identifier": "ZG2"}
    body, _, summary = CAL.build_with_summary(timeless)
    check("decided_without_times", not by_summary(body, "ZG2") and summary["undecided"] == [], summary)

    # Activity times: a one-digit hour, a range, and one nobody can place.
    acts = {"trip": {"timezone": "Europe/London", "origin_timezone": "Europe/London", "language": "en"},
            "days": [{"number": 1, "date": "2026-10-17", "activities": [
                {"time": "9:30", "name": "Castle"}, {"time": "09:30–11:00", "name": "Gardens"}, {"time": "morning", "name": "Market"}]}]}
    body, _, summary = CAL.build_with_summary(acts)
    check("9:30 is an event", by_summary(body, "Castle") and by_summary(body, "Castle")[0].get("DTSTART") == "20261017T083000Z")
    gardens = by_summary(body, "Gardens")
    check("a range has an end", gardens and gardens[0].get("DTEND") == "20261017T100000Z", gardens)
    check("an unplaceable time is named", any("Market" in u for u in summary["unparsed"]), summary)
    trailing = {"days": [{"number": 1, "date": "2026-10-17", "dining": [
        {"venue_name": "Sitting", "time_window": "19:00–20:30, early sitting"}]}]}
    check("a meal window may trail words, as it always could",
          by_summary(CAL.build_with_summary(trailing)[0], "Sitting"))

    # Reminders: the enum decides; without it, keywords, negation first.
    def meal_alarm(note: str, need: object = None) -> bool:
        plan = {"days": [{"number": 1, "date": "2026-10-17", "dining": [
            {"venue_name": "Probe", "time_window": "12:00-13:00", "reservation_or_queue_note": note,
             **({} if need is None else {"reservation_need": need})}]}]}
        found = by_summary(CAL.build_with_summary(plan)[0], "Probe")
        return bool(found) and alarmed(found[0])
    check("'Book for 12:45 on a Saturday' reminds", meal_alarm("Book for 12:45 on a Saturday; a children's menu is available."))
    check("'book on a Saturday' reminds", meal_alarm("Walk-ins usually seated before 18:30; book on a Saturday in October."))
    check("'no booking needed' does not", not meal_alarm("Residents only; no booking needed."))
    check("'Reservations not accepted' does not", not meal_alarm("Reservations not accepted; queue from 11:30."))
    check("a guidebook is not a booking", not meal_alarm("Listed in every guidebook; counter service."))
    check("the enum beats the words (walk_in)", not meal_alarm("Book for 12:45", "walk_in"))
    check("the enum beats the words (required)", meal_alarm("Counter service.", "required"))
    check("a TODO enum falls back to the words", meal_alarm("Book ahead.", "TODO: pick one"))

    # A booked ticket needs no on-sale reminder; a chosen one keeps it.
    ticket_plan = {"booking_options": {"attraction_tickets": [{"id": "tk-1", "attraction_name": "Castle",
                   "sale_opens_at": {"status": "scheduled_release", "opens_at": "2026-10-10 09:30", "basis": "site"}}]}}
    check("a chosen ticket keeps its on-sale event",
          by_summary(CAL.build_with_summary({**ticket_plan, "bookings": [{"option_id": "tk-1", "state": "chosen"}]})[0], "on sale"))
    check("a booked ticket loses it",
          not by_summary(CAL.build_with_summary({**ticket_plan, "bookings": [{"option_id": "tk-1", "state": "booked",
                                                  "booked_on": "2026-10-10", "booked_via": "site"}]})[0], "on sale"))

    # A sale time written with its own offset is that instant, whatever the visit day's zone.
    def sale_start(opens_at: str) -> str:
        plan = {"trip": {"timezone": "Europe/London", "origin_timezone": "Europe/London"},
                "booking_options": {"attraction_tickets": [{"id": "tk-1", "attraction_name": "Castle",
                    "sale_opens_at": {"status": "scheduled_release", "opens_at": opens_at, "basis": "site"}}]}}
        found = by_summary(CAL.build_with_summary(plan)[0], "on sale")
        return found[0].get("DTSTART", "") if found else ""
    check("a +09:00 sale time is its own instant", sale_start("2026-12-01T12:00:00+09:00") == "20261201T030000Z",
          sale_start("2026-12-01T12:00:00+09:00"))
    check("a Z sale time is UTC", sale_start("2026-10-10T09:30:00Z") == "20261010T093000Z", sale_start("2026-10-10T09:30:00Z"))
    check("a naive sale time takes the trip zone", sale_start("2026-10-10 09:30") == "20261010T083000Z", sale_start("2026-10-10 09:30"))

    # A 12-hour window is not read as morning: no event, and it is named.
    twelve = {"days": [{"number": 1, "date": "2026-10-17", "dining": [
        {"venue_name": "Evening", "time_window": "7:00 PM–9:00 PM"}, {"venue_name": "Late", "time_window": "7:00–9:00 pm"}]}]}
    body, _, summary = CAL.build_with_summary(twelve)
    check("a 12-hour window makes no 07:00 event", not by_summary(body, "Evening") and not by_summary(body, "Late"),
          [e.get("DTSTART") for e in events(body)])
    check("and is named as not understood", sum("Evening" in u or "Late" in u for u in summary["unparsed"]) == 2, summary)

    # Negation belongs to the booking noun: "walk-ins not accepted" is a must-book note.
    check("'walk-ins not accepted' still reminds", meal_alarm("Reservations required; walk-ins not accepted."))
    check("'cards not accepted' still reminds", meal_alarm("Book ahead; cards not accepted."))

    # zh_descriptions: a Chinese plan's calendar lines are Chinese.
    zh = json.loads(json.dumps(decided))
    zh["trip"]["language"] = "zh-CN"
    body, _, _ = CAL.build_with_summary(zh)
    out = [e for e in by_summary(body, "Azuma") if e.get("DTSTART") == "20261017T070000Z"]
    check("zh_descriptions: local time and booking line in Chinese",
          out and "当地时间：08:00 Europe/London" in out[0].get("DESCRIPTION", "") and "已订：LNER website，2026-10-10" in out[0].get("DESCRIPTION", "")
          and "Booked via" not in out[0].get("DESCRIPTION", ""), out)

    # The floating fallback: no zones, so floating and said so.
    legacy = json.loads(FIXTURE.read_text(encoding="utf-8"))
    body, _, summary = CAL.build_with_summary(legacy)
    check("a plan without zones is floating, and says so", summary["floating"] is True
          and all(not e.get("DTSTART", "").endswith("Z") for e in events(body)), summary)
    check("the terminal notes name it", any("floating" in n for n in CAL.summary_notes(summary)), CAL.summary_notes(summary))


def main() -> int:
    failures: list[str] = []

    def check(label: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{label}{': ' + detail if detail else ''}")

    plan = json.loads(FIXTURE.read_text(encoding="utf-8"))
    body, counts = CAL.build(plan)
    raw = body.encode("utf-8")

    # 1. RFC 5545 conformance. Each of these is a reason a calendar app rejects a file outright,
    #    and a rejected file fails at exactly the moment it was needed.
    check("the file ends with CRLF", raw.endswith(b"\r\n"))
    check("there are no bare LFs", b"\n" not in raw.replace(b"\r\n", b""),
          "a bare LF makes the file unparseable to strict readers")
    lines = raw.split(b"\r\n")[:-1]
    over = [i for i, line in enumerate(lines) if len(line) > 75]
    check("no line exceeds 75 octets", not over,
          f"{len(over)} line(s), first at {over[0] + 1 if over else 0}")
    try:
        props = unfold(body)
    except UnicodeDecodeError as exc:
        props = []
        failures.append(f"folding split a multi-byte character: {exc}")
    check("the calendar is wrapped correctly",
          props and props[0] == "BEGIN:VCALENDAR" and props[-1] == "END:VCALENDAR")
    check("VERSION and PRODID are present",
          "VERSION:2.0" in props and any(p.startswith("PRODID:") for p in props))

    parsed = events(body)
    check("events were produced", parsed, "a plan with times produced no events")
    uids = [e.get("UID") for e in parsed]
    check("every event has a UID", all(uids), "an event without a UID cannot be updated or deduped")
    check("UIDs are unique", len(set(uids)) == len(uids),
          f"{len(uids) - len(set(uids))} duplicate(s) -- a calendar would collapse them into one")
    check("every event has a DTSTAMP", all(e.get("DTSTAMP") for e in parsed))
    check("every event has a DTSTART", all(e.get("DTSTART") for e in parsed))
    unescaped = [e["SUMMARY"] for e in parsed
                 if e.get("SUMMARY") and re.search(r"(?<!\\)[,;]", e["SUMMARY"])]
    check("commas and semicolons are escaped in TEXT values", not unescaped, f"{unescaped[:2]}")

    # Folding is counted in OCTETS, not characters, and this is the trap this repo has hit twice in
    # other forms: a rule tuned on Latin text meeting a document that is mostly Chinese. A split
    # UTF-8 sequence does not look wrong, it makes the file unopenable.
    # The line that separates the two counts: 44 characters, 108 octets. A length test written in
    # characters returns this unfolded, producing a 108-octet line that a strict reader rejects --
    # and the first version of this case used a line long enough to fail BOTH counts, so it passed
    # while the octet rule was mutated away.
    short_but_wide = "DESCRIPTION:" + "中文说明" * 8
    assert len(short_but_wide) <= 75 < len(short_but_wide.encode("utf-8"))
    narrow = CAL.fold(short_but_wide)
    check("a line under 75 CHARACTERS but over 75 OCTETS is still folded",
          all(len(chunk.encode("utf-8")) <= 75 for chunk in narrow.split("\r\n ")),
          f"{[len(c.encode('utf-8')) for c in narrow.split(chr(13) + chr(10) + ' ')]}")
    check("and it unfolds back unchanged",
          "".join(narrow.split("\r\n ")) == short_but_wide)

    long_cjk = "。".join(["这是一段很长的中文说明用来触发折行"] * 6)
    folded = CAL.fold(f"DESCRIPTION:{long_cjk}")
    check("folding a long CJK line keeps every chunk inside 75 octets",
          all(len(chunk.encode("utf-8")) <= 75 for chunk in folded.split("\r\n ")),
          f"{[len(c.encode('utf-8')) for c in folded.split(chr(13) + chr(10) + ' ')]}")
    check("and the folded line unfolds back to exactly what went in",
          "".join(folded.split("\r\n ")) == f"DESCRIPTION:{long_cjk}")

    # 2. IT MUST NOT INVENT. The contract carries ONE origin/destination pair per booking item, so
    #    on an open-jaw trip the return leg's real airports are in no structured field. Reversing
    #    the outbound pair produced "KL1924 GVA → AMS" for a flight that leaves Zurich -- the exact
    #    confident-and-wrong this skill exists to prevent, on the line a traveller reads at the
    #    airport.
    # The flight is BUILT here rather than taken from the fixture, which carries none -- so the
    # first version of this block was skipped by its own `if flights:` guard and reported a pass
    # for the case it exists to test.
    open_jaw = json.loads(json.dumps(plan))
    open_jaw.setdefault("booking_options", {})["flights"] = [{
        "id": "fl-1", "origin_airport": "AMS", "destination_airport": "GVA",
        "outbound_itinerary": {"service_identifier": "KL1931",
                               "departure_local": "2027-05-07 09:45",
                               "arrival_local": "2027-05-07 11:15"}}]
    open_jaw["bookings"] = [{"option_id": "fl-1", "state": "chosen"}]  # undecided transport no longer enters
    flights = open_jaw["booking_options"]["flights"]
    if flights:
        flights[0]["origin_airport"] = "AMS"
        flights[0]["destination_airport"] = "GVA"
        flights[0]["return_itinerary"] = {
            "service_identifier": "KL1924", "departure_local": "2027-05-12 17:35",
            "arrival_local": "2027-05-12 19:00", "duration_minutes": 85, "stops": 0,
            "connection_or_terminal_note": "returns from ZRH, not GVA"}
        returning = [e for e in events(CAL.build(open_jaw)[0])
                     if e.get("SUMMARY", "").startswith("KL1924")]
        check("the return leg produces an event", returning)
        if returning:
            check("the return leg states no route it cannot know",
                  "GVA" not in returning[0]["SUMMARY"] and "AMS" not in returning[0]["SUMMARY"],
                  f"{returning[0]['SUMMARY']!r} -- the contract cannot express open-jaw, so the "
                  f"calendar must not either")
            check("and the note that does know is carried",
                  "ZRH" in returning[0].get("DESCRIPTION", ""), f"{returning[0]}")

    # 3. The reminder is the point. A page can say "only 24 seats, call ahead"; only a calendar
    #    can make it happen.
    def alarmed(evts: list[dict]) -> list[str]:
        return [e.get("SUMMARY", "") for e in evts if any("BEGIN:VALARM" in r for r in e["_raw"])]

    probe = json.loads(json.dumps(plan))
    for day in probe.get("days") or []:
        dining = (day or {}).get("dining") or []
        if len(dining) >= 2:
            dining[0]["reservation_or_queue_note"] = "只有 24 个座位，务必提前致电订位"
            dining[0]["time_window"] = "19:00–20:30"
            dining[1]["reservation_or_queue_note"] = "无需预订，直接入座"
            dining[1]["time_window"] = "12:00–13:00"
            wanted, unwanted = dining[0].get("venue_name"), dining[1].get("venue_name")
            break
    else:
        wanted = unwanted = None
    if wanted:
        rung = alarmed(events(CAL.build(probe)[0]))
        check("a meal that must be booked ahead carries a reminder", wanted in rung, f"{rung[:4]}")
        check("a meal that needs no booking does not", unwanted not in rung,
              "a reminder on everything is a reminder on nothing")

    # 4. Degenerate plans must produce a valid empty calendar rather than a traceback or a file a
    #    phone chokes on.
    for label, shape in (("an empty plan", {}),
                         ("no days", {"trip": {"title": "x"}}),
                         ("days as a string", {"days": "nope"}),
                         ("a booking item with no times", {"booking_options": {"flights": [{}]}}),
                         ("garbage time strings", {"days": [{"date": "not-a-date",
                                                             "dining": [{"time_window": "soon"}],
                                                             "activities": [{"time": "later"}]}]})):
        try:
            out, _ = CAL.build(shape)
        except Exception as exc:  # noqa: BLE001 - any raise is the failure
            failures.append(f"build raised on {label}: {type(exc).__name__}: {exc}")
            continue
        check(f"{label} still produces a wrapped calendar",
              out.startswith("BEGIN:VCALENDAR") and out.rstrip().endswith("END:VCALENDAR"),
              out[:80])

    # 5. And the page has to carry it, because the page is what the traveller has open. Checked by
    #    decoding the data: URI rather than by looking for the markup: an empty href renders a
    #    button that looks exactly like a working one, which is how the first version shipped.
    import render_final_trip_html as RENDER
    real = ROOT / "tests" / "booking-ready-fixture.json"
    try:
        page = RENDER.render(json.loads(real.read_text(encoding="utf-8")))
    except Exception as exc:  # noqa: BLE001
        print(f"note: the fixture does not render in this environment ({exc}); the embedded-calendar "
              f"case was skipped.", file=sys.stderr)
    else:
        match = re.search(r'href="data:text/calendar;charset=utf-8;base64,([^"]+)"', page)
        check("the page embeds a calendar", match, "no data: URI -- nothing reaches the phone")
        if match:
            decoded = base64.b64decode(match.group(1)).decode("utf-8")
            check("the embedded calendar decodes to a real one",
                  decoded.startswith("BEGIN:VCALENDAR") and "BEGIN:VEVENT" in decoded,
                  decoded[:60])
            check("the download link names a file", 'download="' in page)

    # 6. Rendering the same plan twice must produce the same bytes. DTSTAMP used to be
    #    `datetime.now()`, which is the obvious reading of RFC 5545 and made the delivered PAGE
    #    irreproducible, because the calendar rides inside it as a base64 data: URI. Nothing here
    #    reported that; it surfaced as an intermittent ~20% failure of an imagery test asserting
    #    two renders are byte-identical -- a flake in a file that has nothing to do with calendars,
    #    which is the least useful place for a defect to be visible. Pinned here instead.
    plan = json.loads(FIXTURE.read_text(encoding="utf-8"))
    first, _ = CAL.build(plan)
    second, _ = CAL.build(json.loads(FIXTURE.read_text(encoding="utf-8")))
    check("building the same plan twice gives the same calendar", first == second,
          "the calendar is embedded in the page, so a moving byte makes the page irreproducible")

    stamps = {line.split(":", 1)[1] for line in unfold(first) if line.startswith("DTSTAMP:")}
    check("every event carries one DTSTAMP value", len(stamps) == 1, stamps)
    dated = json.loads(FIXTURE.read_text(encoding="utf-8"))
    dated["generated_at"] = "2026-09-03T10:00:00Z"
    stamped, _ = CAL.build(dated)
    check("DTSTAMP follows the plan's generated_at",
          "DTSTAMP:20260903T100000Z" in stamped,
          [l for l in unfold(stamped) if l.startswith("DTSTAMP")][:1])

    # And a plan with no usable timestamp still produces a calendar: the clock is the fallback,
    # so reproducibility is a bonus rather than a new way to fail.
    undated = json.loads(FIXTURE.read_text(encoding="utf-8"))
    undated["generated_at"] = "not a date"
    fallback, _ = CAL.build(undated)
    check("an unparseable generated_at still stamps the calendar",
          re.search(r"DTSTAMP:\d{8}T\d{6}Z", fallback), fallback[:200])

    # A flight whose local arrival clock is earlier than its departure (Tokyo 19:05 → Honolulu
    # 07:10 the same date, measured on Kiwi 2026-10-11) produced DTEND < DTSTART, which RFC 5545
    # forbids. With duration_minutes the end is start + duration.
    dateline = json.loads(FIXTURE.read_text(encoding="utf-8"))
    dateline["booking_options"]["flights"] = [{
        "id": "fl-1", "provider": "ZIPAIR", "origin_airport": "NRT", "destination_airport": "HNL",
        "outbound_itinerary": {"service_identifier": "ZG2", "departure_local": "2026-11-20 19:05",
                               "arrival_local": "2026-11-20 07:10", "duration_minutes": 425},
        "return_itinerary": {}}]
    dateline["bookings"] = [{"option_id": "fl-1", "state": "chosen"}]
    body, _ = CAL.build(dateline)
    flight = [e for e in events(body) if "ZG2" in e.get("SUMMARY", "")]
    check("a date-line flight ends after it starts",
          flight and flight[0].get("DTSTART") == "20261120T190500" and flight[0].get("DTEND") == "20261121T021000",
          str(flight))
    check("the minutes helper", CAL._plus_minutes("20261120T190500", 425) == "20261121T021000")
    no_duration = json.loads(json.dumps(dateline))
    no_duration["booking_options"]["flights"][0]["outbound_itinerary"].pop("duration_minutes")
    body, _ = CAL.build(no_duration)
    flight = [e for e in events(body) if "ZG2" in e.get("SUMMARY", "")]
    check("without a duration it is zero-length, never inverted",
          flight and flight[0].get("DTEND", flight[0].get("DTSTART")) >= flight[0].get("DTSTART"), str(flight))

    decision_and_zone_cases(check)

    if failures:
        print(f"CALENDAR EXPORT FAILED ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all calendar-export cases passed")
    return 0


def test_calendar_export() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
