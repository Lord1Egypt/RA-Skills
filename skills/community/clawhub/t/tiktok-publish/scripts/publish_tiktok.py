import os
import sys
import json
import argparse

def load_config(config_path):
    env_key = os.environ.get("TIKTOK_API_KEY") or os.environ.get("TIKTOK_AUTHORIZATION_TOKEN")
    if env_key:
        return {"tiktok": {"api_key": env_key}}

    config_path = os.environ.get("TIKTOK_PUBLISHER_CONFIG", config_path)
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        print("Set TIKTOK_API_KEY or create config.json with tiktok.api_key.")
        sys.exit(1)
    with open(config_path, 'r') as f:
        return json.load(f)

def publish_tiktok(args, config):
    import requests

    api_key = config.get('tiktok', {}).get('api_key') or config.get('tiktok', {}).get('authorization_token')
    if not api_key:
        print("Error: TikTok API key not found in config.json")
        sys.exit(1)

    url = "https://api.mybrandmetrics.com/tiktok/publishing/post"
    
    # Check if source is a URL or a local file
    is_url = args.source.startswith('http://') or args.source.startswith('https://')
    
    headers = {
        "X-API-Key": api_key,
        "X-API_KEY": api_key
    }

    if is_url:
        # Remote URL (JSON)
        headers["Content-Type"] = "application/json"
        data = {
            "title": args.title,
            "video_url": args.source,
            "privacy_level": args.privacy_level,
            "wait_for_published": args.wait_for_published
        }
        response = requests.post(url, headers=headers, json=data)
    else:
        # Local File (Multipart/form-data)
        if not os.path.exists(args.source):
            print(f"Error: Local file not found at {args.source}")
            sys.exit(1)
        
        files = {
            'file': open(args.source, 'rb')
        }
        data = {
            "title": args.title,
            "privacy_level": args.privacy_level,
            "wait_for_published": str(args.wait_for_published).lower()
        }
        if args.poll_interval:
            data["poll_interval_ms"] = str(args.poll_interval)
        if args.poll_timeout:
            data["poll_timeout_ms"] = str(args.poll_timeout)
        
        response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code == 200:
        print("Success! Response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: HTTP {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload video to TikTok via MyBrandMetrics API")
    parser.add_argument("--source", required=True, help="URL or local file path of the video")
    parser.add_argument("--title", required=True, help="Title of the TikTok post")
    parser.add_argument("--privacy-level", default="SELF_ONLY", help="Privacy level (e.g., PUBLIC, SELF_ONLY)")
    parser.add_argument("--wait-for-published", action="store_true", help="Wait for the post to be published")
    parser.add_argument("--poll-interval", type=int, help="Polling interval in ms")
    parser.add_argument("--poll-timeout", type=int, help="Polling timeout in ms")
    parser.add_argument("--config", default="/root/.openclaw/workspace/config.json", help="Path to config.json")

    args = parser.parse_args()
    config = load_config(args.config)
    publish_tiktok(args, config)
