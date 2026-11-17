"""Minimal standard-library client for the local UE bridge."""

from __future__ import annotations

import json
import os
import socket
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class BridgeError(RuntimeError):
    def __init__(
        self,
        message: str,
        code: str = "bridge_error",
        http_status: int | None = None,
        hint: str = "",
    ) -> None:
        super().__init__(message)
        self.message = str(message)
        self.code = code
        self.http_status = http_status
        self.hint = hint

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.http_status is not None:
            data["http_status"] = self.http_status
        if self.hint:
            data["hint"] = self.hint
        return data


def read_token(explicit: str | None = None) -> str:
    if explicit:
        return explicit.strip()
    env = os.environ.get("UE_AUDIT_BRIDGE_TOKEN", "").strip()
    if env:
        return env
    token_file = os.environ.get("UE_AUDIT_BRIDGE_TOKEN_FILE", "").strip()
    if token_file:
        paths = [token_file]
    else:
        appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
        paths = [os.path.join(appdata, "ue-audit", "bridge-token")]
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return handle.read().strip()
        except OSError:
            continue
    return ""


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "ok")
    return bool(value)


def _first(payload: dict[str, Any], ue_info: dict[str, Any], key: str) -> Any:
    for source in (payload, ue_info):
        value = source.get(key)
        if value not in (None, ""):
            return value
    return ""


def normalize_health(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    if isinstance(payload.get("result"), dict) and "ue_info" not in payload:
        payload = payload["result"]
    ue_info = payload.get("ue_info")
    if not isinstance(ue_info, dict):
        ue_info = {}
    bridge_loaded = _as_bool(_first(payload, ue_info, "bridge_loaded"))
    return {
        "status": str(payload.get("status") or ("ok" if bridge_loaded else "")),
        "bridge_version": str(_first(payload, ue_info, "bridge_version")),
        "bridge_loaded": bridge_loaded,
        "engine_version": str(_first(payload, ue_info, "engine_version")),
        "project_name": str(_first(payload, ue_info, "project_name")),
        "project_dir": str(_first(payload, ue_info, "project_dir")),
        "uptime_seconds": payload.get("uptime_seconds", 0),
        "request_count": payload.get("request_count", 0),
    }


@dataclass
class BridgeClient:
    host: str = "127.0.0.1"
    port: int = 8889
    token: str = ""
    timeout: float = 8.0
    retries: int = 2
    backoff: float = 0.4

    def __post_init__(self) -> None:
        self.port = int(self.port)
        self.timeout = float(self.timeout)
        self.retries = max(0, int(self.retries))
        self.backoff = max(0.0, float(self.backoff))

    def _url(self, path: str) -> str:
        return f"http://{self.host}:{self.port}{path}"

    def _request(self, method: str, path: str, payload: Any = None) -> Any:
        headers = {"X-Skill-Token": self.token, "Accept": "application/json"}
        body = None
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"

        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            request = urllib.request.Request(
                self._url(path), data=body, method=method, headers=headers
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    raw = response.read().decode("utf-8", "replace")
                    status = response.getcode()
            except urllib.error.HTTPError as exc:
                raw = exc.read().decode("utf-8", "replace")
                if exc.code in (401, 403):
                    raise BridgeError(
                        f"authentication failed (HTTP {exc.code})",
                        "auth_error",
                        exc.code,
                        "check the bridge token or --token",
                    ) from exc
                if exc.code >= 500 and attempt < self.retries:
                    last_error = exc
                    time.sleep(self.backoff * (2**attempt))
                    continue
                raise BridgeError(
                    f"HTTP {exc.code}: {raw[:200]}", "http_error", exc.code
                ) from exc
            except (urllib.error.URLError, socket.timeout, TimeoutError, OSError) as exc:
                last_error = exc
                if attempt < self.retries:
                    time.sleep(self.backoff * (2**attempt))
                    continue
                raise BridgeError(
                    f"cannot connect to bridge {self.host}:{self.port} ({exc})",
                    "network_error",
                    None,
                    "confirm the UE editor is running and the bridge listens on 127.0.0.1",
                ) from exc
            try:
                return json.loads(raw or "{}")
            except json.JSONDecodeError as exc:
                raise BridgeError(
                    f"bridge returned non-JSON: {raw[:200]}", "invalid_json", status
                ) from exc

        raise BridgeError(f"bridge request failed: {last_error}", "network_error")

    def health(self) -> dict[str, Any]:
        return normalize_health(self._request("GET", "/health"))

    def call(self, command: str, params: dict[str, Any] | None = None) -> Any:
        data = self._request(
            "POST",
            "/command",
            {"command": command, "params": params or {}},
        )
        if not isinstance(data, dict):
            raise BridgeError("bridge response is not an object", "invalid_json")
        if not data.get("success"):
            raise BridgeError(
                str(data.get("error") or f"command failed: {command}"),
                "command_failed",
            )
        result = data.get("result")
        if command == "health":
            return normalize_health(result if isinstance(result, dict) else {})
        return result
