#!/usr/bin/env python3
"""Optional light watermark for PNG diagrams."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Skill package assets/ (sibling of scripts/)
_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
_DEFAULT_FONT = _ASSETS_DIR / "DejaVuSans.ttf"


def add_watermark(
    png_path: str | Path,
    text: str = "yanleaf.com",
    out_path: str | Path | None = None,
    opacity: int = 70,
    font_path: str | Path | None = None,
) -> Path:
    """
    Draw a subtle corner watermark. Does not block diagram content.
    Font defaults to assets/DejaVuSans.ttf inside the skill package.
    """
    png_path = Path(png_path)
    out_path = Path(out_path) if out_path else png_path

    im = Image.open(png_path).convert("RGBA")
    overlay = Image.new("RGBA", im.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    font = None
    candidates = []
    if font_path:
        candidates.append(Path(font_path))
    candidates.append(_DEFAULT_FONT)
    candidates.append(Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

    for fp in candidates:
        try:
            if fp.is_file():
                font = ImageFont.truetype(str(fp), 14)
                break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = im.size[0] - tw - 12
    y = im.size[1] - th - 10
    draw.text((x, y), text, fill=(120, 120, 120, opacity), font=font)

    merged = Image.alpha_composite(im, overlay)
    if out_path.suffix.lower() != ".png":
        out_path = out_path.with_suffix(".png")
    merged.convert("RGBA").save(out_path)
    return out_path
