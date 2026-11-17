#!/usr/bin/env python3
"""aa.py - read-only calls to the American Adventurer keyless API.

Python standard library only. Makes HTTPS GET requests to https://davelalande.com
and nothing else. Sends no personal data: the API needs none.

Every output keeps what you must show a reader: the record url, the source, and
the record date. The data is printed as the API sent it, inside a small envelope.

  aa.py root
  aa.py find "hyalite" [--state MT] [--cost free|fee] [--water] [--forest ORGCODE]
                       [--rules] [--open YYYY-MM-DD|today] [--limit 10]
  aa.py camp SLUG [--date YYYY-MM-DD]
  aa.py near LAT LON [--radius 25] [--cost free|fee] [--limit 10]
  aa.py poi LAT LON CATEGORY [--radius 25]      (fuel, grocery, potable_water, dump_station, ...)
  aa.py town "Bozeman" [--state MT] [--radius 25] [--limit 5]   (free camps near a town)
  aa.py forest "gallatin"                       (search; or give a slug for the record)
  aa.py land "adirondack"                       (named state lands that are not national forests)
  aa.py weather LAT LON                         (National Weather Service forecast, via the API)
  aa.py fire LAT LON                            (wildfire reports near a point, via the API)

Add --summary BEFORE the command (aa.py --summary camp SLUG) for a short plain-text
summary instead of JSON.
All distances are straight-line miles. A null or missing field means UNRECORDED.
changes_since and what_we_cover are on the MCP connector (https://davelalande.com/mcp, live 2026-11-11).
land_at (national forests only) is on the MCP connector too (live 2026-11-11).
trip_check (a whole trip on given dates) and rig_math are MCP connector tools too; this script does not call them.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://davelalande.com"
UA = "aa-skill/1 (+https://davelalande.com/skill/)"
CREDIT = "Camp records: American Adventurer (davelalande.com)"
OSM = "Where a record's source names OpenStreetMap, also credit: (c) OpenStreetMap contributors (ODbL)."
PACE = 0.5  # seconds between calls: the site asks for about two requests a second
_last = [0.0]


def get(path, params=None):
    """GET one API address. Returns (url, parsed_json). Retries once on 429/5xx."""
    url = BASE + path
    if params:
        clean = {k: v for k, v in params.items() if v not in (None, "", False)}
        if clean:
            url += "?" + urllib.parse.urlencode(clean)
    last_err = None
    for attempt in range(2):
        wait = PACE - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return url, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last_err = "HTTP %s from %s" % (e.code, url)
            if e.code in (429, 500, 502, 503, 504) and attempt == 0:
                time.sleep(3)
                continue
            break
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            last_err = "could not read %s (%s)" % (url, e)
            if attempt == 0:
                time.sleep(3)
                continue
            break
    # A failed read is "could not read", never "none".
    sys.exit("ERROR: " + str(last_err) + ". Could not read; that is not the same as none.")


def record_date(data):
    """The record date the API states: 'data built ...' in its cite line, or its own date field."""
    pub = data.get("publisher") if isinstance(data, dict) else None
    if isinstance(pub, dict):
        m = re.search(r"data built (\S+)", pub.get("cite", ""))
        if m:
            return m.group(1)
    for k in ("updated", "generated", "data_built_at"):
        if isinstance(data, dict) and data.get(k):
            return data[k]
    return None


def envelope(url, data, source=None):
    d = dict(data) if isinstance(data, dict) else {"data": data}
    d.pop("publisher", None)  # replaced by the credit line below
    src = source or (data.get("source") if isinstance(data, dict) and isinstance(data.get("source"), str) else None)
    return {
        "request_url": url,
        "source": src or "American Adventurer records (davelalande.com); the record's own source is named inside",
        "record_date": record_date(data),
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "credit": CREDIT,
        "osm_note": OSM,
        "distance_unit": "straight-line miles",
        "unrecorded_rule": "A null or missing field is UNRECORDED. Do not estimate it.",
        "data": d,
    }


def fmt_camp(c):
    bits = [c.get("name", "?"), "(%s)" % c.get("state", "?"), c.get("cost", "unrecorded cost"),
            c.get("land_manager") or "manager unrecorded"]
    if c.get("miles") is not None:
        bits.append("%s mi straight-line" % c["miles"])
    r = c.get("rules") or {}
    if r.get("stay_limit_days") is not None:
        bits.append("stay limit %s days" % r["stay_limit_days"])
    elif r.get("stay_limit_status"):
        bits.append("stay limit: %s" % r["stay_limit_status"])
    else:
        bits.append("stay limit unrecorded")
    bits.append("water on record" if c.get("water") else "no water recorded")
    return " | ".join(str(b) for b in bits) + "\n    url: " + str(c.get("url"))


def summarize(env):
    d = env["data"]
    out = []
    if "camp" in d:
        out.append(fmt_camp(d["camp"]))
        s = d["camp"].get("season")
        if s:
            out.append("  season on %s: %s. %s" % (s.get("state_on"), s.get("state"), s.get("why")))
        else:
            out.append("  season: unrecorded")
    elif "camps" in d:
        out.append("%s camps match (showing %d)" % (d.get("total", "?"), len(d["camps"])))
        out += ["  " + fmt_camp(c) for c in d["camps"]]
    elif "forests" in d:
        for f in d["forests"]:
            out.append("%s | states %s | %s camps | %s" % (f["name"], f.get("states"), f.get("camp_count"), f.get("url")))
    elif "forest" in d:
        f = d["forest"]
        out.append("%s | %s camps | %s free | url: %s" % (f["name"], f.get("camps_in_corpus"), f.get("camps_free"), f.get("url")))
    elif "lands" in d:
        for l in d["lands"]:
            out.append("%s | %s | %s" % (l.get("name"), l.get("kind"), l.get("url")))
    elif "periods" in d:
        out.append("Forecast near %s (NWS)" % d.get("nearest"))
        for p in d["periods"][:6]:
            out.append("  %s: %s F, %s, wind %s" % (p["name"], p["temp"], p["short"], p["wind"]))
        out.append("  Only plan spring, summer and fall trips. A snow forecast means not this trip.")
    elif "fires" in d:
        out.append("%s wildfire reports, %s planned burns. Reports only: not perimeters, closures or restrictions." % (d.get("fire_count"), d.get("rx_count")))
        for f in d["fires"][:5]:
            out.append("  %s | %s acres | %s mi %s%s" % (f["name"], f["acres"], f["mi"], f["dir"], " | planned burn" if f.get("rx") else ""))
    elif d.get("type") == "poi":
        out.append("%s %s points within %s mi (a floor, never a survey)" % (d.get("total"), d.get("category"), d.get("radius_miles")))
    else:
        out.append(json.dumps(d)[:400])
    out.append("source: %s | record date: %s | fetched: %s" % (env["source"], env["record_date"], env["fetched_at"]))
    out.append(env["credit"] + ". " + env["osm_note"])
    return "\n".join(out)


def keep_cost(data, cost, limit):
    """/api/near ignores a cost filter (checked 2026-11-11), so filter here and say so."""
    camps = data.get("camps", [])
    if cost:
        camps = [c for c in camps if c.get("cost") == cost]
        data["filtered_here"] = "Kept only camps whose cost verdict is %r, from the nearest %d returned by /api/near; the API's own total counts all costs." % (cost, len(data.get("camps", [])))
    data["camps"] = camps[:limit]


def find_town(name, state):
    url, data = get("/towns.json")
    want = name.strip().lower()
    hits = [t for t in data["towns"] if t[2].lower() == want and (not state or t[3].upper() == state.upper())]
    if not hits:
        sys.exit("ERROR: no town named %r%s in towns.json. Try find or near with coordinates." % (name, " in " + state if state else ""))
    hits.sort(key=lambda t: -(t[4] or 0))
    return hits[0]


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Read-only calls to the American Adventurer API.")
    p.add_argument("--summary", action="store_true", help="short plain-text summary instead of JSON")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("root")
    s = sub.add_parser("find"); s.add_argument("q"); s.add_argument("--state"); s.add_argument("--cost", choices=["free", "fee", "unpriced"])
    s.add_argument("--water", action="store_true"); s.add_argument("--forest"); s.add_argument("--rules", action="store_true")
    s.add_argument("--open", dest="open_"); s.add_argument("--limit", type=int, default=10)
    s = sub.add_parser("camp"); s.add_argument("slug"); s.add_argument("--date")
    s = sub.add_parser("near"); s.add_argument("lat"); s.add_argument("lon"); s.add_argument("--radius", default="25")
    s.add_argument("--cost", choices=["free", "fee", "unpriced"]); s.add_argument("--limit", type=int, default=10)
    s = sub.add_parser("poi"); s.add_argument("lat"); s.add_argument("lon"); s.add_argument("category"); s.add_argument("--radius", default="25")
    s = sub.add_parser("town"); s.add_argument("name"); s.add_argument("--state"); s.add_argument("--radius", default="25"); s.add_argument("--limit", type=int, default=5)
    s = sub.add_parser("forest"); s.add_argument("q")
    s = sub.add_parser("land"); s.add_argument("q")
    s = sub.add_parser("weather"); s.add_argument("lat"); s.add_argument("lon")
    s = sub.add_parser("fire"); s.add_argument("lat"); s.add_argument("lon")
    a = p.parse_args(argv)

    source = None
    if a.cmd == "root":
        url, data = get("/api/")
    elif a.cmd == "find":
        url, data = get("/api/camps", {"q": a.q, "state": a.state, "cost": a.cost, "water": 1 if a.water else None,
                                       "forest": a.forest, "rules": 1 if a.rules else None, "open": a.open_, "limit": a.limit})
    elif a.cmd == "camp":
        url, data = get("/api/camps/" + urllib.parse.quote(a.slug), {"date": a.date})
    elif a.cmd == "near":
        url, data = get("/api/near", {"lat": a.lat, "lon": a.lon, "radius": a.radius, "limit": 100 if a.cost else a.limit})
        keep_cost(data, a.cost, a.limit)
    elif a.cmd == "poi":
        url, data = get("/api/near", {"lat": a.lat, "lon": a.lon, "radius": a.radius, "type": "poi", "cat": a.category})
    elif a.cmd == "town":
        lat, lon, name, st, _ = find_town(a.name, a.state)
        url, data = get("/api/near", {"lat": lat, "lon": lon, "radius": a.radius, "limit": 100})
        keep_cost(data, "free", a.limit)
        data["town"] = {"name": name, "state": st, "lat": lat, "lon": lon, "source": "davelalande.com/towns.json"}
    elif a.cmd == "forest":
        if "-" in a.q and re.fullmatch(r"[a-z0-9-]+", a.q):
            url, data = get("/api/forests/" + a.q)
        else:
            url, data = get("/api/forests", {"q": a.q, "limit": 10})
    elif a.cmd == "land":
        url, data = get("/api/lands", {"q": a.q, "limit": 10})
    elif a.cmd == "weather":
        url, data = get("/api/weather", {"lat": a.lat, "lon": a.lon})
        source = "National Weather Service (weather.gov), via davelalande.com/api/weather"
    else:  # fire
        url, data = get("/api/fire", {"lat": a.lat, "lon": a.lon})
        source = "NIFC wildfire incident reports, via davelalande.com/api/fire (reports, not perimeters or restrictions)"
    env = envelope(url, data, source)
    print(summarize(env) if a.summary else json.dumps(env, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
