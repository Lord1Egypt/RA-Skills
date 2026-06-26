#!/usr/bin/env python3
"""
Daily collection from Beeper-bridged networks: Messenger, WhatsApp, LinkedIn,
Instagram, Twitter DMs.

Uses the existing Matrix client wrapper (`scripts/beeper/client.py`) to list
chats per network. For each chat with recent activity, fetches the last N
events via the homeserver messages endpoint. Since Beeper enforces E2EE,
message BODIES are encrypted on the wire. To decrypt, we use matrix-nio
from the beeper venv when available; otherwise we only report activity
metadata (sender, timestamp, event type).

Output: /tmp/recap/collect-beeper-YYYY-MM-DD.md

Usage:
    python3 collect_beeper_daily.py [--hours 24] [--networks messenger,whatsapp,linkedin]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BBCTL_CFG = Path.home() / ".config" / "bbctl" / "config.json"
NIO_PY = Path.home() / ".venvs" / "beeper" / "bin" / "python"
CLIENT_PY = Path(__file__).with_name("client.py")
NIO_CLIENT_PY = Path(__file__).with_name("nio_client.py")

NETWORK_LABELS = {
    "messenger": "Facebook Messenger",
    "whatsapp":  "WhatsApp",
    "linkedin":  "LinkedIn",
    "instagram": "Instagram",
    "twitter":   "Twitter/X DMs",
}


def load_creds():
    data = json.loads(BBCTL_CFG.read_text())
    env = data["environments"]["prod"]
    return {
        "token": env["access_token"],
        "user_id": f"@{env['username']}:beeper.com",
        "homeserver": f"https://matrix.beeper.com/_hungryserv/{env['username']}",
    }


def api(path, creds, method="GET", body=None):
    url = creds["homeserver"] + path
    headers = {"Authorization": f"Bearer {creds['token']}"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def list_chats_for_network(network: str, limit: int = 300) -> list[dict]:
    """Call the client.py CLI to list chats (already handles bridge state)."""
    out = subprocess.check_output([
        sys.executable,  # regular python3 is fine for client.py (no e2ee)
        str(CLIENT_PY),
        "list-chats",
        "--network", network,
        "--limit", str(limit),
        "--json",
    ], timeout=600)
    return json.loads(out)


def recent_messages(room_id: str, creds: dict, limit: int = 20) -> list[dict]:
    """Fetch the last `limit` events from a room (newest first). Encrypted
    bodies remain encrypted; we still get ts, sender, event type, and
    send status events."""
    path = f"/_matrix/client/v3/rooms/{urllib.parse.quote(room_id)}/messages?dir=b&limit={limit}"
    d = api(path, creds)
    return d.get("chunk", [])


def get_room_name(room_id: str, creds: dict) -> str | None:
    try:
        d = api(
            f"/_matrix/client/v3/rooms/{urllib.parse.quote(room_id)}/state/m.room.name",
            creds,
        )
        return d.get("name")
    except Exception:
        return None


def get_members(room_id: str, creds: dict) -> list[str]:
    """Returns display names of the bridge puppets (real people) in the room."""
    try:
        d = api(
            f"/_matrix/client/v3/rooms/{urllib.parse.quote(room_id)}/joined_members",
            creds,
        )
        names = []
        for uid, info in d.get("joined", {}).items():
            # skip our own user + bridge bots
            if uid.startswith("@jkobject"):
                continue
            if "bot:" in uid:
                continue
            name = info.get("display_name") or info.get("displayname")
            if name:
                names.append(name)
        return names
    except Exception:
        return []


def try_decrypt_batch(room_id: str, limit: int = 20) -> list[dict] | None:
    """Best-effort: call nio_client.py history --json. May return empty/partial
    on first decrypt if group sessions aren't available yet."""
    if not NIO_PY.exists() or not NIO_CLIENT_PY.exists():
        return None
    try:
        out = subprocess.check_output([
            str(NIO_PY), str(NIO_CLIENT_PY),
            "history", "--room", room_id, "--limit", str(limit), "--json",
        ], timeout=120, stderr=subprocess.DEVNULL)
        return json.loads(out) if out.strip() else []
    except Exception:
        return None


def collect_network(network: str, hours: int, creds: dict, chats_limit: int, per_chat: int) -> str:
    label = NETWORK_LABELS.get(network, network)
    lines = [f"## {label}", ""]

    try:
        chats = list_chats_for_network(network, limit=chats_limit)
    except Exception as e:
        lines.append(f"⚠️ list-chats failed: {e}")
        lines.append("")
        return "\n".join(lines)

    if not chats:
        lines.append("_(no chats found)_")
        lines.append("")
        return "\n".join(lines)

    cutoff = (time.time() - hours * 3600) * 1000  # ms since epoch
    actives = []

    for c in chats:
        rid = c["room_id"]
        try:
            msgs = recent_messages(rid, creds, limit=per_chat)
        except Exception:
            continue
        # Filter to recent human-originated events (not bridge meta)
        recent = [
            e for e in msgs
            if e.get("origin_server_ts", 0) >= cutoff
            and e.get("type") in ("m.room.encrypted", "m.room.message")
        ]
        if not recent:
            continue
        # Determine counterparty
        name = c.get("name")
        if not name:
            members = get_members(rid, creds)
            if members:
                name = ", ".join(members[:3])
                if len(members) > 3:
                    name += f" (+{len(members) - 3} others)"
            else:
                name = "(unknown)"
        actives.append({
            "room_id": rid,
            "name": name,
            "count": len(recent),
            "last_ts": max(e["origin_server_ts"] for e in recent),
            "events": recent,
        })

    # Sort by activity
    actives.sort(key=lambda x: x["last_ts"], reverse=True)

    if not actives:
        lines.append(f"_(no activity in the last {hours}h)_")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"**{len(actives)} chat(s) active in the last {hours}h** — most recent first:")
    lines.append("")

    for a in actives:
        ts = time.strftime("%H:%M", time.gmtime(a["last_ts"] / 1000))
        lines.append(f"### {a['name']}  ({a['count']} msg, last @ {ts} UTC)")
        lines.append(f"- room: `{a['room_id']}`")

        # Try to decrypt a handful (may fail silently for old events)
        # `count` is the number of recent encrypted/message events seen via raw Matrix.
        # With very small counts (e.g. 1), asking nio history for `limit=1` can miss the
        # actual text message because the newest event may be bridge/meta noise. Always
        # over-fetch a small window for decryption.
        decrypted = try_decrypt_batch(a["room_id"], limit=max(10, min(a["count"] * 4, 20)))
        if decrypted:
            shown = 0
            for m in decrypted[:10]:
                body = (m.get("body") or "").strip()
                if not body or "[encrypted" in body:
                    continue
                sender = m.get("sender", "?").split(":")[0].lstrip("@")
                ts2 = time.strftime("%H:%M", time.gmtime(m.get("ts", 0) / 1000))
                lines.append(f"  - [{ts2}] **{sender}**: {body[:200]}")
                shown += 1
            if shown == 0:
                lines.append(f"  - _(activity detected but messages not decryptable yet — open Beeper to load keys)_")
        else:
            lines.append(f"  - _(activity detected, decryption unavailable)_")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily Beeper collection")
    parser.add_argument("--hours", type=int, default=24, help="Lookback window in hours")
    parser.add_argument("--networks", default="messenger,whatsapp,linkedin",
                        help="Comma-separated list")
    parser.add_argument("--chats-limit", type=int, default=300,
                        help="Max chats to scan per network")
    parser.add_argument("--per-chat", type=int, default=15,
                        help="Events to fetch per chat")
    parser.add_argument("--output", help="Output file path (default /tmp/recap/collect-beeper-YYYY-MM-DD.md)")
    args = parser.parse_args()

    creds = load_creds()
    today = dt.date.today().isoformat()
    out_path = Path(args.output) if args.output else Path(f"/tmp/recap/collect-beeper-{today}.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    parts = [
        f"# Beeper — {today}",
        f"_generated at {now}, lookback {args.hours}h_",
        "",
        f"Networks: {args.networks}",
        "",
    ]

    for net in [n.strip() for n in args.networks.split(",") if n.strip()]:
        print(f"[collect-beeper] {net}...", file=sys.stderr)
        parts.append(collect_network(net, args.hours, creds, args.chats_limit, args.per_chat))

    out_path.write_text("\n".join(parts))
    print(f"✓ wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
