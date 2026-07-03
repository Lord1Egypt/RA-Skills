#!/usr/bin/env python3
"""
Convert HTML resume to PDF format.
Uses Playwright/Chromium for high-quality output.
"""

import sys
import argparse
from pathlib import Path
from urllib.parse import urlsplit

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


PDF_MARGIN = "10mm"
ALLOWED_RESOURCE_SCHEMES = {"file", "data"}


def block_external_requests(route):
    """Allow only local file/data resources during PDF rendering."""
    parsed = urlsplit(route.request.url)
    if parsed.scheme.lower() in ALLOWED_RESOURCE_SCHEMES:
        route.continue_()
        return
    route.abort()


def convert_with_playwright(html_path, output_path):
    """Convert HTML to PDF using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.route("**/*", block_external_requests)

        # Load HTML file
        html_url = f"file://{Path(html_path).absolute()}"
        page.goto(html_url, wait_until="networkidle")

        # Generate PDF
        page.pdf(
            path=output_path,
            format="A4",
            margin={
                "top": PDF_MARGIN,
                "right": PDF_MARGIN,
                "bottom": PDF_MARGIN,
                "left": PDF_MARGIN
            },
            print_background=True
        )

        browser.close()
    return True


def print_install_instructions():
    """Print the supported PDF export dependency installation steps."""
    print("Error: Playwright is required for PDF conversion.")
    print("Install it with:")
    print("  pip install playwright==1.60.0")
    print("  playwright install chromium")
    print("  PDF rendering blocks external network requests by design.")


def main():
    parser = argparse.ArgumentParser(description='Convert HTML resume to PDF')
    parser.add_argument('html_file', help='Path to HTML resume file')
    parser.add_argument('output_pdf', help='Path to output PDF file')

    args = parser.parse_args()

    if not Path(args.html_file).exists():
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)

    print(f"Converting {args.html_file} to PDF...")

    if not HAS_PLAYWRIGHT:
        print_install_instructions()
        sys.exit(1)

    try:
        print("Using Playwright (Chromium)...")
        convert_with_playwright(args.html_file, args.output_pdf)
    except Exception as e:
        print(f"Playwright PDF conversion failed: {e}")
        print("Ensure the Chromium browser is installed with:")
        print("  playwright install chromium")
        sys.exit(1)

    print(f"PDF generated: {args.output_pdf}")


if __name__ == "__main__":
    main()
