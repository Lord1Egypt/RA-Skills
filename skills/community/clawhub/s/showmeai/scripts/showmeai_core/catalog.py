"""Model catalog and current-token availability intersection."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .errors import SkillError


CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "model-catalog.json"
CREATIVE_CATEGORIES = ("image", "video", "3d", "tts", "stt", "music", "image_tool")

CREATIVE_ID_HINTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("3d", ("3d", "trellis")),
    ("video", ("video", "seedance", "sora", "veo", "kling", "hailuo", "vidu")),
    ("tts", ("tts", "speech", "voice", "cosyvoice")),
    ("stt", ("whisper", "stt", "transcri")),
    ("music", ("music", "suno", "chirp", "udio")),
    ("image", ("image", "banana", "imagen", "flux", "ideogram", "seedream", "recraft")),
)


def load_catalog() -> dict[str, Any]:
    try:
        payload = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SkillError("CATALOG_INVALID", f"Cannot read model catalog: {error}") from error
    if payload.get("schema_version") != 1 or not isinstance(payload.get("models"), list):
        raise SkillError("CATALOG_INVALID", "Unsupported model catalog schema.")
    return payload


def index_catalog(catalog: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    catalog = catalog or load_catalog()
    index: dict[str, dict[str, Any]] = {}
    for model in catalog["models"]:
        index[model["id"]] = model
        for alias in model.get("aliases", []):
            index[alias] = model
    return index


def normalize_live_models(payload: Any) -> list[str]:
    raw = payload.get("data", payload) if isinstance(payload, dict) else payload
    if isinstance(raw, dict):
        raw = raw.get("models", [])
    if not isinstance(raw, list):
        return []
    values: list[str] = []
    for item in raw:
        model_id = item.get("id") if isinstance(item, dict) else item
        if isinstance(model_id, str) and model_id not in values:
            values.append(model_id)
    return values


def infer_creative_category(model_id: str) -> str:
    """Classify newly released creative IDs without treating language models as media models."""
    lowered = model_id.lower()
    for category, hints in CREATIVE_ID_HINTS:
        if any(hint in lowered for hint in hints):
            return category
    return ""


def grouped_models(live_ids: list[str], include_catalog_tasks: bool = True) -> dict[str, list[dict[str, Any]]]:
    catalog = load_catalog()
    index = index_catalog(catalog)
    groups: dict[str, list[dict[str, Any]]] = {category: [] for category in CREATIVE_CATEGORIES}
    seen: set[str] = set()
    for live_id in live_ids:
        model = index.get(live_id)
        if not model:
            category = infer_creative_category(live_id)
            if category:
                groups[category].append(
                    {
                        "id": live_id,
                        "selected_id": live_id,
                        "label": f"{live_id} (new; parameter schema not cataloged)",
                        "category": category,
                        "operations": [],
                        "params": {},
                        "availability": "verified_uncataloged",
                    }
                )
            continue
        item = dict(model)
        item["selected_id"] = live_id
        item["availability"] = "verified"
        groups[item["category"]].append(item)
        seen.add(model["id"])
    if include_catalog_tasks:
        for model in catalog["models"]:
            if model.get("task_api") and model["id"] not in seen:
                item = dict(model)
                item["selected_id"] = model["id"]
                item["availability"] = "verify_on_use"
                groups[item["category"]].append(item)
    return groups


def available_hash(live_ids: list[str]) -> str:
    joined = "\n".join(sorted(live_ids)).encode("utf-8")
    return hashlib.sha256(joined).hexdigest()[:16]


def model_definition(model_id: str) -> dict[str, Any] | None:
    return index_catalog().get(model_id)


def validate_params(model_id: str, params: dict[str, Any], *, reject_unknown: bool = False) -> dict[str, Any]:
    definition = model_definition(model_id)
    if not definition:
        return params
    specs = definition.get("params", {})
    validated: dict[str, Any] = {}
    for key, value in params.items():
        spec = specs.get(key)
        if spec is None:
            if reject_unknown:
                raise SkillError(
                    "UNSUPPORTED_MODEL_PARAMETER",
                    f"{key} is not supported by {model_id}.",
                    details={"model": model_id, "parameter": key, "supported_parameters": sorted(specs)},
                )
            continue
        if value is None or value == "":
            continue
        if spec["type"] == "integer":
            value = int(value)
        elif spec["type"] == "number":
            value = float(value)
        elif spec["type"] == "boolean":
            value = bool(value)
        if "minimum" in spec and value < spec["minimum"]:
            raise SkillError("PARAM_INVALID", f"{key} must be >= {spec['minimum']}.")
        if "maximum" in spec and value > spec["maximum"]:
            raise SkillError("PARAM_INVALID", f"{key} must be <= {spec['maximum']}.")
        if "values" in spec and value not in spec["values"]:
            raise SkillError("PARAM_INVALID", f"{key} must be one of {spec['values']}.")
        validated[key] = value
    return validated


def recommended_image_model(live_ids: list[str]) -> str:
    for candidate in ("gemini-3.1-flash-image", "gpt-image-2", "gemini-3-pro-image", "nano-banana"):
        for live_id in live_ids:
            definition = model_definition(live_id)
            if definition and definition["id"] == candidate:
                return live_id
    for live_id in live_ids:
        definition = model_definition(live_id)
        if (definition and definition.get("category") == "image") or infer_creative_category(live_id) == "image":
            return live_id
    return "gemini-3.1-flash-image"
