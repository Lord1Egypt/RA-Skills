"""Search tweets and page through results using next_cursor.

    export SORSA_API_KEY=your_key
    python search_with_pagination.py "from:elonmusk min_faves:5000"
"""

import os
import sys

import requests

QUERY = sys.argv[1] if len(sys.argv) > 1 else "ethereum"
MAX_PAGES = 3
API_KEY = os.environ["SORSA_API_KEY"]
URL = "https://api.sorsa.io/v3/search-tweets"

cursor = None
seen = 0

for _ in range(MAX_PAGES):
    body = {"query": QUERY, "order": "latest"}
    if cursor:
        body["next_cursor"] = cursor

    resp = requests.post(
        URL,
        headers={"ApiKey": API_KEY, "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()

    for t in data.get("tweets", []):
        seen += 1
        text = t["full_text"].replace("\n", " ")[:80]
        print(f"[{t['created_at']}] @{t['user']['username']}: {text}")

    cursor = data.get("next_cursor")
    if not cursor:
        break

print(f"\nTotal tweets: {seen}")
