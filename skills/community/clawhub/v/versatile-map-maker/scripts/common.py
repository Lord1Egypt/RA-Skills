"""Shared helpers for the choropleth-map-maker skill scripts."""
import re


def extract_paths(svg_text):
    """Return list of (id, d) for every <path id="..." ... d="..."> in the SVG.

    Handles attribute order in either direction (id before or after d).
    """
    out = []
    for m in re.finditer(r'<path\b[^>]*>', svg_text):
        tag = m.group(0)
        id_m = re.search(r'id="([^"]+)"', tag)
        d_m = re.search(r'\bd="([^"]+)"', tag)
        if id_m and d_m:
            out.append((id_m.group(1), d_m.group(1)))
    return out


def parse_path_points(d):
    """Crude path-data parser: collects absolute x,y coordinate pairs.

    Good enough for Highcharts/Highmaps-style paths (M/L/Z with absolute
    coordinates). Does not handle curves (C/Q/A) — those are rare in these
    base maps but if you hit one, fall back to a bounding-box centroid.
    """
    pts = []
    for x, y in re.findall(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', d):
        pts.append((float(x), float(y)))
    return pts


def polygon_centroid(pts):
    """Shoelace-formula centroid of a (possibly unclosed) polygon ring."""
    n = len(pts)
    if n == 0:
        return 0.0, 0.0
    A = Cx = Cy = 0.0
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        cross = x0 * y1 - x1 * y0
        A += cross
        Cx += (x0 + x1) * cross
        Cy += (y0 + y1) * cross
    A *= 0.5
    if abs(A) < 1e-9:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return sum(xs) / n, sum(ys) / n
    return Cx / (6 * A), Cy / (6 * A)


def largest_subpath_centroid(d):
    """Centroid of the largest subpath in a (possibly multi-part) path's `d`.

    Splits on 'M' command starts; picks the subpath with the most points
    (usually the main landmass/region, not a small island or hole).
    """
    subpaths = [s for s in re.split(r'(?=M)', d) if s.strip()]
    best_pts, best_n = [], -1
    for sp in subpaths:
        pts = parse_path_points(sp)
        if len(pts) > best_n:
            best_n = len(pts)
            best_pts = pts
    return polygon_centroid(best_pts)


def svg_bbox(svg_text):
    """Bounding box (minx, maxx, miny, maxy) over every path coordinate."""
    xs, ys = [], []
    for _id, d in extract_paths(svg_text):
        for x, y in parse_path_points(d):
            xs.append(x)
            ys.append(y)
    return min(xs), max(xs), min(ys), max(ys)


def haversine_km(lon1, lat1, lon2, lat2):
    import math
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))
