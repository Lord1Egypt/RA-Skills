#!/usr/bin/env python3
"""Universal ShowMeAI CLI: setup, models, config, generation, and durable tasks."""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import getpass
import json
import sys
from pathlib import Path
from typing import Any

from showmeai_core.catalog import (
    available_hash,
    grouped_models,
    load_catalog,
    model_definition,
    normalize_live_models,
    recommended_image_model,
    validate_params,
)
from showmeai_core.config import (
    DEFAULT_BASE_URL,
    ONBOARDING_CATEGORIES,
    complete_onboarding_category,
    load_config,
    onboarding_status,
    public_config,
    resolve_api_key,
    reset_onboarding_category,
    save_api_key,
    save_config,
    set_path,
)
from showmeai_core.errors import HttpError, SkillError, error_result
from showmeai_core.http import ApiClient
from showmeai_core.outputs import OutputManager
from showmeai_core.paths import config_dir, config_file, credentials_file, state_dir
from showmeai_core.tasks import TaskJournal, TaskRecord, TaskRunner, normalize_response


VERSION = "2.1.0"
MAX_IMAGE_COUNT = 10
DEFAULT_IMAGE_CONCURRENCY = 4
GROUP_NOTICE = (
    "The displayed models reflect only this API key's token group, not the full ShowMeAI catalog. "
    "If a desired model is missing, change the token group or enable automatic grouping in the "
    "ShowMeAI console, then run `models` or `setup` again."
)


def _emit(result: dict[str, Any], *, compact: bool = False) -> None:
    print(json.dumps(result, ensure_ascii=False, indent=None if compact else 2))
    if result.get("ok"):
        for path in result.get("data", {}).get("files", []):
            print(f"MEDIA:{path}")


def _client(config: dict[str, Any], key: str | None = None) -> ApiClient:
    api_key = key or resolve_api_key()[0]
    base_url = str(config.get("api", {}).get("base_url", DEFAULT_BASE_URL)).rstrip("/")
    if not base_url:
        base_url = DEFAULT_BASE_URL
    return ApiClient(base_url, api_key)


def _ordered_candidates(models: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(models, key=lambda item: (item.get("recommended", 999), item.get("label", item["id"])))


def _public_groups(groups: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for category, models in groups.items():
        result[category] = [
            {
                "id": model["selected_id"],
                "canonical_id": model["id"],
                "label": model.get("label", model["id"]),
                "availability": model["availability"],
                "recommended": model.get("recommended") == 1,
                "recommendation_rank": model.get("recommended"),
                "params": model.get("params", {}),
            }
            for model in _ordered_candidates(models)
        ]
    return result


def _onboarding_error(category: str) -> SkillError:
    return SkillError(
        "ONBOARDING_REQUIRED",
        f"Choose and save a default {category} model before starting creative intake or generation.",
        details={
            "stage": "choose_default_model",
            "category": category,
            "blocking": True,
            "must_complete_before_generation": True,
            "models_command": f"python3 scripts/showmeai.py onboarding models --category {category} --json",
            "apply_command": (
                "python3 scripts/showmeai.py onboarding apply "
                f"--category {category} --model <MODEL_ID> --params-json '<JSON>' --json"
            ),
            "agent_instruction": "Complete onboarding before asking for prompt, style, dimensions, quality, or count.",
        },
    )


def _require_category_ready(config: dict[str, Any], category: str) -> None:
    if onboarding_status(config, category) != "complete":
        raise _onboarding_error(category)


def _candidate_for_model(candidates: list[dict[str, Any]], model_id: str) -> dict[str, Any] | None:
    requested = model_definition(model_id)
    for candidate in candidates:
        if candidate["selected_id"] == model_id:
            return candidate
        candidate_definition = model_definition(candidate["selected_id"])
        if requested and candidate_definition and requested["id"] == candidate_definition["id"]:
            return candidate
    return None


def _parse_value(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _prompt_value(name: str, spec: dict[str, Any], current: Any) -> Any:
    choices = f" choices={spec['values']}" if spec.get("values") else ""
    entered = input(f"  {name} [{current}]{choices}: ").strip()
    if not entered:
        return current
    kind = spec.get("type")
    if kind == "integer":
        return int(entered)
    if kind == "number":
        return float(entered)
    if kind == "boolean":
        return entered.lower() in {"1", "true", "yes", "y", "on"}
    return entered


def _select_default(config: dict[str, Any], groups: dict[str, list[dict[str, Any]]], category: str) -> bool:
    candidates = _ordered_candidates(groups.get(category, []))
    if not candidates:
        return False
    current = config["defaults"][category]["model"]
    default_index = next((index for index, item in enumerate(candidates, 1) if item["selected_id"] == current), 1)
    entered = input(f"\nDefault {category} model [number {default_index}, s to skip]: ").strip().lower()
    if entered == "s":
        return False
    try:
        selected_index = int(entered) if entered else default_index
    except ValueError as error:
        raise SkillError("SETUP_INPUT_INVALID", f"{category} model selection must be a number or s.") from error
    if not 1 <= selected_index <= len(candidates):
        raise SkillError("SETUP_INPUT_INVALID", f"{category} model selection is out of range.")
    selected = candidates[selected_index - 1]
    config["defaults"][category]["model"] = selected["selected_id"]
    definition = model_definition(selected["selected_id"]) or {}
    specs = definition.get("params", {})
    basic_specs = {name: spec for name, spec in specs.items() if spec.get("basic")}
    if not basic_specs:
        return True
    print(f"Configure common {category} defaults (press Enter to keep each value):")
    params: dict[str, Any] = {}
    existing = config["defaults"][category].get("params", {})
    for name, spec in basic_specs.items():
        current_value = existing.get(name, spec.get("default"))
        params[name] = _prompt_value(name, spec, current_value)
    config["defaults"][category]["params"] = validate_params(selected["selected_id"], params)
    return True


def _interactive_customize(config: dict[str, Any], groups: dict[str, list[dict[str, Any]]], catalog_hash: str) -> None:
    print("\nCreative models available to this token group:")
    for category, raw_items in groups.items():
        items = _ordered_candidates(raw_items)
        if not items:
            continue
        print(f"\n[{category}]")
        for index, model in enumerate(items, 1):
            recommendation = " RECOMMENDED" if model.get("recommended") == 1 else ""
            print(
                f"  {index}. {model.get('label', model['id'])} ({model['selected_id']}) "
                f"[{model['availability']}]{recommendation}"
            )

    for category in ("image", "video", "3d", "tts", "music"):
        if _select_default(config, groups, category):
            complete_onboarding_category(config, category, catalog_hash)

    output = input(f"\nOutput directory [{config['output']['directory']}]: ").strip()
    if output:
        config["output"]["directory"] = output


def command_setup(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    base_url = (args.base_url or config["api"].get("base_url") or DEFAULT_BASE_URL).rstrip("/")
    existing_key, existing_source = resolve_api_key(required=False)

    if args.key_stdin:
        api_key = sys.stdin.readline().strip()
        if not api_key:
            raise SkillError("KEY_MISSING", "No API key was received on stdin.")
        key_is_new = True
    elif existing_key and not args.replace_key:
        api_key = existing_key
        key_is_new = False
    else:
        api_key = getpass.getpass("ShowMeAI API key (input hidden): ").strip()
        key_is_new = True
    if len(api_key) < 8:
        raise SkillError("KEY_INVALID", "API key is too short.")

    client = ApiClient(base_url, api_key)
    live_payload = client.models()
    live_ids = normalize_live_models(live_payload)
    if not live_ids:
        raise SkillError("MODEL_LIST_EMPTY", "The API key returned no available models. Check its token group.")

    groups = grouped_models(live_ids)
    config["api"]["base_url"] = base_url
    live_hash = available_hash(live_ids)
    config["catalog"]["available_models_hash"] = live_hash
    current_image_model = config["defaults"]["image"].get("model", "")
    if current_image_model not in live_ids:
        config["defaults"]["image"]["model"] = recommended_image_model(live_ids)
    for category in ONBOARDING_CATEGORIES:
        selected = config["defaults"][category].get("model", "")
        if _candidate_for_model(groups.get(category, []), selected) is None:
            reset_onboarding_category(config, category)
    if sys.stdin.isatty() and not args.key_stdin and not args.non_interactive:
        print(f"\nWARNING: {GROUP_NOTICE}")
        _interactive_customize(config, groups, live_hash)

    if key_is_new:
        save_api_key(api_key)
    path = save_config(config)
    return {
        "ok": True,
        "data": {
            "configured": True,
            "config_file": str(path),
            "credential_source": "credentials_file" if key_is_new else existing_source,
            "credential_fingerprint": f"***{api_key[-4:]}",
            "default_image_model": config["defaults"]["image"]["model"],
            "onboarding_status": onboarding_status(config),
            "completed_categories": config["onboarding"]["completed_categories"],
            "models": _public_groups(groups),
            "group_notice": GROUP_NOTICE,
            "next_action": (
                "Use `onboarding apply` to confirm a category model and its supported defaults before generation."
                if onboarding_status(config) != "complete"
                else "Run `doctor` and start generating."
            ),
        },
    }


def command_doctor(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    api_key, source = resolve_api_key()
    live_ids = normalize_live_models(_client(config, api_key).models())
    selected = config["defaults"]["image"]["model"]
    selected_definition = model_definition(selected)
    selected_available = any(
        live_id == selected
        or (
            selected_definition is not None
            and model_definition(live_id) is not None
            and model_definition(live_id)["id"] == selected_definition["id"]
        )
        for live_id in live_ids
    )
    category = getattr(args, "category", "")
    if category and onboarding_status(config, category) != "complete":
        raise _onboarding_error(category)
    return {
        "ok": True,
        "data": {
            "version": VERSION,
            "config_file": str(config_file()),
            "credentials_file": str(credentials_file()),
            "credential_source": source,
            "credential_fingerprint": f"***{api_key[-4:]}",
            "available_model_count": len(live_ids),
            "default_image_model": selected,
            "default_image_model_available": selected_available,
            "onboarding_status": onboarding_status(config, category),
            "completed_categories": config["onboarding"]["completed_categories"],
            "group_notice": GROUP_NOTICE,
        },
    }


def command_onboarding(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    api_key, source = resolve_api_key(required=False)
    if args.onboarding_command == "status":
        status = "needs_key" if not api_key else onboarding_status(config, args.category)
        return {
            "ok": True,
            "data": {
                "status": status,
                "category": args.category or None,
                "completed_categories": config["onboarding"]["completed_categories"],
                "credential_source": source,
                "next_action": "run_setup" if status == "needs_key" else ("choose_defaults" if status != "complete" else "generate"),
            },
        }

    if not api_key:
        resolve_api_key()
    live_ids = normalize_live_models(_client(config, api_key).models())
    groups = grouped_models(live_ids)
    candidates = groups.get(args.category, [])
    if args.onboarding_command == "models":
        return {
            "ok": True,
            "data": {
                "category": args.category,
                "status": onboarding_status(config, args.category),
                "models": _public_groups({args.category: candidates})[args.category],
                "group_notice": GROUP_NOTICE,
                "next_action": "Ask the user to explicitly choose a model and supported defaults, then run `onboarding apply`.",
            },
        }

    candidate = _candidate_for_model(candidates, args.model)
    if candidate is None:
        raise SkillError(
            "MODEL_NOT_AVAILABLE_IN_GROUP",
            f"{args.model} is not available for {args.category} with the current API key group.",
            details={"category": args.category, "group_notice": GROUP_NOTICE},
        )
    try:
        params = json.loads(args.params_json)
    except json.JSONDecodeError as error:
        raise SkillError("SETUP_INPUT_INVALID", "--params-json must be a JSON object.") from error
    if not isinstance(params, dict):
        raise SkillError("SETUP_INPUT_INVALID", "--params-json must be a JSON object.")
    selected_id = candidate["selected_id"]
    if candidate.get("availability") == "verified_uncataloged" and params:
        raise SkillError(
            "MODEL_PARAMETERS_UNCATALOGED",
            f"{selected_id} is visible, but its parameter schema is not cataloged. Confirm it with empty defaults.",
            details={"model": selected_id, "supported_parameters": []},
        )
    validated = validate_params(selected_id, params, reject_unknown=True)
    config["defaults"][args.category] = {"model": selected_id, "params": validated}
    if args.category == "image":
        config["defaults"][args.category]["fallback_candidates"] = [
            item for item in ("gpt-image-2", "gemini-3-pro-image", "nano-banana-pro") if item != selected_id
        ]
        config["defaults"][args.category]["fallback_on"] = ["model_unavailable", "capacity_unavailable"]
    live_hash = available_hash(live_ids)
    config["catalog"]["available_models_hash"] = live_hash
    complete_onboarding_category(config, args.category, live_hash)
    path = save_config(config)
    return {
        "ok": True,
        "data": {
            "status": "complete",
            "category": args.category,
            "model": selected_id,
            "params": validated,
            "config_file": str(path),
            "completed_categories": config["onboarding"]["completed_categories"],
            "next_action": "Use the saved default without asking for the model again unless the user requests an override.",
        },
    }


def command_models(_args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    live_ids = normalize_live_models(_client(config).models())
    return {
        "ok": True,
        "data": {
            "models": _public_groups(grouped_models(live_ids)),
            "live_model_count": len(live_ids),
            "catalog_version": load_catalog()["catalog_version"],
            "group_notice": GROUP_NOTICE,
        },
    }


def command_config_show(_args: argparse.Namespace) -> dict[str, Any]:
    return {"ok": True, "data": public_config(load_config())}


def command_config_set(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    value = _parse_value(args.value)
    cataloged = not (args.path.endswith(".model") and isinstance(value, str)) or model_definition(value) is not None
    set_path(config, args.path, value)
    parts = args.path.split(".")
    if len(parts) >= 3 and parts[0] == "defaults" and parts[1] in ONBOARDING_CATEGORIES:
        reset_onboarding_category(config, parts[1])
    path = save_config(config)
    data: dict[str, Any] = {"config_file": str(path), "path": args.path, "value": value}
    if not cataloged:
        data["warning"] = "This live model is not in the local parameter catalog; its model-specific defaults cannot be validated yet."
    return {"ok": True, "data": data}


def command_paths(_args: argparse.Namespace) -> dict[str, Any]:
    return {
        "ok": True,
        "data": {
            "config_directory": str(config_dir()),
            "config_file": str(config_file()),
            "credentials_file": str(credentials_file()),
            "state_directory": str(state_dir()),
            "policy": "ShowMeAI-owned OS-native paths only; never write to an Agent host configuration directory.",
        },
    }


def _image_params(config: dict[str, Any], args: argparse.Namespace, model: str) -> dict[str, Any]:
    params = dict(config["defaults"]["image"].get("params", {})) if model == config["defaults"]["image"]["model"] else {}
    mapping = {
        "n": args.count,
        "size": args.size,
        "image_size": args.image_size,
        "aspect_ratio": args.aspect_ratio,
        "quality": args.quality,
        "output_format": args.output_format,
        "background": args.background,
        "output_compression": args.output_compression,
    }
    params.update({key: value for key, value in mapping.items() if value is not None and value != ""})
    return validate_params(model, params)


def _image_request(client: ApiClient, model: str, prompt: str, params: dict[str, Any], inputs: list[str], mask: str) -> dict[str, Any]:
    definition = model_definition(model) or {}
    canonical = definition.get("id", model)
    fields: dict[str, Any] = {"model": model, "prompt": prompt}
    if canonical.startswith("gpt-image"):
        fields.update(params)
    else:
        if params.get("image_size"):
            fields["size"] = params["image_size"]
        elif params.get("size"):
            fields["size"] = params["size"]
        if params.get("aspect_ratio"):
            fields["aspect_ratio"] = params["aspect_ratio"]
        fields["response_format"] = "b64_json"
    if inputs:
        files: list[tuple[str, Path]] = []
        for item in inputs:
            path = Path(item).expanduser()
            if not path.is_file():
                raise SkillError("INPUT_NOT_FOUND", f"Input image not found: {item}")
            files.append(("image", path))
        if mask:
            mask_path = Path(mask).expanduser()
            if not mask_path.is_file():
                raise SkillError("INPUT_NOT_FOUND", f"Mask image not found: {mask}")
            files.append(("mask", mask_path))
        return client.request_multipart(client.api_url("images/edits"), fields, files)
    return client.request_json("POST", client.api_url("images/generations"), fields)


def _model_unavailable(error: HttpError) -> bool:
    body = error.body.lower()
    return error.status in {404, 409, 503} or any(token in body for token in ("model not found", "no available", "无可用", "模型不可用"))


def _image_items(response: dict[str, Any]) -> list[dict[str, Any]]:
    data = response.get("data", [])
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict) and (item.get("b64_json") or item.get("url"))]


def _add_usage(total: dict[str, Any], current: dict[str, Any]) -> None:
    """Recursively sum numeric usage fields across image requests."""
    for key, value in current.items():
        if isinstance(value, dict):
            nested = total.setdefault(key, {})
            if isinstance(nested, dict):
                _add_usage(nested, value)
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            existing = total.get(key, 0)
            total[key] = existing + value if isinstance(existing, (int, float)) else value
        elif key not in total:
            total[key] = value


def _complete_image_count(
    client: ApiClient,
    response: dict[str, Any],
    requested_count: int,
    model: str,
    prompt: str,
    params: dict[str, Any],
    inputs: list[str],
    mask: str,
    concurrency: int,
) -> tuple[list[dict[str, Any]], dict[str, Any], int]:
    """Fulfill a requested count when an upstream endpoint returns fewer images than requested."""
    items = _image_items(response)
    if not items:
        raise SkillError("IMAGE_RESULT_MISSING", "Image request completed without image data.")
    usage: dict[str, Any] = {}
    response_usage = response.get("usage", {})
    if isinstance(response_usage, dict):
        _add_usage(usage, response_usage)
    request_count = 1

    missing = requested_count - len(items)
    if missing > 0:
        single_params = dict(params)
        single_params["n"] = 1
        workers = min(missing, concurrency)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            responses = [
                pool.submit(_image_request, client, model, prompt, single_params, inputs, mask)
                for _ in range(missing)
            ]
            extra_responses = [future.result() for future in responses]

    else:
        extra_responses = []

    for extra_response in extra_responses:
        extra_items = _image_items(extra_response)
        if not extra_items:
            raise SkillError(
                "IMAGE_COUNT_INCOMPLETE",
                f"The API returned {len(items)} of {requested_count} requested images; a completion request returned no image data.",
            )
        items.extend(extra_items)
        extra_usage = extra_response.get("usage", {})
        if isinstance(extra_usage, dict):
            _add_usage(usage, extra_usage)
        request_count += 1

    return items[:requested_count], usage, request_count


def command_image(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    client = _client(config)
    _require_category_ready(config, "image")
    model = args.model or config["defaults"]["image"]["model"]
    params = _image_params(config, args, model)
    requested_count = args.count if args.count is not None else int(params.get("n", 1))
    if not 1 <= requested_count <= MAX_IMAGE_COUNT:
        raise SkillError("PARAM_INVALID", f"count must be between 1 and {MAX_IMAGE_COUNT}.")
    concurrency = args.concurrency
    if not 1 <= concurrency <= MAX_IMAGE_COUNT:
        raise SkillError("PARAM_INVALID", f"concurrency must be between 1 and {MAX_IMAGE_COUNT}.")
    used_model = model
    try:
        response = _image_request(client, model, args.prompt, params, args.input, args.mask)
    except HttpError as error:
        fallback_on = config["defaults"]["image"].get("fallback_on", [])
        if "model_unavailable" not in fallback_on or not _model_unavailable(error):
            raise
        response = None
        for candidate in config["defaults"]["image"].get("fallback_candidates", []):
            try:
                candidate_params = validate_params(candidate, params)
                response = _image_request(client, candidate, args.prompt, candidate_params, args.input, args.mask)
                used_model = candidate
                params = candidate_params
                break
            except HttpError as candidate_error:
                if not _model_unavailable(candidate_error):
                    raise
        if response is None:
            raise error

    data, usage, request_count = _complete_image_count(
        client,
        response,
        requested_count,
        used_model,
        args.prompt,
        params,
        args.input,
        args.mask,
        concurrency,
    )
    manager = OutputManager(config, "image", args.out_dir)
    extension = str(params.get("output_format", "png"))
    files: list[str] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        if item.get("b64_json"):
            files.append(str(manager.write_base64(item["b64_json"], args.prompt, extension, args.filename)))
        elif item.get("url"):
            files.append(str(manager.download(client, item["url"], args.prompt, args.filename)))
    if not files:
        raise SkillError("IMAGE_RESULT_MISSING", "Image response contained no URL or base64 data.")
    return {
        "ok": True,
        "data": {
            "kind": "image",
            "model": used_model,
            "files": files,
            "requested_count": requested_count,
            "request_count": request_count,
            "usage": usage,
        },
    }


def _image_content(path_or_url: str, role: str = "") -> dict[str, Any]:
    if path_or_url.startswith(("http://", "https://")):
        url = path_or_url
    else:
        path = Path(path_or_url).expanduser()
        if not path.is_file():
            raise SkillError("INPUT_NOT_FOUND", f"Input image not found: {path_or_url}")
        mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
        url = f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"
    item: dict[str, Any] = {"type": "image_url", "image_url": {"url": url}}
    if role:
        item["role"] = role
    return item


def _task_id(response: dict[str, Any]) -> str:
    for value in (response.get("task_id"), response.get("id"), response.get("data")):
        if isinstance(value, str) and value:
            return value
    if isinstance(response.get("data"), dict):
        for key in ("task_id", "id"):
            if response["data"].get(key):
                return str(response["data"][key])
    raise SkillError("TASK_ID_MISSING", "Task submission returned no task ID.")


def _wait_task(config: dict[str, Any], client: ApiClient, record: TaskRecord, out_dir: str, max_wait: float | None) -> dict[str, Any]:
    result = TaskRunner(client, config).wait(record, out_dir, max_wait)
    return {"ok": True, "data": {"kind": record.kind, "task_id": record.task_id, "files": result["files"], "status": "success"}}


def command_video(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    client = _client(config)
    model = args.model or config["defaults"]["video"]["model"]
    defaults = config["defaults"]["video"].get("params", {}) if model == config["defaults"]["video"]["model"] else {}
    if args.query:
        record = TaskRecord(args.query, "video", client.task_url(f"task/{args.query}"), "video", args.query)
        return _wait_task(config, client, record, args.out_dir, args.max_wait)
    _require_category_ready(config, "video")
    if not args.prompt:
        raise SkillError("PROMPT_REQUIRED", "Video generation requires --prompt.")
    if bool(args.first_frame) != bool(args.last_frame):
        raise SkillError("PARAM_INVALID", "First-frame video requires both --first-frame and --last-frame.")
    if args.image and args.first_frame:
        raise SkillError("PARAM_INVALID", "--image cannot be combined with first/last frames.")
    content: list[dict[str, Any]] = [{"type": "text", "text": args.prompt}]
    if args.image:
        content.append(_image_content(args.image))
    if args.first_frame:
        content.extend([_image_content(args.first_frame, "first_frame"), _image_content(args.last_frame, "last_frame")])
    candidate_params: dict[str, Any] = {
        "generate_audio": args.audio if args.audio is not None else defaults.get("generate_audio", False),
        "resolution": args.resolution if args.resolution is not None else defaults.get("resolution"),
        "ratio": args.ratio if args.ratio is not None else defaults.get("ratio"),
        "duration": args.duration if args.duration is not None else defaults.get("duration"),
        "draft": args.draft if args.draft is not None else defaults.get("draft"),
        "watermark": args.watermark if args.watermark is not None else defaults.get("watermark"),
        "camera_fixed": args.camera_fixed if args.camera_fixed is not None else defaults.get("camera_fixed"),
        "seed": args.seed if args.seed is not None else defaults.get("seed"),
    }
    params = validate_params(model, candidate_params)
    payload: dict[str, Any] = {
        "model": model,
        "content": content,
        "generate_audio": params.get("generate_audio", False),
    }
    for key in ("resolution", "ratio", "duration", "seed"):
        value = params.get(key)
        if value not in (None, "", 0):
            payload[key] = value
    if args.frames not in (None, 0):
        payload["frames"] = args.frames
    for key in ("draft", "watermark", "camera_fixed"):
        value = params.get(key)
        if value is not None:
            payload[key] = bool(value)
    response = client.request_json("POST", client.task_url("task/volces/seedance"), payload)
    status, _progress, urls, _error = normalize_response("video", response)
    if status == "success" and urls:
        manager = OutputManager(config, "video", args.out_dir)
        files = [str(manager.download(client, url, args.prompt, args.filename)) for url in urls]
        return {"ok": True, "data": {"kind": "video", "model": model, "files": files}}
    task_id = _task_id(response)
    record = TaskRecord(task_id, "video", client.task_url(f"task/{task_id}"), "video", args.prompt)
    return _wait_task(config, client, record, args.out_dir, args.max_wait)


def command_3d(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    client = _client(config)
    model = args.model or config["defaults"]["3d"]["model"]
    if args.query:
        record = TaskRecord(args.query, "3d", client.task_url(f"task/{args.query}"), "3d", args.query)
        return _wait_task(config, client, record, args.out_dir, args.max_wait)
    _require_category_ready(config, "3d")
    image_path = Path(args.image).expanduser()
    if not image_path.is_file():
        raise SkillError("INPUT_NOT_FOUND", f"Input image not found: {args.image}")
    defaults = config["defaults"]["3d"].get("params", {}) if model == config["defaults"]["3d"]["model"] else {}
    file_format = args.format or defaults.get("format", "glb")
    raw_params = {
        "texture": args.texture if args.texture is not None else defaults.get("texture", True),
        "num_inference_steps": args.steps if args.steps is not None else defaults.get("num_inference_steps", 5),
        "octree_resolution": args.resolution if args.resolution is not None else defaults.get("octree_resolution", 128),
        "guidance_scale": args.guidance if args.guidance is not None else defaults.get("guidance_scale", 5),
        "format": file_format,
        "seed": args.seed if args.seed is not None else defaults.get("seed", 1234),
    }
    params = validate_params(model, raw_params)
    fields = {
        "model": model,
        "texture": params.get("texture"),
        "num_inference_steps": params.get("num_inference_steps"),
        "octree_resolution": params.get("octree_resolution"),
        "guidance_scale": params.get("guidance_scale"),
        "seed": params.get("seed"),
        "type" if model == "Hunyuan3D-2" else "file_format": params.get("format", file_format),
    }
    response = client.request_multipart(client.task_url("task/gi/image-to-3d"), fields, [("image", image_path)])
    task_id = _task_id(response)
    record = TaskRecord(task_id, "3d", client.task_url(f"task/{task_id}"), "3d", image_path.stem)
    return _wait_task(config, client, record, args.out_dir, args.max_wait)


def command_tts(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    client = _client(config)
    _require_category_ready(config, "tts")
    model = args.model or config["defaults"]["tts"]["model"]
    defaults = config["defaults"]["tts"].get("params", {}) if model == config["defaults"]["tts"]["model"] else {}
    response_format = args.response_format or defaults.get("response_format", "mp3")
    payload: dict[str, Any] = {
        "model": model,
        "input": args.text,
        "voice": args.voice or defaults.get("voice", "alloy"),
        "response_format": response_format,
    }
    if args.speed is not None:
        payload["speed"] = args.speed
    if args.temperature is not None:
        payload["temperature"] = args.temperature
    raw, headers = client.request("POST", client.api_url("audio/speech"), body=json.dumps(payload).encode("utf-8"), timeout=300)
    manager = OutputManager(config, "audio", args.out_dir)
    content_type = headers.get("Content-Type", "")
    if "json" in content_type or raw.lstrip().startswith(b"{"):
        response = json.loads(raw.decode("utf-8"))
        url = response.get("url") or response.get("output", {}).get("audio", {}).get("url")
        if not url:
            raise SkillError("AUDIO_RESULT_MISSING", "TTS response contained no audio URL.")
        path = manager.download(client, url, args.text, args.filename)
    else:
        path = manager.write_bytes(raw, args.text, response_format, args.filename)
    return {"ok": True, "data": {"kind": "tts", "model": model, "files": [str(path)]}}


def command_music(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    client = _client(config)
    _require_category_ready(config, "music")
    model = args.model or config["defaults"]["music"]["model"]
    defaults = config["defaults"]["music"].get("params", {}) if model == config["defaults"]["music"]["model"] else {}
    mode = args.mode or defaults.get("mode", "inspiration")
    payload: dict[str, Any] = {"mv": model}
    if mode == "inspiration":
        if not args.description:
            raise SkillError("PROMPT_REQUIRED", "Inspiration mode requires --description.")
        instrumental = args.instrumental if args.instrumental is not None else defaults.get("make_instrumental", False)
        payload.update({"gpt_description_prompt": args.description, "make_instrumental": instrumental})
    elif mode == "custom":
        if not all((args.lyrics, args.title, args.tags)):
            raise SkillError("PARAM_INVALID", "Custom mode requires --lyrics, --title, and --tags.")
        payload.update({"prompt": args.lyrics, "title": args.title, "tags": args.tags})
    else:
        if not all((args.lyrics, args.title, args.tags, args.continue_task, args.continue_clip)):
            raise SkillError("PARAM_INVALID", "Continue mode requires custom fields plus task and clip IDs.")
        payload.update({"prompt": args.lyrics, "title": args.title, "tags": args.tags, "task_id": args.continue_task, "continue_clip_id": args.continue_clip, "continue_at": args.continue_at})
    response = client.request_json("POST", client.task_url("suno/submit/music"), payload)
    task_id = _task_id(response)
    record = TaskRecord(task_id, "music", client.task_url(f"suno/fetch/{task_id}"), "music", args.title or args.description or task_id)
    return _wait_task(config, client, record, args.out_dir, args.max_wait)


def command_pic(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    client = _client(config)
    image_path = Path(args.image).expanduser()
    if not image_path.is_file():
        raise SkillError("INPUT_NOT_FOUND", f"Input image not found: {args.image}")
    fields: dict[str, Any] = {"sync": 0}
    endpoint = ""
    if args.operation == "upscale":
        endpoint = "task/pic/scale"
        fields.update({"type": "clean" if args.type == "auto" else args.type, "scale_factor": args.scale_factor})
    elif args.operation == "remove-bg":
        endpoint = "task/pic/segmentation"
        fields.update({"type": "" if args.type == "auto" else args.type, "output_type": args.output_type, "crop": int(args.crop), "format": args.format})
    response = client.request_multipart(client.task_url(endpoint), fields, [("image_file", image_path)])
    status, _progress, urls, _error = normalize_response("pic", response)
    if status == "success" and urls:
        manager = OutputManager(config, "image-tool", args.out_dir)
        files = [str(manager.download(client, url, image_path.stem)) for url in urls]
        return {"ok": True, "data": {"kind": "pic", "operation": args.operation, "files": files}}
    task_id = _task_id(response)
    record = TaskRecord(task_id, "pic", client.task_url(f"task/{task_id}"), "image-tool", image_path.stem)
    return _wait_task(config, client, record, args.out_dir, args.max_wait)


def command_tasks(args: argparse.Namespace) -> dict[str, Any]:
    config = load_config()
    journal = TaskJournal()
    records = journal.pending()
    if args.tasks_command == "list":
        return {"ok": True, "data": {"pending": [record.__dict__ for record in records]}}
    client = _client(config)
    runner = TaskRunner(client, config, journal=journal)
    completed: list[dict[str, Any]] = []
    for record in records:
        result = runner.wait(record, args.out_dir, args.max_wait)
        completed.append({"task_id": record.task_id, "files": result["files"]})
    return {"ok": True, "data": {"resumed": len(records), "completed": completed, "files": [path for item in completed for path in item["files"]]}}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Universal ShowMeAI generation and configuration CLI.")
    parser.add_argument("--json", action="store_true", help="Emit compact machine-readable JSON.")
    parser.add_argument("--version", action="version", version=VERSION)
    commands = parser.add_subparsers(dest="command", required=True)

    setup = commands.add_parser("setup", help="Configure key, model defaults, and output settings.")
    setup.add_argument("--key-stdin", action="store_true", help="Read the key from stdin for trusted Agent-assisted setup.")
    setup.add_argument("--base-url", default="")
    setup.add_argument("--replace-key", action="store_true")
    setup.add_argument("--non-interactive", action="store_true")
    setup.set_defaults(func=command_setup)

    doctor = commands.add_parser("doctor", help="Validate configuration, authentication, and model availability.")
    doctor.add_argument("--category", choices=ONBOARDING_CATEGORIES, default="")
    doctor.set_defaults(func=command_doctor)
    models = commands.add_parser("models", help="List creative models visible to the current token group.")
    models.set_defaults(func=command_models)
    paths = commands.add_parser("paths", help="Show the exact ShowMeAI-owned configuration and state paths.")
    paths.set_defaults(func=command_paths)

    onboarding = commands.add_parser("onboarding", help="Inspect or complete first-use model defaults.")
    onboarding_commands = onboarding.add_subparsers(dest="onboarding_command", required=True)
    onboarding_status_parser = onboarding_commands.add_parser("status")
    onboarding_status_parser.add_argument("--category", choices=ONBOARDING_CATEGORIES, default="")
    onboarding_status_parser.set_defaults(func=command_onboarding)
    onboarding_models = onboarding_commands.add_parser("models")
    onboarding_models.add_argument("--category", choices=ONBOARDING_CATEGORIES, required=True)
    onboarding_models.set_defaults(func=command_onboarding)
    onboarding_apply = onboarding_commands.add_parser("apply")
    onboarding_apply.add_argument("--category", choices=ONBOARDING_CATEGORIES, required=True)
    onboarding_apply.add_argument("--model", required=True)
    onboarding_apply.add_argument("--params-json", default="{}")
    onboarding_apply.set_defaults(func=command_onboarding)

    config = commands.add_parser("config", help="Show or edit non-secret preferences.")
    config_commands = config.add_subparsers(dest="config_command", required=True)
    config_show = config_commands.add_parser("show")
    config_show.set_defaults(func=command_config_show)
    config_set = config_commands.add_parser("set")
    config_set.add_argument("path")
    config_set.add_argument("value")
    config_set.set_defaults(func=command_config_set)

    image = commands.add_parser("image", help="Generate or edit images.")
    image.add_argument("--prompt", required=True)
    image.add_argument("--model", default="")
    image.add_argument("--input", action="append", default=[], help="Input image; repeat for multi-image editing.")
    image.add_argument("--mask", default="")
    image.add_argument("--count", type=int)
    image.add_argument(
        "--concurrency",
        type=int,
        default=DEFAULT_IMAGE_CONCURRENCY,
        help="Maximum parallel completion requests when the API returns fewer images than requested (default: 4).",
    )
    image.add_argument("--size", default="")
    image.add_argument("--image-size", default="")
    image.add_argument("--aspect-ratio", default="")
    image.add_argument("--quality", default="")
    image.add_argument("--output-format", choices=["png", "jpeg", "webp"])
    image.add_argument("--background", choices=["auto", "transparent", "opaque"])
    image.add_argument("--output-compression", type=int)
    image.add_argument("--out-dir", default="")
    image.add_argument("--filename", default="")
    image.set_defaults(func=command_image)

    video = commands.add_parser("video", help="Generate video and wait until the final file is available.")
    video.add_argument("--prompt", default="")
    video.add_argument("--query", default="")
    video.add_argument("--model", default="")
    video.add_argument("--image", default="")
    video.add_argument("--first-frame", default="")
    video.add_argument("--last-frame", default="")
    video.add_argument("--audio", action=argparse.BooleanOptionalAction, default=None)
    video.add_argument("--draft", action=argparse.BooleanOptionalAction, default=None)
    video.add_argument("--resolution", choices=["480p", "720p", "1080p"])
    video.add_argument("--ratio", choices=["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"])
    video.add_argument("--duration", type=int)
    video.add_argument("--frames", type=int)
    video.add_argument("--watermark", action=argparse.BooleanOptionalAction, default=None)
    video.add_argument("--camera-fixed", action=argparse.BooleanOptionalAction, default=None)
    video.add_argument("--seed", type=int)
    video.add_argument("--max-wait", type=float)
    video.add_argument("--out-dir", default="")
    video.add_argument("--filename", default="")
    video.set_defaults(func=command_video)

    three_d = commands.add_parser("3d", help="Convert an image to 3D and wait for the final model.")
    source = three_d.add_mutually_exclusive_group(required=True)
    source.add_argument("--image")
    source.add_argument("--query")
    three_d.add_argument("--model", default="")
    three_d.add_argument("--format", choices=["glb", "stl"])
    three_d.add_argument("--texture", action=argparse.BooleanOptionalAction, default=None)
    three_d.add_argument("--steps", type=int)
    three_d.add_argument("--resolution", type=int)
    three_d.add_argument("--guidance", type=float)
    three_d.add_argument("--seed", type=int)
    three_d.add_argument("--max-wait", type=float)
    three_d.add_argument("--out-dir", default="")
    three_d.set_defaults(func=command_3d)

    tts = commands.add_parser("tts", help="Generate speech audio.")
    tts.add_argument("--text", required=True)
    tts.add_argument("--model", default="")
    tts.add_argument("--voice", default="")
    tts.add_argument("--response-format", choices=["mp3", "opus", "aac", "flac", "wav", "pcm"])
    tts.add_argument("--speed", type=float)
    tts.add_argument("--temperature", type=float)
    tts.add_argument("--out-dir", default="")
    tts.add_argument("--filename", default="")
    tts.set_defaults(func=command_tts)

    music = commands.add_parser("music", help="Generate Suno music and wait until audio is available.")
    music.add_argument("--mode", choices=["inspiration", "custom", "continue"])
    music.add_argument("--model", default="")
    music.add_argument("--description", default="")
    music.add_argument("--instrumental", action=argparse.BooleanOptionalAction, default=None)
    music.add_argument("--lyrics", default="")
    music.add_argument("--title", default="")
    music.add_argument("--tags", default="")
    music.add_argument("--continue-task", default="")
    music.add_argument("--continue-clip", default="")
    music.add_argument("--continue-at", type=float, default=0)
    music.add_argument("--max-wait", type=float)
    music.add_argument("--out-dir", default="")
    music.set_defaults(func=command_music)

    pic = commands.add_parser("pic", help="Run image processing and wait until the final file is available.")
    pic.add_argument("operation", choices=["upscale", "remove-bg"])
    pic.add_argument("--image", required=True)
    pic.add_argument("--type", default="auto")
    pic.add_argument("--scale-factor", type=int, choices=[1, 2, 4], default=2)
    pic.add_argument("--output-type", type=int, choices=[1, 2, 3], default=2)
    pic.add_argument("--crop", action="store_true")
    pic.add_argument("--format", choices=["png", "jpg"], default="png")
    pic.add_argument("--max-wait", type=float)
    pic.add_argument("--out-dir", default="")
    pic.set_defaults(func=command_pic)

    tasks = commands.add_parser("tasks", help="Inspect or resume persisted tasks.")
    task_commands = tasks.add_subparsers(dest="tasks_command", required=True)
    task_list = task_commands.add_parser("list")
    task_list.set_defaults(func=command_tasks)
    task_resume = task_commands.add_parser("resume")
    task_resume.add_argument("--max-wait", type=float)
    task_resume.add_argument("--out-dir", default="")
    task_resume.set_defaults(func=command_tasks)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    values = list(sys.argv[1:] if argv is None else argv)
    compact = "--json" in values
    values = [value for value in values if value != "--json"]
    args = parser.parse_args(values)
    args.json = compact
    try:
        result = args.func(args)
        _emit(result, compact=args.json)
        return 0
    except Exception as error:
        result = error_result(error)
        _emit(result, compact=args.json)
        return error.exit_code if isinstance(error, SkillError) else 1


if __name__ == "__main__":
    raise SystemExit(main())
