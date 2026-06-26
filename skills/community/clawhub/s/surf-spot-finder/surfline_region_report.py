#!/usr/bin/env python3
"""Fetch Surfline region/spot forecast summaries (data collection only; no scoring)."""

from __future__ import annotations

import argparse
import json
import math
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

SURFLINE_BASE_URL = "https://services.surfline.com/kbyg/spots/forecasts"
SURFLINE_SPOTS_BASE_URL = "https://services.surfline.com/kbyg/spots"
SURFLINE_MAPVIEW_BASE_URL = "https://services.surfline.com/kbyg/mapview"

# Region aliases to help quickly run common zones.
# Override with --spots if you already have your own spot IDs.
REGION_SPOT_MAP: dict[str, list[str]] = {
    "north-orange-county": [
        "5842041f4e65fad6a770882a",
        "5842041f4e65fad6a770882b",
        "5842041f4e65fad6a7708860",
    ],
    "south-orange-county": [
        "5842041f4e65fad6a77088a6",
        "5842041f4e65fad6a77088a7",
        "5842041f4e65fad6a77088ab",
    ],
    "san-diego": [
        "5842041f4e65fad6a77088b5",
        "5842041f4e65fad6a77088bf",
        "5842041f4e65fad6a77088c0",
    ],
    "santa-cruz": [
        "584204204e65fad6a7709cb6",
        "584204204e65fad6a7709cb8",
        "584204204e65fad6a7709cbc",
    ],
}


@dataclass(frozen=True)
class Bounds:
    south: float
    west: float
    north: float
    east: float


# Approximate bounding boxes for discovery via mapview.
REGION_BOUNDS_MAP: dict[str, Bounds] = {
    "north-orange-county": Bounds(33.50, -118.20, 33.88, -117.68),
    "south-orange-county": Bounds(33.35, -118.05, 33.67, -117.45),
    "san-diego": Bounds(32.52, -117.40, 33.12, -116.85),
    "santa-cruz": Bounds(36.85, -122.30, 37.15, -121.70),
}


@dataclass
class SpotSummary:
    spotId: str
    spotName: str
    avgSurfMinFt: float
    avgSurfMaxFt: float
    avgPrimarySwellFt: float
    avgPrimarySwellPeriodSec: float
    avgPrimarySwellDirectionDeg: float
    avgWindMph: float
    avgWindDirectionDeg: float
    avgTideFt: float
    validHours: int


@dataclass
class ReportPayload:
    region: str
    source: str
    hours: int
    totalSpots: int
    spots: list[SpotSummary]
    generatedAt: str


@dataclass(frozen=True)
class SpotRef:
    id: str
    name: str


def exitf(msg: str, *args: object) -> None:
    sys.stderr.write("error: " + msg.format(*args) + "\n")
    sys.exit(1)


def sorted_region_keys() -> list[str]:
    return sorted(REGION_SPOT_MAP.keys())


def build_mapview_url(b: Bounds) -> str:
    q = urllib.parse.urlencode(
        {
            "south": f"{b.south:f}",
            "west": f"{b.west:f}",
            "north": f"{b.north:f}",
            "east": f"{b.east:f}",
        }
    )
    return f"{SURFLINE_MAPVIEW_BASE_URL}?{q}"


def build_forecast_url(kind: str, spot_id: str, days: int) -> str:
    q = urllib.parse.urlencode(
        {
            "spotId": spot_id,
            "days": str(days),
            "intervalHours": "1",
            "maxHeights": "false",
        }
    )
    return f"{SURFLINE_BASE_URL}/{kind}?{q}"


def build_spot_details_url(spot_id: str) -> str:
    q = urllib.parse.urlencode({"spotId": spot_id})
    return f"{SURFLINE_SPOTS_BASE_URL}/details?{q}"


def _ssl_context() -> ssl.SSLContext:
    """Use a real CA bundle when the interpreter default is empty (e.g. macOS python.org builds)."""
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    for cafile in (
        "/etc/ssl/cert.pem",
        "/etc/ssl/certs/ca-certificates.crt",
    ):
        if os.path.isfile(cafile):
            return ssl.create_default_context(cafile=cafile)
    return ssl.create_default_context()


def fetch_json(url: str, timeout: float) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "surf-agent/1.0",
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(
            req, timeout=timeout, context=_ssl_context()
        ) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read(1024).decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"status {e.code}: {body}") from e


def discover_spots_by_bounds(b: Bounds, timeout: float) -> list[SpotRef]:
    u = build_mapview_url(b)
    resp = fetch_json(u, timeout)
    spots = (resp.get("data") or {}).get("spots") or []
    seen: dict[str, SpotRef] = {}
    for s in spots:
        sid = str(s.get("_id", "")).strip()
        if not sid:
            continue
        name = str(s.get("name", "")).strip()
        seen[sid] = SpotRef(id=sid, name=name)
    out = list(seen.values())
    out.sort(key=lambda r: r.id)
    return out


def resolve_spot_ids(
    region: str, spot_csv: str, discover: bool, timeout: float
) -> tuple[list[str], dict[str, str], str]:
    if spot_csv.strip():
        ids = [p.strip() for p in spot_csv.split(",") if p.strip()]
        return ids, {}, "custom spots"

    region = region.strip().lower()

    if discover:
        b = REGION_BOUNDS_MAP.get(region)
        if b is not None:
            try:
                refs = discover_spots_by_bounds(b, timeout)
            except Exception:
                refs = []
            if refs:
                ids = [r.id for r in refs]
                names = {r.id: r.name for r in refs if r.name}
                return ids, names, f"region discovery: {region}"

    ids = REGION_SPOT_MAP.get(region)
    if not ids:
        return [], {}, ""
    return list(ids), {}, f"region preset: {region}"


def normalize_direction_deg(direction_deg: float) -> float:
    d = direction_deg % 360
    if d < 0:
        d += 360
    return d


def _wave_row(w: dict[str, Any]) -> tuple[float, float, float, float, float]:
    surf = w.get("surf") or {}
    surf_min = float(surf.get("min", 0))
    surf_max = float(surf.get("max", 0))
    swells = w.get("swells") or []
    if swells:
        s0 = swells[0]
        primary = float(s0.get("height", 0))
        primary_period = float(s0.get("period", 0))
        primary_direction = float(s0.get("direction", 0))
    else:
        primary = primary_period = primary_direction = 0.0
    return surf_min, surf_max, primary, primary_period, primary_direction


def build_spot_summary(spot_id: str, hours: int, timeout: float) -> SpotSummary:
    days = max(1, int(math.ceil(hours / 24.0)))
    wave_url = build_forecast_url("wave", spot_id, days)
    wind_url = build_forecast_url("wind", spot_id, days)
    tide_url = build_forecast_url("tides", spot_id, days)

    try:
        wave_resp = fetch_json(wave_url, timeout)
    except Exception as e:
        raise RuntimeError(f"wave fetch failed: {e}") from e
    try:
        wind_resp = fetch_json(wind_url, timeout)
    except Exception as e:
        raise RuntimeError(f"wind fetch failed: {e}") from e
    try:
        tide_resp = fetch_json(tide_url, timeout)
    except Exception as e:
        raise RuntimeError(f"tide fetch failed: {e}") from e

    cutoff = int(time.time()) + hours * 3600

    wave_by_ts: dict[int, tuple[float, float, float, float, float]] = {}
    for w in (wave_resp.get("data") or {}).get("wave") or []:
        ts = int(w.get("timestamp", 0))
        if ts > cutoff:
            continue
        wave_by_ts[ts] = _wave_row(w)

    wind_by_ts: dict[int, tuple[float, float]] = {}
    for w in (wind_resp.get("data") or {}).get("wind") or []:
        ts = int(w.get("timestamp", 0))
        if ts > cutoff:
            continue
        wind_by_ts[ts] = (
            float(w.get("speed", 0)),
            float(w.get("direction", 0)),
        )

    tide_by_ts: dict[int, float] = {}
    for t in (tide_resp.get("data") or {}).get("tides") or []:
        ts = int(t.get("timestamp", 0))
        if ts > cutoff:
            continue
        tide_by_ts[ts] = float(t.get("height", 0))

    s = SpotSummary(
        spotId=spot_id,
        spotName="",
        avgSurfMinFt=0.0,
        avgSurfMaxFt=0.0,
        avgPrimarySwellFt=0.0,
        avgPrimarySwellPeriodSec=0.0,
        avgPrimarySwellDirectionDeg=0.0,
        avgWindMph=0.0,
        avgWindDirectionDeg=0.0,
        avgTideFt=0.0,
        validHours=0,
    )

    for ts, wave in wave_by_ts.items():
        if ts not in wind_by_ts or ts not in tide_by_ts:
            continue
        wind = wind_by_ts[ts]
        tide = tide_by_ts[ts]
        s.avgSurfMinFt += wave[0]
        s.avgSurfMaxFt += wave[1]
        s.avgPrimarySwellFt += wave[2]
        s.avgPrimarySwellPeriodSec += wave[3]
        s.avgPrimarySwellDirectionDeg += wave[4]
        s.avgWindMph += wind[0]
        s.avgWindDirectionDeg += wind[1]
        s.avgTideFt += tide
        s.validHours += 1

    if s.validHours == 0:
        raise RuntimeError("no overlapping hourly points across wave/wind/tide")

    n = float(s.validHours)
    s.avgSurfMinFt /= n
    s.avgSurfMaxFt /= n
    s.avgPrimarySwellFt /= n
    s.avgPrimarySwellPeriodSec /= n
    s.avgPrimarySwellDirectionDeg = normalize_direction_deg(
        s.avgPrimarySwellDirectionDeg / n
    )
    s.avgWindMph /= n
    s.avgWindDirectionDeg = normalize_direction_deg(s.avgWindDirectionDeg / n)
    s.avgTideFt /= n
    return s


def get_spot_name(
    spot_id: str, cache: dict[str, str], timeout: float
) -> str:
    if spot_id in cache:
        return cache[spot_id]
    u = build_spot_details_url(spot_id)
    resp = fetch_json(u, timeout)
    spot = (resp.get("data") or {}).get("spot") or {}
    name = str(spot.get("name", "")).strip()
    cache[spot_id] = name
    return name


def main() -> None:
    p = argparse.ArgumentParser(
        description="Surfline region/spot forecast report (averages over a window)."
    )
    p.add_argument(
        "--region",
        default="",
        help="Region key (e.g. san-diego). Ignored when --spots is set.",
    )
    p.add_argument(
        "--spots",
        default="",
        help="Comma-separated Surfline spot IDs to analyze.",
    )
    p.set_defaults(discover=True)
    p.add_argument(
        "--discover",
        dest="discover",
        action="store_true",
        help="When --region is set, discover spots via mapview (default on).",
    )
    p.add_argument(
        "--no-discover",
        dest="discover",
        action="store_false",
        help="Use region preset spot list only (skip mapview discovery).",
    )
    p.add_argument("--hours", type=int, default=24, help="Forecast window in hours.")
    p.add_argument("--timeout", type=int, default=15, help="HTTP timeout in seconds.")
    p.add_argument(
        "--output",
        default="text",
        choices=("text", "json"),
        help="Output format: text or json.",
    )
    args = p.parse_args()

    if args.hours <= 0:
        exitf("hours must be > 0")

    timeout = float(args.timeout)
    spot_ids, spot_names, source = resolve_spot_ids(
        args.region, args.spots, args.discover, timeout
    )
    if not spot_ids:
        exitf(
            "no spot IDs found. pass --spots or use a known --region: {}",
            ", ".join(sorted_region_keys()),
        )

    if args.output == "text":
        print(
            f"Analyzing {len(spot_ids)} spots ({source}) for next {args.hours} hours...\n"
        )

    summaries: list[SpotSummary] = []
    name_cache = dict(spot_names)
    for spot_id in spot_ids:
        try:
            summ = build_spot_summary(spot_id, args.hours, timeout)
        except Exception as e:
            if args.output == "text":
                print(f"spot {spot_id}: skipped ({e})")
            continue
        try:
            name = get_spot_name(spot_id, name_cache, timeout)
            if name.strip():
                summ.spotName = name
        except Exception:
            pass
        summaries.append(summ)

    if not summaries:
        exitf("unable to fetch usable data for all spots")

    summaries.sort(key=lambda x: x.spotId)

    if args.output == "json":
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        payload = ReportPayload(
            region=args.region,
            source=source,
            hours=args.hours,
            totalSpots=len(summaries),
            spots=summaries,
            generatedAt=generated_at,
        )
        json.dump(asdict(payload), sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        for i, s in enumerate(summaries):
            rank = i + 1
            if s.spotName.strip():
                print(f"{rank}) Spot {s.spotId} ({s.spotName})")
            else:
                print(f"{rank}) Spot {s.spotId}")
            print(
                f"   surf avg: {s.avgSurfMinFt:.1f}-{s.avgSurfMaxFt:.1f}ft | "
                f"primary swell: {s.avgPrimarySwellFt:.1f}ft | "
                f"wind: {s.avgWindMph:.1f}mph @ {s.avgWindDirectionDeg:.0f}deg | "
                f"tide: {s.avgTideFt:.1f}ft"
            )
            print(
                f"   primary swell period: {s.avgPrimarySwellPeriodSec:.1f}s | "
                f"primary swell direction: {s.avgPrimarySwellDirectionDeg:.0f}deg"
            )
            print(f"   valid points: {s.validHours}\n")


if __name__ == "__main__":
    main()
