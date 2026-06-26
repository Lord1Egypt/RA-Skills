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

def check_status(publish_id, config):
    import requests

    api_key = config.get('tiktok', {}).get('api_key') or config.get('tiktok', {}).get('authorization_token')
    if not api_key:
        print("Error: TikTok API key not found in config.json")
        sys.exit(1)

    url = f"https://api.mybrandmetrics.com/tiktok/publishing/status?publish_id={publish_id}"
    
    headers = {
        "X-API-Key": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: HTTP {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check TikTok publishing status")
    parser.add_argument("--publish-id", required=True, help="The publish_id to check")
    parser.add_argument("--config", default="/root/.openclaw/workspace/config.json", help="Path to config.json")

    args = parser.parse_args()
    config = load_config(args.config)
    check_status(args.publish_id, config)
