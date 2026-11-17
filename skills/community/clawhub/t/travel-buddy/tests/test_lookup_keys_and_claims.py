#!/usr/bin/env python3
"""Regression tests for three defects a delivered plan shipped, all of one family.

A traveller read the finished page and asked four questions. Three had the same shape underneath:
something the plan SAID about itself was never compared to the thing it described.

  1. The page had no photographs. The imagery resolver searches Wikipedia by the anchor's name,
     and two of its own rules made that impossible on a Chinese plan: a token floor of three
     characters, tuned for Latin, erased every two-character CJK name (香港, 长洲, 北京, 东京 …),
     and the relevance rule ran on exact title lookups, throwing away the wiki's own
     simplified-to-traditional resolution because 中环街市 and 中環街市 share no token.
  2. The flight button opened an empty search box while the plan declared five fields prefilled.
     The gate checked the declaration's dates by substring, which a sentence typed into a
     free-text `q=` parameter satisfies, and never looked for origin, destination or travellers
     at all. An attestation records that a rule was claimed, never that it was followed.
  3. A run that filled no photographs exited 0 with a few notes that had already scrolled past.

Run:  python tests/test_lookup_keys_and_claims.py
      python -m pytest tests/test_lookup_keys_and_claims.py
"""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import fetch_plan_imagery as IMAGERY  # noqa: E402
import check_plan_consistency as CHECKER  # noqa: E402

FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"


def cjk_token_cases() -> list[str]:
    """A two-character CJK name is a whole name; a Latin floor of three deletes it.

    Measured before the fix: `_tokens("香港")` and `_tokens("长洲")` both returned the empty set,
    so `_relevant` fell into its "the query IS the place" branch, compared two empty sets, and
    returned False for every two-character destination on every Chinese-language plan. The hero
    photograph could not resolve for 香港, 北京, 上海, 东京, 京都, 台北 or 澳门, and the script
    reported "no article both near the trip and about it" and exited 0.
    """
    failures: list[str] = []
    for name in ("香港", "长洲", "北京", "上海", "东京", "台北", "澳門"):
        if not IMAGERY._tokens_raw(name):
            failures.append(f"cjk tokens: {name!r} produced no token, so every lookup that "
                            f"compares it to an article title silently answers False")
    # The Latin floor is what it was: three characters, so `the` and `and` still cost nothing.
    for stop in ("th", "an", "de"):
        if IMAGERY._tokens_raw(stop):
            failures.append(f"cjk tokens: raising the CJK floor also lowered the Latin one — "
                            f"{stop!r} is now a token")
    if "market" not in IMAGERY._tokens_raw("Central Market"):
        failures.append("cjk tokens: Latin words stopped tokenising")
    return failures


def writing_variant_cases() -> list[str]:
    """An exact title lookup has already been answered by the wiki; do not re-litigate it.

    `titles=X&redirects=1` returns page X or its redirect target and can return nothing else, so
    there is no ranking to be sceptical of. Running the token rule on it rejected correct matches
    across writing systems: zh.wikipedia resolves 中环街市 to 中環街市, the two share no token, and
    the article with the right photograph was thrown away by the check meant to protect it.
    """
    failures: list[str] = []
    if IMAGERY._relevant("中环街市", "中環街市", "香港"):
        failures.append("writing variant: the token rule now claims these match, which it cannot "
                        "do across writing systems — the fix is to not run it on exact lookups, "
                        "not to pretend the tokens are equal")
    # The guard the rule exists for must survive: a search that drifts to a different subject.
    if IMAGERY._relevant("阿利坎特中央市场", "阿利坎特轰炸", "阿利坎特"):
        failures.append("writing variant: the relevance rule stopped refusing an article that is "
                        "merely near the place — that is the defect it was written for")

    # The rule above is not where the fix lives, so testing it alone tested nothing: a first
    # version of this file passed while the guard was mutated away. resolve() is the caller that
    # decides whether to run the token rule at all, so it is exercised here with the network
    # stubbed — offline, deterministic, and pointed at the one branch that matters.
    original = IMAGERY._api
    # Keyed by pageid, which is the shape resolve() reads (`pages.values()`); the list form that
    # formatversion=2 returns raised AttributeError here and would have been mistaken for the
    # behaviour under test.
    canned = {"query": {"pages": {"123": {
        "title": "中環街市", "pageimage": "Central_Market.jpg",
        "coordinates": [{"lat": 22.284116, "lon": 114.155481}]}}}}
    try:
        IMAGERY._api = lambda *a, **k: canned
        exact_hit = IMAGERY.resolve("中环街市", (22.2964, 114.1714), "香港", lang="zh", exact=True)
        search_hit = IMAGERY.resolve("中环街市", (22.2964, 114.1714), "香港", lang="zh", exact=False)
    finally:
        IMAGERY._api = original
    if not exact_hit:
        failures.append("writing variant: an EXACT title lookup that the wiki resolved from "
                        "simplified to traditional was refused. `titles=X&redirects=1` returns X "
                        "or its redirect and can return nothing else, so there is no ranking to "
                        "be sceptical of — running the token rule there threw away the article "
                        "with the right photograph")
    if search_hit:
        failures.append("writing variant: a SEARCH result skipped the relevance rule. Search is a "
                        "ranking that drifts, which is why the rule exists; only the exact lookup "
                        "is exempt")
    return failures


def zero_imagery_is_loud_cases() -> list[str]:
    """Filling nothing is a result, and it has to arrive somewhere a reader looks."""
    failures: list[str] = []
    plan = json.loads(FIXTURE.read_text(encoding="utf-8"))
    plan.pop("imagery", None)
    plan.pop("imagery_sidecar", None)
    plan["trip"]["destination"] = "不存在的地方ZZQX"
    plan["destination_experience_anchors"] = [
        {"name": "不存在的锚点ZZQX", "category": "x", "neighborhood_or_area": "x",
         "planned_day": 1, "why_it_matters": "x", "satisfies_preference": "x",
         "source_url": "https://example.invalid/", "checked_at": "2026-08-30"}]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "plan.json"
        path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "fetch_plan_imagery.py"), str(path), "--dry-run"],
            capture_output=True, text=True)
    if "NO IMAGERY" not in result.stderr:
        failures.append("zero imagery: a run that filled nothing said so only in notes on stdout, "
                        "which is how a page shipped with no photographs and nobody looked")
    for cause in ("caption", "lookup key"):
        if cause not in result.stderr:
            failures.append(f"zero imagery: the report does not name {cause!r} as a cause, so it "
                            f"tells the author something is wrong without saying what to change")
    return failures


def declared_prefill_cases() -> list[str]:
    """A declared field must be in the URL as a discrete part, not as a word in a sentence.

    Measured: a delivered plan carried
    `google.com/travel/flights?q=Flights+from+AMS+to+HKG+on+2027-04-17+through+2027-04-22` while
    declaring origin, destination, both dates and travellers prefilled, and passed with zero
    findings. The dates were "in the URL" as text inside one free-text parameter; the other three
    were never looked for. The traveller opened the button and got an empty search box.
    """
    failures: list[str] = []
    # The booking-ready fixture carries no flight, so the flight card is built here rather than
    # borrowed: a test that skips when its subject is absent is a test that reports success on the
    # run that needed it.
    base = json.loads(FIXTURE.read_text(encoding="utf-8"))
    options = base.setdefault("booking_options", {})
    options["flights"] = [{
        "id": "fl-test", "provider": "Test Air", "origin_airport": "AMS",
        "destination_airport": "HKG", "outbound_date": "2027-04-17",
        "return_date": "2027-04-22", "review_url": "https://example.com/air",
        "round_trip_search_provider": "Test", "round_trip_search_checked_at": "2026-08-30",
        "round_trip_search_url": "", "round_trip_prefilled_fields": []}]

    def findings(plan: dict) -> list[str]:
        errors: list[str] = []
        for check in CHECKER.PLAN_CHECKS:
            try:
                check(plan, errors, [])
            except Exception as exc:  # noqa: BLE001 - a raise here hides every other finding
                failures.append(f"prefill: {check.__name__} raised {type(exc).__name__}: {exc}")
        # Matched on the prefill message itself, not on the word "declares": a looser filter
        # caught an unrelated mainland-China map finding from the fixture and reported it as a
        # prefill failure — a test whose filter is wider than its subject fails on work it never
        # examined, which is the same shape as the defects this file is about.
        return [e for e in errors if "prefilled, but the URL" in e]

    flights = ((base.get("booking_options") or {}).get("flights") or [])
    if not flights:
        return failures + ["prefill: the fixture carries no flight to test against"]

    def with_url(url: str) -> dict:
        plan = copy.deepcopy(base)
        for option in plan["booking_options"]["flights"]:
            option["round_trip_search_url"] = url
            option["round_trip_prefilled_fields"] = [
                "origin", "destination", "outbound_date", "return_date", "travellers"]
            option["origin_airport"] = "AMS"
            option["destination_airport"] = "HKG"
            option["outbound_date"] = "2027-04-17"
            option["return_date"] = "2027-04-22"
        plan["trip"]["traveler_count"] = 1
        return plan

    prose = with_url("https://www.google.com/travel/flights"
                     "?q=Flights+from+AMS+to+HKG+on+2027-04-17+through+2027-04-22")
    found = findings(prose)
    if not found:
        failures.append("prefill: a URL whose only parameter is a sentence passed while declaring "
                        "five prefilled fields — that is the delivered defect, unchanged")
    elif not any("free-text" in f for f in found):
        failures.append(f"prefill: the refusal does not say the value sits inside a free-text "
                        f"parameter, which is the part that tells the author what to fix: {found}")

    missing = findings(with_url("https://www.kayak.com/flights"))
    if not missing:
        failures.append("prefill: a URL carrying none of the declared values passed")
    elif not any("does not carry" in f for f in missing):
        failures.append(f"prefill: a wholly absent value is reported with the wording for a "
                        f"buried one; the two need different fixes: {missing}")

    # The honest form, and it must not be punished: providers pack fields into path segments
    # (`AMS-HKG`) and decorate them (`1adults`), and both are still structured.
    structured = findings(with_url(
        "https://www.kayak.com/flights/AMS-HKG/2027-04-17/2027-04-22/1adults"))
    if structured:
        failures.append(f"prefill: a genuinely prefilled path-style URL was refused, which would "
                        f"push authors back to the free-text form: {structured}")

    # Declaring nothing is always honest: a provider that only takes free text can say so.
    quiet = copy.deepcopy(prose)
    for option in quiet["booking_options"]["flights"]:
        option["round_trip_prefilled_fields"] = []
    if findings(quiet):
        failures.append("prefill: declaring no prefilled fields was refused, leaving an author "
                        "with a free-text provider no honest option at all")
    return failures


def containing_place_cases() -> list[str]:
    """An article about the TOWN must not fill a slot asked for the market inside it.

    Measured on a real delivered plan: the anchor "Marché de Vevey" matched the article *Vevey* --
    the town on Lake Geneva -- and a lake photograph was about to be printed under a market's
    heading, with the town's provenance credited beneath it. That is the Larnaca defect this file
    already guards against one level up, arriving through a containing SETTLEMENT rather than
    through the destination, which is the only fall-through the old guard looked for. Sharing one
    specific token was enough, and "Vevey" is a token of "Marché de Vevey".

    Two things make this hard enough to be worth pinning rather than eyeballing:

    * A plain subset rule over-fires. *Lion Monument* is a proper subset of "Lion Monument
      Lucerne" and is exactly the right article; the difference is whether the article dropped the
      SUBJECT or the LOCATION, and the plan's own place names answer that without a gazetteer.
    * The comparison must run on RAW tokens. `castle`, `market`, `church` and `museum` are
      stopwords and their non-English equivalents are not, so cooked, "Chillon Castle" reduces to
      {chillon} -- indistinguishable from a town article -- while "Château de Chillon" keeps
      {château, chillon}. Judged cooked, the guard refused the one correct match the measured trip
      actually found.
    """
    failures: list[str] = []
    trip_places = frozenset({"lucerne", "琉森", "montreux", "蒙特勒", "bern", "伯尔尼",
                             "switzerland", "瑞士", "拉纳卡", "东京"})
    cases = (
        # (query, article title, destination, expected, why)
        ("Marché de Vevey", "Vevey", "瑞士", False,
         "the town standing in for the market inside it -- the measured defect"),
        ("拉纳卡市政市场", "拉纳卡", "拉纳卡", False,
         "the same shape in Chinese, where the destination guard already covers it"),
        ("Luzerner Wochenmarkt", "Luzern", "瑞士", False,
         "a market answered with its city"),
        ("Château de Chillon", "Chillon Castle", "瑞士", True,
         "the subject survives on both sides once stopwords are not stripped"),
        ("Lion Monument Lucerne", "Lion Monument", "瑞士", True,
         "the article dropped the LOCATION, not the subject"),
        ("Kapellbrücke", "Kapellbrücke", "瑞士", True,
         "an exact title must not be read as a proper subset of itself"),
        ("Alicante Central Market", "Bombing of Alicante", "Alicante", False,
         "the rule this guard sits beside still holds"),
    )
    for query, title, place, expected, why in cases:
        got = IMAGERY._relevant(query, title, place, trip_places)
        if got is not expected:
            failures.append(
                f"containing place: _relevant({query!r}, {title!r}) is {got}, expected {expected} "
                f"-- {why}")

    # Token overlap alone cannot finish this job, and the measured trip proved it in one step:
    # refusing the town *Vevey* moved the search onto *Vevey railway station*, which shares the
    # same single place token and carries its own extra ones -- structurally identical to
    # "Château de Chillon"/"Chillon Castle", which is correct. Separating them needs the subject
    # CLASS, which Wikipedia's own short description states as its opening noun and which rides
    # along in the call the module already makes.
    descriptions = (
        ("Marché de Vevey", "Vevey", "Town in Vaud, Switzerland", False,
         "a town article standing in for the market on its lakefront"),
        ("Marché de Vevey", "Vevey railway station", "Railway station in Vevey, Switzerland", False,
         "the station the search reached once the town was refused"),
        ("Château de Chillon", "Chillon Castle", "Castle in Veytaux, Switzerland", True,
         "a castle is not a container class and must still pass"),
        ("Kapellbrücke", "Kapellbrücke", "Bridge across the Reuss River in Lucerne", True,
         "nor is a bridge"),
        # The class is the description's OPENING noun, not any word anywhere in it. A castle
        # whose description happens to mention the town it stands in is still a castle, and
        # reading the whole string would refuse it.
        ("Château de Chillon", "Chillon Castle", "Castle in the town of Veytaux, Switzerland", True,
         "a container word later in the sentence is not the subject class"),
        # And the class only disqualifies when the query did NOT ask for it: an anchor that is
        # itself a district may have the district's article.
        ("Bern old town district", "Bern Altstadt", "District of Bern, Switzerland", True,
         "the query asked for a district, so a district article is the right answer"),
        # CJK is covered by a DIFFERENT mechanism, and the attempt to add a Chinese class list
        # here is why that is now written down. `_tokens` treats a CJK run as one token, so
        # 「沃韦市集」 and 「沃韦市」 share nothing and are refused one check earlier; the only way a
        # Chinese description reaches the class guard is when query and title are the same run, and
        # then the article IS what was asked for. A list that cannot fire where it would help and
        # misfires where it can is coverage on paper. Asserted here so nobody adds it again.
        ("沃韦市集", "沃韦市", "瑞士沃州市镇", False,
         "refused by the token rule, not by the class guard -- CJK runs do not overlap"),
        ("长洲", "长洲", "香港的離島", True,
         "same run means the article IS the anchor; a class guard must not refuse it"),
        # An anchor that IS a place name may have that place's article. The trip's own vocabulary
        # is what makes this decidable.
        ("东京", "东京", "日本東京都的城市", True,
         "a stop that is itself a city, with 东京 in the trip vocabulary"),
        ("Lion Monument", "Lion Monument, Lucerne", None, True,
         "no description is no evidence, and no evidence is not a refusal"),
        # Stated rather than wished away: the two guards overlap, and an anchor that genuinely
        # wants the town's own photograph ("Vevey old town") is refused by the subset rule even
        # though the description rule would clear it. That costs a legitimate image, and it is the
        # direction this file is supposed to err in -- "when a slot cannot be filled to that
        # standard it stays empty", never a substitute. Asserted so the cost is visible rather
        # than discovered later as a surprise.
        ("Vevey old town", "Vevey", "Town in Vaud, Switzerland", False,
         "conservative: the subset rule refuses it even though the description rule would not"),
    )
    for query, title, description, expected, why in descriptions:
        got = IMAGERY._relevant(query, title, "瑞士", trip_places, description)
        if got is not expected:
            failures.append(
                f"subject class: _relevant({query!r}, {title!r}, description={description!r}) is "
                f"{got}, expected {expected} -- {why}")

    # The destination hero legitimately IS a settlement article, and the guard must never reach it:
    # "Federal city of Switzerland" would otherwise delete the opening photograph of every trip.
    for hero in ("伯尔尼", "Bern"):
        if not IMAGERY._relevant(hero, hero, hero, trip_places, "Federal city of Switzerland"):
            failures.append(f"subject class: the destination hero {hero!r} was refused for being a "
                            f"settlement -- the guard belongs on anchors only")

    # The vocabulary has to come from the plan's own fields, or the Lion Monument case cannot be
    # told from the Vevey one. An empty vocabulary must still refuse the town.
    if IMAGERY._relevant("Marché de Vevey", "Vevey", "瑞士", frozenset()):
        failures.append("containing place: an empty place vocabulary still has to refuse the town")

    # Every source contributes a name found in NO other source, or dropping one of them still
    # passes -- which is how the first version of this case reported a green mutation: 伯尔尼 was
    # in the destination string as well as in base_location, so deleting the base_location read
    # was invisible.
    plan = {"trip": {"destination": "瑞士行程",
                     "destination_coords": [{"label": "蒙特勒"}]},
            "booking_options": {"accommodations": [{"stay_location": "格林德瓦"}]},
            "days": [{"base_location": "因特拉肯",
                      "route": {"stops_in_order": ["翁根", "卡佩尔廊桥"]}}]}
    vocabulary = IMAGERY.place_vocabulary(plan)
    for wanted in ("蒙特勒", "格林德瓦", "因特拉肯", "翁根"):
        if wanted not in vocabulary:
            failures.append(f"containing place: place_vocabulary lost {wanted!r} -- it is read from "
                            f"the plan's own destination, stays, bases and stops")
    return failures


def main() -> int:
    failures: list[str] = []
    failures += cjk_token_cases()
    failures += writing_variant_cases()
    failures += zero_imagery_is_loud_cases()
    failures += declared_prefill_cases()
    failures += containing_place_cases()
    if failures:
        print(f"LOOKUP KEYS AND CLAIMS FAILED ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all lookup-key and declared-claim cases passed")
    return 0


def test_lookup_keys_and_claims() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
