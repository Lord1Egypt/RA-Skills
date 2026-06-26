#!/usr/bin/env python3
"""
Places Fetcher

Queries points of interest using goplaces skill or Google Places API.
"""

import argparse
import json
import subprocess
import sys
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch points of interest")
    parser.add_argument("--destinations", required=True, help="Comma-separated cities")
    parser.add_argument("--interests", help="Activity tags (temples,museums,food,shopping)")
    parser.add_argument("--language", default="en", help="Display language")
    parser.add_argument("--output", required=True, help="Output JSON file")
    return parser.parse_args()


def search_places_goplaces(city, query, language):
    """Search places using goplaces CLI"""
    try:
        # Check if GOOGLE_PLACES_API_KEY is set
        if not os.environ.get("GOOGLE_PLACES_API_KEY"):
            print(f"⚠️  GOOGLE_PLACES_API_KEY not set, using fallback data", file=sys.stderr)
            return []
        
        # Call goplaces
        cmd = [
            "goplaces",
            "text-search",
            f"{query} in {city}",
            "--json"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            print(f"⚠️  goplaces failed for {city}/{query}: {result.stderr}", file=sys.stderr)
            return []
        
        data = json.loads(result.stdout)
        places = []
        
        for place in data.get("places", [])[:5]:  # Top 5 results
            places.append({
                "name": place.get("displayName", {}).get("text", ""),
                "name_local": place.get("displayName", {}).get("text", ""),
                "type": query,
                "rating": place.get("rating", 0),
                "address": place.get("formattedAddress", ""),
                "city": city
            })
        
        return places
        
    except Exception as e:
        print(f"⚠️  Error fetching places for {city}/{query}: {e}", file=sys.stderr)
        return []


def get_fallback_places(city, interest):
    """Fallback place data when API is unavailable"""
    fallback_data = {
        "Tokyo": {
            "attractions": [
                {"name": "Tokyo Tower", "name_local": "東京タワー", "type": "landmark", "rating": 4.5},
                {"name": "Senso-ji Temple", "name_local": "浅草寺", "type": "temple", "rating": 4.6},
                {"name": "Shibuya Crossing", "name_local": "渋谷スクランブル交差点", "type": "landmark", "rating": 4.4}
            ],
            "food": [
                {"name": "Tsukiji Outer Market", "name_local": "築地場外市場", "type": "market", "rating": 4.5},
                {"name": "Ramen Street", "name_local": "ラーメンストリート", "type": "restaurant", "rating": 4.3}
            ],
            "temples": [
                {"name": "Senso-ji Temple", "name_local": "浅草寺", "type": "temple", "rating": 4.6},
                {"name": "Meiji Shrine", "name_local": "明治神宮", "type": "shrine", "rating": 4.5}
            ]
        },
        "Osaka": {
            "attractions": [
                {"name": "Osaka Castle", "name_local": "大阪城", "type": "castle", "rating": 4.5},
                {"name": "Dotonbori", "name_local": "道頓堀", "type": "district", "rating": 4.4}
            ],
            "food": [
                {"name": "Kuromon Market", "name_local": "黒門市場", "type": "market", "rating": 4.3},
                {"name": "Takoyaki Dotonbori Kukuru", "name_local": "たこ焼き道頓堀くくる", "type": "restaurant", "rating": 4.4}
            ]
        },
        "Kyoto": {
            "temples": [
                {"name": "Kinkaku-ji", "name_local": "金閣寺", "type": "temple", "rating": 4.6},
                {"name": "Fushimi Inari Shrine", "name_local": "伏見稲荷大社", "type": "shrine", "rating": 4.7}
            ],
            "attractions": [
                {"name": "Arashiyama Bamboo Grove", "name_local": "嵐山竹林", "type": "nature", "rating": 4.5}
            ]
        }
    }
    
    places = fallback_data.get(city, {}).get(interest, [])
    for p in places:
        p["city"] = city
        p["address"] = city
    return places


def main():
    args = parse_args()
    
    cities = [c.strip() for c in args.destinations.split(',')]
    interests = [i.strip() for i in (args.interests or "attractions").split(',')] if args.interests else ["attractions"]
    
    print(f"📍 Fetching places for {len(cities)} cities...")
    
    places_data = {
        "destinations": cities,
        "interests": interests,
        "language": args.language,
        "places": []
    }
    
    use_fallback = not os.environ.get("GOOGLE_PLACES_API_KEY")
    
    for city in cities:
        for interest in interests:
            print(f"   🔍 {city} - {interest}")
            
            if use_fallback:
                results = get_fallback_places(city, interest)
            else:
                results = search_places_goplaces(city, interest, args.language)
                if not results:  # Fallback if API fails
                    results = get_fallback_places(city, interest)
            
            places_data["places"].extend(results)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(places_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Places data saved to: {args.output}")
    print(f"   📊 Total places: {len(places_data['places'])}")
    if use_fallback:
        print(f"   ⚠️  Used fallback data (GOOGLE_PLACES_API_KEY not set)")


if __name__ == "__main__":
    main()
