#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
import sys

import requests

BASE_URL = "https://open.vectcut.com"
ADD_TEXT_PATH = "/cut_jianying/add_text"

ALLOWED_FONTS = {"思源粗宋", "俪金黑", "研宋体", "细体"}
ALLOWED_COLORS = {"#ffffff", "#ffa800", "#b71c1c", "#18893e"}

DEFAULTS = {
    "track_name": "text_title",
    "start": 0.0,
    "font": "思源粗宋",
    "font_size": 18.0,
    "font_color": "#ffffff",
    "shadow_enabled": True,
    "transform_y_px": 1240,
    "fixed_width": 0.6,
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


def _normalize_color(value):
    if not isinstance(value, str):
        raise RuntimeError("font_color must be a string.")
    color = value.strip().lower()
    if not color.startswith("#"):
        color = f"#{color}"
    return color


def _with_defaults(payload):
    merged = dict(DEFAULTS)
    merged.update(payload)
    return merged


def _validate_payload(payload):
    if not isinstance(payload, dict):
        raise RuntimeError("Payload must be a JSON object.")

    required = ("draft_id", "text", "end")
    for key in required:
        value = payload.get(key)
        if isinstance(value, str):
            value = value.strip()
        if value in (None, ""):
            raise RuntimeError(f"{key} is required.")

    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("text must be a non-empty string.")

    start = payload.get("start")
    end = payload.get("end")
    if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
        raise RuntimeError("start/end must be numbers.")
    if end <= start:
        raise RuntimeError("end must be greater than start.")

    font = payload.get("font")
    if font not in ALLOWED_FONTS:
        raise RuntimeError(f"font must be one of: {sorted(ALLOWED_FONTS)}")

    font_color = _normalize_color(payload.get("font_color", ""))
    if font_color not in ALLOWED_COLORS:
        raise RuntimeError(f"font_color must be one of: {sorted(ALLOWED_COLORS)}")
    payload["font_color"] = font_color


def add_title(token, payload):
    resp = requests.post(
        f"{BASE_URL}{ADD_TEXT_PATH}",
        headers=_auth_headers(token),
        json=payload,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    return body


def run(payload):
    token = _ensure_token()
    normalized = _with_defaults(payload)
    _validate_payload(normalized)
    response_body = add_title(token, normalized)
    return {
        "success": True,
        "meta": {
            "endpoint": ADD_TEXT_PATH,
            "draft_id": normalized.get("draft_id"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "request_payload": normalized,
        "result": {
            "raw_response": response_body,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Add fixed-position video title via add_text.")
    parser.add_argument("payload_json", help="Path to request payload JSON.")
    parser.add_argument("--output", default="add_title_result.json")
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
