#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time

import requests

BASE_URL = "https://open.vectcut.com"
SUBMIT_PATH = "/cut_jianying/generate_ai_video"
STATUS_PATH = "/cut_jianying/aivideo/task_status"
DONE_STATUSES = {"succeeded", "failed", "not_found"}


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


def _load_capabilities(cap_path):
    with open(cap_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    models = data.get("models") or {}
    alias_to_model = {}
    for model_name, info in models.items():
        for alias in info.get("aliases") or []:
            alias_to_model[alias] = model_name
    return models, alias_to_model


def _validate_payload(payload, models, alias_to_model):
    if not isinstance(payload, dict):
        raise RuntimeError("Payload must be a JSON object.")

    prompt = payload.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise RuntimeError("Missing required field: prompt")

    input_model = payload.get("model")
    if not isinstance(input_model, str) or not input_model.strip():
        raise RuntimeError("Missing required field: model")
    if input_model not in alias_to_model:
        raise RuntimeError(
            f"Unsupported model {input_model!r}. Supported values: {sorted(alias_to_model)}"
        )
    canonical_model = alias_to_model[input_model]
    model_info = models[canonical_model]

    resolution = payload.get("resolution")
    if not isinstance(resolution, str) or not resolution.strip():
        raise RuntimeError("Missing required field: resolution")
    allowed_resolutions = set(model_info.get("allowed_resolutions") or [])
    if resolution not in allowed_resolutions:
        raise RuntimeError(
            f"Unsupported resolution {resolution!r} for model {canonical_model}. "
            f"Allowed values: {sorted(allowed_resolutions)}"
        )

    images = payload.get("images")
    if images is None:
        image_count = 0
    elif isinstance(images, list):
        cleaned_images = [x.strip() for x in images if isinstance(x, str) and x.strip()]
        image_count = len(cleaned_images)
        payload["images"] = cleaned_images
    else:
        raise RuntimeError("images must be an array of URL strings.")

    if image_count > 0 and not model_info.get("supports_images", False):
        raise RuntimeError(f"Model {canonical_model} does not support images input.")
    max_images = int(model_info.get("max_images") or 0)
    if image_count > max_images:
        raise RuntimeError(
            f"Too many images for model {canonical_model}: {image_count}. "
            f"Max allowed: {max_images}."
        )

    gen_duration = payload.get("gen_duration")
    if gen_duration is not None:
        if not model_info.get("supports_gen_duration", False):
            raise RuntimeError(f"Model {canonical_model} does not support gen_duration.")
        allowed_durations = set(model_info.get("allowed_gen_duration") or [])
        if allowed_durations and gen_duration not in allowed_durations:
            raise RuntimeError(
                f"Invalid gen_duration {gen_duration!r} for model {canonical_model}. "
                f"Allowed values: {sorted(allowed_durations)}"
            )

    generate_audio = payload.get("generate_audio")
    if generate_audio is not None:
        if not isinstance(generate_audio, bool):
            raise RuntimeError("generate_audio must be a boolean.")
        if generate_audio and not model_info.get("supports_generate_audio", False):
            raise RuntimeError(
                f"Model {canonical_model} does not support generate_audio=true."
            )

    payload["model"] = canonical_model
    return {
        "canonical_model": canonical_model,
        "image_count": image_count,
    }


def submit_task(token, payload):
    resp = requests.post(
        f"{BASE_URL}{SUBMIT_PATH}",
        headers=_auth_headers(token),
        json=payload,
        timeout=90,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("message") or str(body))
    task_id = body.get("task_id")
    if not task_id:
        raise RuntimeError(f"submit response missing task_id: {body}")
    return body


def query_task_status(token, task_id):
    resp = requests.get(
        f"{BASE_URL}{STATUS_PATH}",
        headers=_auth_headers(token),
        params={"task_id": task_id},
        timeout=90,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("message") or str(body))
    return body


def wait_until_done(token, task_id, poll_interval, timeout):
    started = time.monotonic()
    while True:
        status_body = query_task_status(token, task_id)
        status = str(status_body.get("status") or "").strip().lower()
        if status in DONE_STATUSES:
            return status_body
        if time.monotonic() - started >= timeout:
            raise RuntimeError(
                f"Polling timeout after {timeout}s. Last body={status_body}"
            )
        time.sleep(poll_interval)


def run(payload, cap_path, poll_interval=2.0, timeout=1800):
    token = _ensure_token()
    models, alias_to_model = _load_capabilities(cap_path)
    validation = _validate_payload(payload, models=models, alias_to_model=alias_to_model)
    submit_body = submit_task(token, payload)
    status_body = wait_until_done(
        token=token,
        task_id=submit_body["task_id"],
        poll_interval=poll_interval,
        timeout=timeout,
    )
    final_status = str(status_body.get("status") or "").strip().lower()
    if final_status != "succeeded":
        err = status_body.get("message") or status_body.get("draft_error") or str(status_body)
        raise RuntimeError(f"generate-ai-video task failed: {err}")

    return {
        "success": True,
        "meta": {
            "task_id": submit_body.get("task_id"),
            "submit_status": submit_body.get("status"),
            "final_status": final_status,
            "progress": status_body.get("progress"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "validation": validation,
        },
        "request_payload": payload,
        "result": {
            "id": status_body.get("id"),
            "video_url": status_body.get("video_url"),
            "draft_id": status_body.get("draft_id"),
            "draft_url": status_body.get("draft_url"),
            "draft_error": status_body.get("draft_error"),
            "raw_result": status_body,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Submit async AI video generation task and poll until done."
    )
    parser.add_argument(
        "payload_json",
        help="Path to request payload JSON for /cut_jianying/generate_ai_video",
    )
    parser.add_argument("--output", default="generated_ai_video_result.json")
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=1800.0)
    parser.add_argument(
        "--capabilities",
        default=str(
            Path(__file__).resolve().parent.parent
            / "references"
            / "model_capabilities.json"
        ),
        help="Model capability JSON path.",
    )
    args = parser.parse_args()

    try:
        with open(args.payload_json, "r", encoding="utf-8") as f:
            payload = json.load(f)
        result = run(
            payload=payload,
            cap_path=args.capabilities,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
        )
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
