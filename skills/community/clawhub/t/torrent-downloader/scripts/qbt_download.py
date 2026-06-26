#!/usr/bin/env python3
"""Push magnet links to qBittorrent for download"""

import sys
import json
import os
import urllib.request
import urllib.parse

# Configuration via environment variables with defaults
QBT_URL = os.environ.get("QBT_URL", "http://localhost:8080")
QBT_USER = os.environ.get("QBT_USER", "admin")
QBT_PASS = os.environ.get("QBT_PASS", "adminadmin")


def login() -> str:
    """Login and return SID cookie."""
    data = urllib.parse.urlencode({"username": QBT_USER, "password": QBT_PASS}).encode()
    req = urllib.request.Request(f"{QBT_URL}/api/v2/auth/login", data=data)
    resp = urllib.request.urlopen(req, timeout=10)
    for header in resp.headers.get_all("Set-Cookie") or []:
        if "SID=" in header:
            return header.split("SID=")[1].split(";")[0]
    body = resp.read().decode()
    if body.strip() == "Ok.":
        pass
    raise RuntimeError(f"Login failed: {body}")


def add_torrent(sid: str, magnet: str, category: str = "", tags: str = "") -> dict:
    """Add a magnet link to qBittorrent."""
    params = {"urls": magnet}
    if category:
        params["category"] = category
    if tags:
        params["tags"] = tags

    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(
        f"{QBT_URL}/api/v2/torrents/add",
        data=data,
        headers={"Cookie": f"SID={sid}"},
    )
    resp = urllib.request.urlopen(req, timeout=10)
    body = resp.read().decode()
    return {"status": "ok" if body.strip() == "Ok." else "error", "response": body.strip()}


def get_torrents(sid: str, sort: str = "added_on", limit: int = 5) -> list:
    """Get recent torrents."""
    req = urllib.request.Request(
        f"{QBT_URL}/api/v2/torrents/info?sort={sort}&reverse=true&limit={limit}",
        headers={"Cookie": f"SID={sid}"},
    )
    resp = urllib.request.urlopen(req, timeout=10)
    return json.loads(resp.read())


def main():
    if len(sys.argv) < 2:
        print("Usage: qbt_download.py <magnet_url> [--category CAT] [--tags TAGS]")
        print("       qbt_download.py --status")
        sys.exit(1)

    try:
        sid = login()
    except Exception:
        # Fallback: try with cookie processor
        data = urllib.parse.urlencode({"username": QBT_USER, "password": QBT_PASS}).encode()
        req = urllib.request.Request(f"{QBT_URL}/api/v2/auth/login", data=data)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
        opener.open(req, timeout=10)

        if sys.argv[1] == "--status":
            req2 = urllib.request.Request(f"{QBT_URL}/api/v2/torrents/info?sort=added_on&reverse=true&limit=5")
            resp2 = opener.open(req2, timeout=10)
            torrents = json.loads(resp2.read())
            for t in torrents:
                progress = t.get("progress", 0) * 100
                state = t.get("state", "unknown")
                name = t.get("name", "?")
                size_gb = t.get("size", 0) / 1024**3
                print(f"  [{state}] {name[:50]} | {size_gb:.1f}GB | {progress:.0f}%")
            sys.exit(0)

        magnet = sys.argv[1]
        params = {"urls": magnet}
        data2 = urllib.parse.urlencode(params).encode()
        req2 = urllib.request.Request(f"{QBT_URL}/api/v2/torrents/add", data=data2)
        resp2 = opener.open(req2, timeout=10)
        body = resp2.read().decode()
        print(json.dumps({"status": "ok" if body.strip() == "Ok." else "error", "response": body.strip()}))
        sys.exit(0)

    if sys.argv[1] == "--status":
        torrents = get_torrents(sid)
        for t in torrents:
            progress = t.get("progress", 0) * 100
            state = t.get("state", "unknown")
            name = t.get("name", "?")
            size_gb = t.get("size", 0) / 1024**3
            dlspeed = t.get("dlspeed", 0) / 1024 / 1024
            print(f"  [{state}] {name[:50]} | {size_gb:.1f}GB | {progress:.0f}% | {dlspeed:.1f}MB/s")
        sys.exit(0)

    magnet = sys.argv[1]
    category = ""
    tags = ""
    for i, arg in enumerate(sys.argv):
        if arg == "--category" and i + 1 < len(sys.argv):
            category = sys.argv[i + 1]
        if arg == "--tags" and i + 1 < len(sys.argv):
            tags = sys.argv[i + 1]

    result = add_torrent(sid, magnet, category, tags)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
