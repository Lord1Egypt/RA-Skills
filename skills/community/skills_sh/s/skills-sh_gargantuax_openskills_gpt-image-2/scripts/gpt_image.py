#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence
from urllib import error, request


DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_IMAGES_MODEL = "gpt-image-2"
DEFAULT_RESPONSES_MODEL = "gpt-5.4"
DEFAULT_TIMEOUT = 300
DEFAULT_SIZE = "auto"
DEFAULT_QUALITY = "high"
DEFAULT_OUTPUT_FORMAT = "webp"
SIZE_PATTERN = re.compile(r"^(\d+)x(\d+)$")


def is_gpt_image_model(model: str) -> bool:
    return model.startswith("gpt-image-")


def is_gpt_image_2_model(model: str) -> bool:
    return model.startswith("gpt-image-2")


def load_dotenv(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if value and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key] = value
    return values


def resolve_dotenv_path(raw_path: str | None) -> Path | None:
    if raw_path:
        return Path(raw_path).expanduser().resolve()
    current = Path.cwd().resolve()
    for directory in (current, *current.parents):
        candidate = directory / ".env"
        if candidate.exists():
            return candidate
    return None


def resolve_value(
    cli_value: Any,
    env_name: str,
    dotenv_values: Dict[str, str],
    default: Any = None,
) -> Any:
    if cli_value is not None:
        return cli_value
    env_value = os.environ.get(env_name)
    if env_value not in (None, ""):
        return env_value
    dotenv_value = dotenv_values.get(env_name)
    if dotenv_value not in (None, ""):
        return dotenv_value
    return default


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "on"}:
        return True
    if text in {"0", "false", "no", "off"}:
        return False
    raise SystemExit(f"Invalid boolean value: {value}")


def parse_int(value: Any, field_name: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise SystemExit(f"{field_name} must be an integer.") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Work with OpenAI-compatible GPT Image 2 APIs across images/generations, images/edits, and responses."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_runtime_args(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--env-file", help="Optional .env file path. Defaults to ./.env when present.")
        subparser.add_argument("--base-url", help="OpenAI-compatible base URL including /v1.")
        subparser.add_argument("--api-key", help="API key. Prefer env var or .env instead of CLI.")
        subparser.add_argument("--model", help="Request model name. Defaults depend on the subcommand.")
        subparser.add_argument("--timeout", type=int, help="HTTP timeout in seconds.")
        subparser.add_argument("--output", required=True, help="Output file path or pattern such as out-{index}.png.")
        subparser.add_argument("--save-response", help="Write the raw JSON response or streamed events to this path.")
        subparser.add_argument("--json", action="store_true", default=None, help="Print the final summary as JSON.")
        subparser.add_argument("--dry-run", action="store_true", default=None, help="Print the built request and exit.")

    def add_common_image_args(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--size", help="Image size, for example 1024x1024, 1536x1024, or auto.")
        subparser.add_argument("--quality", help="Image quality: auto, low, medium, or high.")
        subparser.add_argument("--background", help="Image background: auto or opaque.")
        subparser.add_argument("--format", dest="output_format", help="Output format: png, jpeg, or webp.")
        subparser.add_argument("--compression", type=int, help="Output compression 0..100 for jpeg/webp.")
        subparser.add_argument("--moderation", help="Moderation mode: auto or low.")
        subparser.add_argument("--user", help="Optional OpenAI-compatible user field.")
        subparser.add_argument("--stream", action="store_true", default=None, help="Enable streaming.")
        subparser.add_argument("--partial-images", type=int, help="Partial image count for streaming image flows.")

    generations = subparsers.add_parser("generations", help="Call POST /v1/images/generations.")
    add_runtime_args(generations)
    generations.add_argument("--prompt", required=True, help="Generation prompt.")
    generations.add_argument("--n", type=int, help="Image count 1..10.")
    generations.add_argument("--response-format", help="Legacy compatibility field. Omit it for OpenAI GPT image models.")
    add_common_image_args(generations)

    edits = subparsers.add_parser("edits", help="Call POST /v1/images/edits.")
    add_runtime_args(edits)
    edits.add_argument("--prompt", required=True, help="Edit prompt.")
    edits.add_argument("--image", action="append", default=[], help="Input image path. Repeat to send multiple images.")
    edits.add_argument("--mask", help="Optional mask image path.")
    edits.add_argument("--image-field-style", choices=["simple", "brackets", "indexed"], default="brackets")
    edits.add_argument("--n", type=int, help="Image count 1..10.")
    edits.add_argument("--response-format", help="Legacy compatibility field. Omit it for OpenAI GPT image models.")
    add_common_image_args(edits)

    responses = subparsers.add_parser("responses", help="Call POST /v1/responses with the image_generation tool.")
    add_runtime_args(responses)
    responses.add_argument("--input-text", action="append", default=[], help="Input text item. Repeat to add multiple items.")
    responses.add_argument("--input-image", action="append", default=[], help="Local image path. Converted to a data URL.")
    responses.add_argument("--input-image-url", action="append", default=[], help="Remote image URL.")
    responses.add_argument("--input-image-data-url", action="append", default=[], help="Prebuilt image data URL.")
    responses.add_argument("--input-image-file-id", action="append", default=[], help="Image file reference.")
    responses.add_argument("--mask", help="Optional local mask image path. Sent as a tool object.")
    responses.add_argument("--mask-url", help="Optional mask image URL.")
    responses.add_argument("--mask-file-id", help="Optional mask file reference.")
    responses.add_argument("--tool-model", help="Optional image model for the image_generation tool.")
    responses.add_argument("--action", choices=["auto", "generate", "edit"], help="Optional image_generation tool action.")
    responses.add_argument("--input-fidelity", choices=["high", "low"], help="Optional input_fidelity for supported tool models.")
    responses.add_argument(
        "--tool-choice",
        help="Optional tool_choice. Accepts auto|required|none|image_generation or a raw JSON object.",
    )
    responses.add_argument("--previous-response-id", help="Optional previous_response_id value.")
    responses.add_argument("--metadata-json", help="Optional metadata JSON string.")
    add_common_image_args(responses)

    return parser.parse_args()


def validate_size(size: str | None, model: str) -> None:
    if not size or size == "auto" or not is_gpt_image_2_model(model):
        return
    match = SIZE_PATTERN.match(size)
    if not match:
        raise SystemExit("size must be auto or WIDTHxHEIGHT, for example 1024x1024.")
    width = int(match.group(1))
    height = int(match.group(2))
    if width % 16 != 0 or height % 16 != 0:
        raise SystemExit("gpt-image-2 requires width and height to be multiples of 16.")
    if max(width, height) > 3840:
        raise SystemExit("gpt-image-2 longest edge must be <= 3840.")
    ratio = max(width / height, height / width)
    if ratio > 3:
        raise SystemExit("gpt-image-2 aspect ratio must be <= 3:1.")
    pixels = width * height
    if pixels < 655360 or pixels > 8294400:
        raise SystemExit("gpt-image-2 total pixels must be between 655360 and 8294400.")


def validate_common_options(
    model: str,
    background: str | None,
    output_format: str | None,
    output_compression: int | None,
    partial_images: int | None,
    stream: bool,
) -> None:
    if background == "transparent" and is_gpt_image_2_model(model):
        raise SystemExit("gpt-image-2 does not support transparent background.")
    if output_compression is not None and output_format not in {"jpeg", "webp"}:
        raise SystemExit("output_compression is only valid with output_format jpeg or webp.")
    if output_compression is not None and not 0 <= output_compression <= 100:
        raise SystemExit("output_compression must be between 0 and 100.")
    if partial_images is not None and not stream:
        raise SystemExit("partial_images requires stream=true.")
    if partial_images is not None and not 0 <= partial_images <= 3:
        raise SystemExit("partial_images must be between 0 and 3.")


def validate_public_images_route(
    model: str,
    size: str | None,
    stream: bool,
    n: int,
    response_format: str | None,
) -> None:
    validate_size(size, model)
    if n < 1 or n > 10:
        raise SystemExit("n must be between 1 and 10.")
    if is_gpt_image_model(model) and response_format not in (None, ""):
        raise SystemExit("OpenAI GPT image models return base64 image data by default. Omit response_format.")
    if stream and n > 1:
        raise SystemExit("Public Images routes do not support stream=true with n>1.")


def guess_mime_type(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    return mime_type or "application/octet-stream"


def file_to_data_url(path: Path) -> str:
    mime_type = guess_mime_type(path)
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def make_output_path(template: str, index: int, total: int, variant: str) -> Path:
    path = Path(template)
    rendered = str(path)
    if "{index}" in rendered or "{variant}" in rendered:
        rendered = rendered.replace("{index}", str(index))
        rendered = rendered.replace("{variant}", variant)
        return Path(rendered).expanduser().resolve()
    if total == 1 and variant == "final":
        return path.expanduser().resolve()
    suffix = path.suffix
    stem = str(path.with_suffix(""))
    marker = str(index) if variant == "final" else f"{index}-{variant}"
    return Path(f"{stem}-{marker}{suffix}").expanduser().resolve()


def write_json_file(path: str, data: Any) -> None:
    output_path = Path(path).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def encode_multipart(fields: Sequence[tuple[str, str]], files: Sequence[tuple[str, Path]]) -> tuple[str, bytes]:
    boundary = f"----codex-{uuid.uuid4().hex}"
    body = bytearray()
    for name, value in fields:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(str(value).encode("utf-8"))
        body.extend(b"\r\n")
    for field_name, file_path in files:
        mime_type = guess_mime_type(file_path)
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            f'Content-Disposition: form-data; name="{field_name}"; filename="{file_path.name}"\r\n'.encode("utf-8")
        )
        body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
        body.extend(file_path.read_bytes())
        body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    return f"multipart/form-data; boundary={boundary}", bytes(body)


def send_request(
    *,
    url: str,
    api_key: str,
    body: bytes,
    content_type: str,
    timeout: int,
    stream: bool,
) -> Any:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": content_type,
    }
    if stream:
        headers["Accept"] = "text/event-stream"
    req = request.Request(url, data=body, method="POST", headers=headers)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            if stream:
                return read_sse_events(response)
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Request failed: HTTP {exc.code}\n{error_body}") from exc
    except error.URLError as exc:
        raise SystemExit(f"Request failed: {exc.reason}") from exc


def read_sse_events(response: Any) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    event_name: str | None = None
    data_lines: List[str] = []

    def flush() -> None:
        nonlocal event_name, data_lines
        if not event_name and not data_lines:
            return
        raw_data = "\n".join(data_lines)
        parsed: Any = raw_data
        if raw_data and raw_data != "[DONE]":
            try:
                parsed = json.loads(raw_data)
            except json.JSONDecodeError:
                parsed = raw_data
        events.append(
            {
                "event": event_name or "message",
                "data": parsed,
                "raw": raw_data,
            }
        )
        event_name = None
        data_lines = []

    for raw_line in response:
        line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
        if not line:
            flush()
            continue
        if line.startswith(":"):
            continue
        field, _, value = line.partition(":")
        if value.startswith(" "):
            value = value[1:]
        if field == "event":
            event_name = value
        elif field == "data":
            data_lines.append(value)
    flush()
    return events


def extract_image_records(node: Any, *, event_name: str | None = None) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            if isinstance(value.get("b64_json"), str):
                records.append(
                    {
                        "kind": "partial" if event_name and "partial" in event_name.lower() else "final",
                        "base64": value["b64_json"],
                        "revised_prompt": value.get("revised_prompt"),
                        "source": path or "root",
                    }
                )
            if value.get("type") == "image_generation_call" and isinstance(value.get("result"), str):
                records.append(
                    {
                        "kind": "final",
                        "base64": value["result"],
                        "revised_prompt": value.get("revised_prompt"),
                        "source": path or "root",
                    }
                )
            if isinstance(value.get("image_base64"), str):
                records.append(
                    {
                        "kind": "partial" if event_name and "partial" in event_name.lower() else "final",
                        "base64": value["image_base64"],
                        "revised_prompt": value.get("revised_prompt"),
                        "source": path or "root",
                    }
                )
            for partial_key in ("partial_image_b64", "partial_b64_json", "partial_image_base64"):
                if isinstance(value.get(partial_key), str):
                    records.append(
                        {
                            "kind": "partial",
                            "base64": value[partial_key],
                            "revised_prompt": value.get("revised_prompt"),
                            "source": path or "root",
                        }
                    )
            for key, child in value.items():
                walk(child, f"{path}.{key}" if path else key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}[{index}]")

    walk(node, "")
    return records


def decode_image_record(record: Dict[str, Any]) -> Dict[str, Any]:
    try:
        image_bytes = base64.b64decode(record["base64"])
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Failed to decode base64 image from {record['source']}.") from exc
    digest = hashlib.sha256(image_bytes).hexdigest()
    return {
        **record,
        "bytes": image_bytes,
        "digest": digest,
    }


def save_images(records: List[Dict[str, Any]], output_template: str) -> List[Dict[str, Any]]:
    saved: List[Dict[str, Any]] = []
    seen: set[str] = set()
    filtered = [decode_image_record(record) for record in records]
    for record in filtered:
        if record["digest"] in seen:
            continue
        seen.add(record["digest"])
        index = len(saved) + 1
        output_path = make_output_path(output_template, index=index, total=len(filtered), variant=record["kind"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(record["bytes"])
        saved.append(
            {
                "path": str(output_path),
                "kind": record["kind"],
                "revised_prompt": record.get("revised_prompt"),
                "source": record.get("source"),
                "sha256": record["digest"],
            }
        )
    if not saved:
        raise SystemExit("No image payloads were found in the response.")
    return saved


def load_file_paths(paths: Sequence[str]) -> List[Path]:
    resolved: List[Path] = []
    for raw in paths:
        path = Path(raw).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"File not found: {path}")
        resolved.append(path)
    return resolved


def common_settings(args: argparse.Namespace, dotenv_values: Dict[str, str]) -> Dict[str, Any]:
    api_key = resolve_value(args.api_key, "OPENAI_API_KEY", dotenv_values)
    if not api_key and not args.dry_run:
        raise SystemExit("Missing OPENAI_API_KEY. Set it in the environment or a .env file.")
    timeout = parse_int(resolve_value(args.timeout, "OPENAI_IMAGE_TIMEOUT", dotenv_values, DEFAULT_TIMEOUT), "timeout")
    settings = {
        "api_key": str(api_key) if api_key else "",
        "base_url": str(resolve_value(args.base_url, "OPENAI_BASE_URL", dotenv_values, DEFAULT_BASE_URL)).rstrip("/"),
        "timeout": timeout,
        "json_output": bool(args.json),
        "dry_run": bool(args.dry_run),
    }
    return settings


def resolve_images_model(args: argparse.Namespace, dotenv_values: Dict[str, str]) -> str:
    return str(resolve_value(args.model, "OPENAI_IMAGE_MODEL", dotenv_values, DEFAULT_IMAGES_MODEL))


def resolve_responses_model(args: argparse.Namespace, dotenv_values: Dict[str, str]) -> str:
    return str(resolve_value(args.model, "OPENAI_RESPONSES_MODEL", dotenv_values, DEFAULT_RESPONSES_MODEL))


def resolve_tool_model(args: argparse.Namespace, dotenv_values: Dict[str, str]) -> str | None:
    value = resolve_value(getattr(args, "tool_model", None), "OPENAI_IMAGE_TOOL_MODEL", dotenv_values)
    if value in (None, ""):
        return None
    return str(value)


def normalize_tool_choice(raw_value: Any) -> str | Dict[str, Any]:
    if raw_value in (None, ""):
        return {"type": "image_generation"}
    if isinstance(raw_value, dict):
        return raw_value
    text = str(raw_value).strip()
    if text in {"none", "auto", "required"}:
        return text
    if text == "image_generation":
        return {"type": "image_generation"}
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit("tool_choice must be auto, required, none, image_generation, or a JSON object.") from exc
    if not isinstance(parsed, dict):
        raise SystemExit("tool_choice JSON must decode to an object.")
    return parsed


def validate_responses_model(model: str) -> None:
    if is_gpt_image_model(model):
        raise SystemExit(
            "For responses with the image_generation tool, use a text-capable Responses model such as gpt-5.4 "
            "instead of a GPT image model."
        )


def validate_input_fidelity(tool_model: str | None, input_fidelity: str | None) -> None:
    if input_fidelity in (None, ""):
        return
    if tool_model is None or is_gpt_image_2_model(tool_model):
        raise SystemExit("input_fidelity is not configurable for gpt-image-2. Omit --input-fidelity.")
    if tool_model.startswith("gpt-image-1-mini"):
        raise SystemExit("input_fidelity is not supported for gpt-image-1-mini.")


def resolve_common_image_options(args: argparse.Namespace, dotenv_values: Dict[str, str]) -> Dict[str, Any]:
    size = resolve_value(getattr(args, "size", None), "OPENAI_IMAGE_SIZE", dotenv_values, DEFAULT_SIZE)
    quality = resolve_value(getattr(args, "quality", None), "OPENAI_IMAGE_QUALITY", dotenv_values, DEFAULT_QUALITY)
    background = resolve_value(getattr(args, "background", None), "OPENAI_IMAGE_BACKGROUND", dotenv_values)
    output_format = resolve_value(
        getattr(args, "output_format", None), "OPENAI_IMAGE_FORMAT", dotenv_values, DEFAULT_OUTPUT_FORMAT
    )
    output_compression_raw = resolve_value(getattr(args, "compression", None), "OPENAI_IMAGE_COMPRESSION", dotenv_values)
    moderation = resolve_value(getattr(args, "moderation", None), "OPENAI_IMAGE_MODERATION", dotenv_values)
    user = resolve_value(getattr(args, "user", None), "OPENAI_IMAGE_USER", dotenv_values)
    stream = parse_bool(resolve_value(getattr(args, "stream", None), "OPENAI_IMAGE_STREAM", dotenv_values, False))
    partial_images_raw = resolve_value(getattr(args, "partial_images", None), "OPENAI_IMAGE_PARTIAL_IMAGES", dotenv_values)
    partial_images = None if partial_images_raw in (None, "") else parse_int(partial_images_raw, "partial_images")
    output_compression = None if output_compression_raw in (None, "") else parse_int(output_compression_raw, "output_compression")
    return {
        "size": size,
        "quality": quality,
        "background": background,
        "output_format": output_format,
        "output_compression": output_compression,
        "moderation": moderation,
        "user": user,
        "stream": stream,
        "partial_images": partial_images,
    }


def build_generations_request(args: argparse.Namespace, dotenv_values: Dict[str, str], settings: Dict[str, Any]) -> Dict[str, Any]:
    model = resolve_images_model(args, dotenv_values)
    image_options = resolve_common_image_options(args, dotenv_values)
    n = parse_int(resolve_value(args.n, "OPENAI_IMAGE_N", dotenv_values, 1), "n")
    response_format = resolve_value(args.response_format, "OPENAI_IMAGE_RESPONSE_FORMAT", dotenv_values)
    validate_common_options(
        model,
        image_options["background"],
        image_options["output_format"],
        image_options["output_compression"],
        image_options["partial_images"],
        image_options["stream"],
    )
    validate_public_images_route(model, image_options["size"], image_options["stream"], n, response_format)
    payload: Dict[str, Any] = {
        "model": model,
        "prompt": args.prompt,
        "n": n,
    }
    if response_format not in (None, ""):
        payload["response_format"] = response_format
    for key, value in image_options.items():
        if value in (None, ""):
            continue
        if key == "stream" and not value:
            continue
        payload[key] = value
    return {
        "url": f"{settings['base_url']}/images/generations",
        "content_type": "application/json",
        "body": json.dumps(payload).encode("utf-8"),
        "stream": image_options["stream"],
        "request_preview": payload,
    }


def build_edits_request(args: argparse.Namespace, dotenv_values: Dict[str, str], settings: Dict[str, Any]) -> Dict[str, Any]:
    model = resolve_images_model(args, dotenv_values)
    image_options = resolve_common_image_options(args, dotenv_values)
    n = parse_int(resolve_value(args.n, "OPENAI_IMAGE_N", dotenv_values, 1), "n")
    response_format = resolve_value(args.response_format, "OPENAI_IMAGE_RESPONSE_FORMAT", dotenv_values)
    image_paths = load_file_paths(args.image)
    if not image_paths:
        raise SystemExit("edits requires at least one --image.")
    validate_common_options(
        model,
        image_options["background"],
        image_options["output_format"],
        image_options["output_compression"],
        image_options["partial_images"],
        image_options["stream"],
    )
    validate_public_images_route(model, image_options["size"], image_options["stream"], n, response_format)

    fields: List[tuple[str, str]] = [
        ("model", model),
        ("prompt", args.prompt),
        ("n", str(n)),
    ]
    if response_format not in (None, ""):
        fields.append(("response_format", str(response_format)))
    for key, value in image_options.items():
        if value in (None, ""):
            continue
        if key == "stream" and not value:
            continue
        fields.append((key, str(value).lower() if isinstance(value, bool) else str(value)))

    files: List[tuple[str, Path]] = []
    for index, path in enumerate(image_paths):
        field_name = "image"
        if args.image_field_style == "brackets":
            field_name = "image[]"
        elif args.image_field_style == "indexed":
            field_name = f"image[{index}]"
        files.append((field_name, path))
    if args.mask:
        mask_path = Path(args.mask).expanduser().resolve()
        if not mask_path.exists():
            raise SystemExit(f"File not found: {mask_path}")
        files.append(("mask", mask_path))

    content_type, body = encode_multipart(fields, files)
    request_preview = {
        "fields": fields,
        "files": [{"field": field, "path": str(path)} for field, path in files],
    }
    return {
        "url": f"{settings['base_url']}/images/edits",
        "content_type": content_type,
        "body": body,
        "stream": image_options["stream"],
        "request_preview": request_preview,
    }


def build_response_input_items(args: argparse.Namespace) -> List[Dict[str, Any]]:
    content: List[Dict[str, Any]] = []
    for text in args.input_text:
        content.append({"type": "input_text", "text": text})
    for path in load_file_paths(args.input_image):
        content.append({"type": "input_image", "image_url": file_to_data_url(path)})
    for url in args.input_image_url:
        content.append({"type": "input_image", "image_url": url})
    for data_url in args.input_image_data_url:
        content.append({"type": "input_image", "image_url": data_url})
    for file_id in args.input_image_file_id:
        content.append({"type": "input_image", "file_id": file_id})
    return content


def build_mask_object(args: argparse.Namespace) -> Dict[str, Any] | None:
    if args.mask:
        path = Path(args.mask).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"File not found: {path}")
        return {"image_url": file_to_data_url(path)}
    if args.mask_url:
        return {"image_url": args.mask_url}
    if args.mask_file_id:
        return {"file_id": args.mask_file_id}
    return None


def build_responses_request(args: argparse.Namespace, dotenv_values: Dict[str, str], settings: Dict[str, Any]) -> Dict[str, Any]:
    responses_model = resolve_responses_model(args, dotenv_values)
    validate_responses_model(responses_model)
    tool_model = resolve_tool_model(args, dotenv_values)
    tool_validation_model = tool_model or DEFAULT_IMAGES_MODEL
    image_options = resolve_common_image_options(args, dotenv_values)
    validate_size(image_options["size"], tool_validation_model)
    validate_common_options(
        tool_validation_model,
        image_options["background"],
        image_options["output_format"],
        image_options["output_compression"],
        image_options["partial_images"],
        image_options["stream"],
    )
    input_fidelity = resolve_value(args.input_fidelity, "OPENAI_IMAGE_INPUT_FIDELITY", dotenv_values)
    validate_input_fidelity(tool_model, input_fidelity)
    tool_choice = normalize_tool_choice(resolve_value(args.tool_choice, "OPENAI_IMAGE_TOOL_CHOICE", dotenv_values))
    input_items = build_response_input_items(args)
    payload: Dict[str, Any] = {
        "model": responses_model,
        "tools": [{"type": "image_generation"}],
        "tool_choice": tool_choice,
        "stream": image_options["stream"],
    }
    if input_items:
        payload["input"] = [{"role": "user", "content": input_items}]
    if args.previous_response_id:
        payload["previous_response_id"] = args.previous_response_id
    if args.metadata_json:
        payload["metadata"] = json.loads(args.metadata_json)
    for key in ("size", "quality", "background", "output_format", "output_compression", "moderation"):
        value = image_options.get(key)
        if value not in (None, ""):
            payload["tools"][0][key] = value
    if tool_model is not None:
        payload["tools"][0]["model"] = tool_model
    if args.action is not None:
        payload["tools"][0]["action"] = args.action
    if input_fidelity not in (None, ""):
        payload["tools"][0]["input_fidelity"] = input_fidelity
    mask_object = build_mask_object(args)
    if mask_object is not None:
        payload["tools"][0]["input_image_mask"] = mask_object
    if image_options["partial_images"] is not None:
        payload["tools"][0]["partial_images"] = image_options["partial_images"]
    if image_options["user"] not in (None, ""):
        payload["user"] = image_options["user"]
    return {
        "url": f"{settings['base_url']}/responses",
        "content_type": "application/json",
        "body": json.dumps(payload).encode("utf-8"),
        "stream": image_options["stream"],
        "request_preview": payload,
    }


def summarize_stream(events: List[Dict[str, Any]], output_template: str) -> Dict[str, Any]:
    image_records: List[Dict[str, Any]] = []
    for event in events:
        if event["raw"] == "[DONE]":
            continue
        image_records.extend(extract_image_records(event["data"], event_name=event["event"]))
    saved = save_images(image_records, output_template)
    return {
        "mode": "stream",
        "events": len(events),
        "images": saved,
    }


def summarize_json_response(response: Any, output_template: str) -> Dict[str, Any]:
    image_records = extract_image_records(response)
    saved = save_images(image_records, output_template)
    return {
        "mode": "json",
        "images": saved,
    }


def print_result(result: Dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"Mode: {result['mode']}")
    if "events" in result:
        print(f"Events: {result['events']}")
    for item in result["images"]:
        print(f"Saved: {item['path']} [{item['kind']}]")
        if item.get("revised_prompt"):
            print(f"Revised prompt: {item['revised_prompt']}")


def main() -> int:
    args = parse_args()
    dotenv_path = resolve_dotenv_path(args.env_file)
    dotenv_values = load_dotenv(dotenv_path) if dotenv_path else {}
    settings = common_settings(args, dotenv_values)

    if args.command == "generations":
        prepared = build_generations_request(args, dotenv_values, settings)
    elif args.command == "edits":
        prepared = build_edits_request(args, dotenv_values, settings)
    else:
        prepared = build_responses_request(args, dotenv_values, settings)

    if settings["dry_run"]:
        print(
            json.dumps(
                {
                    "command": args.command,
                    "url": prepared["url"],
                    "stream": prepared["stream"],
                    "request": prepared["request_preview"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    response = send_request(
        url=prepared["url"],
        api_key=settings["api_key"],
        body=prepared["body"],
        content_type=prepared["content_type"],
        timeout=settings["timeout"],
        stream=prepared["stream"],
    )

    if args.save_response:
        write_json_file(args.save_response, response)

    if prepared["stream"]:
        result = summarize_stream(response, args.output)
    else:
        result = summarize_json_response(response, args.output)

    result["command"] = args.command
    result["url"] = prepared["url"]
    print_result(result, settings["json_output"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Cancelled.", file=sys.stderr)
        raise SystemExit(130)
