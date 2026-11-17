from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

try:
    from . import camera_proto
except ImportError:
    import camera_proto

try:
    from .device_mgmt import resolve_target, CameraConfig, _is_non_sk_camera, _unsupported_protocol_message
except ImportError:
    from device_mgmt import resolve_target, CameraConfig, _is_non_sk_camera, _unsupported_protocol_message

try:
    from ._argnorm import coerce_str
except ImportError:
    from _argnorm import coerce_str

class IlluminationAction(str, Enum):
    QUERY = "get"
    SET = "set"

class DaynightMode(str, Enum):
    DAY = "day"
    NIGHT = "night"
    AUTO = "auto"
    TIMER = "timer"
    SMART = "smart"

class FilllightModeEnum(str, Enum):
    FULL_COLOR = "full_color"
    INFRARED = "infrared"
    SMART = "smart"

DAYNIGHT_MODES = {
    0: "Day mode", 1: "Night mode", 2: "Auto mode", 3: "Schedule mode", 4: "Smart mode",
}

FILLLIGHT_MODES = {
    0: "Full-color mode", 1: "Infrared mode", 2: "Smart night-vision mode",
}

@dataclass
class IlluminationInfo:
    name: str
    label: str
    type: str = "int"
    min: Optional[int] = None
    max: Optional[int] = None
    current: Optional[Any] = None
    current_text: str = ""
    options: Dict[str, str] = field(default_factory=dict)

@dataclass
class FilllightQueryResult:
    ok: bool
    camera: str = ""
    channel: str = ""
    capabilities: list = field(default_factory=list)
    current: Dict[str, Any] = field(default_factory=dict)
    error_code: str = ""
    message: str = ""
    hint: str = ""
    needs_input: list = field(default_factory=list)

@dataclass
class FilllightSetResult:
    ok: bool
    camera: str = ""
    channel: str = ""
    updated: Dict[str, Any] = field(default_factory=dict)
    current: Dict[str, Any] = field(default_factory=dict)
    verified: bool = True
    error_code: str = ""
    message: str = ""
    hint: str = ""
    needs_input: list = field(default_factory=list)

_SK_IMAGE_PORT = 9010
_SK_IMAGE_TIMEOUT = 3.0

_SK_FILLLIGHT_SUPPORTED = ("daynightmode", "filllightmode")

_SK_FILLLIGHT_LABELS = {
    "daynightmode": "Day/night mode (light-on setting)",
    "filllightmode": "Fill light mode",
}

_SK_FILLLIGHT_VALUE_TEXTS = {
    "daynightmode": {0: "Day mode", 1: "Night mode", 2: "Auto mode", 3: "Schedule mode", 4: "Smart mode"},
    "filllightmode": {0: "Full-color mode", 1: "Infrared mode", 2: "Smart night-vision mode"},
}

_SK_DAYNIGHT_ALIASES = {"day": 0, "白天": 0, "night": 1, "夜晚": 1, "auto": 2, "自动": 2,
                        "timer": 3, "定时": 3, "smart": 4, "智能": 4}
_SK_FILLMODE_ALIASES = {"color": 0, "full_color": 0, "全彩": 0,
                        "ir": 1, "infrared": 1, "红外": 1,
                        "smart": 2, "智能夜视": 2}

def _sk_err(result_cls, error_code: str, message: str, hint: str = "", needs_input=None, camera: str = ""):
    return result_cls(ok=False, error_code=error_code, message=message, hint=hint,
                      needs_input=needs_input or [], camera=camera)

def _sk_resolve_camera(name, answers, result_cls):
    rt = resolve_target(name=name, answers=answers)
    if not rt["ok"]:
        return _sk_err(result_cls, rt.get("error_code", "RESOLVE_FAILED"),
                       rt.get("message", "Failed to resolve target camera"), rt.get("hint", ""),
                       rt.get("needs_input")), None
    return None, rt["camera"]

def _envelope(env: Dict[str, Any]):
    status = env.get("http_status") or None
    if env.get("ok") == 1 and isinstance(env.get("body"), dict):
        return True, env["body"], status
    return False, None, status

def _coerce_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None

def _merge_capabilities(caps: list, current: Dict[str, Any],
                        labels: Optional[Dict[str, str]] = None,
                        value_texts: Optional[Dict[str, dict]] = None) -> list:
    labels = labels if labels is not None else _SK_FILLLIGHT_LABELS
    value_texts = value_texts if value_texts is not None else _SK_FILLLIGHT_VALUE_TEXTS
    merged = []
    for item in caps:
        if not isinstance(item, dict):
            continue
        fname = str(item.get("name", ""))
        specs = item.get("specs") or {}
        entry: Dict[str, Any] = {
            "name": fname,
            "label": labels.get(fname, fname),
            "type": item.get("type", "int"),
            "min": _coerce_int(specs.get("min")),
            "max": _coerce_int(specs.get("max")),
        }
        if fname in current:
            entry["current"] = current[fname]
            text_map = value_texts.get(fname)
            cv = _coerce_int(current[fname])
            if text_map and cv is not None and cv in text_map:
                entry["current_text"] = text_map[cv]
            if text_map:
                lo, hi = entry["min"], entry["max"]
                if lo is not None and hi is not None:
                    entry["options"] = {str(v): text_map[v] for v in range(lo, hi + 1) if v in text_map}
        merged.append(entry)
    return merged

def _enum_coerce(v, aliases: Dict[str, int], field_name: str, result_cls, camera: str = ""):
    if isinstance(v, bool):
        return False, None, _sk_err(result_cls, "INVALID_PARAM_TYPE",
                                    f"{field_name} expects an int or string alias, got {v!r}", camera=camera)
    if isinstance(v, int):
        return True, v, None
    if isinstance(v, str):
        s = v.strip().lower()
        if s in aliases:
            return True, aliases[s], None
        if s.isdigit():
            return True, int(s), None
    return False, None, _sk_err(result_cls, "INVALID_PARAM_VALUE",
                                f"Unrecognized value {v!r} for {field_name}",
                                f"Supported: int or one of: {', '.join(sorted(aliases))}", camera=camera)

def _sk_filllight_option(cam) -> Dict[str, Any]:
    ok, resp, _status = _envelope(camera_proto.filllight_get_option(
        cam.ip, cam.sn_code, cam.username, cam.password, _SK_IMAGE_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": _status}
    caps = resp.get("filllight")
    _ok = camera_proto.code_ok(resp.get("code", "")) and isinstance(caps, list)
    return {"ok": _ok, "capabilities": caps if isinstance(caps, list) else [],
            "code": resp.get("code", ""), "status": _status, "raw": resp}

def _sk_filllight_cur(cam) -> Dict[str, Any]:
    ok, resp, _status = _envelope(camera_proto.filllight_get(
        cam.ip, cam.sn_code, cam.username, cam.password, _SK_IMAGE_TIMEOUT))
    if not ok or not resp:
        return {"ok": False, "status": _status}
    _head = {"service_type", "msg_id", "cmd_name", "ver", "code", "msg", "channel", "sequence"}
    current = {k: v for k, v in resp.items() if k not in _head}
    _ok = camera_proto.code_ok(resp.get("code", ""))
    return {"ok": _ok, "current": current,
            "code": resp.get("code", ""), "status": _status, "raw": resp}

def _sk_filllight_set(cam, updates: Dict[str, Any]) -> FilllightSetResult:

    opt = _sk_filllight_option(cam)
    if not opt["ok"]:
        if opt.get("status") is None:
            return _sk_err(FilllightSetResult, "DEVICE_UNREACHABLE",
                           f"Cannot connect to {cam.ip}:{_SK_IMAGE_PORT} (SK HTTP no response)", camera=cam.name)
        return _sk_err(FilllightSetResult, "OPTION_QUERY_FAILED",
                       f"Failed to query fill light capabilities (code={opt.get('code') or '404'})", camera=cam.name)
    cap_map: Dict[str, dict] = {}
    for item in opt["capabilities"]:
        if isinstance(item, dict) and item.get("name"):
            cap_map[str(item["name"])] = item
    for k, v in updates.items():
        item = cap_map.get(k)
        if item is None:
            return _sk_err(FilllightSetResult, "PARAM_NOT_SUPPORTED",
                           f"Camera does not support fill light parameter {k}",
                           f"Supported parameters: {', '.join(sorted(cap_map)) or 'none'}", camera=cam.name)
        specs = item.get("specs") or {}
        lo, hi = _coerce_int(specs.get("min")), _coerce_int(specs.get("max"))
        if lo is not None and hi is not None and not (lo <= v <= hi):
            return _sk_err(FilllightSetResult, "PARAM_OUT_OF_RANGE",
                           f"{k}={v} out of allowed range {lo}-{hi}", camera=cam.name)

    base = _sk_filllight_cur(cam)
    if not base["ok"]:
        if base.get("status") is None:
            return _sk_err(FilllightSetResult, "DEVICE_UNREACHABLE",
                           f"Cannot connect to {cam.ip}:{_SK_IMAGE_PORT} (SK HTTP no response)", camera=cam.name)
        return _sk_err(FilllightSetResult, "CURRENT_QUERY_FAILED",
                       f"Failed to query current fill light values (code={base['code']})", camera=cam.name)
    payload = dict(base["current"])
    payload.update(updates)

    ok, resp, _status = _envelope(camera_proto.filllight_set(
        cam.ip, cam.sn_code, cam.username, cam.password, payload, _SK_IMAGE_TIMEOUT))
    if not ok or not resp:
        return _sk_err(FilllightSetResult, "DEVICE_UNREACHABLE" if _status is None else "SET_FAILED",
                       f"Failed to send fill light set command to {cam.ip}:{_SK_IMAGE_PORT}"
                       + ("" if _status is None else f" (HTTP {_status})"), camera=cam.name)
    if not camera_proto.code_ok(resp.get("code", "")):
        return _sk_err(FilllightSetResult, "SET_FAILED",
                       f"Device rejected the set (code={resp.get('code')} msg={resp.get('msg')})", camera=cam.name)

    rb = _sk_filllight_cur(cam)
    cur = rb["current"] if rb["ok"] else dict(payload)
    cur = {k: v for k, v in cur.items() if k in _SK_FILLLIGHT_SUPPORTED}
    updated = {k: cur[k] for k in updates if k in cur}
    return FilllightSetResult(ok=True, camera=cam.name, channel="sk", updated=updated, current=cur,
                              message=f"Fill light parameters applied: {updated}")

def _query_filllight_cam(cam) -> FilllightQueryResult:
    opt = _sk_filllight_option(cam)
    if not opt["ok"]:
        if opt.get("status") is None:
            return _sk_err(FilllightQueryResult, "DEVICE_UNREACHABLE",
                           f"Cannot connect to {cam.ip}:{_SK_IMAGE_PORT} (SK HTTP no response)",
                           "Check the camera is online and reachable, with correct registered credentials", camera=cam.name)
        return _sk_err(FilllightQueryResult, "OPTION_QUERY_FAILED",
                       f"Failed to query fill light capabilities (code={opt.get('code') or '404'})",
                       "Check whether the device firmware supports fill light settings", camera=cam.name)
    cur = _sk_filllight_cur(cam)
    if not cur["ok"]:
        return _sk_err(FilllightQueryResult, "CURRENT_QUERY_FAILED",
                       f"Failed to query current fill light values (code={cur['code']})", camera=cam.name)

    caps = [c for c in opt["capabilities"]
            if isinstance(c, dict) and str(c.get("name", "")) in _SK_FILLLIGHT_SUPPORTED]
    current = {k: v for k, v in cur["current"].items() if k in _SK_FILLLIGHT_SUPPORTED}
    return FilllightQueryResult(
        ok=True, camera=cam.name, channel="sk",
        capabilities=_merge_capabilities(caps, current,
                                         _SK_FILLLIGHT_LABELS, _SK_FILLLIGHT_VALUE_TEXTS),
        current=current,
    )

def _set_filllight_cam(cam, updates: Dict[str, Any]) -> FilllightSetResult:
    return _sk_filllight_set(cam, updates)

def big_filllight_query(
    name: Optional[str] = None,
    answers: Optional[Dict[str, Any]] = None,
) -> FilllightQueryResult:
    err, cam = _sk_resolve_camera(name, answers, FilllightQueryResult)
    if err:
        return err
    result = _query_filllight_cam(cam)
    return result

def big_filllight_set(
    name: Optional[str] = None,
    daynightmode=None,
    filllightmode=None,
    answers: Optional[Dict[str, Any]] = None,
) -> FilllightSetResult:
    updates: Dict[str, Any] = {}
    for k, v, aliases in (("daynightmode", daynightmode, _SK_DAYNIGHT_ALIASES),
                          ("filllightmode", filllightmode, _SK_FILLMODE_ALIASES)):
        if v is None:
            continue
        okv, val, err = _enum_coerce(v, aliases, k, FilllightSetResult)
        if not okv:
            return err
        updates[k] = val
    if not updates:
        return _sk_err(FilllightSetResult, "NO_PARAMS", "No fill light parameters provided to modify",
                       "Pass at least one parameter, e.g. daynightmode='auto'; call big_filllight_query first to see available options")

    err, cam = _sk_resolve_camera(name, answers, FilllightSetResult)
    if err:
        return err
    result = _set_filllight_cam(cam, updates)
    return result

def manage_illumination(
    action: IlluminationAction = IlluminationAction.QUERY,
    camera_name: Optional[str] = None,
    name: Optional[str] = None,
    daynightmode=None,
    filllightmode=None,
    answers: Optional[Dict[str, Any]] = None,
):
    camera_name = coerce_str(camera_name)
    name = coerce_str(name)

    resolved_name = camera_name or name

    if _is_non_sk_camera(resolved_name):
        return FilllightSetResult(
            ok=False, error_code="UNSUPPORTED_PROTOCOL",
            message=_unsupported_protocol_message(resolved_name, "illumination/night vision control"),
        )

    if action == IlluminationAction.QUERY:
        return big_filllight_query(name=resolved_name, answers=answers)
    elif action == IlluminationAction.SET:
        return big_filllight_set(
            name=resolved_name,
            daynightmode=daynightmode,
            filllightmode=filllightmode,
            answers=answers,
        )
    else:
        return FilllightSetResult(ok=False, error_code="INVALID_ACTION",
                                  message=f"Unsupported action: {action}")

def probe_illumination_capability(
    name: Optional[str] = None,
    answers: Optional[Dict[str, Any]] = None,
) -> FilllightQueryResult:
    return big_filllight_query(name=name, answers=answers)
