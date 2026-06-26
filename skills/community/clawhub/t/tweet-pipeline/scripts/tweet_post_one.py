#!/usr/bin/env python3
"""Post a single tweet by Notion page ID. Designed to be called from one-shot crons.

Usage:
  python3 scripts/tweet_post_one.py <notion_page_id>
"""

import sys, os, json, yaml, subprocess, urllib.request, urllib.parse, base64
import hmac, hashlib, time, random, string
from datetime import datetime
from zoneinfo import ZoneInfo

AEST = ZoneInfo("Australia/Sydney")
TWEET_API = "https://api.x.com/2/tweets"


def notion_headers():
    sa = open(os.path.expanduser("~/.config/openclaw/.op-service-token")).read().strip()
    env = {**os.environ, "OP_SERVICE_ACCOUNT_TOKEN": sa}
    key = subprocess.check_output(
        ["op", "read", "op://OpenClaw/Notion API Key/credential"], env=env
    ).decode().strip()
    return {
        "Authorization": f"Bearer {key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }


def get_tweet_text(page_id: str, headers: dict) -> str:
    req = urllib.request.Request(
        f"https://api.notion.com/v1/blocks/{page_id}/children", headers=headers
    )
    blocks = json.loads(urllib.request.urlopen(req).read()).get("results", [])
    parts = []
    for block in blocks:
        if block["type"] == "paragraph":
            for rt in block["paragraph"].get("rich_text", []):
                parts.append(rt.get("plain_text", ""))
    return "\n".join(parts).strip()


def get_page_status(page_id: str, headers: dict) -> str:
    req = urllib.request.Request(
        f"https://api.notion.com/v1/pages/{page_id}", headers=headers
    )
    page = json.loads(urllib.request.urlopen(req).read())
    return page["properties"]["Status"]["select"]["name"]


def update_tweet_status(page_id: str, status: str, headers: dict, tweet_id: str = None):
    props = {"Status": {"select": {"name": status}}}
    if tweet_id:
        props["Tweet ID"] = {"rich_text": [{"text": {"content": tweet_id}}]}
    if status == "Posted":
        props["Posted At"] = {"date": {"start": datetime.now(AEST).isoformat()}}
    data = json.dumps({"properties": props}).encode()
    req = urllib.request.Request(
        f"https://api.notion.com/v1/pages/{page_id}",
        data=data, headers=headers, method="PATCH"
    )
    urllib.request.urlopen(req)


def load_oauth1_creds():
    with open(os.path.expanduser("~/.xurl")) as f:
        d = yaml.safe_load(f)
    oauth1 = d["apps"]["redditech"]["oauth1_token"]["oauth1"]
    return {
        "consumer_key": oauth1["consumer_key"],
        "consumer_secret": oauth1["consumer_secret"],
        "access_token": oauth1["access_token"],
        "token_secret": oauth1["token_secret"],
    }


def oauth1_header(method: str, url: str, creds: dict) -> str:
    nonce = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    ts = str(int(time.time()))
    params = {
        "oauth_consumer_key": creds["consumer_key"],
        "oauth_nonce": nonce,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": ts,
        "oauth_token": creds["access_token"],
        "oauth_version": "1.0",
    }
    param_str = "&".join(f"{urllib.parse.quote(k,'')  }={urllib.parse.quote(v,'')}" for k, v in sorted(params.items()))
    base = "&".join([method.upper(), urllib.parse.quote(url, ''), urllib.parse.quote(param_str, '')])
    signing_key = f"{urllib.parse.quote(creds['consumer_secret'], '')}&{urllib.parse.quote(creds['token_secret'], '')}"
    sig = base64.b64encode(hmac.new(signing_key.encode(), base.encode(), hashlib.sha1).digest()).decode()  # type: ignore
    params["oauth_signature"] = sig
    header = "OAuth " + ", ".join(f'{urllib.parse.quote(k,"")}="{urllib.parse.quote(v,"")}"' for k, v in sorted(params.items()))
    return header


def refresh_twitter_token():
    # OAuth1 doesn't need refresh — kept for compat
    sa = open(os.path.expanduser("~/.config/openclaw/.op-service-token")).read().strip()
    env = {**os.environ, "OP_SERVICE_ACCOUNT_TOKEN": sa}
    client_id = subprocess.check_output(
        ["op", "read", "op://OpenClaw/aennkmzygiq2z63vm7rbpmwn6a/username"], env=env
    ).decode().strip()
    client_secret = subprocess.check_output(
        ["op", "read", "op://OpenClaw/aennkmzygiq2z63vm7rbpmwn6a/credential"], env=env
    ).decode().strip()

    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    body = urllib.parse.urlencode({"grant_type": "refresh_token", "refresh_token": refresh}).encode()
    req = urllib.request.Request("https://api.x.com/2/oauth2/token", data=body, headers={
        "Authorization": f"Basic {basic}",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    tokens = json.loads(urllib.request.urlopen(req).read())
    user["access_token"] = tokens["access_token"]
    if "refresh_token" in tokens:
        user["refresh_token"] = tokens["refresh_token"]
    with open(xurl_path, "w") as f:
        yaml.dump(d, f)
    return tokens["access_token"]


def post_tweet(text: str, creds: dict) -> dict:
    data = json.dumps({"text": text}).encode()
    auth_header = oauth1_header("POST", TWEET_API, creds)
    req = urllib.request.Request(TWEET_API, data=data, headers={
        "Authorization": auth_header,
        "Content-Type": "application/json",
    })
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())


def main():
    if len(sys.argv) < 2:
        print("Usage: tweet_post_one.py <notion_page_id>")
        sys.exit(1)

    page_id = sys.argv[1]
    headers = notion_headers()

    # Safety: only post if still Approved (prevents double-posting if cron fires late)
    status = get_page_status(page_id, headers)
    if status != "Approved":
        print(f"Skipping — status is '{status}', not 'Approved'")
        return

    text = get_tweet_text(page_id, headers)
    if not text:
        print("ERROR: No tweet text found on page")
        update_tweet_status(page_id, "Failed", headers)
        return

    if len(text) > 280:
        print(f"ERROR: {len(text)} chars — over 280 limit")
        update_tweet_status(page_id, "Failed", headers)
        return

    creds = load_oauth1_creds()
    try:
        resp = post_tweet(text, creds)
        tweet_id = resp.get("data", {}).get("id", "unknown")
        print(f"✅ Posted! Tweet ID: {tweet_id}")
        print(f"   https://x.com/redditech/status/{tweet_id}")
        update_tweet_status(page_id, "Posted", headers, tweet_id=tweet_id)
    except Exception as e:
        print(f"❌ Failed: {e}")
        update_tweet_status(page_id, "Failed", headers)


if __name__ == "__main__":
    main()
