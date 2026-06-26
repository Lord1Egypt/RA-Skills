#!/usr/bin/env python3
"""
fetch_reviews_places.py — Fetch Google reviews via Places API (New).

Usage:
    python3 fetch_reviews_places.py "Business Name City"
    python3 fetch_reviews_places.py "Business Name City" --json
    python3 fetch_reviews_places.py "Business Name City" --json --output /path/to/output.json

Uses Google Places API (New) Text Search + Place Details to extract:
- Business name, rating, review count, address, phone
- Up to 5 most recent reviews (API limit)

Requires: GOOGLE_PLACES_API_KEY env var or credentials/google-places-api-key file.
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path


def get_api_key() -> str:
    """Get API key from env var or local credentials file.
    
    Lookup order:
      1. GOOGLE_PLACES_API_KEY environment variable
      2. credentials/google-places-api-key (relative to cwd)
    """
    key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if key:
        return key
    
    # Try local credentials file (relative to working directory)
    cred_path = Path("credentials") / "google-places-api-key"
    if cred_path.exists():
        return cred_path.read_text().strip()
    
    print("Error: No API key found. Set GOOGLE_PLACES_API_KEY env var or create credentials/google-places-api-key", file=sys.stderr)
    sys.exit(1)


def text_search(query: str, api_key: str) -> dict | None:
    """Search for a place by text query. Returns first match."""
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.nationalPhoneNumber,places.websiteUri,places.googleMapsUri"
    }
    body = json.dumps({"textQuery": query}).encode()
    
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            places = data.get("places", [])
            return places[0] if places else None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"Error: Text Search API returned {e.code}: {error_body}", file=sys.stderr)
        return None


def get_place_reviews(place_id: str, api_key: str) -> list:
    """Fetch reviews for a place by ID."""
    url = f"https://places.googleapis.com/v1/{place_id}"
    headers = {
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "reviews"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return data.get("reviews", [])
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"Error: Place Details API returned {e.code}: {error_body}", file=sys.stderr)
        return []


def format_review(review: dict) -> dict:
    """Normalize a Places API review into our standard format."""
    author = review.get("authorAttribution", {})
    return {
        "author": author.get("displayName", "Anonymous"),
        "authorUri": author.get("uri", ""),
        "rating": review.get("rating", 0),
        "text": review.get("text", {}).get("text", ""),
        "relativeTime": review.get("relativePublishTimeDescription", ""),
        "publishTime": review.get("publishTime", ""),
        "language": review.get("text", {}).get("languageCode", "en"),
    }


def fetch_reviews(query: str, api_key: str) -> dict:
    """Full pipeline: search → get details + reviews."""
    result = {
        "query": query,
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "source": "google-places-api",
        "place": None,
        "rating": None,
        "reviewCount": None,
        "reviewsExtracted": 0,
        "reviews": []
    }
    
    # Step 1: Find the place
    place = text_search(query, api_key)
    if not place:
        print(f"No results found for: {query}", file=sys.stderr)
        return result
    
    place_id = place.get("id", "")
    result["place"] = {
        "id": place_id,
        "name": place.get("displayName", {}).get("text", ""),
        "address": place.get("formattedAddress", ""),
        "phone": place.get("nationalPhoneNumber", ""),
        "website": place.get("websiteUri", ""),
        "mapsUrl": place.get("googleMapsUri", ""),
    }
    result["rating"] = place.get("rating")
    result["reviewCount"] = place.get("userRatingCount")
    
    # Step 2: Get reviews
    # The place_id from searchText is just the ID, need full resource name
    resource_name = f"places/{place_id}"
    reviews_raw = get_place_reviews(resource_name, api_key)
    result["reviews"] = [format_review(r) for r in reviews_raw]
    result["reviewsExtracted"] = len(result["reviews"])
    
    return result


def print_human_readable(data: dict):
    """Print a human-readable summary."""
    place = data.get("place")
    if not place:
        print("No business found.")
        return
    
    print(f"\n{'='*60}")
    print(f"  {place['name']}")
    print(f"  {place['address']}")
    if place.get('phone'):
        print(f"  📞 {place['phone']}")
    if place.get('website'):
        print(f"  🌐 {place['website']}")
    print(f"{'='*60}")
    print(f"\n  ⭐ {data['rating']} ({data['reviewCount']} reviews)")
    print(f"  Fetched: {data['fetchedAt']}")
    
    if data["reviews"]:
        print(f"\n  --- Recent Reviews ({data['reviewsExtracted']}) ---\n")
        for i, review in enumerate(data["reviews"], 1):
            stars = "★" * review["rating"] + "☆" * (5 - review["rating"])
            print(f"  {i}. {stars}  by {review['author']} ({review['relativeTime']})")
            text = review["text"]
            if text:
                # Wrap long text
                if len(text) > 200:
                    text = text[:200] + "..."
                print(f"     \"{text}\"")
            print()
    else:
        print("\n  No reviews extracted.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fetch Google reviews via Places API")
    parser.add_argument("query", help="Business search query (e.g., 'Best Coffee Shop Seattle')")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of human-readable")
    parser.add_argument("--output", "-o", help="Write JSON output to file")
    args = parser.parse_args()
    
    api_key = get_api_key()
    data = fetch_reviews(args.query, api_key)
    
    if args.json or args.output:
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(json_str)
            print(f"Written to {args.output}", file=sys.stderr)
        else:
            print(json_str)
    else:
        print_human_readable(data)


if __name__ == "__main__":
    main()
