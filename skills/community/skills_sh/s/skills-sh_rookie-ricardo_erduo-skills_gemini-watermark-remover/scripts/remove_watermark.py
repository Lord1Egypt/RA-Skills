#!/usr/bin/env python3
import os
import sys
from typing import List, Tuple

from PIL import Image

ALPHA_THRESHOLD = 0.002
MAX_ALPHA = 0.99
LOGO_VALUE = 255


def detect_watermark_config(width: int, height: int) -> Tuple[int, int, int]:
    if width > 1024 and height > 1024:
        return 96, 64, 64
    return 48, 32, 32


def calculate_position(width: int, height: int, logo_size: int, margin_right: int, margin_bottom: int) -> Tuple[int, int]:
    return width - margin_right - logo_size, height - margin_bottom - logo_size


def load_alpha_map(logo_size: int) -> List[float]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    asset_name = "bg_48.png" if logo_size == 48 else "bg_96.png"
    asset_path = os.path.abspath(os.path.join(script_dir, "..", "assets", asset_name))

    with Image.open(asset_path) as img:
        img = img.convert("RGB")
        if img.width != logo_size or img.height != logo_size:
            raise ValueError(f"Unexpected asset size for {asset_name}: {img.width}x{img.height}")
        pixels = list(img.getdata())

    alpha_map: List[float] = [0.0] * (logo_size * logo_size)
    for i, (r, g, b) in enumerate(pixels):
        max_channel = r if r >= g and r >= b else (g if g >= b else b)
        alpha_map[i] = max_channel / 255.0

    return alpha_map


def remove_watermark(input_path: str, output_path: str) -> None:
    with Image.open(input_path) as img:
        img = img.convert("RGBA")
        width, height = img.size
        logo_size, margin_right, margin_bottom = detect_watermark_config(width, height)
        start_x, start_y = calculate_position(width, height, logo_size, margin_right, margin_bottom)
        alpha_map = load_alpha_map(logo_size)

        pixels = img.load()
        for row in range(logo_size):
            y = start_y + row
            if y < 0 or y >= height:
                continue
            alpha_row_offset = row * logo_size
            for col in range(logo_size):
                x = start_x + col
                if x < 0 or x >= width:
                    continue
                alpha = alpha_map[alpha_row_offset + col]
                if alpha < ALPHA_THRESHOLD:
                    continue
                if alpha > MAX_ALPHA:
                    alpha = MAX_ALPHA
                one_minus_alpha = 1.0 - alpha

                r, g, b, a = pixels[x, y]
                r_out = int(round((r - alpha * LOGO_VALUE) / one_minus_alpha))
                g_out = int(round((g - alpha * LOGO_VALUE) / one_minus_alpha))
                b_out = int(round((b - alpha * LOGO_VALUE) / one_minus_alpha))

                r_out = 0 if r_out < 0 else (255 if r_out > 255 else r_out)
                g_out = 0 if g_out < 0 else (255 if g_out > 255 else g_out)
                b_out = 0 if b_out < 0 else (255 if b_out > 255 else b_out)

                pixels[x, y] = (r_out, g_out, b_out, a)

        output_ext = os.path.splitext(output_path)[1].lower()
        if output_ext in {".jpg", ".jpeg"}:
            img = img.convert("RGB")

        img.save(output_path)


def usage() -> str:
    script_name = os.path.basename(sys.argv[0])
    return f"Usage: python {script_name} <input-image> <output-image>"


def main() -> int:
    if len(sys.argv) != 3:
        print(usage(), file=sys.stderr)
        return 1

    input_path, output_path = sys.argv[1], sys.argv[2]
    try:
        remove_watermark(input_path, output_path)
    except Exception as exc:
        print(f"Failed: {exc}", file=sys.stderr)
        return 1

    print(f"Removed watermark -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
