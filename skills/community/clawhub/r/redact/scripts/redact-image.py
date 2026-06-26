#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPStructureV3 Image Redaction Tool

Usage:
  redact-image.py <image> <rules.csv> <output>     # Redact image with privacy rules
  redact-image.py --debug <image> [output_dir]     # Debug mode: output JSON and render
  redact-image.py --help                           # Show help

Rules CSV format:
  target_text,replacement_text    # Replace with new text (sample background color)
  target_text,                    # Empty replacement = cover with solid color block
"""

import argparse
import csv
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, Sequence, Tuple

os.environ.setdefault("DISABLE_MODEL_SOURCE_CHECK", "True")
os.environ.setdefault("FLAGS_use_mkldnn", "0")

from PIL import Image, ImageDraw, ImageFont
from paddleocr import PPStructureV3
import paddle

# PPStructureV3 result keys
TEXT_KEYS = ("rec_text", "text", "ocr_text", "transcription", "label", "content", "markdown", "block_content")
BOX_KEYS = ("text_region", "text_box", "dt_polys", "poly", "bbox", "box", "points", "position", "region", "block_bbox", "coordinate")

# Debug colors for different region types
REGION_COLORS = {
    "ocr": (255, 0, 0),
    "table": (0, 255, 0),
    "table_cell": (0, 128, 255),
    "title": (255, 0, 255),
    "figure_title": (255, 0, 255),
    "figure": (0, 255, 255),
    "header": (255, 255, 0),
    "footer": (255, 128, 0),
    "number": (128, 128, 255),
    "redacted": (50, 50, 50),
    "unknown": (128, 128, 128),
}

# Default cover color (dark gray)
DEFAULT_COVER_COLOR = (50, 50, 50)


@dataclass
class TextRegion:
    """Represents a detected text region."""
    text: str
    polygon: List[Tuple[float, float]]
    region_type: str = "ocr"
    confidence: float = 1.0


@dataclass
class ReplacementRule:
    """Represents a replacement rule."""
    target: str
    replacement: Optional[str]  # None = cover with solid color


@dataclass
class TextMatch:
    """Represents a matched text position within a region."""
    region: TextRegion
    target: str
    start_idx: int
    end_idx: int
    rule: ReplacementRule


def eprint(*args: Any) -> None:
    """Print to stderr."""
    print(*args, file=sys.stderr)


def get_pipeline() -> PPStructureV3:
    """Initialize PPStructureV3 pipeline."""
    device = "gpu" if paddle.is_compiled_with_cuda() else "cpu"
    eprint(f"Initializing PPStructureV3 on {device}...")
    return PPStructureV3(device=device, use_doc_unwarping=False)


def run_pipeline(pipeline: PPStructureV3, image_path: Path) -> List[Any]:
    """Run PPStructureV3 and export results as JSON."""
    temp_dir = Path(tempfile.mkdtemp(prefix="ppstructure_"))
    results: List[Any] = []
    
    eprint(f"Processing: {image_path}")
    predictions = pipeline.predict(input=str(image_path))
    
    for idx, pred in enumerate(predictions):
        pred_dir = temp_dir / f"res_{idx}"
        pred_dir.mkdir(parents=True, exist_ok=True)
        pred.save_to_json(str(pred_dir))
        
        for json_file in sorted(pred_dir.glob("*_res.json")):
            with json_file.open("r", encoding="utf-8") as f:
                results.append(json.load(f))
    
    return results


def normalize_polygon(value: Any) -> Optional[List[Tuple[float, float]]]:
    """Convert various box formats to polygon (list of 4 points)."""
    if value is None:
        return None
    
    if isinstance(value, dict):
        for key in BOX_KEYS:
            if key in value:
                result = normalize_polygon(value[key])
                if result:
                    return result
        return None
    
    if not isinstance(value, (list, tuple)):
        return None
    
    # [x1, y1, x2, y2] format
    if len(value) == 4 and all(isinstance(v, (int, float)) for v in value):
        x1, y1, x2, y2 = value
        return [(float(x1), float(y1)), (float(x2), float(y1)), 
                (float(x2), float(y2)), (float(x1), float(y2))]
    
    # [[x, y], [x, y], ...] format
    if value and all(
        isinstance(p, (list, tuple)) and len(p) >= 2 and 
        all(isinstance(v, (int, float)) for v in p[:2])
        for p in value
    ):
        return [(float(p[0]), float(p[1])) for p in value]
    
    return None


def extract_text(value: Any) -> Optional[str]:
    """Extract text string from various formats."""
    if isinstance(value, str):
        text = value.strip()
        return text or None
    
    if isinstance(value, dict):
        for key in TEXT_KEYS:
            if key in value:
                result = extract_text(value[key])
                if result:
                    return result
        for nested in value.values():
            result = extract_text(nested)
            if result:
                return result
        return None
    
    if isinstance(value, list):
        parts: List[str] = []
        for item in value:
            result = extract_text(item)
            if result:
                parts.append(result)
        return " ".join(parts) if parts else None
    
    return None


def collect_regions(data: Any) -> List[TextRegion]:
    """Extract all text regions from PPStructureV3 result."""
    regions: List[TextRegion] = []
    seen: set = set()
    
    def add_region(text: Optional[str], polygon: Optional[List[Tuple[float, float]]], 
                   region_type: str = "ocr", confidence: float = 1.0) -> None:
        if not text or not polygon:
            return
        key = (text, tuple(polygon))
        if key in seen:
            return
        seen.add(key)
        regions.append(TextRegion(text=text, polygon=polygon, region_type=region_type, confidence=confidence))
    
    def walk(node: Any, default_type: str = "unknown") -> None:
        if isinstance(node, dict):
            # Handle parsing_res_list (block results)
            if "block_label" in node and "block_content" in node:
                text = node.get("block_content")
                bbox = node.get("block_bbox")
                label = node.get("block_label", default_type)
                # Skip table HTML content
                if label != "table" or not text.startswith("<"):
                    add_region(extract_text(text), normalize_polygon(bbox), label)
            
            # Handle layout_det_res boxes
            if "label" in node and "coordinate" in node:
                text = node.get("label")
                coord = node.get("coordinate")
                score = node.get("score", 1.0)
                add_region(text, normalize_polygon(coord), text, score)
            
            # Handle overall_ocr_res / OCR results
            dt_polys = node.get("dt_polys")
            rec_texts = node.get("rec_texts")
            if dt_polys and rec_texts:
                for poly, text in zip(dt_polys, rec_texts):
                    add_region(extract_text(text), normalize_polygon(poly), "ocr")
            
            # Handle single OCR result
            if "rec_text" in node or "text" in node:
                text = extract_text(node)
                box = None
                for key in BOX_KEYS:
                    if key in node:
                        box = normalize_polygon(node[key])
                        if box:
                            break
                rtype = node.get("type", node.get("block_label", "ocr"))
                add_region(text, box, rtype)
            
            # Handle table cells
            if "cells" in node:
                for cell in node["cells"]:
                    walk(cell, "table_cell")
            
            # Recurse into nested structures
            for key, value in node.items():
                if key in ("dt_polys", "rec_texts", "boxes"):
                    continue
                if isinstance(value, (dict, list)):
                    walk(value, default_type)
        
        elif isinstance(node, list):
            for item in node:
                walk(item, default_type)
    
    walk(data)
    return regions


def load_rules(csv_path: Path) -> List[ReplacementRule]:
    """Load replacement rules from CSV file."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    rules: List[ReplacementRule] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            target = row[0].strip() if row[0] else ""
            if not target:
                continue
            
            if len(row) >= 2 and row[1]:
                replacement = row[1].strip()
            else:
                replacement = None
            
            rules.append(ReplacementRule(target=target, replacement=replacement))
    
    if not rules:
        raise ValueError(f"No valid replacement rules found in: {csv_path}")
    
    return rules


def find_matches(regions: List[TextRegion], rules: Sequence[ReplacementRule]) -> List[TextMatch]:
    """Find all text matches in regions."""
    matches: List[TextMatch] = []
    
    for region in regions:
        for rule in rules:
            # Find all occurrences of target in text
            start = 0
            while True:
                idx = region.text.find(rule.target, start)
                if idx == -1:
                    break
                matches.append(TextMatch(
                    region=region,
                    target=rule.target,
                    start_idx=idx,
                    end_idx=idx + len(rule.target),
                    rule=rule
                ))
                start = idx + 1
    
    return matches


def polygon_bounds(polygon: Sequence[Tuple[float, float]]) -> Tuple[int, int, int, int]:
    """Get bounding box of polygon."""
    xs = [p[0] for p in polygon]
    ys = [p[1] for p in polygon]
    return int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))


def get_text_width(text: str, font: ImageFont.ImageFont, draw: ImageDraw.ImageDraw) -> int:
    """Get text width in pixels."""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def calculate_sub_region(region: TextRegion, start_idx: int, end_idx: int,
                         font: ImageFont.ImageFont, draw: ImageDraw.ImageDraw) -> List[Tuple[float, float]]:
    """
    Calculate the polygon for a substring within a text region.
    Uses character position to estimate horizontal position.
    """
    x1, y1, x2, y2 = polygon_bounds(region.polygon)
    total_width = x2 - x1
    
    # Calculate character widths
    full_text = region.text
    full_width = get_text_width(full_text, font, draw)
    
    # Calculate prefix and target widths
    prefix_text = full_text[:start_idx]
    target_text = full_text[start_idx:end_idx]
    
    prefix_width = get_text_width(prefix_text, font, draw) if prefix_text else 0
    target_width = get_text_width(target_text, font, draw)
    
    # Scale to actual region width
    scale = total_width / full_width if full_width > 0 else 1
    
    # Calculate x positions
    start_x = x1 + prefix_width * scale
    end_x = x1 + (prefix_width + target_width) * scale
    
    # Add small padding
    padding = 1
    start_x = max(x1, start_x - padding)
    end_x = min(x2, end_x + padding)
    
    # Create sub-polygon (same y coordinates, different x)
    return [
        (start_x, float(y1)),
        (end_x, float(y1)),
        (end_x, float(y2)),
        (start_x, float(y2))
    ]


def sample_background_color(image: Image.Image, polygon: Sequence[Tuple[float, float]]) -> Tuple[int, int, int]:
    """Sample background color from the region corners and edges."""
    x1, y1, x2, y2 = polygon_bounds(polygon)
    width, height = x2 - x1, y2 - y1
    
    sample_points = []
    margin = max(2, min(width, height) // 10)
    
    # Sample from corners
    for dx, dy in [(margin, margin), (width - margin, margin), 
                   (margin, height - margin), (width - margin, height - margin)]:
        sample_points.append((x1 + dx, y1 + dy))
    
    # Sample from edges
    if width > 20:
        sample_points.append((x1 + width // 2, y1 + margin))
        sample_points.append((x1 + width // 2, y2 - margin))
    if height > 20:
        sample_points.append((x1 + margin, y1 + height // 2))
        sample_points.append((x2 - margin, y1 + height // 2))
    
    pixels = image.load()
    colors = []
    img_width, img_height = image.size
    
    for px, py in sample_points:
        if 0 <= px < img_width and 0 <= py < img_height:
            pixel = pixels[px, py]
            colors.append(pixel[:3] if isinstance(pixel, (list, tuple)) and len(pixel) >= 3 else pixel)
    
    if not colors:
        return (255, 255, 255)
    
    r = sorted(c[0] for c in colors)[len(colors) // 2]
    g = sorted(c[1] for c in colors)[len(colors) // 2]
    b = sorted(c[2] for c in colors)[len(colors) // 2]
    return (r, g, b)


def resolve_font(font_size: int) -> ImageFont.ImageFont:
    """Find a suitable font for rendering across platforms."""
    candidates = [
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        # Windows
        r"C:\\Windows\\Fonts\\msyh.ttc",
        r"C:\\Windows\\Fonts\\msyhbd.ttc",
        r"C:\\Windows\\Fonts\\simhei.ttf",
        r"C:\\Windows\\Fonts\\simsun.ttc",
        r"C:\\Windows\\Fonts\\arialuni.ttf",
        # Linux
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, max(10, font_size))
            except Exception:
                continue
    return ImageFont.load_default()


def estimate_font_size(region: TextRegion) -> int:
    """Estimate font size based on region height."""
    _, y1, _, y2 = polygon_bounds(region.polygon)
    height = y2 - y1
    # Estimate font size as ~80% of region height
    return max(10, int(height * 0.8))


def cover_sub_region(draw: ImageDraw.ImageDraw, polygon: Sequence[Tuple[float, float]], 
                     color: Tuple[int, int, int] = DEFAULT_COVER_COLOR) -> None:
    """Cover a sub-region with solid color block."""
    points = [(int(x), int(y)) for x, y in polygon]
    draw.polygon(points, fill=color)


def replace_text_in_sub_region(image: Image.Image, region: TextRegion, 
                               sub_polygon: List[Tuple[float, float]],
                               new_text: str, font: ImageFont.ImageFont) -> Image.Image:
    """Replace text in a sub-region with new text."""
    x1, y1, x2, y2 = polygon_bounds(sub_polygon)
    width, height = x2 - x1, y2 - y1
    
    # Sample background color from the sub-region
    bg_color = sample_background_color(image, sub_polygon)
    
    draw = ImageDraw.Draw(image)
    
    # Fill sub-region with background color
    points = [(int(x), int(y)) for x, y in sub_polygon]
    draw.polygon(points, fill=bg_color)
    
    # Adjust font size to fit the sub-region width
    test_font = font
    font_size = estimate_font_size(region)
    while font_size >= 10:
        test_font = resolve_font(font_size)
        text_width = get_text_width(new_text, test_font, draw)
        if text_width <= width - 2:
            break
        font_size -= 1
    
    # Get text dimensions
    text_width = get_text_width(new_text, test_font, draw)
    bbox = draw.textbbox((0, 0), new_text, font=test_font)
    text_height = bbox[3] - bbox[1]
    
    # Center text in sub-region
    text_x = x1 + max(0, (width - text_width) // 2)
    text_y = y1 + max(0, (height - text_height) // 2)
    
    # Determine text color based on background brightness
    brightness = (bg_color[0] * 299 + bg_color[1] * 587 + bg_color[2] * 114) / 1000
    text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)
    
    draw.text((text_x, text_y), new_text, fill=text_color, font=test_font)
    
    return image


def render_debug(image_path: Path, regions: List[TextRegion], output_path: Path,
                 matches: Optional[List[TextMatch]] = None) -> None:
    """Render debug visualization with colored boxes and labels."""
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    
    # Draw all regions
    for region in regions:
        color = REGION_COLORS.get(region.region_type, REGION_COLORS["unknown"])
        points = [(int(x), int(y)) for x, y in region.polygon]
        draw.polygon(points, outline=color, width=1)
    
    # Draw matched sub-regions with highlight
    if matches:
        for match in matches:
            font_size = estimate_font_size(match.region)
            font = resolve_font(font_size)
            sub_poly = calculate_sub_region(match.region, match.start_idx, match.end_idx, font, draw)
            points = [(int(x), int(y)) for x, y in sub_poly]
            # Draw with thicker red outline
            draw.polygon(points, outline=(255, 0, 0), width=2)
            
            # Draw label
            x1, y1 = min(p[0] for p in sub_poly), min(p[1] for p in sub_poly)
            label_font = resolve_font(12)
            label = f"'{match.target}'"
            bbox = draw.textbbox((x1, y1 - 16), label, font=label_font)
            draw.rectangle(bbox, fill=(255, 0, 0))
            draw.text((x1, y1 - 16), label, fill="white", font=label_font)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    eprint(f"Debug image saved: {output_path}")


def save_json(data: Any, path: Path, description: str = "JSON") -> None:
    """Save data as JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    eprint(f"{description} saved: {path}")


def cmd_debug(args: argparse.Namespace) -> int:
    """Debug mode: output JSON and render debug image."""
    image_path = Path(args.image).expanduser().resolve()
    if not image_path.exists():
        eprint(f"Image not found: {image_path}")
        return 1
    
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else image_path.parent
    
    pipeline = get_pipeline()
    results = run_pipeline(pipeline, image_path)
    
    # Save full JSON
    json_path = output_dir / f"{image_path.stem}_ppstructure.json"
    save_json(results, json_path, "Full JSON")
    
    # Extract and save regions
    regions = collect_regions(results)
    regions = [r for r in regions if r.region_type == "ocr" and r.text]  # Filter to OCR regions with text
    regions_data = [
        {
            "text": r.text, 
            "polygon": r.polygon, 
            "bbox": list(polygon_bounds(r.polygon)),
            "type": r.region_type, 
            "confidence": r.confidence
        }
        for r in regions
    ]
    regions_path = output_dir / f"{image_path.stem}_regions.json"
    save_json(regions_data, regions_path, "Regions JSON")
    
    # Render debug image
    debug_path = output_dir / f"{image_path.stem}_debug.png"
    render_debug(image_path, regions, debug_path)
    
    # Print summary
    print("\n" + "=" * 60)
    print("PPStructureV3 Debug Results")
    print("=" * 60)
    print(f"Image: {image_path}")
    print(f"Total regions: {len(regions)}")
    print(f"\nOutput files:")
    print(f"  - Full JSON: {json_path}")
    print(f"  - Regions JSON: {regions_path}")
    print(f"  - Debug image: {debug_path}")
    print("\n" + "-" * 60)
    print("Detected Regions:")
    print("-" * 60)
    for i, r in enumerate(regions, 1):
        bbox = polygon_bounds(r.polygon)
        print(f"{i:3d}. [{r.region_type:12s}] bbox={bbox} | {r.text[:40]}{'...' if len(r.text) > 40 else ''}")
    
    return 0


def cmd_redact(args: argparse.Namespace) -> int:
    """Redact mode: apply privacy rules to image."""
    image_path = Path(args.image).expanduser().resolve()
    rules_path = Path(args.rules).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    
    if not image_path.exists():
        eprint(f"Image not found: {image_path}")
        return 1
    
    rules = load_rules(rules_path)
    pipeline = get_pipeline()
    
    results = run_pipeline(pipeline, image_path)
    regions = collect_regions(results)
    regions = [r for r in regions if r.region_type == "ocr" and r.text]
    # Find all matches
    matches = find_matches(regions, rules)
    
    if not matches:
        eprint("No matching privacy text found.")
        image = Image.open(image_path).convert("RGB")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)
        print(str(output_path))
        return 0
    
    # Load image
    image = Image.open(image_path).convert("RGB")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Process each match
    for match in matches:
        region = match.region
        rule = match.rule
        
        # Estimate font size for this region
        font_size = estimate_font_size(region)
        font = resolve_font(font_size)
        
        # Calculate sub-region polygon for the matched text
        sub_polygon = calculate_sub_region(region, match.start_idx, match.end_idx, font, ImageDraw.Draw(image))
        
        if rule.replacement is None:
            # Cover with solid color
            eprint(f"Covering: '{match.target}' in '{region.text}'")
            draw = ImageDraw.Draw(image)
            cover_sub_region(draw, sub_polygon)
        else:
            # Replace text
            eprint(f"Replacing: '{match.target}' -> '{rule.replacement}' in '{region.text}'")
            image = replace_text_in_sub_region(image, region, sub_polygon, rule.replacement, font)
    
    image.save(output_path)
    print(str(output_path))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="PPStructureV3 Image Redaction Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Debug mode - analyze image and output JSON + debug visualization
  %(prog)s --debug image.png
  %(prog)s --debug image.png ./output_dir

  # Redact mode - apply privacy replacement rules
  %(prog)s image.png rules.csv output.png

Rules CSV format:
  target_text,new_text      # Replace with new text (sample background color)
  target_text,              # Empty = cover with solid color block
"""
    )
    
    parser.add_argument("--debug", action="store_true", help="Debug mode: output JSON and render debug image")
    parser.add_argument("image", help="Input image path (required)")
    parser.add_argument("rules_csv", nargs="?", help="Rules CSV file (required for redact mode)")
    parser.add_argument("output_path", nargs="?", help="Output image path (required for redact mode)")
    
    args = parser.parse_args()
    
    # Debug mode: image is required, output_dir is optional
    if args.debug:
        args.output_dir = args.rules_csv
        return cmd_debug(args)
    
    # Redact mode: all three arguments are required
    missing = []
    if not args.rules_csv:
        missing.append("rules_csv (CSV file with replacement rules)")
    if not args.output_path:
        missing.append("output_path (output image path)")
    
    if missing:
        parser.error(f"Redact mode requires missing arguments:\n  - " + "\n  - ".join(missing) + 
                    f"\n\nUsage: %(prog)s image.png rules.csv output.png")
    
    args.rules = args.rules_csv
    args.output = args.output_path
    return cmd_redact(args)


if __name__ == "__main__":
    raise SystemExit(main())
