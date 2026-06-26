#!/usr/bin/env python3
"""Small helper for common WGS84 checks."""

from __future__ import annotations

import argparse
import json
import sys


def valid_lon(value: float) -> bool:
    return -180.0 <= value <= 180.0


def valid_lat(value: float) -> bool:
    return -90.0 <= value <= 90.0


def in_mainland_china_extent(lon: float, lat: float) -> bool:
    return 73.0 <= lon <= 135.0 and 18.0 <= lat <= 54.5


def recommend_utm_epsg(lon: float, lat: float) -> tuple[int, str, str]:
    zone = int((lon + 180.0) // 6.0) + 1
    if zone < 1:
        zone = 1
    if zone > 60:
        zone = 60
    hemisphere = "north" if lat >= 0 else "south"
    epsg = f"EPSG:{32600 + zone}" if hemisphere == "north" else f"EPSG:{32700 + zone}"
    return zone, hemisphere, epsg


def cmd_validate(args: argparse.Namespace) -> int:
    payload = {
        "input": {"lon": args.lon, "lat": args.lat},
        "valid": valid_lon(args.lon) and valid_lat(args.lat),
        "longitude_valid": valid_lon(args.lon),
        "latitude_valid": valid_lat(args.lat),
        "crs": "WGS84 / EPSG:4326",
        "units": "degrees",
    }
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


def cmd_guess_order(args: argparse.Namespace) -> int:
    a, b = args.a, args.b
    lonlat_valid = valid_lon(a) and valid_lat(b)
    latlon_valid = valid_lat(a) and valid_lon(b)

    if lonlat_valid and not latlon_valid:
        guess = "lon,lat"
        confidence = "high"
    elif latlon_valid and not lonlat_valid:
        guess = "lat,lon"
        confidence = "high"
    elif lonlat_valid and latlon_valid:
        guess = "ambiguous"
        confidence = "low"
    else:
        guess = "invalid"
        confidence = "high"

    payload = {
        "input": {"a": a, "b": b},
        "guess": guess,
        "confidence": confidence,
        "lonlat_valid": lonlat_valid,
        "latlon_valid": latlon_valid,
        "note": "Ambiguous means both orders are numerically possible; use source system context.",
    }
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


def cmd_utm(args: argparse.Namespace) -> int:
    payload = {
        "input": {"lon": args.lon, "lat": args.lat},
        "valid": valid_lon(args.lon) and valid_lat(args.lat),
    }

    if not payload["valid"]:
        payload["error"] = "Invalid WGS84 longitude/latitude range."
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 1

    zone, hemisphere, epsg = recommend_utm_epsg(args.lon, args.lat)
    payload.update(
        {
            "recommended_projected_crs": epsg,
            "utm_zone": zone,
            "hemisphere": hemisphere,
            "units": "meters",
            "note": "UTM is a practical default for regional analysis, but local/national CRS may be better.",
        }
    )
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


def cmd_china_check(args: argparse.Namespace) -> int:
    payload = {
        "input": {"lon": args.lon, "lat": args.lat},
        "valid": valid_lon(args.lon) and valid_lat(args.lat),
    }
    if not payload["valid"]:
        payload["error"] = "Invalid WGS84 longitude/latitude range."
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 1

    in_china = in_mainland_china_extent(args.lon, args.lat)
    payload.update(
        {
            "in_mainland_china_extent": in_china,
            "offset_risk": "possible" if in_china else "low",
            "note": (
                "Inside common mainland-China extent. Verify whether source coordinates are WGS84, GCJ-02, or BD-09."
                if in_china
                else "Outside common mainland-China extent. GCJ-02 / BD-09 confusion is less likely."
            ),
        }
    )
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


def cmd_recommend(args: argparse.Namespace) -> int:
    payload = {
        "input": {"lon": args.lon, "lat": args.lat, "task": args.task},
        "valid": valid_lon(args.lon) and valid_lat(args.lat),
    }
    if not payload["valid"]:
        payload["error"] = "Invalid WGS84 longitude/latitude range."
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 1

    zone, hemisphere, utm_epsg = recommend_utm_epsg(args.lon, args.lat)
    in_china = in_mainland_china_extent(args.lon, args.lat)

    if args.task == "exchange":
        recommendation = "EPSG:4326"
        units = "degrees"
        reason = "Best default for interoperable storage and API exchange."
    elif args.task == "web-map":
        recommendation = "EPSG:3857"
        units = "meters"
        reason = "Best default for slippy-map and web-tile display."
    else:
        recommendation = utm_epsg
        units = "meters"
        reason = "Projected CRS in meters is better for distance, area, and buffer analysis."

    payload.update(
        {
            "recommended_crs": recommendation,
            "recommended_units": units,
            "reason": reason,
            "utm_zone": zone,
            "hemisphere": hemisphere,
            "analysis_default": utm_epsg,
            "china_offset_warning": (
                "Verify WGS84 vs GCJ-02 / BD-09 before further processing."
                if in_china
                else ""
            ),
        }
    )
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Common WGS84 helpers.")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate WGS84 lon/lat ranges.")
    validate.add_argument("--lon", type=float, required=True)
    validate.add_argument("--lat", type=float, required=True)
    validate.set_defaults(func=cmd_validate)

    guess = sub.add_parser("guess-order", help="Guess lon/lat or lat/lon ordering.")
    guess.add_argument("--a", type=float, required=True)
    guess.add_argument("--b", type=float, required=True)
    guess.set_defaults(func=cmd_guess_order)

    utm = sub.add_parser("utm", help="Recommend a UTM zone and EPSG code.")
    utm.add_argument("--lon", type=float, required=True)
    utm.add_argument("--lat", type=float, required=True)
    utm.set_defaults(func=cmd_utm)

    china = sub.add_parser("china-check", help="Flag common China mapping offset risk.")
    china.add_argument("--lon", type=float, required=True)
    china.add_argument("--lat", type=float, required=True)
    china.set_defaults(func=cmd_china_check)

    recommend = sub.add_parser("recommend", help="Recommend a CRS for a concrete task.")
    recommend.add_argument("--lon", type=float, required=True)
    recommend.add_argument("--lat", type=float, required=True)
    recommend.add_argument(
        "--task",
        choices=["exchange", "web-map", "analysis"],
        required=True,
    )
    recommend.set_defaults(func=cmd_recommend)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
