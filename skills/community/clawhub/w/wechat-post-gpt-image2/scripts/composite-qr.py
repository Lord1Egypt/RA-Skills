#!/usr/bin/env python3
"""Composite QR code onto a WeChat post image."""
import sys
from pathlib import Path
from PIL import Image

def composite_qr(main_path: str, qr_path: str, output_path: str):
    main = Image.open(main_path).convert("RGBA")
    qr = Image.open(qr_path).convert("RGBA")

    # QR size: 12% of main image width
    qr_width = int(main.width * 0.12)
    qr_height = int(qr_width * qr.height / qr.width)
    qr = qr.resize((qr_width, qr_height), Image.LANCZOS)

    # White border: 3% of QR width
    border = int(qr_width * 0.03)
    bordered = Image.new("RGBA", (qr_width + 2*border, qr_height + 2*border), (255, 255, 255, 255))
    bordered.paste(qr, (border, border))

    # Position: bottom-right, 5% margin
    margin = int(main.width * 0.05)
    x = main.width - bordered.width - margin
    y = main.height - bordered.height - margin

    main.paste(bordered, (x, y), bordered)
    main.save(output_path, "PNG")
    print(f"QR composited → {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: composite-qr.py <main_image> <qr_image> <output_path>")
        sys.exit(1)
    composite_qr(sys.argv[1], sys.argv[2], sys.argv[3])
