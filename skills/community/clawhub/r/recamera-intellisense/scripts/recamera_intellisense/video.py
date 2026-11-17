"""Video stream encode settings (``/video/{0,1}/encode``)."""

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

__all__ = ["get_video_encode", "set_video_encode"]

PATH_ENCODE = "/cgi-bin/entry.cgi/video/{}/encode"

_STREAM_IDS = {"main": 0, "sub": 1}


def get_video_encode(
    device_name: Optional[str] = None,
    *,
    stream: str = "main",
) -> Dict[str, Any]:
    """Encode parameters for `stream` (``"main"``|``"sub"``):
    ``{stream, stream_type, enabled, codec, resolution, frame_rate, gop,
    rc_mode, rc_quality, max_rate(kbps)}``."""
    key = str(stream).strip().lower()
    if key not in _STREAM_IDS:
        raise ValueError(
            f"stream must be one of {sorted(_STREAM_IDS)}; got {stream!r}"
        )
    dev = _config.resolve(device_name)
    d = _http.get_json(dev, PATH_ENCODE.format(_STREAM_IDS[key]))
    if not isinstance(d, dict):
        raise RecameraError("get video encode failed: unexpected payload")
    return {
        "stream": key,
        "stream_type": d.get("sStreamType", ""),
        "enabled": bool(d.get("iEnabled", 0)),
        "codec": d.get("sOutputDataType", ""),
        "resolution": d.get("sResolution", ""),
        "frame_rate": d.get("sFrameRate", ""),
        "gop": int(d.get("iGOP", 0)),
        "rc_mode": d.get("sRCMode", ""),
        "rc_quality": d.get("sRCQuality", ""),
        "max_rate": int(d.get("iMaxRate", 0)),
    }


COMMANDS = {"get_video_encode": get_video_encode}

_CODECS = ("H.264", "H.265")
_RC_MODES = ("CBR", "VBR")
_RC_QUALITIES = ("highest", "high", "medium", "low")


def _int_field(name: str, value: Any, lo: int, hi: int) -> int:
    try:
        ivalue = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be an integer {lo}~{hi}") from None
    if isinstance(value, bool) or (isinstance(value, float)
                                   and value != ivalue) \
            or not lo <= ivalue <= hi:
        raise ValueError(f"{name} must be an integer {lo}~{hi}")
    return ivalue


def _norm_resolution(value: Any) -> str:
    text = str(value or "").lower().replace("x", "*")
    try:
        w_s, h_s = text.split("*", 1)
        w, h = int(w_s), int(h_s)
    except (ValueError, AttributeError):
        raise ValueError(
            "resolution must be \"WxH\" within 384*384 ~ 3840*2160") from None
    if not (384 <= w <= 3840 and 384 <= h <= 2160):
        raise ValueError("resolution must be \"WxH\" within 384*384 ~ 3840*2160")
    return f"{w}*{h}"


def set_video_encode(
    device_name: Optional[str] = None,
    *,
    stream: str = "main",
    codec: Optional[str] = None,
    resolution: Optional[str] = None,
    frame_rate: Optional[Any] = None,
    gop: Optional[Any] = None,
    rc_mode: Optional[str] = None,
    rc_quality: Optional[str] = None,
    max_rate: Optional[Any] = None,
    enabled: Optional[bool] = None,
) -> Dict[str, Any]:
    """Update encode parameters for `stream`; only the fields passed are
    changed (the rest keep their stored values), and the result is verified
    by re-reading the device. Changing these briefly re-inits the encoder.
    """
    dev = _config.resolve(device_name)
    key = str(stream).strip().lower()
    if key not in _STREAM_IDS:
        raise ValueError(
            f"stream must be one of {sorted(_STREAM_IDS)}; got {stream!r}")
    payload: Dict[str, Any] = {}
    checks: Dict[str, Any] = {}
    if codec is not None:
        codec = str(codec).upper()
        if codec not in _CODECS:
            raise ValueError(f"codec must be one of {list(_CODECS)}")
        payload["sOutputDataType"] = codec
        checks["codec"] = codec
    if resolution is not None:
        payload["sResolution"] = _norm_resolution(resolution)
        checks["resolution"] = payload["sResolution"]
    if frame_rate is not None:
        fps = _int_field("frame_rate", frame_rate, 1, 120)
        payload["sFrameRate"] = str(fps)  # wire type is a numeric string
        checks["frame_rate"] = str(fps)
    if gop is not None:
        payload["iGOP"] = _int_field("gop", gop, 1, 120)
        checks["gop"] = payload["iGOP"]
    if rc_mode is not None:
        rc_mode = str(rc_mode).upper()
        if rc_mode not in _RC_MODES:
            raise ValueError(f"rc_mode must be one of {list(_RC_MODES)}")
        payload["sRCMode"] = rc_mode
        checks["rc_mode"] = rc_mode
    if rc_quality is not None:
        rc_quality = str(rc_quality).lower()
        if rc_quality not in _RC_QUALITIES:
            raise ValueError(
                f"rc_quality must be one of {list(_RC_QUALITIES)}")
        payload["sRCQuality"] = rc_quality
        checks["rc_quality"] = rc_quality
    if max_rate is not None:
        payload["iMaxRate"] = _int_field("max_rate", max_rate, 3, 65536)
        checks["max_rate"] = payload["iMaxRate"]
    if enabled is not None:
        payload["iEnabled"] = 1 if enabled else 0
        checks["enabled"] = bool(enabled)
    if not payload:
        raise ValueError(
            "nothing to change: pass codec, resolution, frame_rate, gop, "
            "rc_mode, rc_quality, max_rate, or enabled")
    _http.expect_ok(
        _http.post_json(dev, PATH_ENCODE.format(_STREAM_IDS[key]),
                        payload=payload),
        "set video encode")
    after = get_video_encode(device_name, stream=key)
    mismatched = {
        k: {"wanted": v, "got": after.get(k)}
        for k, v in checks.items()
        if str(after.get(k)) != str(v)
    }
    if mismatched:
        raise RecameraError(
            f"set video encode did not apply: {mismatched}")
    return {"changed": True, "stream": key, "applied": checks}


COMMANDS["set_video_encode"] = set_video_encode
