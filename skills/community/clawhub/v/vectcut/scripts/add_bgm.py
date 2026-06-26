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
QUERY_SCRIPT_PATH = "/cut_jianying/query_script"
GET_DURATION_PATH = "/cut_jianying/get_duration"
ADD_AUDIO_PATH = "/cut_jianying/add_audio"
DEFAULT_TRACK_NAME = "audio_bgm"

URL_PATTERN = re.compile(r"https?://[^\s'\"<>]+")
DEFAULT_BGM_LIST_PATH = Path(__file__).resolve().parents[1] / "references" / "bgms.json"


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


def _read_bgms(bgm_list_path):
    path = Path(bgm_list_path)
    if not path.exists():
        raise RuntimeError(f"BGM list file not found: {path}")
    text = path.read_text(encoding="utf-8")
    urls = []

    if path.suffix.lower() == ".json":
        try:
            body = json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid bgm json file: {e}")
        arr = body.get("bgms")
        if not isinstance(arr, list):
            raise RuntimeError("bgm json must contain key 'bgms' with array value.")
        for item in arr:
            if isinstance(item, str) and item.strip():
                urls.append(item.strip())
    else:
        # backward compatible: parse plain text / markdown that contains URLs
        urls = URL_PATTERN.findall(text)
        urls = [u.strip().rstrip(",") for u in urls if u.strip()]
    deduped = []
    seen = set()
    for u in urls:
        if u not in seen:
            seen.add(u)
            deduped.append(u)
    if not deduped:
        raise RuntimeError(f"No usable BGM URL found in: {path}")
    return deduped


def _query_draft_duration_seconds(token, draft_id):
    resp = requests.post(
        f"{BASE_URL}{QUERY_SCRIPT_PATH}",
        headers=_auth_headers(token),
        json={"draft_id": draft_id, "force_update": True},
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))

    output_raw = body.get("output")
    if isinstance(output_raw, str):
        try:
            draft = json.loads(output_raw)
        except json.JSONDecodeError:
            raise RuntimeError("query_script output is not valid JSON string.")
    elif isinstance(output_raw, dict):
        draft = output_raw
    else:
        raise RuntimeError(f"Unexpected query_script output: {type(output_raw).__name__}")

    duration_us = draft.get("duration")
    if not isinstance(duration_us, (int, float)) or duration_us <= 0:
        raise RuntimeError(f"Invalid draft duration: {duration_us!r}")
    return float(duration_us) / 1_000_000.0


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

    output = body.get("output") or {}
    duration = output.get("duration")
    if not isinstance(duration, (int, float)) or duration <= 0:
        raise RuntimeError(f"Invalid media duration from get_duration: {duration!r}")
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


def _pick_bgm(payload, bgms):
    if payload.get("bgm_url"):
        return payload["bgm_url"]

    idx = payload.get("bgm_index")
    if idx is None:
        if payload.get("random_bgm", False):
            return random.choice(bgms)
        return bgms[0]

    if not isinstance(idx, int):
        raise RuntimeError("bgm_index must be an integer.")
    if idx < 0 or idx >= len(bgms):
        raise RuntimeError(f"bgm_index out of range: {idx}, valid [0, {len(bgms)-1}]")
    return bgms[idx]


def _validate_payload(payload):
    if not isinstance(payload, dict):
        raise RuntimeError("Payload must be a JSON object.")
    draft_id = payload.get("draft_id")
    if not isinstance(draft_id, str) or not draft_id.strip():
        raise RuntimeError("draft_id is required.")

    for key in ("volume", "speed"):
        if key in payload and not isinstance(payload[key], (int, float)):
            raise RuntimeError(f"{key} must be a number.")

    if "random_bgm" in payload and not isinstance(payload["random_bgm"], bool):
        raise RuntimeError("random_bgm must be boolean.")


def run(payload):
    _validate_payload(payload)
    token = _ensure_token()

    bgm_list_path = payload.get("bgm_list_path") or str(DEFAULT_BGM_LIST_PATH)
    bgms = _read_bgms(bgm_list_path)
    bgm_url = _pick_bgm(payload, bgms)

    draft_id = payload["draft_id"]
    track_name = payload.get("track_name", DEFAULT_TRACK_NAME)
    volume = payload.get("volume")
    speed = payload.get("speed")
    fade_in_duration = payload.get("fade_in_duration")
    fade_out_duratioin = payload.get("fade_out_duratioin")

    draft_duration_sec = _query_draft_duration_seconds(token, draft_id)
    bgm_duration_sec = _get_media_duration_seconds(token, bgm_url)

    if bgm_duration_sec <= 0:
        raise RuntimeError("BGM duration must be greater than 0.")

    pos = 0.0
    idx = 0
    added = []
    last_response = None

    while pos < draft_duration_sec - 1e-6:
        remaining = draft_duration_sec - pos
        clip_len = min(bgm_duration_sec, remaining)
        req = {
            "audio_url": bgm_url,
            "draft_id": draft_id,
            "start": 0.0,
            "end": round(clip_len, 6),
            "target_start": round(pos, 6),
            "track_name": track_name,
            "duration": round(bgm_duration_sec, 6),
        }
        if volume is not None:
            req["volume"] = float(volume)
        if speed is not None:
            req["speed"] = float(speed)
        if isinstance(fade_in_duration, (int, float)):
            req["fade_in_duration"] = float(fade_in_duration)
        if isinstance(fade_out_duratioin, (int, float)):
            req["fade_out_duratioin"] = float(fade_out_duratioin)

        resp_body = _add_audio_once(token, req)
        output = resp_body.get("output") or {}
        last_response = output
        added.append(
            {
                "index": idx,
                "target_start": req["target_start"],
                "end": req["end"],
                "material_id": output.get("material_id"),
            }
        )
        pos += clip_len
        idx += 1

    return {
        "success": True,
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "draft_id": draft_id,
            "track_name": track_name,
            "bgm_list_path": str(bgm_list_path),
            "selected_bgm_url": bgm_url,
            "available_bgm_count": len(bgms),
            "draft_duration_seconds": draft_duration_sec,
            "bgm_duration_seconds": bgm_duration_sec,
            "segment_count": len(added),
        },
        "result": {
            "draft_id": (last_response or {}).get("draft_id", draft_id),
            "draft_url": (last_response or {}).get("draft_url"),
            "added_segments": added,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Query draft duration, tile BGM by add_audio until full timeline coverage."
    )
    parser.add_argument("payload_json", help="Path to add-bgm payload JSON.")
    parser.add_argument("--output", default="add_bgm_result.json")
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
