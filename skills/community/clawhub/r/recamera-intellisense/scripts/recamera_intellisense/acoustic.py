"""Acoustic / sound-event detection model API (``/extension/acousticslab``)."""

from __future__ import annotations

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from recamera_intellisense._cli import main

    raise SystemExit(main())

from typing import Any, Dict, List, Optional

from . import _config, _http
from ._errors import RecameraError

__all__ = ["get_active_acoustic_model", "list_acoustic_models",
           "set_acoustic_model"]

PATH_ACTIVE = "/extension/acousticslab/api/v1/active"
PATH_WORKSPACES = "/extension/acousticslab/api/v1/workspaces"
PATH_HEADS = "/extension/acousticslab/api/v1/workspaces/{}/heads"


def get_active_acoustic_model(device_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Return the active sound-event model, or `None`.

    Keys: `runtime_head_id`, `labels`, `n_classes?`, `sha256?`,
    `activated_at?`. `labels` feeds the `label_filter` of inference_set rules
    with `source_filter=["acousticslab"]`. `None` means the AcousticsLab app
    is stopped (lifecycle-managed in the App Center).
    """
    dev = _config.resolve(device_name)
    data = _http.get_json(dev, PATH_ACTIVE)
    if not isinstance(data, dict):
        return None
    labels = [c for c in (data.get("labels") or []) if isinstance(c, str)]
    if not data.get("runtime_head_id") and not labels:
        return None
    return {
        "runtime_head_id": data.get("runtime_head_id", ""),
        "labels": labels,
        "n_classes": data.get("n_classes"),
        "sha256": data.get("sha256"),
        "activated_at": data.get("activated_at"),
    }


def list_acoustic_models(device_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """All trained heads across workspaces; the active one is marked
    ``active: true``. [] when the AcousticsLab app is stopped. Read-only:
    head activation is a separate deliberate action."""
    dev = _config.resolve(device_name)
    try:
        ws_data = _http.get_json(dev, PATH_WORKSPACES)
    except RecameraError:
        return []  # AcousticsLab stopped / unreachable
    if not isinstance(ws_data, dict):
        return []
    active_id = ""
    try:
        active = get_active_acoustic_model(device_name)
        active_id = (active or {}).get("runtime_head_id", "")
    except RecameraError:
        pass
    out: List[Dict[str, Any]] = []
    for ws in ws_data.get("workspaces") or []:
        if not isinstance(ws, dict) or not ws.get("id"):
            continue
        try:
            heads_data = _http.get_json(dev, PATH_HEADS.format(ws["id"]))
        except RecameraError:
            continue
        for head in (heads_data or {}).get("heads") or []:
            if not isinstance(head, dict) or not head.get("head_id"):
                continue
            out.append({
                "workspace_id": ws["id"],
                "workspace_name": ws.get("name", ""),
                "head_id": head["head_id"],
                "n_classes": head.get("n_classes"),
                "created_at": head.get("created_at"),
                "status": head.get("status", ""),
                "active": head["head_id"] == active_id,
            })
    return out


COMMANDS = {"get_active_acoustic_model": get_active_acoustic_model,
            "list_acoustic_models": list_acoustic_models}


def set_acoustic_model(
    device_name: Optional[str] = None,
    *,
    workspace_id: Optional[str] = None,
    head_id: Optional[str] = None,
    default: bool = False,
) -> Dict[str, Any]:
    """Switch the live acoustic inference head (ids from
    ``list_acoustic_models``); ``default=true`` restores the factory head.
    Requires the AcousticsLab app running — start it first otherwise.
    """
    dev = _config.resolve(device_name)
    if default:
        if workspace_id or head_id:
            raise ValueError(
                "default=true cannot be combined with workspace_id/head_id")
        payload: Dict[str, Any] = {"default": True}
    else:
        if not workspace_id or not head_id:
            raise ValueError(
                "workspace_id and head_id are required (or default=true); "
                "see list_acoustic_models")
        try:
            ws_data = _http.get_json(dev, PATH_WORKSPACES)
        except RecameraError as exc:
            raise RecameraError(
                "AcousticsLab console unreachable — is the app running? "
                "(start_app 'acousticslab'); " + str(exc)) from exc
        workspaces = (ws_data or {}).get("workspaces") or []
        ws_ids = [w.get("id") for w in workspaces]
        if workspace_id not in ws_ids:
            raise ValueError(
                f"unknown workspace_id {workspace_id!r}; available: {ws_ids}")
        heads_data = _http.get_json(dev, PATH_HEADS.format(workspace_id))
        heads = (heads_data or {}).get("heads") or []
        head_ids = [h.get("head_id") for h in heads]
        if head_id not in head_ids:
            raise ValueError(
                f"unknown head_id {head_id!r} in workspace {workspace_id}; "
                f"available: {head_ids}")
        payload = {"workspace_id": workspace_id, "head_id": head_id}
    # Plain JSON response (no envelope): HTTP status is the error signal.
    _http.post_json(dev, PATH_ACTIVE, payload=payload)
    return {"changed": True, "default": bool(default),
            "workspace_id": workspace_id, "head_id": head_id}


COMMANDS["set_acoustic_model"] = set_acoustic_model
