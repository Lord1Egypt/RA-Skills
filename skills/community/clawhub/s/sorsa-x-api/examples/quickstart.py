"""Quickstart: fetch one X/Twitter profile via the Sorsa API.

    export SORSA_API_KEY=your_key   # from https://api.sorsa.io/overview
    python quickstart.py elonmusk
"""

import os
import sys

import requests

username = sys.argv[1] if len(sys.argv) > 1 else "elonmusk"

resp = requests.get(
    "https://api.sorsa.io/v3/info",
    headers={"ApiKey": os.environ["SORSA_API_KEY"]},
    params={"username": username},
    timeout=60,
)
resp.raise_for_status()
u = resp.json()

print(f"@{u['username']} ({u['display_name']})")
print(f"  followers : {u['followers_count']:,}")
print(f"  following : {u['followings_count']:,}")
print(f"  tweets    : {u['tweets_count']:,}")
print(f"  verified  : {u['verified']}")
