#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright


def read_input(value: str | None) -> tuple[str, Path | None]:
    if value is None:
        return sys.stdin.read(), None
    candidate = Path(value)
    if candidate.exists() and candidate.is_file():
        return candidate.read_text(encoding="utf-8"), candidate
    return value, None


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def render_png(html_path: Path, png_path: Path, width: int, scale: float) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": width, "height": 1000},
            device_scale_factor=scale,
        )
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        page.screenshot(path=str(png_path), full_page=True)
        browser.close()


def write_temp_html(content: str) -> Path:
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(content)
        return Path(tmp.name)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render complete HTML into a long PNG screenshot. Input can be an HTML file path, raw HTML string, or stdin."
    )
    parser.add_argument(
        "--input",
        help="Input HTML file path or raw HTML string. If omitted, read from stdin.",
    )
    parser.add_argument(
        "--html-out",
        help="Optional persistent HTML output path. If omitted and --input is an existing HTML file, reuse that file. Otherwise create a temp HTML file and delete it after rendering.",
    )
    parser.add_argument("--png-out", required=True, help="Output PNG path.")
    parser.add_argument("--width", type=int, default=1080, help="Viewport width in CSS pixels.")
    parser.add_argument("--scale", type=float, default=2.0, help="Device scale factor.")
    args = parser.parse_args()

    content, input_html_path = read_input(args.input)
    if not content.strip():
        raise SystemExit("Input HTML is empty.")

    png_path = Path(args.png_out)
    ensure_parent(png_path)

    cleanup_html = False
    if args.html_out:
        html_path = Path(args.html_out)
        ensure_parent(html_path)
        html_path.write_text(content, encoding="utf-8")
    elif input_html_path is not None:
        html_path = input_html_path
    else:
        html_path = write_temp_html(content)
        cleanup_html = True

    try:
        render_png(html_path, png_path, args.width, args.scale)
    finally:
        if cleanup_html:
            html_path.unlink(missing_ok=True)

    print(f"HTML: {html_path}")
    print(f"PNG: {png_path}")
    if cleanup_html:
        print("HTML_CLEANUP: auto-deleted temp HTML after render")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
