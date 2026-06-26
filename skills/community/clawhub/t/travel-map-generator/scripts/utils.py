#!/usr/bin/env python3
"""Shared utilities for travel-map-generator skill.

Provides Web Mercator projection, viewport calculation, adaptive icon sizing,
overlap resolution, and nearest-neighbor route ordering.
"""

import json
import math
import os
from typing import List, Dict, Tuple, Optional


# ---------------------------------------------------------------------------
# Web Mercator Projection
# ---------------------------------------------------------------------------

def latlng_to_pixel(
    lat: float,
    lng: float,
    center_lat: float,
    center_lng: float,
    zoom: float,
    img_width: int,
    img_height: int,
) -> Tuple[int, int]:
    """Convert latitude/longitude to pixel coordinates on a map screenshot.

    Uses Web Mercator (EPSG:3857) projection matching Google Maps.

    Args:
        lat, lng: Target point coordinates.
        center_lat, center_lng: Map center coordinates (what the screenshot is centered on).
        zoom: Google Maps zoom level (supports fractional values).
        img_width, img_height: Screenshot dimensions in pixels.

    Returns:
        (px_x, px_y) pixel position on the screenshot image.
    """
    scale = 256 * (2 ** zoom)

    # World pixel for the target point
    target_wx = ((lng + 180.0) / 360.0) * scale
    sin_lat = math.sin(math.radians(lat))
    # Clamp to avoid math domain errors near poles
    sin_lat = max(-0.9999, min(0.9999, sin_lat))
    target_wy = (0.5 - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi)) * scale

    # World pixel for the center
    center_wx = ((center_lng + 180.0) / 360.0) * scale
    sin_center = math.sin(math.radians(center_lat))
    sin_center = max(-0.9999, min(0.9999, sin_center))
    center_wy = (0.5 - math.log((1 + sin_center) / (1 - sin_center)) / (4 * math.pi)) * scale

    # Pixel position on the screenshot
    px_x = int((target_wx - center_wx) + img_width / 2)
    px_y = int((target_wy - center_wy) + img_height / 2)

    return (px_x, px_y)


# ---------------------------------------------------------------------------
# Viewport Computation
# ---------------------------------------------------------------------------

def compute_viewport(
    pois: List[Dict],
    img_width: int = 1536,
    img_height: int = 1024,
    padding_factor: float = 0.25,
) -> Dict:
    """Compute the optimal map center and zoom level to fit all POIs.

    Args:
        pois: List of dicts with 'lat' and 'lng' keys.
        img_width, img_height: Desired output image dimensions.
        padding_factor: Extra padding around the bounding box (0.25 = 25%).

    Returns:
        Dict with 'center_lat', 'center_lng', 'zoom'.
    """
    if not pois:
        raise ValueError("At least one POI is required")

    lats = [p["lat"] for p in pois]
    lngs = [p["lng"] for p in pois]

    min_lat, max_lat = min(lats), max(lats)
    min_lng, max_lng = min(lngs), max(lngs)

    center_lat = (min_lat + max_lat) / 2.0
    center_lng = (min_lng + max_lng) / 2.0

    # Add padding
    lat_span = (max_lat - min_lat) * (1 + padding_factor)
    lng_span = (max_lng - min_lng) * (1 + padding_factor)

    # Ensure minimum span for single-point cases
    lat_span = max(lat_span, 0.01)
    lng_span = max(lng_span, 0.01)

    # Find the best zoom level
    # For longitude: visible_lng_span = 360 * img_width / (256 * 2^zoom)
    # For latitude: more complex due to Mercator, but approximate similarly
    zoom_lng = math.log2(360.0 * img_width / (256.0 * lng_span)) if lng_span > 0 else 18
    zoom_lat = math.log2(180.0 * img_height / (256.0 * lat_span)) if lat_span > 0 else 18

    zoom = min(zoom_lng, zoom_lat)
    # Clamp zoom and subtract a small margin for safety
    zoom = max(1, min(18, zoom - 0.5))
    # Round to one decimal for cleaner URLs
    zoom = round(zoom, 1)

    return {
        "center_lat": round(center_lat, 6),
        "center_lng": round(center_lng, 6),
        "zoom": zoom,
    }


# ---------------------------------------------------------------------------
# Adaptive Icon Sizing
# ---------------------------------------------------------------------------

def compute_icon_size(num_pois: int, map_width: int, map_height: int) -> int:
    """Compute adaptive icon size based on number of POIs and map dimensions.

    Formula: base_size * (5 / num_pois) ^ 0.4, clamped to [60, 280].

    Args:
        num_pois: Number of POI icons to place.
        map_width, map_height: Map image dimensions.

    Returns:
        Icon diameter in pixels.
    """
    if num_pois <= 0:
        return 180

    base_size = min(map_width, map_height) * 0.18
    scale_factor = (5.0 / num_pois) ** 0.4
    icon_size = int(base_size * scale_factor)
    return max(60, min(280, icon_size))


# ---------------------------------------------------------------------------
# Overlap Resolution
# ---------------------------------------------------------------------------

def resolve_overlaps(
    positions: List[Tuple[int, int]],
    icon_size: int,
    max_iterations: int = 50,
) -> List[Tuple[int, int]]:
    """Nudge overlapping icon positions apart.

    Uses a simple repulsion algorithm: iteratively push overlapping icons
    away from each other until no overlaps remain or max iterations reached.

    Args:
        positions: List of (x, y) pixel positions.
        icon_size: Diameter of each icon.
        max_iterations: Maximum adjustment iterations.

    Returns:
        Adjusted list of (x, y) positions.
    """
    if len(positions) <= 1:
        return list(positions)

    min_dist = icon_size * 0.85  # Allow slight overlap for aesthetics
    pos = [list(p) for p in positions]

    for _ in range(max_iterations):
        moved = False
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                dx = pos[j][0] - pos[i][0]
                dy = pos[j][1] - pos[i][1]
                dist = math.sqrt(dx * dx + dy * dy)

                if dist < min_dist and dist > 0:
                    # Push apart
                    overlap = (min_dist - dist) / 2.0
                    nx = dx / dist
                    ny = dy / dist
                    pos[i][0] -= int(nx * overlap)
                    pos[i][1] -= int(ny * overlap)
                    pos[j][0] += int(nx * overlap)
                    pos[j][1] += int(ny * overlap)
                    moved = True
                elif dist == 0:
                    # Identical positions: offset diagonally
                    pos[j][0] += int(min_dist * 0.5)
                    pos[j][1] += int(min_dist * 0.5)
                    moved = True

        if not moved:
            break

    return [(int(p[0]), int(p[1])) for p in pos]


# ---------------------------------------------------------------------------
# Route Ordering (Nearest Neighbor TSP)
# ---------------------------------------------------------------------------

def _haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Haversine distance in kilometers between two coordinates."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlng / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def nearest_neighbor_route(pois: List[Dict]) -> List[int]:
    """Compute a visit order using greedy nearest-neighbor heuristic.

    Starts from the POI closest to the geographic centroid, then greedily
    visits the nearest unvisited POI.

    Args:
        pois: List of dicts with 'lat' and 'lng' keys.

    Returns:
        List of indices representing the visit order.
    """
    n = len(pois)
    if n <= 1:
        return list(range(n))

    # Find centroid
    avg_lat = sum(p["lat"] for p in pois) / n
    avg_lng = sum(p["lng"] for p in pois) / n

    # Start from the POI closest to centroid
    start = min(range(n), key=lambda i: _haversine(avg_lat, avg_lng, pois[i]["lat"], pois[i]["lng"]))

    visited = [start]
    remaining = set(range(n)) - {start}

    while remaining:
        current = visited[-1]
        nearest = min(
            remaining,
            key=lambda i: _haversine(
                pois[current]["lat"], pois[current]["lng"],
                pois[i]["lat"], pois[i]["lng"],
            ),
        )
        visited.append(nearest)
        remaining.remove(nearest)

    return visited


# ---------------------------------------------------------------------------
# Palette Loading
# ---------------------------------------------------------------------------

def load_ghibli_palette(palette_path: Optional[str] = None) -> Dict[str, str]:
    """Load the Ghibli color palette from JSON.

    Args:
        palette_path: Path to palette JSON. Defaults to assets/ghibli_palette.json
                      relative to this script's parent directory.

    Returns:
        Dict mapping element names to color hex strings.
    """
    if palette_path is None:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        palette_path = os.path.join(skill_dir, "assets", "ghibli_palette.json")

    with open(palette_path, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Quick sanity checks
    print("=== Utils Self-Test ===")

    # Test Mercator projection: Tokyo Tower
    px = latlng_to_pixel(35.6586, 139.7454, 35.68, 139.76, 13, 1536, 1024)
    print(f"Tokyo Tower pixel position (zoom 13, center 35.68/139.76): {px}")
    assert 0 <= px[0] <= 1536, f"x out of range: {px[0]}"
    assert 0 <= px[1] <= 1024, f"y out of range: {px[1]}"

    # Test viewport computation
    test_pois = [
        {"lat": 35.6586, "lng": 139.7454, "name": "Tokyo Tower"},
        {"lat": 35.7148, "lng": 139.7967, "name": "Senso-ji"},
        {"lat": 35.6595, "lng": 139.7004, "name": "Shibuya Crossing"},
    ]
    vp = compute_viewport(test_pois)
    print(f"Viewport for Tokyo POIs: {vp}")
    assert 35.0 < vp["center_lat"] < 36.0
    assert 139.0 < vp["center_lng"] < 140.0

    # Test icon sizing
    for n in [3, 5, 8, 10]:
        size = compute_icon_size(n, 1536, 1024)
        print(f"  {n} POIs -> icon size: {size}px")
    assert compute_icon_size(3, 1536, 1024) > compute_icon_size(10, 1536, 1024)

    # Test overlap resolution
    overlapping = [(100, 100), (110, 105), (500, 500)]
    resolved = resolve_overlaps(overlapping, 150)
    print(f"Overlap resolution: {overlapping} -> {resolved}")

    # Test route ordering
    route = nearest_neighbor_route(test_pois)
    print(f"Route order: {route}")
    assert len(route) == 3
    assert set(route) == {0, 1, 2}

    print("\nAll tests passed!")
