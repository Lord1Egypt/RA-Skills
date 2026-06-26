#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
import sys

import requests

BASE_URL = "https://open.vectcut.com"
ADD_PRESET_PATH = "/cut_jianying/add_preset"


def _auth_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _ensure_token() -> str:
    token = os.environ.get("VECTCUT_API_KEY")
    if not token:
        raise RuntimeError(
            "Environment variable VECTCUT_API_KEY is not set. "
            "Please call the vectcut-login skill first."
        )
    return token


def _parse_json_response(resp: requests.Response) -> dict:
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"Invalid JSON response: {resp.text}")


def _validate_payload(payload: object) -> None:
    if not isinstance(payload, dict):
        raise RuntimeError("Payload must be a JSON object.")

    preset_id = payload.get("preset_id")
    replacements = payload.get("replacements")

    draft_id = payload.get("draft_id")
    if draft_id is not None and (not isinstance(draft_id, str) or not draft_id.strip()):
        raise RuntimeError("draft_id must be a non-empty string when provided.")
    if not isinstance(preset_id, str) or not preset_id.strip():
        raise RuntimeError("preset_id is required and must be a non-empty string.")

    if replacements is not None:
        if not isinstance(replacements, list) or not replacements:
            raise RuntimeError("replacements must be a non-empty list when provided.")
        for idx, item in enumerate(replacements):
            if not isinstance(item, dict) or not item:
                raise RuntimeError(f"replacements[{idx}] must be a non-empty object.")


def add_preset(token: str, payload: dict) -> dict:
    resp = requests.post(
        f"{BASE_URL}{ADD_PRESET_PATH}",
        headers=_auth_headers(token),
        json=payload,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    return body


def run(payload: dict) -> dict:
    token = _ensure_token()
    _validate_payload(payload)
    response_body = add_preset(token, payload)
    return {
        "success": True,
        "meta": {
            "endpoint": ADD_PRESET_PATH,
            "draft_id": payload.get("draft_id"),
            "preset_id": payload.get("preset_id"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "request_payload": payload,
        "result": {
            "raw_response": response_body,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Add preset segment into draft via add_preset.")
    parser.add_argument("payload_json", help="Path to add_preset request payload JSON.")
    parser.add_argument("--output", default="add_preset_result.json")
    args = parser.parse_args()

    try:
        with open(args.payload_json, "r", encoding="utf-8") as f:
            payload = json.load(f)
        result = run(payload)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
