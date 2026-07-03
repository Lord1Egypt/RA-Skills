"""AppDaemon plugin for HomeKit devices via Homebridge REST API.

File MUST be named homebridgeplugin.py for AppDaemon to load it.
Class MUST be named HomebridgePlugin (title case of plugin type).
"""

import asyncio
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class HomebridgePlugin:
    """AppDaemon plugin for HomeKit devices via Homebridge.

    Required methods for AppDaemon PluginBase:
    - __init__(ad, name, args)
    - get_namespace() -> str
    - get_updates() -> async coroutine (main polling loop)
    - stop()
    - get_complete_state() -> dict
    - get_metadata() -> dict
    - utility() -> called every second
    """

    def __init__(self, ad, name: str, args: Dict):
        self.AD = ad
        self.name = name
        self.config = args
        self.namespace = args.get("namespace", "homekit")
        self.stopping = False

        # Import client
        import sys
        plugin_dir = str(Path(__file__).parent)
        if plugin_dir not in sys.path:
            sys.path.insert(0, plugin_dir)
        from homebridgeclient import HomebridgeClient

        # Plugin config
        self._poll_interval = args.get("poll_interval", 30)
        self._accessory_type_map = {
            "Lightbulb": "light",
            "Switch": "switch",
            "Outlet": "switch",
            "Thermostat": "climate",
            "Fan": "fan",
            "WindowCovering": "cover",
            "LockMechanism": "lock",
            "GarageDoorOpener": "cover",
            "MotionSensor": "binary_sensor",
            "ContactSensor": "binary_sensor",
            "TemperatureSensor": "sensor",
            "HumiditySensor": "sensor",
            "LightSensor": "sensor",
        }

        # Client
        self.client = HomebridgeClient(
            url=args.get("homebridge_url", "http://localhost:8581"),
            username=args.get("username", "admin"),
            password=args.get("password", "admin"),
        )

        # State tracking
        self._state: Dict[str, Dict] = {}
        self._registered_entities: Dict[str, Dict] = {}
        self._running = False
        self._last_poll = 0
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
                print(f"[HomebridgePlugin:{self.name}] Poll error: {e}")
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
        """Called every second by AppDaemon. Handles polling."""
        if not self._running or self.stopping:
            return

        now = time.time()
        if now - self._last_poll < self._poll_interval:
            return

        self._last_poll = now

        # Refresh accessories from Homebridge
        self.client._refresh_accessories()

        # Update state for all registered entities
        for entity_id, conf in self._registered_entities.items():
            self._update_entity_state(entity_id, conf)

    # === Initialization ===

    async def initialize(self) -> bool:
        if self._initialized:
            return True

        success = self.client.initialize()
        if not success:
            print(f"[HomebridgePlugin:{self.name}] Failed to connect to Homebridge")
            return False

        print(f"[HomebridgePlugin:{self.name}] Connected, {len(self.client.accessories)} accessories found")

        self._load_entity_registrations()
        self._auto_register_accessories()

        self._running = True
        self._initialized = True
        print(f"[HomebridgePlugin:{self.name}] Initialized, {len(self._registered_entities)} entities")
        return True

    def _load_entity_registrations(self):
        """Load entity_id -> accessory mapping from devices.yaml."""
        devices_file = self.config.get("devices_file")
        if devices_file:
            fpath = Path(devices_file)
            if not fpath.is_absolute():
                fpath = Path(".") / devices_file
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    devices_config = yaml.safe_load(f)
            except Exception as e:
                print(f"[HomebridgePlugin] Failed to load {devices_file}: {e}")
                devices_config = {}
        else:
            devices_config = self.config.get("devices", {})

        for category in ["sensors", "lights", "switches", "curtains", "climate", "scenes"]:
            for device_conf in devices_config.get(category, []):
                if device_conf.get("platform") == "homekit":
                    entity_id = device_conf.get("entity_id")
                    if entity_id:
                        self._registered_entities[entity_id] = device_conf

    def _auto_register_accessories(self):
        """Auto-register Homebridge accessories not already in devices.yaml."""
        existing_uids = {conf.get("accessory_id") for conf in self._registered_entities.values()}

        for acc in self.client.accessories:
            uid = acc.get("uniqueId", "")
            if uid in existing_uids:
                continue

            acc_type = acc.get("type", "")
            ha_type = self._accessory_type_map.get(acc_type, "switch")
            name = acc.get("serviceName", uid)
            entity_id = f"{ha_type}.{name.lower().replace(' ', '_')}"

            self._registered_entities[entity_id] = {
                "entity_id": entity_id,
                "name": name,
                "platform": "homekit",
                "accessory_id": uid,
                "type": ha_type,
                "homekit_type": acc_type,
            }

    def _update_entity_state(self, entity_id: str, conf: Dict):
        """Update entity state from Homebridge accessory."""
        uid = conf.get("accessory_id")
        if not uid:
            return

        values = self.client.get_accessory_state(uid)
        if values is None:
            return

        ha_type = conf.get("type", "switch")

        # Determine state based on type
        if ha_type in ("light", "switch"):
            state = "on" if values.get("On") else "off"
        elif ha_type == "binary_sensor":
            state = "on" if values.get("MotionDetected") or values.get("ContactSensorState") else "off"
        elif ha_type == "climate":
            state = str(values.get("TargetTemperature", "unknown"))
        else:
            state = str(values.get("On", "unknown"))

        self._state[entity_id] = {
            "entity_id": entity_id,
            "state": state,
            "attributes": {
                "friendly_name": conf.get("name", entity_id),
                "accessory_id": uid,
                "platform": "homekit",
                "values": values,
            },
            "last_changed": time.time(),
        }

    # === Public API for Apps ===

    def get_state(self, entity_id: str, attribute: Optional[str] = None) -> Any:
        state = self._state.get(entity_id)
        if state is None:
            return None
        if attribute:
            return state.get("attributes", {}).get(attribute)
        return state.get("state")

    def call_service(self, domain: str, service: str, data: Dict) -> bool:
        """Call a HomeKit device service."""
        entity_id = data.get("entity_id", "")
        entity_conf = self._registered_entities.get(entity_id)
        if not entity_conf:
            return False

        uid = entity_conf.get("accessory_id")
        if not uid:
            return False

        if service == "turn_on":
            return self.client.turn_on(uid)
        elif service == "turn_off":
            return self.client.turn_off(uid)
        elif service == "set":
            characteristic = data.get("characteristic")
            value = data.get("value")
            if characteristic and value is not None:
                return self.client.set_accessory(uid, characteristic, value)
        return False

    def get_entity_by_name(self, name: str) -> Optional[Dict]:
        for entity_id, conf in self._registered_entities.items():
            if conf.get("name") == name:
                return {"entity_id": entity_id, **conf}
        return None

    def get_all_entities(self) -> Dict[str, Dict]:
        return self._registered_entities.copy()

    def get_accessories(self) -> List[Dict]:
        return self.client.accessories
