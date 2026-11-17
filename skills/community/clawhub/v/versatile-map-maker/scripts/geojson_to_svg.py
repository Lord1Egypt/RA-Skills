#!/usr/bin/env python3
"""Convert Polygon/MultiPolygon GeoJSON into an editable SVG base map.

This is intentionally dependency-light. It uses an equirectangular lon/lat
projection and writes a matching affine transform for later overlays.
"""
import argparse
import html
import json
import re
from pathlib import Path


COMMON_ID_FIELDS = ["id", "GEOID", "geo_id", "ISO_A2", "ISO_A3", "hc-key", "hasc", "name", "NAME"]


def slug(value):
    s = re.sub(r"[^A-Za-z0-9_.-]+", "-", str(value).strip())
    return s.strip("-") or "region"


def iter_polygons(geometry):
    if not geometry:
        return
    gtype = geometry.get("type")
    coords = geometry.get("coordinates", [])
    if gtype == "Polygon":
        yield coords
    elif gtype == "MultiPolygon":
        for poly in coords:
            yield poly


def all_lonlat(features):
    for feat in features:
        for poly in iter_polygons(feat.get("geometry")):
            for ring in poly:
                for lon, lat, *_ in ring:
                    yield float(lon), float(lat)


def pick_id(props, fallback, id_field):
    if id_field and props.get(id_field) not in (None, ""):
        return slug(props[id_field])
    for key in COMMON_ID_FIELDS:
        if props.get(key) not in (None, ""):
            return slug(props[key])
    return f"region-{fallback}"


def project(lon, lat, min_lon, max_lat, scale, pad):
    return (lon - min_lon) * scale + pad, (max_lat - lat) * scale + pad


def ring_path(ring, min_lon, max_lat, scale, pad):
    pts = [project(float(lon), float(lat), min_lon, max_lat, scale, pad) for lon, lat, *_ in ring]
    if not pts:
        return ""
    return "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("geojson")
    ap.add_argument("out_svg")
    ap.add_argument("--id-field")
    ap.add_argument("--name-field", default="name")
    ap.add_argument("--width", type=float, default=1000)
    ap.add_argument("--padding", type=float, default=20)
    ap.add_argument("--metadata-out")
    ap.add_argument("--transform-out")
    args = ap.parse_args()

    data = json.loads(Path(args.geojson).read_text(encoding="utf-8"))
    features = data.get("features", [])
    pts = list(all_lonlat(features))
    if not pts:
        raise SystemExit("No Polygon or MultiPolygon coordinates found in GeoJSON.")

    min_lon, max_lon = min(p[0] for p in pts), max(p[0] for p in pts)
    min_lat, max_lat = min(p[1] for p in pts), max(p[1] for p in pts)
    lon_span = max(max_lon - min_lon, 1e-9)
    lat_span = max(max_lat - min_lat, 1e-9)
    scale = (args.width - 2 * args.padding) / lon_span
    height = lat_span * scale + 2 * args.padding

    paths = []
    index = []
    used = {}
    for i, feat in enumerate(features, start=1):
        props = feat.get("properties", {})
        rid = pick_id(props, i, args.id_field)
        if rid in used:
            used[rid] += 1
            rid = f"{rid}-{used[rid]}"
        else:
            used[rid] = 1
        name = props.get(args.name_field) or props.get("NAME") or props.get("name") or rid
        d_parts = []
        for poly in iter_polygons(feat.get("geometry")):
            for ring in poly:
                d = ring_path(ring, min_lon, max_lat, scale, args.padding)
                if d:
                    d_parts.append(d)
        if not d_parts:
            continue
        paths.append(
            f'<path id="{html.escape(rid)}" data-name="{html.escape(str(name))}" '
            f'd="{" ".join(d_parts)}" fill="#EDEAE3" stroke="#B9B3A6" stroke-width="0.7"/>'
        )
        index.append({"id": rid, "name": name, "properties": props})

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {args.width:.2f} {height:.2f}">\n'
        '<g id="regions">\n' + "\n".join(paths) + "\n</g>\n</svg>\n"
    )
    Path(args.out_svg).write_text(svg, encoding="utf-8")
    if args.metadata_out:
        Path(args.metadata_out).write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.transform_out:
        transform = {
            "coef_x": [scale, 0.0, args.padding - min_lon * scale],
            "coef_y": [0.0, -scale, args.padding + max_lat * scale],
            "mean_error_px": 0.0,
            "max_error_px": 0.0,
            "projection": "equirectangular",
        }
        Path(args.transform_out).write_text(json.dumps(transform, indent=2), encoding="utf-8")
    print(f"Wrote {args.out_svg} ({len(paths)} regions)")


if __name__ == "__main__":
    main()

