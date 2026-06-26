"""Central HTTP entry for generated swagger-skills API clients."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import requests

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from field_mapper import transform_response
from skill_common import (
    field_index_path,
    get_default_timeout,
    get_field_mapping_enabled,
    join_api_url,
)


def _raw_json_requested() -> bool:
    value = os.environ.get("SWAGGER_RAW_JSON", "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _should_apply_mapping(apply_field_mapping: bool | None, config_path: str | Path | None) -> bool:
    if _raw_json_requested():
        return False
    if apply_field_mapping is not None:
        return bool(apply_field_mapping)
    return get_field_mapping_enabled(config_path=config_path)


def _parse_response_json(response: requests.Response) -> Any:
    text = response.text
    if not text.strip():
        return None
    try:
        return response.json()
    except ValueError:
        return {"_raw": text}


def call_api_json(
    document_id: str,
    method: str,
    path_template: str,
    *,
    path_params: dict[str, Any] | None = None,
    http_method: str | None = None,
    path: str | None = None,
    operation_id: str | None = None,
    apply_field_mapping: bool | None = None,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    json_body: Any | None = None,
    data: Any | None = None,
    timeout: int | None = None,
    config_path: str | Path | None = None,
) -> Any:
    """Call a business API and return parsed JSON with optional field key mapping."""

    del operation_id  # reserved for future route-specific overrides

    url = join_api_url(
        document_id,
        path_template,
        path_params,
        config_path=config_path,
    )
    effective_timeout = timeout if timeout is not None else get_default_timeout(config_path=config_path)
    response = requests.request(
        method=method.upper(),
        url=url,
        params=params,
        headers=headers,
        json=json_body,
        data=data,
        timeout=effective_timeout,
    )
    response.raise_for_status()
    payload = _parse_response_json(response)

    route_method = http_method or method
    route_path = path or path_template
    for key, value in (path_params or {}).items():
        route_path = route_path.replace("{" + key + "}", str(value))

    if not _should_apply_mapping(apply_field_mapping, config_path):
        return payload
    if payload is None:
        return payload

    return transform_response(
        payload,
        http_method=str(route_method),
        path=str(route_path),
        index_path=field_index_path(),
    )
