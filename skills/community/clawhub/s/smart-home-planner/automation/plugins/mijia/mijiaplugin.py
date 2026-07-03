"""AppDaemon plugin for Xiaomi/Mijia devices via mijia-api.

File MUST be named mijiaplugin.py for AppDaemon to load it.
Class MUST be named MijiaPlugin (title case of plugin type).
"""

import asyncio
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class MijiaPlugin:
    """AppDaemon plugin for Mijia devices.

    Required methods for AppDaemon PluginBase:
    - __init__(ad, name, args)
    - get_namespace() -> str
    - get_updates() -> async coroutine (main polling loop)
    - stop()
    - get_complete_state() -> dict
    - get_metadata() -> dict
    - utility() -> called every second
    - get_state(entity_id, attribute) -> value
    - call_service(domain, service, data) -> bool
    """

    def __init__(self, ad, name: str, args: Dict):
        self.AD = ad
        self.name = name
        self.config = args
        self.namespace = args.get("namespace", "mijia")
        self.stopping = False

        # Import client
        import sys
        plugin_dir = str(Path(__file__).parent)
        if plugin_dir not in sys.path:
            sys.path.insert(0, plugin_dir)
        from mijia_client import MijiaClient

        # Plugin config
        self._default_poll_interval = args.get("poll_interval", 30)
        self._smart_poll = args.get("smart_poll", True)
        self._occupancy_sensors = args.get("occupancy_sensors", [])
        self._fast_interval = args.get("fast_poll_interval", 10)
        self._slow_interval = args.get("slow_poll_interval", 60)

        # Client
        self.client = MijiaClient(auth_path=args.get("auth_path"))

        # State tracking
        self._state: Dict[str, Dict] = {}
        self._registered_entities: Dict[str, Dict] = {}
        self._running = False
        self._last_poll = 0
        self._poll_interval = self._default_poll_interval
        self._initialized = False

    # === Required AppDaemon Methods ===

    def get_namespace(self) -> str:
        return self.namespace

    async def get_updates(self):
        """Main polling loop - called by AppDaemon as a background task."""
        while not self.stopping:
            try:
                if self._running:
                    self.utility()
            except Exception as e:
                print(f"[MijiaPlugin:{self.name}] Poll error: {e}")
            await asyncio.sleep(1)

    def stop(self):
        self.stopping = True
        self._running = False

    async def get_complete_state(self) -> Dict:
        return {self.namespace: self._state.copy()}

    async def get_metadata(self) -> Dict:
        return {
            "latitude": 39.9042,
            "longitude": 116.4074,
            "elevation": 43,
            "time_zone": "Asia/Shanghai",
        }

    def utility(self):
        """Called every second by AppDaemon. Handles smart polling."""
        if not self._running or self.stopping:
            return

        now = time.time()
        if now - self._last_poll < self._poll_interval:
            return

        self._last_poll = now

        # Smart polling: adjust interval based on occupancy
        if self._smart_poll and self._occupancy_sensors:
            occupied = self._check_occupancy()
            self._poll_interval = self._fast_interval if occupied else self._slow_interval
        else:
            self._poll_interval = self._default_poll_interval

        # Poll all registered sensors
        for entity_id, conf in self._registered_entities.items():
            if conf.get("type") in ("sensor", "binary_sensor", "occupancy"):
                self._poll_entity(entity_id, conf)

    # === Initialization ===

    async def initialize(self) -> bool:
        if self._initialized:
            return True
        success = self.client.initialize()
        if not success:
            print(f"[MijiaPlugin:{self.name}] Failed to initialize - auth invalid")
            return False
        print(f"[MijiaPlugin:{self.name}] Connected, {len(self.client.devices)} devices found")
        self._load_entity_registrations()
        self._running = True
        self._initialized = True
        print(f"[MijiaPlugin:{self.name}] Initialized, {len(self._registered_entities)} entities")
        return True

    def _load_entity_registrations(self):
        """Load entity_id -> device mapping from devices.yaml file."""
        devices_file = self.config.get("devices_file")
        if devices_file:
            fpath = Path(devices_file)
            if not fpath.is_absolute():
                fpath = Path(".") / devices_file
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    devices_config = yaml.safe_load(f)
            except Exception as e:
                print(f"[MijiaPlugin] Failed to load {devices_file}: {e}")
                devices_config = {}
        else:
            devices_config = self.config.get("devices", {})

        for category in ["sensors", "lights", "switches", "curtains", "climate", "scenes"]:
            for device_conf in devices_config.get(category, []):
                entity_id = device_conf.get("entity_id")
                if entity_id:
                    self._registered_entities[entity_id] = device_conf

    # === Internal Helpers ===

    def _check_occupancy(self) -> bool:
        for sensor_did in self._occupancy_sensors:
            cached = self.client.get_cached_state(sensor_did, 2, 1)
            if cached in (True, 1):
                return True
        return False

    def _poll_entity(self, entity_id: str, conf: Dict):
        did = conf.get("did")
        siid = conf.get("siid", 2)
        piid = conf.get("piid", 1)
        value, old_value = self.client.poll_device_state(did, siid, piid)
        if value is not None:
            state_str = self._format_state(value, conf.get("type"))
            old_state_str = self._format_state(old_value, conf.get("type")) if old_value is not None else None
            self._state[entity_id] = {
                "entity_id": entity_id,
                "state": state_str,
                "attributes": {
                    "friendly_name": conf.get("name", entity_id),
                    "device_id": did,
                    "model": conf.get("model", ""),
                    "siid": siid, "piid": piid,
                    "raw_value": value,
                },
                "last_changed": time.time(),
            }
            if old_state_str is not None and state_str != old_state_str:
                if hasattr(self.AD, "events"):
                    self.AD.events.process_event(self.namespace, "state_changed", {
                        "entity_id": entity_id,
                        "old_state": old_state_str,
                        "new_state": state_str,
                    })

    def _format_state(self, value: Any, device_type: Optional[str]) -> str:
        if device_type in ("occupancy", "motion", "binary_sensor"):
            return "on" if value in (True, 1) else "off"
        if isinstance(value, bool):
            return "on" if value else "off"
        return str(value) if value is not None else "unknown"

    # === Public API for Apps ===

    def get_state(self, entity_id: str, attribute: Optional[str] = None) -> Any:
        state = self._state.get(entity_id)
        if state is None:
            return None
        if attribute:
            return state.get("attributes", {}).get(attribute)
        return state.get("state")

    def call_service(self, domain: str, service: str, data: Dict) -> bool:
        if service == "set_property":
            return self.client.set_device_property(
                did=data.get("did"), siid=data.get("siid"),
                piid=data.get("piid"), value=data.get("value"),
            )
        elif service == "run_scene":
            return self.client.run_scene(
                scene_id=data.get("scene_id"),
                home_id=data.get("home_id"),
            )
        elif service == "run_action":
            return self.client.run_device_action(
                did=data.get("did"), siid=data.get("siid"),
                aiid=data.get("aiid"), params=data.get("params", []),
            )
        return False

    def get_entity_by_name(self, name: str) -> Optional[Dict]:
        for entity_id, conf in self._registered_entities.items():
            if conf.get("name") == name:
                return {"entity_id": entity_id, **conf}
        return None

    def get_all_entities(self) -> Dict[str, Dict]:
        return self._registered_entities.copy()

    def get_scenes(self) -> List[Dict]:
        return self.client.get_scenes()

    def get_devices(self) -> List[Dict]:
        return self.client.devices
