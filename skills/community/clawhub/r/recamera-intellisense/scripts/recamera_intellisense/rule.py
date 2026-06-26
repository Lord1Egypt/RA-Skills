"""Record rule system: config, schedule, and trigger tagged-union (``/record/rule/...``)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from . import _config, _http

__all__ = [
    "get_rule_system_info",
    "get_record_config",
    "set_record_config",
    "get_schedule_rule",
    "set_schedule_rule",
    "get_record_trigger",
    "set_record_trigger",
    "activate_http_trigger",
]

PATH_CONFIG = "/cgi-bin/entry.cgi/record/rule/config"
PATH_INFO = "/cgi-bin/entry.cgi/record/rule/info"
PATH_SCHEDULE = "/cgi-bin/entry.cgi/record/rule/schedule-rule-config"
PATH_RECORD_RULE = "/cgi-bin/entry.cgi/record/rule/record-rule-config"
PATH_HTTP_ACTIVATE = "/cgi-bin/entry.cgi/record/rule/http-rule-activate"


def get_rule_system_info(device_name: str) -> Dict[str, Any]:
    """Health / availability snapshot of the rule subsystem."""
    dev = _config.resolve(device_name)
    d = _http.get_json(dev, PATH_INFO) or {}
    return {
        "ready_for_new_event": bool(d.get("bReadyForNewEvent", False)),
        "last_event": _parse_event(d.get("dLastRuleEvent")),
        "last_event_owner": _parse_event_owner(d.get("dLastRuleEventOwner")),
        "available_gpios": {
            k: _parse_avail_gpio(v) for k, v in (d.get("dAvailableGPIOs") or {}).items()
        },
        "available_ttys": {
            k: _parse_avail_tty(v) for k, v in (d.get("dAvailableTTYs") or {}).items()
        },
        "media_paused": bool(d.get("bMediaPaused", False)),
        "video_clip_length_seconds": int(d.get("bVideoClipLengthSeconds", 0)),
    }


def _parse_event(v: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(v, dict):
        return None
    status = v.get("sStatus")
    ts = v.get("iTimestamp")
    if not isinstance(status, str) or not isinstance(ts, int):
        return None
    return {"status": status, "timestamp_unix_ms": ts}


def _parse_event_owner(v: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(v, dict):
        return None
    return {
        "rule_type": v.get("sRuleType", ""),
        "rule_id": v.get("sRuleID", ""),
        "timestamp_unix_ms": int(v.get("iTimestamp", 0)),
    }


def _parse_avail_gpio(v: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "num": int(v.get("iNum", 0)),
        "state": v.get("sState"),
        "capabilities": list(v.get("lCapabilities") or []),
        "level": v.get("sLevel"),
    }


def _parse_avail_tty(v: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "socket_path": v.get("sSocketPath", ""),
        "buffer_size": int(v.get("iBufferSize", 0)),
    }


def get_record_config(device_name: str) -> Dict[str, Any]:
    """Return ``{rule_enabled, writer: {format, interval_ms}}``."""
    dev = _config.resolve(device_name)
    d = _http.get_json(dev, PATH_CONFIG) or {}
    writer = d.get("dWriterConfig") or {}
    return {
        "rule_enabled": bool(d.get("bRuleEnabled", False)),
        "writer": {
            "format": writer.get("sFormat", ""),
            "interval_ms": int(writer.get("iIntervalMs", 0)),
        },
    }


def set_record_config(
    device_name: str,
    *,
    rule_enabled: bool,
    writer_format: str,
    writer_interval_ms: int = 0,
) -> None:
    """Enable/disable the rule pipeline and set the writer format (``JPG``/``MP4``/``RAW``)."""
    dev = _config.resolve(device_name)
    payload = {
        "bRuleEnabled": bool(rule_enabled),
        "dWriterConfig": {
            "sFormat": str(writer_format).upper(),
            "iIntervalMs": int(writer_interval_ms),
        },
    }
    resp = _http.post_json(dev, PATH_CONFIG, payload=payload)
    _http.expect_ok(resp, "set rule config")


def get_schedule_rule(device_name: str) -> Optional[List[Dict[str, str]]]:
    """Active-weekdays list, or ``None`` when the schedule is disabled."""
    dev = _config.resolve(device_name)
    d = _http.get_json(dev, PATH_SCHEDULE) or {}
    if not d.get("bEnabled"):
        return None
    ranges = []
    for r in d.get("lActiveWeekdays") or []:
        s = r.get("sStart")
        e = r.get("sEnd")
        if isinstance(s, str) and isinstance(e, str):
            ranges.append({"start": s, "end": e})
    return ranges or None


def set_schedule_rule(
    device_name: str,
    schedule: Optional[List[Dict[str, str]]] = None,
) -> None:
    """Pass ``None`` or ``[]`` (or omit) to disable (rule active 24/7)."""
    dev = _config.resolve(device_name)
    ranges = schedule or []
    enabled = bool(ranges)
    weekdays = [
        {"sStart": r["start"], "sEnd": r["end"]}
        for r in ranges
        if isinstance(r, dict) and "start" in r and "end" in r
    ]
    payload = {"bEnabled": enabled, "lActiveWeekdays": weekdays}
    resp = _http.post_json(dev, PATH_SCHEDULE, payload=payload)
    _http.expect_ok(resp, "set schedule rule")


_FULL_FRAME_REGION = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]


def get_record_trigger(device_name: str) -> Dict[str, Any]:
    """Return the current trigger as a tagged-union dict; see :func:`trigger_to_json` for each shape."""
    dev = _config.resolve(device_name)
    d = _http.get_json(dev, PATH_RECORD_RULE) or {}
    return parse_trigger(d)


def parse_trigger(d: Dict[str, Any]) -> Dict[str, Any]:
    """Decode a device trigger payload into the tagged-union form."""
    kind = d.get("sCurrentSelected", "").upper()
    if kind == "INFERENCE_SET":
        rules = [_parse_detection_rule(r) for r in (d.get("lInferenceSet") or [])]
        return {"kind": "inference_set", "rules": rules}
    if kind == "TIMER":
        t = d.get("dTimer") or {}
        return {"kind": "timer", "interval_seconds": int(t.get("iIntervalSeconds", 0))}
    if kind == "GPIO":
        g = d.get("dGPIO") or {}
        out: Dict[str, Any] = {
            "kind": "gpio",
            "state": g.get("sState", "FLOATING"),
            "signal": g.get("sSignal", "RISING"),
            "debounce_ms": int(g.get("iDebounceDurationMs", 0)),
        }
        if "sName" in g:
            out["name"] = g["sName"]
        if "iNum" in g:
            out["num"] = int(g["iNum"])
        return out
    if kind == "TTY":
        t = d.get("dTTY") or {}
        return {
            "kind": "tty",
            "name": t.get("sName", ""),
            "command": t.get("sCommand", ""),
        }
    if kind == "HTTP":
        return {"kind": "http"}
    if kind == "ALWAYS_ON":
        return {"kind": "always_on"}
    raise ValueError(f"Unknown trigger kind {kind!r}")


def _parse_detection_rule(v: Dict[str, Any]) -> Dict[str, Any]:
    confidence = v.get("lConfidenceFilter") or [0.0, 1.0]
    labels = [x for x in (v.get("lClassFilter") or []) if isinstance(x, str)]
    regions_raw = v.get("lRegionFilter")
    regions: Optional[List[List[List[float]]]] = None
    if isinstance(regions_raw, list):
        regions = []
        for r in regions_raw:
            poly = r.get("lPolygon") if isinstance(r, dict) else None
            if isinstance(poly, list):
                regions.append(
                    [[float(c) for c in pt] for pt in poly if isinstance(pt, list)]
                )
    return {
        "name": v.get("sID", ""),
        "debounce_times": int(v.get("iDebounceTimes", 0)),
        "confidence_range_filter": [float(c) for c in confidence],
        "label_filter": labels,
        "region_filter": regions,
    }


def _detection_rule_to_json(rule: Dict[str, Any]) -> Dict[str, Any]:
    regions = rule.get("region_filter")
    if not regions:
        # Empty/omitted region_filter means full-frame detection.
        regions = [_FULL_FRAME_REGION]
    confidence = list(rule.get("confidence_range_filter", [0.0, 1.0]))
    _validate_confidence_range(rule.get("name", ""), confidence)
    return {
        "sID": str(rule.get("name", "")),
        "iDebounceTimes": int(rule.get("debounce_times", 0)),
        "lConfidenceFilter": confidence,
        "lClassFilter": list(rule.get("label_filter", [])),
        "lRegionFilter": [{"lPolygon": poly} for poly in regions],
    }


def _validate_confidence_range(rule_name: Any, confidence: List[Any]) -> None:
    """Enforce ``confidence_range_filter = [min, max]`` with both ∈ [0, 1] and min ≤ max."""
    label = f"rule {rule_name!r}" if rule_name else "rule"
    if not isinstance(confidence, list) or len(confidence) != 2:
        raise ValueError(
            f"{label}: confidence_range_filter must be exactly [min, max]; "
            f"got {len(confidence) if isinstance(confidence, list) else type(confidence).__name__} value(s)"
        )
    try:
        lo, hi = float(confidence[0]), float(confidence[1])
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"{label}: confidence_range_filter entries must be numeric; got {confidence!r}"
        ) from exc
    if not (0.0 <= lo <= 1.0) or not (0.0 <= hi <= 1.0):
        raise ValueError(
            f"{label}: confidence_range_filter values must be within [0.0, 1.0]; got [{lo}, {hi}]"
        )
    if lo > hi:
        raise ValueError(
            f"{label}: confidence_range_filter min ({lo}) must be <= max ({hi})"
        )


_TRIGGER_SIBLING_KEYS = ("lInferenceSet", "dTimer", "dGPIO", "dTTY")


def _trigger_patch(trigger: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
    """Return ``(sCurrentSelected, {key: value, ...})`` for *trigger*.

    The patch dict contains only the sub-object(s) owned by the selected
    kind. HTTP / ALWAYS_ON return an empty patch — they just flip the tag.
    """
    kind = str(trigger.get("kind", "")).lower()
    if kind == "inference_set":
        rules = trigger.get("rules") or []
        return "INFERENCE_SET", {
            "lInferenceSet": [_detection_rule_to_json(r) for r in rules],
        }
    if kind == "timer":
        return "TIMER", {
            "dTimer": {"iIntervalSeconds": int(trigger.get("interval_seconds", 0))},
        }
    if kind == "gpio":
        name = trigger.get("name")
        num = trigger.get("num")
        if name is None and num is None:
            raise ValueError("GPIO trigger requires either 'name' or 'num'.")
        gpio: Dict[str, Any] = {}
        if name is not None:
            gpio["sName"] = str(name)
        if num is not None:
            gpio["iNum"] = int(num)
        gpio["sState"] = str(trigger.get("state", "FLOATING"))
        gpio["sSignal"] = str(trigger.get("signal", "RISING"))
        gpio["iDebounceDurationMs"] = int(trigger.get("debounce_ms", 0))
        return "GPIO", {"dGPIO": gpio}
    if kind == "tty":
        name = str(trigger.get("name", "")).strip()
        command = str(trigger.get("command", "")).strip()
        if not name or not command:
            raise ValueError("TTY trigger requires non-empty 'name' and 'command'.")
        return "TTY", {"dTTY": {"sName": name, "sCommand": command}}
    if kind == "http":
        return "HTTP", {}
    if kind == "always_on":
        return "ALWAYS_ON", {}
    raise ValueError(f"Unknown trigger kind {kind!r}")


def _merge_trigger_payload(
    current: Optional[Dict[str, Any]], trigger: Dict[str, Any]
) -> Dict[str, Any]:
    """Layer the *trigger* patch on top of *current* config sibling fields.

    Other trigger kinds' remembered sub-objects (e.g. ``dGPIO`` when switching
    to ``inference_set``) are copied forward so other clients — and later
    switches back — don't lose state. Only allowlisted keys are carried to
    avoid round-tripping server-only metadata.
    """
    kind, patch = _trigger_patch(trigger)
    out: Dict[str, Any] = {}
    if isinstance(current, dict):
        for key in _TRIGGER_SIBLING_KEYS:
            if key in current:
                out[key] = current[key]
    out["sCurrentSelected"] = kind
    out.update(patch)
    return out


def trigger_to_json(trigger: Dict[str, Any]) -> Dict[str, Any]:
    """Encode a tagged-union trigger as a standalone full-replace payload.

    Accepted shapes::

        {"kind": "timer", "interval_seconds": 60}
        {"kind": "gpio", "name": "GPIO_01", "state": "FLOATING", "signal": "RISING", "debounce_ms": 0}
        {"kind": "inference_set", "rules": [...]}
        {"kind": "http"} | {"kind": "always_on"}
        {"kind": "tty", "name": "...", "command": "..."}

    Prefer :func:`set_record_trigger`, which performs a read-modify-write so
    other trigger kinds' remembered settings survive a kind switch.
    """
    return _merge_trigger_payload(None, trigger)


def set_record_trigger(device_name: str, trigger: Dict[str, Any]) -> None:
    """Install *trigger* while preserving other kinds' remembered settings.

    Fetches the current ``record-rule-config``, copies the sibling sub-objects
    (``lInferenceSet``, ``dTimer``, ``dGPIO``, ``dTTY``) forward, overwrites
    only ``sCurrentSelected`` and the sub-object for the selected kind, then
    POSTs. A GET failure degrades gracefully to a full-replace payload so
    this still works on a freshly provisioned device.

    See :func:`trigger_to_json` for accepted trigger shapes.
    """
    dev = _config.resolve(device_name)
    try:
        current = _http.get_json(dev, PATH_RECORD_RULE)
    except Exception:
        current = None
    payload = _merge_trigger_payload(
        current if isinstance(current, dict) else None, trigger
    )
    resp = _http.post_json(dev, PATH_RECORD_RULE, payload=payload)
    _http.expect_ok(resp, "set record trigger")


def activate_http_trigger(device_name: str) -> None:
    """Fire a one-shot record event on an HTTP-kind trigger."""
    dev = _config.resolve(device_name)
    resp = _http.post_json(dev, PATH_HTTP_ACTIVATE)
    _http.expect_ok(resp, "activate HTTP trigger")


COMMANDS = {
    "get_rule_system_info": get_rule_system_info,
    "get_record_config": get_record_config,
    "set_record_config": set_record_config,
    "get_schedule_rule": get_schedule_rule,
    "set_schedule_rule": set_schedule_rule,
    "get_record_trigger": get_record_trigger,
    "set_record_trigger": set_record_trigger,
    "activate_http_trigger": activate_http_trigger,
}
COMMAND_SCHEMAS = {
    "get_rule_system_info": {"required": {"device_name"}, "optional": set()},
    "get_record_config": {"required": {"device_name"}, "optional": set()},
    "set_record_config": {
        "required": {"device_name", "rule_enabled", "writer_format"},
        "optional": {"writer_interval_ms"},
    },
    "get_schedule_rule": {"required": {"device_name"}, "optional": set()},
    "set_schedule_rule": {"required": {"device_name"}, "optional": {"schedule"}},
    "get_record_trigger": {"required": {"device_name"}, "optional": set()},
    "set_record_trigger": {"required": {"device_name", "trigger"}, "optional": set()},
    "activate_http_trigger": {"required": {"device_name"}, "optional": set()},
}
