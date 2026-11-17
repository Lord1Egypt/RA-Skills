#!/usr/bin/env python3
"""
Fit an affine (lon, lat) -> (px, py) transform using a base map's own region
centroids: real polygon centroids from the SVG paths, paired with each
region's longitude/latitude from the matching GeoJSON.

This is far more accurate than using the GeoJSON's given label-point
lon/lat against the SVG's *label position* (hc-middle-x/y) — computing true
polygon centroids on both sides typically gets mean error down to a few
pixels on a ~700px map.

Usage:
    python fit_transform.py <map.svg> <map.geo.json> <out transform.json>
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import extract_paths, largest_subpath_centroid


def region_id(props):
    """Best-effort id matching the SVG path's id attribute for this feature."""
    if "hasc" in props and props["hasc"]:
        return props["hasc"]
    if "hc-key" in props and props["hc-key"]:
        # e.g. 'us-ca' -> 'US.CA' (the usual Highcharts SVG id convention)
        parts = props["hc-key"].split("-")
        if len(parts) >= 2:
            return f"{parts[0].upper()}.{'-'.join(parts[1:]).upper()}"
        return props["hc-key"].upper()
    return None


def main(svg_path, geo_path, out_path):
    svg = Path(svg_path).read_text()
    geo = json.loads(Path(geo_path).read_text())

    px_centroids = {}
    for pid, d in extract_paths(svg):
        px_centroids[pid] = largest_subpath_centroid(d)

    lons, lats, pxs, pys = [], [], [], []
    unmatched = []
    for feat in geo["features"]:
        props = feat["properties"]
        rid = region_id(props)
        if rid is None or rid not in px_centroids:
            unmatched.append(props.get("name", "?"))
            continue
        if "longitude" not in props or "latitude" not in props:
            continue
        lons.append(float(props["longitude"]))
        lats.append(float(props["latitude"]))
        cx, cy = px_centroids[rid]
        pxs.append(cx)
        pys.append(cy)

    if len(lons) < 3:
        print(f"Only matched {len(lons)} regions between SVG and GeoJSON — "
              f"can't fit a reliable transform. Unmatched: {unmatched[:10]}",
              file=sys.stderr)
        sys.exit(1)

    lons, lats = np.array(lons), np.array(lats)
    pxs, pys = np.array(pxs), np.array(pys)
    A = np.column_stack([lons, lats, np.ones_like(lons)])
    coef_x, *_ = np.linalg.lstsq(A, pxs, rcond=None)
    coef_y, *_ = np.linalg.lstsq(A, pys, rcond=None)

    pred_x = A @ coef_x
    pred_y = A @ coef_y
    err = np.sqrt((pred_x - pxs) ** 2 + (pred_y - pys) ** 2)

    print(f"Fit using {len(lons)} regions. Mean px error: {err.mean():.2f}, "
          f"max: {err.max():.2f}")
    if unmatched:
        print(f"Note: {len(unmatched)} feature(s) in the GeoJSON had no matching "
              f"SVG path id and were skipped: {unmatched[:10]}", file=sys.stderr)

    Path(out_path).write_text(json.dumps({
        "coef_x": coef_x.tolist(),
        "coef_y": coef_y.tolist(),
        "mean_error_px": float(err.mean()),
        "max_error_px": float(err.max()),
    }, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    main(*sys.argv[1:4])
