"""Result-push (notify) configuration API (``/notify/cfg``).

The pipeline is shared by the built-in vision inference and system sources
such as AcousticsLab. Secrets (passwords/tokens) are redacted on read: the
device returns them in cleartext, and they must not enter agent contexts.
"""

from __future__ import annotations

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from recamera_intellisense._cli import main

    raise SystemExit(main())

from typing import Any, Dict, Optional

from . import _config, _http
from ._errors import RecameraError

__all__ = ["get_notify_config", "set_notify_config"]

PATH_CFG = "/cgi-bin/entry.cgi/notify/cfg"

_MODE_NAMES = {0: "off", 1: "mqtt", 2: "http", 3: "uart"}
_REDACTED = "***"


def _redact(value: Any) -> Any:
    """Non-empty secret strings become ``"***"``."""
    return _REDACTED if isinstance(value, str) and value else value


def get_notify_config(device_name: Optional[str] = None) -> Dict[str, Any]:
    """Result-push configuration (secrets redacted).

    Shape: ``{mode, mode_name, mqtt, http, uart, templates}``; ``mode`` is
    0=off / 1=MQTT / 2=HTTP / 3=UART. ``password``/``token`` read back as
    ``"***"`` when set. Empty ``templates`` values select the built-in
    per-task defaults.
    """
    dev = _config.resolve(device_name)
    d = _http.get_json(dev, PATH_CFG)
    if d is None:
        d = {}  # codebase GET norm: tolerate an empty body
    if not isinstance(d, dict):
        raise RecameraError("get notify config failed: unexpected payload")
    mqtt = d.get("dMqtt") or {}
    http = d.get("dHttp") or {}
    # Wire quirk: MQTT spells its host field "sURL", HTTP "sUrl".
    uart = d.get("dUart") or {}
    tpl = d.get("dTemplate") or {}
    mode = int(d.get("iMode", 0))
    return {
        "mode": mode,
        "mode_name": _MODE_NAMES.get(mode, f"unknown({mode})"),
        "mqtt": {
            "url": mqtt.get("sURL", ""),
            "port": int(mqtt.get("iPort", 1883)),
            "client_id": mqtt.get("sClientId", ""),
            "username": mqtt.get("sUsername", ""),
            "password": _redact(mqtt.get("sPassword", "")),
            "topic": mqtt.get("sTopic", ""),
        },
        "http": {
            "url": http.get("sUrl", ""),
            "token": _redact(http.get("sToken", "")),
        },
        "uart": {
            "port": uart.get("sPort", ""),
            "port_dev": uart.get("sPortDev", ""),
        },
        "templates": {
            "classification": tpl.get("sClassification", ""),
            "detection": tpl.get("sDetection", ""),
            "keypoint": tpl.get("sKeypoint", ""),
            "segmentation": tpl.get("sSegmentation", ""),
            "tracking": tpl.get("sTracking", ""),
        },
    }


COMMANDS = {"get_notify_config": get_notify_config}

_MQTT_FIELDS = {
    "url": "sURL", "port": "iPort", "client_id": "sClientId",
    "username": "sUsername", "password": "sPassword", "topic": "sTopic",
}
_HTTP_FIELDS = {"url": "sUrl", "token": "sToken"}
_TEMPLATE_FIELDS = {
    "classification": "sClassification", "detection": "sDetection",
    "segmentation": "sSegmentation", "tracking": "sTracking",
    "keypoint": "sKeypoint",
}


def _merge_channel(raw_block: Any, changes: Any, field_map: Dict[str, str],
                   secret: Optional[str], section: str) -> Dict[str, Any]:
    """Merge caller `changes` onto the raw stored block so omitted fields
    (including secrets, which the read API redacts) survive the write."""
    if not isinstance(changes, dict):
        raise ValueError(f"{section} must be an object of fields {sorted(field_map)}")
    unknown = sorted(set(changes) - set(field_map))
    if unknown:
        raise ValueError(
            f"{section}: unknown fields {unknown}; allowed: {sorted(field_map)}")
    if secret and changes.get(secret) == _REDACTED:
        raise ValueError(
            f"{section}.{secret}={_REDACTED!r} is the redaction placeholder, not a "
            "secret — pass the real value, '' to clear, or omit the field to keep "
            "the stored one")
    merged = dict(raw_block) if isinstance(raw_block, dict) else {}
    for key, value in changes.items():
        if key == "port":
            if isinstance(value, bool) or not isinstance(value, int) \
                    or not 1 <= value <= 65535:
                raise ValueError(f"{section}.port must be an integer 1~65535")
        elif not isinstance(value, str):
            raise ValueError(f"{section}.{key} must be a string")
        merged[field_map[key]] = value
    return merged


def set_notify_config(
    device_name: Optional[str] = None,
    *,
    mode: Optional[int] = None,
    mqtt: Optional[Dict[str, Any]] = None,
    http: Optional[Dict[str, Any]] = None,
    templates: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Update the result-push configuration.

    `mqtt` accepts {url, port, client_id, username, password, topic},
    `http` {url, token}, `templates` {classification, detection, keypoint,
    segmentation, tracking} (empty string restores the built-in default).
    Fields omitted from a section keep their stored values — secrets are
    merged from the device's own config, so a redacted read followed by a
    write cannot clobber them. Empty sections (``{}``) are ignored.

    NOTE: the device restarts its notify service and recameraipc to apply,
    briefly interrupting streams/results/recording.
    """
    if mode is None and not mqtt and not http and not templates:
        raise ValueError("nothing to change: pass mode, mqtt, http, or templates")
    if mode is not None and (isinstance(mode, bool) or mode not in _MODE_NAMES):
        raise ValueError("mode must be 0 (off), 1 (MQTT), 2 (HTTP), or 3 (UART)")
    dev = _config.resolve(device_name)
    raw = _http.get_json(dev, PATH_CFG)
    raw = raw if isinstance(raw, dict) else {}
    payload: Dict[str, Any] = {}
    if mode is not None:
        payload["iMode"] = mode
    if mqtt:
        payload["dMqtt"] = _merge_channel(raw.get("dMqtt"), mqtt,
                                          _MQTT_FIELDS, "password", "mqtt")
    if http:
        payload["dHttp"] = _merge_channel(raw.get("dHttp"), http,
                                          _HTTP_FIELDS, "token", "http")
    if templates:
        if not isinstance(templates, dict):
            raise ValueError(f"templates must be an object of fields "
                             f"{sorted(_TEMPLATE_FIELDS)}")
        unknown = sorted(set(templates) - set(_TEMPLATE_FIELDS))
        if unknown:
            raise ValueError(
                f"templates: unknown fields {unknown}; allowed: "
                f"{sorted(_TEMPLATE_FIELDS)}")
        merged_t = dict(raw.get("dTemplate")) if isinstance(
            raw.get("dTemplate"), dict) else {}
        for key, value in templates.items():
            if not isinstance(value, str):
                raise ValueError(f"templates.{key} must be a string")
            merged_t[_TEMPLATE_FIELDS[key]] = value
        payload["dTemplate"] = merged_t
    # Mirror the server's merged-config requirements so mistakes fail here.
    merged_mode = mode if mode is not None else int(raw.get("iMode", 0) or 0)
    merged_mqtt = payload.get("dMqtt", raw.get("dMqtt")) or {}
    merged_http = payload.get("dHttp", raw.get("dHttp")) or {}
    if merged_mode == 1 and not str(merged_mqtt.get("sURL") or "").strip():
        raise ValueError("mode=1 (MQTT) requires mqtt.url")
    if merged_mode == 2 and not str(merged_http.get("sUrl") or "").strip():
        raise ValueError("mode=2 (HTTP) requires http.url")
    _http.expect_ok(_http.post_json(dev, PATH_CFG, payload=payload),
                    "set notify config")
    return {
        "changed": True,
        "mode": merged_mode,
        "mode_name": _MODE_NAMES.get(merged_mode, f"unknown({merged_mode})"),
        "note": "device restarts its notify service and recameraipc to apply "
                "(brief pipeline gap)",
    }


COMMANDS["set_notify_config"] = set_notify_config
