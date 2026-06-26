#!/usr/bin/env python3
"""Main compositing engine for travel-map-generator skill.

Takes a stylized map background, POI icon images, coordinate metadata,
and route information, then produces the final illustrated travel map PNG.

Usage:
    python3 composite.py --map stylized_map.png --config config.json --output final_map.png
"""

import argparse
import json
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Add scripts directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    compute_icon_size,
    latlng_to_pixel,
    load_ghibli_palette,
    nearest_neighbor_route,
    resolve_overlaps,
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Sepia-brown color for route lines and borders
ROUTE_COLOR = (139, 115, 85)       # #8B7355
ROUTE_WIDTH = 3
DASH_ON = 10
DASH_OFF = 5

BADGE_FILL = (255, 248, 231)      # cream
BADGE_BORDER = (93, 78, 55)       # dark brown
BADGE_SIZE = 22

LABEL_BG = (255, 248, 231, 220)   # cream with alpha
LABEL_TEXT = (93, 78, 55)          # dark brown
LABEL_PADDING = 6

TITLE_BG = (93, 78, 55, 200)      # dark brown with alpha
TITLE_TEXT = (255, 248, 231)       # cream

SHADOW_OFFSET = 4
SHADOW_BLUR = 6
SHADOW_OPACITY = 80

ICON_BORDER_WIDTH = 3
ICON_BORDER_COLOR = (139, 115, 85)  # sepia


# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

def _get_font(size, bold=False):
    """Try to load a system font, fall back to default."""
    font_candidates = [
        # macOS fonts
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        # Linux fonts
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        # Windows fonts
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for font_path in font_candidates:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except (IOError, OSError):
                continue
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Drawing primitives
# ---------------------------------------------------------------------------

def _create_circular_icon(icon_img, size):
    """Resize an icon image, apply circular mask with border and shadow.

    Returns:
        (icon_rgba, shadow_rgba): The masked icon and its drop shadow,
        both as RGBA images with extra padding for shadow.
    """
    total_size = size + SHADOW_OFFSET * 2 + SHADOW_BLUR * 2
    padding = SHADOW_OFFSET + SHADOW_BLUR

    # Resize icon to fill the circle
    icon_resized = icon_img.resize((size, size), Image.LANCZOS)

    # Create circular mask with antialiasing
    mask_size = size * 4  # supersample for smooth edges
    mask = Image.new("L", (mask_size, mask_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, mask_size - 1, mask_size - 1], fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)

    # Apply mask to icon
    icon_rgba = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    icon_rgb = icon_resized.convert("RGB")
    icon_rgba.paste(icon_rgb, (0, 0))
    icon_rgba.putalpha(mask)

    # Draw border ring
    border_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border_layer)
    for w in range(ICON_BORDER_WIDTH):
        border_draw.ellipse(
            [w, w, size - 1 - w, size - 1 - w],
            outline=ICON_BORDER_COLOR + (220,),
        )
    icon_rgba = Image.alpha_composite(icon_rgba, border_layer)

    # Create shadow
    shadow = Image.new("RGBA", (total_size, total_size), (0, 0, 0, 0))
    shadow_circle = Image.new("L", (size, size), 0)
    shadow_draw = ImageDraw.Draw(shadow_circle)
    shadow_draw.ellipse([0, 0, size - 1, size - 1], fill=SHADOW_OPACITY)
    shadow.paste(
        Image.new("RGBA", (size, size), (0, 0, 0, SHADOW_OPACITY)),
        (padding + SHADOW_OFFSET, padding + SHADOW_OFFSET),
        shadow_circle,
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=SHADOW_BLUR))

    # Place icon on padded canvas
    result = Image.new("RGBA", (total_size, total_size), (0, 0, 0, 0))
    result = Image.alpha_composite(result, shadow)
    result.paste(icon_rgba, (padding, padding), icon_rgba)

    return result


def _draw_dashed_bezier(draw, p0, p1, color, width, wobble=2.5):
    """Draw a hand-drawn dashed Bezier curve between two points.

    Creates a quadratic Bezier with a perpendicular offset control point
    and adds slight random jitter for a hand-drawn feel.
    """
    # Compute perpendicular control point
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    length = math.sqrt(dx * dx + dy * dy)
    if length < 1:
        return mx, my

    # Perpendicular offset (15% of length)
    offset = length * 0.15
    nx, ny = -dy / length, dx / length
    # Alternate side based on hash of coordinates for variety
    side = 1 if (int(p0[0] + p0[1]) % 2 == 0) else -1
    cx = mx + nx * offset * side
    cy = my + ny * offset * side

    # Generate Bezier points
    num_points = max(int(length / 3), 20)
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        # Quadratic Bezier: B(t) = (1-t)^2 * P0 + 2(1-t)t * C + t^2 * P1
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * cx + t ** 2 * p1[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * cy + t ** 2 * p1[1]
        # Add hand-drawn wobble
        if 0.05 < t < 0.95:
            x += random.uniform(-wobble, wobble)
            y += random.uniform(-wobble, wobble)
        points.append((x, y))

    # Draw as dashed segments
    dash_counter = 0
    drawing = True
    for i in range(len(points) - 1):
        if drawing:
            draw.line(
                [points[i], points[i + 1]],
                fill=color,
                width=width,
            )
        dash_counter += 1
        segment_len = math.sqrt(
            (points[i + 1][0] - points[i][0]) ** 2 +
            (points[i + 1][1] - points[i][1]) ** 2
        )
        if drawing and dash_counter * segment_len > DASH_ON:
            drawing = False
            dash_counter = 0
        elif not drawing and dash_counter * segment_len > DASH_OFF:
            drawing = True
            dash_counter = 0

    # Return midpoint for badge placement
    t_mid = 0.5
    mid_x = (1 - t_mid) ** 2 * p0[0] + 2 * (1 - t_mid) * t_mid * cx + t_mid ** 2 * p1[0]
    mid_y = (1 - t_mid) ** 2 * p0[1] + 2 * (1 - t_mid) * t_mid * cy + t_mid ** 2 * p1[1]
    return mid_x, mid_y


def _draw_number_badge(draw, x, y, number, font):
    """Draw a small numbered circle badge at the given position."""
    r = BADGE_SIZE // 2
    draw.ellipse(
        [x - r, y - r, x + r, y + r],
        fill=BADGE_FILL,
        outline=BADGE_BORDER,
        width=2,
    )
    text = str(number)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(
        (x - tw // 2, y - th // 2 - 1),
        text,
        fill=BADGE_BORDER,
        font=font,
    )


def _draw_label(img, x, y, text, icon_size, font):
    """Draw a POI name label below the icon with a semi-transparent background pill."""
    draw = ImageDraw.Draw(img, "RGBA")
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    label_x = x - tw // 2
    label_y = y + icon_size // 2 + 8  # Below the icon

    # Background pill
    pill_rect = [
        label_x - LABEL_PADDING,
        label_y - LABEL_PADDING // 2,
        label_x + tw + LABEL_PADDING,
        label_y + th + LABEL_PADDING // 2,
    ]
    draw.rounded_rectangle(pill_rect, radius=8, fill=LABEL_BG)
    draw.text((label_x, label_y), text, fill=LABEL_TEXT, font=font)


def _draw_title_banner(img, city_name, font):
    """Draw a decorative city name title banner at the top-center."""
    draw = ImageDraw.Draw(img, "RGBA")
    bbox = font.getbbox(city_name)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    cx = img.width // 2
    banner_padding_x = 30
    banner_padding_y = 12

    banner_rect = [
        cx - tw // 2 - banner_padding_x,
        15,
        cx + tw // 2 + banner_padding_x,
        15 + th + banner_padding_y * 2,
    ]
    draw.rounded_rectangle(banner_rect, radius=12, fill=TITLE_BG)

    # Draw decorative lines on sides
    line_y = 15 + (th + banner_padding_y * 2) // 2
    draw.line(
        [banner_rect[0] - 40, line_y, banner_rect[0] - 5, line_y],
        fill=BADGE_BORDER + (150,),
        width=2,
    )
    draw.line(
        [banner_rect[2] + 5, line_y, banner_rect[2] + 40, line_y],
        fill=BADGE_BORDER + (150,),
        width=2,
    )

    draw.text(
        (cx - tw // 2, 15 + banner_padding_y),
        city_name,
        fill=TITLE_TEXT,
        font=font,
    )


def _draw_compass_rose(img, position="bottom-right", size=60):
    """Draw a simple compass rose in the specified corner."""
    draw = ImageDraw.Draw(img, "RGBA")
    margin = 25

    if position == "bottom-right":
        cx = img.width - margin - size // 2
        cy = img.height - margin - size // 2
    elif position == "bottom-left":
        cx = margin + size // 2
        cy = img.height - margin - size // 2
    elif position == "top-right":
        cx = img.width - margin - size // 2
        cy = margin + size // 2
    else:
        cx = margin + size // 2
        cy = margin + size // 2

    r = size // 2
    color = BADGE_BORDER + (180,)

    # Draw circle background
    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        fill=(255, 248, 231, 160),
        outline=color,
        width=2,
    )

    # Draw N-S-E-W lines
    inner_r = r - 8
    # N
    draw.line([(cx, cy), (cx, cy - inner_r)], fill=color, width=2)
    # S
    draw.line([(cx, cy), (cx, cy + inner_r)], fill=(139, 115, 85, 100), width=1)
    # E
    draw.line([(cx, cy), (cx + inner_r, cy)], fill=(139, 115, 85, 100), width=1)
    # W
    draw.line([(cx, cy), (cx - inner_r, cy)], fill=(139, 115, 85, 100), width=1)

    # N arrow head (filled triangle)
    arrow_size = 6
    draw.polygon(
        [
            (cx, cy - inner_r),
            (cx - arrow_size, cy - inner_r + arrow_size * 2),
            (cx + arrow_size, cy - inner_r + arrow_size * 2),
        ],
        fill=color,
    )

    # "N" label
    small_font = _get_font(11, bold=True)
    draw.text((cx - 3, cy - inner_r - 14), "N", fill=color, font=small_font)


# ---------------------------------------------------------------------------
# Main compositing function
# ---------------------------------------------------------------------------

def composite(map_path, config_path, output_path):
    """Assemble the final travel itinerary map.

    Args:
        map_path: Path to the stylized map background PNG.
        config_path: Path to the JSON configuration file.
        output_path: Path for the final composite PNG output.

    Raises:
        FileNotFoundError: If map or config file doesn't exist.
        ValueError: If config is missing required fields.
    """
    # Validate inputs
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Map file not found: {map_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    # Load configuration
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")

    # Validate required fields
    required_fields = ["viewport", "pois", "city_name"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Config missing required field: {field}")

    viewport_fields = ["center_lat", "center_lng", "zoom", "width", "height"]
    for field in viewport_fields:
        if field not in config["viewport"]:
            raise ValueError(f"Viewport missing required field: {field}")

    viewport = config["viewport"]
    pois = config["pois"]
    city_name = config.get("city_name", "Travel Map")

    center_lat = viewport["center_lat"]
    center_lng = viewport["center_lng"]
    zoom = viewport["zoom"]
    map_width = viewport["width"]
    map_height = viewport["height"]

    print(f"Loading map background: {map_path}")
    try:
        map_img = Image.open(map_path).convert("RGBA")
    except Exception as e:
        raise ValueError(f"Failed to load map image: {e}")
    # Ensure map matches expected dimensions
    if map_img.size != (map_width, map_height):
        map_img = map_img.resize((map_width, map_height), Image.LANCZOS)

    # Compute icon size
    num_pois = len(pois)
    icon_size = compute_icon_size(num_pois, map_width, map_height)
    print(f"Adaptive icon size: {icon_size}px for {num_pois} POIs")

    # Convert coordinates to pixel positions
    pixel_positions = []
    for poi in pois:
        px, py = latlng_to_pixel(
            poi["lat"], poi["lng"],
            center_lat, center_lng,
            zoom, map_width, map_height,
        )
        pixel_positions.append((px, py))

    # Determine route order
    explicit_order = all(poi.get("order") is not None for poi in pois)
    if explicit_order:
        route_order = sorted(range(num_pois), key=lambda i: pois[i]["order"])
    else:
        route_order = nearest_neighbor_route(pois)

    print(f"Route order: {[pois[i]['name'] for i in route_order]}")

    # Resolve overlaps
    original_positions = list(pixel_positions)
    adjusted_positions = resolve_overlaps(pixel_positions, icon_size)

    # Load fonts
    label_font = _get_font(max(14, icon_size // 8))
    title_font = _get_font(max(24, min(40, map_width // 30)), bold=True)
    badge_font = _get_font(max(12, BADGE_SIZE - 8), bold=True)

    # --- Start compositing ---
    canvas = map_img.copy()

    # 1. Draw route lines
    print("Drawing route lines...")
    route_draw = ImageDraw.Draw(canvas, "RGBA")
    route_midpoints = []
    for step in range(len(route_order) - 1):
        i = route_order[step]
        j = route_order[step + 1]
        p0 = adjusted_positions[i]
        p1 = adjusted_positions[j]

        random.seed(i * 1000 + j)  # deterministic wobble
        mid = _draw_dashed_bezier(
            route_draw, p0, p1,
            color=ROUTE_COLOR + (200,),
            width=ROUTE_WIDTH,
        )
        route_midpoints.append((mid, step + 1))

    # 2. Draw connector lines for nudged icons
    for i in range(num_pois):
        orig = original_positions[i]
        adj = adjusted_positions[i]
        dist = math.sqrt((orig[0] - adj[0]) ** 2 + (orig[1] - adj[1]) ** 2)
        if dist > 5:
            route_draw.line(
                [adj, orig],
                fill=(139, 115, 85, 100),
                width=1,
            )
            route_draw.ellipse(
                [orig[0] - 3, orig[1] - 3, orig[0] + 3, orig[1] + 3],
                fill=(139, 115, 85, 120),
            )

    # 3. Place POI icons
    print("Placing POI icons...")
    for i in range(num_pois):
        poi = pois[i]
        icon_path = poi.get("icon_path", "")

        if icon_path and os.path.exists(icon_path):
            icon_img = Image.open(icon_path).convert("RGBA")
        else:
            # Fallback: create a colored placeholder circle
            print(f"  Warning: Icon not found for {poi['name']}, using placeholder")
            icon_img = Image.new("RGBA", (256, 256), (200, 180, 160, 255))
            placeholder_draw = ImageDraw.Draw(icon_img)
            placeholder_draw.ellipse([10, 10, 245, 245], fill=(180, 160, 140, 255))

        circular_icon = _create_circular_icon(icon_img, icon_size)
        px, py = adjusted_positions[i]

        # Center the icon on the position
        paste_x = px - circular_icon.width // 2
        paste_y = py - circular_icon.height // 2

        canvas.paste(circular_icon, (paste_x, paste_y), circular_icon)

    # 4. Draw route number badges
    print("Drawing route badges...")
    badge_draw = ImageDraw.Draw(canvas, "RGBA")
    for (mx, my), num in route_midpoints:
        _draw_number_badge(badge_draw, int(mx), int(my), num, badge_font)

    # Also draw start/end badges on the first and last POI
    first_pos = adjusted_positions[route_order[0]]
    _draw_number_badge(
        badge_draw,
        first_pos[0] + icon_size // 2 - 5,
        first_pos[1] - icon_size // 2 + 5,
        1,
        badge_font,
    )

    # 5. Draw POI labels
    print("Drawing POI labels...")
    for i in range(num_pois):
        px, py = adjusted_positions[i]
        # Find the route number for this POI
        route_num = route_order.index(i) + 1
        label_text = f"{route_num}. {pois[i]['name']}"
        _draw_label(canvas, px, py, label_text, icon_size, label_font)

    # 6. Draw title banner
    print("Drawing title banner...")
    _draw_title_banner(canvas, city_name, title_font)

    # 7. Draw compass rose
    _draw_compass_rose(canvas, position="bottom-right", size=50)

    # Save final output
    final_rgb = canvas.convert("RGB")
    final_rgb.save(output_path, "PNG", quality=95)
    print(f"\nFinal map saved to: {output_path}")
    print(f"  Dimensions: {map_width}x{map_height}")
    print(f"  POIs: {num_pois}")
    print(f"  Route: {' → '.join(pois[i]['name'] for i in route_order)}")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Composite the final illustrated travel itinerary map"
    )
    parser.add_argument("--map", required=True, help="Stylized map background PNG")
    parser.add_argument("--config", required=True, help="JSON config with viewport and POI data")
    parser.add_argument("--output", required=True, help="Output final map PNG path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    try:
        result = composite(args.map, args.config, args.output)
        print(f"\n✓ Map saved to: {result}")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
