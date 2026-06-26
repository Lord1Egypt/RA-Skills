#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.parse

# Brave Search API Configuration
# Reads from environment variable BRAVE_API_KEY
API_KEY = os.getenv("BRAVE_API_KEY")
BASE_URL = "https://api.search.brave.com/res/v1/web/search"

def search_brave(query, count=5):
    if not API_KEY:
        return {"error": "Environment variable BRAVE_API_KEY is not set."}
        
    params = urllib.parse.urlencode({"q": query, "count": count})
    url = f"{BASE_URL}?{params}"
    
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": API_KEY
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                results = []
                if "web" in data and "results" in data["web"]:
                    for item in data.get("web", {}).get("results", []):
                        results.append({
                            "title": item.get("title"),
                            "url": item.get("url"),
                            "description": item.get("description")
                        })
                return results
            else:
                return {"error": f"HTTP {response.status}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No query provided"}, indent=2))
        sys.exit(1)
        
    query = " ".join(sys.argv[1:])
    results = search_brave(query)
    print(json.dumps(results, indent=2, ensure_ascii=False))
