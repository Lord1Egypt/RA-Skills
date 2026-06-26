# Coordinate Mapping Reference

## Web Mercator Projection (EPSG:3857)

Google Maps uses the Web Mercator projection. This document details the math
used by `utils.py` to convert latitude/longitude coordinates into pixel
positions on a map screenshot.

## Core Formula

### Lat/Lng to World Pixel

At zoom level `z`, the entire world map is `256 * 2^z` pixels wide and tall.

```
scale = 256 * 2^z

world_x = ((lng + 180) / 360) * scale

sin_lat = sin(lat * PI / 180)
world_y = (0.5 - ln((1 + sin_lat) / (1 - sin_lat)) / (4 * PI)) * scale
```

### World Pixel to Screenshot Pixel

Given a map screenshot centered at `(center_lat, center_lng)` with dimensions
`(img_width, img_height)`:

1. Compute world pixels for both the center and the target point
2. The screenshot pixel position is:

```
screen_x = (target_world_x - center_world_x) + img_width / 2
screen_y = (target_world_y - center_world_y) + img_height / 2
```

## Computing Optimal Zoom Level

To fit all POIs within the viewport:

1. Find the bounding box of all POI coordinates
2. Add padding (default 25%)
3. For each candidate zoom level, compute the visible geographic span
4. Choose the maximum zoom level where both lat and lng spans fit
5. Subtract 0.5 for safety margin

### Visible span at zoom `z`

```
visible_lng_span = 360 * img_width / (256 * 2^z)
visible_lat_span ≈ 180 * img_height / (256 * 2^z)  (approximate, exact requires inverse Mercator)
```

## Fractional Zoom

Google Maps supports fractional zoom levels (e.g., `14.5z`).
The formula handles this naturally since `2^z` works with floats.

## Edge Cases

### Anti-Meridian Crossing
If POIs span across longitude 180/-180 (e.g., Pacific islands), the bounding
box calculation needs to detect this and use a wrapped longitude span.

**Detection**: If `max_lng - min_lng > 180`, the POIs likely cross the
anti-meridian. In this case, shift longitudes by 360 for the western group
before computing the bounding box.

### Extreme Latitudes
Mercator projection becomes infinite at the poles. The `sin_lat` value is
clamped to `[-0.9999, 0.9999]` (roughly ±89.4 degrees) to prevent math
domain errors.

### POIs Spread Too Far Apart
If the lat/lng span exceeds 5 degrees in either direction, the resulting
map will be zoomed out too far to show useful detail. The SKILL.md instructs
the agent to warn the user and suggest splitting into multiple regional maps.

### Google Maps UI Chrome
The actual visible map area may be slightly offset from the geometric center
due to Google Maps UI elements (search bar, controls). The stylize_map.py
script processes the full screenshot, and the agent should try to hide UI
elements before taking the screenshot.

## Accuracy Considerations

The coordinate-to-pixel mapping assumes:
- The screenshot is taken at exactly the computed center and zoom
- No UI overlays shift the map center
- The browser viewport matches the expected dimensions

In practice, small offsets (5-15 pixels) are acceptable since the icons
are large enough to visually convey the correct location.
