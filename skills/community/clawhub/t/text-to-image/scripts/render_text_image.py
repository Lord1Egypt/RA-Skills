#!/usr/bin/env python3
import argparse
import base64
import io
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from xml.sax.saxutils import escape

from PIL import Image, ImageColor, ImageDraw, ImageFont


DEFAULT_FONT_FAMILY = "Microsoft YaHei, PingFang SC, Arial, sans-serif"
DEFAULT_COLOR = "#111111"
DEFAULT_BACKGROUND = "transparent"
DEFAULT_PADDING = 24
DEFAULT_LINE_HEIGHT = 1.2
DEFAULT_ALIGN = "center"
DEFAULT_VALIGN = "middle"
DEFAULT_MIN_FONT_SIZE = 12.0
DEFAULT_MAX_FONT_SIZE = 512.0
DEFAULT_FORMAT = "svg"
FONT_CANDIDATES = (
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/SFNS.ttf",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/arial.ttf",
)
MIME_TYPES = {
    "svg": "image/svg+xml",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
}

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TMP_DIR = SKILL_ROOT / "tmp"


def as_int(value: Any, field_name: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise SystemExit(f"Spec field '{field_name}' must be an integer.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render text into an image and return a file path plus optional data URI."
    )
    parser.add_argument("--spec-file", help="Path to a JSON spec file.")
    parser.add_argument("--spec-json", help="Inline JSON spec string.")
    parser.add_argument("--output", help="Optional output image file path.")
    parser.add_argument(
        "--write-temp-file",
        action="store_true",
        help="Deprecated flag kept for compatibility. Temp files are written by default.",
    )
    parser.add_argument(
        "--no-data-url",
        action="store_true",
        help="Omit the base64 data URL from output JSON and return file metadata only.",
    )
    return parser.parse_args()


def load_spec(args: argparse.Namespace) -> Dict[str, Any]:
    if args.spec_json:
        return json.loads(args.spec_json)
    if args.spec_file:
        raw = Path(args.spec_file).read_bytes()
        for encoding in ("utf-8", "utf-8-sig", "utf-16", "utf-16-le", "utf-16-be", "gbk"):
            try:
                return json.loads(raw.decode(encoding))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
        raise SystemExit(f"Unable to decode JSON spec file: {args.spec_file}")
    raise SystemExit("Provide --spec-json or --spec-file.")


def normalize_segments(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    default_color = spec.get("default_color", DEFAULT_COLOR)
    segments = spec.get("segments")
    if segments:
        normalized = []
        for item in segments:
            text = str(item.get("text", ""))
            if not text:
                continue
            normalized.append(
                {
                    "text": text,
                    "color": item.get("color", default_color),
                }
            )
        if normalized:
            return normalized

    text = str(spec.get("text", ""))
    if not text:
        raise SystemExit("Spec must include non-empty 'text' or 'segments'.")

    ranges = normalize_highlight_ranges(spec.get("highlight_ranges", []), text)
    ranges.extend(
        build_highlight_ranges_from_matches(
            text,
            spec.get("highlight_texts", []),
            default_color,
        )
    )
    if not ranges:
        return [{"text": text, "color": default_color}]
    return build_segments_from_ranges(text, ranges, default_color)


def normalize_highlight_ranges(ranges: Any, text: str) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in ranges or []:
        start = as_int(item.get("start"), "highlight_ranges.start")
        end = as_int(item.get("end"), "highlight_ranges.end")
        if start < 0 or end < 0 or start >= end or end > len(text):
            continue
        color = str(item.get("color", DEFAULT_COLOR))
        normalized.append({"start": start, "end": end, "color": color})
    return normalized


def build_highlight_ranges_from_matches(
    text: str,
    highlight_texts: Any,
    default_color: str,
) -> List[Dict[str, Any]]:
    ranges: List[Dict[str, Any]] = []
    for item in highlight_texts or []:
        match = str(item.get("match", ""))
        if not match:
            continue
        color = str(item.get("color", default_color))
        case_sensitive = bool(item.get("case_sensitive", True))
        occurrence = str(item.get("occurrence", "all")).lower()
        matches = find_substring_ranges(text, match, case_sensitive)
        if not matches:
            continue
        if occurrence == "first":
            matches = matches[:1]
        elif occurrence == "last":
            matches = matches[-1:]
        elif occurrence == "all":
            pass
        else:
            try:
                index = int(occurrence)
            except ValueError:
                index = 0
            if 0 <= index < len(matches):
                matches = [matches[index]]
            else:
                matches = []
        for start, end in matches:
            ranges.append({"start": start, "end": end, "color": color})
    return ranges


def find_substring_ranges(text: str, needle: str, case_sensitive: bool) -> List[Tuple[int, int]]:
    haystack = text if case_sensitive else text.lower()
    target = needle if case_sensitive else needle.lower()
    ranges: List[Tuple[int, int]] = []
    start = 0
    while True:
        index = haystack.find(target, start)
        if index < 0:
            break
        ranges.append((index, index + len(needle)))
        start = index + len(needle)
    return ranges


def build_segments_from_ranges(
    text: str,
    ranges: List[Dict[str, Any]],
    default_color: str,
) -> List[Dict[str, Any]]:
    colors = [default_color] * len(text)
    for item in ranges:
        start = item["start"]
        end = item["end"]
        color = item["color"]
        for index in range(start, end):
            colors[index] = color

    segments: List[Dict[str, Any]] = []
    current_text = text[0]
    current_color = colors[0]
    for index in range(1, len(text)):
        if colors[index] == current_color:
            current_text += text[index]
            continue
        segments.append({"text": current_text, "color": current_color})
        current_text = text[index]
        current_color = colors[index]
    segments.append({"text": current_text, "color": current_color})
    return segments


def normalize_format(spec: Dict[str, Any]) -> str:
    image_format = str(spec.get("format", DEFAULT_FORMAT)).lower()
    if image_format not in MIME_TYPES:
        raise SystemExit("Spec 'format' must be one of: svg, png, jpg, jpeg.")
    return image_format


def is_cjk(char: str) -> bool:
    code = ord(char)
    return (
        0x4E00 <= code <= 0x9FFF
        or 0x3400 <= code <= 0x4DBF
        or 0x3040 <= code <= 0x30FF
        or 0xAC00 <= code <= 0xD7AF
        or 0xF900 <= code <= 0xFAFF
    )


def char_width_em(char: str) -> float:
    if char == " ":
        return 0.33
    if char == "\t":
        return 1.32
    if char == "\n":
        return 0.0
    if is_cjk(char):
        return 1.0
    if char.isupper():
        return 0.68
    if char.islower() or char.isdigit():
        return 0.58
    if char in ",.;:!?":
        return 0.32
    if char in "-_/\\|":
        return 0.38
    if char in "()[]{}":
        return 0.36
    return 0.6


def text_width(text: str, font_size: float) -> float:
    return sum(char_width_em(char) for char in text) * font_size


def parse_background(background: str, image_format: str) -> Tuple[int, int, int, int]:
    if background == "transparent":
        if image_format in ("jpg", "jpeg"):
            return (255, 255, 255, 255)
        return (255, 255, 255, 0)
    rgba = ImageColor.getcolor(background, "RGBA")
    if image_format in ("jpg", "jpeg"):
        return (rgba[0], rgba[1], rgba[2], 255)
    return rgba


def normalize_color_for_raster(color: str) -> Tuple[int, int, int, int]:
    return ImageColor.getcolor(color, "RGBA")


def choose_font_file(spec: Dict[str, Any]) -> Optional[str]:
    requested = spec.get("font_path")
    if requested:
        candidate = Path(str(requested))
        if candidate.exists():
            return str(candidate)
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


def tokenize_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    tokens: List[Dict[str, Any]] = []
    for seg in segments:
        text = seg["text"]
        color = seg["color"]
        buffer = ""
        for char in text:
            if char == "\n":
                if buffer:
                    tokens.append({"type": "text", "text": buffer, "color": color})
                    buffer = ""
                tokens.append({"type": "newline"})
            elif char == " ":
                buffer += char
                tokens.append({"type": "text", "text": buffer, "color": color})
                buffer = ""
            else:
                buffer += char
        if buffer:
            tokens.append({"type": "text", "text": buffer, "color": color})
    return merge_adjacent_tokens(tokens)


def merge_adjacent_tokens(tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged: List[Dict[str, Any]] = []
    for token in tokens:
        if token["type"] != "text":
            merged.append(token)
            continue
        if (
            merged
            and merged[-1]["type"] == "text"
            and merged[-1]["color"] == token["color"]
        ):
            merged[-1]["text"] += token["text"]
        else:
            merged.append(token.copy())
    return merged


def split_text_token(token: Dict[str, Any], font_size: float, max_width: float) -> List[Dict[str, Any]]:
    text = token["text"]
    color = token["color"]
    parts: List[Dict[str, Any]] = []
    current = ""
    for char in text:
        candidate = current + char
        if current and text_width(candidate, font_size) > max_width:
            parts.append({"type": "text", "text": current, "color": color})
            current = char
        else:
            current = candidate
    if current:
        parts.append({"type": "text", "text": current, "color": color})
    return parts or [{"type": "text", "text": text, "color": color}]


def wrap_lines(
    segments: List[Dict[str, Any]],
    font_size: float,
    width: float,
    padding: float,
) -> List[List[Dict[str, Any]]]:
    max_width = max(width - padding * 2, font_size)
    tokens = tokenize_segments(segments)
    lines: List[List[Dict[str, Any]]] = [[]]
    line_width = 0.0

    for token in tokens:
        if token["type"] == "newline":
            lines.append([])
            line_width = 0.0
            continue

        token_width = text_width(token["text"], font_size)
        if not lines[-1]:
            if token_width <= max_width:
                lines[-1].append(token)
                line_width = token_width
            else:
                parts = split_text_token(token, font_size, max_width)
                for index, part in enumerate(parts):
                    if index > 0:
                        lines.append([])
                    lines[-1].append(part)
                line_width = text_width(lines[-1][-1]["text"], font_size)
            continue

        if line_width + token_width <= max_width:
            lines[-1].append(token)
            line_width += token_width
            continue

        if token["text"].isspace():
            lines.append([])
            line_width = 0.0
            continue

        if token_width > max_width:
            parts = split_text_token(token, font_size, max_width)
            for part in parts:
                if lines[-1]:
                    lines.append([])
                lines[-1].append(part)
            line_width = text_width(lines[-1][-1]["text"], font_size)
            continue

        lines.append([token])
        line_width = token_width

    return [trim_trailing_space(line) for line in lines] or [[]]


def trim_trailing_space(line: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not line:
        return line
    trimmed = [item.copy() for item in line]
    while trimmed and trimmed[-1]["text"].isspace():
        trimmed.pop()
    return trimmed


def line_pixel_width(line: List[Dict[str, Any]], font_size: float) -> float:
    return sum(text_width(item["text"], font_size) for item in line)


def total_text_height(line_count: int, font_size: float, line_height: float) -> float:
    if line_count <= 0:
        return 0.0
    return line_count * font_size * line_height


def fits(
    segments: List[Dict[str, Any]],
    width: int,
    height: int,
    padding: int,
    font_size: float,
    line_height: float,
) -> Tuple[bool, List[List[Dict[str, Any]]]]:
    lines = wrap_lines(segments, font_size, width, padding)
    content_height = total_text_height(len(lines), font_size, line_height)
    return content_height <= max(height - padding * 2, font_size), lines


def choose_font_size(spec: Dict[str, Any], segments: List[Dict[str, Any]]) -> Tuple[float, List[List[Dict[str, Any]]]]:
    width = int(spec["width"])
    height = int(spec["height"])
    padding = int(spec.get("padding", DEFAULT_PADDING))
    line_height = float(spec.get("line_height", DEFAULT_LINE_HEIGHT))

    explicit_font_size = spec.get("font_size")
    if explicit_font_size is not None:
        font_size = float(explicit_font_size)
        _, lines = fits(segments, width, height, padding, font_size, line_height)
        return font_size, lines

    low = float(spec.get("min_font_size", DEFAULT_MIN_FONT_SIZE))
    high = float(spec.get("max_font_size", DEFAULT_MAX_FONT_SIZE))
    best_size = low
    best_lines = wrap_lines(segments, low, width, padding)

    while high - low > 0.5:
        mid = (low + high) / 2
        ok, lines = fits(segments, width, height, padding, mid, line_height)
        if ok:
            best_size = mid
            best_lines = lines
            low = mid
        else:
            high = mid

    return round(best_size, 2), best_lines


def line_start_x(align: str, width: int, padding: int, line_width_px: float) -> float:
    if align == "left":
        return float(padding)
    if align == "right":
        return float(width - padding) - line_width_px
    return float(width) / 2.0 - line_width_px / 2.0


def top_y(valign: str, height: int, padding: int, content_height: float) -> float:
    available_top = float(padding)
    available_bottom = float(height - padding)
    available_height = available_bottom - available_top
    if valign == "top":
        return available_top
    if valign == "bottom":
        return available_top + max(available_height - content_height, 0.0)
    return available_top + max((available_height - content_height) / 2.0, 0.0)


def render_svg(spec: Dict[str, Any], segments: List[Dict[str, Any]]) -> Tuple[str, float, List[List[Dict[str, Any]]]]:
    width = int(spec["width"])
    height = int(spec["height"])
    padding = int(spec.get("padding", DEFAULT_PADDING))
    background = spec.get("background", DEFAULT_BACKGROUND)
    line_height = float(spec.get("line_height", DEFAULT_LINE_HEIGHT))
    align = spec.get("align", DEFAULT_ALIGN)
    valign = spec.get("valign", DEFAULT_VALIGN)
    font_family = spec.get("font_family", DEFAULT_FONT_FAMILY)

    font_size, lines = choose_font_size(spec, segments)
    content_height = total_text_height(len(lines), font_size, line_height)
    start_y = top_y(valign, height, padding, content_height) + font_size

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="{escape(background)}" />',
    ]

    for index, line in enumerate(lines):
        y = start_y + index * font_size * line_height
        current_x = line_start_x(align, width, padding, line_pixel_width(line, font_size))
        svg_lines.append(
            f'<text x="{current_x:.2f}" y="{y:.2f}" font-size="{font_size:.2f}" font-family="{escape(font_family)}">'
        )
        for item in line:
            color = escape(str(item["color"]))
            text = escape(item["text"])
            svg_lines.append(
                f'<tspan fill="{color}" x="{current_x:.2f}" dy="0">{text}</tspan>'
            )
            current_x += text_width(item["text"], font_size)
        svg_lines.append("</text>")

    svg_lines.append("</svg>")
    return "\n".join(svg_lines), font_size, lines


def load_font(font_path: Optional[str], font_size: float) -> ImageFont.ImageFont:
    size = max(1, int(round(font_size)))
    if font_path:
        try:
            return ImageFont.truetype(font_path, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def measure_text_px(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> float:
    if not text:
        return 0.0
    bbox = draw.textbbox((0, 0), text, font=font)
    return float(bbox[2] - bbox[0])


def line_pixel_width_raster(
    draw: ImageDraw.ImageDraw,
    line: List[Dict[str, Any]],
    font: ImageFont.ImageFont,
) -> float:
    return sum(measure_text_px(draw, item["text"], font) for item in line)


def render_raster(
    spec: Dict[str, Any],
    segments: List[Dict[str, Any]],
    image_format: str,
) -> Tuple[bytes, float, List[List[Dict[str, Any]]]]:
    width = int(spec["width"])
    height = int(spec["height"])
    padding = int(spec.get("padding", DEFAULT_PADDING))
    line_height = float(spec.get("line_height", DEFAULT_LINE_HEIGHT))
    align = spec.get("align", DEFAULT_ALIGN)
    valign = spec.get("valign", DEFAULT_VALIGN)
    background = parse_background(spec.get("background", DEFAULT_BACKGROUND), image_format)
    font_path = choose_font_file(spec)

    image_mode = "RGBA" if image_format == "png" else "RGB"
    background_color = background if image_mode == "RGBA" else background[:3]
    image = Image.new(image_mode, (width, height), background_color)
    draw = ImageDraw.Draw(image)

    font_size, lines = choose_font_size(spec, segments)
    font = load_font(font_path, font_size)
    line_spacing = font_size * line_height
    content_height = total_text_height(len(lines), font_size, line_height)
    start_y = top_y(valign, height, padding, content_height)

    for index, line in enumerate(lines):
        y = start_y + index * line_spacing
        current_x = line_start_x(
            align,
            width,
            padding,
            line_pixel_width_raster(draw, line, font),
        )
        for item in line:
            color = normalize_color_for_raster(str(item["color"]))
            fill = color if image_mode == "RGBA" else color[:3]
            draw.text((current_x, y), item["text"], font=font, fill=fill)
            current_x += measure_text_px(draw, item["text"], font)

    if image_format in ("jpg", "jpeg") and image.mode != "RGB":
        image = image.convert("RGB")

    buffer = io.BytesIO()
    save_format = "JPEG" if image_format in ("jpg", "jpeg") else image_format.upper()
    image.save(buffer, format=save_format, quality=95)
    return buffer.getvalue(), font_size, lines


def ensure_required_dimensions(spec: Dict[str, Any]) -> None:
    if "width" not in spec or "height" not in spec:
        raise SystemExit("Spec must include integer 'width' and 'height'.")


def file_suffix(image_format: str) -> str:
    if image_format == "jpeg":
        return ".jpg"
    return f".{image_format}"


def next_tmp_path(image_format: str) -> Path:
    DEFAULT_TMP_DIR.mkdir(parents=True, exist_ok=True)
    suffix = file_suffix(image_format)
    for index in range(10000):
        candidate = DEFAULT_TMP_DIR / f"rendered-{index:04d}{suffix}"
        if not candidate.exists():
            return candidate
    raise SystemExit(f"Unable to allocate a tmp file in: {DEFAULT_TMP_DIR}")


def write_output_files(
    payload_bytes: bytes,
    output: Optional[str],
    image_format: str,
) -> Optional[str]:
    path: Optional[str] = None
    if output:
        target = Path(output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload_bytes)
        path = str(target.resolve())
    else:
        target = next_tmp_path(image_format)
        target.write_bytes(payload_bytes)
        path = str(target.resolve())
    return path


def main() -> None:
    args = parse_args()
    spec = load_spec(args)
    ensure_required_dimensions(spec)
    segments = normalize_segments(spec)
    image_format = normalize_format(spec)

    if image_format == "svg":
        svg, font_size, lines = render_svg(spec, segments)
        payload_bytes = svg.encode("utf-8")
    else:
        payload_bytes, font_size, lines = render_raster(spec, segments, image_format)

    mime_type = MIME_TYPES[image_format]
    file_path = write_output_files(payload_bytes, args.output, image_format)
    path_obj = Path(file_path) if file_path else None
    file_name = path_obj.name if path_obj else None
    file_size = len(payload_bytes)
    relative_file_path = None
    if path_obj:
        try:
            relative_file_path = path_obj.relative_to(SKILL_ROOT).as_posix()
        except ValueError:
            relative_file_path = None

    payload: Dict[str, Any] = {
        "mime_type": mime_type,
        "format": image_format,
        "width": int(spec["width"]),
        "height": int(spec["height"]),
        "font_size": font_size,
        "line_count": len(lines),
        "resolved_segments": segments,
        "file_path": file_path,
        "file_name": file_name,
        "file_size": file_size,
        "relative_file_path": relative_file_path,
    }
    if not args.no_data_url:
        payload["image_url"] = f"data:{mime_type};base64," + base64.b64encode(payload_bytes).decode("ascii")

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
