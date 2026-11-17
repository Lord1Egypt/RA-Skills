#!/usr/bin/env python3
"""
WeChat Official Account Draft Publish Script (Generic Version)

Publish a draft from the draft box to all subscribers via freepublish/submit.

Usage:
    python3 publish_draft.py --env ~/.wechat-mp.env --media-id MEDIA_ID

Requirements:
    - curl
    - A .env file with WECHAT_APPID and WECHAT_SECRET
    - The account must be a verified enterprise/organization (freepublish permission)
"""

import json
import subprocess
import sys
import argparse
import os
import time


def load_credentials(env_path):
    """Load WeChat credentials from a .env file."""
    creds = {}
    if not os.path.exists(env_path):
        print(f"ERROR: env file not found: {env_path}")
        sys.exit(1)
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                creds[key.strip()] = value.strip()
    for required in ("WECHAT_APPID", "WECHAT_SECRET"):
        if required not in creds:
            print(f"ERROR: {required} not found in {env_path}")
            sys.exit(1)
    return creds


def get_access_token(appid, secret):
    """Get WeChat access_token. Handle IP whitelist error (40164)."""
    result = subprocess.run(
        [
            "curl", "-s",
            f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}",
        ],
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    if "access_token" not in data:
        errcode = data.get("errcode")
        print(f"ERROR getting access_token: {data}")
        if errcode == 40164:
            ip_result = subprocess.run(
                ["curl", "-s", "https://api.ipify.org"],
                capture_output=True,
                text=True,
            )
            server_ip = ip_result.stdout.strip()
            print(f"\n[IP Whitelist Error]")
            print(f"  Server IP: {server_ip}")
            print(f"  Add this IP to: mp.weixin.qq.com -> Development -> Basic Configuration -> IP Whitelist")
        sys.exit(1)
    return data["access_token"]


def publish_draft(token, media_id):
    """Call freepublish/submit to publish a draft. Returns the API response dict."""
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={token}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"media_id": media_id}),
        ],
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description="Publish a WeChat MP draft to all subscribers")
    parser.add_argument("--env", required=True, help="Path to .env credential file")
    parser.add_argument("--media-id", required=True, help="Draft media_id to publish")
    parser.add_argument("--retries", type=int, default=3, help="Retry count for system errors (default: 3)")
    args = parser.parse_args()

    # Load credentials
    creds = load_credentials(args.env)

    # Get access token
    token = get_access_token(creds["WECHAT_APPID"], creds["WECHAT_SECRET"])

    # Attempt publish with retries for transient system errors
    for attempt in range(1, args.retries + 1):
        print(f"Publishing draft (attempt {attempt}/{args.retries})...")
        result = publish_draft(token, args.media_id)
        errcode = result.get("errcode", 0)

        if errcode == 0:
            publish_id = result.get("publish_id", "")
            print(f"\n[SUCCESS] Draft published!")
            print(f"  media_id:  {args.media_id}")
            print(f"  publish_id: {publish_id}")
            return

        if errcode == -1 and attempt < args.retries:
            # Transient system error — retry with a fresh token
            print(f"  System error (-1), retrying in 3 seconds...")
            time.sleep(3)
            token = get_access_token(creds["WECHAT_APPID"], creds["WECHAT_SECRET"])
            continue

        # Non-retryable error or retries exhausted
        print(f"\n[FAILED] Publish failed: {result}")
        if errcode == 48001:
            print("\n  -> API permission (freepublish) not yet active.")
            print("     This requires a verified enterprise/organization account.")
            print("     Permission activates ~24 hours after verification.")
            print("     Please publish manually:")
            print("       mp.weixin.qq.com -> Draft Box (草稿箱) -> Click Publish (发布)")
        elif errcode == 40007:
            print("\n  -> media_id is invalid. The draft may have been already published or deleted.")
            print("     Check the draft box at mp.weixin.qq.com.")
        elif errcode == -1:
            print(f"\n  -> System error persisted after {args.retries} attempts.")
            print("     This may be a temporary WeChat server issue.")
            print("     Please publish manually from the draft box.")
        else:
            print(f"\n  -> Unknown error code: {errcode}")
            print(f"     errmsg: {result.get('errmsg', 'N/A')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
