#!/usr/bin/env python3
"""Ring doorbell/camera tool for OpenClaw"""
import asyncio
import json
import sys
import os
from pathlib import Path
from datetime import datetime

TOKEN_FILE = Path.home() / ".openclaw" / "ring_token.json"
SNAPSHOT_DIR = Path.home() / ".openclaw" / "media" / "ring"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

def token_updated(token):
    TOKEN_FILE.write_text(json.dumps(token))

async def authenticate():
    """Authenticate with Ring (first-time setup with 2FA)"""
    from ring_doorbell import Auth, Ring
    from ring_doorbell.const import USER_AGENT, PACKAGE_NAME, __version__
    
    print("Ring Authentication")
    print("===================")
    
    username = input("Enter your Ring email: ").strip()
    password = input("Enter your Ring password: ").strip()
    
    auth = Auth(USER_AGENT, None, token_updated)
    try:
        await auth.async_fetch_token(username, password)
    except Exception as e:
        if "2FA" in str(e) or "verification" in str(e).lower():
            code = input("Enter the 2FA code sent to your email/SMS: ").strip()
            await auth.async_fetch_token(username, password, code)
        else:
            raise
    
    ring = Ring(auth)
    await ring.async_update_data()
    
    print(f"\n✓ Authenticated successfully!")
    print(f"  Token saved to: {TOKEN_FILE}")
    print(f"  Found {len(ring.get_device_list())} devices")
    
    # Save token
    token_updated(auth._token)

async def get_ring():
    from ring_doorbell import Auth, Ring
    from ring_doorbell.const import USER_AGENT
    if not TOKEN_FILE.exists():
        print("ERROR: Ring not authenticated. Run: ring_tool.py auth")
        sys.exit(1)
    auth = Auth(USER_AGENT, json.loads(TOKEN_FILE.read_text()), token_updated)
    ring = Ring(auth)
    await ring.async_update_data()
    return ring

async def list_devices():
    ring = await get_ring()
    devices = []
    for d in ring.get_device_list():
        battery = getattr(d, 'battery_life', None)
        online = getattr(d, 'is_connected', True)
        devices.append({
            "name": d.name,
            "type": type(d).__name__,
            "id": d.id,
            "battery": battery,
            "online": online
        })
    print(json.dumps(devices, ensure_ascii=False, indent=2))

async def get_snapshot(device_name: str):
    import subprocess
    ring = await get_ring()
    device = None
    for d in ring.get_device_list():
        if device_name.lower() in d.name.lower():
            device = d
            break
    if not device:
        print(f"ERROR: Device '{device_name}' not found")
        sys.exit(1)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = device.name.replace(" ", "_")
    out_path = SNAPSHOT_DIR / f"{safe_name}_{ts}.jpg"

    # Try live snapshot first
    img = await device.async_get_snapshot(retries=2)
    if img:
        out_path.write_bytes(img)
        print(json.dumps({"path": str(out_path), "device": device.name}))
        return

    # Fall back to latest recording frame (requires ffmpeg)
    if not hasattr(device, 'async_history'):
        print("ERROR: Device does not support history")
        sys.exit(1)
    history = await device.async_history(limit=1)
    if not history:
        print("ERROR: No history available")
        sys.exit(1)
    event_id = history[0]['id']
    url = await device.async_recording_url(event_id)
    if not url:
        print("ERROR: Could not get recording URL")
        sys.exit(1)
    result = subprocess.run(
        ['ffmpeg', '-y', '-i', url, '-frames:v', '1', '-q:v', '2', str(out_path)],
        capture_output=True, text=True
    )
    if out_path.exists():
        event_time = history[0].get('created_at', '')
        print(json.dumps({"path": str(out_path), "device": device.name, "from_recording": True, "event_time": str(event_time)}))
    else:
        print(f"ERROR: ffmpeg failed: {result.stderr[-200:]}")

async def get_events(device_name: str = None, limit: int = 10):
    ring = await get_ring()
    results = []
    devices = ring.get_device_list()
    for d in devices:
        if device_name and device_name.lower() not in d.name.lower():
            continue
        if not hasattr(d, 'async_history'):
            continue
        try:
            history = await d.async_history(limit=limit)
            for h in history[:limit]:
                results.append({
                    "device": d.name,
                    "kind": h.get("kind", "unknown"),
                    "created_at": h.get("created_at", ""),
                    "duration": h.get("duration", 0),
                    "id": h.get("id", "")
                })
        except Exception as e:
            pass
    results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    print(json.dumps(results[:limit], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ring tool")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("auth", help="Authenticate with Ring (first-time setup)")
    subparsers.add_parser("list", help="List all devices")
    
    snap = subparsers.add_parser("snapshot", help="Get snapshot from camera")
    snap.add_argument("device", help="Device name (partial match ok)")
    
    events = subparsers.add_parser("events", help="Get recent events")
    events.add_argument("--device", help="Filter by device name", default=None)
    events.add_argument("--limit", type=int, default=10)
    
    args = parser.parse_args()
    
    if args.command == "auth":
        asyncio.run(authenticate())
    elif args.command == "list":
        asyncio.run(list_devices())
    elif args.command == "snapshot":
        asyncio.run(get_snapshot(args.device))
    elif args.command == "events":
        asyncio.run(get_events(args.device, args.limit))
    else:
        parser.print_help()
