#!/usr/bin/env python3
"""A leg's speed has to be survivable by its mode, and its button has to open that mode.

Two holes a synthetic English self-drive trip found on 2026-09-24, and the real workspace confirmed:

* No ceiling on anything but walking. check_implied_speed capped a walk at 6 km/h and floored
  transit at 4 km/h, so a 118 km drive claimed in 20 minutes -- 354 km/h -- passed every gate. On a
  self-drive trip the drive time is what the whole day is planned around.
* Nothing compared a segment's button with the segment's own mode. A walking leg whose button asked
  for driving directions passed; in the real workspace, 20 taxi and ride-hail legs carried Amap
  buttons in bus mode, so the traveller pressing "open this leg" got a bus route for a taxi ride.

Modes are free text, mostly Chinese, so classification is conservative: a leg is judged only when
its words name one class and its button names a contradicting one. An ambiguous leg such as
「公共交通或网约车」 is skipped, not guessed. On a self-drive trip an unclassified non-walking leg is
a road leg, because that is what self-drive means.

Run:  python tests/test_travel_modes.py
      python -m pytest tests/test_travel_modes.py
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
BASE = json.loads(FIXTURE.read_text(encoding="utf-8"))

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def with_leg(mode: str, km: float, minutes: float, *, url: str | None = None,
             self_drive: bool = False) -> dict:
    plan = copy.deepcopy(BASE)
    segment = plan["days"][0]["route"]["segments"][0]
    segment.update(mode=mode, distance_km=km, duration_minutes=minutes)
    if url is not None:
        segment["verified_map_url"] = url
    if self_drive:
        plan["transport_preference"]["mode"] = "self-drive"
    return plan


def run(name: str, plan: dict) -> list[str]:
    check_fn = getattr(cpc, name, None)
    if check_fn is None:
        failures.append(f"{name} does not exist")
        return []
    errors: list[str] = []
    check_fn(plan, errors, [])
    return [e for e in errors if "segment 1" in e]


def main() -> int:
    classify = getattr(cpc, "_mode_class", None)
    if classify is None:
        failures.append("_mode_class does not exist")
    else:
        for words, expected in (("步行", "walk"), ("walk", "walk"), ("网约车", "car"),
                                ("self-drive", "car"), ("机场巴士", "bus"), ("水上巴士", "ferry"),
                                ("古董电车与火车", "rail"), ("metro", "rail"),
                                ("地铁/机场巴士/网约车（择一）", "mixed"),
                                ("公共交通或网约车", "mixed"), ("直飞航班", "air"),
                                # its own class, which names no map mode: still never judged, and
                                # no longer a road leg on a self-drive trip the way None made it
                                ("缆车", "lift")):
            check(f"{words!r} is classified {expected!r}", classify(words) == expected,
                  classify(words))

    # Speed ceilings.
    check("a 118 km drive in 20 minutes is refused",
          run("check_implied_speed", with_leg("驾车", 118, 20)), "354 km/h passed")
    check("a 118 km drive in 90 minutes passes",
          not run("check_implied_speed", with_leg("驾车", 118, 90)))
    check("a 300 km high-speed rail hour passes",
          not run("check_implied_speed", with_leg("高铁", 300, 60)))
    check("an unclassified leg on a self-drive trip is a road leg",
          run("check_implied_speed", with_leg("Loch road", 118, 20, self_drive=True)),
          "354 km/h passed on a self-drive trip")
    check("an unclassified leg on a public-transit trip is not guessed",
          not run("check_implied_speed", with_leg("Loch road", 118, 20)))

    # The button opens the leg's own mode.
    google = "https://www.google.com/maps/dir/?api=1&origin=1,2&destination=3,4&travelmode="
    amap = "https://uri.amap.com/navigation?from=104.0665,30.5723,A&to=104.07,30.6,B&mode="
    check("a walking leg whose button drives is refused",
          run("check_map_link_modes", with_leg("步行", 1, 15, url=google + "driving")))
    check("a ride-hail leg whose button opens bus directions is refused",
          run("check_map_link_modes", with_leg("网约车", 4, 12, url=amap + "bus")))
    check("a metro leg with transit directions passes",
          not run("check_map_link_modes", with_leg("地铁", 4, 20, url=google + "transit")))
    check("a walking leg with Amap walking directions passes",
          not run("check_map_link_modes", with_leg("步行", 1, 15, url=amap + "walk")))
    check("an ambiguous leg is not judged",
          not run("check_map_link_modes", with_leg("公共交通或网约车", 4, 15, url=amap + "car")))
    check("a self-drive leg whose button opens walking directions is refused",
          run("check_map_link_modes", with_leg("A9 north", 118, 90, url=google + "walking",
                                               self_drive=True)))

    # Words one class borrows from another are not that class. `car` matched "cable car" and
    # "street car", so a cable-car leg with a transit button was told to switch to driving; "Le
    # Shuttle" -- the car train under the Channel -- was a bus; and a self-drive trip's vehicle ferry
    # was told its driving directions were wrong, when driving directions are the ones that include
    # the crossing. An aerial lift names no map mode at all, on any trip.
    if classify is not None:
        for words in ("Cable car to the summit", "Street car", "Sleeper car", "缆车"):
            check(f"{words!r} is not judged as a car", classify(words) != "car", classify(words))
    check("a cable-car leg with transit directions passes",
          not run("check_map_link_modes", with_leg("Cable car to the summit", 2, 10,
                                                   url=google + "transit")))
    check("a cable-car leg on a self-drive trip is not a road leg",
          not run("check_map_link_modes", with_leg("缆车", 2, 10, url=google + "walking",
                                                   self_drive=True)))
    check("Le Shuttle on a self-drive trip with driving directions passes",
          not run("check_map_link_modes", with_leg("Eurotunnel Le Shuttle", 50, 35,
                                                   url=google + "driving", self_drive=True)))
    check("a vehicle ferry on a self-drive trip with driving directions passes",
          not run("check_map_link_modes", with_leg("CalMac ferry Uig to Tarbert", 45, 100,
                                                   url=google + "driving", self_drive=True)))
    check("a ferry on a self-drive trip with walking directions is still refused",
          run("check_map_link_modes", with_leg("CalMac ferry Uig to Tarbert", 45, 100,
                                               url=google + "walking", self_drive=True)))
    check("a foot-passenger ferry on a public-transit trip with driving directions is refused",
          run("check_map_link_modes", with_leg("Ferry to the island", 12, 40,
                                               url=google + "driving")))
    check("a hire car with transit directions is still refused",
          run("check_map_link_modes", with_leg("Hire car", 30, 30, url=google + "transit")))
    check("an airport shuttle bus is still a bus",
          classify is None or classify("Airport shuttle bus") == "bus",
          classify and classify("Airport shuttle bus"))

    # Words a plan outside the author's Chinese workspace writes. Probed 2026-09-24 on 46 mode
    # strings: 34 named no class, so the check was blind to London's Tube, Singapore's MRT, a
    # vaporetto, a hike -- and 电动车 (an e-bike or e-scooter) read as rail because it contains 动车
    # (a bullet train), which tells a scooter leg to open public-transport directions.
    if classify is not None:
        for words, expected in (
                ("Tube (Piccadilly line)", "rail"), ("London Overground", "rail"), ("DLR", "rail"),
                ("MRT (East-West line)", "rail"), ("LRT", "rail"), ("MTR Island line", "rail"),
                ("BTS Skytrain", "rail"), ("RER B", "rail"), ("Monorail", "rail"),
                ("Minibus", "bus"), ("Trolleybus", "bus"),
                ("Vaporetto line 1", "ferry"), ("Catamaran", "ferry"), ("Hydrofoil", "ferry"),
                ("Speedboat", "ferry"), ("Water taxi", "ferry"),
                ("Hike to the viewpoint", "walk"), ("Stroll along the river", "walk"),
                ("Rideshare", "car"), ("Minicab", "car"), ("DiDi", "car"),
                ("滴滴", "car"), ("专车", "car"), ("拼车", "car"), ("城际列车", "rail"),
                ("磁悬浮", "rail"), ("捷运淡水线", "rail"), ("港铁", "rail"), ("坐船", "ferry"),
                ("快艇", "ferry"), ("散步", "walk"), ("Bike", "bike"), ("骑电动车", "bike")):
            check(f"{words!r} is classified {expected!r}", classify(words) == expected,
                  classify(words))
        for words in ("电动车", "机动车道边步行", "YouTube video stop"):
            check(f"{words!r} is not a rail leg", classify(words) != "rail", classify(words))
    check("an e-bike leg with walking directions is not told to take public transport",
          not run("check_map_link_modes", with_leg("电动车", 3, 12, url=amap + "walk")))
    check("a Tube leg whose button drives is refused",
          run("check_map_link_modes", with_leg("Tube (Piccadilly line)", 8, 25,
                                               url=google + "driving")))
    # From the fresh review: 单车 (bike) is also the head of 单车道 (a single-lane road), and plans in
    # Traditional Chinese were unclassified -- on a self-drive trip an unclassified leg is a road
    # leg, so 搭捷運 with a transit button was told to switch to driving.
    if classify is not None:
        for words, expected in (("自驾（单车道山路）", "car"), ("單車道山路自駕", "car"),
                                ("搭捷運", "rail"), ("地鐵", "rail"), ("高鐵", "rail"),
                                ("公車", "bus"), ("客運", "bus"), ("計程車", "car"),
                                ("腳踏車", "bike"), ("渡輪", "ferry"), ("纜車", "lift")):
            check(f"{words!r} is classified {expected!r}", classify(words) == expected,
                  classify(words))
        check("'電動車' is not a rail leg", classify("電動車") != "rail", classify("電動車"))
    check("a Traditional-Chinese metro leg on a self-drive trip keeps its transit button",
          not run("check_map_link_modes", with_leg("搭捷運", 8, 25, url=google + "transit",
                                                   self_drive=True)))
    check("a vaporetto leg with transit directions passes",
          not run("check_map_link_modes", with_leg("Vaporetto line 1", 3, 20,
                                                   url=google + "transit")))

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("travel mode cases passed")
    return 0


def test_travel_modes() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
