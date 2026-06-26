#!/usr/bin/env python3
"""Generate high-quality screenshot of schedule HTML."""

import sys
from playwright.sync_api import sync_playwright

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_screenshot.py <html_path> <output_path>")
        sys.exit(1)
    
    html_path = sys.argv[1]
    output_path = sys.argv[2]
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # High resolution with device scale factor
        page = browser.new_page(
            viewport={'width': 600, 'height': 1200},
            device_scale_factor=2
        )
        page.goto(f'file://{html_path}')
        page.wait_for_timeout(2000)  # Wait for fonts to load
        page.screenshot(path=output_path, full_page=True)
        browser.close()
    
    print(f"Screenshot saved: {output_path}")

if __name__ == "__main__":
    main()
