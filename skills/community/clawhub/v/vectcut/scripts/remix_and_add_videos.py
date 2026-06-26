#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
import random
import sys
from typing import Dict, List, Optional, Tuple

import requests

BASE_URL = "https://open.vectcut.com"
GET_DURATION_PATH = "/cut_jianying/get_duration"
ADD_VIDEO_PATH = "/cut_jianying/add_video"
DEFAULT_MIN_CLIP_SECONDS = 2.5
DEFAULT_MAX_CLIP_SECONDS = 7.0
DEFAULT_TRACK_NAME = "video_broll"
DEFAULT_TARGET_TOTAL_SECONDS = 45.0
MAX_SEGMENTS = 40


def _auth_headers(token: str) -> Dict[str, str]:
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


def _parse_json_response(resp: requests.Response) -> Dict:
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"Invalid JSON response: {resp.text}")


def _get_media_duration_seconds(token: str, url: str) -> float:
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
        raise RuntimeError(f"Invalid duration from get_duration: {duration!r}")
    return float(duration)


def _add_video_once(token: str, payload: Dict) -> Dict:
    resp = requests.post(
        f"{BASE_URL}{ADD_VIDEO_PATH}",
        headers=_auth_headers(token),
        json=payload,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))
    return body


def _validate_payload(payload: Dict) -> None:
    if not isinstance(payload, dict):
        raise RuntimeError("payload must be a JSON object.")

    video_urls = payload.get("video_urls")
    if not isinstance(video_urls, list) or not video_urls:
        raise RuntimeError("video_urls is required and must be a non-empty array.")
    if not all(isinstance(url, str) and url.strip() for url in video_urls):
        raise RuntimeError("Every item in video_urls must be a non-empty string URL.")

    min_clip = payload.get("min_clip_seconds", DEFAULT_MIN_CLIP_SECONDS)
    max_clip = payload.get("max_clip_seconds", DEFAULT_MAX_CLIP_SECONDS)
    target_total = payload.get("target_total_seconds", DEFAULT_TARGET_TOTAL_SECONDS)

    if not isinstance(min_clip, (int, float)) or min_clip <= 0:
        raise RuntimeError("min_clip_seconds must be > 0.")
    if not isinstance(max_clip, (int, float)) or max_clip <= 0:
        raise RuntimeError("max_clip_seconds must be > 0.")
    if min_clip > max_clip:
        raise RuntimeError("min_clip_seconds must be <= max_clip_seconds.")
    if not isinstance(target_total, (int, float)) or target_total <= 0:
        raise RuntimeError("target_total_seconds must be > 0.")

    if "seed" in payload and not isinstance(payload["seed"], int):
        raise RuntimeError("seed must be an integer.")


def _pick_clip_window(
    source_duration: float, min_clip: float, max_clip: float, rng: random.Random
) -> Tuple[float, float]:
    max_allowed = min(max_clip, source_duration)
    min_allowed = min(min_clip, max_allowed)
    if max_allowed <= 0:
        raise RuntimeError(f"Invalid source duration: {source_duration}")
    clip_len = rng.uniform(min_allowed, max_allowed)

    if source_duration <= clip_len + 1e-6:
        return 0.0, round(source_duration, 6)

    start = rng.uniform(0.0, source_duration - clip_len)
    end = start + clip_len
    return round(start, 6), round(end, 6)


def run(payload: Dict) -> Dict:
    _validate_payload(payload)
    token = _ensure_token()

    video_urls: List[str] = [u.strip() for u in payload["video_urls"]]
    draft_id: Optional[str] = payload.get("draft_id") or None
    min_clip = float(payload.get("min_clip_seconds", DEFAULT_MIN_CLIP_SECONDS))
    max_clip = float(payload.get("max_clip_seconds", DEFAULT_MAX_CLIP_SECONDS))
    target_total = float(payload.get("target_total_seconds", DEFAULT_TARGET_TOTAL_SECONDS))
    track_name = payload.get("track_name", DEFAULT_TRACK_NAME)
    seed = payload.get("seed")

    rng = random.Random(seed)

    durations: Dict[str, float] = {}
    for url in video_urls:
        durations[url] = _get_media_duration_seconds(token, url)

    current_start = 0.0
    segment_index = 0
    segments = []
    last_output = {}

    # Randomly sample sources until target duration is reached.
    while current_start < target_total - 1e-6 and segment_index < MAX_SEGMENTS:
        source_url = rng.choice(video_urls)
        source_duration = durations[source_url]
        clip_start, clip_end = _pick_clip_window(source_duration, min_clip, max_clip, rng)
        clip_len = round(clip_end - clip_start, 6)
        if clip_len <= 0:
            break

        remaining = target_total - current_start
        if clip_len > remaining:
            clip_end = round(clip_start + remaining, 6)
            clip_len = round(clip_end - clip_start, 6)

        req = {
            "video_url": source_url,
            "start": clip_start,
            "end": clip_end,
            "target_start": round(current_start, 6),
            "track_name": track_name,
            "volume": -100,
        }
        if draft_id:
            req["draft_id"] = draft_id

        resp_body = _add_video_once(token, req)
        output = resp_body.get("output") or {}
        draft_id = output.get("draft_id") or draft_id
        last_output = output

        segments.append(
            {
                "index": segment_index,
                "video_url": source_url,
                "source_duration_seconds": source_duration,
                "start": clip_start,
                "end": clip_end,
                "target_start": req["target_start"],
                "clip_duration_seconds": clip_len,
                "volume": -100,
                "material_id": output.get("material_id"),
            }
        )
        current_start += clip_len
        segment_index += 1

    if not draft_id:
        raise RuntimeError("Failed to create/update draft_id from add_video responses.")

    return {
        "success": True,
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "seed": seed,
            "input_video_count": len(video_urls),
            "segment_count": len(segments),
            "target_total_seconds": target_total,
            "actual_total_seconds": round(current_start, 6),
            "track_name": track_name,
            "fixed_volume": -100,
        },
        "durations": durations,
        "result": {
            "draft_id": draft_id,
            "draft_url": last_output.get("draft_url"),
            "segments": segments,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Randomly remix multiple videos into muted B-roll by add_video."
    )
    parser.add_argument("payload_json", help="Path to remix payload JSON.")
    parser.add_argument("--output", default="remix_result.json")
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
