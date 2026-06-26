#!/usr/bin/env python3
import sys, json, requests

def main():
    data = json.load(sys.stdin)
    query = data.get("query","")

    r = requests.get(
        "http://localhost:8080/search",
        params={"q": query, "format": "json"},
        timeout=10
    )

    results = []
    for item in r.json().get("results", [])[:5]:
        results.append({
            "title": item.get("title"),
            "url": item.get("url")
        })

    json.dump(results, sys.stdout)

if __name__ == "__main__":
    main()
