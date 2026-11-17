#!/usr/bin/env python3
"""
Pull real river geometry from Natural Earth (public domain, 1:10m scale) —
for tracing boundary stretches that historically followed a river, instead
of guessing coordinates by hand.

Two modes:

1) Fetch named rivers' full geometry:
   python fetch_rivers.py "Danube" "Sava" "Drina" --out rivers.json

2) Slice a fetched river between two lon,lat anchor points (nearest-point
   matching on each end, returned in anchor1 -> anchor2 order):
   python fetch_rivers.py --slice rivers.json "Danube" 20.455,44.840 22.545,44.226 --out danube_seg.json

Coverage: the global 10m rivers file covers major rivers worldwide; the
Europe supplement adds smaller named tributaries within Europe. If a river
name isn't found, this prints what's available with a similar name — don't
guess coordinates by hand as a silent fallback, tell the user instead.
"""
import json
import sys
import os
import tempfile
import urllib.request
from pathlib import Path

MAIN_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_rivers_lake_centerlines.geojson"
EUROPE_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_rivers_europe.geojson"


def default_cache_dir():
    root = os.environ.get("XDG_CACHE_HOME") or os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()
    return Path(root) / "versatile-map-maker" / "natural-earth-rivers"


def ensure_files():
    cache_dir = default_cache_dir()
    cache_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for url in (MAIN_URL, EUROPE_URL):
        fname = cache_dir / url.split("/")[-1]
        if not fname.exists():
            print(f"Downloading {fname.name} (first run only, cached after)...", file=sys.stderr)
            urllib.request.urlretrieve(url, fname)
        paths.append(fname)
    return paths


def load_all_features():
    feats = []
    for p in ensure_files():
        d = json.loads(p.read_text())
        feats.extend(d["features"])
    return feats


def feature_name(props):
    return props.get("name") or props.get("name_en")


def as_parts(geometry):
    """Normalize LineString/MultiLineString geometry to a list of parts."""
    if geometry["type"] == "LineString":
        return [geometry["coordinates"]]
    if geometry["type"] == "MultiLineString":
        return geometry["coordinates"]
    return []


def fetch(names, out_path):
    feats = load_all_features()
    all_names = [feature_name(f["properties"]) for f in feats if feature_name(f["properties"])]
    result = {}
    for name in names:
        matches = [f for f in feats if feature_name(f["properties"]) == name]
        if not matches:
            similar = sorted({n for n in all_names if name.lower() in n.lower()})[:8]
            print(f"'{name}' not found in Natural Earth rivers data."
                  + (f" Similar names available: {similar}" if similar else " No similar names found either — this stretch likely needs a schematic line instead."),
                  file=sys.stderr)
            continue
        # if multiple features share a name, keep all their parts together
        parts = []
        for f in matches:
            parts.extend(as_parts(f["geometry"]))
        result[name] = parts
        print(f"'{name}': {len(parts)} part(s), {sum(len(p) for p in parts)} total points")
    Path(out_path).write_text(json.dumps(result))
    print(f"Wrote {out_path}")


def nearest(coords, target):
    tx, ty = target
    best_i, best_d = 0, float("inf")
    for i, (x, y) in enumerate(coords):
        d = (x - tx) ** 2 + (y - ty) ** 2
        if d < best_d:
            best_d = d
            best_i = i
    return best_i, best_d ** 0.5


def slice_river(rivers_path, name, anchor1, anchor2, out_path):
    rivers = json.loads(Path(rivers_path).read_text())
    if name not in rivers:
        print(f"'{name}' not in {rivers_path}. Available: {list(rivers.keys())}", file=sys.stderr)
        sys.exit(1)
    parts = rivers[name]
    best = None  # (total_err, part_idx, i1, i2)
    for pi, part in enumerate(parts):
        i1, e1 = nearest(part, anchor1)
        i2, e2 = nearest(part, anchor2)
        if best is None or (e1 + e2) < best[0]:
            best = (e1 + e2, pi, i1, i2)
    total_err, pi, i1, i2 = best
    part = parts[pi]
    lo, hi = min(i1, i2), max(i1, i2)
    seg = part[lo:hi + 1]
    if i1 > i2:
        seg = list(reversed(seg))
    print(f"Matched part {pi}, anchor errors: {(total_err):.4f} deg total "
          f"(~{total_err * 111:.0f} km combined) — {len(seg)} points, "
          f"anchor1-first order.")
    Path(out_path).write_text(json.dumps(seg))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    if args[0] == "--slice":
        rivers_path, name, a1, a2 = args[1], args[2], args[3], args[4]
        out_idx = args.index("--out")
        out_path = args[out_idx + 1]
        lon1, lat1 = map(float, a1.split(","))
        lon2, lat2 = map(float, a2.split(","))
        slice_river(rivers_path, name, (lon1, lat1), (lon2, lat2), out_path)
    else:
        out_idx = args.index("--out")
        names = args[:out_idx]
        out_path = args[out_idx + 1]
        fetch(names, out_path)
