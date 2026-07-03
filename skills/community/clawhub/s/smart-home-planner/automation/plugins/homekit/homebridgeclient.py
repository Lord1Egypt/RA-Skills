"""Homebridge REST API client for AppDaemon plugin."""

import requests
from typing import Any, Dict, List, Optional


class HomebridgeClient:
    """Wrapper around Homebridge Config UI REST API."""

    def __init__(self, url: str = "http://localhost:8581",
                 username: str = "admin", password: str = "admin"):
        self.base_url = url.rstrip("/")
        self.username = username
        self.password = password
        self._token: Optional[str] = None
        self._accessories: List[Dict] = []
        self._accessory_map: Dict[str, Dict] = {}  # uniqueId -> accessory

    def initialize(self) -> bool:
        """Authenticate and discover accessories."""
        if not self._login():
            return False
        self._refresh_accessories()
        return True

    def _login(self) -> bool:
        """Authenticate with Homebridge and get JWT token."""
        try:
            resp = requests.post(f"{self.base_url}/api/auth/login", json={
                "username": self.username,
                "password": self.password,
            }, timeout=10)
            if resp.status_code == 200:
                self._token = resp.json().get("access_token")
                return True
            print(f"[HomebridgeClient] Login failed: {resp.status_code}")
        except Exception as e:
            print(f"[HomebridgeClient] Login error: {e}")
        return False

    def _refresh_token(self) -> bool:
        """Refresh JWT token."""
        if not self._token:
            return self._login()
        try:
            resp = requests.post(
                f"{self.base_url}/api/auth/refresh",
                headers=self._headers(),
                timeout=10,
            )
            if resp.status_code == 200:
                self._token = resp.json().get("access_token")
                return True
        except Exception:
            pass
        return self._login()

    def _headers(self, content_type: bool = False) -> Dict:
        """Build request headers."""
        h = {"Authorization": f"Bearer {self._token}"}
        if content_type:
            h["Content-Type"] = "application/json"
        return h

    def _request(self, method: str, path: str, **kwargs) -> Optional[requests.Response]:
        """Make an authenticated request with auto token refresh."""
        for attempt in range(2):
            try:
                resp = requests.request(
                    method,
                    f"{self.base_url}{path}",
                    headers=self._headers(content_type=kwargs.get("json") is not None),
                    timeout=10,
                    **kwargs,
                )
                if resp.status_code == 401 and attempt == 0:
                    self._refresh_token()
                    continue
                return resp
            except Exception as e:
                print(f"[HomebridgeClient] Request error: {e}")
                return None
        return None

    def _refresh_accessories(self):
        """Fetch all accessories from Homebridge."""
        resp = self._request("GET", "/api/accessories")
        if resp and resp.status_code == 200:
            self._accessories = resp.json()
            self._accessory_map = {}
            for acc in self._accessories:
                uid = acc.get("uniqueId", "")
                if uid:
                    self._accessory_map[uid] = acc
        else:
            print(f"[HomebridgeClient] Failed to fetch accessories")

    @property
    def accessories(self) -> List[Dict]:
        return self._accessories

    def get_accessory(self, unique_id: str) -> Optional[Dict]:
        """Get accessory by uniqueId."""
        return self._accessory_map.get(unique_id)

    def get_accessory_state(self, unique_id: str) -> Optional[Dict]:
        """Get current state values of an accessory."""
        acc = self._accessory_map.get(unique_id)
        if acc:
            return acc.get("values", {})
        return None

    def set_accessory(self, unique_id: str, characteristic: str, value: Any) -> bool:
        """Set an accessory characteristic (e.g., On, Brightness, TargetTemperature)."""
        resp = self._request(
            "PUT",
            f"/api/accessories/{requests.utils.quote(unique_id, safe='')}",
            json={"characteristicType": characteristic, "value": value},
        )
        if resp and resp.status_code == 200:
            # Update local cache
            if unique_id in self._accessory_map:
                if "values" not in self._accessory_map[unique_id]:
                    self._accessory_map[unique_id]["values"] = {}
                self._accessory_map[unique_id]["values"][characteristic] = value
            return True
        return False

    def turn_on(self, unique_id: str) -> bool:
        return self.set_accessory(unique_id, "On", True)

    def turn_off(self, unique_id: str) -> bool:
        return self.set_accessory(unique_id, "On", False)

    def set_brightness(self, unique_id: str, brightness: int) -> bool:
        return self.set_accessory(unique_id, "Brightness", brightness)

    def set_temperature(self, unique_id: str, temp: float) -> bool:
        return self.set_accessory(unique_id, "TargetTemperature", temp)

    def get_status(self) -> Optional[Dict]:
        """Get Homebridge server status."""
        resp = self._request("GET", "/api/status/homebridge")
        if resp and resp.status_code == 200:
            return resp.json()
        return None
