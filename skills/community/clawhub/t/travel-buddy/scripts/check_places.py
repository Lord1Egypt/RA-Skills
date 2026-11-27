#!/usr/bin/env python3
"""Check the plan's places against OpenStreetMap: is each pin where its label says, does each
named venue exist, and how long is each walk really.

Usage: python check_places.py <plan.json> [--into] [--json out.json] [--delay 1.1]

WHY THIS EXISTS
---------------
Every walking check in `check_plan_consistency.py` reads the plan's own numbers. When a pin or a
distance is wrong, the check passes on wrong input. A verified Alicante plan put its "hotel" pin
on City Hall, 1.4 km from the hotel it booked, so every "12-minute walk from the hotel" was
measured from the wrong building. The walk to MARQ is really about 38 minutes, over the
traveller's 30-minute limit. The same plan scheduled two dinners at a restaurant that no source
could find in the city, while saying its rating had been read off a map page. All three are
decidable from public map data, so this script decides them instead of asking a reviewer to
notice.

WHAT IT DOES
------------
- hotel: geocodes each accommodation's `property_name` near the destination.
- pin: for each map-button endpoint whose label names the hotel, compares the pin with the
  geocoded hotel. For other labels, compares the pin with the nearest OSM match for the label.
- walk: re-routes every walking segment on OSM foot routing, from the real hotel when the leg
  starts or ends there, and compares it with the plan's minutes and the traveller's walking cap.
- venue: looks each dining `venue_name` up near the destination.

A venue OSM cannot find is `unverifiable`, not `wrong`: OSM misses many small restaurants. It
still reaches the page, through the plan's `place_check` block, until someone confirms it from a
real listing and writes that into `resolution`.

`--into` writes the result into the plan as `place_check` and keeps any `resolved`/`resolution`
already written for the same finding. `check_plan_consistency.py` refuses a verified save whose
`place_check` does not cover the plan's current places, so editing a pin means running this again.

NETWORK AND PRIVACY
-------------------
Sends place names and coordinates (never anything about the traveller) to
nominatim.openstreetmap.org and routing.openstreetmap.de, at most one request per second to
Nominatim as its usage policy asks. An input the network could not answer is left out of
`inputs`, so the gate still asks for a rerun rather than treating it as checked.

MAINLAND CHINA
--------------
Amap pins are written in GCJ-02, China's offset datum, which sits a few hundred metres from the
WGS-84 that OpenStreetMap uses. They are converted before any comparison. Before that conversion
existed, the 30 Amap pins and walks of a Beijing plan were skipped outright. OpenStreetMap lists
few hotels and restaurants in mainland China: none of the four hotels in a Shenzhen plan were
found. So with `AMAP_KEY` set to an Amap Web Service key (free from lbs.amap.com), hotels,
venues and pin labels inside mainland China are looked up on Amap's place search, which also
sends their names to Amap. Without the key they go to OSM as before and a note says why so
many come back unverifiable.

ADDRESSES
---------
Each hotel found is recorded with its name and address as the map writes them, in the local
language, under `place_check.addresses`. The page prints them as a card to show a taxi driver,
which works when the phone is offline. A match counts only when its name carries the property's
own words (`names_property`) and it lies near the destination; otherwise the hotel is looked up by
its `address_or_location_reference`, because OSM often has the building but not a small hotel's
name. On a Milan plan the unguarded lookup matched a restaurant 190 m away for one hotel and a
place in Poland for another.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_plan_consistency import (  # noqa: E402
    _endpoint_coords, _great_circle_km, _is_walk, _lon_first, _map_endpoints, _num, _obj, _seq)

UA = "travel-buddy-skill (place check; https://github.com/dong845/travel-buddy)"
NOMINATIM = "https://nominatim.openstreetmap.org"
FOOT_ROUTER = "https://routing.openstreetmap.de/routed-foot/route/v1/foot"
AMAP_PLACE = "https://restapi.amap.com/v3/place/text"
# A dining "venue" that is really an area ("the arcade near the station, pick on the day") has
# nothing to look up; searching it only produces a false "not found".
AREA_WORDS = re.compile(r"一带|周边|沿线|附近|择店|自选|\barea\b|nearby|on the day|various", re.IGNORECASE)
HOTEL_WORDS = re.compile(r"住宿|酒店|宾馆|旅馆|民宿|hotel|hostel|accommodation|lodging|\bstay\b",
                         re.IGNORECASE)
PIN_TOLERANCE_M = 400       # a pin further than this from the named place is the wrong place
HOTEL_TOLERANCE_M = 300
WALK_SLACK_MIN = 8          # routed walk this much longer than the plan (and 40% longer) is wrong
VIEWBOX_DEG = 0.3


class Net:
    """The two services, with Nominatim's one-request-per-second policy and a per-run cache.
    `fetch` is replaceable so the tests run offline."""

    def __init__(self, delay: float = 1.1, fetch=None, amap_key: str | None = None):
        self.delay = delay
        self.amap_key = amap_key
        self.fetch = fetch or self._fetch
        self._last = 0.0
        self._cache: dict[str, object] = {}

    def _fetch(self, url: str):
        request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        with urllib.request.urlopen(request, timeout=25) as response:
            return json.loads(response.read().decode("utf-8"))

    def get(self, url: str):
        if url in self._cache:
            return self._cache[url]
        if url.startswith(NOMINATIM):
            wait = self.delay - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
        try:
            data = self.fetch(url)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            data = {"_error": str(exc)}
        self._cache[url] = data
        return data


def _viewbox(centre: tuple[float, float]) -> str:
    lat, lon = centre
    return f"{lon - VIEWBOX_DEG},{lat + VIEWBOX_DEG},{lon + VIEWBOX_DEG},{lat - VIEWBOX_DEG}"


def geocode(net: Net, query: str, centre: tuple[float, float] | None,
            bounded: bool = True) -> list[dict] | None:
    """Matches near the destination (or, unbounded, anywhere but preferring it), or None when the
    service did not answer."""
    params = {"q": query, "format": "jsonv2", "limit": 5, "addressdetails": 1}
    if centre is not None:
        params.update(viewbox=_viewbox(centre), bounded=1 if bounded else 0)
    url = f"{NOMINATIM}/search?" + urllib.parse.urlencode(params)
    data = net.get(url)
    if isinstance(data, dict) and "_error" in data:
        return None
    return [d for d in data if isinstance(d, dict)] if isinstance(data, list) else []


def reverse(net: Net, point: tuple[float, float]) -> str | None:
    url = f"{NOMINATIM}/reverse?" + urllib.parse.urlencode(
        {"lat": point[0], "lon": point[1], "format": "jsonv2", "zoom": 18})
    data = net.get(url)
    if not isinstance(data, dict) or "_error" in data:
        return None
    return str(data.get("display_name") or "") or None


def walk_minutes(net: Net, a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float] | None:
    """(minutes, km) on OSM foot routing, or None when it did not answer."""
    url = f"{FOOT_ROUTER}/{a[1]},{a[0]};{b[1]},{b[0]}?overview=false"
    data = net.get(url)
    if not isinstance(data, dict) or data.get("code") != "Ok" or not data.get("routes"):
        return None
    route = data["routes"][0]
    return route["duration"] / 60, route["distance"] / 1000


# ---------------------------------------------------------------- mainland China (GCJ-02)

_A, _EE = 6378245.0, 0.00669342162296594323


def in_mainland(point: tuple[float, float]) -> bool:
    """Inside the box where GCJ-02 applies. Hong Kong and Macau fall inside it too, and Amap
    offsets them as well, so treating them alike is correct for Amap pins."""
    lat, lon = point
    return 73.66 < lon < 135.05 and 3.86 < lat < 53.55


def _offset(lat: float, lon: float) -> tuple[float, float]:
    x, y = lon - 105.0, lat - 35.0
    common = (20 * math.sin(6 * x * math.pi) + 20 * math.sin(2 * x * math.pi)) * 2 / 3
    dlat = (-100 + 2 * x + 3 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x)) + common
            + (20 * math.sin(y * math.pi) + 40 * math.sin(y / 3 * math.pi)) * 2 / 3
            + (160 * math.sin(y / 12 * math.pi) + 320 * math.sin(y * math.pi / 30)) * 2 / 3)
    dlon = (300 + x + 2 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x)) + common
            + (20 * math.sin(x * math.pi) + 40 * math.sin(x / 3 * math.pi)) * 2 / 3
            + (150 * math.sin(x / 12 * math.pi) + 300 * math.sin(x / 30 * math.pi)) * 2 / 3)
    rad = lat / 180 * math.pi
    magic = 1 - _EE * math.sin(rad) ** 2
    dlat = dlat * 180 / ((_A * (1 - _EE)) / (magic * math.sqrt(magic)) * math.pi)
    dlon = dlon * 180 / (_A / math.sqrt(magic) * math.cos(rad) * math.pi)
    return dlat, dlon


def wgs_to_gcj(point: tuple[float, float]) -> tuple[float, float]:
    if not in_mainland(point):
        return point
    dlat, dlon = _offset(*point)
    return point[0] + dlat, point[1] + dlon


def gcj_to_wgs(point: tuple[float, float]) -> tuple[float, float]:
    """Inverse by fixed-point iteration; converges to well under a metre in a few steps."""
    if not in_mainland(point):
        return point
    lat, lon = point
    for _ in range(6):
        g = wgs_to_gcj((lat, lon))
        lat, lon = lat - (g[0] - point[0]), lon - (g[1] - point[1])
    return lat, lon


def amap_search(net: Net, query: str, city: str) -> list[dict] | None:
    """Amap place search, answered in the same shape as a Nominatim match (WGS-84). None when
    the service did not answer or refused the key."""
    params = {"keywords": query, "city": city, "offset": 5, "key": net.amap_key, "output": "json"}
    data = net.get(f"{AMAP_PLACE}?" + urllib.parse.urlencode(params))
    if not isinstance(data, dict) or "_error" in data or str(data.get("status")) != "1":
        return None
    out = []
    for poi in _seq(data.get("pois")):
        loc = str(_obj(poi).get("location") or "")
        if "," not in loc:
            continue
        lon, lat = (float(v) for v in loc.split(",")[:2])
        lat, lon = gcj_to_wgs((lat, lon))
        address = " ".join(str(poi.get(k) or "") for k in ("cityname", "adname", "address")
                           if isinstance(poi.get(k), str)).strip()
        out.append({"name": poi.get("name"), "display_name": f"{poi.get('name')}, {address}",
                    "lat": lat, "lon": lon, "address_text": address, "source": "amap",
                    "osm_type": "amap", "osm_id": poi.get("id")})
    return out


def _address_text(item: dict) -> str:
    """The address a driver needs, as the map writes it: street and number, then the town."""
    if item.get("address_text"):
        return str(item["address_text"])
    a = _obj(item.get("address"))
    street = " ".join(str(a[k]) for k in ("road", "house_number") if a.get(k))
    town = " ".join(str(a[k]) for k in ("postcode",) if a.get(k))
    town = " ".join(filter(None, [town, str(a.get("city") or a.get("town") or a.get("village") or "")]))
    if street:
        return ", ".join(filter(None, [street, str(a.get("suburb") or ""), town]))
    return ", ".join(str(item.get("display_name") or "").split(", ")[1:5])


def _point(item: dict) -> tuple[float, float]:
    return float(item["lat"]), float(item["lon"])


def _osm_url(item: dict) -> str:
    return f"https://www.openstreetmap.org/{item.get('osm_type', 'node')}/{item.get('osm_id', '')}"


def _directions_url(a, b) -> str:
    return ("https://www.openstreetmap.org/directions?engine=fossgis_osrm_foot&route="
            f"{a[0]:.5f}%2C{a[1]:.5f}%3B{b[0]:.5f}%2C{b[1]:.5f}")


CJK = re.compile(r"[\u3000-\u9fff\uff00-\uffef]+")
NEAR_KM = 3.0               # a same-name match further than this from the pin is another place
LARGE_AREA_M = 800          # a matched area wider than this has no single "there" to route to
IATA = re.compile(r"^[A-Z]{3}$")


def label_query(label: str) -> str:
    """The searchable part of a label. '中央市场（Mercado Central）' is searched as
    'Mercado Central', and 'Mercado Central 内熟食摊' as 'Mercado Central': the local name is
    what OSM carries. A label with no local-script part is searched as written."""
    inner = re.findall(r"[（(]([^）)]+)[）)]", label or "")
    latin = [s for s in inner if re.search(r"[A-Za-zÀ-ÿ]", s) and not IATA.match(s.strip())]
    codes = [s.strip() for s in inner if IATA.match(s.strip())]
    if codes and not latin:
        return f"{codes[0]} airport"
    if latin:
        return latin[0].strip()
    bare = re.sub(r"[（(][^）)]*[）)]", "", label or "").strip()
    if re.search(r"[A-Za-zÀ-ÿ]", bare):
        bare = re.sub(r"\s+", " ", CJK.sub(" ", bare)).strip()
    return bare


def hotel_queries(name: str) -> list[str]:
    """'AC Hotel by Marriott Alicante' -> itself, then without the 'by <brand>' part, which is
    how OSM usually names it ('Hotel AC Alicante')."""
    base = re.sub(r"[（(][^）)]*[）)]", "", name or "").strip()
    out = [base]
    latin = re.sub(r"\s+", " ", re.sub(r"[^\sA-Za-zÀ-ÿ0-9'&.-]+", " ", base)).strip()
    if latin and latin != base and re.search(r"[\u3000-\u9fff]", base):
        out.append(latin)                     # '西鉄イン日本橋 Nishitetsu Inn ...' -> the Latin name
        base = latin
    short = re.sub(r"\s+by\s+\w+", "", base, flags=re.IGNORECASE).strip()
    if short and short != base:
        out.append(short)
    words = short.split()
    if len(words) > 2 and words[0].casefold() != "hotel":
        out.append("Hotel " + " ".join(words[1:]))  # 'Sercotel Maya Alicante' -> 'Hotel Maya Alicante'
    return [q for q in out if q]


ADDRESS_KM = 50             # a hotel matched further than this from the destination gets no taxi card


_FILLER = {"hotel", "hotels", "hostel", "inn", "suites", "suite", "rooms", "apartments", "apartment", "the",
           "and", "by", "de", "del", "la", "le", "il", "el", "di", "b&b", "bnb"}


def _words(text: str) -> set[str]:
    plain = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))
    return {w for w in re.findall(r"[a-z0-9]+", plain.casefold()) if len(w) >= 2 and w not in _FILLER}


def names_property(match: dict, name: str, city: str) -> bool:
    """Is this map result the property, not merely something a query variant found? For one of
    the name variants the lookup itself tries, the result's name must carry at least half of that
    variant's own words, the city left out (or share four CJK characters with it). Measured:
    'LE COLONNE MILANO' matched a restaurant called 'Todos a Cuba' 190 m away, and 'Nuvola B&B'
    matched 'La Nuvola' in Poland; both would have printed that address on the taxi card."""
    found = str(match.get("name") or str(match.get("display_name") or "").split(",")[0])
    have = _words(found)
    town = _words(city)
    for variant in hotel_queries(name):
        want = _words(variant) - town
        if want and len(want & have) * 2 >= len(want):
            return True
    cjk_name = "".join(CJK.findall(name))
    cjk_found = "".join(CJK.findall(found))
    return bool(cjk_name) and any(cjk_name[i:i + 4] in cjk_found for i in range(max(1, len(cjk_name) - 3)))


def city_name(net: Net, centre: tuple[float, float]) -> str:
    """The destination's own name for itself, for queries like 'Mercado Central de Alicante'."""
    url = f"{NOMINATIM}/reverse?" + urllib.parse.urlencode(
        {"lat": centre[0], "lon": centre[1], "format": "jsonv2", "zoom": 10})
    data = net.get(url)
    address = _obj(_obj(data).get("address"))
    name = str(address.get("city") or address.get("town") or address.get("village") or "")
    return name.split("/")[-1].strip()


def find(net: Net, queries: list[str], centre, city: str, near=None,
         bounded: bool = True) -> list[dict] | None:
    """Try each query alone, then with the city name. With `near`, only a match within NEAR_KM
    of it counts: a market of the same name in the next town is not this market.
    None means the service did not answer. Inside mainland China with an Amap key, Amap answers
    instead."""
    if net.amap_key and centre is not None and in_mainland(centre):
        result = amap_search(net, queries[0], city) if queries and queries[0] else []
        if result is None:
            return None
        anchor = near or centre
        limit = NEAR_KM if near is not None else (None if not bounded else 50)
        return [r for r in result if limit is None or _great_circle_km(anchor, _point(r)) <= limit]
    variants = []
    for q in queries:
        if q.endswith(" airport") and IATA.match(q.split()[0]) and city:
            variants.append(f"{city} airport")
        variants += [q] + ([f"{q} {city}", f"{q} de {city}"] if city and city.casefold() not in q.casefold() else [])
    for query in dict.fromkeys(v for v in variants if v):
        result = geocode(net, query, centre, bounded=bounded)
        if result is None:
            return None
        if near is not None:
            result = [r for r in result if _great_circle_km(near, _point(r)) <= NEAR_KM]
        if result:
            return result
    return []


# ---------------------------------------------------------------- what the plan says


def _day_hotel_index(plan: dict, day_index: int) -> int | None:
    accs = [a for a in _seq(_obj(plan.get("booking_options")).get("accommodations")) if isinstance(a, dict)]
    days = [d for d in _seq(plan.get("days")) if isinstance(d, dict)]
    for i in range(day_index, -1, -1):
        wanted = _obj(days[i]).get("accommodation_option_id") if i < len(days) else None
        for j, acc in enumerate(accs):
            if wanted and acc.get("id") == wanted:
                return j
    return 0 if accs else None


def place_inputs(plan: dict) -> list[dict]:
    """Every place fact this script checks, each with a stable key. The gate recomputes these
    from the current plan and asks for a rerun when any key is not covered."""
    out: list[dict] = []
    for j, acc in enumerate(_seq(_obj(plan.get("booking_options")).get("accommodations"))):
        name = str(_obj(acc).get("property_name") or "").strip()
        if name:
            pointer = f"booking_options.accommodations[{j}].property_name"
            out.append({"kind": "hotel", "pointer": pointer, "label": name, "key": f"hotel|{pointer}|{name}",
                        "address": str(_obj(acc).get("address_or_location_reference") or "").strip()})
    for i, day in enumerate(_seq(plan.get("days"))):
        day = _obj(day)
        for k, card in enumerate(_seq(day.get("dining"))):
            name = str(_obj(card).get("venue_name") or "").strip()
            if name and not HOTEL_WORDS.search(name) and not AREA_WORDS.search(name):
                pointer = f"days[{i}].dining[{k}].venue_name"
                out.append({"kind": "venue", "pointer": pointer, "label": name, "key": f"venue|{pointer}|{name}"})
        for k, seg in enumerate(_seq(_obj(day.get("route")).get("segments"))):
            seg = _obj(seg)
            url = str(seg.get("verified_map_url") or "")
            ends = _map_endpoints(url)
            if len(ends) < 2:
                continue
            lon_first = _lon_first(url)
            a = _endpoint_coords(ends[0][1], lon_first)
            b = _endpoint_coords(ends[-1][1], lon_first)
            if lon_first:   # Amap writes GCJ-02; everything below compares in WGS-84
                a, b = (gcj_to_wgs(p) if p else p for p in (a, b))
            pointer = f"days[{i}].route.segments[{k}]"
            for side, point, label in (("from", a, seg.get("from")), ("to", b, seg.get("to"))):
                if point is None or not label:
                    continue
                out.append({"kind": "pin", "pointer": f"{pointer}.{side}", "label": str(label),
                            "point": point, "day": i,
                            "key": f"pin|{pointer}.{side}|{point[0]:.5f},{point[1]:.5f}|{label}"})
            if _is_walk(seg) and a and b:
                minutes = _num(seg.get("duration_minutes")) or _num(seg.get("walking_minutes"))
                out.append({"kind": "walk", "pointer": pointer, "label": f"{seg.get('from')} → {seg.get('to')}",
                            "a": a, "b": b, "minutes": minutes, "day": i,
                            "from": str(seg.get("from") or ""), "to": str(seg.get("to") or ""),
                            "key": f"walk|{pointer}|{a[0]:.5f},{a[1]:.5f}|{b[0]:.5f},{b[1]:.5f}|{minutes:g}"})
    return out


def input_keys(plan: dict) -> set[str]:
    return {item["key"] for item in place_inputs(plan)}


# ---------------------------------------------------------------- checking


def run(plan: dict, net: Net, addresses: list | None = None) -> tuple[list[dict], list[str], list[str]]:
    """Returns (findings, keys that were actually checked, notes). Each hotel found is appended
    to `addresses` when a list is given."""
    inputs = place_inputs(plan)
    findings: list[dict] = []
    checked: list[str] = []
    notes: list[str] = []
    trip = _obj(plan.get("trip"))
    cap = _num(_obj(trip.get("traveler_constraints")).get("max_continuous_walking_minutes"))
    centre = None
    coords = trip.get("destination_coords")
    if isinstance(coords, dict) and "lat" in coords:
        centre = (float(coords["lat"]), float(coords["lon"] if "lon" in coords else coords["lng"]))
    elif isinstance(coords, (list, tuple)) and len(coords) == 2:
        centre = (float(coords[0]), float(coords[1]))
    if centre is None:
        centre = next((x["point"] for x in inputs if x["kind"] == "pin"), None)
    if centre is None and trip.get("destination"):
        found = geocode(net, label_query(str(trip["destination"])), None)
        if found:
            centre = _point(found[0])
    if centre is None:
        return findings, checked, ["no destination_coords, no usable pin, and the destination name "
                                   "did not geocode: nothing to check against"]

    china = in_mainland(centre)
    if china and net.amap_key:
        city = re.sub(r"[（(][^）)]*[）)]", "", str(trip.get("destination") or "")).split("，")[0].split(",")[0].strip()
    else:
        city = city_name(net, centre)
    if china and not net.amap_key:
        notes.append("mainland China: OpenStreetMap lists few hotels and restaurants here, so expect "
                     "many 'unverifiable' findings. Set AMAP_KEY (a free Amap Web Service key from "
                     "lbs.amap.com) to look them up on Amap instead")
    hotels: dict[int, tuple[float, float]] = {}
    unanswered: set[int] = set()   # hotels the geocoder never answered for: their pins wait too
    hotel_items = [x for x in inputs if x["kind"] == "hotel"]
    for item in hotel_items:
        j = int(re.search(r"\[(\d+)\]", item["pointer"]).group(1))
        # Unbounded: a trip can book a night in the departure city too.
        result = find(net, hotel_queries(item["label"]), centre, city, bounded=False)
        if result is None:
            notes.append(f"{item['pointer']}: geocoder did not answer; not checked")
            unanswered.add(j)
            continue
        checked.append(item["key"])
        named = [r for r in result if names_property(r, item["label"], city)]
        result = [r for r in named if _great_circle_km(centre, _point(r)) <= ADDRESS_KM]
        by_address = False
        if not result and re.search(r"\d", item["address"]) and re.search(r"[A-Za-z]", item["address"]):
            # OSM often lacks a small hotel's name but has its building: 'Via Urbano III 3, 20123
            # Milano' is a house node even where 'LE COLONNE MILANO' finds nothing.
            found = geocode(net, item["address"], centre, bounded=True)
            result = [dict(r, name=item["label"]) for r in (found or [])
                      if r.get("category") in ("building", "place") or r.get("type") in ("house", "building")
                      or _obj(r.get("address")).get("house_number")]
            by_address = bool(result)
        near = bool(result)
        result = result or named        # a departure-city hotel is far on purpose: no taxi card
        if result:
            hotels[j] = _point(result[0])
            if addresses is not None and near:
                addresses.append({"pointer": item["pointer"], "property_name": item["label"],
                                  "local_name": str(result[0].get("name") or item["label"]),
                                  "address": _address_text(result[0]),
                                  "lat": round(hotels[j][0], 6), "lon": round(hotels[j][1], 6),
                                  "source": "Amap" if result[0].get("source") == "amap" else "OpenStreetMap"})
            if by_address:
                notes.append(f"{item['pointer']}: no map place by that name; located by its address instead")
        else:
            findings.append({
                "kind": "hotel", "pointer": item["pointer"], "label": item["label"], "verdict": "unverifiable", "severity": "minor",
                "claim": f"The plan books '{item['label']}'.",
                "correction": "OpenStreetMap has no place by this name near the destination, so its "
                              "location (and every walk from it) could not be checked. Confirm the "
                              "property on its own site and pin its real address.",
                "evidence_url": f"{NOMINATIM}/ui/search.html?q={urllib.parse.quote(item['label'])}"})

    for item in inputs:
        if item["kind"] == "venue":
            result = find(net, [label_query(item["label"])], centre, city)
            if result is None:
                notes.append(f"{item['pointer']}: geocoder did not answer; not checked")
                continue
            checked.append(item["key"])
            if not result:
                findings.append({
                    "kind": "venue", "pointer": item["pointer"], "label": item["label"], "verdict": "unverifiable", "severity": "major",
                    "claim": f"The plan schedules a meal at '{item['label']}'.",
                    "correction": "OpenStreetMap has no place by this name near the destination. OSM "
                                  "misses many small restaurants, so this is not proof it is gone, but "
                                  "nothing here confirms it exists either. Confirm it on its own site or "
                                  "a current listing, or replace it.",
                    "evidence_url": f"{NOMINATIM}/ui/search.html?q={urllib.parse.quote(label_query(item['label']))}"})

        elif item["kind"] == "pin":
            point = item["point"]
            if HOTEL_WORDS.search(item["label"]):
                j = _day_hotel_index(plan, item["day"])
                if j in unanswered:
                    notes.append(f"{item['pointer']}: its hotel was not looked up; not checked")
                    continue
                checked.append(item["key"])
                if j is None or j not in hotels or _great_circle_km(point, hotels[j]) > 50:
                    continue  # hotel not found (that finding says so), or a hotel in another city
                gap = _great_circle_km(point, hotels[j]) * 1000
                if gap > HOTEL_TOLERANCE_M:
                    where = reverse(net, point) or "somewhere else"
                    name = _obj(_seq(_obj(plan.get("booking_options")).get("accommodations"))[j]).get("property_name")
                    findings.append({
                        "kind": "pin", "pointer": item["pointer"], "label": item["label"], "verdict": "wrong", "severity": "major",
                        "claim": f"The map button's '{item['label']}' point is the hotel.",
                        "correction": f"The point ({point[0]:.5f},{point[1]:.5f}) is {gap:,.0f} m from "
                                      f"{name} (OSM {hotels[j][0]:.5f},{hotels[j][1]:.5f}); it is at {where}. "
                                      "Every walk and route from this pin starts at the wrong building.",
                        "evidence_url": f"https://www.openstreetmap.org/?mlat={point[0]:.5f}&mlon={point[1]:.5f}#map=17/{point[0]:.5f}/{point[1]:.5f}"})
                continue
            query = label_query(item["label"])
            result = find(net, [query], centre, city, near=point) if query else []
            if result is None:
                notes.append(f"{item['pointer']}: geocoder did not answer; not checked")
                continue
            checked.append(item["key"])
            if not result:
                continue  # an unnamed or unsearchable label proves nothing either way
            best = min(result, key=lambda r: _great_circle_km(point, _point(r)))
            gap = _great_circle_km(point, _point(best)) * 1000
            box = [float(v) for v in _seq(best.get("boundingbox"))] if len(_seq(best.get("boundingbox"))) == 4 else None
            span = _great_circle_km((box[0], box[2]), (box[1], box[3])) * 1000 if box else 0
            if gap <= PIN_TOLERANCE_M and span > LARGE_AREA_M:
                findings.append({
                    "kind": "pin", "pointer": item["pointer"], "label": item["label"], "verdict": "misleading", "severity": "major",
                    "claim": f"The map button's point for '{item['label']}' is where the traveller goes.",
                    "correction": f"The pin is the middle of {best.get('name') or query}, an area about "
                                  f"{span / 1000:.1f} km across, and a map app routes to that middle point. "
                                  "Point it at the terminal, entrance or stop the traveller actually uses.",
                    "evidence_url": _osm_url(best)})
            elif gap > PIN_TOLERANCE_M:
                findings.append({
                    "kind": "pin", "pointer": item["pointer"], "label": item["label"], "verdict": "wrong", "severity": "major",
                    "claim": f"The map button's point for '{item['label']}' is that place.",
                    "correction": f"The nearest OSM match for '{query}' ({best.get('display_name', '')[:90]}) "
                                  f"is {gap:,.0f} m from the pin ({point[0]:.5f},{point[1]:.5f}).",
                    "evidence_url": _osm_url(best)})

        elif item["kind"] == "walk":
            a, b = item["a"], item["b"]
            j = _day_hotel_index(plan, item["day"])
            moved = []
            near = j in hotels and _great_circle_km(hotels[j], item["a"]) <= 50
            if near and HOTEL_WORDS.search(item["from"]):
                a = hotels[j]; moved.append("from")
            if near and HOTEL_WORDS.search(item["to"]):
                b = hotels[j]; moved.append("to")
            routed = walk_minutes(net, a, b)
            if routed is None:
                notes.append(f"{item['pointer']}: foot router did not answer; not checked")
                continue
            checked.append(item["key"])
            minutes, km = routed
            planned = item["minutes"]
            over_cap = bool(cap) and minutes > cap
            too_long = minutes >= planned + WALK_SLACK_MIN and minutes >= planned * 1.4
            if not (too_long or (over_cap and planned <= cap)):
                continue
            critical = over_cap and planned <= cap
            start = " from the real hotel location" if moved else ""
            findings.append({
                "kind": "walk", "pointer": item["pointer"], "label": item["label"], "verdict": "wrong",
                "severity": "critical" if critical else "major",
                "planned_minutes": int(planned) if planned == int(planned) else planned,
                "routed_minutes": round(minutes),
                "claim": f"Walking {item['label']} takes {planned:g} minutes.",
                "correction": f"OSM foot routing{start} gives about {minutes:.0f} minutes for {km:.1f} km"
                              + (f", over the traveller's {cap:g}-minute walking limit" if over_cap else "")
                              + ". Re-route this leg (transit, taxi, or a closer stop) or fix its endpoints.",
                "evidence_url": _directions_url(a, b)})
    return findings, checked, notes


def merge_resolutions(new: list[dict], old: list[dict]) -> list[dict]:
    """A rerun keeps what a person already decided about the same finding."""
    kept = {(f.get("kind"), f.get("pointer")): f for f in old if isinstance(f, dict)}
    for finding in new:
        prior = kept.get((finding["kind"], finding["pointer"]))
        if prior and prior.get("resolution"):
            finding["resolved"] = prior.get("resolved", True)
            finding["resolution"] = prior["resolution"]
    return new


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("plan")
    parser.add_argument("--into", action="store_true", help="write the result into the plan as place_check")
    parser.add_argument("--json", help="also write the findings to this file")
    parser.add_argument("--delay", type=float, default=1.1, help="seconds between Nominatim requests")
    args = parser.parse_args()

    path = Path(args.plan)
    plan = json.loads(path.read_text(encoding="utf-8"))
    addresses: list[dict] = []
    findings, checked, notes = run(plan, Net(delay=args.delay, amap_key=os.environ.get("AMAP_KEY") or None),
                                   addresses)
    total = len(place_inputs(plan))
    old = _seq(_obj(plan.get("place_check")).get("findings"))
    findings = merge_resolutions(findings, old)
    block = {"tool": "check_places.py", "checked_at": dt.date.today().isoformat(),
             "inputs": sorted(checked), "findings": findings, "addresses": addresses}

    for f in findings:
        mark = " (resolved)" if f.get("resolution") else ""
        print(f"{f['severity'].upper():8} {f['verdict']:12} {f['pointer']}{mark}\n         {f['correction']}")
    for note in notes:
        print(f"NOTE     {note}")
    print(f"checked {len(checked)} of {total} place facts; {len(findings)} findings")
    if args.json:
        Path(args.json).write_text(json.dumps(block, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.into:
        plan["place_check"] = block
        path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote place_check into {path}")
    open_wrong = [f for f in findings if f["verdict"] == "wrong" and not f.get("resolution")]
    if len(checked) < total:
        return 2
    return 1 if open_wrong else 0


if __name__ == "__main__":
    sys.exit(main())
