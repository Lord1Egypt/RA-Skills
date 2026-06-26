#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "playwright",
# ]
# ///
"""
HTML to PDF converter using Playwright.
Usage: uv run html_to_pdf.py --html report.html --output report.pdf
"""

import argparse
import sys
import os


def convert(html_path: str, output_path: str):
    from playwright.sync_api import sync_playwright

    html_path = os.path.abspath(html_path)
    output_path = os.path.abspath(output_path)

    if not os.path.exists(html_path):
        sys.exit(f"ERROR: HTML file not found: {html_path}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    file_url = f"file://{html_path}"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(2000)  # wait for Tailwind CDN to load
        page.pdf(
            path=output_path,
            format="A4",
            margin={"top": "10mm", "right": "10mm", "bottom": "10mm", "left": "10mm"},
            print_background=True,
        )
        browser.close()

    print(f"MEDIA:{output_path}")
    print(f"✅ PDF saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert HTML report to PDF")
    parser.add_argument("--html", required=True, help="Input HTML file path")
    parser.add_argument("--output", required=True, help="Output PDF file path")
    args = parser.parse_args()
    convert(args.html, args.output)


if __name__ == "__main__":
    main()
