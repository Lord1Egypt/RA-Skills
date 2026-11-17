from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

try:
    from . import camera_proto
except ImportError:
    import camera_proto

try:
    from .device_mgmt import resolve_target, CameraConfig, _is_non_sk_camera, _unsupported_protocol_message
except ImportError:
    from device_mgmt import resolve_target, CameraConfig, _is_non_sk_camera, _unsupported_protocol_message

try:
    from .illumination import (
        _envelope,
        _sk_err,
        _sk_resolve_camera,
        _coerce_int,
        _merge_capabilities,
    )
except ImportError:
    from illumination import (
        _envelope,
        _sk_err,
        _sk_resolve_camera,
        _coerce_int,
        _merge_capabilities,
    )

try:
    from ._argnorm import coerce_str
except ImportError:
    from _argnorm import coerce_str

class TrackingAction(str, Enum):
    QUERY = "get"
    SET = "set"

class DetectType(str, Enum):
    HUMAN = "human"
    VEHICLE = "vehicle"
    AREA = "area"
    MOTION = "motion"
    LINE = "line"
    ALL = "all"

_SK_TRACKING_PORT = 9010
_SK_TRACKING_TIMEOUT = 3.0

_SETTABLE_FIELDS = {"enable", "tracking", "level"}

_TRACKING_LABELS = {
    "enable": "Enable switch",
    "tracking": "Tracking",
    "indoor": "Scene mode",
    "thresh": "Sensitivity",
    "level": "Sensitivity level",
    "screenenable": "Target marker",
    "blink": "Box blinking",
    "alarm_enable": "Audio alarm",
    "alarm_type": "Alarm type",
    "white_light": "White-light alarm",
    "duration": "White-light duration",
    "timestrategy": "Detection schedule",
    "humandistance": "Human size",
    "drag": "Target marker display",
    "mbdesc": "Detection region",
    "distance": "Target size",
    "object": "Target type",
    "trigger": "Trigger target",
    "idenable": "License plate detection",

    "x0": "Line start X", "y0": "Line start Y",
    "x1": "Line end X", "y1": "Line end Y",
    "x2": "Direction start X", "y2": "Direction start Y",
    "x3": "Direction end X", "y3": "Direction end Y",
    "dir": "Detection direction",
    "enter_alarm_enable": "Enter alarm",
    "enter_alarm_type": "Enter alarm type",
    "leave_alarm_enable": "Leave alarm",
    "leave_alarm_type": "Leave alarm type",

    "dx0": "Direction start X (point A)", "dy0": "Direction start Y (point A)",
    "dx1": "Direction end X (point B)", "dy1": "Direction end Y (point B)",
    "AtoB_alarm_enable": "A→B alarm",
    "AtoB_alarm_type": "A→B alarm type",
    "BtoA_alarm_enable": "B→A alarm",
    "BtoA_alarm_type": "B→A alarm type",
}

_TRACKING_VALUE_TEXTS = {
    "enable": {0: "Off", 1: "On"},
    "tracking": {0: "Off", 1: "On"},
    "screenenable": {0: "Off", 1: "On"},
    "blink": {0: "Off", 1: "Blinking"},
    "drag": {0: "Hidden", 1: "Shown"},
    "alarm_enable": {0: "Off", 1: "On"},
    "white_light": {0: "Off", 1: "On"},
    "idenable": {0: "Off", 1: "On"},
    "enter_alarm_enable": {0: "Off", 1: "On"},
    "leave_alarm_enable": {0: "Off", 1: "On"},
    "AtoB_alarm_enable": {0: "Off", 1: "On"},
    "BtoA_alarm_enable": {0: "Off", 1: "On"},
    "indoor": {0: "Outdoor mode", 1: "Indoor mode", 2: "Outdoor (person+vehicle)"},
    "level": {0: "Off", 1: "Low", 2: "Medium", 3: "High"},
    "dir": {0: "Enter region", 1: "Leave region", 2: "Both directions"},
}

@dataclass
class TrackingQueryResult:
    ok: bool
    camera: str = ""
    channel: str = "sk"
    human_capabilities: List[Dict[str, Any]] = field(default_factory=list)
    vehicle_capabilities: List[Dict[str, Any]] = field(default_factory=list)
    area_capabilities: List[Dict[str, Any]] = field(default_factory=list)
    motion_capabilities: List[Dict[str, Any]] = field(default_factory=list)
    line_capabilities: List[Dict[str, Any]] = field(default_factory=list)
    human_current: Dict[str, Any] = field(default_factory=dict)
    vehicle_current: Dict[str, Any] = field(default_factory=dict)
    area_current: Dict[str, Any] = field(default_factory=dict)
    motion_current: Dict[str, Any] = field(default_factory=dict)
    line_current: Dict[str, Any] = field(default_factory=dict)
    error_code: str = ""
    message: str = ""
    hint: str = ""
    needs_input: List[str] = field(default_factory=list)

@dataclass
class TrackingSetResult:
    ok: bool
    camera: str = ""
    channel: str = "sk"
    detect_type: str = ""
    updated: Dict[str, Any] = field(default_factory=dict)
    current: Dict[str, Any] = field(default_factory=dict)
    message: str = ""
    error_code: str = ""
    hint: str = ""
    needs_input: List[str] = field(default_factory=list)

_RESP_HEAD = {"service_type", "msg_id", "cmd_name", "ver", "code", "msg",
              "channel", "sequence"}

def _sk_human_option(cam) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_get_option(
        camera_proto.DETECT_HUMAN, cam.ip, cam.sn_code, cam.username, cam.password,
        _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    caps = resp.get("humandetect")
    _ok = camera_proto.code_ok(resp.get("code", "")) and isinstance(caps, list)
    return {"ok": _ok, "capabilities": caps if isinstance(caps, list) else [],
            "code": resp.get("code", ""), "status": status, "raw": resp}

def _sk_human_cur(cam) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_get(
        camera_proto.DETECT_HUMAN, cam.ip, cam.sn_code, cam.username, cam.password,
        _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    current = {k: v for k, v in resp.items() if k not in _RESP_HEAD}
    _ok = camera_proto.code_ok(resp.get("code", ""))
    return {"ok": _ok, "current": current,
            "code": resp.get("code", ""), "status": status, "raw": resp}

def _sk_human_set(cam, payload: Dict[str, Any]) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_set(
        camera_proto.DETECT_HUMAN, cam.ip, cam.sn_code, cam.username, cam.password,
        payload, _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    _ok = camera_proto.code_ok(resp.get("code", ""))
    return {"ok": _ok, "code": resp.get("code", ""), "msg": resp.get("msg", ""),
            "status": status, "raw": resp}

def _sk_vehicle_option(cam) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_get_option(
        camera_proto.DETECT_VEHICLE, cam.ip, cam.sn_code, cam.username, cam.password,
        _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    caps = resp.get("objectdetect")
    _ok = camera_proto.code_ok(resp.get("code", "")) and isinstance(caps, list)
    return {"ok": _ok, "capabilities": caps if isinstance(caps, list) else [],
            "code": resp.get("code", ""), "status": status, "raw": resp}

def _sk_vehicle_cur(cam) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_get(
        camera_proto.DETECT_VEHICLE, cam.ip, cam.sn_code, cam.username, cam.password,
        _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    current = {k: v for k, v in resp.items() if k not in _RESP_HEAD}
    _ok = camera_proto.code_ok(resp.get("code", ""))
    return {"ok": _ok, "current": current,
            "code": resp.get("code", ""), "status": status, "raw": resp}

def _sk_vehicle_set(cam, payload: Dict[str, Any]) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_set(
        camera_proto.DETECT_VEHICLE, cam.ip, cam.sn_code, cam.username, cam.password,
        payload, _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    _ok = camera_proto.code_ok(resp.get("code", ""))
    return {"ok": _ok, "code": resp.get("code", ""), "msg": resp.get("msg", ""),
            "status": status, "raw": resp}

def _sk_area_option(cam) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_get_option(
        camera_proto.DETECT_REGION, cam.ip, cam.sn_code, cam.username, cam.password,
        _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    caps = resp.get("vgrectdetect")
    _ok = camera_proto.code_ok(resp.get("code", "")) and isinstance(caps, list)
    return {"ok": _ok, "capabilities": caps if isinstance(caps, list) else [],
            "code": resp.get("code", ""), "status": status, "raw": resp}

def _sk_area_cur(cam) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_get(
        camera_proto.DETECT_REGION, cam.ip, cam.sn_code, cam.username, cam.password,
        _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    current = {k: v for k, v in resp.items() if k not in _RESP_HEAD}
    _ok = camera_proto.code_ok(resp.get("code", ""))
    return {"ok": _ok, "current": current,
            "code": resp.get("code", ""), "status": status, "raw": resp}

def _sk_area_set(cam, payload: Dict[str, Any]) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_set(
        camera_proto.DETECT_REGION, cam.ip, cam.sn_code, cam.username, cam.password,
        payload, _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    _ok = camera_proto.code_ok(resp.get("code", ""))
    return {"ok": _ok, "code": resp.get("code", ""), "msg": resp.get("msg", ""),
            "status": status, "raw": resp}

def _sk_motion_option(cam) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_get_option(
        camera_proto.DETECT_MOTION, cam.ip, cam.sn_code, cam.username, cam.password,
        _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    caps = resp.get("motiondetect")
    _ok = camera_proto.code_ok(resp.get("code", "")) and isinstance(caps, list)
    return {"ok": _ok, "capabilities": caps if isinstance(caps, list) else [],
            "code": resp.get("code", ""), "status": status, "raw": resp}

def _sk_motion_cur(cam) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_get(
        camera_proto.DETECT_MOTION, cam.ip, cam.sn_code, cam.username, cam.password,
        _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    current = {k: v for k, v in resp.items() if k not in _RESP_HEAD}
    _ok = camera_proto.code_ok(resp.get("code", ""))
    return {"ok": _ok, "current": current,
            "code": resp.get("code", ""), "status": status, "raw": resp}

def _sk_motion_set(cam, payload: Dict[str, Any]) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_set(
        camera_proto.DETECT_MOTION, cam.ip, cam.sn_code, cam.username, cam.password,
        payload, _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    _ok = camera_proto.code_ok(resp.get("code", ""))
    return {"ok": _ok, "code": resp.get("code", ""), "msg": resp.get("msg", ""),
            "status": status, "raw": resp}

def _sk_line_option(cam) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_get_option(
        camera_proto.DETECT_LINE, cam.ip, cam.sn_code, cam.username, cam.password,
        _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    caps = resp.get("vglinedetect")
    _ok = camera_proto.code_ok(resp.get("code", "")) and isinstance(caps, list)
    return {"ok": _ok, "capabilities": caps if isinstance(caps, list) else [],
            "code": resp.get("code", ""), "status": status, "raw": resp}

def _sk_line_cur(cam) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_get(
        camera_proto.DETECT_LINE, cam.ip, cam.sn_code, cam.username, cam.password,
        _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    current = {k: v for k, v in resp.items() if k not in _RESP_HEAD}
    _ok = camera_proto.code_ok(resp.get("code", ""))
    return {"ok": _ok, "current": current,
            "code": resp.get("code", ""), "status": status, "raw": resp}

def _sk_line_set(cam, payload: Dict[str, Any]) -> Dict[str, Any]:
    ok, resp, status = _envelope(camera_proto.detect_set(
        camera_proto.DETECT_LINE, cam.ip, cam.sn_code, cam.username, cam.password,
        payload, _SK_TRACKING_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": status}
    _ok = camera_proto.code_ok(resp.get("code", ""))
    return {"ok": _ok, "code": resp.get("code", ""), "msg": resp.get("msg", ""),
            "status": status, "raw": resp}

def big_tracking_query(
    name: Optional[str] = None,
    detect_type: str = "all",
    answers: Optional[Dict[str, Any]] = None,
) -> TrackingQueryResult:
    err, cam = _sk_resolve_camera(name, answers, TrackingQueryResult)
    if err:
        return err

    dt = detect_type.lower() if detect_type else "all"

    result = TrackingQueryResult(ok=True, camera=cam.name, channel="sk")

    if dt in ("all", "human"):
        opt = _sk_human_option(cam)
        if not opt["ok"]:
            if opt.get("status") is None:
                return _sk_err(TrackingQueryResult, "DEVICE_UNREACHABLE",
                                 f"Cannot connect to {cam.ip}:{_SK_TRACKING_PORT} (SK HTTP no response)",
                                 "Check the camera is online and reachable", camera=cam.name)
        else:
            cur = _sk_human_cur(cam)
            if cur["ok"]:
                result.human_capabilities = [
                    c for c in _merge_capabilities(
                        opt["capabilities"], cur["current"],
                        _TRACKING_LABELS, _TRACKING_VALUE_TEXTS)
                    if c.get("name") in _SETTABLE_FIELDS]
                result.human_current = {
                    k: v for k, v in cur["current"].items() if k in _SETTABLE_FIELDS}

    if dt in ("all", "vehicle"):
        opt = _sk_vehicle_option(cam)
        if not opt["ok"]:
            if opt.get("status") is None:
                return _sk_err(TrackingQueryResult, "DEVICE_UNREACHABLE",
                                 f"Cannot connect to {cam.ip}:{_SK_TRACKING_PORT} (SK HTTP no response)",
                                 "Check the camera is online and reachable", camera=cam.name)
        else:
            cur = _sk_vehicle_cur(cam)
            if cur["ok"]:
                result.vehicle_capabilities = [
                    c for c in _merge_capabilities(
                        opt["capabilities"], cur["current"],
                        _TRACKING_LABELS, _TRACKING_VALUE_TEXTS)
                    if c.get("name") in _SETTABLE_FIELDS]
                result.vehicle_current = {
                    k: v for k, v in cur["current"].items() if k in _SETTABLE_FIELDS}

    if dt in ("all", "area"):
        opt = _sk_area_option(cam)
        if not opt["ok"]:
            if opt.get("status") is None:
                return _sk_err(TrackingQueryResult, "DEVICE_UNREACHABLE",
                                 f"Cannot connect to {cam.ip}:{_SK_TRACKING_PORT} (SK HTTP no response)",
                                 "Check the camera is online and reachable", camera=cam.name)
        else:
            cur = _sk_area_cur(cam)
            if cur["ok"]:
                result.area_capabilities = [
                    c for c in _merge_capabilities(
                        opt["capabilities"], cur["current"],
                        _TRACKING_LABELS, _TRACKING_VALUE_TEXTS)
                    if c.get("name") in _SETTABLE_FIELDS]
                result.area_current = {
                    k: v for k, v in cur["current"].items() if k in _SETTABLE_FIELDS}

    if dt in ("all", "motion"):
        opt = _sk_motion_option(cam)
        if not opt["ok"]:
            if opt.get("status") is None:
                return _sk_err(TrackingQueryResult, "DEVICE_UNREACHABLE",
                                 f"Cannot connect to {cam.ip}:{_SK_TRACKING_PORT} (SK HTTP no response)",
                                 "Check the camera is online and reachable", camera=cam.name)
        else:
            cur = _sk_motion_cur(cam)
            if cur["ok"]:
                result.motion_capabilities = [
                    c for c in _merge_capabilities(
                        opt["capabilities"], cur["current"],
                        _TRACKING_LABELS, _TRACKING_VALUE_TEXTS)
                    if c.get("name") in _SETTABLE_FIELDS]
                result.motion_current = {
                    k: v for k, v in cur["current"].items() if k in _SETTABLE_FIELDS}

    if dt in ("all", "line"):
        opt = _sk_line_option(cam)
        if not opt["ok"]:
            if opt.get("status") is None:
                return _sk_err(TrackingQueryResult, "DEVICE_UNREACHABLE",
                                 f"Cannot connect to {cam.ip}:{_SK_TRACKING_PORT} (SK HTTP no response)",
                                 "Check the camera is online and reachable", camera=cam.name)
        else:
            cur = _sk_line_cur(cam)
            if cur["ok"]:
                result.line_capabilities = [
                    c for c in _merge_capabilities(
                        opt["capabilities"], cur["current"],
                        _TRACKING_LABELS, _TRACKING_VALUE_TEXTS)
                    if c.get("name") in _SETTABLE_FIELDS]
                result.line_current = {
                    k: v for k, v in cur["current"].items() if k in _SETTABLE_FIELDS}

    result.message = (f"Detection query complete: "
                      f"human={len(result.human_capabilities)}, "
                      f"vehicle={len(result.vehicle_capabilities)}, "
                      f"area={len(result.area_capabilities)}, "
                      f"motion={len(result.motion_capabilities)}, "
                      f"line={len(result.line_capabilities)}")
    return result

def big_tracking_set(
    name: Optional[str] = None,
    detect_type: str = "human",
    enable: Optional[bool] = None,
    tracking: Optional[bool] = None,
    sensitivity_level: Optional[int] = None,
    answers: Optional[Dict[str, Any]] = None,
) -> TrackingSetResult:

    updates: Dict[str, Any] = {}
    if enable is not None:
        updates["enable"] = 1 if enable else 0
    if tracking is not None:
        updates["tracking"] = 1 if tracking else 0
    if sensitivity_level is not None:
        updates["level"] = sensitivity_level
    if not updates:
        return _sk_err(TrackingSetResult, "NO_PARAMS",
                       "No parameters provided to modify",
                       "Pass at least enable or tracking; call big_tracking_query first to see settable fields")

    err, cam = _sk_resolve_camera(name, answers, TrackingSetResult)
    if err:
        return err

    dt = detect_type.lower() if detect_type else "human"
    if dt not in ("human", "vehicle", "area", "motion", "line"):
        return _sk_err(TrackingSetResult, "INVALID_DETECT_TYPE",
                       f"Unsupported detection type: {detect_type}",
                       "Supported: human (person tracking) / vehicle (vehicle tracking) / area (region detection) / motion (motion detection) / line (line-crossing detection)")

    if dt in ("area", "line") and tracking is not None:
        updates.pop("tracking", None)

    if dt == "human":
        option_fn, cur_fn, set_fn = _sk_human_option, _sk_human_cur, _sk_human_set
    elif dt == "vehicle":
        option_fn, cur_fn, set_fn = _sk_vehicle_option, _sk_vehicle_cur, _sk_vehicle_set
    elif dt == "area":
        option_fn, cur_fn, set_fn = _sk_area_option, _sk_area_cur, _sk_area_set
    elif dt == "motion":
        option_fn, cur_fn, set_fn = _sk_motion_option, _sk_motion_cur, _sk_motion_set
    else:
        option_fn, cur_fn, set_fn = _sk_line_option, _sk_line_cur, _sk_line_set

    opt = option_fn(cam)
    if not opt["ok"]:
        if opt.get("status") is None:
            return _sk_err(TrackingSetResult, "DEVICE_UNREACHABLE",
                           f"Cannot connect to {cam.ip}:{_SK_TRACKING_PORT} (SK HTTP no response)",
                           camera=cam.name)
        return _sk_err(TrackingSetResult, "OPTION_QUERY_FAILED",
                       f"Failed to query {dt} detection capabilities (code={opt.get('code') or '404'})",
                       camera=cam.name)
    cap_map: Dict[str, dict] = {}
    for item in opt["capabilities"]:
        if isinstance(item, dict) and item.get("name"):
            cap_map[str(item["name"])] = item

    for k, v in updates.items():
        item = cap_map.get(k)
        if item is None:
            return _sk_err(TrackingSetResult, "PARAM_NOT_SUPPORTED",
                           f"Camera does not support {dt} detection parameter {k}",
                           f"Supported parameters: {', '.join(sorted(cap_map)) or 'none'}",
                           camera=cam.name)
        specs = item.get("specs") or {}
        lo, hi = _coerce_int(specs.get("min")), _coerce_int(specs.get("max"))
        if lo is not None and hi is not None and not (lo <= v <= hi):
            return _sk_err(TrackingSetResult, "PARAM_OUT_OF_RANGE",
                           f"{k}={v} out of allowed range {lo}-{hi}", camera=cam.name)

    base = cur_fn(cam)
    if not base["ok"]:
        if base.get("status") is None:
            return _sk_err(TrackingSetResult, "DEVICE_UNREACHABLE",
                           f"Cannot connect to {cam.ip}:{_SK_TRACKING_PORT} (SK HTTP no response)",
                           camera=cam.name)
        return _sk_err(TrackingSetResult, "CURRENT_QUERY_FAILED",
                       f"Failed to query current {dt} detection values (code={base.get('code')})",
                       camera=cam.name)

    payload = dict(base["current"])
    payload.update(updates)

    set_result = set_fn(cam, payload)
    if not set_result["ok"]:
        if set_result.get("status") is None:
            return _sk_err(TrackingSetResult, "DEVICE_UNREACHABLE",
                           f"Cannot connect to {cam.ip}:{_SK_TRACKING_PORT} (SK HTTP no response)",
                           camera=cam.name)
        return _sk_err(TrackingSetResult, "SET_FAILED",
                       f"{dt} detection set command failed (code={set_result.get('code')} "
                       f"msg={set_result.get('msg')})",
                       camera=cam.name)

    rb = cur_fn(cam)
    full_cur = rb["current"] if rb["ok"] else dict(payload)
    cur = {k: full_cur[k] for k in _SETTABLE_FIELDS if k in full_cur}
    updated = {k: cur[k] for k in updates if k in cur}

    type_names = {"human": "Human tracking", "vehicle": "Vehicle tracking", "area": "Region detection",
                  "motion": "Motion detection", "line": "Line-crossing detection"}
    return TrackingSetResult(
        ok=True, camera=cam.name, channel="sk", detect_type=dt,
        updated=updated, current=cur,
        message=f"{type_names.get(dt, dt)} parameters applied: {updated}")

def manage_tracking(
    action: TrackingAction = TrackingAction.QUERY,
    camera_name: Optional[str] = None,
    name: Optional[str] = None,
    detect_type: Optional[str] = None,
    enable: Optional[bool] = None,
    tracking: Optional[bool] = None,
    sensitivity_level: Optional[int] = None,
    answers: Optional[Dict[str, Any]] = None,
):
    camera_name = coerce_str(camera_name)
    name = coerce_str(name)

    resolved_name = camera_name or name
    dt = detect_type or "all"

    if _is_non_sk_camera(resolved_name):
        return TrackingSetResult(
            ok=False, error_code="UNSUPPORTED_PROTOCOL",
            message=_unsupported_protocol_message(resolved_name, "smart detection/tracking"),
        )

    if action == TrackingAction.QUERY:
        return big_tracking_query(name=resolved_name, detect_type=dt, answers=answers)
    elif action == TrackingAction.SET:

        if isinstance(enable, int) and not isinstance(enable, bool):
            enable = bool(enable)
        if isinstance(tracking, int) and not isinstance(tracking, bool):
            tracking = bool(tracking)
        return big_tracking_set(
            name=resolved_name, detect_type=dt,
            enable=enable, tracking=tracking,
            sensitivity_level=sensitivity_level, answers=answers)
    else:
        return TrackingSetResult(ok=False, error_code="INVALID_ACTION",
                                 message=f"Unsupported action: {action}")
