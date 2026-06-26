#!/usr/bin/env python3
"""
Shared Apify REST API client helpers.
Uses urllib directly and does not depend on the apify-client SDK.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import urllib.parse

API_BASE = "https://api.apify.com/v2"

# Actor ID mapping
ACTORS = {
    "tiktok": "clockworks/tiktok-scraper",
    "instagram": "apify/instagram-scraper",
    "twitter": "apidojo/tweet-scraper",
    "twitter_unlimited": "apidojo/twitter-scraper-lite",
    "youtube": "streamers/youtube-scraper",
}


def get_token():
    """Read APIFY_TOKEN from the environment."""
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        print("Error: APIFY_TOKEN environment variable not set.", file=sys.stderr)
        print("Set it with: export APIFY_TOKEN='apify_api_xxx'", file=sys.stderr)
        sys.exit(1)
    return token


def _request(method, url, data=None, token=None):
    """Execute an HTTP request and return parsed JSON."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def run_actor(actor_key, run_input, timeout_secs=300):
    """
    Start an Apify actor run, wait for completion, and return dataset items.

    Args:
        actor_key: key in ACTORS or a full actor ID such as "clockworks/tiktok-scraper"
        run_input: actor input payload
        timeout_secs: maximum wait time in seconds, default 300

    Returns:
        list: dataset items
    """
    token = get_token()
    actor_id = ACTORS.get(actor_key, actor_key)
    encoded_id = urllib.parse.quote(actor_id, safe="")

    # Start the run.
    start_url = f"{API_BASE}/acts/{encoded_id}/runs?token={token}"
    run_data = _request("POST", start_url, data=run_input)
    run_id = run_data["data"]["id"]
    dataset_id = run_data["data"]["defaultDatasetId"]

    print(f"Actor run started: {run_id}", file=sys.stderr)

    # Poll until the run finishes.
    poll_url = f"{API_BASE}/actor-runs/{run_id}?token={token}"
    elapsed = 0
    poll_interval = 3

    while elapsed < timeout_secs:
        time.sleep(poll_interval)
        elapsed += poll_interval
        status_data = _request("GET", poll_url)
        status = status_data["data"]["status"]

        if status in ("SUCCEEDED",):
            break
        elif status in ("FAILED", "ABORTED", "TIMED-OUT"):
            print(f"Actor run {status}: {run_id}", file=sys.stderr)
            # Try to read any partial data that may already exist.
            break

        # Increase the polling interval gradually.
        if elapsed > 30:
            poll_interval = 10
        elif elapsed > 10:
            poll_interval = 5

    # Fetch dataset items.
    items_url = f"{API_BASE}/datasets/{dataset_id}/items?format=json&token={token}"
    items = _request("GET", items_url)

    if isinstance(items, list):
        return items
    elif isinstance(items, dict) and "items" in items:
        return items["items"]
    return items


def run_actor_sync(actor_key, run_input, timeout_secs=300):
    """
    Run an Apify actor through the sync API and return items directly.
    Best for smaller jobs where polling is unnecessary.

    Args:
        actor_key: key in ACTORS
        run_input: actor input payload
        timeout_secs: timeout in seconds

    Returns:
        list: dataset items
    """
    token = get_token()
    actor_id = ACTORS.get(actor_key, actor_key)
    encoded_id = urllib.parse.quote(actor_id, safe="")

    url = f"{API_BASE}/acts/{encoded_id}/run-sync-get-dataset-items?token={token}&timeout={timeout_secs}"
    items = _request("POST", url, data=run_input)

    if isinstance(items, list):
        return items
    elif isinstance(items, dict) and "items" in items:
        return items["items"]
    return items if items else []
