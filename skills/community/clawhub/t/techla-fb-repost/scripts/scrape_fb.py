#!/usr/bin/env python3
"""
Scrape Facebook post using Apify API.
Usage: python3 scrape_fb.py "<FB_URL>" "<APIFY_TOKEN>"
"""

import sys
import json
import time
import requests

APIFY_TOKEN = sys.argv[2] if len(sys.argv) > 2 else None
FB_URL = sys.argv[1] if len(sys.argv) > 1 else None

if not APIFY_TOKEN or not FB_URL:
    print(json.dumps({"error": "Missing required arguments: FB_URL and APIFY_TOKEN"}))
    sys.exit(1)

ACTOR_ID = "apify~facebook-posts-scraper"
API_BASE = "https://api.apify.com/v2"

def run_actor():
    """Run Apify actor and get dataset items."""
    # Start actor run
    run_url = f"{API_BASE}/acts/{ACTOR_ID}/runs"
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": APIFY_TOKEN,
        "startUrls": [{"url": FB_URL}],
        "maxPosts": 1,
        "waitForFinish": 60  # Wait up to 60 seconds
    }
    
    try:
        response = requests.post(run_url, json=payload, headers=headers, timeout=70)
        response.raise_for_status()
        run_data = response.json()
        
        run_id = run_data["data"]["id"]
        dataset_id = run_data["data"]["defaultDatasetId"]
        
        # Poll for completion
        status_url = f"{API_BASE}/actor-runs/{run_id}"
        for _ in range(30):  # Max 30 attempts
            status_resp = requests.get(f"{status_url}?token={APIFY_TOKEN}", timeout=30)
            status_data = status_resp.json()
            status = status_data["data"]["status"]
            
            if status == "SUCCEEDED":
                break
            elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
                print(json.dumps({"error": f"Actor run failed with status: {status}"}))
                sys.exit(1)
            time.sleep(2)
        
        # Get dataset items
        dataset_url = f"{API_BASE}/datasets/{dataset_id}/items"
        items_resp = requests.get(f"{dataset_url}?token={APIFY_TOKEN}", timeout=30)
        items = items_resp.json()
        
        if not items:
            # Try alternative actor
            return try_alternative_actor()
        
        # Extract relevant fields
        post = items[0]
        result = {
            "text": post.get("text", ""),
            "images": post.get("images", []),
            "video": post.get("videoUrl") or post.get("video", ""),
            "likesCount": post.get("likesCount", 0),
            "commentsCount": post.get("commentsCount", 0),
            "sharesCount": post.get("sharesCount", 0),
            "pageName": post.get("pageName", ""),
            "url": post.get("url", FB_URL),
            "timestamp": post.get("timestamp", "")
        }
        
        print(json.dumps(result, ensure_ascii=False))
        
    except requests.exceptions.Timeout:
        print(json.dumps({"error": "Request timeout - Apify is taking too long"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

def try_alternative_actor():
    """Try alternative Facebook scraper if main fails."""
    alt_actor = "apify~facebook-scraper"
    run_url = f"{API_BASE}/acts/{alt_actor}/runs"
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": APIFY_TOKEN,
        "startUrls": [{"url": FB_URL}],
        "resultsLimit": 1
    }
    
    try:
        response = requests.post(run_url, json=payload, headers=headers, timeout=70)
        response.raise_for_status()
        run_data = response.json()
        
        run_id = run_data["data"]["id"]
        dataset_id = run_data["data"]["defaultDatasetId"]
        
        # Wait and poll
        status_url = f"{API_BASE}/actor-runs/{run_id}"
        for _ in range(30):
            status_resp = requests.get(f"{status_url}?token={APIFY_TOKEN}", timeout=30)
            status_data = status_resp.json()
            if status_data["data"]["status"] == "SUCCEEDED":
                break
            time.sleep(2)
        
        dataset_url = f"{API_BASE}/datasets/{dataset_id}/items"
        items_resp = requests.get(f"{dataset_url}?token={APIFY_TOKEN}", timeout=30)
        items = items_resp.json()
        
        if not items:
            print(json.dumps({"error": "Could not scrape post - may be private or deleted"}))
            sys.exit(1)
        
        post = items[0]
        result = {
            "text": post.get("text", ""),
            "images": post.get("images", []),
            "video": post.get("videoUrl", ""),
            "likesCount": post.get("likes", 0),
            "commentsCount": post.get("comments", 0),
            "sharesCount": post.get("shares", 0),
            "pageName": post.get("page", {}).get("name", ""),
            "url": FB_URL
        }
        print(json.dumps(result, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({"error": f"Alternative actor also failed: {str(e)}"}))
        sys.exit(1)

if __name__ == "__main__":
    run_actor()
