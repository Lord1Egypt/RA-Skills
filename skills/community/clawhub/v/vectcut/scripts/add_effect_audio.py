#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import random
import re
import sys

import requests

BASE_URL = "https://open.vectcut.com"
GET_DURATION_PATH = "/cut_jianying/get_duration"
ADD_AUDIO_PATH = "/cut_jianying/add_audio"
DEFAULT_TRACK_NAME = "audio_effect"
DEFAULT_VOLUME_DB = 0.0
DEFAULT_TARGET_START = 0.0
DEFAULT_LIST_PATH = (
    Path(__file__).resolve().parents[1] / "references" / "effect_audios.json"
)
URL_PATTERN = re.compile(r"https?://[^\s'\"<>]+")


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


def _read_effect_audios(list_path):
    path = Path(list_path)
    if not path.exists():
        raise RuntimeError(f"effect audio list file not found: {path}")

    text = path.read_text(encoding="utf-8")
    urls = []
    if path.suffix.lower() == ".json":
        try:
            body = json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"invalid effect audio json: {e}")
        arr = body.get("effect_audios")
        if not isinstance(arr, list):
            raise RuntimeError("json must contain key 'effect_audios' with array value.")
        for item in arr:
            if isinstance(item, str) and item.strip():
                urls.append(item.strip())
    else:
        urls = URL_PATTERN.findall(text)
        urls = [u.strip().rstrip(",") for u in urls if u.strip()]

    deduped = []
    seen = set()
    for u in urls:
        if u not in seen:
            seen.add(u)
            deduped.append(u)
    if not deduped:
        raise RuntimeError("no usable effect audio url found in list file")
    return deduped


def _pick_effect_audio(payload, urls):
    if payload.get("effect_audio_url"):
        return payload["effect_audio_url"]

    idx = payload.get("effect_audio_index")
    if idx is None:
        if payload.get("random_effect_audio", False):
            return random.choice(urls)
        return urls[0]

    if not isinstance(idx, int):
        raise RuntimeError("effect_audio_index must be an integer.")
    if idx < 0 or idx >= len(urls):
        raise RuntimeError(
            f"effect_audio_index out of range: {idx}, valid [0, {len(urls)-1}]"
        )
    return urls[idx]


def _get_media_duration_seconds(token, url):
    resp = requests.post(
        f"{BASE_URL}{GET_DURATION_PATH}",
        headers=_auth_headers(token),
        json={"url": url},
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))
    duration = (body.get("output") or {}).get("duration")
    if not isinstance(duration, (int, float)) or duration <= 0:
        raise RuntimeError(f"invalid duration from get_duration: {duration!r}")
    return float(duration)


def _add_audio_once(token, payload):
    resp = requests.post(
        f"{BASE_URL}{ADD_AUDIO_PATH}",
        headers=_auth_headers(token),
        json=payload,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))
    return body


def _validate_payload(payload):
    if not isinstance(payload, dict):
        raise RuntimeError("payload must be a JSON object.")
    draft_id = payload.get("draft_id")
    if not isinstance(draft_id, str) or not draft_id.strip():
        raise RuntimeError("draft_id is required.")

    for key in ("target_start", "volume", "clip_duration", "speed"):
        if key in payload and not isinstance(payload[key], (int, float)):
            raise RuntimeError(f"{key} must be a number.")
    if "random_effect_audio" in payload and not isinstance(
        payload["random_effect_audio"], bool
    ):
        raise RuntimeError("random_effect_audio must be boolean.")


def run(payload):
    _validate_payload(payload)
    token = _ensure_token()

    list_path = payload.get("effect_audio_list_path") or str(DEFAULT_LIST_PATH)
    urls = _read_effect_audios(list_path)
    selected_url = _pick_effect_audio(payload, urls)

    source_duration = _get_media_duration_seconds(token, selected_url)
    clip_duration = float(payload.get("clip_duration", source_duration))
    if clip_duration <= 0:
        raise RuntimeError("clip_duration must be > 0.")
    clip_duration = min(clip_duration, source_duration)

    req = {
        "audio_url": selected_url,
        "draft_id": payload["draft_id"],
        "track_name": payload.get("track_name", DEFAULT_TRACK_NAME),
        "target_start": float(payload.get("target_start", DEFAULT_TARGET_START)),
        "start": 0.0,
        "end": round(clip_duration, 6),
        "duration": round(source_duration, 6),
        "volume": float(payload.get("volume", DEFAULT_VOLUME_DB)),
    }
    if "speed" in payload:
        req["speed"] = float(payload["speed"])

    resp_body = _add_audio_once(token, req)
    output = resp_body.get("output") or {}
    return {
        "success": True,
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "draft_id": payload["draft_id"],
            "effect_audio_list_path": str(list_path),
            "available_effect_audio_count": len(urls),
            "selected_effect_audio_url": selected_url,
            "source_duration_seconds": source_duration,
            "clip_duration_seconds": clip_duration,
            "target_start_seconds": req["target_start"],
        },
        "request_payload": req,
        "result": {
            "draft_id": output.get("draft_id", payload["draft_id"]),
            "draft_url": output.get("draft_url"),
            "material_id": output.get("material_id"),
            "raw_response": resp_body,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Add one short effect audio cue at a key timeline position."
    )
    parser.add_argument("payload_json", help="Path to add-effect_audio payload JSON.")
    parser.add_argument("--output", default="add_effect_audio_result.json")
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
