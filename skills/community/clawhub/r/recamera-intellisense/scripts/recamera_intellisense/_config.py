"""Device profile store at ``~/.recamera/devices.json`` (schema matches the Rust ``DeviceEntry``)."""

from __future__ import annotations

import json
import os
import re
import socket
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict

from ._errors import RecameraError

RECAMERA_DIR = Path.home() / ".recamera"
DEVICE_PROFILES_PATH = RECAMERA_DIR / "devices.json"


class DeviceRecord(TypedDict, total=False):
    name: str
    host: str
    token: str
    protocol: str
    allow_unsecured: bool
    port: Optional[int]


_TOKEN_RE = re.compile(r"^sk_[A-Za-z0-9_\-]+$")
_HOSTNAME_RE = re.compile(
    r"^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*$"
)


def is_valid_host(host: str) -> bool:
    host = host.strip()
    if not host:
        return False
    for family in (socket.AF_INET, socket.AF_INET6):
        try:
            socket.inet_pton(family, host)
            return True
        except OSError:
            continue
    return bool(_HOSTNAME_RE.match(host))


def validate_token(token: str) -> None:
    if not isinstance(token, str) or not _TOKEN_RE.match(token.strip()):
        raise ValueError(f"Invalid token format: expected 'sk_<chars>', got {token!r}.")


def validate_name(name: str) -> None:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Device name must be a non-empty string.")


def validate_host(host: str) -> None:
    if not isinstance(host, str) or not is_valid_host(host):
        raise ValueError(
            f"Invalid host: {host!r}. Expected IPv4/IPv6 address or DNS hostname."
        )


def validate_protocol(protocol: str) -> None:
    if protocol not in ("http", "https"):
        raise ValueError(
            f"Unsupported protocol: {protocol!r} (expected 'http' or 'https')."
        )


def _ensure_dir() -> None:
    RECAMERA_DIR.mkdir(parents=True, exist_ok=True)


def _normalize_entry(raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    host = raw.get("host")
    token = raw.get("token")
    if not isinstance(host, str) or not isinstance(token, str):
        return None
    protocol = raw.get("protocol", "http")
    if protocol not in ("http", "https"):
        protocol = "http"
    # Secure-by-default: TLS verification is on unless the user opts in.
    allow_unsecured = bool(raw.get("allow_unsecured", False))
    port = raw.get("port")
    if port is not None:
        try:
            port = int(port)
        except (TypeError, ValueError):
            port = None
    entry: Dict[str, Any] = {
        "host": host.strip(),
        "token": token,
        "protocol": protocol,
        "allow_unsecured": allow_unsecured,
    }
    if port is not None:
        entry["port"] = port
    return entry


def load_all() -> Dict[str, Dict[str, Any]]:
    """Load all device entries; returns ``{}`` when no file exists."""
    _ensure_dir()
    if not DEVICE_PROFILES_PATH.exists():
        return {}
    try:
        with open(DEVICE_PROFILES_PATH, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except json.JSONDecodeError as exc:
        raise RecameraError(
            f"Credential store {DEVICE_PROFILES_PATH} contains invalid JSON."
        ) from exc
    except OSError as exc:
        raise RecameraError(
            f"Unable to read credential store {DEVICE_PROFILES_PATH}."
        ) from exc
    if not isinstance(raw, dict):
        raise RecameraError(
            f"Credential store {DEVICE_PROFILES_PATH} must contain a JSON object."
        )
    out: Dict[str, Dict[str, Any]] = {}
    for name, info in raw.items():
        if not isinstance(name, str) or not isinstance(info, dict):
            continue
        norm = _normalize_entry(info)
        if norm is not None:
            out[name] = norm
    return out


def save_all(devices: Dict[str, Dict[str, Any]]) -> None:
    """Atomic write with 0600 perms."""
    _ensure_dir()
    fd, tmp_path = tempfile.mkstemp(
        dir=str(RECAMERA_DIR), prefix=".devices_", suffix=".json"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(devices, fh, indent=2, ensure_ascii=False, sort_keys=True)
            fh.write("\n")
        os.replace(tmp_path, str(DEVICE_PROFILES_PATH))
        try:
            os.chmod(DEVICE_PROFILES_PATH, 0o600)
        except OSError:
            pass
    except Exception as exc:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise RecameraError(
            f"Failed to save credential store {DEVICE_PROFILES_PATH}: {exc}"
        ) from exc


def resolve(device_name: str) -> DeviceRecord:
    """Return a fully-populated :class:`DeviceRecord`; raise if unknown."""
    if not isinstance(device_name, str) or not device_name.strip():
        raise RecameraError("'device_name' must not be empty.")
    devices = load_all()
    entry = devices.get(device_name)
    if entry is None:
        raise RecameraError(
            f"Device '{device_name}' not found. "
            "Use add_device to register it first (or list_devices to check)."
        )
    rec: DeviceRecord = {
        "name": device_name,
        "host": entry["host"],
        "token": entry["token"],
        "protocol": entry.get("protocol", "http"),
        "allow_unsecured": bool(entry.get("allow_unsecured", False)),
        "port": entry.get("port"),
    }
    return rec


def list_records_on_disk() -> List[DeviceRecord]:
    devices = load_all()
    out: List[DeviceRecord] = []
    for name in sorted(devices, key=str.lower):
        entry = devices[name]
        out.append(
            DeviceRecord(
                name=name,
                host=entry["host"],
                token=entry["token"],
                protocol=entry.get("protocol", "http"),
                allow_unsecured=bool(entry.get("allow_unsecured", False)),
                port=entry.get("port"),
            )
        )
    return out
