#!/usr/bin/env python3
"""Turn source copy into a YouTube thumbnail plan and optionally generate it.

The workflow is:
1. Send the source copy to Gemini text generation.
2. Receive structured JSON with angle, overlay text, and final image prompt.
3. Optionally call the Gemini image endpoint to generate the PNG.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

from generate_image import (
    build_url,
    extract_image_bytes,
    extract_text,
    post_json,
    require_api_key,
    write_outputs,
)


TEXT_MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "gemini-2.5-flash-image"
EXIT_SUCCESS = 0
EXIT_RUNTIME_ERROR = 1
EXIT_ARGUMENT_ERROR = 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a thumbnail concept from copy and optionally render it."
    )
    parser.add_argument("--copy", required=True, help="Source copy or title.")
    parser.add_argument("--audience", help="Target audience.")
    parser.add_argument("--style", help="Desired visual style.")
    parser.add_argument("--brand-colors", help="Comma-separated brand colors.")
    parser.add_argument("--must-include", help="Required visual elements.")
    parser.add_argument("--avoid", help="Banned visual elements.")
    parser.add_argument(
        "--text-model",
        default=TEXT_MODEL,
        help=f"Gemini text model for analysis. Default: {TEXT_MODEL}",
    )
    parser.add_argument(
        "--image-model",
        default=IMAGE_MODEL,
        help=f"Gemini image model for rendering. Default: {IMAGE_MODEL}",
    )
    parser.add_argument(
        "--output-json",
        default="outputs/thumbnail-plan.json",
        help="Where to save the structured result JSON.",
    )
    parser.add_argument(
        "--image-output",
        default="outputs/generated-thumbnail.png",
        help="Where to save the generated PNG if --generate-image is used.",
    )
    parser.add_argument(
        "--generate-image",
        action="store_true",
        help="Generate the PNG after the plan is created.",
    )
    parser.add_argument(
        "--stdout-json",
        action="store_true",
        help="Print the final result JSON to stdout.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Request timeout in seconds.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Retry count for transient API failures.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the text-model payload and exit.",
    )
    return parser.parse_args()


def build_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "angle": {
                "type": "string",
                "description": "Single-sentence thumbnail angle.",
            },
            "overlay_text": {
                "type": "string",
                "description": "Short on-image headline, ideally 2-6 words.",
            },
            "prompt": {
                "type": "string",
                "description": "Final English image prompt for Nano Banana.",
            },
            "generation_notes": {
                "type": "string",
                "description": "One short operational note for image generation.",
            },
        },
        "required": ["angle", "overlay_text", "prompt", "generation_notes"],
        "propertyOrdering": [
            "angle",
            "overlay_text",
            "prompt",
            "generation_notes",
        ],
    }


def normalize_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def validate_args(args: argparse.Namespace) -> None:
    args.copy = normalize_text(args.copy)
    args.audience = normalize_text(args.audience)
    args.style = normalize_text(args.style)
    args.brand_colors = normalize_text(args.brand_colors)
    args.must_include = normalize_text(args.must_include)
    args.avoid = normalize_text(args.avoid)

    if not args.copy:
        raise ValueError("--copy must not be empty.")


def build_analysis_prompt(args: argparse.Namespace) -> str:
    extra = {
        "target_audience": args.audience,
        "visual_style": args.style,
        "brand_colors": args.brand_colors,
        "must_include": args.must_include,
        "avoid": args.avoid,
    }
    extra_context = json.dumps(extra, ensure_ascii=False, indent=2)
    return f"""You are building a YouTube thumbnail plan from source copy.

Return JSON only. Follow these rules:
- Optimize for high click-through rate and mobile readability.
- Choose one dominant visual story.
- Write overlay text that is short and punchy.
- Write the final image prompt in English.
- The image prompt must describe a 16:9 YouTube thumbnail, strong contrast, one dominant subject, and clear negative space for large text.
- Avoid poster-like compositions, clutter, tiny props, and long text inside the image.
- If the source copy is abstract, infer a more visual angle without copying the full sentence into the overlay text.
- Respect must_include and avoid constraints when provided.

User inputs:
{extra_context}

Source copy:
{args.copy}
"""


def build_text_payload(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "contents": [{"parts": [{"text": build_analysis_prompt(args)}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": build_schema(),
            "temperature": 0.7,
        },
    }


def request_thumbnail_plan(args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    response = post_json(
        url=build_url(args.text_model),
        api_key=api_key,
        payload=build_text_payload(args),
        timeout=args.timeout,
        retries=args.retries,
    )
    text = extract_text(response)
    if not text:
        raise RuntimeError(
            "The text model did not return plan text. Full response:\n"
            + json.dumps(response, ensure_ascii=False, indent=2)
        )
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Model returned non-JSON text: {text}") from exc


def save_plan(path: pathlib.Path, plan: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_result(
    *,
    args: argparse.Namespace,
    plan: dict[str, Any] | None,
    plan_path: pathlib.Path | None,
    image_path: pathlib.Path | None,
    image_metadata_path: pathlib.Path | None,
    error: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "ok": error is None,
        "input": {
            "copy": args.copy,
            "audience": args.audience,
            "style": args.style,
            "brand_colors": args.brand_colors,
            "must_include": args.must_include,
            "avoid": args.avoid,
            "generate_image": args.generate_image,
            "text_model": args.text_model,
            "image_model": args.image_model,
        },
        "plan": plan,
        "artifacts": {
            "plan_json": str(plan_path) if plan_path else None,
            "image_png": str(image_path) if image_path else None,
            "image_metadata_json": (
                str(image_metadata_path) if image_metadata_path else None
            ),
        },
        "error": error,
    }


def print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def write_result(path: pathlib.Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_image(args: argparse.Namespace, api_key: str, plan: dict[str, Any]) -> tuple[pathlib.Path, pathlib.Path]:
    payload = {
        "contents": [{"parts": [{"text": plan["prompt"]}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }
    response = post_json(
        url=build_url(args.image_model),
        api_key=api_key,
        payload=payload,
        timeout=args.timeout,
        retries=args.retries,
    )
    image_bytes = extract_image_bytes(response)
    output_path = pathlib.Path(args.image_output)
    metadata_path = pathlib.Path(f"{args.image_output}.json")
    metadata = {
        "model": args.image_model,
        "angle": plan["angle"],
        "overlay_text": plan["overlay_text"],
        "prompt": plan["prompt"],
        "generation_notes": plan["generation_notes"],
        "response_text": extract_text(response),
    }
    write_outputs(
        output_path=output_path,
        metadata_path=metadata_path,
        image_bytes=image_bytes,
        metadata=metadata,
    )
    return output_path, metadata_path


def main() -> int:
    args = parse_args()
    try:
        validate_args(args)
    except ValueError as exc:
        result = build_result(
            args=args,
            plan=None,
            plan_path=None,
            image_path=None,
            image_metadata_path=None,
            error={"code": "invalid_arguments", "message": str(exc)},
        )
        if args.stdout_json:
            print_json(result)
        else:
            print(str(exc), file=sys.stderr)
        return EXIT_ARGUMENT_ERROR

    payload = build_text_payload(args)
    if args.dry_run:
        print_json(payload)
        return EXIT_SUCCESS

    plan_path = pathlib.Path(args.output_json)
    image_path: pathlib.Path | None = None
    image_metadata_path: pathlib.Path | None = None

    try:
        api_key = require_api_key()
        plan = request_thumbnail_plan(args, api_key)
        result = build_result(
            args=args,
            plan=plan,
            plan_path=plan_path,
            image_path=None,
            image_metadata_path=None,
            error=None,
        )
        write_result(plan_path, result)

        if args.generate_image:
            image_path, image_metadata_path = render_image(args, api_key, plan)
            result = build_result(
                args=args,
                plan=plan,
                plan_path=plan_path,
                image_path=image_path,
                image_metadata_path=image_metadata_path,
                error=None,
            )
            write_result(plan_path, result)

        if args.stdout_json:
            print_json(result)
        else:
            print(plan_path)
            if image_path and image_metadata_path:
                print(image_path)
                print(image_metadata_path)
        return EXIT_SUCCESS
    except Exception as exc:
        result = build_result(
            args=args,
            plan=None,
            plan_path=plan_path,
            image_path=image_path,
            image_metadata_path=image_metadata_path,
            error={"code": "runtime_error", "message": str(exc)},
        )
        write_result(plan_path, result)
        if args.stdout_json:
            print_json(result)
        else:
            print(str(exc), file=sys.stderr)
            print(plan_path)
        return EXIT_RUNTIME_ERROR


if __name__ == "__main__":
    sys.exit(main())
