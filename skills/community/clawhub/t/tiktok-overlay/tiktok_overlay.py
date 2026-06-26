"""
TikTok-style text overlay tool.

Flexible input formats — all of these work:

    # Style: string, enum, or None
    overlay_text(img, "Hello", style="classic")
    overlay_text(img, "Hello", style=TikTokStyle.CLASSIC)

    # Color: hex, rgb tuple, rgba tuple, or named color
    overlay_text(img, "Hello", text_color="#FF0000")
    overlay_text(img, "Hello", text_color="red")
    overlay_text(img, "Hello", text_color=(255, 0, 0))
    overlay_text(img, "Hello", text_color=(255, 0, 0, 128))

    # Input: file path, PIL Image, or numpy array
    overlay_text("photo.jpg", "Hello", "output.jpg")
    overlay_text(pil_image, "Hello", "output.jpg")
    overlay_text(numpy_array, "Hello", "output.jpg")

    # Output: file path, or None to get PIL Image back
    result_img = overlay_text("photo.jpg", "Hello")

    # Position: string, tuple px, tuple %, or dict
    overlay_text(img, "Hello", position="center")
    overlay_text(img, "Hello", position=(100, 200))
    overlay_text(img, "Hello", position=("50%", "80%"))
    overlay_text(img, "Hello", position={"x": "50%", "y": "top"})

    # Font size: int px, string, or named size
    overlay_text(img, "Hello", font_size=48)
    overlay_text(img, "Hello", font_size="large")
    overlay_text(img, "Hello", font_size="48px")

    # Opacity: float 0-1, int 0-255, or string percentage
    overlay_text(img, "Hello", bg_opacity=0.6)
    overlay_text(img, "Hello", bg_opacity=153)
    overlay_text(img, "Hello", bg_opacity="60%")

    # Multiple text overlays (list of TextOverlay, dicts, or tuples)
    overlay_texts(img, [
        TextOverlay("Top", position="top"),
        {"text": "Middle", "position": "center", "style": "strong"},
        ("Bottom text", {"position": "bottom", "text_color": "red"}),
    ])
"""

from PIL import Image, ImageDraw, ImageFont, ImageColor
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union
import os


# --- Font mapping (macOS system fonts as TikTok-like substitutes) ---

FONT_DIR = "/System/Library/Fonts/Supplemental"
FONT_DIR_SYSTEM = "/System/Library/Fonts"


class TikTokStyle(str, Enum):
    CLASSIC = "classic"          # Clean sans-serif (like TikTok Classic)
    TYPEWRITER = "typewriter"    # Monospace/typewriter look
    HANDWRITING = "handwriting"  # Casual handwriting
    NEON = "neon"                # Bold glow effect
    SERIF = "serif"              # Traditional serif
    STRONG = "strong"            # Extra bold / impact
    COMIC = "comic"             # Playful comic style


FONT_MAP = {
    TikTokStyle.CLASSIC: [
        os.path.join(FONT_DIR, "Arial Bold.ttf"),
        os.path.join(FONT_DIR_SYSTEM, "Helvetica.ttc"),
    ],
    TikTokStyle.TYPEWRITER: [
        os.path.join(FONT_DIR, "AmericanTypewriter.ttc"),
        os.path.join(FONT_DIR, "Courier New Bold.ttf"),
    ],
    TikTokStyle.HANDWRITING: [
        os.path.join(FONT_DIR, "ChalkboardSE.ttc"),
        os.path.join(FONT_DIR, "Chalkboard.ttc"),
    ],
    TikTokStyle.NEON: [
        os.path.join(FONT_DIR, "Arial Rounded Bold.ttf"),
        os.path.join(FONT_DIR, "Arial Bold.ttf"),
    ],
    TikTokStyle.SERIF: [
        os.path.join(FONT_DIR, "Georgia Bold.ttf"),
        os.path.join(FONT_DIR, "Georgia.ttf"),
    ],
    TikTokStyle.STRONG: [
        os.path.join(FONT_DIR, "Impact.ttf"),
        os.path.join(FONT_DIR, "Arial Bold.ttf"),
    ],
    TikTokStyle.COMIC: [
        os.path.join(FONT_DIR, "Comic Sans MS Bold.ttf"),
        os.path.join(FONT_DIR, "Comic Sans MS.ttf"),
    ],
}

# Named font sizes
NAMED_SIZES = {
    "xs": 24, "extra-small": 24,
    "sm": 32, "small": 32,
    "md": 48, "medium": 48,
    "lg": 64, "large": 64,
    "xl": 80, "extra-large": 80,
    "xxl": 96, "huge": 96,
    "title": 72,
    "subtitle": 40,
    "caption": 28,
}


# --- Flexible input normalizers ---

def _normalize_color(color, opacity: float = 1.0) -> tuple:
    """Accept hex, rgb tuple, rgba tuple, named color, or None."""
    if color is None:
        return (255, 255, 255, int(opacity * 255))

    # Already an RGBA tuple
    if isinstance(color, (tuple, list)):
        if len(color) == 4:
            return tuple(color)
        if len(color) == 3:
            return (*color, int(opacity * 255))
        raise ValueError(f"Color tuple must have 3 or 4 values, got {len(color)}")

    if not isinstance(color, str):
        raise ValueError(f"Unsupported color type: {type(color)}")

    color = color.strip()

    # Hex color
    if color.startswith("#"):
        hex_color = color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join(c * 2 for c in hex_color)
        if len(hex_color) == 8:  # RGBA hex
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            a = int(hex_color[6:8], 16)
            return (r, g, b, a)
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return (r, g, b, int(opacity * 255))

    # Try PIL named color (red, blue, coral, etc.)
    try:
        r, g, b = ImageColor.getrgb(color)
        return (r, g, b, int(opacity * 255))
    except ValueError:
        pass

    # rgb(...) / rgba(...) string
    if color.startswith("rgb"):
        nums = [int(x.strip().rstrip("%")) for x in color.split("(")[1].rstrip(")").split(",")]
        if len(nums) == 3:
            return (*nums, int(opacity * 255))
        return tuple(nums)

    raise ValueError(f"Cannot parse color: {color}")


def _normalize_opacity(value) -> float:
    """Accept float 0-1, int 0-255, or string like '60%'."""
    if value is None:
        return 1.0
    if isinstance(value, str):
        value = value.strip()
        if value.endswith("%"):
            return float(value.rstrip("%")) / 100.0
        return float(value)
    if isinstance(value, int) and value > 1:
        return value / 255.0
    return float(value)


def _normalize_font_size(value) -> int:
    """Accept int, string like '48px', or named size like 'large'."""
    if value is None:
        return 48
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        value = value.strip().lower()
        if value in NAMED_SIZES:
            return NAMED_SIZES[value]
        # Strip 'px' or 'pt' suffix
        for suffix in ("px", "pt", "sp"):
            if value.endswith(suffix):
                return int(value.removesuffix(suffix))
        return int(value)
    return 48


def _normalize_style(style) -> TikTokStyle:
    """Accept TikTokStyle enum, string, or None."""
    if style is None:
        return TikTokStyle.CLASSIC
    if isinstance(style, TikTokStyle):
        return style
    if isinstance(style, str):
        style = style.strip().lower()
        try:
            return TikTokStyle(style)
        except ValueError:
            # Try matching by name
            for s in TikTokStyle:
                if s.name.lower() == style:
                    return s
            raise ValueError(f"Unknown style: {style}. Options: {', '.join(s.value for s in TikTokStyle)}")
    raise ValueError(f"Unsupported style type: {type(style)}")


def _normalize_position(position, img_w: int = 0, img_h: int = 0):
    """
    Accept:
      - string: "top", "center", "bottom", "top-left", "top-right", "bottom-left", "bottom-right"
      - tuple of int: (x, y) in pixels
      - tuple of str: ("50%", "80%") as percentage of image size
      - dict: {"x": 100, "y": 200} or {"x": "50%", "y": "top"}
      - list: [x, y]
    """
    if position is None:
        return "center"

    if isinstance(position, str):
        return position.strip().lower()

    if isinstance(position, dict):
        x = position.get("x", "50%")
        y = position.get("y", "50%")
        return _resolve_xy(x, y, img_w, img_h)

    if isinstance(position, (tuple, list)) and len(position) == 2:
        x, y = position
        return _resolve_xy(x, y, img_w, img_h)

    return position


def _resolve_xy(x, y, img_w, img_h):
    """Resolve x, y which can be int, float, or percentage string."""
    def _resolve_one(val, total):
        if isinstance(val, str):
            val = val.strip()
            if val.endswith("%"):
                return int(float(val.rstrip("%")) / 100.0 * total)
            if val in ("top", "left"):
                return int(total * 0.08)
            if val in ("center", "middle"):
                return total // 2
            if val in ("bottom", "right"):
                return int(total * 0.92)
            return int(val)
        return int(val)

    return (_resolve_one(x, img_w), _resolve_one(y, img_h))


def _normalize_input(input_source) -> Image.Image:
    """Accept file path string, PIL Image, numpy array, or bytes."""
    if isinstance(input_source, Image.Image):
        return input_source.copy()

    if isinstance(input_source, str):
        return Image.open(input_source)

    if isinstance(input_source, bytes):
        import io
        return Image.open(io.BytesIO(input_source))

    # numpy array
    try:
        import numpy as np
        if isinstance(input_source, np.ndarray):
            return Image.fromarray(input_source)
    except ImportError:
        pass

    raise ValueError(f"Unsupported input type: {type(input_source)}")


def _normalize_overlay(item) -> 'TextOverlay':
    """Accept TextOverlay, dict, or (text, kwargs_dict) tuple."""
    if isinstance(item, TextOverlay):
        return item

    if isinstance(item, dict):
        return TextOverlay(**{k: v for k, v in item.items()})

    if isinstance(item, (tuple, list)):
        if len(item) == 2 and isinstance(item[1], dict):
            return TextOverlay(text=item[0], **item[1])
        if len(item) >= 1 and isinstance(item[0], str):
            return TextOverlay(text=item[0])

    raise ValueError(f"Cannot convert to TextOverlay: {item}")


# --- Core functions ---

def _load_font(style: TikTokStyle, size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_MAP.get(style, []):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Word-wrap text to fit within max_width pixels."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current_line = ""
        for word in words:
            test = f"{current_line} {word}".strip()
            bbox = font.getbbox(test)
            if bbox[2] - bbox[0] > max_width and current_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test
        if current_line:
            lines.append(current_line)
    return lines if lines else [""]


@dataclass
class TextOverlay:
    text: str
    style: Union[TikTokStyle, str, None] = TikTokStyle.CLASSIC
    font_size: Union[int, str] = 48
    text_color: Union[str, tuple, None] = "#FFFFFF"
    bg_style: Optional[str] = "highlight"   # none, highlight, full_bg, letter
    bg_color: Union[str, tuple, None] = "#000000"
    bg_opacity: Union[float, int, str] = 0.6
    position: Union[str, tuple, list, dict, None] = "center"
    alignment: Optional[str] = "center"     # left, center, right
    stroke_width: Union[int, str] = 0
    stroke_color: Union[str, tuple, None] = "#000000"
    padding: Union[int, str] = 8
    line_spacing: Union[int, str] = 6
    max_width_ratio: Union[float, str] = 0.85
    rotation: float = 0.0

    def __post_init__(self):
        """Normalize all fields to their canonical types."""
        self.style = _normalize_style(self.style)
        self.font_size = _normalize_font_size(self.font_size)
        self.bg_opacity = _normalize_opacity(self.bg_opacity)
        self.bg_style = (self.bg_style or "none").strip().lower()
        self.alignment = (self.alignment or "center").strip().lower()
        self.stroke_width = int(self.stroke_width) if self.stroke_width else 0
        self.padding = int(self.padding) if self.padding else 8
        self.line_spacing = int(self.line_spacing) if self.line_spacing else 6
        if isinstance(self.max_width_ratio, str):
            v = self.max_width_ratio.strip().rstrip("%")
            self.max_width_ratio = float(v) / 100.0 if float(v) > 1 else float(v)


def _compute_position(
    img_w: int, img_h: int,
    block_w: int, block_h: int,
    position: Union[str, tuple],
) -> tuple[int, int]:
    if isinstance(position, (tuple, list)):
        return (int(position[0]), int(position[1]))

    position = str(position).strip().lower()
    # Horizontal alignment for compound positions
    if "left" in position:
        x = int(img_w * 0.05)
    elif "right" in position:
        x = int(img_w * 0.95) - block_w
    else:
        x = (img_w - block_w) // 2

    if position.startswith("top"):
        y = int(img_h * 0.08)
    elif position.startswith("bottom"):
        y = int(img_h * 0.92) - block_h
    else:  # center
        y = (img_h - block_h) // 2
    return x, y


def _draw_text_block(
    img: Image.Image,
    overlay: TextOverlay,
) -> Image.Image:
    """Draw a single text overlay onto the image (returns new image)."""
    img = img.convert("RGBA")
    font = _load_font(overlay.style, overlay.font_size)
    max_width = int(img.width * overlay.max_width_ratio)
    lines = _wrap_text(overlay.text, font, max_width)

    # Measure each line
    line_sizes = []
    for line in lines:
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        line_sizes.append((w, h))

    ascent, descent = font.getmetrics()
    line_height = ascent + descent
    pad = overlay.padding
    total_h = len(lines) * line_height + (len(lines) - 1) * overlay.line_spacing
    block_w = max(s[0] for s in line_sizes) + pad * 2
    block_h = total_h + pad * 2

    # Normalize position (may need image dimensions for % values)
    pos = _normalize_position(overlay.position, img.width, img.height)
    bx, by = _compute_position(img.width, img.height, block_w, block_h, pos)

    # Create overlay layer for backgrounds
    bg_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg_layer)
    bg_rgba = _normalize_color(overlay.bg_color, overlay.bg_opacity)

    # Draw backgrounds per line or full block
    if overlay.bg_style == "full_bg":
        bg_draw.rounded_rectangle(
            [bx, by, bx + block_w, by + block_h],
            radius=8, fill=bg_rgba,
        )
    elif overlay.bg_style in ("highlight", "letter"):
        y_cursor = by + pad
        for i, line in enumerate(lines):
            lw, _ = line_sizes[i]
            if overlay.alignment == "center":
                lx = bx + (block_w - lw) // 2 - pad
            elif overlay.alignment == "right":
                lx = bx + block_w - lw - pad * 2
            else:
                lx = bx

            bg_draw.rounded_rectangle(
                [lx, y_cursor - 2, lx + lw + pad * 2, y_cursor + line_height + 2],
                radius=4, fill=bg_rgba,
            )
            y_cursor += line_height + overlay.line_spacing

    img = Image.alpha_composite(img, bg_layer)

    # Draw text
    txt_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_layer)
    text_rgba = _normalize_color(overlay.text_color)
    stroke_rgba = _normalize_color(overlay.stroke_color) if overlay.stroke_width > 0 else None

    # Neon glow effect
    if overlay.style == TikTokStyle.NEON:
        glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        glow_color = _normalize_color(overlay.text_color, 0.15)
        y_cursor = by + pad
        for i, line in enumerate(lines):
            lw, _ = line_sizes[i]
            if overlay.alignment == "center":
                lx = bx + (block_w - lw) // 2
            elif overlay.alignment == "right":
                lx = bx + block_w - lw - pad
            else:
                lx = bx + pad
            for dx in range(-4, 5):
                for dy in range(-4, 5):
                    glow_draw.text((lx + dx, y_cursor + dy), line, font=font, fill=glow_color)
            y_cursor += line_height + overlay.line_spacing
        img = Image.alpha_composite(img, glow_layer)

    y_cursor = by + pad
    for i, line in enumerate(lines):
        lw, _ = line_sizes[i]
        if overlay.alignment == "center":
            lx = bx + (block_w - lw) // 2
        elif overlay.alignment == "right":
            lx = bx + block_w - lw - pad
        else:
            lx = bx + pad

        if overlay.stroke_width > 0:
            txt_draw.text(
                (lx, y_cursor), line, font=font, fill=text_rgba,
                stroke_width=overlay.stroke_width, stroke_fill=stroke_rgba,
            )
        else:
            txt_draw.text((lx, y_cursor), line, font=font, fill=text_rgba)

        y_cursor += line_height + overlay.line_spacing

    img = Image.alpha_composite(img, txt_layer)
    return img


def overlay_text(
    input_source,
    text: str,
    output_path: Optional[str] = None,
    style=None,
    font_size=48,
    text_color="#FFFFFF",
    bg_style="highlight",
    bg_color="#000000",
    bg_opacity=0.6,
    position="center",
    alignment="center",
    stroke_width=0,
    stroke_color="#000000",
    padding=8,
    line_spacing=6,
    max_width_ratio=0.85,
    rotation=0.0,
) -> Union[str, Image.Image]:
    """
    Add a single TikTok-style text overlay to an image.

    Args:
        input_source: File path, PIL Image, numpy array, or bytes.
        text: Text to overlay.
        output_path: Save path. If None, returns PIL Image instead.
        style: "classic", "strong", "neon", etc. or TikTokStyle enum.
        font_size: Int pixels, "48px", or named: "small", "medium", "large", "xl", "title".
        text_color: "#FF0000", "red", (255,0,0), or (255,0,0,128).
        bg_style: "none", "highlight", "full_bg", "letter".
        bg_color: Same formats as text_color.
        bg_opacity: 0.0-1.0, 0-255, or "60%".
        position: "top", "center", "bottom", "top-left", "bottom-right",
                  (x, y), ("50%", "80%"), {"x": 100, "y": "top"}.
        alignment: "left", "center", "right".
        stroke_width: Outline thickness (4-6 for TikTok look).
        stroke_color: Same formats as text_color.
        padding: Padding around text in pixels.
        line_spacing: Space between lines in pixels.
        max_width_ratio: 0.0-1.0 or "85%".

    Returns:
        output_path if saving to file, PIL Image if output_path is None.
    """
    img = _normalize_input(input_source)
    t = TextOverlay(
        text=text, style=style, font_size=font_size, text_color=text_color,
        bg_style=bg_style, bg_color=bg_color, bg_opacity=bg_opacity,
        position=position, alignment=alignment, stroke_width=stroke_width,
        stroke_color=stroke_color, padding=padding, line_spacing=line_spacing,
        max_width_ratio=max_width_ratio, rotation=rotation,
    )
    result = _draw_text_block(img, t)

    if output_path is None:
        return result
    result.convert("RGB").save(output_path, quality=95)
    return output_path


def overlay_texts(
    input_source,
    overlays: list,
    output_path: Optional[str] = None,
) -> Union[str, Image.Image]:
    """
    Add multiple TikTok-style text overlays to an image.

    Args:
        input_source: File path, PIL Image, numpy array, or bytes.
        overlays: List of TextOverlay, dicts, or (text, kwargs) tuples.
            Examples:
              TextOverlay("Hello", position="top")
              {"text": "Hello", "position": "top", "style": "strong"}
              ("Hello", {"position": "top", "text_color": "red"})
        output_path: Save path. If None, returns PIL Image instead.

    Returns:
        output_path if saving to file, PIL Image if output_path is None.
    """
    img = _normalize_input(input_source)
    for item in overlays:
        t = _normalize_overlay(item)
        img = _draw_text_block(img, t)

    if output_path is None:
        return img
    img.convert("RGB").save(output_path, quality=95)
    return output_path


# --- CLI usage ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python tiktok_overlay.py <input_image> <text> [output_image] [style]")
        print(f"Styles: {', '.join(s.value for s in TikTokStyle)}")
        print(f"Sizes:  {', '.join(NAMED_SIZES.keys())}")
        sys.exit(1)

    input_path = sys.argv[1]
    text = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else input_path.rsplit(".", 1)[0] + "_overlay." + input_path.rsplit(".", 1)[1]
    style = sys.argv[4] if len(sys.argv) > 4 else "classic"

    overlay_text(input_path, text, output_path, style=style, stroke_width=2)
    print(f"Saved to {output_path}")
