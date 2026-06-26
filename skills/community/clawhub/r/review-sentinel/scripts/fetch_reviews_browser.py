#!/usr/bin/env python3
"""
fetch_reviews_browser.py — Browser-assisted review fetcher.

This script is designed to be called by the OpenClaw agent, which will use
its browser automation capability to navigate Google Maps and extract reviews.

This script processes the raw page content after the agent captures it.

Usage:
    # The agent captures page HTML via browser tool, saves to a temp file
    python3 fetch_reviews_browser.py --parse /tmp/reviews_page.html --output state/business.json
    
    # Or: generate the URL to visit
    python3 fetch_reviews_browser.py --url "Best Coffee Shop Seattle"
"""

import sys
import json
import re
import html
from datetime import datetime, timezone


def generate_maps_url(query: str) -> str:
    """Generate a Google Maps search URL."""
    import urllib.parse
    encoded = urllib.parse.quote(query)
    return f"https://www.google.com/maps/search/{encoded}"


def parse_reviews_html(html_content: str) -> dict:
    """Parse review data from saved Google Maps HTML."""
    result = {
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "rating": None,
        "reviewCount": None,
        "reviews": [],
    }
    
    # Extract rating
    for pattern in [r'(\d\.\d)\s*stars?', r'"(\d\.\d)".*?stars?']:
        m = re.search(pattern, html_content, re.IGNORECASE)
        if m:
            result["rating"] = float(m.group(1))
            break
    
    # Extract review count
    for pattern in [r'([\d,]+)\s*reviews?', r'([\d,]+)\s*Google reviews?']:
        m = re.search(pattern, html_content, re.IGNORECASE)
        if m:
            result["reviewCount"] = int(m.group(1).replace(",", ""))
            break
    
    # Extract review blocks — look for common patterns in Maps HTML
    # These patterns work on the rendered DOM that the agent captures
    review_blocks = re.findall(
        r'class="[^"]*review[^"]*"[^>]*>.*?(?=class="[^"]*review[^"]*"|$)',
        html_content, re.DOTALL | re.IGNORECASE
    )
    
    for block in review_blocks[:20]:
        review = {"author": None, "rating": None, "text": None, "date": None}
        
        # Author name
        author_m = re.search(r'aria-label="([^"]+)".*?photo', block)
        if author_m:
            review["author"] = author_m.group(1)
        
        # Star rating
        star_m = re.search(r'(\d)\s*star', block, re.IGNORECASE)
        if star_m:
            review["rating"] = int(star_m.group(1))
        
        # Review text
        text_m = re.search(r'class="[^"]*text[^"]*"[^>]*>([^<]+)', block)
        if text_m:
            review["text"] = html.unescape(text_m.group(1).strip())
        
        # Date
        date_m = re.search(r'(\d+\s*(?:day|week|month|year)s?\s*ago)', block, re.IGNORECASE)
        if date_m:
            review["date"] = date_m.group(1)
        
        if review["text"] and len(review["text"]) > 5:
            result["reviews"].append(review)
    
    return result


def main():
    if "--url" in sys.argv:
        idx = sys.argv.index("--url")
        if idx + 1 < len(sys.argv):
            print(generate_maps_url(sys.argv[idx + 1]))
        else:
            print("Error: --url requires a search query", file=sys.stderr)
            sys.exit(1)
    
    elif "--parse" in sys.argv:
        idx = sys.argv.index("--parse")
        if idx + 1 >= len(sys.argv):
            print("Error: --parse requires a file path", file=sys.stderr)
            sys.exit(1)
        
        filepath = sys.argv[idx + 1]
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        result = parse_reviews_html(content)
        
        output_path = None
        if "--output" in sys.argv:
            oidx = sys.argv.index("--output")
            if oidx + 1 < len(sys.argv):
                output_path = sys.argv[oidx + 1]
        
        output = json.dumps(result, indent=2, ensure_ascii=False)
        if output_path:
            with open(output_path, "w") as f:
                f.write(output)
            print(f"Parsed {len(result['reviews'])} reviews → {output_path}")
        else:
            print(output)
    
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
