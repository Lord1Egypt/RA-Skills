"""Mijia client wrapper for AppDaemon plugin."""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent to path for mijiaAPI import
sys.path.insert(0, str(Path(__file__).parent))

from mijiaAPI import mijiaAPI


class MijiaClient:
    """Wrapper around mijia-api with device mapping and state caching."""

    def __init__(self, auth_path: Optional[str] = None):
        self.api = mijiaAPI(auth_data_path=auth_path)
        self._devices: List[Dict] = []
        self._device_map: Dict[str, Dict] = {}  # did -> device info
        self._state_cache: Dict[str, Dict] = {}  # did -> {siid.piid: value}
        self._home_id: Optional[str] = None

    def initialize(self) -> bool:
        """Initialize client: verify auth, discover devices."""
        if not self.api.available:
            return False
        self._refresh_devices()
        return True

    def _refresh_devices(self):
        """Refresh device list from cloud."""
        self._devices = self.api.get_devices_list()
        self._device_map = {}
        for d in self._devices:
            did = d.get("did", "")
            self._device_map[did] = d
        homes = self.api.get_homes_list()
        if homes:
            self._home_id = homes[0].get("id")

    @property
    def devices(self) -> List[Dict]:
        return self._devices

    @property
    def home_id(self) -> Optional[str]:
        return self._home_id

    def get_device_by_did(self, did: str) -> Optional[Dict]:
        return self._device_map.get(did)

    def poll_device_state(self, did: str, siid: int, piid: int) -> tuple:
        """Poll a single device property. Returns (value, old_value)."""
        try:
            result = self.api.get_devices_prop([{"did": did, "siid": siid, "piid": piid}])
            if result and len(result) > 0:
                value = result[0].get("value")
                cache_key = f"{siid}.{piid}"
                if did not in self._state_cache:
                    self._state_cache[did] = {}
                old_value = self._state_cache[did].get(cache_key)
                self._state_cache[did][cache_key] = value
                return value, old_value
        except Exception as e:
            print(f"[MijiaClient] Poll error for {did} siid={siid} piid={piid}: {e}")
        return None, None

    def set_device_property(self, did: str, siid: int, piid: int, value: Any) -> bool:
        try:
            self.api.set_devices_prop([{"did": did, "siid": siid, "piid": piid, "value": value}])
            return True
        except Exception as e:
            print(f"[MijiaClient] Set property error: {e}")
            return False

    def run_device_action(self, did: str, siid: int, aiid: int, params: List = None) -> bool:
        try:
            self.api.run_action({"did": did, "siid": siid, "aiid": aiid, "in": params or []})
            return True
        except Exception as e:
            print(f"[MijiaClient] Run action error: {e}")
            return False

    def run_scene(self, scene_id: str, home_id: Optional[str] = None) -> bool:
        try:
            self.api.run_scene(scene_id=scene_id, home_id=home_id or self._home_id)
            return True
        except Exception as e:
            print(f"[MijiaClient] Run scene error: {e}")
            return False

    def get_scenes(self) -> List[Dict]:
        try:
            return self.api.get_scenes_list()
        except Exception as e:
            print(f"[MijiaClient] Get scenes error: {e}")
            return []

    def get_cached_state(self, did: str, siid: int, piid: int) -> Any:
        cache_key = f"{siid}.{piid}"
        if did in self._state_cache:
            return self._state_cache[did].get(cache_key)
        return None
