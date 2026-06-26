#!/usr/bin/env python3
"""
fetch_reviews.py — Fetch Google Maps review data for a business.

Usage:
    python3 fetch_reviews.py "Business Name City"
    python3 fetch_reviews.py "Business Name City" --json
    python3 fetch_reviews.py "Business Name City" --json --output /path/to/output.json

Scrapes Google Maps search results to extract:
- Business name, rating, review count
- Rating breakdown (if available)
- Recent review texts, authors, ratings, dates

Output: JSON to stdout (--json) or human-readable summary.

Note: This uses Google Maps web scraping. Rate-limit to a few calls per day.
For production use, consider the Google Places API (paid).
"""

import sys
import json
import re
import urllib.request
import urllib.parse
import html
from datetime import datetime, timezone


def fetch_google_maps_page(query: str) -> str:
    """Fetch Google Maps search results page."""
    encoded = urllib.parse.quote(query)
    url = f"https://www.google.com/maps/search/{encoded}"
    
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_rating_and_count(page_text: str) -> dict:
    """Extract rating and review count from page source.
    
    Returns a dict with 'rating' (float or None), 'reviewCount' (int or None), 'name' (str or None).
    Tries multiple regex patterns to handle Google Maps page variations.
    """
    if not page_text or len(page_text) < 100:
        return {"rating": None, "reviewCount": None, "name": None}
    result = {"rating": None, "reviewCount": None, "name": None}
    
    # Try to find rating pattern: X.X stars
    rating_patterns = [
        r'"(\d\.\d)" stars',
        r'(\d\.\d) stars',
        r'"rating":(\d\.?\d?)',
        r'(\d\.\d)\s*\([\d,]+\s*(?:review|avis)',
    ]
    for pattern in rating_patterns:
        m = re.search(pattern, page_text)
        if m:
            result["rating"] = float(m.group(1))
            break
    
    # Try to find review count
    count_patterns = [
        r'(\d[\d,]*)\s*(?:review|avis|rese)',
        r'"userRatingsTotal":(\d+)',
        r'(\d[\d,]*)\s*Google review',
    ]
    for pattern in count_patterns:
        m = re.search(pattern, page_text)
        if m:
            count_str = m.group(1).replace(",", "")
            result["reviewCount"] = int(count_str)
            break
    
    return result


def extract_reviews_from_page(page_text: str) -> list:
    """Extract individual reviews from page data."""
    reviews = []
    
    # Look for review blocks in the page source
    # Google Maps embeds review data in various JSON structures
    review_patterns = [
        # Pattern: review text blocks
        r'\[\[null,null,null,"([^"]{10,500})"',
        r'"snippet":"([^"]{10,500})"',
    ]
    
    texts_found = set()
    for pattern in review_patterns:
        for m in re.finditer(pattern, page_text):
            text = m.group(1)
            text = text.encode().decode('unicode_escape', errors='replace')
            text = html.unescape(text)
            if len(text) > 10 and text not in texts_found:
                texts_found.add(text)
                reviews.append({
                    "text": text,
                    "author": None,
                    "rating": None,
                    "date": None,
                })
    
    return reviews[:20]  # Cap at 20


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_reviews.py 'Business Name City' [--json] [--output path]")
        sys.exit(1)
    
    query = sys.argv[1]
    as_json = "--json" in sys.argv
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
    
    try:
        page = fetch_google_maps_page(query)
    except Exception as e:
        error = {"error": str(e), "query": query}
        if as_json:
            print(json.dumps(error, indent=2))
        else:
            print(f"Error fetching reviews for '{query}': {e}")
        sys.exit(1)
    
    info = extract_rating_and_count(page)
    reviews = extract_reviews_from_page(page)
    
    result = {
        "query": query,
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "rating": info["rating"],
        "reviewCount": info["reviewCount"],
        "reviewsExtracted": len(reviews),
        "reviews": reviews,
    }
    
    if as_json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
        if output_path:
            with open(output_path, "w") as f:
                f.write(output)
            print(f"Written to {output_path}")
        else:
            print(output)
    else:
        print(f"Business: {query}")
        print(f"Rating: {info['rating'] or 'Not found'}")
        print(f"Reviews: {info['reviewCount'] or 'Not found'}")
        print(f"Fetched: {result['fetchedAt']}")
        if reviews:
            print(f"\nExtracted {len(reviews)} review snippets:")
            for i, r in enumerate(reviews[:5], 1):
                text = r['text'][:150] + "..." if len(r['text']) > 150 else r['text']
                print(f"  {i}. {text}")
        else:
            print("\nNo review text extracted (this is normal for initial search — ")
            print("individual reviews require navigating to the reviews panel).")
            print("The agent can use browser automation for deeper extraction.")


if __name__ == "__main__":
    main()
