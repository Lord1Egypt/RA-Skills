"""App Center applications: listing and logs (``/api/app-center/v1/apps``).

Building NEW apps is the recamera-pysdk skill's domain."""

from __future__ import annotations

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from recamera_intellisense._cli import main

    raise SystemExit(main())

import re
from typing import Any, Dict, List, Optional

from . import _config, _http
from ._errors import RecameraError

__all__ = ["list_apps", "get_app_logs", "start_app", "stop_app", "restart_app"]

PATH_APPS = "/api/app-center/v1/apps"

MAX_LOG_TAIL = 2000

# Mirrors the appmgr route guard; app_id is URL-path interpolated.
_APP_ID_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def _require_app_id(app_id: Any) -> str:
    app_id = str(app_id or "")
    if not _APP_ID_RE.match(app_id):
        raise ValueError(
            f"invalid app_id {app_id!r}: must match {_APP_ID_RE.pattern} "
            "(see list_apps)"
        )
    return app_id


def list_apps(device_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """App Center apps, normalized: ``{id, name, name_zh, version, status,
    system, installed, description}``.

    ``system`` marks firmware apps (``builtin``, ``acousticslab``) that cannot
    be uninstalled. A stopped app produces no frames for recording rules."""
    dev = _config.resolve(device_name)
    data = _http.get_json(dev, PATH_APPS)
    if data is None:
        data = {}  # codebase GET norm: tolerate an empty body
    if not isinstance(data, dict):
        raise RecameraError("list apps failed: unexpected payload")
    out: List[Dict[str, Any]] = []
    for app in data.get("apps") or []:
        if not isinstance(app, dict) or not app.get("id"):
            continue
        manifest = app.get("manifest") or {}
        out.append({
            "id": app["id"],
            "name": app.get("name") or manifest.get("name") or app["id"],
            "name_zh": app.get("name_zh") or manifest.get("name_zh"),
            "version": app.get("version") or manifest.get("version"),
            "status": app.get("status", ""),
            "system": bool(app.get("system") or app.get("type") == "system"
                           or app.get("type") == "builtin"),
            "installed": bool(app.get("installed", True)),
            "description": app.get("description") or manifest.get("description") or "",
        })
    return out


def get_app_logs(
    device_name: Optional[str] = None,
    *,
    app_id: str,
    tail: int = 200,
) -> Dict[str, Any]:
    """The app's recent log lines: ``{id, lines, text}``; ``tail`` clamps to
    [1, 2000] and spans the rotated log."""
    dev = _config.resolve(device_name)
    app_id = _require_app_id(app_id)
    tail = min(MAX_LOG_TAIL, max(1, int(tail)))
    data = _http.get_json(dev, f"{PATH_APPS}/{app_id}/logs",
                          params={"tail": str(tail)})
    if not isinstance(data, dict):
        raise RecameraError(f"get app logs failed for {app_id!r}: unexpected payload")
    return {
        "id": data.get("id", app_id),
        "lines": [line for line in (data.get("lines") or []) if isinstance(line, str)],
        "text": data.get("text", ""),
    }


COMMANDS = {"list_apps": list_apps, "get_app_logs": get_app_logs}


def _lifecycle(app_id: Any, action: str, device_name: Optional[str] = None,
               *, confirm: bool = False) -> Dict[str, Any]:
    app_id = _require_app_id(app_id)
    apps = list_apps(device_name)
    app = next((a for a in apps if a["id"] == app_id), None)
    if app is None:
        raise ValueError(
            f"unknown app {app_id!r}; installed: {[a['id'] for a in apps]}")
    if action != "start" and app.get("system") and not confirm:
        raise ValueError(
            f"{action} on system app {app_id!r} interrupts a firmware-managed "
            "result source (recording rules fed by it go silent) — re-run "
            "with confirm=true")
    # Plain JSON response (no envelope): HTTP status is the error signal.
    dev = _config.resolve(device_name)
    _http.post_json(dev, f"{PATH_APPS}/{app_id}/{action}", payload={})
    return {"changed": True, "id": app_id, "action": action, "async": True}


def start_app(app_id: str, device_name: Optional[str] = None) -> Dict[str, Any]:
    """Start an app (202 queued; poll `list_apps` for status ``running``)."""
    return _lifecycle(app_id, "start", device_name)


def stop_app(app_id: str, device_name: Optional[str] = None, *,
             confirm: bool = False) -> Dict[str, Any]:
    """Stop an app. Stopping a SYSTEM app requires ``confirm=true``."""
    return _lifecycle(app_id, "stop", device_name, confirm=confirm)


def restart_app(app_id: str, device_name: Optional[str] = None, *,
                confirm: bool = False) -> Dict[str, Any]:
    """Restart an app. Restarting a SYSTEM app requires ``confirm=true``."""
    return _lifecycle(app_id, "restart", device_name, confirm=confirm)


COMMANDS.update({
    "start_app": start_app,
    "stop_app": stop_app,
    "restart_app": restart_app,
})
