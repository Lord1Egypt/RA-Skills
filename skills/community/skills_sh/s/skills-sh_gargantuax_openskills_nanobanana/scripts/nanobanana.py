#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence
from urllib import error, request


DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = "nanobanana"
DEFAULT_TIMEOUT = 300
DEFAULT_OUTPUT_DIR = "./nanobanana-images"
DEFAULT_BATCH_PREFIX = "image"
DEFAULT_BATCH_COUNT = 10
DEFAULT_BATCH_DELAY = 3.0
DEFAULT_BATCH_PARALLEL = 1

MODEL_ALIASES = {
    "nanobanana": "gemini-2.5-flash-image",
    "nano-banana": "gemini-2.5-flash-image",
    "nanobanana-2": "gemini-3.1-flash-image-preview",
    "nano-banana-2": "gemini-3.1-flash-image-preview",
    "nanobanana2": "gemini-3.1-flash-image-preview",
    "nanobanana-pro": "gemini-3-pro-image-preview",
    "nano-banana-pro": "gemini-3-pro-image-preview",
}

GEMINI_25_FLASH_IMAGE = "gemini-2.5-flash-image"
GEMINI_31_FLASH_IMAGE_PREVIEW = "gemini-3.1-flash-image-preview"
GEMINI_3_PRO_IMAGE_PREVIEW = "gemini-3-pro-image-preview"

RATIOS_GEMINI_25 = {"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"}
RATIOS_GEMINI_3 = {
    "1:1",
    "1:4",
    "1:8",
    "2:3",
    "3:2",
    "3:4",
    "4:1",
    "4:3",
    "4:5",
    "5:4",
    "8:1",
    "9:16",
    "16:9",
    "21:9",
}

MODEL_RULES: Dict[str, Dict[str, Any]] = {
    GEMINI_25_FLASH_IMAGE: {
        "label": "Nano Banana",
        "supports_size": False,
        "sizes": set(),
        "ratios": RATIOS_GEMINI_25,
    },
    GEMINI_31_FLASH_IMAGE_PREVIEW: {
        "label": "Nano Banana 2",
        "supports_size": True,
        "sizes": {"512", "1K", "2K", "4K"},
        "ratios": RATIOS_GEMINI_3,
    },
    GEMINI_3_PRO_IMAGE_PREVIEW: {
        "label": "Nano Banana Pro",
        "supports_size": True,
        "sizes": {"1K", "2K", "4K"},
        "ratios": RATIOS_GEMINI_3,
    },
}


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


def resolve_value(cli_value: Any, env_name: str, dotenv_values: Dict[str, str], default: Any = None) -> Any:
    if cli_value is not None:
        return cli_value
    env_value = os.environ.get(env_name)
    if env_value not in (None, ""):
        return env_value
    dotenv_value = dotenv_values.get(env_name)
    if dotenv_value not in (None, ""):
        return dotenv_value
    return default


def resolve_value_with_source(
    cli_value: Any,
    env_name: str,
    dotenv_values: Dict[str, str],
    default: Any = None,
) -> tuple[Any, str]:
    if cli_value is not None:
        return cli_value, "cli"
    env_value = os.environ.get(env_name)
    if env_value not in (None, ""):
        return env_value, "env"
    dotenv_value = dotenv_values.get(env_name)
    if dotenv_value not in (None, ""):
        return dotenv_value, "dotenv"
    return default, "default"


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


def parse_float(value: Any, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise SystemExit(f"{field_name} must be a number.") from exc


def normalize_alias(value: str) -> str:
    return value.strip().lower().replace("_", "-").replace(" ", "-")


def resolve_model_name(raw_value: str) -> str:
    normalized = normalize_alias(raw_value)
    if normalized in MODEL_ALIASES:
        return MODEL_ALIASES[normalized]
    return raw_value.strip()


def ensure_known_model(model: str) -> Dict[str, Any]:
    rules = MODEL_RULES.get(model)
    if rules is None:
        raise SystemExit(
            "Unsupported Nano Banana model. Use nanobanana, nanobanana-2, nanobanana-pro, "
            "or one of the exact supported model IDs."
        )
    return rules


def validate_base_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if normalized.endswith("/models"):
        raise SystemExit("base-url must point to the Gemini API root, for example https://.../v1beta, not /models.")
    return normalized


def guess_mime_type(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    return mime_type or "application/octet-stream"


def load_file_paths(paths: Sequence[str]) -> List[Path]:
    resolved: List[Path] = []
    for raw in paths:
        path = Path(raw).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"File not found: {path}")
        resolved.append(path)
    return resolved


def image_part_from_path(path: Path) -> Dict[str, Any]:
    return {
        "inline_data": {
            "mime_type": guess_mime_type(path),
            "data": base64.b64encode(path.read_bytes()).decode("ascii"),
        }
    }


def validate_image_options(model: str, aspect_ratio: str | None, image_size: str | None) -> None:
    rules = ensure_known_model(model)
    if aspect_ratio is not None and aspect_ratio not in rules["ratios"]:
        allowed = ", ".join(sorted(rules["ratios"]))
        raise SystemExit(f"{model} does not support aspect ratio {aspect_ratio}. Supported values: {allowed}")
    if image_size in (None, ""):
        return
    if not rules["supports_size"]:
        raise SystemExit(f"{model} does not support image_size. Omit --size.")
    if image_size not in rules["sizes"]:
        order = {"512": 0, "1K": 1, "2K": 2, "4K": 3}
        allowed_sizes = ", ".join(sorted(rules["sizes"], key=lambda item: order.get(item, 99)))
        raise SystemExit(f"{model} does not support image_size={image_size}. Supported values: {allowed_sizes}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate and edit images with Gemini-native Nano Banana models."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_runtime_args(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--env-file", help="Optional .env file path. Defaults to ./.env when present.")
        subparser.add_argument("--base-url", help="Gemini-compatible API root, for example https://.../v1beta.")
        subparser.add_argument("--api-key", help="API key. Prefer env var or .env instead of CLI.")
        subparser.add_argument("--auth-mode", choices=["auto", "x-goog-api-key", "bearer"], help="Header style for auth.")
        subparser.add_argument("--model", help="Model alias or exact supported model ID.")
        subparser.add_argument("--timeout", type=int, help="HTTP timeout in seconds.")
        subparser.add_argument("--ratio", help="Aspect ratio, for example 1:1 or 16:9.")
        subparser.add_argument("--size", help="Image size on Gemini 3 image models: 512, 1K, 2K, or 4K.")
        subparser.add_argument("--search", action="store_true", default=None, help="Enable Google Search grounding.")
        subparser.add_argument("--json", action="store_true", default=None, help="Print the final summary as JSON.")
        subparser.add_argument("--dry-run", action="store_true", default=None, help="Print the built request and exit.")

    generate = subparsers.add_parser("generate", help="Send one generateContent request.")
    add_runtime_args(generate)
    generate.add_argument("--prompt", required=True, help="Prompt or editing instruction.")
    generate.add_argument("--input-image", action="append", default=[], help="Local input image path. Repeat as needed.")
    generate.add_argument("--output", help="Output file path. Defaults to GEMINI_OUTPUT_DIR/timestamp.png.")
    generate.add_argument("--save-response", help="Write the raw JSON response to this path.")

    batch = subparsers.add_parser("batch", help="Repeat the same request multiple times with sequential filenames.")
    add_runtime_args(batch)
    batch.add_argument("--prompt", required=True, help="Prompt or editing instruction.")
    batch.add_argument("--input-image", action="append", default=[], help="Local input image path. Repeat as needed.")
    batch.add_argument("--count", type=int, help="Number of requests to make.")
    batch.add_argument("--dir", dest="output_dir", help="Output directory.")
    batch.add_argument("--prefix", help="Filename prefix.")
    batch.add_argument("--delay", type=float, help="Delay between sequential requests.")
    batch.add_argument("--parallel", type=int, help="Parallel worker count.")
    batch.add_argument("--quiet", action="store_true", default=None, help="Suppress per-request progress output.")

    return parser.parse_args()


def common_settings(args: argparse.Namespace, dotenv_values: Dict[str, str]) -> Dict[str, Any]:
    api_key = resolve_value(args.api_key, "GEMINI_API_KEY", dotenv_values)
    if not api_key and not args.dry_run:
        raise SystemExit("Missing GEMINI_API_KEY. Set it in the environment or a .env file.")
    base_url = validate_base_url(str(resolve_value(args.base_url, "GEMINI_BASE_URL", dotenv_values, DEFAULT_BASE_URL)))
    timeout = parse_int(resolve_value(args.timeout, "GEMINI_TIMEOUT", dotenv_values, DEFAULT_TIMEOUT), "timeout")
    model = resolve_model_name(str(resolve_value(args.model, "GEMINI_MODEL", dotenv_values, DEFAULT_MODEL)))
    auth_mode = str(resolve_value(args.auth_mode, "GEMINI_AUTH_MODE", dotenv_values, "auto"))
    if auth_mode not in {"auto", "x-goog-api-key", "bearer"}:
        raise SystemExit("auth-mode must be one of: auto, x-goog-api-key, bearer.")
    aspect_ratio = resolve_value(args.ratio, "GEMINI_ASPECT_RATIO", dotenv_values)
    image_size, image_size_source = resolve_value_with_source(args.size, "GEMINI_IMAGE_SIZE", dotenv_values)
    if image_size not in (None, ""):
        image_size = str(image_size)
    model_rules = ensure_known_model(model)
    if image_size not in (None, "") and not model_rules["supports_size"] and image_size_source != "cli":
        image_size = None
    use_search = parse_bool(resolve_value(args.search, "GEMINI_USE_SEARCH", dotenv_values, False))
    validate_image_options(model, aspect_ratio, image_size)
    return {
        "api_key": str(api_key) if api_key else "",
        "base_url": base_url,
        "timeout": timeout,
        "model": model,
        "auth_mode": auth_mode,
        "aspect_ratio": aspect_ratio,
        "image_size": image_size,
        "use_search": use_search,
        "output_dir": str(resolve_value(None, "GEMINI_OUTPUT_DIR", dotenv_values, DEFAULT_OUTPUT_DIR)),
        "json_output": bool(args.json),
        "dry_run": bool(args.dry_run),
    }


def build_headers(api_key: str, auth_mode: str, base_url: str) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    is_google_endpoint = "generativelanguage.googleapis.com" in base_url
    if auth_mode == "x-goog-api-key":
        headers["x-goog-api-key"] = api_key
    elif auth_mode == "bearer":
        headers["Authorization"] = f"Bearer {api_key}"
    elif is_google_endpoint:
        headers["x-goog-api-key"] = api_key
    else:
        headers["Authorization"] = f"Bearer {api_key}"
        headers["x-goog-api-key"] = api_key
    return headers


def build_request_payload(
    prompt: str,
    input_images: Sequence[Path],
    model: str,
    aspect_ratio: str | None,
    image_size: str | None,
    use_search: bool,
) -> Dict[str, Any]:
    parts = [image_part_from_path(path) for path in input_images]
    parts.append({"text": prompt})
    payload: Dict[str, Any] = {
        "contents": [
            {
                "role": "user",
                "parts": parts,
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        },
    }
    image_config: Dict[str, Any] = {}
    if aspect_ratio not in (None, ""):
        image_config["aspectRatio"] = aspect_ratio
    if image_size not in (None, ""):
        image_config["imageSize"] = image_size
    if image_config:
        payload["generationConfig"]["imageConfig"] = image_config
    if use_search:
        payload["tools"] = [{"google_search": {}}]
    return payload


def request_url(base_url: str, model: str) -> str:
    return f"{base_url}/models/{model}:generateContent"


def send_request(
    *,
    url: str,
    headers: Dict[str, str],
    body: bytes,
    timeout: int,
) -> Dict[str, Any]:
    req = request.Request(url, data=body, method="POST", headers=headers)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Request failed: HTTP {exc.code}\n{error_body}") from exc
    except error.URLError as exc:
        raise SystemExit(f"Request failed: {exc.reason}") from exc


def write_json_file(path: str, data: Any) -> None:
    output_path = Path(path).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def iter_candidate_parts(response: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    for candidate in response.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            if isinstance(part, dict):
                yield part


def extract_images_and_text(response: Dict[str, Any]) -> Dict[str, Any]:
    images: List[Dict[str, Any]] = []
    texts: List[str] = []
    for part in iter_candidate_parts(response):
        text_value = part.get("text")
        if isinstance(text_value, str) and text_value:
            texts.append(text_value)
        inline_data = part.get("inline_data") or part.get("inlineData")
        if not isinstance(inline_data, dict):
            continue
        mime_type = inline_data.get("mime_type") or inline_data.get("mimeType") or "image/png"
        data = inline_data.get("data")
        if isinstance(data, str) and mime_type.startswith("image/"):
            images.append(
                {
                    "mime_type": mime_type,
                    "data": data,
                }
            )
    if not images:
        raise SystemExit("No image payloads were found in the response.")
    return {"images": images, "texts": texts}


def file_extension_for_mime(mime_type: str) -> str:
    extension = mimetypes.guess_extension(mime_type) or ".png"
    if extension == ".jpe":
        return ".jpg"
    return extension


def decode_image_record(record: Dict[str, Any]) -> Dict[str, Any]:
    image_bytes = base64.b64decode(record["data"])
    digest = hashlib.sha256(image_bytes).hexdigest()
    return {
        **record,
        "bytes": image_bytes,
        "sha256": digest,
    }


def auto_output_path(output_dir: str, extension: str, prefix: str = "nanobanana", suffix: str | None = None) -> Path:
    base = Path(output_dir).expanduser().resolve()
    base.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rendered_suffix = f"_{suffix}" if suffix else ""
    return base / f"{prefix}_{stamp}{rendered_suffix}{extension}"


def render_output_path(template: str | None, index: int, total: int, extension: str, default_output_dir: str) -> Path:
    if template in (None, ""):
        suffix = None if total == 1 else str(index)
        return auto_output_path(default_output_dir, extension, suffix=suffix)
    raw = str(Path(template).expanduser())
    if "{index}" in raw:
        rendered = raw.replace("{index}", str(index))
        candidate = Path(rendered)
    else:
        candidate = Path(raw)
        if total > 1:
            stem = str(candidate.with_suffix(""))
            suffix = candidate.suffix or extension
            candidate = Path(f"{stem}-{index}{suffix}")
    if candidate.suffix == "":
        candidate = candidate.with_suffix(extension)
    return candidate.resolve()


def save_images(records: List[Dict[str, Any]], output_template: str | None, default_output_dir: str) -> List[Dict[str, Any]]:
    decoded = [decode_image_record(record) for record in records]
    saved: List[Dict[str, Any]] = []
    seen: set[str] = set()
    total = len(decoded)
    for record in decoded:
        if record["sha256"] in seen:
            continue
        seen.add(record["sha256"])
        extension = file_extension_for_mime(record["mime_type"])
        output_path = render_output_path(output_template, len(saved) + 1, total, extension, default_output_dir)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(record["bytes"])
        saved.append(
            {
                "path": str(output_path),
                "mime_type": record["mime_type"],
                "sha256": record["sha256"],
            }
        )
    if not saved:
        raise SystemExit("No image payloads were saved from the response.")
    return saved


def summarize_result(
    *,
    response: Dict[str, Any],
    output_template: str | None,
    default_output_dir: str,
    command: str,
    model: str,
    url: str,
) -> Dict[str, Any]:
    extracted = extract_images_and_text(response)
    saved_images = save_images(extracted["images"], output_template, default_output_dir)
    return {
        "command": command,
        "model": model,
        "url": url,
        "images": saved_images,
        "texts": extracted["texts"],
    }


def print_result(result: Dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"Command: {result['command']}")
    print(f"Model: {result['model']}")
    for image in result["images"]:
        print(f"Saved: {image['path']} [{image['mime_type']}]")
    for text in result.get("texts", []):
        print(f"Text: {text}")


def run_generate(args: argparse.Namespace, dotenv_values: Dict[str, str]) -> int:
    settings = common_settings(args, dotenv_values)
    input_images = load_file_paths(args.input_image)
    payload = build_request_payload(
        prompt=args.prompt,
        input_images=input_images,
        model=settings["model"],
        aspect_ratio=settings["aspect_ratio"],
        image_size=settings["image_size"],
        use_search=settings["use_search"],
    )
    url = request_url(settings["base_url"], settings["model"])
    headers = build_headers(settings["api_key"], settings["auth_mode"], settings["base_url"])

    if settings["dry_run"]:
        print(
            json.dumps(
                {
                    "command": "generate",
                    "model": settings["model"],
                    "url": url,
                    "auth_mode": settings["auth_mode"],
                    "request": payload,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    response = send_request(
        url=url,
        headers=headers,
        body=json.dumps(payload).encode("utf-8"),
        timeout=settings["timeout"],
    )
    if args.save_response:
        write_json_file(args.save_response, response)
    result = summarize_result(
        response=response,
        output_template=args.output,
        default_output_dir=settings["output_dir"],
        command="generate",
        model=settings["model"],
        url=url,
    )
    print_result(result, settings["json_output"])
    return 0


def batch_settings(args: argparse.Namespace, dotenv_values: Dict[str, str]) -> Dict[str, Any]:
    output_dir = str(resolve_value(args.output_dir, "GEMINI_OUTPUT_DIR", dotenv_values, DEFAULT_OUTPUT_DIR))
    prefix = str(resolve_value(args.prefix, "GEMINI_BATCH_PREFIX", dotenv_values, DEFAULT_BATCH_PREFIX))
    count = parse_int(resolve_value(args.count, "GEMINI_BATCH_COUNT", dotenv_values, DEFAULT_BATCH_COUNT), "count")
    delay = parse_float(resolve_value(args.delay, "GEMINI_BATCH_DELAY", dotenv_values, DEFAULT_BATCH_DELAY), "delay")
    parallel = parse_int(
        resolve_value(args.parallel, "GEMINI_BATCH_PARALLEL", dotenv_values, DEFAULT_BATCH_PARALLEL),
        "parallel",
    )
    quiet = bool(args.quiet)
    if count < 1:
        raise SystemExit("count must be >= 1.")
    if parallel < 1:
        raise SystemExit("parallel must be >= 1.")
    return {
        "output_dir": output_dir,
        "prefix": prefix,
        "count": count,
        "delay": delay,
        "parallel": parallel,
        "quiet": quiet,
    }


def build_batch_output_template(output_dir: str, prefix: str) -> str:
    directory = Path(output_dir).expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True)
    return str(directory / f"{prefix}-{{index}}")


def execute_single_batch_request(
    *,
    prompt: str,
    input_images: Sequence[Path],
    settings: Dict[str, Any],
    output_template: str,
    default_output_dir: str,
    index: int,
) -> Dict[str, Any]:
    payload = build_request_payload(
        prompt=prompt,
        input_images=input_images,
        model=settings["model"],
        aspect_ratio=settings["aspect_ratio"],
        image_size=settings["image_size"],
        use_search=settings["use_search"],
    )
    url = request_url(settings["base_url"], settings["model"])
    headers = build_headers(settings["api_key"], settings["auth_mode"], settings["base_url"])
    response = send_request(
        url=url,
        headers=headers,
        body=json.dumps(payload).encode("utf-8"),
        timeout=settings["timeout"],
    )
    result = summarize_result(
        response=response,
        output_template=output_template.replace("{index}", f"{index:02d}"),
        default_output_dir=default_output_dir,
        command="batch",
        model=settings["model"],
        url=url,
    )
    result["index"] = index
    return result


def run_batch(args: argparse.Namespace, dotenv_values: Dict[str, str]) -> int:
    settings = common_settings(args, dotenv_values)
    batch = batch_settings(args, dotenv_values)
    input_images = load_file_paths(args.input_image)
    output_template = build_batch_output_template(batch["output_dir"], batch["prefix"])
    url = request_url(settings["base_url"], settings["model"])
    request_preview = build_request_payload(
        prompt=args.prompt,
        input_images=input_images,
        model=settings["model"],
        aspect_ratio=settings["aspect_ratio"],
        image_size=settings["image_size"],
        use_search=settings["use_search"],
    )

    if settings["dry_run"]:
        previews = []
        for index in range(1, batch["count"] + 1):
            previews.append(
                {
                    "index": index,
                    "output_template": output_template.replace("{index}", f"{index:02d}"),
                    "request": request_preview,
                }
            )
        print(
            json.dumps(
                {
                    "command": "batch",
                    "model": settings["model"],
                    "url": url,
                    "auth_mode": settings["auth_mode"],
                    "count": batch["count"],
                    "parallel": batch["parallel"],
                    "requests": previews,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    results: List[Dict[str, Any]] = []
    if batch["parallel"] > 1:
        with ThreadPoolExecutor(max_workers=batch["parallel"]) as executor:
            futures = [
                executor.submit(
                    execute_single_batch_request,
                    prompt=args.prompt,
                    input_images=input_images,
                    settings=settings,
                    output_template=output_template,
                    default_output_dir=batch["output_dir"],
                    index=index,
                )
                for index in range(1, batch["count"] + 1)
            ]
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                if not batch["quiet"]:
                    print(f"[{result['index']}/{batch['count']}] ok")
    else:
        for index in range(1, batch["count"] + 1):
            result = execute_single_batch_request(
                prompt=args.prompt,
                input_images=input_images,
                settings=settings,
                output_template=output_template,
                default_output_dir=batch["output_dir"],
                index=index,
            )
            results.append(result)
            if not batch["quiet"]:
                print(f"[{index}/{batch['count']}] ok")
            if index < batch["count"] and batch["delay"] > 0:
                time.sleep(batch["delay"])

    results.sort(key=lambda item: item["index"])
    summary = {
        "command": "batch",
        "model": settings["model"],
        "url": url,
        "count": batch["count"],
        "results": results,
    }
    if settings["json_output"]:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"Command: batch")
        print(f"Model: {settings['model']}")
        print(f"Completed: {len(results)}/{batch['count']}")
        for item in results:
            for image in item["images"]:
                print(f"Saved: {image['path']} [{image['mime_type']}]")
    return 0


def main() -> int:
    args = parse_args()
    dotenv_path = resolve_dotenv_path(getattr(args, "env_file", None))
    dotenv_values = load_dotenv(dotenv_path) if dotenv_path else {}
    if args.command == "generate":
        return run_generate(args, dotenv_values)
    return run_batch(args, dotenv_values)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Cancelled.", file=sys.stderr)
        raise SystemExit(130)
