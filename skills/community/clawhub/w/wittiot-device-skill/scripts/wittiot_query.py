#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WittIoT weather station query skill.

Supported actions:
  devices   — list all devices bound to the account
  realtime  — get real-time sensor readings for a device
  history   — get historical data for a device
  shortcode — get public data by shortcode (no auth needed)

Auth: WITTIOT_API_KEY env var, or --api-key arg, or config.json
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
from typing import Any, Dict, List, Optional

BASE_URL = "https://wittiot.com"

WIND_DIR_LABELS = {
    (0, 22): "N", (22, 67): "NE", (67, 112): "E", (112, 157): "SE",
    (157, 202): "S", (202, 247): "SW", (247, 292): "W", (292, 337): "NW", (337, 360): "N",
}


def deep_get(data: Any, path: str) -> Any:
    cur = data
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def http_request(
    method: str,
    url: str,
    headers: Dict[str, str] = None,
    payload: Dict[str, Any] = None,
) -> Dict[str, Any]:
    headers = headers or {}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body)
        except Exception:
            raise SystemExit(f"HTTP {e.code}: {body[:200]}")


def load_config() -> Dict[str, Any]:
    path = os.path.join(os.getcwd(), "config.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def resolve_api_key(cfg: Dict[str, Any], arg_key: Optional[str]) -> Optional[str]:
    if arg_key:
        return arg_key
    env_key = os.getenv("WITTIOT_API_KEY")
    if env_key:
        return env_key
    return cfg.get("apiKey")


def make_headers(api_key: Optional[str]) -> Dict[str, str]:
    headers: Dict[str, str] = {"Accept": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    return headers


def wind_direction_label(degrees: Optional[float]) -> str:
    if degrees is None:
        return "unknown"
    d = float(degrees) % 360
    for (lo, hi), label in WIND_DIR_LABELS.items():
        if lo <= d < hi:
            return label
    return "N"


def format_sensor_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format raw sensor data into human-readable output."""
    out: Dict[str, Any] = {}
    if data.get("temperature") is not None:
        out["temperature"] = f"{data['temperature']} °C"
    if data.get("humidity") is not None:
        out["humidity"] = f"{data['humidity']} %"
    if data.get("pressure") is not None:
        out["pressure"] = f"{data['pressure']} hPa"
    if data.get("light") is not None:
        out["light"] = f"{data['light']} Klux"
    if data.get("wind_speed") is not None:
        out["wind_speed"] = f"{data['wind_speed']} m/s"
    if data.get("wind_gust") is not None:
        out["wind_gust"] = f"{data['wind_gust']} m/s"
    if data.get("wind_direction") is not None:
        label = wind_direction_label(data["wind_direction"])
        out["wind_direction"] = f"{data['wind_direction']}° ({label})"
    if data.get("rainfall") is not None:
        out["rainfall"] = f"{data['rainfall']} mm"
    return out


# ─────────────────────────────── actions ────────────────────────────────

def action_devices(api_key: str) -> None:
    url = f"{BASE_URL}/api/v1.Device/index"
    resp = http_request("GET", url, headers=make_headers(api_key))
    if resp.get("code") != 200:
        print(json.dumps({"error": resp.get("msg", "Unknown error"), "code": resp.get("code")}, ensure_ascii=False))
        sys.exit(2)
    devices: List[Dict] = resp.get("data", [])
    if not devices:
        print(json.dumps({"devices": [], "message": "No devices found"}, ensure_ascii=False))
        return
    out = []
    for d in devices:
        out.append({
            "id": d.get("id"),
            "name": d.get("name"),
            "model": d.get("model"),
            "sn": d.get("sn"),
            "online": d.get("online"),
            "visibility": d.get("visibility"),
        })
    print(json.dumps({"devices": out}, ensure_ascii=False))


def action_realtime(api_key: str, device_id: Optional[int], device_name: Optional[str], devices_cache: Optional[List] = None) -> None:
    # Resolve device_id from name if needed
    if device_id is None and device_name:
        if devices_cache is None:
            url = f"{BASE_URL}/api/v1.Device/index"
            resp = http_request("GET", url, headers=make_headers(api_key))
            if resp.get("code") != 200:
                print(json.dumps({"error": resp.get("msg", "Failed to list devices")}, ensure_ascii=False))
                sys.exit(2)
            devices_cache = resp.get("data", [])
        matched = [d for d in devices_cache if d.get("name") == device_name]
        if not matched:
            names = [d.get("name") for d in devices_cache]
            print(json.dumps({"error": f"Device '{device_name}' not found", "available": names}, ensure_ascii=False))
            sys.exit(4)
        if len(matched) > 1:
            print(json.dumps({"choose_device": [{"id": d["id"], "name": d["name"]} for d in matched]}, ensure_ascii=False))
            sys.exit(3)
        device_id = matched[0]["id"]

    if device_id is None:
        # No device specified — if only one device exists, auto-select
        url = f"{BASE_URL}/api/v1.Device/index"
        resp = http_request("GET", url, headers=make_headers(api_key))
        devices_list = resp.get("data", [])
        if len(devices_list) == 0:
            print(json.dumps({"error": "No devices found"}, ensure_ascii=False))
            sys.exit(2)
        if len(devices_list) > 1:
            print(json.dumps({"choose_device": [{"id": d["id"], "name": d["name"]} for d in devices_list]}, ensure_ascii=False))
            sys.exit(3)
        device_id = devices_list[0]["id"]

    url = f"{BASE_URL}/api/v1.Realtime/index?id={device_id}"
    resp = http_request("GET", url, headers=make_headers(api_key))
    if resp.get("code") != 200:
        print(json.dumps({"error": resp.get("msg", "Unknown error"), "code": resp.get("code")}, ensure_ascii=False))
        sys.exit(2)
    payload = resp.get("data", {})
    sensor_raw = payload.get("data") or {}
    output = {
        "device_id": device_id,
        "device_name": payload.get("device_name"),
        "online": payload.get("online"),
        "sensors": format_sensor_data(sensor_raw),
        "_raw": sensor_raw,
    }
    print(json.dumps(output, ensure_ascii=False))


def action_history(api_key: str, device_id: Optional[int], device_name: Optional[str], range_: str) -> None:
    # Resolve device_id
    if device_id is None and device_name:
        url = f"{BASE_URL}/api/v1.Device/index"
        resp = http_request("GET", url, headers=make_headers(api_key))
        devices_list = resp.get("data", [])
        matched = [d for d in devices_list if d.get("name") == device_name]
        if not matched:
            print(json.dumps({"error": f"Device '{device_name}' not found", "available": [d["name"] for d in devices_list]}, ensure_ascii=False))
            sys.exit(4)
        device_id = matched[0]["id"]

    if device_id is None:
        print(json.dumps({"error": "Provide --device-id or --device-name"}, ensure_ascii=False))
        sys.exit(2)

    url = f"{BASE_URL}/api/v1.History/index?id={device_id}&range={range_}"
    resp = http_request("GET", url, headers=make_headers(api_key))
    if resp.get("code") != 200:
        print(json.dumps({"error": resp.get("msg", "Unknown error"), "code": resp.get("code")}, ensure_ascii=False))
        sys.exit(2)
    points = resp.get("data", [])
    print(json.dumps({"device_id": device_id, "range": range_, "count": len(points), "data": points}, ensure_ascii=False))


def action_shortcode(code: str) -> None:
    # Step 1: verify shortcode exists
    url = f"{BASE_URL}/api/v1.Shortcode/read?code={urllib.parse.quote(code)}"
    resp = http_request("GET", url, headers={"Accept": "application/json"})
    if resp.get("code") != 200:
        print(json.dumps({"error": "Shortcode not found or device is private", "code": resp.get("code")}, ensure_ascii=False))
        sys.exit(4)
    device_info = resp.get("data", {}).get("device", {})
    online = resp.get("data", {}).get("online", False)

    # Step 2: get public sensor data
    data_url = f"{BASE_URL}/api/v1.Shortcode/data?code={urllib.parse.quote(code)}"
    data_resp = http_request("GET", data_url, headers={"Accept": "application/json"})
    sensor_raw = {}
    if data_resp.get("code") == 200:
        sensor_raw = data_resp.get("data", {}).get("data") or {}

    output = {
        "shortcode": code,
        "device_name": device_info.get("name"),
        "model": device_info.get("model"),
        "online": online,
        "sensors": format_sensor_data(sensor_raw),
        "_raw": sensor_raw,
    }
    print(json.dumps(output, ensure_ascii=False))


# ─────────────────────────────── main ───────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="WittIoT weather station query skill.")
    parser.add_argument("--action", choices=["devices", "realtime", "history", "shortcode"],
                        default="realtime", help="Action to perform (default: realtime)")
    parser.add_argument("--api-key", default=None, help="WittIoT API Key (witt_sk_xxxx)")
    parser.add_argument("--device-id", type=int, default=None, help="Device ID")
    parser.add_argument("--device-name", default=None, help="Device name (partial match not supported)")
    parser.add_argument("--range", dest="range_", default="24h", choices=["24h", "7d", "30d"],
                        help="History range (default: 24h)")
    parser.add_argument("--code", default=None, help="Shortcode (6-char, for --action shortcode)")
    args = parser.parse_args()

    cfg = load_config()
    api_key = resolve_api_key(cfg, args.api_key)

    if args.action == "shortcode":
        if not args.code:
            print(json.dumps({"error": "Provide --code for shortcode action"}, ensure_ascii=False))
            sys.exit(2)
        action_shortcode(args.code)
        return

    # All other actions require auth
    if not api_key:
        print(json.dumps({
            "error": "Missing API key. Set WITTIOT_API_KEY env var, pass --api-key, or add to config.json",
            "hint": "Get your API key at https://wittiot.com/index/apikey"
        }, ensure_ascii=False))
        sys.exit(2)

    if args.action == "devices":
        action_devices(api_key)
    elif args.action == "realtime":
        action_realtime(api_key, args.device_id, args.device_name)
    elif args.action == "history":
        action_history(api_key, args.device_id, args.device_name, args.range_)


if __name__ == "__main__":
    main()
