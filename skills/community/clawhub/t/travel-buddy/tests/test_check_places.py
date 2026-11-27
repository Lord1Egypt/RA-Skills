"""check_places.py against canned OpenStreetMap answers, and the verified-save gate that reads it.

The plan is a cut-down copy of the Alicante case that motivated the script: a "hotel" pin on City
Hall, a walk from it that is really over the traveller's limit, a dinner at a venue no map lists,
and a port pin at the middle of the whole harbour. Offline: every request is answered from a table.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_places as CP  # noqa: E402
from check_plan_consistency import check_place_check  # noqa: E402

CITY_HALL = (38.34520, -0.48150)
HOTEL = (38.33862, -0.49486)
MARQ = (38.353885, -0.476215)
PORT = (38.328293, -0.494711)
EXPLANADA = (38.343141, -0.483295)


def gmaps(a, b, mode):
    return (f"https://www.google.com/maps/dir/?api=1&origin={a[0]}%2C{a[1]}"
            f"&destination={b[0]}%2C{b[1]}&travelmode={mode}")


PLAN = {
    "trip": {"destination": "阿利坎特", "destination_coords": {"lat": 38.3452, "lon": -0.4815},
             "traveler_constraints": {"max_continuous_walking_minutes": 30}},
    "booking_options": {"accommodations": [{"id": "acc-1", "property_name": "AC Hotel by Marriott Alicante"}]},
    "days": [
        {"accommodation_option_id": "acc-1",
         "dining": [{"venue_name": "Cervecería Sánchez"}, {"venue_name": "Nou Manolin"},
                    {"venue_name": "人形町 站前一带（当日择店）"}],
         "route": {"segments": [
             {"from": "住宿（市中心一带）", "to": "MARQ 考古博物馆", "mode": "步行", "duration_minutes": 22,
              "verified_map_url": gmaps(CITY_HALL, MARQ, "walking")},
             {"from": "埃斯普拉纳达海滨长廊（Explanada de España）", "to": "阿利坎特港（Puerto de Alicante）",
              "mode": "公交", "duration_minutes": 18, "verified_map_url": gmaps(EXPLANADA, PORT, "transit")},
         ]}},
    ],
}


def place(name, point, box=None, osm_id=1):
    return {"name": name, "display_name": name, "lat": str(point[0]), "lon": str(point[1]),
            "osm_type": "way", "osm_id": osm_id,
            "boundingbox": [str(v) for v in (box or (point[0] - 0.0005, point[0] + 0.0005,
                                                    point[1] - 0.0005, point[1] + 0.0005))]}


SEARCH = {
    "AC Hotel by Marriott Alicante": [],
    "AC Hotel Alicante": [place("Hotel AC Alicante", HOTEL)],
    "Nou Manolin": [place("Nou Manolin", (38.3466, -0.4846))],
    "Explanada de España": [place("Explanada d'Espanya", EXPLANADA)],
    "Puerto de Alicante": [place("Port d'Alacant", PORT, box=(38.319, 38.3386, -0.5021, -0.4825))],
}


def fake_fetch(url: str):
    parsed = urlparse(url)
    query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
    if parsed.path.endswith("/reverse"):
        if query.get("zoom") == "10":
            return {"address": {"city": "Alacant / Alicante"}}
        return {"display_name": "1, Plaça de l'Ajuntament, Alacant"}
    if parsed.path.endswith("/search"):
        return SEARCH.get(query["q"], [])
    if "routed-foot" in url:
        # hotel -> MARQ is 2.8 km, 38 minutes on foot; anything else is short.
        if f"{HOTEL[1]},{HOTEL[0]}" in url:
            return {"code": "Ok", "routes": [{"duration": 2254, "distance": 2805}]}
        return {"code": "Ok", "routes": [{"duration": 600, "distance": 800}]}
    raise AssertionError(f"unexpected request {url}")


def run(plan, fetch=fake_fetch):
    return CP.run(plan, CP.Net(delay=0, fetch=fetch))


def by_pointer(findings):
    return {(f["kind"], f["pointer"]): f for f in findings}


def test_finds_the_alicante_defects() -> None:
    findings, checked, notes = run(PLAN)
    found = by_pointer(findings)

    hotel_pin = found[("pin", "days[0].route.segments[0].from")]
    assert hotel_pin["verdict"] == "wrong" and "Ajuntament" in hotel_pin["correction"]

    walk = found[("walk", "days[0].route.segments[0]")]
    assert walk["severity"] == "critical" and "38 minutes" in walk["correction"]
    assert "real hotel location" in walk["correction"]

    venue = found[("venue", "days[0].dining[0].venue_name")]
    assert venue["verdict"] == "unverifiable"
    assert ("venue", "days[0].dining[1].venue_name") not in found       # Nou Manolin exists

    port = found[("pin", "days[0].route.segments[1].to")]
    assert port["verdict"] == "misleading" and "km across" in port["correction"]

    # Every input was examined; the area "venue" was never an input at all.
    assert set(checked) == CP.input_keys(PLAN)
    assert not any(key.startswith("venue|") and "一带" in key for key in checked)


def test_silent_service_leaves_inputs_uncovered() -> None:
    def down(url):
        raise OSError("network unreachable")
    findings, checked, notes = run(PLAN, fetch=down)
    assert not findings and not checked
    assert any("did not answer" in n for n in notes) or any("nothing to check" in n for n in notes)


def test_rerun_keeps_resolutions() -> None:
    findings, _, _ = run(PLAN)
    old = [dict(f, resolved=True, resolution="confirmed on the venue's own site")
           for f in findings if f["kind"] == "venue"]
    again, _, _ = run(PLAN)
    merged = by_pointer(CP.merge_resolutions(again, old))
    assert merged[("venue", "days[0].dining[0].venue_name")]["resolution"].startswith("confirmed")


def test_label_queries() -> None:
    assert CP.label_query("中央市场（Mercado Central）") == "Mercado Central"
    assert CP.label_query("Mercado Central 内熟食摊") == "Mercado Central"
    assert CP.label_query("阿利坎特-埃尔切机场（ALC）") == "ALC airport"
    assert "Hotel Maya Alicante" in CP.hotel_queries("Sercotel Maya Alicante")


def _gate(plan) -> list[str]:
    errors: list[str] = []
    check_place_check(plan, errors, [])
    return errors


def test_gate_on_verified_saves() -> None:
    plan = copy.deepcopy(PLAN)
    plan["verification_status"] = "verified"
    assert any("carries no place_check" in e for e in _gate(plan))

    findings, checked, _ = run(plan)
    plan["place_check"] = {"inputs": checked, "findings": findings}
    errors = _gate(plan)
    assert any("unresolved" in e and "segments[0]" in e for e in errors)
    assert not any("dining[0]" in e for e in errors), "an unverifiable venue does not block the save"

    for f in plan["place_check"]["findings"]:
        f.update(resolved=True, resolution="re-pinned and re-routed")
    assert _gate(plan) == []

    plan["days"][0]["route"]["segments"][0]["verified_map_url"] = gmaps(HOTEL, MARQ, "walking")
    assert any("does not cover" in e for e in _gate(plan)), "an edited pin needs a rerun"

    draft = copy.deepcopy(PLAN)
    draft["verification_status"] = "unverified"
    assert _gate(draft) == [], "an unverified plan already carries its banner"


def test_verification_needs_fresh_eyes() -> None:
    """The authoring session cannot verify its own plan, and a report has to say who did."""
    from check_plan_consistency import check_verification  # noqa: PLC0415

    def errors_for(mode):
        report = {"checked_at": "2026-08-03", "plan": "plan.json", "domains": [], "audits": []}
        if mode is not None:
            report["verification_mode"] = mode
        errors: list[str] = []
        check_verification(report, errors, [])
        return [e for e in errors if "verification_mode" in e]

    assert any("same_session" in e for e in errors_for("same_session"))
    assert errors_for(None), "a report that does not say who checked is refused"
    assert errors_for("thorough"), "an invented mode is refused"
    assert errors_for("independent_agents") == []
    assert errors_for("separate_processes") == []


def test_next_steps_panel_leads_with_the_all_in_cost() -> None:
    """The page opens with the real per-person total and the open decisions, in the trip language."""
    from render_final_trip_html import labels_for, next_steps_panel  # noqa: PLC0415

    plan = {
        "trip": {"currency": "EUR"},
        "budget": {"breakdown": [{"per_person_low": 154, "per_person_high": 154},
                                 {"per_person_low": 505, "per_person_high": 505},
                                 {"per_person_low": 187, "per_person_high": 316}]},
        "booking_options": {"flights": [{"id": "fl-1", "price_checked_at": "2026-08-09"}],
                            "accommodations": [{"id": "acc-1", "checked_at": "2026-08-10"}]},
        "bookings": [{"option_id": "acc-1", "state": "booked"}],
        "days": [{"number": 2, "dining": [{"venue_name": "Nou Manolin", "reservation_need": "required"}]}],
        "place_check": {"findings": [
            {"kind": "venue", "label": "Cervecería Sánchez"},
            {"kind": "walk", "label": "Hotel → MARQ", "routed_minutes": 38, "planned_minutes": 22},
            {"kind": "venue", "label": "Settled Bar", "resolution": "confirmed on its own site"}]},
    }
    en = next_steps_panel(plan, labels_for("en"))
    assert "EUR 846–975 per person" in en
    assert "Choose and book a flight: 1 option(s), prices checked 2026-08-09" in en
    assert "a place to stay" not in en, "a booked stay is not an open decision"
    assert "Reserve Nou Manolin (day 2" in en
    assert "Cervecería Sánchez" in en and "about 38 minutes" in en
    assert "Settled Bar" not in en, "a resolved place finding is no longer open"

    zh = next_steps_panel(plan, labels_for("zh-CN"))
    assert "下单前要做的事" in zh and "人均全部花费 EUR 846–975" in zh
    assert "Before you book" not in zh and "per person" not in zh


# ---------------------------------------------------------------- mainland China and the taxi card

BJ_HOTEL_WGS = (39.93539, 116.43724)      # 北京东直门智选假日酒店 as OSM places it


def amap_url(a, b):
    """An Amap navigation link, written the way Amap writes it: lon,lat in GCJ-02."""
    ga, gb = CP.wgs_to_gcj(a), CP.wgs_to_gcj(b)
    return (f"https://uri.amap.com/navigation?from={ga[1]:.6f},{ga[0]:.6f},A"
            f"&to={gb[1]:.6f},{gb[0]:.6f},B&mode=walk")


def test_gcj_round_trip_and_known_offset() -> None:
    wgs = (39.9087, 116.3975)                      # Tiananmen
    gcj = CP.wgs_to_gcj(wgs)
    assert abs(gcj[0] - 39.91010) < 2e-4 and abs(gcj[1] - 116.40374) < 2e-4
    back = CP.gcj_to_wgs(gcj)
    assert abs(back[0] - wgs[0]) < 1e-6 and abs(back[1] - wgs[1]) < 1e-6
    assert CP.gcj_to_wgs((38.3452, -0.4815)) == (38.3452, -0.4815), "no offset outside China"


def _beijing_plan(pin_wgs):
    return {
        "trip": {"destination": "北京", "destination_coords": {"lat": 39.93, "lon": 116.43}},
        "booking_options": {"accommodations": [{"id": "acc-1", "property_name": "北京东直门智选假日酒店"}]},
        "days": [{"accommodation_option_id": "acc-1", "dining": [{"venue_name": "四季民福烤鸭店"}],
                  "route": {"segments": [{"from": "北京朝阳站", "to": "北京东直门智选假日酒店", "mode": "公交",
                                          "duration_minutes": 30,
                                          "verified_map_url": amap_url((39.94, 116.48), pin_wgs)}]}}]}


def _china_fetch(amap_answers):
    def fetch(url):
        parsed = urlparse(url)
        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        if url.startswith(CP.AMAP_PLACE):
            return {"status": "1", "pois": amap_answers.get(query["keywords"], [])}
        if parsed.path.endswith("/reverse"):
            return {"display_name": "左家庄桥, 朝阳区, 北京市", "address": {"city": "北京市"}}
        if parsed.path.endswith("/search"):
            if query["q"].startswith("北京东直门智选假日酒店"):
                return [dict(place("北京东直门智选假日酒店", BJ_HOTEL_WGS),
                             address={"road": "春秀路", "house_number": "1号", "city": "北京市"})]
            return []
        raise AssertionError(f"unexpected request {url}")
    return fetch


def test_amap_pins_are_converted_and_checked() -> None:
    """Before the conversion, all 30 Amap pins of a Beijing plan were skipped unchecked."""
    right = _beijing_plan(BJ_HOTEL_WGS)
    findings, checked, notes = run(right, fetch=_china_fetch({}))
    assert set(checked) == CP.input_keys(right)
    assert not [f for f in findings if f["kind"] == "pin"], "a correct GCJ-02 pin is not 500 m off"
    assert any("AMAP_KEY" in n for n in notes)

    wrong = _beijing_plan((39.94963, 116.44079))   # the real plan's pin: 1.6 km north, at 左家庄桥
    findings, _, _ = run(wrong, fetch=_china_fetch({}))
    pin = by_pointer(findings)[("pin", "days[0].route.segments[0].to")]
    assert pin["verdict"] == "wrong" and "1,6" in pin["correction"]


def test_amap_key_looks_names_up_on_amap_and_records_the_address() -> None:
    gcj = CP.wgs_to_gcj(BJ_HOTEL_WGS)
    answers = {
        "北京东直门智选假日酒店": [{"id": "B0", "name": "智选假日酒店(北京东直门店)", "cityname": "北京市",
                              "adname": "东城区", "address": "春秀路1号", "location": f"{gcj[1]},{gcj[0]}"}],
        "四季民福烤鸭店": [{"id": "B1", "name": "四季民福烤鸭店(东四十条店)", "cityname": "北京市",
                       "adname": "东城区", "address": "东四十条", "location": f"{gcj[1]},{gcj[0]}"}],
    }
    plan = _beijing_plan(BJ_HOTEL_WGS)
    addresses: list = []
    findings, checked, _ = CP.run(plan, CP.Net(delay=0, fetch=_china_fetch(answers), amap_key="k"), addresses)
    assert set(checked) == CP.input_keys(plan)
    assert not findings, findings
    assert addresses == [{"pointer": "booking_options.accommodations[0].property_name",
                          "property_name": "北京东直门智选假日酒店", "local_name": "智选假日酒店(北京东直门店)",
                          "address": "北京市 东城区 春秀路1号", "lat": addresses[0]["lat"],
                          "lon": addresses[0]["lon"], "source": "Amap"}]
    assert abs(addresses[0]["lat"] - BJ_HOTEL_WGS[0]) < 1e-5, "stored in WGS-84, not GCJ-02"


def test_osm_address_is_recorded_in_the_local_language() -> None:
    def fetch(url):
        data = fake_fetch(url)
        if isinstance(data, list):
            for item in data:
                item["address"] = {"road": "Avenida de Elche", "house_number": "3", "postcode": "03008",
                                   "city": "Alacant / Alicante"}
        return data
    addresses: list = []
    CP.run(PLAN, CP.Net(delay=0, fetch=fetch), addresses)
    assert addresses[0]["local_name"] == "Hotel AC Alicante"
    assert addresses[0]["address"] == "Avenida de Elche 3, 03008 Alacant / Alicante"
    assert addresses[0]["source"] == "OpenStreetMap"


def test_driver_card_shows_the_local_address_in_the_trip_language() -> None:
    from render_final_trip_html import driver_card_panel, labels_for  # noqa: PLC0415
    plan = {"place_check": {"addresses": [{"pointer": "p", "property_name": "AC Hotel by Marriott Alicante",
                                           "local_name": "Hotel AC Alicante",
                                           "address": "Avenida de Elche 3, 03008 Alacant / Alicante",
                                           "source": "OpenStreetMap"}]}}
    zh = driver_card_panel(plan, labels_for("zh-CN"))
    assert "给司机看的地址" in zh and "Avenida de Elche 3" in zh and "AC Hotel by Marriott Alicante" in zh
    assert "Show the driver" not in zh
    assert "Show the driver" in driver_card_panel(plan, labels_for("en"))
    assert driver_card_panel({}, labels_for("en")) == "", "no addresses, no card"


def test_a_hotel_match_must_be_the_property_and_nearby_for_the_taxi_card() -> None:
    """Measured on a Milan plan: 'LE COLONNE MILANO' matched the restaurant 'Todos a Cuba' 190 m
    away and 'Nuvola B&B' matched 'La Nuvola' in Poland, and both went onto the taxi card."""
    assert not CP.names_property({"name": "Todos a Cuba"}, "LE COLONNE MILANO", "Milano")
    assert CP.names_property({"name": "Hotel AC Alicante"}, "AC Hotel by Marriott Alicante", "Alicante")

    plan = {"trip": {"destination": "Milano", "destination_coords": {"lat": 45.4642, "lon": 9.1916}},
            "booking_options": {"accommodations": [{"id": "acc-1", "property_name": "Nuvola B&B"},
                                                   {"id": "acc-2", "property_name": "LE COLONNE MILANO"}]},
            "days": []}

    def fetch(url):
        parsed = urlparse(url)
        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        if parsed.path.endswith("/reverse"):
            return {"address": {"city": "Milano"}}
        if query["q"].startswith("Nuvola"):
            return [place("La Nuvola", (52.159319, 20.79972))]          # Pruszków, Poland
        if "COLONNE" in query["q"].upper():
            return [place("Todos a Cuba", (45.457845, 9.180508))]
        return []
    addresses: list = []
    findings, _, _ = CP.run(plan, CP.Net(delay=0, fetch=fetch), addresses)
    assert addresses == [], "neither match is the property near the destination"
    colonne = by_pointer(findings)[("hotel", "booking_options.accommodations[1].property_name")]
    assert colonne["verdict"] == "unverifiable"
