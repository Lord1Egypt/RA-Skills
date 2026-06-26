#!/usr/bin/env python3
"""
High-resolution HTML screenshot via Playwright.

Usage:
    python3 screenshot.py <html_file> [output.png] [--scale 4] [--width 1920] [--height 1080] [--full-page]

Defaults:
    - scale: 4 (ultra-high resolution)
    - width: 1920
    - height: 1080
    - full-page: enabled (captures entire scrollable content)
"""

import argparse
import sys
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="High-res HTML screenshot via Playwright")
    parser.add_argument("html", help="Path to HTML file or URL")
    parser.add_argument("output", nargs="?", default=None, help="Output PNG path (default: same name as input with .png)")
    parser.add_argument("--scale", type=int, default=4, help="Device scale factor (default: 4 = ultra-high res)")
    parser.add_argument("--width", type=int, default=1920, help="Viewport width in CSS pixels (default: 1920)")
    parser.add_argument("--height", type=int, default=1080, help="Viewport height in CSS pixels (default: 1080)")
    parser.add_argument("--full-page", action="store_true", default=True, help="Capture full scrollable page (default: true)")
    parser.add_argument("--no-full-page", action="store_true", help="Capture only the viewport")
    parser.add_argument("--wait", type=int, default=1000, help="Wait time in ms after page load (default: 1000)")
    parser.add_argument("--format", choices=["png", "jpeg"], default="png", help="Output format (default: png)")
    parser.add_argument("--quality", type=int, default=92, help="JPEG quality 0-100 (only for jpeg format)")

    args = parser.parse_args()

    full_page = not args.no_full_page

    # Determine input URL
    html_path = args.html
    if not html_path.startswith(("http://", "https://", "file://")):
        abs_path = os.path.abspath(html_path)
        if not os.path.exists(abs_path):
            print(f"Error: File not found: {abs_path}", file=sys.stderr)
            sys.exit(1)
        html_path = f"file://{abs_path}"

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        base = Path(args.html).stem if not args.html.startswith("http") else "screenshot"
        output_path = f"{base}.png"

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)

    print(f"Rendering: {html_path}")
    print(f"Viewport: {args.width}x{args.height} @ {args.scale}x scale")
    print(f"Output resolution: {args.width * args.scale}x{args.height * args.scale}+ pixels")
    print(f"Full page: {full_page}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
        )
        page.goto(html_path, wait_until="networkidle")

        if args.wait > 0:
            page.wait_for_timeout(args.wait)

        screenshot_args = {"path": output_path, "full_page": full_page}
        if args.format == "jpeg":
            screenshot_args["type"] = "jpeg"
            screenshot_args["quality"] = args.quality

        page.screenshot(**screenshot_args)
        browser.close()

    file_size = os.path.getsize(output_path)
    size_str = f"{file_size / 1024:.0f}KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.1f}MB"

    # Get actual image dimensions
    try:
        from PIL import Image
        img = Image.open(output_path)
        actual_w, actual_h = img.size
        print(f"✅ Saved: {output_path} ({actual_w}x{actual_h}px, {size_str})")
    except ImportError:
        print(f"✅ Saved: {output_path} ({size_str})")


if __name__ == "__main__":
    main()
