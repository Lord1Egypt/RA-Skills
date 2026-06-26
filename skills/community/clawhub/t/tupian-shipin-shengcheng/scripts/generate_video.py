#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import sys

from client import (
    ConfigError,
    extract_task_id,
    parse_name_value_args,
    parse_payload_args,
    print_json,
    request_json,
    request_multipart,
)
from schedule_task_watch import WatchSchedulingError, build_watch_job_plan, schedule_task_watch


VEO_MODELS = {
    "veo_3_1-fast": {
        "kind": "video",
        "summary": "Text-to-video and reference-image video. Supports up to 3 reference images.",
        "rules": [
            "Text-to-video: prompt required, no reference image required.",
            "Reference-image mode: use up to 3 images.",
            "JSON mode only supports Base64 data inside input_reference, not HTTP image URLs.",
            "Multipart mode is recommended for local image files.",
        ],
    },
    "veo_3_1-fast-fl": {
        "kind": "video",
        "summary": "Start/end frame mode. Supports 1-2 images.",
        "rules": [
            "Must provide 1 or 2 images.",
            "Image 1 is the start frame.",
            "Image 2, if present, is the end frame.",
            "Multipart mode is recommended for local image files.",
        ],
    },
    "veo_3_fast": {
        "kind": "video",
        "summary": "General VEO video generation.",
        "rules": [
            "Prompt required.",
            "Use raw JSON if you need provider-specific fields not exposed by this script.",
        ],
    },
    "veo_3": {
        "kind": "video",
        "summary": "General VEO video generation.",
        "rules": [
            "Prompt required.",
            "Use raw JSON if you need provider-specific fields not exposed by this script.",
        ],
    },
}

BANANA_STANDARD_MODELS = {
    "nano_banana_2",
    "nano_banana_pro",
    "nano_banana_pro-1K",
    "nano_banana_pro-2K",
    "nano_banana_pro-4K",
}

BANANA_GEMINI_MODELS = {
    "nano_banana_2-landscape",
    "nano_banana_2-portrait",
    "nano_banana_pro-1K-landscape",
    "nano_banana_pro-1K-portrait",
    "nano_banana_pro-2K-landscape",
    "nano_banana_pro-2K-portrait",
    "nano_banana_pro-4K-landscape",
    "nano_banana_pro-4K-portrait",
}

SORA_MODELS = {
    "sora-2-landscape-10s",
    "sora-2-portrait-10s",
    "sora-2-landscape-15s",
    "sora-2-portrait-15s",
    "sora-2-pro-landscape-25s",
    "sora-2-pro-portrait-25s",
    "sora-2-pro-landscape-hd-15s",
    "sora-2-pro-portrait-hd-15s",
}


def build_parser():
    parser = argparse.ArgumentParser(
        description="Submit a VEO, Banana, or Sora generation request through the platform relay API."
    )
    parser.add_argument("--model", help="Model path segment, for example veo_3_1-fast or sora-2-landscape-10s.")
    parser.add_argument("--list-models", action="store_true", help="Print the built-in model guide and exit.")
    parser.add_argument("--describe-model", help="Print detailed guidance for one model and exit.")

    parser.add_argument("--payload-json", help="Inline JSON object payload for raw JSON mode.")
    parser.add_argument("--payload-file", help="Path to a JSON file containing the request payload for raw JSON mode.")
    parser.add_argument(
        "--field",
        action="append",
        default=[],
        help="Raw multipart text field in name=value format. Repeatable.",
    )
    parser.add_argument(
        "--file-field",
        action="append",
        default=[],
        help="Raw multipart file field in name=path format. Repeatable.",
    )

    parser.add_argument("--prompt", help="Prompt text for guided builder mode.")
    parser.add_argument("--size", default="1920x1080", help="Video size for VEO builder mode. Default: 1920x1080.")
    parser.add_argument("--style", help="Style field for Sora builder mode.")
    parser.add_argument("--aspect-ratio", help="Aspect ratio for Banana standard builder mode.")
    parser.add_argument("--image-url", help="Sora image-to-video URL input. Do not combine with local reference files.")
    parser.add_argument(
        "--reference-url",
        action="append",
        default=[],
        help="Reference URL. Repeatable. Supported for Banana standard.",
    )
    parser.add_argument(
        "--reference-file",
        action="append",
        default=[],
        help="Reference image file path. Repeatable.",
    )
    parser.add_argument("--start-frame-file", help="Start frame file path for VEO start/end frame mode.")
    parser.add_argument("--end-frame-file", help="End frame file path for VEO start/end frame mode.")

    parser.add_argument(
        "--no-watch",
        action="store_true",
        help="Submit only and skip OpenClaw cron watcher creation.",
    )
    parser.add_argument("--watch-interval", default="30s", help="Cron watcher interval. Default: 30s.")
    parser.add_argument("--notify-session-key", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-session-id", default="", help=argparse.SUPPRESS)
    return parser


def model_family(model_name):
    normalized = str(model_name or "").strip()
    if normalized in VEO_MODELS or normalized.startswith("veo_"):
        return "veo"
    if normalized in SORA_MODELS or normalized.startswith("sora-"):
        return "sora"
    if normalized in BANANA_STANDARD_MODELS:
        return "banana-standard"
    if normalized in BANANA_GEMINI_MODELS:
        return "banana-gemini"
    return "unknown"


def print_model_guide():
    guide = {
        "veo_video_models": {
            "veo_3_1-fast": "Text-to-video or reference-image video. Reference mode supports up to 3 images.",
            "veo_3_1-fast-fl": "Start/end frame mode. Must provide 1-2 images.",
            "veo_3_fast": "General VEO video generation.",
            "veo_3": "General VEO video generation.",
        },
        "banana_image_models": {
            "standard": sorted(BANANA_STANDARD_MODELS),
            "gemini": sorted(BANANA_GEMINI_MODELS),
        },
        "sora_video_models": sorted(SORA_MODELS),
        "notes": [
            "VEO reference images: local file upload is recommended.",
            "VEO JSON mode only supports Base64 input_reference, not HTTP image URLs.",
            "Sora: use image_url or one local input_reference file, not both.",
            "Banana standard: use prompt plus optional metadata.urls and metadata.aspectRatio.",
            "Banana gemini: use contents plus generationConfig, or use the builder mode with prompt and local reference files.",
        ],
    }
    print_json(guide)


def print_model_description(model_name):
    family = model_family(model_name)
    normalized = str(model_name or "").strip()
    if family == "veo":
        payload = {
            "model": normalized,
            "family": "veo",
            "summary": VEO_MODELS.get(normalized, {}).get("summary", "VEO model"),
            "rules": VEO_MODELS.get(normalized, {}).get(
                "rules",
                ["Prompt required. Use raw JSON if you need provider-specific fields not exposed by this script."],
            ),
        }
        print_json(payload)
        return
    if family == "sora":
        print_json(
            {
                "model": normalized,
                "family": "sora",
                "summary": "Sora video generation",
                "rules": [
                    "Prompt required.",
                    "Text-to-video: no image input.",
                    "Image-to-video: provide image_url or one local input_reference file.",
                    "Do not combine image_url with local reference files.",
                ],
            }
        )
        return
    if family == "banana-standard":
        print_json(
            {
                "model": normalized,
                "family": "banana-standard",
                "summary": "Banana standard async image generation",
                "rules": [
                    "Prompt required.",
                    "Optional aspect ratio goes into metadata.aspectRatio.",
                    "Reference URLs or local image files become metadata.urls.",
                ],
            }
        )
        return
    if family == "banana-gemini":
        print_json(
            {
                "model": normalized,
                "family": "banana-gemini",
                "summary": "Gemini Banana async image generation via platform conversion",
                "rules": [
                    "Prompt required.",
                    "Local reference files become contents[].parts[].inline_data.",
                    "Use raw JSON if you need to hand-author contents or generationConfig.",
                ],
            }
        )
        return
    raise ValueError(f"Unknown model: {model_name}")


def file_to_data_url(file_path):
    with open(file_path, "rb") as handle:
        raw = handle.read()
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    return f"data:{mime_type};base64,{base64.b64encode(raw).decode('ascii')}"


def require_prompt(args):
    prompt = str(args.prompt or "").strip()
    if not prompt:
        raise ValueError("Prompt is required in builder mode. Use --prompt or switch to raw payload mode.")
    return prompt


def validate_file_paths(paths):
    normalized = []
    for item in paths:
        if not item:
            continue
        file_path = os.path.abspath(item)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Reference file not found: {item}")
        normalized.append(file_path)
    return normalized


def build_veo_submission(args):
    prompt = require_prompt(args)
    reference_files = validate_file_paths(args.reference_file)
    start_frame_files = validate_file_paths([args.start_frame_file] if args.start_frame_file else [])
    end_frame_files = validate_file_paths([args.end_frame_file] if args.end_frame_file else [])
    all_frame_files = start_frame_files + end_frame_files
    if all_frame_files and reference_files:
        raise ValueError("Do not mix --start-frame-file/--end-frame-file with generic --reference-file.")
    if args.reference_url:
        raise ValueError(
            "VEO builder mode does not accept HTTP reference URLs. Use local files or raw JSON with Base64 input_reference."
        )

    if args.model == "veo_3_1-fast-fl":
        if reference_files:
            raise ValueError("veo_3_1-fast-fl expects start/end frames. Use --start-frame-file and optional --end-frame-file.")
        if not all_frame_files:
            raise ValueError("veo_3_1-fast-fl requires 1 or 2 images. Provide --start-frame-file and optional --end-frame-file.")
        if len(all_frame_files) > 2:
            raise ValueError("veo_3_1-fast-fl supports at most 2 images.")
        fields = [("model", args.model), ("prompt", prompt), ("size", args.size)]
        file_fields = [("input_reference[]", item) for item in all_frame_files]
        fields.append(("input_reference", json.dumps([file_to_data_url(item) for item in all_frame_files], ensure_ascii=False)))
        return {
            "request_kind": "multipart",
            "fields": fields,
            "file_fields": file_fields,
        }

    if len(reference_files) > 3:
        raise ValueError(f"{args.model} supports at most 3 reference images.")
    if reference_files:
        fields = [("model", args.model), ("prompt", prompt), ("size", args.size)]
        file_fields = [("input_reference[]", item) for item in reference_files]
        fields.append(("input_reference", json.dumps([file_to_data_url(item) for item in reference_files], ensure_ascii=False)))
        return {
            "request_kind": "multipart",
            "fields": fields,
            "file_fields": file_fields,
        }

    return {
        "request_kind": "json",
        "payload": {
            "model": args.model,
            "prompt": prompt,
            "size": args.size,
            "input_reference": "[]",
        },
    }


def build_sora_submission(args):
    prompt = require_prompt(args)
    reference_files = validate_file_paths(args.reference_file)
    if args.start_frame_file or args.end_frame_file:
        raise ValueError("Sora does not use start/end frame arguments. Use --reference-file or --image-url.")
    if args.reference_url:
        raise ValueError("Sora builder mode does not use --reference-url. Use --image-url for public URLs.")
    if args.image_url and reference_files:
        raise ValueError("Sora accepts image_url or local input_reference file, not both.")
    if len(reference_files) > 1:
        raise ValueError("Sora accepts at most one local input_reference file.")

    if reference_files:
        fields = [("model", args.model), ("prompt", prompt)]
        if args.style:
            fields.append(("style", args.style))
        return {
            "request_kind": "multipart",
            "fields": fields,
            "file_fields": [("input_reference", reference_files[0])],
        }

    payload = {
        "model": args.model,
        "prompt": prompt,
    }
    if args.style:
        payload["style"] = args.style
    if args.image_url:
        payload["image_url"] = args.image_url
    return {
        "request_kind": "json",
        "payload": payload,
    }


def build_banana_standard_submission(args):
    prompt = require_prompt(args)
    reference_files = validate_file_paths(args.reference_file)
    if args.start_frame_file or args.end_frame_file or args.image_url:
        raise ValueError("Banana standard does not use image_url or start/end frame arguments.")
    urls = [item.strip() for item in args.reference_url if item.strip()]
    urls.extend(file_to_data_url(item) for item in reference_files)
    metadata = {}
    if args.aspect_ratio:
        metadata["aspectRatio"] = args.aspect_ratio
    if urls:
        metadata["urls"] = urls
    payload = {
        "model": args.model,
        "prompt": prompt,
    }
    if metadata:
        payload["metadata"] = metadata
    return {
        "request_kind": "json",
        "payload": payload,
    }


def build_banana_gemini_submission(args):
    prompt = require_prompt(args)
    reference_files = validate_file_paths(args.reference_file)
    if args.reference_url:
        raise ValueError("Gemini Banana builder mode supports local files only. Use raw JSON if you need custom contents.")
    if args.start_frame_file or args.end_frame_file or args.image_url or args.style:
        raise ValueError("Gemini Banana builder mode only uses prompt and local reference files.")
    parts = [{"inline_data": {"mime_type": mimetypes.guess_type(item)[0] or "image/png", "data": file_to_data_url(item).split(",", 1)[1]}} for item in reference_files]
    parts.append({"text": prompt})
    payload = {
        "model": args.model,
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    return {
        "request_kind": "json",
        "payload": payload,
    }


def build_guided_submission(args):
    if not args.model:
        raise ValueError("Model is required unless you use --list-models or --describe-model.")
    family = model_family(args.model)
    if family == "veo":
        return build_veo_submission(args)
    if family == "sora":
        return build_sora_submission(args)
    if family == "banana-standard":
        return build_banana_standard_submission(args)
    if family == "banana-gemini":
        return build_banana_gemini_submission(args)
    raise ValueError(
        f"Unknown model '{args.model}'. Use --list-models for built-in guidance or raw payload mode if this is a new model."
    )


def has_raw_payload_args(args):
    return bool(args.payload_json or args.payload_file or args.field or args.file_field)


def has_guided_args(args):
    return bool(
        args.prompt
        or args.style
        or args.image_url
        or args.reference_url
        or args.reference_file
        or args.start_frame_file
        or args.end_frame_file
        or args.aspect_ratio
    )


def submit_request(args):
    if args.list_models:
        print_model_guide()
        return None
    if args.describe_model:
        print_model_description(args.describe_model)
        return None

    if not args.model:
        raise ValueError("Model is required for submission.")

    if has_raw_payload_args(args) and has_guided_args(args):
        raise ValueError("Do not mix raw payload args with guided builder args.")

    if has_raw_payload_args(args):
        if args.payload_json or args.payload_file:
            payload = parse_payload_args(payload_json=args.payload_json, payload_file=args.payload_file)
            return request_json("POST", f"/veo2/custom_video/model/{args.model}", payload=payload)
        fields = parse_name_value_args(args.field, label="--field")
        file_fields = parse_name_value_args(args.file_field, label="--file-field")
        return request_multipart("POST", f"/veo2/custom_video/model/{args.model}", fields=fields, file_fields=file_fields)

    submission_plan = build_guided_submission(args)
    if submission_plan["request_kind"] == "json":
        return request_json("POST", f"/veo2/custom_video/model/{args.model}", payload=submission_plan["payload"])
    return request_multipart(
        "POST",
        f"/veo2/custom_video/model/{args.model}",
        fields=submission_plan["fields"],
        file_fields=submission_plan["file_fields"],
    )


def task_kind_for_model(model_name):
    family = model_family(model_name)
    if family == "banana-standard" or family == "banana-gemini":
        return "banana-image"
    if family == "sora":
        return "sora-video"
    return "veo-video"


def task_label_for_args(args):
    if args.prompt:
        return str(args.prompt).strip()[:80]
    return str(args.model or "").strip()


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        submission = submit_request(args)
        if submission is None:
            return 0
        task_id = extract_task_id(submission)
        result = {
            "submission": submission,
            "task_id": task_id,
        }
        if not args.no_watch:
            if not task_id:
                raise RuntimeError("Submission succeeded but no task id was returned, so watcher creation is not possible.")
            watcher = None
            watcher_error = None
            watcher_status = "unavailable"
            watch_command = None
            try:
                plan = build_watch_job_plan(
                    task_id=str(task_id),
                    task_kind=task_kind_for_model(args.model),
                    label=task_label_for_args(args),
                    every=args.watch_interval,
                    notify_session_key=args.notify_session_key,
                    notify_session_id=args.notify_session_id,
                )
                watch_command = plan.get("shell_command")
                watcher = schedule_task_watch(
                    task_id=str(task_id),
                    task_kind=task_kind_for_model(args.model),
                    label=task_label_for_args(args),
                    every=args.watch_interval,
                    notify_session_key=args.notify_session_key,
                    notify_session_id=args.notify_session_id,
                )
                watcher_status = "scheduled"
            except WatchSchedulingError as exc:
                watcher_error = str(exc)
                watcher_status = "failed"
            result["watcher"] = {
                "status": watcher_status,
                "job_id": (watcher or {}).get("job_id"),
                "notify_on_completion": watcher_status == "scheduled" and bool((watcher or {}).get("job_id")),
                "interval": args.watch_interval,
                "command": watch_command,
                "error": watcher_error,
                "task_kind": task_kind_for_model(args.model),
            }
        print_json(result)
        return 0
    except (ConfigError, FileNotFoundError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"{exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
