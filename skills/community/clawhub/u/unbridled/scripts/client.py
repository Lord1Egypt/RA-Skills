#!/usr/bin/env python3
"""
Beeper/Matrix client wrapper for Clawd.

Uses the Beeper hungryserv Matrix homeserver via the standard client-server API.
Reads the access token from bbctl's config (~/.config/bbctl/config.json).

Connected networks (bridged in Beeper cloud):
- facebook   (Messenger)
- instagram
- whatsapp
- linkedin
- twitter
(+ discordgo, not logged in yet)

Quick usage:
    python3 client.py whoami
    python3 client.py list-chats --network facebook --limit 20
    python3 client.py list-chats --network whatsapp
    python3 client.py send --room '!abc:beeper.local' --text "hello from clawd"
    python3 client.py history --room '!abc:beeper.local' --limit 10
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any

import urllib.request
import urllib.error

BBCTL_CONFIG = Path.home() / ".config" / "bbctl" / "config.json"


def load_creds() -> dict[str, str]:
    if not BBCTL_CONFIG.exists():
        raise FileNotFoundError(f"bbctl config not found at {BBCTL_CONFIG}. Run `bbctl login`.")
    data = json.loads(BBCTL_CONFIG.read_text())
    env = data["environments"]["prod"]
    username = env["username"]
    return {
        "access_token": env["access_token"],
        "user_id": f"@{username}:beeper.com",
        "homeserver": f"https://matrix.beeper.com/_hungryserv/{username}",
        "device_id": data.get("device_id", ""),
    }


def _req(method: str, url: str, token: str, body: dict | None = None) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code} {e.reason} on {url}\n{body_text}") from None


def get(path: str, token: str, homeserver: str, **params) -> dict:
    url = homeserver + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    return _req("GET", url, token)


def post(path: str, token: str, homeserver: str, body: dict) -> dict:
    url = homeserver + path
    return _req("POST", url, token, body)


def put(path: str, token: str, homeserver: str, body: dict) -> dict:
    url = homeserver + path
    return _req("PUT", url, token, body)


# ---------- high-level helpers ----------

def whoami(creds: dict) -> dict:
    return get("/_matrix/client/v3/account/whoami", creds["access_token"], creds["homeserver"])


def joined_rooms(creds: dict) -> list[str]:
    d = get("/_matrix/client/v3/joined_rooms", creds["access_token"], creds["homeserver"])
    return d.get("joined_rooms", [])


def bridge_info(room_id: str, creds: dict) -> dict | None:
    """Return the m.bridge state event content for a room, or None if not bridged."""
    path = f"/_matrix/client/v3/rooms/{urllib.parse.quote(room_id)}/state/m.bridge"
    try:
        return get(path, creds["access_token"], creds["homeserver"])
    except RuntimeError as e:
        # rooms without a bridge state event (e.g. native Matrix rooms) → 404
        if "404" in str(e):
            return None
        raise


def room_name(room_id: str, creds: dict) -> str | None:
    path = f"/_matrix/client/v3/rooms/{urllib.parse.quote(room_id)}/state/m.room.name"
    try:
        d = get(path, creds["access_token"], creds["homeserver"])
        return d.get("name")
    except RuntimeError as e:
        if "404" in str(e):
            return None
        raise


# Friendly alias → actual bridge name in m.bridge state event
NETWORK_ALIASES = {
    "messenger": "facebookgo",
    "facebook":  "facebookgo",
    "fb":        "facebookgo",
    "instagram": "instagramgo",
    "ig":        "instagramgo",
    "whatsapp":  "whatsapp",
    "wa":        "whatsapp",
    "linkedin":  "linkedin",
    "twitter":   "twitter",
    "x":         "twitter",
    "discord":   "discordgo",
}


def resolve_network(name: str | None) -> str | None:
    if name is None:
        return None
    return NETWORK_ALIASES.get(name.lower(), name.lower())


def list_chats(network: str | None, creds: dict, limit: int = 50) -> list[dict]:
    """Iterate joined rooms, keep only those matching the given bridge network.

    Accepts friendly aliases: messenger/facebook/fb, ig, wa, x, ...
    """
    target = resolve_network(network)
    rooms = joined_rooms(creds)
    results: list[dict] = []
    for rid in rooms:
        info = bridge_info(rid, creds)
        if info is None:
            continue
        bridge = info.get("com.beeper.bridge_name") or info.get("protocol", {}).get("id")
        if target is not None and bridge != target:
            continue
        chan = info.get("channel", {})
        results.append({
            "room_id": rid,
            "network": bridge,
            "name": chan.get("displayname") or room_name(rid, creds),
            "external_id": chan.get("id"),
        })
        if len(results) >= limit:
            break
    return results


def send_message(room_id: str, text: str, creds: dict) -> dict:
    """Send a plain text message. Uses a txn ID based on epoch ms."""
    txn_id = f"clawd-{int(time.time() * 1000)}"
    path = f"/_matrix/client/v3/rooms/{urllib.parse.quote(room_id)}/send/m.room.message/{txn_id}"
    body = {"msgtype": "m.text", "body": text}
    return put(path, creds["access_token"], creds["homeserver"], body)


def history(room_id: str, creds: dict, limit: int = 20) -> list[dict]:
    """Fetch recent messages in a room (latest first)."""
    path = f"/_matrix/client/v3/rooms/{urllib.parse.quote(room_id)}/messages"
    d = get(path, creds["access_token"], creds["homeserver"], dir="b", limit=limit)
    out = []
    for ev in d.get("chunk", []):
        if ev.get("type") != "m.room.message":
            continue
        content = ev.get("content", {})
        out.append({
            "sender": ev.get("sender"),
            "ts": ev.get("origin_server_ts"),
            "body": content.get("body"),
            "msgtype": content.get("msgtype"),
        })
    return out


# ---------- CLI ----------

def main() -> int:
    parser = argparse.ArgumentParser(description="Beeper/Matrix client for Clawd")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami", help="Check credentials")

    p_list = sub.add_parser("list-chats", help="List chats")
    p_list.add_argument("--network", help="facebook, whatsapp, instagram, linkedin, twitter, ...")
    p_list.add_argument("--limit", type=int, default=50)
    p_list.add_argument("--json", action="store_true")

    p_send = sub.add_parser("send", help="Send a message")
    p_send.add_argument("--room", required=True)
    p_send.add_argument("--text", required=True)

    p_hist = sub.add_parser("history", help="Fetch recent messages")
    p_hist.add_argument("--room", required=True)
    p_hist.add_argument("--limit", type=int, default=20)
    p_hist.add_argument("--json", action="store_true")

    args = parser.parse_args()
    creds = load_creds()

    if args.cmd == "whoami":
        d = whoami(creds)
        print(f"user_id:    {d['user_id']}")
        print(f"device_id:  {d.get('device_id', '')}")
        print(f"homeserver: {creds['homeserver']}")
        return 0

    if args.cmd == "list-chats":
        chats = list_chats(args.network, creds, limit=args.limit)
        if args.json:
            print(json.dumps(chats, indent=2, ensure_ascii=False))
        else:
            print(f"{len(chats)} chat(s):")
            for c in chats:
                print(f"  [{c['network']}] {c['name']!r:40} {c['room_id']}")
        return 0

    if args.cmd == "send":
        d = send_message(args.room, args.text, creds)
        print(f"sent event_id: {d.get('event_id')}")
        return 0

    if args.cmd == "history":
        msgs = history(args.room, creds, limit=args.limit)
        if args.json:
            print(json.dumps(msgs, indent=2, ensure_ascii=False, default=str))
        else:
            for m in msgs:
                ts = time.strftime("%Y-%m-%d %H:%M", time.gmtime(m["ts"] / 1000)) if m["ts"] else "?"
                body = (m["body"] or "")[:120]
                print(f"  [{ts}] {m['sender']}: {body}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
