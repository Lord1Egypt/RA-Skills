"""ISP / image settings (`/image/0`): one getter + a section-scoped setter.

The device exposes the full config as `{videoAdjustment, nightToDay, profile[3]}`
with per-section PUT endpoints. Both directions are driven by the ``_SECTIONS``
table: friendly snake_case keys out, device `s*`/`i*` keys in.
"""

from __future__ import annotations

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from recamera_intellisense._cli import main

    raise SystemExit(main())

import re
from typing import Any, Dict, Optional

from . import _config, _http
from ._errors import RecameraError

__all__ = ["get_image_settings", "set_image_settings"]

PATH_IMAGE = "/cgi-bin/entry.cgi/image/0"

_SCENES = (0, 1, 2)  # GET /image/0 carries 3 profiles; the live one is nightToDay.iProfileCur
_OPEN_CLOSE = frozenset({"open", "close"})
_FRACTION_RE = re.compile(r"^[1-9]\d*/[1-9]\d*$")


class _Field:
    def __init__(self, key: str, *, enum=None, bounds=None, fraction: bool = False):
        self.key = key
        self.enum = enum
        self.bounds = bounds
        self.fraction = fraction


class _Section:
    def __init__(self, device_key: str, path: str, fields: Dict[str, _Field], extras=None):
        self.device_key = device_key  # key inside GET /image/0 (or inside a profile)
        self.path = path  # full PUT path; '{scene}' substituted for profile sections
        self.fields = fields
        self.extras = extras or {}  # read-only device_key -> friendly mappings
        self.profile = "{scene}" in path


def _pct(key: str) -> _Field:
    return _Field(key, bounds=(0, 100))


_SECTIONS: Dict[str, _Section] = {
    "video_adjustment": _Section("videoAdjustment", "/cgi-bin/entry.cgi/image/0/video-adjustment", {
        "rotation": _Field("iImageRotation", enum={0, 90, 180, 270}),
        "flip": _Field("sImageFlip", enum={"close", "mirror", "flip", "centrosymmetric"}),
        "power_line_frequency": _Field("sPowerLineFrequencyMode", enum={"PAL(50HZ)", "NTSC(60HZ)"}),
    }),
    "night_to_day": _Section("nightToDay", "/cgi-bin/entry.cgi/image/0/night-to-day", {
        "mode": _Field("iMode", enum={0, 1, 2}),
        "filter_level": _Field("iNightToDayFilterLevel", enum={0, 1, 2}),
        "filter_time": _Field("iNightToDayFilterTime", bounds=(1, 60)),
        "dawn_time": _Field("iDawnTime", bounds=(0, 86400)),
        "dusk_time": _Field("iDuskTime", bounds=(0, 86400)),
        "profile_select": _Field("iProfileSelect", enum=_SCENES),
    }, extras={"iProfileCur": "profile_current"}),
    "adjustment": _Section("imageAdjustment", "/cgi-bin/entry.cgi/image/0/{scene}/adjustment", {
        "brightness": _pct("iBrightness"),
        "contrast": _pct("iContrast"),
        "hue": _pct("iHue"),
        "saturation": _pct("iSaturation"),
        "sharpness": _pct("iSharpness"),
    }),
    "exposure": _Section("exposure", "/cgi-bin/entry.cgi/image/0/{scene}/exposure", {
        "exposure_mode": _Field("sExposureMode", enum={"auto", "manual"}),
        "gain_mode": _Field("sGainMode", enum={"auto", "manual"}),
        "exposure_time": _Field("sExposureTime", fraction=True),
        "exposure_gain": _Field("iExposureGain", bounds=(1, 128)),
    }),
    "backlight": _Section("BLC", "/cgi-bin/entry.cgi/image/0/{scene}/blc", {
        "blc_region": _Field("sBLCRegion", enum=_OPEN_CLOSE),
        "blc_strength": _pct("iBLCStrength"),
        "dark_boost_level": _pct("iDarkBoostLevel"),
        "hdr": _Field("sHDR", enum=_OPEN_CLOSE),
        "hdr_level": _Field("iHDRLevel", enum={1}),
        "hlc": _Field("sHLC", enum=_OPEN_CLOSE),
        "hlc_level": _Field("iHLCLevel", bounds=(1, 100)),
    }),
    "white_balance": _Section("whiteBlance", "/cgi-bin/entry.cgi/image/0/{scene}/white-blance", {
        "style": _Field(
            "sWhiteBlanceStyle", enum={"auto", "manual", "daylight", "streetlamp", "outdoor"}
        ),
        "color_temperature": _Field("iWhiteBalanceCT", bounds=(2800, 7500)),
    }),
    "enhancement": _Section("imageEnhancement", "/cgi-bin/entry.cgi/image/0/{scene}/enhancement", {
        "noise_reduce_mode": _Field("iNoiseReduceMode", enum={0, 1}),
        "spatial_denoise_level": _pct("iSpatialDenoiseLevel"),
        "temporal_denoise_level": _pct("iTemporalDenoiseLevel"),
    }),
}

_PROFILE_SECTIONS = ("adjustment", "exposure", "backlight", "white_balance", "enhancement")


def _fetch_config(dev) -> Dict[str, Any]:
    return _http.get_json(dev, PATH_IMAGE) or {}


def _normalize_section(spec: _Section, raw: Dict[str, Any]) -> Dict[str, Any]:
    out = {friendly: raw.get(field.key) for friendly, field in spec.fields.items()}
    out.update({friendly: raw.get(key) for key, friendly in spec.extras.items()})
    return out


def get_image_settings(device_name: Optional[str] = None) -> Dict[str, Any]:
    """Full ISP config: video adjustment, night-to-day, and 3 scene profiles."""
    dev = _config.resolve(device_name)
    d = _fetch_config(dev)
    profiles = d.get("profile") or []
    return {
        "video_adjustment": _normalize_section(
            _SECTIONS["video_adjustment"], d.get("videoAdjustment") or {}
        ),
        "night_to_day": _normalize_section(
            _SECTIONS["night_to_day"], d.get("nightToDay") or {}
        ),
        "profiles": [
            {
                name: _normalize_section(_SECTIONS[name], p.get(_SECTIONS[name].device_key) or {})
                for name in _PROFILE_SECTIONS
            }
            for p in profiles
            if isinstance(p, dict)
        ],
    }


def _validate_value(section: str, key: str, field: _Field, value: Any) -> Any:
    where = f"{section}.{key}"
    if isinstance(value, bool):  # bool is an int subclass; never a valid field value
        raise ValueError(f"{where} must not be a boolean; got {value!r}")
    if field.enum is not None:
        if value not in field.enum:
            raise ValueError(f"{where} must be one of {sorted(field.enum, key=str)}; got {value!r}")
        return value
    if field.fraction:
        if not isinstance(value, str) or not _FRACTION_RE.match(value):
            raise ValueError(f"{where} must be a fraction string like '1/60'; got {value!r}")
        return value
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{where} must be an integer; got {value!r}")
    lo, hi = field.bounds
    if not lo <= value <= hi:
        raise ValueError(f"{where} must be within [{lo}, {hi}]; got {value}")
    return value


def _check_section_rules(section: str, merged: Dict[str, Any]) -> None:
    if section == "backlight":
        open_ones = [k for k in ("sBLCRegion", "sHDR", "sHLC") if merged.get(k) == "open"]
        if len(open_ones) > 1:
            raise ValueError(
                f"backlight: BLC/HDR/HLC are mutually exclusive, "
                f"but {open_ones} would all be 'open'"
            )
    if section == "night_to_day":
        dawn, dusk = merged.get("iDawnTime"), merged.get("iDuskTime")
        if isinstance(dawn, int) and isinstance(dusk, int) and dusk <= dawn:
            raise ValueError(
                f"night_to_day: dusk_time ({dusk}) must be greater than dawn_time ({dawn})"
            )


def _section_state(spec: _Section, config: Dict[str, Any], scene_id: Optional[int]) -> Dict[str, Any]:
    if spec.profile:
        profiles = config.get("profile") or []
        entry = profiles[scene_id] if scene_id is not None and scene_id < len(profiles) else None
        raw = (entry or {}).get(spec.device_key) or {}
    else:
        raw = config.get(spec.device_key) or {}
    return _normalize_section(spec, raw)


def _active_scene(config: Dict[str, Any]) -> int:
    cur = (config.get("nightToDay") or {}).get("iProfileCur")
    if cur not in _SCENES:
        raise RecameraError(
            "device did not report an active image profile (iProfileCur)",
            detail={"nightToDay": config.get("nightToDay")},
        )
    return int(cur)


def set_image_settings(
    device_name: Optional[str] = None,
    *,
    section: str,
    values: Dict[str, Any],
    scene_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Merge *values* into one ISP section, PUT it, return the re-read state.

    `section` is one of: video_adjustment, night_to_day, adjustment, exposure,
    backlight, white_balance, enhancement. Profile sections default `scene_id`
    to the profile the camera is currently using (night_to_day.profile_current),
    so writes take visible effect immediately; pass 0/1/2 explicitly to
    pre-configure an inactive profile. Returns `{section, changed, state}`
    (plus `scene_id` for profile sections) where `state` is the section
    re-read after the write — proof the device accepted it.
    """
    spec = _SECTIONS.get(section)
    if spec is None:
        raise ValueError(f"unknown section {section!r}; expected one of {sorted(_SECTIONS)}")
    if spec.profile:
        if scene_id is not None and scene_id not in _SCENES:
            raise ValueError(f"scene_id must be one of {_SCENES}; got {scene_id!r}")
    elif scene_id is not None:
        raise ValueError(f"section {section!r} does not take a scene_id")
    if not isinstance(values, dict) or not values:
        raise ValueError("'values' must be a non-empty object of section fields")
    unknown = set(values) - set(spec.fields)
    if unknown:
        raise ValueError(
            f"unknown field(s) for section {section!r}: {sorted(unknown)}; "
            f"allowed: {sorted(spec.fields)}"
        )
    updates = {
        spec.fields[key].key: _validate_value(section, key, spec.fields[key], value)
        for key, value in values.items()
    }

    dev = _config.resolve(device_name)
    config = _fetch_config(dev)
    if spec.profile and scene_id is None:
        scene_id = _active_scene(config)
    if spec.profile:
        profiles = config.get("profile") or []
        assert scene_id is not None
        entry = profiles[scene_id] if scene_id < len(profiles) else None
        if not isinstance(entry, dict):
            raise ValueError(f"device returned no profile for scene_id {scene_id}")
    state_now = _section_state(spec, config, scene_id)
    payload = {
        field.key: state_now[friendly]
        for friendly, field in spec.fields.items()
        if state_now.get(friendly) is not None
    }
    payload.update(updates)
    _check_section_rules(section, payload)

    path = spec.path.replace("{scene}", str(scene_id)) if spec.profile else spec.path
    resp = _http.put_json(dev, path, payload=payload)
    _http.expect_ok(resp, f"set image settings {section}")

    out: Dict[str, Any] = {
        "section": section,
        "changed": dict(values),
        "state": _section_state(spec, _fetch_config(dev), scene_id),
    }
    if spec.profile:
        out["scene_id"] = scene_id
    return out


COMMANDS = {
    "get_image_settings": get_image_settings,
    "set_image_settings": set_image_settings,
}
