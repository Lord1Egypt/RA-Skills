#!/usr/bin/env python3
"""
xiaomi-home-ha Mock HA Server
模拟 Home Assistant REST API，用于离线测试

Usage:
    python3 mock-ha-server.py [--port 18123]

Endpoints implemented:
    GET  /api/                          → {"message": "API running.", "version": "2024.11.0"}
    GET  /api/states                    → all mock entities
    GET  /api/states/<entity_id>        → single entity or 404
    POST /api/services/<domain>/<svc>   → accept & update state, return []
"""

import json
import re
import time
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

VALID_TOKEN = "mock_test_token_abc123"

# ── Mock entity store ─────────────────────────────────────────────────────────
ENTITY_STORE: dict[str, dict] = {
    "light.bed_lamp": {
        "entity_id": "light.bed_lamp",
        "state": "off",
        "attributes": {
            "friendly_name": "Bed Lamp",
            "brightness": None,
            "color_temp_kelvin": 4000,
            "min_color_temp_kelvin": 2000,
            "max_color_temp_kelvin": 6500,
            "supported_color_modes": ["color_temp"],
            "area_id": "bedroom",
        },
        "last_changed": "2026-03-11T00:00:00+00:00",
        "last_updated": "2026-03-11T00:00:00+00:00",
    },
    "light.ceiling": {
        "entity_id": "light.ceiling",
        "state": "off",
        "attributes": {
            "friendly_name": "Ceiling Light",
            "brightness": None,
            "color_temp_kelvin": 4000,
            "supported_color_modes": ["color_temp"],
            "area_id": "living_room",
        },
        "last_changed": "2026-03-11T00:00:00+00:00",
        "last_updated": "2026-03-11T00:00:00+00:00",
    },
    "switch.fan": {
        "entity_id": "switch.fan",
        "state": "off",
        "attributes": {"friendly_name": "Bedroom Fan", "area_id": "bedroom"},
        "last_changed": "2026-03-11T00:00:00+00:00",
        "last_updated": "2026-03-11T00:00:00+00:00",
    },
    "sensor.temperature": {
        "entity_id": "sensor.temperature",
        "state": "24.5",
        "attributes": {
            "friendly_name": "Room Temperature",
            "unit_of_measurement": "°C",
            "device_class": "temperature",
        },
        "last_changed": "2026-03-11T00:00:00+00:00",
        "last_updated": "2026-03-11T00:00:00+00:00",
    },
    "sensor.humidity": {
        "entity_id": "sensor.humidity",
        "state": "55",
        "attributes": {
            "friendly_name": "Room Humidity",
            "unit_of_measurement": "%",
            "device_class": "humidity",
        },
        "last_changed": "2026-03-11T00:00:00+00:00",
        "last_updated": "2026-03-11T00:00:00+00:00",
    },
    "media_player.xiaomi_speaker": {
        "entity_id": "media_player.xiaomi_speaker",
        "state": "idle",
        "attributes": {
            "friendly_name": "Xiaomi Speaker",
            "volume_level": 0.5,
            "is_volume_muted": False,
        },
        "last_changed": "2026-03-11T00:00:00+00:00",
        "last_updated": "2026-03-11T00:00:00+00:00",
    },
    "climate.bedroom_ac": {
        "entity_id": "climate.bedroom_ac",
        "state": "off",
        "attributes": {
            "friendly_name": "Bedroom AC",
            "temperature": 26,
            "current_temperature": 28,
            "hvac_mode": "off",
            "hvac_modes": ["off", "cool", "heat", "auto"],
        },
        "last_changed": "2026-03-11T00:00:00+00:00",
        "last_updated": "2026-03-11T00:00:00+00:00",
    },
    "scene.bedtime_mode": {
        "entity_id": "scene.bedtime_mode",
        "state": "unknown",
        "attributes": {"friendly_name": "Bedtime Mode"},
        "last_changed": "2026-03-11T00:00:00+00:00",
        "last_updated": "2026-03-11T00:00:00+00:00",
    },
}


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())


def apply_service(domain: str, service: str, body: dict) -> tuple[bool, str]:
    """Apply a service call to the mock entity store. Returns (ok, message)."""
    entity_id = body.get("entity_id", "")
    if not entity_id:
        return False, "entity_id is required"

    if entity_id not in ENTITY_STORE:
        return False, f"Entity not found: {entity_id}"

    entity = ENTITY_STORE[entity_id]
    attrs = entity["attributes"]
    ts = now_iso()

    # ── light services ─────────────────────────────────────────────────────
    if service == "turn_on":
        entity["state"] = "on"
        if "brightness_pct" in body:
            attrs["brightness"] = round(body["brightness_pct"] / 100 * 255)
        if "brightness" in body:
            attrs["brightness"] = body["brightness"]
        if "color_temp_kelvin" in body:
            attrs["color_temp_kelvin"] = body["color_temp_kelvin"]
        if "rgb_color" in body:
            attrs["rgb_color"] = body["rgb_color"]
        if "temperature" in body:
            attrs["temperature"] = body["temperature"]
        if "hvac_mode" in body:
            attrs["hvac_mode"] = body["hvac_mode"]
            entity["state"] = body["hvac_mode"]
        if "volume_level" in body:
            attrs["volume_level"] = body["volume_level"]

    elif service == "turn_off":
        entity["state"] = "off"
        if domain == "light":
            attrs["brightness"] = None

    elif service == "toggle":
        entity["state"] = "on" if entity["state"] == "off" else "off"

    elif service == "volume_set":
        attrs["volume_level"] = body.get("volume_level", attrs.get("volume_level", 0.5))

    elif service == "media_play":
        entity["state"] = "playing"

    elif service == "media_pause":
        entity["state"] = "paused"

    elif service == "media_stop":
        entity["state"] = "idle"

    elif service == "set_temperature":
        if "temperature" in body:
            attrs["temperature"] = body["temperature"]
        if "hvac_mode" in body:
            attrs["hvac_mode"] = body["hvac_mode"]
            entity["state"] = body["hvac_mode"]

    entity["last_updated"] = ts
    entity["last_changed"] = ts
    return True, "ok"


class HAHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # suppress default logging
        pass

    def _auth(self) -> bool:
        auth = self.headers.get("Authorization", "")
        return auth == f"Bearer {VALID_TOKEN}"

    def _json(self, code: int, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if not self._auth():
            self._json(401, {"message": "Unauthorized"})
            return

        path = urlparse(self.path).path

        if path == "/api/" or path == "/api":
            self._json(200, {"message": "API running.", "version": "2024.11.0"})

        elif path == "/api/states":
            self._json(200, list(ENTITY_STORE.values()))

        elif m := re.match(r"^/api/states/(.+)$", path):
            eid = m.group(1)
            if eid in ENTITY_STORE:
                self._json(200, ENTITY_STORE[eid])
            else:
                self._json(404, {"message": f"Entity not found: {eid}"})

        else:
            self._json(404, {"message": "Not found"})

    def do_POST(self):
        if not self._auth():
            self._json(401, {"message": "Unauthorized"})
            return

        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw)
        except json.JSONDecodeError:
            self._json(400, {"message": "Invalid JSON"})
            return

        if m := re.match(r"^/api/services/([^/]+)/([^/]+)$", path):
            domain, service = m.group(1), m.group(2)
            ok, msg = apply_service(domain, service, body)
            if ok:
                self._json(200, [])
            else:
                self._json(400, {"message": msg})
        else:
            self._json(404, {"message": "Not found"})


def main():
    parser = argparse.ArgumentParser(description="Mock HA server for xiaomi-home-ha tests")
    parser.add_argument("--port", type=int, default=18123, help="Port to listen on")
    args = parser.parse_args()

    server = HTTPServer(("127.0.0.1", args.port), HAHandler)
    print(f"Mock HA server running on http://127.0.0.1:{args.port}")
    print(f"Token: {VALID_TOKEN}")
    print(f"Entities: {len(ENTITY_STORE)}")
    print("Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
