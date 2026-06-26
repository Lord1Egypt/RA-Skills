#!/usr/bin/env python3
"""
teams-delegate auth via MSAL.
Usage:
  python3 auth.py --client-id YOUR_CLIENT_ID   # first time
  python3 auth.py                               # re-auth/refresh
"""
import json, os, sys, argparse
import msal

TOKEN_DIR   = os.path.expanduser("~/.teams-delegate")
TOKEN_CACHE = os.path.join(TOKEN_DIR, "token_cache.bin")
CONFIG_FILE = os.path.join(TOKEN_DIR, "config.json")
GRAPH_BASE  = "https://graph.microsoft.com/v1.0"

SCOPES = ["Chat.Read","Chat.ReadWrite","ChannelMessage.Read.All",
          "ChannelMessage.Send","Presence.Read.All","User.Read"]

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f: return json.load(f)
    return {}

def save_config(cfg):
    os.makedirs(TOKEN_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f: json.dump(cfg, f, indent=2)

def get_app(client_id):
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE):
        cache.deserialize(open(TOKEN_CACHE).read())
    app = msal.PublicClientApplication(
        client_id,
        authority="https://login.microsoftonline.com/organizations",
        token_cache=cache)
    return app, cache

def save_cache(cache):
    os.makedirs(TOKEN_DIR, exist_ok=True)
    if cache.has_state_changed:
        open(TOKEN_CACHE, "w").write(cache.serialize())

def get_token():
    cfg = load_config()
    client_id = cfg.get("client_id")
    if not client_id:
        print("Run: python3 auth.py --client-id YOUR_CLIENT_ID", file=sys.stderr)
        sys.exit(1)
    app, cache = get_app(client_id)
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            save_cache(cache)
            return result["access_token"]
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        print(f"Device flow failed: {flow.get('error_description')}", file=sys.stderr)
        sys.exit(1)
    print(flow["message"])
    print(f"\nCode expires in {flow.get('expires_in', 900)} seconds — go NOW.")
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        print(f"Auth failed: {result.get('error_description')}", file=sys.stderr)
        sys.exit(1)
    save_cache(cache)
    print("Authentication complete.")
    return result["access_token"]

import urllib.request
def graph_get(path, token):
    req = urllib.request.Request(
        f"{GRAPH_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
    with urllib.request.urlopen(req) as r: return json.loads(r.read())

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--client-id")
    args = p.parse_args()
    if args.client_id:
        cfg = load_config()
        cfg["client_id"] = args.client_id
        save_config(cfg)
        print("Client ID saved.")
    token = get_token()
    try:
        me = graph_get("/me", token)
        print(f"Authenticated as: {me.get('displayName')} ({me.get('mail') or me.get('userPrincipalName')})")
    except Exception as e:
        print(f"Auth successful. /me check: {e}")
