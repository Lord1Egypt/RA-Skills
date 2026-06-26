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
SUBMIT_PATH = "/llm/image/submit_task/generate"
STATUS_PATH = "/llm/image/submit_task/task_status"
DONE_STATUSES = {"success", "failed"}

# These fields only make sense when compose_draft=true.
DRAFT_ONLY_FIELDS = {
    "start",
    "end",
    "draft_id",
    "transform_x",
    "transform_y",
    "scale_x",
    "scale_y",
    "track_name",
    "relative_index",
    "intro_animation",
    "intro_animation_duration",
    "outro_animation",
    "outro_animation_duration",
    "combo_animation",
    "combo_animation_duration",
    "transition",
    "transition_duration",
    "mask_type",
    "mask_center_x",
    "mask_center_y",
    "mask_size",
    "mask_rotation",
    "mask_feather",
    "mask_invert",
    "mask_rect_width",
    "mask_round_corner",
    "background_blur",
    "alpha",
    "flip_horizontal",
    "rotation",
    "transform_x_px",
    "transform_y_px",
    "mix_type",
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


def _load_capabilities(cap_path):
    with open(cap_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    models = data.get("models") or {}
    alias_to_model = {}
    for model_name, info in models.items():
        aliases = info.get("aliases") or []
        for alias in aliases:
            alias_to_model[alias] = model_name
    return data, models, alias_to_model


def _collect_reference_images(payload):
    refs = []
    one = payload.get("reference_image")
    many = payload.get("reference_images")
    if isinstance(one, str) and one.strip():
        refs.append(one.strip())
    if isinstance(many, list):
        refs.extend([x.strip() for x in many if isinstance(x, str) and x.strip()])
    return refs


def _validate_payload(payload, models, alias_to_model, ref_limit):
    if not isinstance(payload.get("prompt"), str) or not payload["prompt"].strip():
        raise RuntimeError("Missing required field: prompt")

    input_model = payload.get("model")
    if not isinstance(input_model, str) or not input_model.strip():
        raise RuntimeError("Missing required field: model")
    if input_model not in alias_to_model:
        supported = sorted(alias_to_model.keys())
        raise RuntimeError(
            f"Unsupported model {input_model!r}. Supported values: {supported}"
        )
    canonical_model = alias_to_model[input_model]

    model_info = models[canonical_model]
    size = payload.get("size")
    if not isinstance(size, str) or not size.strip():
        raise RuntimeError("Missing required field: size")
    allowed = set(model_info.get("allowed_sizes") or [])
    if size not in allowed:
        raise RuntimeError(
            f"Unsupported size {size!r} for model {canonical_model}. "
            f"Allowed sizes: {sorted(allowed)}"
        )

    one = payload.get("reference_image")
    many = payload.get("reference_images")
    refs = _collect_reference_images(payload)
    if one and many:
        raise RuntimeError(
            "reference_image and reference_images cannot be used together. "
            "Use reference_image for one image, reference_images for multiple images."
        )
    if isinstance(many, list) and len(many) == 1:
        raise RuntimeError(
            "If only one reference image is provided, use reference_image instead of reference_images."
        )
    if refs:
        if not model_info.get("supports_reference_images", False):
            raise RuntimeError(
                f"Model {canonical_model} does not support reference images."
            )
        if len(refs) >= ref_limit:
            raise RuntimeError(
                f"Too many reference images: {len(refs)}. Must be < {ref_limit}."
            )

    payload["model"] = canonical_model
    if "compose_draft" not in payload:
        payload["compose_draft"] = True

    if payload.get("compose_draft") is True:
        missing = []
        if "start" not in payload:
            missing.append("start")
        if "end" not in payload:
            missing.append("end")
        if missing:
            raise RuntimeError(
                f"compose_draft=true requires fields: {missing}"
            )

    ignored_fields = []
    if payload.get("compose_draft") is False:
        for field in sorted(DRAFT_ONLY_FIELDS):
            if field in payload:
                ignored_fields.append(field)
                payload.pop(field, None)

    return {
        "canonical_model": canonical_model,
        "reference_image_count": len(refs),
        "ignored_fields_when_compose_false": ignored_fields,
    }


def submit_task(token, payload):
    resp = requests.post(
        f"{BASE_URL}{SUBMIT_PATH}",
        headers=_auth_headers(token),
        json=payload,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))
    if not body.get("task_id"):
        raise RuntimeError(f"submit response missing task_id: {body}")
    return body


def query_task_status(token, task_id):
    resp = requests.get(
        f"{BASE_URL}{STATUS_PATH}",
        headers=_auth_headers(token),
        params={"task_id": task_id},
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    return body


def wait_until_done(token, task_id, poll_interval, timeout):
    started = time.monotonic()
    while True:
        status_body = query_task_status(token, task_id)
        status = status_body.get("status")
        if status in DONE_STATUSES:
            return status_body
        if time.monotonic() - started >= timeout:
            raise RuntimeError(
                f"Polling timeout after {timeout}s. "
                f"Last status={status!r}, body={status_body}"
            )
        time.sleep(poll_interval)


def run(payload, cap_path, poll_interval=2.0, timeout=600):
    token = _ensure_token()
    caps_raw, models, alias_to_model = _load_capabilities(cap_path)
    validation_meta = _validate_payload(
        payload=payload,
        models=models,
        alias_to_model=alias_to_model,
        ref_limit=caps_raw.get("reference_image_limit_exclusive", 14),
    )
    submit_body = submit_task(token, payload)
    status_body = wait_until_done(
        token=token,
        task_id=submit_body["task_id"],
        poll_interval=poll_interval,
        timeout=timeout,
    )
    if status_body.get("status") != "success":
        error = (
            (status_body.get("result") or {}).get("error")
            or status_body.get("error")
            or str(status_body)
        )
        raise RuntimeError(f"generate_ai_image task failed: {error}")

    result = status_body.get("result") or {}
    return {
        "success": True,
        "meta": {
            "task_id": submit_body.get("task_id"),
            "message_id": submit_body.get("message_id"),
            "submit_status": submit_body.get("status"),
            "queue_name": submit_body.get("queue_name"),
            "final_status": status_body.get("status"),
            "progress": status_body.get("progress"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "validation": validation_meta,
        },
        "request_payload": payload,
        "result": {
            "image": result.get("image"),
            "draft_id": result.get("draft_id"),
            "draft_url": result.get("draft_url"),
            "reused_from_history": result.get("reused_from_history"),
            "purchase_link": result.get("purchase_link"),
            "raw_result": result,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Submit async AI image generation task and poll until done."
    )
    parser.add_argument(
        "payload_json",
        help="Path to a JSON file containing request payload for /llm/image/submit_task/generate",
    )
    parser.add_argument("--output", default="generated_ai_image_result.json")
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument(
        "--capabilities",
        default=str(
            Path(__file__).resolve().parent.parent
            / "references"
            / "ai-image-model_capabilities.json"
        ),
        help="AI image model capability enum json path",
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
