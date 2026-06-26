#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
import sys

import requests

BASE_URL = "https://open.vectcut.com"
ADD_EFFECT_PATH = "/cut_jianying/add_effect"
SCENE_TYPES_PATH = "/cut_jianying/get_video_scene_effect_types"
CHARACTER_TYPES_PATH = "/cut_jianying/get_video_character_effect_types"

DEFAULTS = {
    "start": 0.0,
    "end": 3.0,
    "track_name": "effect_01",
    "width": 1080,
    "height": 1920,
    "effect_category": "auto",
}


def _auth_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _ensure_token():
    token = os.environ.get("VECTCUT_API_KEY")
    if not token:
        raise RuntimeError(
            "Environment variable VECTCUT_API_KEY is not set. "
            "Please call the vectcut-login skill first."
        )
    return token


def _parse_json_response(resp):
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"Invalid JSON response: {resp.text}")


def _extract_names(body):
    output = body.get("output")
    names = []
    if isinstance(output, list):
        for item in output:
            if isinstance(item, dict):
                name = item.get("name")
                if isinstance(name, str) and name.strip():
                    names.append(name.strip())
    return names


def get_scene_effect_types(token):
    resp = requests.get(
        f"{BASE_URL}{SCENE_TYPES_PATH}",
        headers=_auth_headers(token),
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    return _extract_names(body)


def get_character_effect_types(token):
    resp = requests.get(
        f"{BASE_URL}{CHARACTER_TYPES_PATH}",
        headers=_auth_headers(token),
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    return _extract_names(body)


def _with_defaults(payload):
    merged = dict(DEFAULTS)
    merged.update(payload)
    return merged


def _validate_payload(payload):
    if not isinstance(payload, dict):
        raise RuntimeError("Payload must be a JSON object.")

    effect_type = payload.get("effect_type")
    if not isinstance(effect_type, str) or not effect_type.strip():
        raise RuntimeError("effect_type is required and must be a non-empty string.")

    start = payload.get("start")
    end = payload.get("end")
    if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
        raise RuntimeError("start/end must be numbers.")
    if start < 0 or end < 0:
        raise RuntimeError("start/end cannot be negative.")
    if end <= start:
        raise RuntimeError("end must be greater than start.")

    track_name = payload.get("track_name")
    if not isinstance(track_name, str) or not track_name.strip():
        raise RuntimeError("track_name must be a non-empty string.")

    for key in ("width", "height"):
        value = payload.get(key)
        if not isinstance(value, int) or value <= 0:
            raise RuntimeError(f"{key} must be a positive integer.")

    params = payload.get("params")
    if params is not None:
        if not isinstance(params, list):
            raise RuntimeError("params must be a list of numbers.")
        for idx, value in enumerate(params):
            if not isinstance(value, (int, float)):
                raise RuntimeError(f"params[{idx}] must be a number.")

    category = payload.get("effect_category", "auto")
    if category not in {"scene", "character", "auto"}:
        raise RuntimeError("effect_category must be one of: scene, character, auto.")

    draft_id = payload.get("draft_id")
    if draft_id is not None and (
        not isinstance(draft_id, str) or not draft_id.strip()
    ):
        raise RuntimeError("draft_id must be a non-empty string when provided.")


def _resolve_and_check_effect_type(token, effect_type, effect_category):
    scene_types = get_scene_effect_types(token)
    character_types = get_character_effect_types(token)
    scene_set = set(scene_types)
    character_set = set(character_types)

    if effect_category == "scene":
        if effect_type not in scene_set:
            raise RuntimeError(
                f"effect_type '{effect_type}' not found in scene effect types."
            )
        return "scene", scene_types, character_types

    if effect_category == "character":
        if effect_type not in character_set:
            raise RuntimeError(
                f"effect_type '{effect_type}' not found in character effect types."
            )
        return "character", scene_types, character_types

    if effect_type in scene_set and effect_type in character_set:
        return "scene", scene_types, character_types
    if effect_type in scene_set:
        return "scene", scene_types, character_types
    if effect_type in character_set:
        return "character", scene_types, character_types

    raise RuntimeError(
        f"effect_type '{effect_type}' not found in official scene/character effect types."
    )


def _build_add_effect_payload(payload):
    req = {
        "effect_type": payload["effect_type"],
        "start": payload["start"],
        "end": payload["end"],
        "track_name": payload["track_name"],
        "width": payload["width"],
        "height": payload["height"],
    }
    if payload.get("draft_id"):
        req["draft_id"] = payload["draft_id"]
    if payload.get("params") is not None:
        req["params"] = payload["params"]
    return req


def add_effect(token, payload):
    resp = requests.post(
        f"{BASE_URL}{ADD_EFFECT_PATH}",
        headers=_auth_headers(token),
        json=payload,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    if body.get("success") is False:
        raise RuntimeError(body.get("error") or str(body))
    return body


def run(payload, validate_effect_type=True):
    token = _ensure_token()
    normalized = _with_defaults(payload)
    _validate_payload(normalized)

    resolved_category = "unknown"
    scene_types = []
    character_types = []
    if validate_effect_type:
        resolved_category, scene_types, character_types = _resolve_and_check_effect_type(
            token=token,
            effect_type=normalized["effect_type"],
            effect_category=normalized.get("effect_category", "auto"),
        )

    request_payload = _build_add_effect_payload(normalized)
    response_body = add_effect(token, request_payload)
    return {
        "success": True,
        "meta": {
            "endpoint": ADD_EFFECT_PATH,
            "effect_type": normalized["effect_type"],
            "resolved_category": resolved_category,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "request_payload": request_payload,
        "result": {
            "draft_id": response_body.get("output", {}).get("draft_id")
            if isinstance(response_body.get("output"), dict)
            else None,
            "draft_url": response_body.get("output", {}).get("draft_url")
            if isinstance(response_body.get("output"), dict)
            else None,
            "raw_response": response_body,
        },
        "effect_catalog_summary": {
            "scene_count": len(scene_types),
            "character_count": len(character_types),
        },
    }


def run_list(token, list_scene=False, list_character=False):
    scene_types = get_scene_effect_types(token) if list_scene else []
    character_types = get_character_effect_types(token) if list_character else []
    return {
        "success": True,
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "scene_types_path": SCENE_TYPES_PATH,
            "character_types_path": CHARACTER_TYPES_PATH,
        },
        "scene_effect_types": scene_types,
        "character_effect_types": character_types,
    }


def main():
    parser = argparse.ArgumentParser(description="Add video effect via add_effect.")
    parser.add_argument("payload_json", nargs="?")
    parser.add_argument("--output", default="add_effect_result.json")
    parser.add_argument("--no-validate-effect-type", action="store_true")
    parser.add_argument("--list-scene", action="store_true")
    parser.add_argument("--list-character", action="store_true")
    parser.add_argument("--list-all", action="store_true")
    args = parser.parse_args()

    try:
        token = _ensure_token()
        if args.list_all or args.list_scene or args.list_character:
            list_scene = args.list_all or args.list_scene
            list_character = args.list_all or args.list_character
            result = run_list(token, list_scene=list_scene, list_character=list_character)
        else:
            if not args.payload_json:
                raise RuntimeError(
                    "payload_json is required when not using --list-scene/--list-character/--list-all."
                )
            with open(args.payload_json, "r", encoding="utf-8") as f:
                payload = json.load(f)
            result = run(
                payload=payload,
                validate_effect_type=not args.no_validate_effect_type,
            )

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
