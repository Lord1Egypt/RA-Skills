"""Device profile CRUD (mirrors the MCP server's ``Device``-prefixed tools)."""

from __future__ import annotations

import http.client
import os
import socket
from typing import Any, Dict, List, Optional

from . import _config
from ._config import DeviceRecord
from ._errors import RecameraError

__all__ = [
    "detect_local_device",
    "add_device",
    "update_device",
    "remove_device",
    "get_device",
    "list_devices",
]

# Connectivity probe

_PROBE_PATH = "/api/v1/recamera-generate-204"
_PROBE_TIMEOUT = 3.0
_LOCAL_DAEMON_SOCKET = "/dev/shm/rcisd.sock"


def _probe(
    host: str, port: int, token: Optional[str], use_tls: bool, allow_unsecured: bool
) -> Optional[str]:
    """Return ``None`` on success or a human-readable error otherwise."""
    try:
        connect_host = host.strip()
        if use_tls:
            import ssl

            ctx = ssl.create_default_context()
            if allow_unsecured:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
            conn = http.client.HTTPSConnection(
                connect_host, port, timeout=_PROBE_TIMEOUT, context=ctx
            )
        else:
            conn = http.client.HTTPConnection(
                connect_host, port, timeout=_PROBE_TIMEOUT
            )
        headers = {"Authorization": token} if token else {}
        try:
            conn.request("GET", _PROBE_PATH, headers=headers)
            resp = conn.getresponse()
            status = resp.status
        finally:
            conn.close()
        if 200 <= status < 400:
            return None
        if status in (401, 403):
            return f"Authentication failed (HTTP {status}). Verify the token."
        return f"Unexpected response from device (HTTP {status})."
    except (socket.timeout, TimeoutError):
        return f"Connection to {host}:{port} timed out after {_PROBE_TIMEOUT:.0f}s."
    except ConnectionRefusedError:
        return f"Connection refused by {host}:{port}."
    except OSError as exc:
        return f"Unable to connect to {host}:{port} — {exc}."


def detect_local_device(socket_path: str = _LOCAL_DAEMON_SOCKET) -> Optional[str]:
    """Return *socket_path* if a local ``rcisd`` daemon accepts a Unix-socket
    connection there, else ``None``.

    The daemon serves its HTTP API over a Unix domain socket (default
    ``/dev/shm/rcisd.sock``); it does not listen on TCP. This mirrors the MCP
    server's ``detect_local_device`` tool.
    """
    if not socket_path or not hasattr(socket, "AF_UNIX"):
        return None
    if not os.path.exists(socket_path):
        return None
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(_PROBE_TIMEOUT)
    try:
        sock.connect(socket_path)
    except OSError:
        return None
    finally:
        sock.close()
    return socket_path


def add_device(
    name: str,
    host: str,
    token: str,
    *,
    protocol: str = "http",
    allow_unsecured: bool = False,
    port: Optional[int] = None,
) -> DeviceRecord:
    """Register a new device; fails if *name* already exists. Connectivity is probed first.

    ``allow_unsecured`` defaults to ``False``: HTTPS connections require a trusted
    certificate chain. Pass ``allow_unsecured=True`` only for self-signed certs on
    a trusted network.
    """
    _config.validate_name(name)
    _config.validate_host(host)
    _config.validate_token(token)
    _config.validate_protocol(protocol)
    if port is not None:
        port = int(port)
        if not 1 <= port <= 65535:
            raise ValueError(f"Port {port} out of range.")

    devices = _config.load_all()
    if name in devices:
        raise RecameraError(
            f"Device '{name}' already exists. Use update_device to modify it, or remove_device first."
        )
    probe_port = port if port is not None else (443 if protocol == "https" else 80)
    err = _probe(host, probe_port, token.strip(), protocol == "https", allow_unsecured)
    if err is not None:
        raise RecameraError(f"Device registration failed: {err}")

    entry: Dict[str, Any] = {
        "host": host.strip(),
        "token": token.strip(),
        "protocol": protocol,
        "allow_unsecured": bool(allow_unsecured),
    }
    if port is not None:
        entry["port"] = port
    devices[name] = entry
    _config.save_all(devices)
    return _config.resolve(name)


def update_device(
    device_name: str,
    *,
    host: Optional[str] = None,
    token: Optional[str] = None,
    protocol: Optional[str] = None,
    allow_unsecured: Optional[bool] = None,
    port: Optional[int] = None,
) -> DeviceRecord:
    """Update fields of an existing device; resulting credentials are re-probed before save."""
    _config.validate_name(device_name)
    devices = _config.load_all()
    if device_name not in devices:
        raise RecameraError(
            f"Device '{device_name}' not found. Use list_devices to inspect available profiles."
        )
    entry = dict(devices[device_name])
    if host is not None:
        _config.validate_host(host)
        entry["host"] = host.strip()
    if token is not None:
        _config.validate_token(token)
        entry["token"] = token.strip()
    if protocol is not None:
        _config.validate_protocol(protocol)
        entry["protocol"] = protocol
    if allow_unsecured is not None:
        entry["allow_unsecured"] = bool(allow_unsecured)
    if port is not None:
        port = int(port)
        if not 1 <= port <= 65535:
            raise ValueError(f"Port {port} out of range.")
        entry["port"] = port

    probe_port = entry.get("port") or (443 if entry.get("protocol") == "https" else 80)
    err = _probe(
        entry["host"],
        probe_port,
        entry["token"],
        entry.get("protocol") == "https",
        bool(entry.get("allow_unsecured", False)),
    )
    if err is not None:
        raise RecameraError(f"Device update failed: {err}")

    devices[device_name] = entry
    _config.save_all(devices)
    return _config.resolve(device_name)


def remove_device(device_name: str) -> bool:
    """Delete *device_name*; returns ``True`` if something was removed."""
    _config.validate_name(device_name)
    devices = _config.load_all()
    if device_name not in devices:
        return False
    del devices[device_name]
    _config.save_all(devices)
    return True


def get_device(device_name: str) -> Optional[DeviceRecord]:
    """Return the profile for *device_name*, or ``None``."""
    _config.validate_name(device_name)
    devices = _config.load_all()
    if device_name not in devices:
        return None
    return _config.resolve(device_name)


def list_devices() -> List[DeviceRecord]:
    """Every saved device, sorted by name (case-insensitive)."""
    return _config.list_records_on_disk()


COMMANDS = {
    "detect_local_device": detect_local_device,
    "add_device": add_device,
    "update_device": update_device,
    "remove_device": remove_device,
    "get_device": get_device,
    "list_devices": list_devices,
}
COMMAND_SCHEMAS = {
    "detect_local_device": {"required": set(), "optional": {"socket_path"}},
    "add_device": {
        "required": {"name", "host", "token"},
        "optional": {"protocol", "allow_unsecured", "port"},
    },
    "update_device": {
        "required": {"device_name"},
        "optional": {"host", "token", "protocol", "allow_unsecured", "port"},
    },
    "remove_device": {"required": {"device_name"}, "optional": set()},
    "get_device": {"required": {"device_name"}, "optional": set()},
    "list_devices": {"required": set(), "optional": set()},
}
