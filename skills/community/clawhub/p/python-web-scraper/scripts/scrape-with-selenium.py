#!/usr/bin/env python3
"""
scrape-with-selenium.py — JavaScript-heavy sites with Selenium
Usage: python3 scrape-with-selenium.py <url> [--wait 3] [--selector div.item]

Requires: pip install selenium webdriver-manager

Handles:
- Dynamic content (JS-rendered pages)
- Scroll-to-load (infinite scroll)
- Waiting for specific elements
- Cookie/header injection
"""

import argparse
import json
import sys
import time
from urllib.parse import urljoin

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
except ImportError:
    print("❌ Selenium not installed. Run: pip install selenium webdriver-manager")
    sys.exit(1)


def make_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


def main():
    parser = argparse.ArgumentParser(description="Scrape JS-heavy sites with Selenium.")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--selector", "-s", default="body", help="CSS selector to extract")
    parser.add_argument("--attr", help="HTML attribute to extract (default: text)")
    parser.add_argument("--wait", type=float, default=3.0, help="Seconds to wait for page load")
    parser.add_argument("--wait-for", help="CSS selector to wait for (defaults to --selector)")
    parser.add_argument("--scroll", type=int, help="Number of scrolls for infinite scroll pages")
    parser.add_argument("--scroll-delay", type=float, default=2.0, help="Delay between scrolls")
    parser.add_argument("--output", "-o", default="-", help="Output file ('-' for stdout)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    parser.add_argument("--visible", action="store_true", help="Show browser window (not headless)")
    args = parser.parse_args()

    driver = make_driver(headless=not args.visible)

    try:
        print(f"🌐 Navigating to: {args.url}", file=sys.stderr)
        driver.get(args.url)

        # Wait for element
        wait_for = args.wait_for or args.selector
        try:
            WebDriverWait(driver, args.wait).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, wait_for))
            )
            print(f"  ✓ Element '{wait_for}' appeared", file=sys.stderr)
        except TimeoutException:
            print(f"  ⚠️  Timeout waiting for '{wait_for}', continuing…", file=sys.stderr)

        # Scroll for infinite scroll
        if args.scroll:
            print(f"  🔃 Scrolling {args.scroll} times…", file=sys.stderr)
            for i in range(args.scroll):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(args.scroll_delay)

        # Extract
        elements = driver.find_elements(By.CSS_SELECTOR, args.selector)
        results = []
        for el in elements:
            if args.attr:
                val = el.get_attribute(args.attr)
                if val and args.attr == "href" and not val.startswith(("http://", "https://", "javascript:")):
                    val = urljoin(args.url, val)
                results.append(val)
            else:
                results.append(el.text)

        # Output
        output = json.dumps(results, indent=2 if args.pretty else None, ensure_ascii=False)
        if args.output == "-":
            print(output)
        else:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"✅ Wrote {len(results)} items to {args.output}", file=sys.stderr)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
