import time
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from typing import Any, Dict, Optional, Protocol, Tuple, cast

try:
    from . import camera_proto
except ImportError:
    import camera_proto

try:
    from .illumination import _envelope
except ImportError:
    from illumination import _envelope

try:
    from ._argnorm import coerce_str
except ImportError:
    from _argnorm import coerce_str

class PTZDirection(str, Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

_DIRECTION_ALIAS: Dict[str, PTZDirection] = {
    "上": PTZDirection.UP,
    "下": PTZDirection.DOWN,
    "左": PTZDirection.LEFT,
    "右": PTZDirection.RIGHT,
}

_SK_CMD_MAP: Dict[PTZDirection, str] = {
    PTZDirection.UP:        "up",
    PTZDirection.DOWN:      "down",
    PTZDirection.LEFT:      "left",
    PTZDirection.RIGHT:     "right",
}

_DEGREES_PER_SECOND = 34.0

_SK_PTZ_TIMEOUT = 5.0

@dataclass
class PTZMoveResult:
    success: bool
    protocol: str = ""
    error_message: str = ""

    requested_duration_seconds: float = 0.0
    actual_duration_seconds: float = 0.0

    degrees: float = 0.0
    method: str = ""

@dataclass
class PTZInfo:
    preset_max: int = 0
    cruise_max: int = 0
    scan_max: int = 0
    presets_per_cruise: int = 0
    presets_per_scan: int = 0
    preset_num: int = 0
    cruise_num: int = 0
    scan_num: int = 0

def _get_camera(camera_name: str):
    from .device_mgmt import _find_camera
    return _find_camera(camera_name)

def _sk_ptz_set(cam, payload: dict) -> Tuple[bool, str]:
    ok, data, status = _envelope(camera_proto.ptz_set(
        cam.ip, cam.sn_code, cam.username, cam.password, payload, _SK_PTZ_TIMEOUT))
    if not ok or not data:
        return False, f"SK SET_PTZ request failed (status={status})"
    if not camera_proto.code_ok(data.get("code", "")):
        return False, f"SK SET_PTZ returned code={data.get('code')} msg={data.get('msg')}"
    return True, ""

def _resolve_direction(direction) -> Optional[PTZDirection]:
    if isinstance(direction, PTZDirection):
        return direction
    if isinstance(direction, str):
        if direction.strip() in _DIRECTION_ALIAS:
            return _DIRECTION_ALIAS[direction.strip()]
        try:
            return PTZDirection(direction.strip().lower())
        except ValueError:
            return None
    return None

_DIRECTION_SIGN: Dict[PTZDirection, tuple] = {
    PTZDirection.UP:        (0, +1),
    PTZDirection.DOWN:      (0, -1),
    PTZDirection.LEFT:      (-1, 0),
    PTZDirection.RIGHT:     (+1, 0),
}

_ONVIF_MIN_MOVE_TIMEOUT = 1.0

class _ONVIFPTZService(Protocol):
    def ContinuousMove(self, request: Dict[str, Any]) -> Any: ...
    def Stop(self, request: Dict[str, Any]) -> Any: ...

def _onvif_ptz(cam) -> Tuple[Optional[_ONVIFPTZService], str, str]:
    try:
        from .device_mgmt import _connected_devices
        onvif_cam = (_connected_devices.get(cam.name) or {}).get("onvif_camera")
        if onvif_cam is None:
            if not cam.port:
                return None, "", "Missing ONVIF port; call connect_device first to complete the connection"
            from onvif import ONVIFCamera
            onvif_cam = ONVIFCamera(
                host=cam.ip, port=cam.port,
                user=cam.username or "admin", passwd=cam.password or "",
            )
        profiles = onvif_cam.create_media_service().GetProfiles()
        if not profiles:
            return None, "", "ONVIF returned no profiles; the device may not support PTZ"
        return cast(_ONVIFPTZService, onvif_cam.create_ptz_service()), profiles[0].token, ""
    except Exception as e:
        return None, "", f"ONVIF PTZ service initialization failed: {e}"

def _onvif_move(cam, vx: float, vy: float, duration: float) -> Tuple[bool, str]:
    ptz, token, err = _onvif_ptz(cam)
    if ptz is None:
        return False, err

    if not (vx or vy):
        return False, "Velocity vector is zero; no valid movement direction"
    velocity = {"PanTilt": {"x": vx, "y": vy}}

    try:
        ptz.ContinuousMove({
            "ProfileToken": token,
            "Velocity": velocity,
            "Timeout": timedelta(seconds=max(_ONVIF_MIN_MOVE_TIMEOUT, duration)),
        })
    except Exception as e:
        return False, f"ONVIF ContinuousMove failed: {e}"

    time.sleep(duration)
    try:
        ptz.Stop({"ProfileToken": token, "PanTilt": True})
    except Exception as e:
        return False, f"ONVIF movement started but stop failed: {e}"
    return True, ""

def _onvif_stop(cam) -> Tuple[bool, str]:
    ptz, token, err = _onvif_ptz(cam)
    if ptz is None:
        return False, err
    try:
        ptz.Stop({"ProfileToken": token, "PanTilt": True})
        return True, ""
    except Exception as e:
        return False, f"ONVIF Stop failed: {e}"

def _onvif_control(
    cam,
    direction: PTZDirection,
    speed: float,
    duration_seconds: Optional[float],
    degrees: Optional[float],
) -> PTZMoveResult:
    if degrees is not None:
        return PTZMoveResult(
            success=False, protocol="onvif", degrees=degrees,
            error_message="ONVIF movement by degrees is not supported — use duration_seconds instead",
        )

    duration = duration_seconds if duration_seconds is not None else 1.0

    pan_sign, tilt_sign = _DIRECTION_SIGN.get(direction, (0, 0))
    ok, err = _onvif_move(cam, pan_sign * speed, tilt_sign * speed, duration)

    if not ok:
        return PTZMoveResult(
            success=False, protocol="onvif",
            requested_duration_seconds=duration,
            error_message=err,
        )

    return PTZMoveResult(
        success=True, protocol="onvif",
        requested_duration_seconds=duration,
        actual_duration_seconds=duration,
        method="onvif_time",
    )

def control_ptz(
    camera_name: str,
    direction: PTZDirection,
    speed: float = 0.5,
    duration_seconds: Optional[float] = None,
    degrees: Optional[float] = None,
) -> PTZMoveResult:
    camera_name = coerce_str(camera_name)

    resolved_direction = _resolve_direction(direction)
    if resolved_direction is None:
        return PTZMoveResult(
            success=False,
            error_message="Invalid direction; valid: up/down/left/right",
        )

    speed = max(0.1, min(1.0, speed))

    if degrees is not None and duration_seconds is not None:
        return PTZMoveResult(
            success=False,
            error_message="degrees and duration_seconds cannot both be specified",
        )
    if degrees is None and duration_seconds is None:
        duration_seconds = 1.0
    if duration_seconds is not None:
        duration_seconds = max(0.1, min(10.0, duration_seconds))
    if degrees is not None:
        degrees = max(0.1, min(360.0, degrees))

    cam = _get_camera(camera_name)
    if not cam:
        return PTZMoveResult(
            success=False,
            error_message=f"Camera '{camera_name}' is not registered; register it first",
        )

    if cam.protocol_type in ("J", "O"):
        return _onvif_control(cam, resolved_direction, speed, duration_seconds, degrees)

    if degrees is None:
        duration = duration_seconds if duration_seconds is not None else 1.0
        sk_cmd = _SK_CMD_MAP[resolved_direction]
        ok, err = _sk_ptz_set(cam, {"cmd": sk_cmd})
        if not ok:
            return PTZMoveResult(
                success=False, protocol="sky_private",
                error_message=f"Failed to start directional movement: {err}",
            )
        time.sleep(duration)
        _sk_ptz_set(cam, {"cmd": "stop", "action": sk_cmd})

        return PTZMoveResult(
            success=True, protocol="sky_private",
            requested_duration_seconds=duration,
            actual_duration_seconds=duration,
            method="sk_time",
        )

    duration_seconds = degrees / 34.0
    duration_seconds = max(0.1, min(10.0, duration_seconds))
    sk_cmd = _SK_CMD_MAP[resolved_direction]
    ok, err = _sk_ptz_set(cam, {"cmd": sk_cmd})
    if not ok:
        return PTZMoveResult(
            success=False, protocol="sky_private", degrees=degrees,
            error_message=f"Failed to start directional movement: {err}",
        )
    time.sleep(duration_seconds)
    _sk_ptz_set(cam, {"cmd": "stop", "action": sk_cmd})

    return PTZMoveResult(
        success=True, protocol="sky_private",
        degrees=degrees,
        requested_duration_seconds=round(duration_seconds, 2),
        actual_duration_seconds=round(duration_seconds, 2),
        method="sk_degrees",
    )

def stop_ptz(
    camera_name: str,
) -> PTZMoveResult:
    camera_name = coerce_str(camera_name)

    cam = _get_camera(camera_name)
    if not cam:
        return PTZMoveResult(
            success=False,
            error_message=f"Camera '{camera_name}' is not registered",
        )

    if cam.protocol_type in ("J", "O"):
        ok, err = _onvif_stop(cam)
        if ok:
            return PTZMoveResult(success=True, protocol="onvif")
        return PTZMoveResult(success=False, protocol="onvif", error_message=err)

    ok, err = _sk_ptz_set(cam, {"cmd": "stop"})
    if ok:
        return PTZMoveResult(success=True, protocol="sky_private")
    return PTZMoveResult(success=False, protocol="sky_private", error_message=err)
