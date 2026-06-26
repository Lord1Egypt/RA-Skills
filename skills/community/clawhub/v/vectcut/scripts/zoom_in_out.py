#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
import re
import sys
import time

import requests

BASE_URL = "https://open.vectcut.com"
SPLIT_SUBMIT_PATH = "/process/split_video/submit_task/submit_split_video_task"
SPLIT_STATUS_PATH = "/process/split_video/submit_task/task_status"
ADD_VIDEO_PATH = "/cut_jianying/add_video"
ADD_VIDEO_KEYFRAME_PATH = "/cut_jianying/add_video_keyframe"
QUERY_SCRIPT_PATH = "/cut_jianying/query_script"

DONE_STATUSES = {"success", "failed", "not_found", "succeeded"}
TIME_PATTERN = re.compile(r"^(?:(\d+):)?([0-5]?\d):([0-5]?\d(?:\.\d+)?)$")

DEFAULTS = {
    "target_start": 0.0,
    "track_name": "zoom_video",
    "width": 1080,
    "height": 1920,
    "mode": "in-out",
    "interval_seconds": 0.2,
    "scale_normal": 1.0,
    "scale_emphasis": 1.1,
    "poll_interval": 2.0,
    "poll_timeout": 600.0,
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


def _extract_status(body):
    status = str(body.get("status") or "").strip().lower()
    if status:
        return status
    result = body.get("result")
    if isinstance(result, dict):
        return str(result.get("status") or "").strip().lower()
    return ""


def _parse_time_to_seconds(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise RuntimeError("time value cannot be empty")
        try:
            return float(text)
        except ValueError:
            pass
        match = TIME_PATTERN.match(text)
        if not match:
            raise RuntimeError(
                f"Invalid time format: {value!r}. Use seconds or HH:MM:SS(.ms)."
            )
        hour = int(match.group(1) or 0)
        minute = int(match.group(2))
        second = float(match.group(3))
        return hour * 3600 + minute * 60 + second
    raise RuntimeError(f"Unsupported time type: {type(value).__name__}")


def _with_defaults(payload):
    merged = dict(DEFAULTS)
    merged.update(payload)
    return merged


def _validate_payload(payload):
    if not isinstance(payload, dict):
        raise RuntimeError("Payload must be a JSON object.")

    video_url = payload.get("video_url")
    if not isinstance(video_url, str) or not video_url.startswith(("http://", "https://")):
        raise RuntimeError("video_url is required and must be a valid http/https URL.")

    for key in ("clip_start", "clip_end"):
        if key not in payload:
            raise RuntimeError(f"{key} is required.")

    clip_start = _parse_time_to_seconds(payload["clip_start"])
    clip_end = _parse_time_to_seconds(payload["clip_end"])
    if clip_start < 0 or clip_end < 0:
        raise RuntimeError("clip_start/clip_end cannot be negative.")
    if clip_end <= clip_start:
        raise RuntimeError("clip_end must be greater than clip_start.")

    target_start = payload.get("target_start")
    if not isinstance(target_start, (int, float)) or target_start < 0:
        raise RuntimeError("target_start must be a non-negative number.")

    for key in ("width", "height"):
        value = payload.get(key)
        if not isinstance(value, int) or value <= 0:
            raise RuntimeError(f"{key} must be a positive integer.")

    mode = payload.get("mode")
    if mode not in {"in-out", "out-in"}:
        raise RuntimeError("mode must be one of: in-out, out-in.")

    interval = payload.get("interval_seconds")
    if not isinstance(interval, (int, float)) or interval <= 0:
        raise RuntimeError("interval_seconds must be a positive number.")

    scale_normal = payload.get("scale_normal")
    scale_emphasis = payload.get("scale_emphasis")
    if not isinstance(scale_normal, (int, float)) or scale_normal <= 0:
        raise RuntimeError("scale_normal must be a positive number.")
    if not isinstance(scale_emphasis, (int, float)) or scale_emphasis <= 0:
        raise RuntimeError("scale_emphasis must be a positive number.")

    clip_duration = clip_end - clip_start
    if clip_duration <= 2 * float(interval):
        raise RuntimeError(
            "Clip duration is too short for start/end keyframe pairs. "
            "Need clip_duration > 2 * interval_seconds."
        )

    track_name = payload.get("track_name")
    if not isinstance(track_name, str) or not track_name.strip():
        raise RuntimeError("track_name must be a non-empty string.")

    draft_id = payload.get("draft_id")
    if draft_id is not None and (
        not isinstance(draft_id, str) or not draft_id.strip()
    ):
        raise RuntimeError("draft_id must be a non-empty string when provided.")

    for key in ("poll_interval", "poll_timeout"):
        value = payload.get(key)
        if not isinstance(value, (int, float)) or value <= 0:
            raise RuntimeError(f"{key} must be a positive number.")

    payload["_clip_start_seconds"] = clip_start
    payload["_clip_end_seconds"] = clip_end
    payload["_clip_duration_seconds"] = clip_duration


def _split_video_submit(token, video_url, start_seconds, end_seconds):
    payload = {
        "video_url": video_url,
        "start": start_seconds,
        "end": end_seconds,
    }
    resp = requests.post(
        f"{BASE_URL}{SPLIT_SUBMIT_PATH}",
        headers=_auth_headers(token),
        json=payload,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or body.get("success") is False:
        raise RuntimeError(body.get("error") or str(body))
    task_id = body.get("task_id")
    if not task_id:
        raise RuntimeError(f"split-video submit response missing task_id: {body}")
    return body


def _split_video_wait(token, task_id, poll_interval, poll_timeout):
    started = time.monotonic()
    while True:
        resp = requests.get(
            f"{BASE_URL}{SPLIT_STATUS_PATH}",
            headers=_auth_headers(token),
            params={"task_id": task_id},
            timeout=60,
        )
        body = _parse_json_response(resp)
        if resp.status_code != 200:
            raise RuntimeError(body.get("error") or str(body))

        status = _extract_status(body)
        if status in DONE_STATUSES:
            if status not in {"success", "succeeded"}:
                raise RuntimeError(f"split-video task failed: {body}")
            return body

        if time.monotonic() - started >= poll_timeout:
            raise RuntimeError(
                f"split-video polling timeout after {poll_timeout}s, last body: {body}"
            )
        time.sleep(poll_interval)


def _split_video(token, video_url, clip_start, clip_end, poll_interval, poll_timeout):
    submit_body = _split_video_submit(token, video_url, clip_start, clip_end)
    status_body = _split_video_wait(
        token=token,
        task_id=submit_body["task_id"],
        poll_interval=poll_interval,
        poll_timeout=poll_timeout,
    )
    result = status_body.get("result")
    if not isinstance(result, dict):
        result = {}
    clip_url = result.get("public_url")
    if not isinstance(clip_url, str) or not clip_url:
        raise RuntimeError(f"split-video result missing public_url: {status_body}")
    return {
        "submit": submit_body,
        "status": status_body,
        "clip_url": clip_url,
    }


def _add_video(token, payload):
    req = {
        "video_url": payload["video_url"],
        "target_start": payload["target_start"],
        "track_name": payload["track_name"],
        "width": payload["width"],
        "height": payload["height"],
    }
    if payload.get("draft_id"):
        req["draft_id"] = payload["draft_id"]

    resp = requests.post(
        f"{BASE_URL}{ADD_VIDEO_PATH}",
        headers=_auth_headers(token),
        json=req,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or body.get("success") is False:
        raise RuntimeError(body.get("error") or str(body))
    output = body.get("output")
    if not isinstance(output, dict) or not output.get("draft_id"):
        raise RuntimeError(f"add_video response missing output.draft_id: {body}")
    return body


def _add_keyframes(token, draft_id, track_name, times, values):
    req = {
        "draft_id": draft_id,
        "track_name": track_name,
        "property_types": ["uniform_scale", "uniform_scale"],
        "times": times,
        "values": [str(values[0]), str(values[1])],
    }
    resp = requests.post(
        f"{BASE_URL}{ADD_VIDEO_KEYFRAME_PATH}",
        headers=_auth_headers(token),
        json=req,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or body.get("success") is False:
        raise RuntimeError(body.get("error") or str(body))
    return body


def _query_draft(token, draft_id, force_update=True):
    req = {
        "draft_id": draft_id,
        "force_update": force_update,
    }
    resp = requests.post(
        f"{BASE_URL}{QUERY_SCRIPT_PATH}",
        headers=_auth_headers(token),
        json=req,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or body.get("success") is False:
        raise RuntimeError(body.get("error") or str(body))

    output_raw = body.get("output")
    if isinstance(output_raw, str):
        try:
            draft = json.loads(output_raw)
        except json.JSONDecodeError:
            draft = output_raw
    else:
        draft = output_raw
    return {"raw_response": body, "draft": draft}


def _verify_draft(draft, track_name):
    if not isinstance(draft, dict):
        return {
            "track_found": False,
            "video_segment_count": 0,
            "notes": "query_script output is not a JSON object",
        }

    tracks = draft.get("tracks")
    if not isinstance(tracks, list):
        return {
            "track_found": False,
            "video_segment_count": 0,
            "notes": "draft.tracks missing or invalid",
        }

    matched_track = None
    total_video_segments = 0
    for track in tracks:
        if not isinstance(track, dict):
            continue
        t_type = track.get("type")
        segments = track.get("segments")
        if t_type == "video" and isinstance(segments, list):
            total_video_segments += len(segments)
        if track.get("name") == track_name:
            matched_track = track

    matched_segment_count = 0
    if isinstance(matched_track, dict) and isinstance(matched_track.get("segments"), list):
        matched_segment_count = len(matched_track["segments"])

    return {
        "track_found": matched_track is not None,
        "video_segment_count": total_video_segments,
        "matched_track_segment_count": matched_segment_count,
        "notes": "Keyframe count is primarily validated by add_video_keyframe API success responses.",
    }


def run(payload):
    token = _ensure_token()
    normalized = _with_defaults(payload)
    _validate_payload(normalized)

    split_result = _split_video(
        token=token,
        video_url=normalized["video_url"],
        clip_start=normalized["_clip_start_seconds"],
        clip_end=normalized["_clip_end_seconds"],
        poll_interval=float(normalized["poll_interval"]),
        poll_timeout=float(normalized["poll_timeout"]),
    )

    add_video_body = _add_video(
        token=token,
        payload={
            "video_url": split_result["clip_url"],
            "target_start": normalized["target_start"],
            "track_name": normalized["track_name"],
            "width": normalized["width"],
            "height": normalized["height"],
            "draft_id": normalized.get("draft_id"),
        },
    )

    draft_output = add_video_body.get("output", {})
    draft_id = draft_output.get("draft_id")
    if not draft_id:
        raise RuntimeError(f"add_video did not return draft_id: {add_video_body}")

    target_start = float(normalized["target_start"])
    interval = float(normalized["interval_seconds"])
    clip_duration = float(normalized["_clip_duration_seconds"])
    clip_end_on_timeline = target_start + clip_duration

    if normalized["mode"] == "in-out":
        start_values = (normalized["scale_normal"], normalized["scale_emphasis"])
        end_values = (normalized["scale_emphasis"], normalized["scale_normal"])
    else:
        start_values = (normalized["scale_emphasis"], normalized["scale_normal"])
        end_values = (normalized["scale_normal"], normalized["scale_emphasis"])

    start_times = [target_start, target_start + interval]
    end_times = [clip_end_on_timeline - interval, clip_end_on_timeline]

    start_kf_body = _add_keyframes(
        token=token,
        draft_id=draft_id,
        track_name=normalized["track_name"],
        times=start_times,
        values=start_values,
    )
    end_kf_body = _add_keyframes(
        token=token,
        draft_id=draft_id,
        track_name=normalized["track_name"],
        times=end_times,
        values=end_values,
    )

    query_result = _query_draft(token=token, draft_id=draft_id, force_update=True)
    verification = _verify_draft(query_result["draft"], normalized["track_name"])

    return {
        "success": True,
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mode": normalized["mode"],
            "interval_seconds": interval,
            "scale_normal": normalized["scale_normal"],
            "scale_emphasis": normalized["scale_emphasis"],
            "workflow": [
                "split-video",
                "add-video",
                "add-video-keyframe(start pair)",
                "add-video-keyframe(end pair)",
                "query-draft",
            ],
        },
        "input": {
            "video_url": normalized["video_url"],
            "clip_start": normalized["clip_start"],
            "clip_end": normalized["clip_end"],
            "target_start": normalized["target_start"],
            "track_name": normalized["track_name"],
            "draft_id": normalized.get("draft_id"),
        },
        "split": {
            "task_id": split_result["submit"].get("task_id"),
            "clip_url": split_result["clip_url"],
            "raw_submit": split_result["submit"],
            "raw_status": split_result["status"],
        },
        "add_video": {
            "draft_id": draft_id,
            "draft_url": draft_output.get("draft_url"),
            "raw_response": add_video_body,
        },
        "keyframes": {
            "start_pair": {
                "times": start_times,
                "values": list(start_values),
                "raw_response": start_kf_body,
            },
            "end_pair": {
                "times": end_times,
                "values": list(end_values),
                "raw_response": end_kf_body,
            },
        },
        "verification": verification,
        "query_draft": {
            "raw_response": query_result["raw_response"],
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Zoom in/out emphasis workflow: split-video -> add_video -> "
            "add_video_keyframe -> query-draft verification."
        )
    )
    parser.add_argument("payload_json", help="Path to zoom-in-out payload JSON.")
    parser.add_argument("--output", default="zoom_in_out_result.json")
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
