"""Device profile CRUD (mirrors the MCP server's ``Device``-prefixed tools)."""

from __future__ import annotations

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from recamera_intellisense._cli import main

    raise SystemExit(main())

import http.client
import socket
from typing import Any, Dict, List, Optional, cast

from . import _config, _http
from ._coerce import to_bool
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


def _public(record: DeviceRecord) -> DeviceRecord:
    """External views never expose the bearer token (transport keeps it internally)."""
    return cast(DeviceRecord, {k: v for k, v in record.items() if k != "token"})


# Connectivity probe

_PROBE_PATH = "/api/v1/recamera-generate-204"
_DEFAULT_PROBE_TIMEOUT = 2.0


def _probe(
    host: str,
    port: int,
    token: Optional[str],
    use_tls: bool,
    allow_unsecured: bool,
    timeout: float,
    *,
    auth_error_is_reachable: bool = False,
) -> Optional[str]:
    """Return `None` on success or a human-readable error otherwise.

    With *auth_error_is_reachable*, HTTP 401/403 counts as reachable
    (used by detection); otherwise it is reported as an auth failure.
    """
    try:
        connect_host = host.strip()
        try:
            socket.inet_pton(socket.AF_INET6, connect_host)
            host_header = f"[{connect_host}]"
        except OSError:
            host_header = connect_host
        if use_tls:
            if allow_unsecured:
                ctx = _http.insecure_ssl_context(host)
            else:
                import ssl

                ctx = ssl.create_default_context()
            conn: http.client.HTTPConnection = http.client.HTTPSConnection(
                connect_host, port, timeout=timeout, context=ctx
            )
        else:
            conn = http.client.HTTPConnection(connect_host, port, timeout=timeout)
        headers = {"Host": host_header}
        if token:
            headers["Authorization"] = token
        try:
            conn.request("GET", _PROBE_PATH, headers=headers)
            resp = conn.getresponse()
            status = resp.status
        finally:
            conn.close()
        if 200 <= status < 400:
            return None
        if status in (401, 403):
            if auth_error_is_reachable:
                return None
            return f"Authentication failed (HTTP {status}). Verify the token."
        return f"Unexpected response from device (HTTP {status})."
    except (socket.timeout, TimeoutError):
        return f"Connection to {host}:{port} timed out after {timeout:.0f}s."
    except ConnectionRefusedError:
        return f"Connection refused by {host}:{port}."
    except OSError as exc:
        return f"Unable to connect to {host}:{port} — {exc}."


def detect_local_device(
    host: str,
    port: Optional[int] = None,
    *,
    token: str = "",
    timeout: float = _DEFAULT_PROBE_TIMEOUT,
) -> Optional[Dict[str, Any]]:
    """Probe *host* for a reCamera HTTP/HTTPS API.

    Tries HTTPS (validated), HTTPS (self-signed), then HTTP. Returns `None`
    if no reachable API is found. Auth failures count as "detected".
    """
    _config.validate_host(host)
    _config.validate_token(token)
    host = host.strip()
    token = token.strip() or ""
    if port is not None:
        port = int(port)
        if not 1 <= port <= 65535:
            raise ValueError(f"Port {port} out of range.")
    timeout = float(timeout)
    if timeout <= 0:
        raise ValueError("timeout must be positive.")

    probes = [
        ("https", port or 443, False),
        ("https", port or 443, True),
        ("http", port or 80, False),
    ]
    for protocol, probe_port, allow_unsecured in probes:
        if (
            _probe(
                host,
                probe_port,
                token,
                use_tls=(protocol == "https"),
                allow_unsecured=allow_unsecured,
                timeout=timeout,
                auth_error_is_reachable=True,
            )
            is None
        ):
            return {
                "host": host,
                "port": probe_port,
                "protocol": protocol,
                "allow_unsecured": allow_unsecured,
            }
    return None


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

    `token` may be empty for local/trusted devices. `allow_unsecured=True`
    is required for local HTTPS devices that use self-signed certificates.
    """
    _config.validate_name(name)
    _config.validate_host(host)
    _config.validate_token(token)
    _config.validate_protocol(protocol)
    allow_unsecured = to_bool(allow_unsecured, "allow_unsecured")
    if port is not None:
        port = int(port)
        if not 1 <= port <= 65535:
            raise ValueError(f"Port {port} out of range.")

    devices = _config.load_all()
    if name in devices:
        raise RecameraError(
            f"Device '{name}' already exists. Use update_device to modify it, "
            "or remove_device first."
        )
    probe_port = port if port is not None else (443 if protocol == "https" else 80)
    err = _probe(
        host,
        probe_port,
        token.strip(),
        protocol == "https",
        allow_unsecured,
        timeout=_DEFAULT_PROBE_TIMEOUT,
    )
    if err is not None:
        raise RecameraError(f"Device registration failed: {err}")

    entry: Dict[str, Any] = {
        "host": host.strip(),
        "token": token.strip(),
        "protocol": protocol,
        "allow_unsecured": allow_unsecured,
    }
    if port is not None:
        entry["port"] = port
    devices[name] = entry
    _config.save_all(devices)
    return _public(_config.resolve(name))


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
        entry["allow_unsecured"] = to_bool(allow_unsecured, "allow_unsecured")
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
        timeout=_DEFAULT_PROBE_TIMEOUT,
    )
    if err is not None:
        raise RecameraError(f"Device update failed: {err}")

    devices[device_name] = entry
    _config.save_all(devices)
    return _public(_config.resolve(device_name))


def remove_device(device_name: str) -> bool:
    """Delete *device_name*; returns `True` if something was removed."""
    _config.validate_name(device_name)
    devices = _config.load_all()
    if device_name not in devices:
        return False
    del devices[device_name]
    _config.save_all(devices)
    return True


def get_device(device_name: str) -> Optional[DeviceRecord]:
    """Return the profile for *device_name*, or `None`."""
    _config.validate_name(device_name)
    devices = _config.load_all()
    if device_name not in devices:
        return None
    return _public(_config.resolve(device_name))


def list_devices() -> List[DeviceRecord]:
    """Every saved device, sorted by name (case-insensitive)."""
    return [_public(r) for r in _config.list_records_on_disk()]


COMMANDS = {
    "detect_local_device": detect_local_device,
    "add_device": add_device,
    "update_device": update_device,
    "remove_device": remove_device,
    "get_device": get_device,
    "list_devices": list_devices,
}
