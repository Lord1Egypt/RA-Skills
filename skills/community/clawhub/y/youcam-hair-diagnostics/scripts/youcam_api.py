"""YouCam AI API calls

Each call here makes a single request and returns the parsed response.
Multi-step flows like upload -> create task -> poll live in youcam_tasks.py.
"""

import json
import os
from typing import Any, Optional
from urllib.parse import urlparse

import requests
import yaml

from constants import (
    DEFAULT_API_BALANCE_PATH,
    DEFAULT_API_FEAT_COST_PATH,
    DEFAULT_UPLOAD_PATH,
    CREDENTIALS_FILE,
    API_FALLBACK_DOC,
    REQUEST_TIMEOUT,
    SUPPORT_FILE_TYPES,
    UPLOAD_TIMEOUT,
)
from youcam_init import exit_with_error


def load_contract(feature: Optional[str] = None) -> dict[str, Any]:
    """Load api-fallback.yaml describing base URL, billing, and features.

    Args:
        feature: Which feature's config to load, e.g. "skin-analysis". If omitted, the returned "features" dict is empty.

    Returns:
        dict[str, Any]: {"base_url": str, "credit": dict, "features": {feature: dict} or {}}.
    """
    with open(API_FALLBACK_DOC, "r", encoding="utf-8") as fh:
        loader = yaml.SafeLoader(fh)
        try:
            root = loader.get_single_node()
            contract: dict[str, Any] = {"features": {}}
            for key_node, val_node in root.value:
                key = loader.construct_object(key_node)
                if key != "features":
                    contract[key] = loader.construct_object(val_node, deep=True)
                    continue
                if feature is None:
                    continue
                names, found = [], None
                for fkey_node, fval_node in val_node.value:
                    name = loader.construct_object(fkey_node)
                    names.append(name)
                    if name == feature:
                        found = fval_node
                if found is None:
                    raise ValueError(f"Unknown feature '{feature}'. Valid features: {sorted(names)}")
                contract["features"][feature] = loader.construct_object(found, deep=True)
        finally:
            loader.dispose()
    return contract


def feature_cfg(contract: dict[str, Any], feature: str, version: Optional[str] = None) -> dict[str, Any]:
    """Resolve one feature's config from the api-fallback.yaml, with an optional version override applied to task_path.

    Args:
        contract: The loaded contract (from load_contract), containing the feature's config.
        feature: Which feature to resolve, e.g. "skin-analysis".
        version: Which version of the feature to use. Defaults to the feature's version as recorded in api-fallback.yaml
                 if not given.

    Returns:
        dict[str, Any]: A copy of the feature's config with "_task_path" and "_version" resolved for the chosen version.
    """
    feats = contract.get("features", {})
    if feature not in feats:
        raise ValueError(f"Unknown feature '{feature}'. Valid features: {sorted(feats)}")
    cfg = dict(feats[feature])
    default_ver = cfg["version"]
    ver = version or default_ver  # lets the LLM override the version from the live doc
    cfg["_task_path"] = cfg["task_path"].replace(default_ver, ver, 1)
    cfg["_version"] = ver
    return cfg


# ---------- API ----------


def get_key() -> str:
    """Resolve the API key from the YOUCAM_API_KEY env var or credentials.json.

    Exits with code 2 and a structured error if no usable key is configured.

    Returns:
        str: The resolved API key.
    """
    env = os.environ.get("YOUCAM_API_KEY")
    if env:
        return env

    example = os.path.join(os.path.dirname(CREDENTIALS_FILE), "credentials.example.json")
    format_hint = f" (see {example} for the expected format)." if os.path.isfile(example) else ""
    if not os.path.isfile(CREDENTIALS_FILE):
        exit_with_error(
            "No API key configured.",
            hint=f'Set the YOUCAM_API_KEY env var, or create {CREDENTIALS_FILE} with {{"api_key": "..."}}'
            + format_hint,
            details="Neither YOUCAM_API_KEY nor credentials.json was found.",
            code=2,
        )

    hint = f"Set the YOUCAM_API_KEY env var, or fix {CREDENTIALS_FILE}" + format_hint
    try:
        with open(CREDENTIALS_FILE, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        exit_with_error("Could not read api_key.", hint=hint, details=f"{CREDENTIALS_FILE}: {exc}", code=2)
    if not isinstance(data, dict):
        exit_with_error(
            "Could not read api_key.",
            hint=hint,
            details=f'{CREDENTIALS_FILE} must contain a JSON object like {{"api_key": "..."}}.',
            code=2,
        )
    key = data.get("api_key")
    if not key:
        exit_with_error(
            "Could not read api_key.",
            hint=hint,
            details=f'{CREDENTIALS_FILE} has no "api_key" field.',
            code=2,
        )
    return key


def get_credits(key: str) -> dict[str, Any]:
    """Fetch the account's credit balance, split into spendable units and totals by type.

    Args:
        key: The API key to authenticate with.

    Returns:
        dict[str, Any]: {"api_spendable_units": int, "by_type": dict}.
    """
    contract = load_contract()
    cr = contract.get("credit", {})
    base = contract["base_url"]
    prefix = cr.get("api_spendable_prefix", "Api")
    r = requests.get(
        f"{base}{cr.get('balance_path', DEFAULT_API_BALANCE_PATH)}",
        headers=headers(key),
        timeout=REQUEST_TIMEOUT,
    )
    r.raise_for_status()
    batches = r.json().get("results", []) or []
    spendable = sum(b.get("amount", 0) for b in batches if str(b.get("type", "")).startswith(prefix))
    by_type = {}
    for b in batches:
        by_type[b.get("type", "?")] = by_type.get(b.get("type", "?"), 0) + b.get("amount", 0)
    return {"api_spendable_units": spendable, "by_type": by_type}


def get_feature_cost(key: str, feature: Optional[str] = None) -> list[dict[str, Any]]:
    """Fetch per-call credit costs for one feature, or all features if none is given.

    Args:
        key: The API key to authenticate with.
        feature: Which feature to filter costs for. If not given, returns costs for all features.

    Returns:
        list[dict[str, Any]]: One entry per SKU with "description", "amount", "unit", "proc_unit", and "feature".
    """
    contract = load_contract(feature)
    path = contract.get("credit", {}).get("feature_cost_path", DEFAULT_API_FEAT_COST_PATH)
    base = contract["base_url"]
    skus, token = [], None
    while True:
        params = {"page_size": 20}
        if token:
            params["starting_token"] = token
        r = requests.get(f"{base}{path}", headers=headers(key), params=params, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        res = r.json().get("result", {}) or {}
        skus += res.get("skus", []) or []
        token = res.get("next_token")
        if not token:
            break

    def slug_of(u: str) -> str:
        return u.rstrip("/").split("/task/")[-1] if u and "/task/" in u else "(other)"

    if feature:
        # Match on the exact endpoint `run` calls: a slug can have several priced endpoints,
        # e.g. image-to-video (V1.0) vs image-to-video/youcam (V2.0), or v2.0 vs v2.1.
        task_path = feature_cfg(contract, feature)["_task_path"]
        skus = [s for s in skus if urlparse(s.get("run_task_url") or "").path == task_path]
    return [
        {
            "description": s.get("description"),
            "amount": s.get("amount"),
            "unit": s.get("unit"),
            "proc_unit": s.get("proc_unit"),
            "feature": slug_of(s.get("run_task_url", "")),
        }
        for s in skus
    ]


def list_templates(
    key: str,
    feature: str,
    version: Optional[str] = None,
    page_size: int = 20,
    starting_token: Optional[str] = None,
) -> dict[str, Any]:
    """Fetch one page of a feature's predefined templates (e.g. look-vto looks, hair-transfer styles).

    Args:
        key: The API key to authenticate with.
        feature: Which feature to list templates for, e.g. "look-vto".
        version: Which version of the feature to use. Defaults to the feature's version
            as recorded in the contract if not given.
        page_size: How many templates to return in this page (the API allows 1-20).
        starting_token: The `next_token` from the previous page. Omit for the first page.

    Returns:
        dict[str, Any]: {"templates": list of {"id", "title", "thumb", ...}, "next_token": str or None}.
                        Pass a template's "id" as `template_id` when running the feature.

    Raises:
        ValueError: The feature has no predefined templates.
    """
    contract = load_contract(feature)
    cfg = feature_cfg(contract, feature, version)
    path = cfg.get("template_list")
    if not path:
        raise ValueError(f"feature '{feature}' has no predefined templates to list")
    path = path.replace(cfg["version"], cfg["_version"], 1)
    params: dict[str, Any] = {"page_size": page_size}
    if starting_token:
        params["starting_token"] = starting_token
    r = requests.get(
        f"{contract['base_url']}{path}", headers=headers(key), params=params, timeout=REQUEST_TIMEOUT
    )
    r.raise_for_status()
    data = r.json().get("data", {}) or {}
    return {"templates": data.get("templates", []) or [], "next_token": data.get("next_token")}


def upload_file(contract: dict[str, Any], file_path: str, key: str) -> str:
    """Upload a local file and return its file_id.

    Uploads always go through the single generic upload endpoint (contract["file_path"],
    falling back to DEFAULT_UPLOAD_PATH), which every feature shares.

    Args:
        contract: The loaded API contract, e.g. from load_contract().
        file_path: Path to the local file to upload. Must be jpg, jpeg, png, or mp4.
        key: The API key to authenticate the request with.

    Returns:
        str: The uploaded file's file_id.

    Raises:
        FileNotFoundError: file_path doesn't point to an existing local file.
        ValueError: The file's extension isn't a supported type.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    base = contract["base_url"]
    ext = os.path.splitext(file_path)[1].lower()
    ct = SUPPORT_FILE_TYPES.get(ext)

    if not ct:
        raise ValueError(
            f"[Upload File] Unsupported extension {ext}. this engine does not convert files, "
            "provide jpg, jpeg, or png, or mp4 for video"
        )
    meta = requests.post(
        f"{base}{contract.get('file_path', DEFAULT_UPLOAD_PATH)}",
        headers=headers(key),
        json={
            "files": [
                {
                    "content_type": ct,
                    "file_name": os.path.basename(file_path),
                    "file_size": os.path.getsize(file_path),
                }
            ]
        },
        timeout=REQUEST_TIMEOUT,
    )
    meta.raise_for_status()
    info = meta.json()["data"]["files"][0]
    put_req = info["requests"][0]
    with open(file_path, "rb") as fh:
        requests.put(
            put_req["url"],
            headers=put_req.get("headers", {"Content-Type": ct}),
            data=fh,
            timeout=UPLOAD_TIMEOUT,
        ).raise_for_status()
    return info["file_id"]


def create_task(
    contract: dict[str, Any], feature: str, body: dict[str, Any], key: str, version: Optional[str] = None
) -> str:
    """Create a processing task for a feature and return its task_id.

    Args:
        contract: The feature's loaded API contract, e.g. from load_contract().
        feature: Which YouCam feature to create a task for, e.g. "skin-analysis".
        body: The request payload, e.g. file_id(s)/url(s) and any feature-specific params.
        key: The API key to authenticate the request with.
        version: Which version of the feature to call. Defaults to the standard version.

    Returns:
        str: The created task's task_id.
    """
    base, cfg = contract["base_url"], feature_cfg(contract, feature, version)
    r = requests.post(f"{base}{cfg['_task_path']}", headers=headers(key), json=body, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()["data"]["task_id"]


def get_task(
    contract: dict[str, Any], feature: str, task_id: str, key: str, version: Optional[str] = None
) -> dict[str, Any]:
    """Fetch a task's current status once.

    Args:
        contract: The feature's loaded API contract, e.g. from load_contract().
        feature: Which YouCam feature this task belongs to, e.g. "skin-analysis".
        task_id: The task to check, as returned by create_task().
        key: The API key to authenticate the request with.
        version: Which version of the feature to call. Defaults to the standard version.

    Returns:
        dict[str, Any]: The task's "data" payload, including "task_status".
    """
    base, cfg = contract["base_url"], feature_cfg(contract, feature, version)
    r = requests.get(f"{base}{cfg['_task_path']}/{task_id}", headers=headers(key), timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json().get("data", {})


def headers(key: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json", "X-Pxy-Src": "skill"}
