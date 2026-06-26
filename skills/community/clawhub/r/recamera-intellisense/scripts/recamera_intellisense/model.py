"""Detection model management (``/model/{list,inference}``)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from . import _config, _http
from ._errors import RecameraError

__all__ = [
    "get_detection_models_info",
    "get_detection_model",
    "set_detection_model",
]

PATH_LIST = "/cgi-bin/entry.cgi/model/list"
PATH_INFERENCE = "/cgi-bin/entry.cgi/model/inference"


def _parse_model(index: int, d: Dict[str, Any]) -> Dict[str, Any]:
    info = d.get("modelInfo") if isinstance(d.get("modelInfo"), dict) else {}
    labels_raw = info.get("classes") or []
    labels = [c for c in labels_raw if isinstance(c, str)]
    return {
        "id": int(index),
        "name": d.get("model", ""),
        "algorithm": info.get("algorithm"),
        "framework": info.get("framework"),
        "version": info.get("version"),
        "labels": labels,
    }


def get_detection_models_info(device_name: str) -> List[Dict[str, Any]]:
    """List installed detection models."""
    dev = _config.resolve(device_name)
    data = _http.get_json(dev, PATH_LIST)
    if isinstance(data, list):
        models = data
    elif isinstance(data, dict):
        models = data.get("lModels") or []
    else:
        models = []
    return [_parse_model(i, m) for i, m in enumerate(models) if isinstance(m, dict)]


def get_detection_model(device_name: str) -> Optional[Dict[str, Any]]:
    """Currently-active detection model, or ``None``."""
    dev = _config.resolve(device_name)
    data = _http.get_json(dev, PATH_INFERENCE) or {}
    if not data.get("iEnable"):
        return None
    name = data.get("sModel")
    if not name:
        return None
    for m in get_detection_models_info(device_name):
        if m["name"] == name:
            return {
                **m,
                "fps": int(data.get("iFPS", 0) or 0),
                "status": data.get("sStatus"),
            }
    return {
        "id": -1,
        "name": name,
        "labels": [],
        "fps": int(data.get("iFPS", 0) or 0),
        "status": data.get("sStatus"),
    }


def set_detection_model(
    device_name: str,
    *,
    model_id: Optional[int] = None,
    model_name: Optional[str] = None,
    fps: int = 30,
) -> Dict[str, Any]:
    """Activate a detection model by id or by name."""
    if model_id is None and model_name is None:
        raise ValueError("set_detection_model requires 'model_id' or 'model_name'.")
    dev = _config.resolve(device_name)
    models = get_detection_models_info(device_name)
    if model_id is None:
        match = next((m for m in models if m["name"] == model_name), None)
        if match is None:
            raise ValueError(f"Model {model_name!r} is not installed.")
    else:
        match = next((m for m in models if m["id"] == int(model_id)), None)
        if match is None:
            raise ValueError(f"Model id {model_id} is not installed.")
    payload = {"iEnable": 1, "iFPS": int(fps), "sModel": match["name"]}
    resp = _http.post_json(
        dev, PATH_INFERENCE, params={"id": match["id"]}, payload=payload
    )
    _http.expect_ok(resp, "set detection model")
    result = get_detection_model(device_name)
    if result is None:
        raise RecameraError(
            "Device reported detection model is not active after setting it."
        )
    return result


COMMANDS = {
    "get_detection_models_info": get_detection_models_info,
    "get_detection_model": get_detection_model,
    "set_detection_model": set_detection_model,
}
COMMAND_SCHEMAS = {
    "get_detection_models_info": {"required": {"device_name"}, "optional": set()},
    "get_detection_model": {"required": {"device_name"}, "optional": set()},
    "set_detection_model": {
        "required": {"device_name"},
        "optional": {"model_id", "model_name", "fps"},
    },
}
