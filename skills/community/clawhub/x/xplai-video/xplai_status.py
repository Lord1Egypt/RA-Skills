#!/usr/bin/env python3

import argparse
import http.client
import json
import sys
import debug_utils
from urllib.parse import urlencode

API_BASE_URL = "https://eagle-api.xplai.ai"
API_ENDPOINT = "/api/solve/video_status_mcp"


def query_video_status(video_id):
    url = f"{API_BASE_URL}{API_ENDPOINT}"
    params = {"video_id": video_id}

    debug_utils.log_request("GET", url, params=params)

    try:
        conn = http.client.HTTPSConnection("eagle-api.xplai.ai", timeout=30)
        query_string = urlencode(params)
        full_url = f"{API_ENDPOINT}?{query_string}"
        headers = {"Content-Type": "application/json"}
        conn.request("GET", full_url, headers=headers)
        response = conn.getresponse()
        response_body = response.read().decode("utf-8")
        
        if response.status >= 400:
            print(f"HTTP Error: {response.status} {response.reason}", file=sys.stderr)
            sys.exit(1)
        
        debug_utils.log_response(response, response_body)
        
        result = json.loads(response_body)
        conn.close()

        if result.get("code") == 0:
            data = result.get("data", {})
            card = data.get("card", {})
            
            status = card.get("status")
            video_url = card.get("video_url")
            
            print(f"Video ID: {data.get('video_id')}")
            print(f"Title: {card.get('title')}")
            print(f"Subject: {card.get('subject')}")
            print(f"Status: {status}")
            
            if video_url and status == "v_succ":
                print(f"Video URL: {video_url}")
                print(f"Xplai web page URL: https://www.xplai.ai/#/video/{video_id}")
            elif status == "v_fail":
                print("Video generation failed")
            else:
                print(f"Queue Index: {data.get('queue_index', 'N/A')}")
                print("Video is still processing...")
            
            return status
        else:
            print(f"Error: {result.get('msg')}", file=sys.stderr)
            sys.exit(1)
    except (http.client.HTTPException, OSError) as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query video generation status from xplai API")
    parser.add_argument("video_id", type=str, help="Video ID to query")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode to print request/response details")

    args = parser.parse_args()

    debug_utils.set_debug(args.debug)

    query_video_status(args.video_id)


if __name__ == "__main__":
    main()
