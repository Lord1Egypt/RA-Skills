#!/usr/bin/env python3
"""Standalone Mijia + HomeKit Automation Engine.

Supports both Mijia (via mijia-api) and HomeKit (via Homebridge) devices
in a single automation engine. No AppDaemon dependency.

Usage:
    python3 run_automations.py [--config path/to/conf]
    python3 run_automations.py --discover              # List Mijia devices
    python3 run_automations.py --discover-homekit      # List Homebridge accessories
"""

import argparse
import asyncio
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Add plugin dirs to path
sys.path.insert(0, str(Path(__file__).parent / "plugins" / "mijia"))
sys.path.insert(0, str(Path(__file__).parent / "plugins" / "homekit"))

from mijia_client import MijiaClient
from homebridgeclient import HomebridgeClient


class AutomationEngine:
    """Dual-platform automation engine — Mijia + HomeKit."""

    def __init__(self, config_dir: str):
        self.config_dir = Path(config_dir)
        self.automations: List[Dict] = []
        self.entity_map: Dict[str, Dict] = {}
        self.state: Dict[str, Dict] = {}
        self._running = False
        self._last_triggered: Dict[str, float] = {}
        self._cooldown = 5

        # Platform clients
        self.mijia_client: Optional[MijiaClient] = None
        self.homekit_client: Optional[HomebridgeClient] = None

    def initialize(self) -> bool:
        """Initialize clients and load configs."""
        print("[Engine] Initializing...")

        # Load configs first
        devices_path = self.config_dir / "devices.yaml"
        if devices_path.exists():
            self._load_devices(devices_path)

        auto_path = self.config_dir / "automations.yaml"
        if auto_path.exists():
            self._load_automations(auto_path)

        # Detect which platforms are needed
        platforms = self._detect_platforms()

        # Initialize Mijia client
        if "mijia" in platforms:
            print("[Engine] Connecting to Mijia...")
            self.mijia_client = MijiaClient()
            if self.mijia_client.initialize():
                print(f"[Engine] Mijia: {len(self.mijia_client.devices)} devices")
            else:
                print("[Engine] Mijia: auth invalid, skipping")
                self.mijia_client = None

        # Initialize Homebridge client
        if "homekit" in platforms:
            config = self._load_config()
            hb_url = config.get("homebridge_url", "http://localhost:8581")
            hb_user = config.get("username", "admin")
            hb_pass = config.get("password", "admin")

            print(f"[Engine] Connecting to Homebridge at {hb_url}...")
            self.homekit_client = HomebridgeClient(hb_url, hb_user, hb_pass)
            if self.homekit_client.initialize():
                print(f"[Engine] HomeKit: {len(self.homekit_client.accessories)} accessories")
            else:
                print("[Engine] HomeBridge: connection failed, skipping")
                self.homekit_client = None

        print(f"[Engine] Loaded {len(self.entity_map)} entities, {len(self.automations)} automations")
        return True

    def _load_config(self) -> Dict:
        """Load appdaemon.yaml for Homebridge connection settings."""
        config_path = self.config_dir / "appdaemon.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data.get("appdaemon", {}).get("plugins", {}).get("homekit", {})
        return {}

    def _detect_platforms(self) -> set:
        """Detect which platforms are used by registered entities."""
        platforms = set()
        for conf in self.entity_map.values():
            p = conf.get("platform", "mijia")
            platforms.add(p)
        return platforms

    def _load_devices(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for category in ["sensors", "lights", "switches", "curtains", "climate", "scenes"]:
            for device in data.get(category, []):
                eid = device.get("entity_id")
                if eid:
                    self.entity_map[eid] = device

    def _load_automations(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if isinstance(data, list):
            for auto in data:
                if auto.get("trigger") and auto.get("action"):
                    if not isinstance(auto["trigger"], list):
                        auto["trigger"] = [auto["trigger"]]
                    if not isinstance(auto["action"], list):
                        auto["action"] = [auto["action"]]
                    self.automations.append(auto)

    async def run(self):
        """Main event loop with smart polling."""
        self._running = True

        # Detect occupancy sensors for smart polling
        occupancy_sensors = [
            conf.get("did") for conf in self.entity_map.values()
            if conf.get("type") in ("occupancy", "motion") and conf.get("platform") == "mijia"
        ]

        print(f"[Engine] Running... (Ctrl+C to stop)")
        print(f"[Engine] Platforms: Mijia={'YES' if self.mijia_client else 'NO'}, HomeKit={'YES' if self.homekit_client else 'NO'}")

        while self._running:
            try:
                # Smart polling interval
                occupied = False
                if self.mijia_client and occupancy_sensors:
                    occupied = any(
                        self.mijia_client.get_cached_state(did, 2, 1) in (True, 1)
                        for did in occupancy_sensors if did
                    )
                interval = 10 if occupied else 60

                # Poll Mijia sensors
                if self.mijia_client:
                    for entity_id, conf in self.entity_map.items():
                        if conf.get("platform") == "mijia" and conf.get("type") in (
                            "sensor", "binary_sensor", "occupancy", "motion"
                        ):
                            await self._poll_mijia(entity_id, conf)

                # Poll Homebridge accessories
                if self.homekit_client:
                    self.homekit_client._refresh_accessories()
                    for entity_id, conf in self.entity_map.items():
                        if conf.get("platform") == "homekit":
                            self._update_homekit_state(entity_id, conf)

                # Check time triggers
                self._check_time_triggers()

                await asyncio.sleep(interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[Engine] Error: {e}")
                await asyncio.sleep(5)

    async def _poll_mijia(self, entity_id: str, conf: Dict):
        """Poll a Mijia sensor and evaluate automations if changed."""
        did = conf.get("did")
        siid = conf.get("siid", 2)
        piid = conf.get("piid", 1)
        value, old_value = self.mijia_client.poll_device_state(did, siid, piid)

        if value is not None:
            state_str = self._format_state(value, conf.get("type"))
            old_state_str = self._format_state(old_value, conf.get("type")) if old_value is not None else None
            self.state[entity_id] = {"state": state_str, "attributes": conf, "last_changed": time.time()}

            if old_state_str is not None and state_str != old_state_str:
                print(f"[Engine] State: {conf.get('name', entity_id)} {old_state_str} -> {state_str}")
                await self._evaluate_automations(entity_id, old_state_str, state_str)

    def _update_homekit_state(self, entity_id: str, conf: Dict):
        """Update entity state from Homebridge accessory."""
        uid = conf.get("accessory_id")
        if not uid:
            return

        values = self.homekit_client.get_accessory_state(uid)
        if values is None:
            return

        ha_type = conf.get("type", "switch")
        if ha_type in ("light", "switch"):
            state = "on" if values.get("On") else "off"
        elif ha_type == "binary_sensor":
            state = "on" if values.get("MotionDetected") or values.get("ContactSensorState") else "off"
        elif ha_type == "climate":
            state = str(values.get("TargetTemperature", "unknown"))
        else:
            state = str(values.get("On", "unknown"))

        old_state = self.state.get(entity_id, {}).get("state")
        self.state[entity_id] = {
            "state": state,
            "attributes": {**conf, "values": values},
            "last_changed": time.time(),
        }

        if old_state is not None and state != old_state:
            print(f"[Engine] State: {conf.get('name', entity_id)} {old_state} -> {state}")
            asyncio.create_task(self._evaluate_automations(entity_id, old_state, state))

    def _format_state(self, value: Any, device_type: Optional[str]) -> str:
        if device_type in ("occupancy", "motion", "binary_sensor"):
            return "on" if value in (True, 1) else "off"
        if isinstance(value, bool):
            return "on" if value else "off"
        return str(value) if value is not None else "unknown"

    async def _evaluate_automations(self, entity_id: str, old_state: str, new_state: str):
        for auto in self.automations:
            auto_id = auto.get("id", auto.get("alias", "unknown"))
            now = time.time()
            if now - self._last_triggered.get(auto_id, 0) < self._cooldown:
                continue

            triggered = any(
                self._evaluate_trigger(t, entity_id, old_state, new_state)
                for t in auto.get("trigger", [])
            )
            if not triggered:
                continue

            if not self._evaluate_conditions(auto.get("condition", [])):
                continue

            print(f"[Engine] >>> Triggered: {auto.get('alias', auto_id)}")
            self._last_triggered[auto_id] = now
            await self._execute_actions(auto["action"])

    def _evaluate_trigger(self, trigger: Dict, entity_id: str, old_state: str, new_state: str) -> bool:
        platform = trigger.get("platform")
        if platform == "state":
            if trigger.get("entity_id") != entity_id:
                return False
            if trigger.get("to") is not None and str(new_state) != str(trigger["to"]):
                return False
            if trigger.get("from") is not None and str(old_state) != str(trigger["from"]):
                return False
            return True
        elif platform == "numeric_state":
            if trigger.get("entity_id") != entity_id:
                return False
            try:
                value = float(new_state)
            except (ValueError, TypeError):
                return False
            if trigger.get("above") is not None and value <= float(trigger["above"]):
                return False
            if trigger.get("below") is not None and value >= float(trigger["below"]):
                return False
            return True
        return False

    def _evaluate_conditions(self, conditions: List[Dict]) -> bool:
        if not conditions:
            return True
        return all(self._evaluate_single_condition(c) for c in conditions)

    def _evaluate_single_condition(self, cond: Dict) -> bool:
        ctype = cond.get("condition")
        if ctype == "state":
            entity_id = cond.get("entity_id")
            expected = cond.get("state")
            if entity_id and expected is not None:
                return str(self.state.get(entity_id, {}).get("state")) == str(expected)
        elif ctype == "time":
            now = datetime.now().strftime("%H:%M:%S")
            if cond.get("after") and now < cond["after"]:
                return False
            if cond.get("before") and now > cond["before"]:
                return False
            return True
        elif ctype == "and":
            return self._evaluate_conditions(cond.get("conditions", []))
        elif ctype == "or":
            return any(self._evaluate_single_condition(c) for c in cond.get("conditions", []))
        elif ctype == "not":
            return not self._evaluate_conditions(cond.get("conditions", []))
        return True

    async def _execute_actions(self, actions: List[Dict]):
        for action in actions:
            await self._execute_single_action(action)

    async def _execute_single_action(self, action: Dict):
        service = action.get("service")
        if not service:
            return

        parts = service.split(".", 1)
        domain, service_name = parts[0], parts[1] if len(parts) > 1 else ""
        target = action.get("target", {})
        data = action.get("data", {})
        entity_id = target.get("entity_id", data.get("entity_id", ""))
        entity_conf = self.entity_map.get(entity_id)

        # Route to correct platform
        platform = entity_conf.get("platform", "mijia") if entity_conf else "mijia"

        if platform == "mijia":
            self._execute_mijia_action(domain, service_name, entity_conf, data)
        elif platform == "homekit":
            self._execute_homekit_action(domain, service_name, entity_conf, data)

        # Handle delay
        delay = action.get("delay")
        if delay:
            seconds = self._parse_delay(delay)
            print(f"[Engine]   Delay: {seconds}s")
            await asyncio.sleep(seconds)

    def _execute_mijia_action(self, domain: str, service_name: str, entity_conf: Dict, data: Dict):
        if domain == "scene" and service_name == "turn_on":
            if entity_conf and "scene_id" in entity_conf:
                self.mijia_client.run_scene(entity_conf["scene_id"])
                print(f"[Engine]   Mijia: run scene {entity_conf.get('name')}")

        elif domain in ("light", "switch"):
            if entity_conf:
                value = service_name == "turn_on"
                self.mijia_client.set_device_property(
                    entity_conf["did"], entity_conf.get("siid", 2),
                    entity_conf.get("piid", 1), value,
                )
                print(f"[Engine]   Mijia: {entity_conf.get('name')} -> {'on' if value else 'off'}")

        elif domain == "mijia":
            self.mijia_client.run_device_action(
                data.get("did"), data.get("siid"),
                data.get("aiid"), data.get("params", []),
            )
            print(f"[Engine]   Mijia: {service_name}")

    def _execute_homekit_action(self, domain: str, service_name: str, entity_conf: Dict, data: Dict):
        if not self.homekit_client or not entity_conf:
            return

        uid = entity_conf.get("accessory_id")
        if not uid:
            return

        if domain in ("light", "switch") and service_name == "turn_on":
            self.homekit_client.turn_on(uid)
            print(f"[Engine]   HomeKit: {entity_conf.get('name')} -> on")
        elif domain in ("light", "switch") and service_name == "turn_off":
            self.homekit_client.turn_off(uid)
            print(f"[Engine]   HomeKit: {entity_conf.get('name')} -> off")
        elif service_name == "set":
            characteristic = data.get("characteristic")
            value = data.get("value")
            if characteristic and value is not None:
                self.homekit_client.set_accessory(uid, characteristic, value)
                print(f"[Engine]   HomeKit: {entity_conf.get('name')} {characteristic}={value}")

    def _parse_delay(self, delay) -> int:
        if isinstance(delay, (int, float)):
            return int(delay)
        if isinstance(delay, str):
            if ":" in delay:
                parts = delay.split(":")
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            return int(delay)
        if isinstance(delay, dict):
            return int(delay.get("seconds", 0)) + int(delay.get("minutes", 0)) * 60
        return 0

    def _check_time_triggers(self):
        now = datetime.now().strftime("%H:%M:%S")
        for auto in self.automations:
            for trigger in auto.get("trigger", []):
                if trigger.get("platform") == "time":
                    at_time = trigger.get("at")
                    if at_time and now >= at_time:
                        auto_id = auto.get("id", "unknown")
                        if time.time() - self._last_triggered.get(auto_id, 0) > 60:
                            print(f"[Engine] >>> Time trigger: {auto.get('alias', auto_id)}")
                            self._last_triggered[auto_id] = time.time()
                            asyncio.create_task(self._execute_actions(auto["action"]))

    def stop(self):
        self._running = False


def discover_mijia(config_dir: str):
    """List all Mijia devices."""
    client = MijiaClient()
    if not client.initialize():
        print("ERROR: Mijia auth invalid")
        return

    print(f"\n{'='*60}")
    print(f"Mijia Devices: {len(client.devices)}")
    print(f"{'='*60}\n")
    for d in client.devices:
        name = d.get("name", "?")
        model = d.get("model", "?")
        did = d.get("did", "?")
        online = "ON" if d.get("isOnline") else "OFF"
        print(f"  [{online:3}] {name:30} {model:35} DID:{did}")

    scenes = client.get_scenes()
    print(f"\n{'='*60}")
    print(f"Mijia Scenes: {len(scenes)}")
    print(f"{'='*60}\n")
    for s in scenes:
        print(f"  {s.get('name', '?'):30} ID:{s.get('scene_id', '?')}")


def discover_homekit(config_dir: str):
    """List all Homebridge accessories."""
    config_path = Path(config_dir) / "appdaemon.yaml"
    if not config_path.exists():
        print("ERROR: appdaemon.yaml not found")
        return

    with open(config_path, "r") as f:
        data = yaml.safe_load(f)

    hb_config = data.get("appdaemon", {}).get("plugins", {}).get("homekit", {})
    url = hb_config.get("homebridge_url", "http://localhost:8581")
    user = hb_config.get("username", "admin")
    passwd = hb_config.get("password", "admin")

    client = HomebridgeClient(url, user, passwd)
    if not client.initialize():
        print(f"ERROR: Cannot connect to Homebridge at {url}")
        return

    print(f"\n{'='*60}")
    print(f"Homebridge Accessories: {len(client.accessories)}")
    print(f"{'='*60}\n")
    for acc in client.accessories:
        uid = acc.get("uniqueId", "?")
        name = acc.get("serviceName", "?")
        acc_type = acc.get("type", "?")
        values = acc.get("values", {})
        on_state = values.get("On", "?")
        status = "ON" if on_state else "OFF" if on_state is False else "?"
        print(f"  [{status:3}] {name:30} Type:{acc_type:20} UID:{uid}")


async def main():
    parser = argparse.ArgumentParser(description="Mijia + HomeKit Automation Engine")
    parser.add_argument("--config", default=str(Path.home() / ".config/smart-home-planner/automation/conf"))
    parser.add_argument("--discover", action="store_true", help="List Mijia devices")
    parser.add_argument("--discover-homekit", action="store_true", help="List Homebridge accessories")
    args = parser.parse_args()

    if args.discover:
        discover_mijia(args.config)
        return
    if getattr(args, "discover_homekit"):
        discover_homekit(args.config)
        return

    engine = AutomationEngine(args.config)
    if not engine.initialize():
        sys.exit(1)

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, engine.stop)

    await engine.run()
    print("[Engine] Stopped.")


if __name__ == "__main__":
    asyncio.run(main())
