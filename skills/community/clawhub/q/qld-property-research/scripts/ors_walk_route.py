#!/usr/bin/env python3
"""Fetch a walking route from openrouteservice for station-access scoring."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

ORS_URL = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"
ATTRIBUTION = "© openrouteservice.org by HeiGIT | Map data © OpenStreetMap contributors"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a walking route from openrouteservice as GeoJSON."
    )
    parser.add_argument("--from-lon", type=float, required=True)
    parser.add_argument("--from-lat", type=float, required=True)
    parser.add_argument("--to-lon", type=float, required=True)
    parser.add_argument("--to-lat", type=float, required=True)
    parser.add_argument(
        "--timeout-seconds", type=int, default=30, help="HTTP timeout in seconds"
    )
    return parser.parse_args()


def get_api_key() -> str | None:
    return os.environ.get("ORS_API_KEY") or os.environ.get("OPENROUTESERVICE_API_KEY")


def fetch_route(args: argparse.Namespace, api_key: str) -> dict:
    payload = {
        "coordinates": [
            [args.from_lon, args.from_lat],
            [args.to_lon, args.to_lat],
        ],
        "instructions": True,
        "units": "m",
    }
    req = urllib.request.Request(
        ORS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
            "Accept": "application/geo+json, application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=args.timeout_seconds) as resp:
        return json.load(resp)


def summarize_route(route_doc: dict) -> dict:
    features = route_doc.get("features") or []
    if not features:
        raise SystemExit("openrouteservice returned no route features.")

    feature = features[0]
    props = feature.get("properties") or {}
    segments = props.get("segments") or []
    summary = props.get("summary") or {}

    step_count = sum(len(segment.get("steps") or []) for segment in segments)

    return {
        "distance_m": summary.get("distance"),
        "duration_s": summary.get("duration"),
        "step_count": step_count,
        "attribution": ATTRIBUTION,
        "route": route_doc,
    }


def main() -> int:
    args = parse_args()
    api_key = get_api_key()
    if not api_key:
        print(
            json.dumps(
                {
                    "status": "not_configured",
                    "provider": "openrouteservice",
                    "message": "Missing API key. Set ORS_API_KEY (preferred) or OPENROUTESERVICE_API_KEY.",
                    "attribution": ATTRIBUTION,
                },
                indent=2,
            )
        )
        return 0
    try:
        route_doc = fetch_route(args, api_key)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(
            json.dumps(
                {
                    "error": "openrouteservice_http_error",
                    "status": exc.code,
                    "body": body,
                },
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1
    except urllib.error.URLError as exc:
        print(
            json.dumps(
                {"error": "openrouteservice_connection_error", "reason": str(exc)},
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1

    print(json.dumps(summarize_route(route_doc), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
