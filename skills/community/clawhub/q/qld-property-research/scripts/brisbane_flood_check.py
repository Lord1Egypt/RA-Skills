#!/usr/bin/env python3
"""Query Brisbane's public flood-awareness services without using the browser UI."""

from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request

GEOCODER = (
    "https://spatial-gis.information.qld.gov.au/arcgis/rest/services/Location/"
    "QldCompositeLocator/GeocodeServer/findAddressCandidates"
)
PARCELS = (
    "https://services2.arcgis.com/dEKgZETqwmDAh1rP/arcgis/rest/services/"
    "property_boundaries_parcel/FeatureServer/0/query"
)
METRICS = (
    "https://services2.arcgis.com/dEKgZETqwmDAh1rP/arcgis/rest/services/"
    "FAM_Property_Parcel_Metrics/FeatureServer/0/query"
)
FLOOD_LAYERS = {
    "flood_risk_overall": (
        "https://services2.arcgis.com/dEKgZETqwmDAh1rP/arcgis/rest/services/"
        "Flood_Awareness_Flood_Risk_Overall/FeatureServer/0/query"
    ),
    "overland_overall_1pct": (
        "https://services2.arcgis.com/dEKgZETqwmDAh1rP/arcgis/rest/services/"
        "Flood_Awareness_Overland_Flow_Overall_1percent_Annual_Chance/"
        "FeatureServer/0/query"
    ),
    "overland": (
        "https://services2.arcgis.com/dEKgZETqwmDAh1rP/arcgis/rest/services/"
        "Flood_Awareness_Overland_Flow/FeatureServer/0/query"
    ),
    "creek": (
        "https://services2.arcgis.com/dEKgZETqwmDAh1rP/arcgis/rest/services/"
        "Flood_Awareness_Creek/FeatureServer/0/query"
    ),
    "river": (
        "https://services2.arcgis.com/dEKgZETqwmDAh1rP/arcgis/rest/services/"
        "Flood_Awareness_River/FeatureServer/0/query"
    ),
    "storm_tide": (
        "https://services2.arcgis.com/dEKgZETqwmDAh1rP/arcgis/rest/services/"
        "Flood_Awareness_Storm_Tide/FeatureServer/0/query"
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query Brisbane flood-awareness services for an address."
    )
    parser.add_argument("--address", required=True, help="Full Brisbane street address")
    parser.add_argument(
        "--timeout-seconds", type=int, default=30, help="HTTP timeout in seconds"
    )
    return parser.parse_args()


def fetch_json(url: str, timeout_seconds: int) -> dict:
    with urllib.request.urlopen(url, timeout=timeout_seconds) as resp:
        return json.load(resp)


def geocode(address: str, timeout_seconds: int) -> dict:
    url = GEOCODER + "?" + urllib.parse.urlencode({"SingleLine": address, "f": "pjson"})
    obj = fetch_json(url, timeout_seconds)
    candidates = obj.get("candidates") or []
    if not candidates:
        raise SystemExit("No geocoder candidates returned for the supplied address.")
    return candidates[0]


def get_parcel(lon: float, lat: float, timeout_seconds: int) -> dict:
    params = {
        "f": "pjson",
        "geometry": json.dumps({"x": lon, "y": lat, "spatialReference": {"wkid": 4283}}),
        "geometryType": "esriGeometryPoint",
        "inSR": "4283",
        "spatialRel": "esriSpatialRelIntersects",
        "returnGeometry": "true",
        "outFields": (
            "LOTPLAN,PROPERTY_ID,HOUSE_NUMBER,CORRIDOR_NAME,SUBURB,POSTCODE,"
            "CITY_PLAN_AREA,LOT_TITLE_AREA"
        ),
    }
    url = PARCELS + "?" + urllib.parse.urlencode(params)
    obj = fetch_json(url, timeout_seconds)
    features = obj.get("features") or []
    if not features:
        raise SystemExit("No Brisbane parcel matched the supplied coordinates.")
    return features[0]


def get_metrics(lotplan: str, timeout_seconds: int) -> dict:
    params = {
        "where": f"LOTPLAN='{lotplan}'",
        "returnGeometry": "false",
        "outFields": "*",
        "f": "pjson",
    }
    url = METRICS + "?" + urllib.parse.urlencode(params)
    obj = fetch_json(url, timeout_seconds)
    metrics = {}
    for feature in obj.get("features") or []:
        attrs = feature["attributes"]
        metrics[attrs["METRIC"]] = attrs["VALUE"]
    return metrics


def get_flood_counts(geometry: dict, timeout_seconds: int) -> dict:
    geom = json.dumps(geometry)
    counts = {}
    for key, base in FLOOD_LAYERS.items():
        params = {
            "f": "pjson",
            "geometry": geom,
            "geometryType": "esriGeometryPolygon",
            "inSR": "28356",
            "spatialRel": "esriSpatialRelIntersects",
            "returnGeometry": "false",
            "outFields": "*",
        }
        url = base + "?" + urllib.parse.urlencode(params)
        obj = fetch_json(url, timeout_seconds)
        counts[key] = len(obj.get("features") or [])
    return counts


def summarize(address_candidate: dict, parcel: dict, metrics: dict, counts: dict) -> dict:
    attrs = parcel["attributes"]
    any_hits = any(counts.values())
    if any_hits:
        result = "Mapped flood overlap present on one or more Brisbane awareness layers."
        subscore = 20
        interpretation = (
            "The parcel intersects at least one current Brisbane flood-awareness layer "
            "and needs closer review."
        )
    else:
        result = "No current parcel overlap found on Brisbane flood-awareness layers."
        subscore = 95
        interpretation = (
            "The parcel does not intersect the current Brisbane flood-awareness layers. "
            "Treat this as lower mapped risk, not no flood risk."
        )

    return {
        "status": "ok",
        "address": address_candidate["address"],
        "property": {
            "lotplan": attrs["LOTPLAN"],
            "property_id": attrs["PROPERTY_ID"],
            "city_plan_area": attrs["CITY_PLAN_AREA"],
            "lot_title_area": attrs["LOT_TITLE_AREA"],
            "coordinates": {
                "lon": address_candidate["location"]["x"],
                "lat": address_candidate["location"]["y"],
            },
        },
        "flood": {
            "result": result,
            "layer_hits": counts,
            "metrics": metrics,
            "recommended_subscore": subscore,
            "interpretation": interpretation,
        },
        "sources": {
            "geocoder": GEOCODER,
            "parcel_boundaries": PARCELS,
            "parcel_metrics": METRICS,
            "flood_layers": FLOOD_LAYERS,
        },
    }


def main() -> int:
    args = parse_args()
    candidate = geocode(args.address, args.timeout_seconds)
    parcel = get_parcel(
        candidate["location"]["x"], candidate["location"]["y"], args.timeout_seconds
    )
    metrics = get_metrics(parcel["attributes"]["LOTPLAN"], args.timeout_seconds)
    counts = get_flood_counts(parcel["geometry"], args.timeout_seconds)
    print(json.dumps(summarize(candidate, parcel, metrics, counts), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
