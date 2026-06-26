#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPStructureV3 PDF Redaction Tool

Usage:
  redact-pdf.py <pdf> <rules.csv> <output>     # Redact PDF with privacy rules
  redact-pdf.py --debug <pdf> [output_dir]     # Debug mode: output JSON and render
  redact-pdf.py --help                         # Show help

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
from typing import Any, Dict, List, Optional, Sequence, Tuple

os.environ.setdefault("DISABLE_MODEL_SOURCE_CHECK", "True")
os.environ.setdefault("FLAGS_use_mkldnn", "0")

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
from paddleocr import PPStructureV3
import paddle

# Reuse constants from redact-image
TEXT_KEYS = ("rec_text", "text", "ocr_text", "transcription", "label", "content", "markdown", "block_content")
BOX_KEYS = ("text_region", "text_box", "dt_polys", "poly", "bbox", "box", "points", "position", "region", "block_bbox", "coordinate")

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

DEFAULT_COVER_COLOR = (50, 50, 50)

# Threshold for determining if a page is image-based
IMAGE_PAGE_TEXT_THRESHOLD = 50  # If less than this many chars, treat as image page


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


@dataclass
class PDFTextSpan:
    """Represents a text span in PDF with position."""
    text: str
    bbox: Tuple[float, float, float, float]  # (x0, y0, x1, y1)
    page_num: int
    font_size: float


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
    """Calculate the polygon for a substring within a text region."""
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
    
    # Create sub-polygon
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
    return max(10, int(height * 0.8))


def cover_sub_region(draw: ImageDraw.ImageDraw, polygon: Sequence[Tuple[float, float]], 
                     color: Tuple[int, int, int] = DEFAULT_COVER_COLOR,
                     debug: bool = False, label: str = "", font: Optional[ImageFont.ImageFont] = None) -> None:
    """Cover a sub-region with solid color block, or transparent + border + label in debug mode."""
    points = [(int(x), int(y)) for x, y in polygon]
    
    if debug:
        # Debug mode: transparent fill + red border + label text
        draw.polygon(points, outline=(255, 0, 0), width=2)
        
        if label and font:
            x1, y1, x2, y2 = polygon_bounds(polygon)
            width, height = x2 - x1, y2 - y1
            
            # Get text dimensions
            text_bbox = draw.textbbox((0, 0), label, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Center text in the region
            text_x = x1 + max(0, (width - text_width) // 2)
            text_y = y1 + max(0, (height - text_height) // 2)
            
            # Draw text with red color
            draw.text((text_x, text_y), label, fill=(255, 0, 0), font=font)
    else:
        # Normal mode: solid color block
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


# ============== PDF-specific functions ==============

def extract_pdf_text_spans(page: fitz.Page) -> List[PDFTextSpan]:
    """Extract all text spans with positions from a PDF page."""
    spans: List[PDFTextSpan] = []
    
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                text = span.get("text", "").strip()
                if not text:
                    continue
                bbox = span.get("bbox", (0, 0, 0, 0))
                font_size = span.get("size", 12)
                spans.append(PDFTextSpan(
                    text=text,
                    bbox=bbox,
                    page_num=page.number,
                    font_size=font_size
                ))
    
    return spans


def is_image_page(page: fitz.Page) -> bool:
    """Determine if a page is primarily image-based (scanned)."""
    text = page.get_text().strip()
    if len(text) < IMAGE_PAGE_TEXT_THRESHOLD:
        return True
    
    # Check for images on the page
    images = page.get_images()
    if images and len(text) < 200:
        return True
    
    return False


def page_to_image(page: fitz.Page, dpi: int = 150) -> Image.Image:
    """Render PDF page to PIL Image."""
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    
    from io import BytesIO
    return Image.open(BytesIO(img_data)).convert("RGB")


def find_pdf_text_matches(spans: List[PDFTextSpan], rules: Sequence[ReplacementRule]) -> List[Tuple[PDFTextSpan, ReplacementRule, int, int]]:
    """Find text matches in PDF text spans."""
    matches: List[Tuple[PDFTextSpan, ReplacementRule, int, int]] = []
    
    for span in spans:
        for rule in rules:
            start = 0
            while True:
                idx = span.text.find(rule.target, start)
                if idx == -1:
                    break
                matches.append((span, rule, idx, idx + len(rule.target)))
                start = idx + 1
    
    return matches


def redact_pdf_text_page(page: fitz.Page, spans: List[PDFTextSpan], 
                         rules: Sequence[ReplacementRule], debug: bool = False) -> int:
    """Redact text directly on PDF page. Returns count of redactions."""
    matches = find_pdf_text_matches(spans, rules)
    
    if not matches:
        return 0
    
    count = 0
    for span, rule, start_idx, end_idx in matches:
        target_text = span.text[start_idx:end_idx]
        
        # Calculate the bbox for the matched portion
        # We need to estimate the position of the substring
        x0, y0, x1, y1 = span.bbox
        span_width = x1 - x0
        char_width = span_width / len(span.text) if span.text else 0
        
        # Calculate substring position
        sub_x0 = x0 + start_idx * char_width
        sub_x1 = x0 + end_idx * char_width
        
        # Add small padding
        padding = 1
        sub_x0 = max(x0, sub_x0 - padding)
        sub_x1 = min(x1, sub_x1 + padding)
        
        # Create redaction annotation
        rect = fitz.Rect(sub_x0, y0, sub_x1, y1)
        
        if rule.replacement is None:
            if debug:
                # Debug mode: draw red border rectangle and label
                eprint(f"  Marking (debug): '{target_text}' in '{span.text}'")
                shape = page.new_shape()
                shape.draw_rect(rect)
                shape.finish(color=(1, 0, 0), width=1)  # Red border
                shape.commit()
                
                # Add label text
                font_size = min(span.font_size, (y1 - y0) * 0.8)
                center_x = (sub_x0 + sub_x1) / 2
                center_y = (y0 + y1) / 2
                writer = fitz.TextWriter(page.rect)
                writer.append(
                    (center_x, center_y),
                    target_text,
                    fontsize=font_size * 0.8,
                    fontname="helv"
                )
                writer.write_text(page, color=(1, 0, 0))  # Red text
            else:
                # Cover with solid color
                eprint(f"  Covering: '{target_text}' in '{span.text}'")
                page.add_redact_annot(rect, fill=(0.2, 0.2, 0.2))  # Dark gray
        else:
            # Replace text - we'll add a text box after redaction
            eprint(f"  Replacing: '{target_text}' -> '{rule.replacement}' in '{span.text}'")
            page.add_redact_annot(rect, fill=(1, 1, 1))  # White background
        
        count += 1
    
    # Apply all redactions (only in non-debug mode for cover operations)
    if not debug:
        page.apply_redactions()
    
    # Now add replacement text where needed
    for span, rule, start_idx, end_idx in matches:
        if rule.replacement is not None:
            target_text = span.text[start_idx:end_idx]
            x0, y0, x1, y1 = span.bbox
            span_width = x1 - x0
            char_width = span_width / len(span.text) if span.text else 0
            
            sub_x0 = x0 + start_idx * char_width
            sub_x1 = x0 + end_idx * char_width
            sub_width = sub_x1 - sub_x0
            
            # Calculate center position for replacement text
            center_x = (sub_x0 + sub_x1) / 2
            center_y = (y0 + y1) / 2
            
            # Insert replacement text
            # Use a reasonable font size
            font_size = min(span.font_size, (y1 - y0) * 0.8)
            
            # Create a text writer
            writer = fitz.TextWriter(page.rect)
            writer.append(
                (center_x, center_y),
                rule.replacement,
                fontsize=font_size,
                fontname="helv"
            )
            writer.write_text(page)
    
    return count


def redact_image_page(image: Image.Image, rules: List[ReplacementRule], 
                      pipeline: PPStructureV3, dpi: int = 150, debug: bool = False) -> Image.Image:
    """Redact an image using OCR (same logic as redact-image)."""
    # Save image to temp file for processing
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        image.save(tmp.name, "PNG")
        tmp_path = Path(tmp.name)
    
    try:
        results = run_pipeline(pipeline, tmp_path)
        regions = collect_regions(results)
        regions = [r for r in regions if r.region_type == "ocr" and r.text]
        # Find all matches
        matches = find_matches(regions, rules)
        
        if not matches:
            eprint("  No matching privacy text found.")
            return image
        
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
                # Cover with solid color (or debug mode)
                if debug:
                    eprint(f"  Marking (debug): '{match.target}' in '{region.text}'")
                else:
                    eprint(f"  Covering: '{match.target}' in '{region.text}'")
                draw = ImageDraw.Draw(image)
                cover_sub_region(draw, sub_polygon, debug=debug, label=match.target, font=font)
            else:
                # Replace text
                eprint(f"  Replacing: '{match.target}' -> '{rule.replacement}' in '{region.text}'")
                image = replace_text_in_sub_region(image, region, sub_polygon, rule.replacement, font)
        
        return image
    finally:
        # Clean up temp file
        if tmp_path.exists():
            tmp_path.unlink()


def image_to_pdf_page(image: Image.Image, page_rect: fitz.Rect) -> bytes:
    """Convert PIL Image to PDF page content."""
    from io import BytesIO
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    
    # Create a new PDF with the image
    doc = fitz.open()
    page = doc.new_page(width=page_rect.width, height=page_rect.height)
    
    # Insert the image to fill the page
    page.insert_image(page.rect, stream=img_bytes)
    
    # Get the PDF bytes
    pdf_bytes = doc.tobytes()
    doc.close()
    
    return pdf_bytes


def cmd_debug(args: argparse.Namespace) -> int:
    """Debug mode: analyze PDF and output JSON + debug images."""
    pdf_path = Path(args.pdf).expanduser().resolve()
    if not pdf_path.exists():
        eprint(f"PDF not found: {pdf_path}")
        return 1
    
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else pdf_path.parent
    
    # Open PDF
    doc = fitz.open(str(pdf_path))
    
    all_results: List[Dict[str, Any]] = []
    pipeline = None  # Lazy load
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        eprint(f"\nProcessing page {page_num + 1}/{len(doc)}...")
        
        page_result: Dict[str, Any] = {
            "page_num": page_num + 1,
            "is_image_page": is_image_page(page),
            "text_spans": [],
            "ocr_regions": []
        }
        
        # Extract text spans
        spans = extract_pdf_text_spans(page)
        page_result["text_spans"] = [
            {"text": s.text, "bbox": s.bbox, "font_size": s.font_size}
            for s in spans
        ]
        
        # If image page, also do OCR
        if page_result["is_image_page"]:
            eprint(f"  Page {page_num + 1} detected as image-based, running OCR...")
            if pipeline is None:
                pipeline = get_pipeline()
            
            # Render page to image
            image = page_to_image(page)
            
            # Save temp image for OCR
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                image.save(tmp.name, "PNG")
                tmp_path = Path(tmp.name)
            
            try:
                results = run_pipeline(pipeline, tmp_path)
                regions = collect_regions(results)
                regions = [r for r in regions if r.region_type == "ocr" and r.text]
                page_result["ocr_regions"] = [
                    {
                        "text": r.text,
                        "polygon": r.polygon,
                        "bbox": list(polygon_bounds(r.polygon)),
                        "type": r.region_type,
                        "confidence": r.confidence
                    }
                    for r in regions
                ]
                
                # Render debug image
                debug_path = output_dir / f"{pdf_path.stem}_page{page_num + 1}_debug.png"
                render_debug(tmp_path, regions, debug_path)
                page_result["debug_image"] = str(debug_path)
            finally:
                if tmp_path.exists():
                    tmp_path.unlink()
        
        all_results.append(page_result)
    
    doc.close()
    
    # Save full JSON
    json_path = output_dir / f"{pdf_path.stem}_debug.json"
    save_json(all_results, json_path, "Debug JSON")
    
    # Print summary
    print("\n" + "=" * 60)
    print("PDF Debug Results")
    print("=" * 60)
    print(f"PDF: {pdf_path}")
    print(f"Total pages: {len(all_results)}")
    print(f"\nOutput files:")
    print(f"  - Debug JSON: {json_path}")
    
    for page_result in all_results:
        page_type = "image-based" if page_result["is_image_page"] else "text-based"
        print(f"\n  Page {page_result['page_num']} ({page_type}):")
        print(f"    - Text spans: {len(page_result['text_spans'])}")
        if page_result["is_image_page"]:
            print(f"    - OCR regions: {len(page_result['ocr_regions'])}")
            if "debug_image" in page_result:
                print(f"    - Debug image: {page_result['debug_image']}")
    
    return 0


def cmd_redact(args: argparse.Namespace) -> int:
    """Redact mode: apply privacy rules to PDF."""
    pdf_path = Path(args.pdf).expanduser().resolve()
    rules_path = Path(args.rules).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    debug = getattr(args, 'debug', False)
    
    if not pdf_path.exists():
        eprint(f"PDF not found: {pdf_path}")
        return 1
    
    rules = load_rules(rules_path)
    
    # Open PDF
    doc = fitz.open(str(pdf_path))
    pipeline = None  # Lazy load
    
    total_redactions = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        eprint(f"\nProcessing page {page_num + 1}/{len(doc)}...")
        
        if is_image_page(page):
            # Image-based page: render, OCR, redact, replace
            eprint(f"  Page {page_num + 1} is image-based, using OCR...")
            if pipeline is None:
                pipeline = get_pipeline()
            
            # Render page to image
            image = page_to_image(page)
            
            # Redact the image
            redacted_image = redact_image_page(image, rules, pipeline, debug=debug)
            
            # Create new page with redacted image
            # Get original page dimensions
            page_rect = page.rect
            
            # Convert redacted image back to PDF
            from io import BytesIO
            buffer = BytesIO()
            redacted_image.save(buffer, format="PNG")
            img_bytes = buffer.getvalue()
            
            # Clear the page and insert the redacted image
            # Create a new page with the redacted image
            new_page = doc.new_page(page_num, width=page_rect.width, height=page_rect.height)
            new_page.insert_image(new_page.rect, stream=img_bytes)
            # Delete the old page
            doc.delete_page(page_num + 1)  # +1 because we inserted a new page before
            
        else:
            # Text-based page: direct text replacement
            eprint(f"  Page {page_num + 1} is text-based, using direct text replacement...")
            spans = extract_pdf_text_spans(page)
            count = redact_pdf_text_page(page, spans, rules, debug=debug)
            total_redactions += count
    
    # Save the redacted PDF
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path), garbage=4, deflate=True)
    doc.close()
    
    eprint(f"\nTotal redactions: {total_redactions}")
    print(str(output_path))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="PPStructureV3 PDF Redaction Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Debug mode - analyze PDF and output JSON + debug visualization
  %(prog)s --debug-only document.pdf
  %(prog)s --debug-only document.pdf ./output_dir

  # Redact mode - apply privacy replacement rules
  %(prog)s document.pdf rules.csv output.pdf

  # Redact mode with debug visualization (transparent + border + label)
  %(prog)s --debug document.pdf rules.csv output.pdf

Rules CSV format:
  target_text,new_text      # Replace with new text (sample background color)
  target_text,              # Empty = cover with solid color block (or show label in debug mode)

Page type detection:
  - Text-based pages: Direct text replacement in PDF layer
  - Image-based pages: OCR detection + image redaction (for scanned documents)
"""
    )
    
    parser.add_argument("--debug", action="store_true", help="Debug mode for redaction: show transparent + border + original text label instead of solid color block")
    parser.add_argument("--debug-only", action="store_true", help="Debug-only mode: analyze PDF and output JSON + debug visualization (no redaction)")
    parser.add_argument("pdf", help="Input PDF path (required)")
    parser.add_argument("rules_csv", nargs="?", help="Rules CSV file (required for redact mode)")
    parser.add_argument("output_path", nargs="?", help="Output PDF path (required for redact mode)")
    
    args = parser.parse_args()
    
    # Debug-only mode (analyze only, no redaction)
    if args.debug_only:
        args.output_dir = args.rules_csv
        return cmd_debug(args)
    
    # Redact mode: all three arguments are required
    missing = []
    if not args.rules_csv:
        missing.append("rules_csv (CSV file with replacement rules)")
    if not args.output_path:
        missing.append("output_path (output PDF path)")
    
    if missing:
        parser.error(f"Redact mode requires missing arguments:\n  - " + "\n  - ".join(missing) + 
                    f"\n\nUsage: %(prog)s document.pdf rules.csv output.pdf")
    
    args.rules = args.rules_csv
    args.output = args.output_path
    return cmd_redact(args)


if __name__ == "__main__":
    raise SystemExit(main())
