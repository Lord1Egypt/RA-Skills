#!/usr/bin/env python3
"""
SVG Architecture Diagram → High-res PNG screenshot via Playwright.

Usage:
    python3 screenshot.py <input.html> [output.png] [--scale 2] [--width 1600] [--height 1000]

Defaults optimized for architecture diagrams:
    - scale: 2 (high-res, good balance of quality and file size)
    - width: 1600
    - height: 1000
"""

import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser(description="SVG diagram screenshot via Playwright")
    parser.add_argument("html", help="Path to HTML file containing SVG diagram")
    parser.add_argument("output", nargs="?", default=None, help="Output PNG path")
    parser.add_argument("--scale", type=int, default=4, help="Device scale factor (default: 4)")
    parser.add_argument("--width", type=int, default=1600, help="Viewport width (default: 1600)")
    parser.add_argument("--height", type=int, default=1000, help="Viewport height (default: 1000)")
    parser.add_argument("--wait", type=int, default=1500, help="Wait ms after load (default: 1500)")

    args = parser.parse_args()

    html_path = args.html
    if not html_path.startswith(("http://", "https://", "file://")):
        abs_path = os.path.abspath(html_path)
        if not os.path.exists(abs_path):
            print(f"Error: File not found: {abs_path}", file=sys.stderr)
            sys.exit(1)
        html_path = f"file://{abs_path}"

    if args.output:
        output_path = args.output
    else:
        from pathlib import Path
        output_path = f"{Path(args.html).stem}.png"

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)

    print(f"Rendering: {html_path}")
    print(f"Viewport: {args.width}x{args.height} @ {args.scale}x")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
        )
        page.goto(html_path, wait_until="networkidle")
        if args.wait > 0:
            page.wait_for_timeout(args.wait)
        page.screenshot(path=output_path, full_page=True)
        browser.close()

    file_size = os.path.getsize(output_path)
    size_str = f"{file_size / 1024:.0f}KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.1f}MB"

    try:
        from PIL import Image
        img = Image.open(output_path)
        print(f"✅ {output_path} ({img.size[0]}x{img.size[1]}, {size_str})")
    except ImportError:
        print(f"✅ {output_path} ({size_str})")


if __name__ == "__main__":
    main()
