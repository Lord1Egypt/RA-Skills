#!/usr/bin/env python3
"""pettracer_mapshot.py — generate a static map image for a pet's latest PetTracer fix.

This is intended for agents:
- Pull latest location from PetTracer (same portal API as pettracer_cli.py)
- Render a *map screenshot* as a PNG image using a static maps HTTP API
- Emit stable JSON describing the generated file for downstream sending

Default map provider: **Google Maps Static API**

Why Google by default:
- One HTTP GET returns an image
- Most OpenClaw users already have a Google Cloud project

Environment variables:
- GOOGLE_MAPS_API_KEY            (required)
- GOOGLE_MAPS_MAPTYPE            (optional; default: hybrid)
- GOOGLE_MAPS_SIZE               (optional; default: 640x640)
- GOOGLE_MAPS_SCALE              (optional; default: 2)

PetTracer env vars are the same as pettracer_cli.py:
- PETTRACER_TOKEN or (PETTRACER_USERNAME/PETTRACER_EMAIL + PETTRACER_PASSWORD)

Exit codes:
- 0: success (including "no_recent_fix" JSON)
- 1: generic error
- 2: invalid args / missing prerequisites
- 3: device not found
- 4: auth error
- 5: timeout
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# Reuse the robust PetTracer selection + parsing logic.
# This file lives in the same directory as pettracer_cli.py, so a plain import works.
import pettracer_cli as pt

GOOGLE_STATIC_ENDPOINT = "https://maps.googleapis.com/maps/api/staticmap"
USER_AGENT = "pettracer-agent-skill/0.4"


def _json_dumps(obj: Any, pretty: bool) -> str:
    if pretty:
        return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)


def _emit(payload: Any, *, fmt: str, pretty: bool) -> None:
    if fmt == "json":
        print(_json_dumps(payload, pretty))
    else:
        print(payload)


def _emit_error(*, fmt: str, pretty: bool, error_type: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
    if fmt == "json":
        err: Dict[str, Any] = {"error": {"type": error_type, "message": message}}
        if details:
            err["error"]["details"] = details
        print(_json_dumps(err, pretty))
    else:
        print(f"{error_type}: {message}", file=sys.stderr)
        if details:
            print(details, file=sys.stderr)


def _env_first(*names: str) -> Optional[str]:
    for n in names:
        v = os.getenv(n)
        if v:
            return v
    return None


def _safe_filename(s: str) -> str:
    # Keep it boring and filesystem-safe.
    s2 = re.sub(r"[^a-zA-Z0-9._-]+", "_", s.strip())
    return s2.strip("._-") or "pet"


def _default_out_path(*, pet_name: str, device_id: int) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = _safe_filename(pet_name)[:32]
    os.makedirs("output", exist_ok=True)
    return os.path.join("output", f"pettracer_{base}_{device_id}_{ts}.png")


def _label_from_name(name: str) -> str:
    # Google marker label is a single alphanumeric character.
    for ch in name.strip():
        if ch.isalnum():
            return ch.upper()[:1]
    return "P"


def build_google_static_url(
    *,
    lat: float,
    lon: float,
    api_key: str,
    zoom: int,
    size: str,
    scale: int,
    maptype: str,
    label: str,
) -> str:
    # Marker string uses pipe separators; urlencode will safely encode them.
    marker = f"color:red|label:{label}|{lat},{lon}"
    params = {
        "center": f"{lat},{lon}",
        "zoom": str(int(zoom)),
        "size": size,
        "scale": str(int(scale)),
        "maptype": maptype,
        "format": "png",
        "markers": marker,
        "key": api_key,
    }
    return f"{GOOGLE_STATIC_ENDPOINT}?{urlencode(params)}"


def _download_image(url: str, *, out_path: str, timeout_s: int) -> Tuple[int, str]:
    """Download URL to out_path.

    Returns: (bytes_written, content_type)
    """

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "image/*,*/*;q=0.8",
    }

    req = Request(url, headers=headers, method="GET")

    try:
        with urlopen(req, timeout=timeout_s) as resp:
            content_type = resp.headers.get("Content-Type", "")
            data = resp.read()

        if not content_type.lower().startswith("image/"):
            # Often an HTML error page.
            snippet = ""
            try:
                snippet = data.decode("utf-8", errors="replace")[:400]
            except Exception:
                snippet = "<non-text response>"
            raise RuntimeError(f"Non-image response (Content-Type={content_type}): {snippet}")

        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(data)
        return (len(data), content_type)

    except HTTPError as e:
        body = b""
        try:
            body = e.read()  # type: ignore[attr-defined]
        except Exception:
            body = b""
        snippet = ""
        try:
            snippet = body.decode("utf-8", errors="replace")[:400]
        except Exception:
            snippet = "<non-text response>"
        raise RuntimeError(f"HTTP {e.code} {e.reason}: {snippet}".strip())
    except URLError as e:
        raise RuntimeError(f"Network error: {e}") from e


class ExitCode:
    OK = 0
    ERROR = 1
    INVALID_ARGS = 2
    NOT_FOUND = 3
    AUTH = 4
    TIMEOUT = 5


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pettracer_mapshot.py")

    # Pet selection
    p.add_argument("--device-id", type=int, help="PetTracer device id.")
    p.add_argument("--pet", help="Pet name (matches device.details.name).")

    # PetTracer auth
    p.add_argument("--username", help="PetTracer login (prefer env var PETTRACER_USERNAME).")
    p.add_argument("--password", help="PetTracer password (prefer env var PETTRACER_PASSWORD).")

    # HTTP behaviour
    p.add_argument("--timeout-s", type=int, default=20, help="Request timeout in seconds.")
    p.add_argument(
        "--retries",
        type=int,
        default=int(os.getenv("PETTRACER_RETRIES", "2")),
        help="Retries for transient PetTracer failures (default: 2).",
    )

    # Map output
    p.add_argument("--out", help="Output path for PNG (default: output/pettracer_<pet>_<id>_<ts>.png)")
    p.add_argument(
        "--zoom",
        type=int,
        default=17,
        help="Map zoom (street-level is ~16–18).",
    )
    p.add_argument(
        "--size",
        default=_env_first("GOOGLE_MAPS_SIZE") or "640x640",
        help="Image size, e.g. 640x640 (Google Static API max is typically 640x640; use scale=2 for higher res).",
    )
    p.add_argument(
        "--scale",
        type=int,
        default=int(_env_first("GOOGLE_MAPS_SCALE") or "2"),
        choices=[1, 2],
        help="Pixel density multiplier (1 or 2).",
    )
    p.add_argument(
        "--maptype",
        default=_env_first("GOOGLE_MAPS_MAPTYPE") or "hybrid",
        choices=["roadmap", "satellite", "hybrid", "terrain"],
        help="Map type.",
    )
    p.add_argument(
        "--label",
        help="Single-character marker label (default: first letter of pet name).",
    )

    # Output formatting
    p.add_argument("--format", choices=["json", "text"], default="json")
    p.add_argument("--pretty", action="store_true")

    return p


def main() -> int:
    args = build_parser().parse_args()

    # Map API key
    api_key = _env_first("GOOGLE_MAPS_API_KEY", "GMAPS_API_KEY")
    if not api_key:
        _emit_error(
            fmt=args.format,
            pretty=args.pretty,
            error_type="missing_prerequisite",
            message="Missing GOOGLE_MAPS_API_KEY (Google Maps Static API).",
            details={
                "hint": "Set GOOGLE_MAPS_API_KEY in the agent environment. See references/maps.md for setup.",
            },
        )
        return ExitCode.INVALID_ARGS

    try:
        # PetTracer snapshot
        token = pt.get_token_or_login(username=args.username, password=args.password, timeout_s=args.timeout_s, retries=args.retries)
        devices = pt.fetch_devices(token=token, timeout_s=args.timeout_s, retries=args.retries)
        sel = pt.select_device(devices, device_id=args.device_id, pet_name=args.pet)
        device = next(d for d in devices if int(d.get("id")) == sel.device_id)

        now = datetime.now(timezone.utc)
        summary = pt._summarise_device(device, now=now)  # type: ignore[attr-defined]

        pos = summary.get("last_fix", {})
        lat = pos.get("lat")
        lon = pos.get("lon")

        if lat is None or lon is None:
            payload = {
                "pet": asdict(sel),
                "error": "no_recent_fix",
                "last_contact": summary.get("last_contact"),
                "last_contact_age_s": summary.get("last_contact_age_s"),
                "battery_mv": summary.get("battery_mv"),
                "battery_percent_est": summary.get("battery_percent_est"),
                "mode_id": summary.get("mode_id"),
                "mode_name": summary.get("mode_name"),
            }
            _emit(payload, fmt=args.format, pretty=args.pretty)
            return ExitCode.OK

        lat_f = float(lat)
        lon_f = float(lon)

        out_path = args.out or _default_out_path(pet_name=sel.name, device_id=sel.device_id)
        label = (args.label or _label_from_name(sel.name)).upper()[:1]

        url = build_google_static_url(
            lat=lat_f,
            lon=lon_f,
            api_key=str(api_key),
            zoom=int(args.zoom),
            size=str(args.size),
            scale=int(args.scale),
            maptype=str(args.maptype),
            label=label,
        )

        # Download image
        n_bytes, content_type = _download_image(url, out_path=out_path, timeout_s=args.timeout_s)

        # Compute expected pixel dimensions from size*scale when possible.
        width_px: Optional[int] = None
        height_px: Optional[int] = None
        try:
            w_s, h_s = str(args.size).lower().split("x", 1)
            width_px = int(w_s) * int(args.scale)
            height_px = int(h_s) * int(args.scale)
        except Exception:
            pass

        payload = {
            "pet": asdict(sel),
            "provider": "google_maps_static",
            "image": {
                "path": out_path,
                "content_type": content_type,
                "bytes": n_bytes,
                "width_px": width_px,
                "height_px": height_px,
            },
            "last_fix": {
                "lat": lat_f,
                "lon": lon_f,
                "time": summary.get("last_fix_time"),
                "age_s": summary.get("last_fix_age_s"),
                "accuracy_m": pos.get("accuracy_m"),
            },
            "map": {
                "zoom": int(args.zoom),
                "maptype": str(args.maptype),
                "size": str(args.size),
                "scale": int(args.scale),
                "marker_label": label,
            },
            "links": {
                "google_maps": f"https://www.google.com/maps?q={lat_f},{lon_f}",
                "openstreetmap": f"https://www.openstreetmap.org/?mlat={lat_f}&mlon={lon_f}#map=18/{lat_f}/{lon_f}",
            },
        }

        _emit(payload, fmt=args.format, pretty=args.pretty)
        return ExitCode.OK

    except pt.PetTracerNotFoundError as e:
        _emit_error(fmt=args.format, pretty=args.pretty, error_type="not_found", message=str(e))
        return ExitCode.NOT_FOUND
    except pt.PetTracerAuthError as e:
        _emit_error(fmt=args.format, pretty=args.pretty, error_type="auth", message=str(e))
        return ExitCode.AUTH
    except TimeoutError as e:
        _emit_error(fmt=args.format, pretty=args.pretty, error_type="timeout", message=str(e))
        return ExitCode.TIMEOUT
    except pt.PetTracerApiError as e:
        _emit_error(fmt=args.format, pretty=args.pretty, error_type="api_error", message=str(e))
        return ExitCode.ERROR
    except Exception as e:
        _emit_error(fmt=args.format, pretty=args.pretty, error_type="error", message=str(e))
        return ExitCode.ERROR


if __name__ == "__main__":
    raise SystemExit(main())
