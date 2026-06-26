#!/usr/bin/env python3
"""Unified image rendering command for zhuang-infochart-master channels."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import shutil
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render an infochart image from a final prompt.")
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Final image prompt text.")
    prompt_group.add_argument("--prompt-file", help="Text file containing the final image prompt.")
    parser.add_argument("--mode", default="create", choices=["create", "edit"], help="Generation mode.")
    parser.add_argument("--run-dir", help="Output run directory. Defaults to runs/YYYYMMDD_HHMMSS_infochart.")
    parser.add_argument("--channel", help="Channel name from config.json. Defaults to default_channel.")
    parser.add_argument("--config", default=str(SKILL_DIR / "config.json"), help="Path to config.json.")
    parser.add_argument("--image-size", help="Provider image size. Defaults to landscape_16_9 for create and auto for edit.")
    parser.add_argument("--quality", default="high", choices=["auto", "low", "medium", "high"])
    parser.add_argument("--num-images", type=int, default=1, choices=range(1, 5), metavar="{1,2,3,4}")
    parser.add_argument("--output-format", default="png", choices=["png", "jpeg", "webp"])
    parser.add_argument("--output-prefix", default="output", help="Image filename prefix.")
    parser.add_argument("--image-url", action="append", default=[], help="Reference image URL for edit mode. Can be repeated.")
    parser.add_argument("--image-urls-json", help="JSON array of reference image URLs for edit mode.")
    parser.add_argument("--mask-url", help="Optional mask image URL for edit mode.")
    parser.add_argument("--extra-json", default="{}", help="Extra provider parameters as a JSON object.")
    parser.add_argument("--dry-run", action="store_true", help="Write request files without calling the provider.")
    return parser.parse_args()


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        return Path(args.prompt_file).expanduser().read_text(encoding="utf-8").strip()
    return args.prompt.strip()


def load_config(path: str) -> dict[str, Any]:
    config_path = Path(path).expanduser()
    if not config_path.exists():
        raise SystemExit(f"Config file not found: {config_path}")
    return json.loads(config_path.read_text(encoding="utf-8"))


def make_run_dir(run_dir_arg: str | None) -> Path:
    if run_dir_arg:
        run_dir = Path(run_dir_arg).expanduser()
        if not run_dir.is_absolute():
            run_dir = SKILL_DIR / run_dir
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = SKILL_DIR / "runs" / f"{stamp}_infochart"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def resolve_channel(config: dict[str, Any], channel_name: str | None) -> tuple[str, dict[str, Any]]:
    name = channel_name or config.get("default_channel")
    channels = config.get("channels", {})
    if not name or name not in channels:
        available = ", ".join(sorted(channels)) or "(none)"
        raise SystemExit(f"Unknown channel '{name}'. Available channels: {available}")
    return name, channels[name]


def edit_image_urls(args: argparse.Namespace) -> list[str]:
    image_urls = list(args.image_url or [])
    if args.image_urls_json:
        try:
            parsed = json.loads(args.image_urls_json)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"--image-urls-json is not valid JSON: {exc}") from exc
        if not isinstance(parsed, list) or not all(isinstance(item, str) for item in parsed):
            raise SystemExit("--image-urls-json must be a JSON array of strings.")
        image_urls.extend(parsed)
    return image_urls


def provider_arguments(args: argparse.Namespace, prompt: str) -> dict[str, Any]:
    try:
        extra = json.loads(args.extra_json)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--extra-json is not valid JSON: {exc}") from exc
    if not isinstance(extra, dict):
        raise SystemExit("--extra-json must decode to a JSON object.")

    image_size = args.image_size or ("auto" if args.mode == "edit" else "landscape_16_9")
    arguments = {
        "prompt": prompt,
        "image_size": image_size,
        "quality": args.quality,
        "num_images": args.num_images,
        "output_format": args.output_format,
    }
    if args.mode == "edit":
        image_urls = edit_image_urls(args)
        if not image_urls:
            raise SystemExit("Edit mode requires at least one --image-url or --image-urls-json value.")
        arguments["image_urls"] = image_urls
        if args.mask_url:
            arguments["mask_url"] = args.mask_url
    arguments.update(extra)
    return arguments


def resolve_model_id(channel: dict[str, Any], mode: str) -> str:
    key = "edit_model_id" if mode == "edit" else "model_id"
    model_id = channel.get(key)
    if not model_id:
        raise SystemExit(f"Channel requires {key}.")
    return str(model_id)


def call_provider(channel: dict[str, Any], mode: str, arguments: dict[str, Any]) -> dict[str, Any]:
    provider = channel.get("provider")
    if provider == "fal.ai":
        log("waiting for fal.ai provider")
        return call_fal(channel, mode, arguments)
    raise SystemExit(f"Unsupported provider: {provider}")


def call_fal(channel: dict[str, Any], mode: str, arguments: dict[str, Any]) -> dict[str, Any]:
    api_key = (channel.get("api_key") or "").strip()
    if not api_key:
        raise SystemExit("Missing API key. Fill config.json channels.fal.api_key.")

    model_id = resolve_model_id(channel, mode)

    try:
        import fal_client  # type: ignore
    except ImportError:
        log("fal_client is not installed; using direct HTTP request")
        return call_fal_http(channel, model_id, arguments, api_key)

    os.environ["FAL_KEY"] = api_key
    log(f"submitting request to fal.ai model {model_id}")
    result = fal_client.subscribe(model_id, arguments=arguments)
    if not isinstance(result, dict):
        return {"result": result}
    return result


def call_fal_http(channel: dict[str, Any], model_id: str, arguments: dict[str, Any], api_key: str) -> dict[str, Any]:
    base_url = (channel.get("base_url") or "https://fal.run").rstrip("/")
    model_path = model_id.strip("/")
    url = f"{base_url}/{model_path}"
    log(f"submitting HTTP request to {url}")
    body = json.dumps(arguments).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"fal HTTP request failed: {exc.code} {detail}") from exc


def extract_image_urls(value: Any) -> list[str]:
    urls: list[str] = []

    def walk(node: Any, key_hint: str = "") -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                walk(child, key)
        elif isinstance(node, list):
            for child in node:
                walk(child, key_hint)
        elif isinstance(node, str):
            if node.startswith("http") and (
                key_hint in {"url", "image_url", "content_url"}
                or re.search(r"\.(png|jpg|jpeg|webp)(\?|$)", node, re.IGNORECASE)
            ):
                urls.append(node)

    walk(value)
    return urls


def log(message: str) -> None:
    print(f"[zhuang-infochart-master] {message}", file=sys.stderr, flush=True)


def output_path(run_dir: Path, prefix: str, index: int, total: int, output_format: str) -> Path:
    suffix = ".jpg" if output_format == "jpeg" else f".{output_format}"
    if total == 1:
        return run_dir / f"{prefix}{suffix}"
    return run_dir / f"{prefix}_{index:02d}{suffix}"


def download_image(url: str, destination: Path) -> Path:
    log(f"downloading image to {destination}")
    request = urllib.request.Request(url, headers={"User-Agent": "zhuang-infochart-master/1.0"})
    with urllib.request.urlopen(request, timeout=300) as response:
        content_type = response.headers.get("Content-Type", "")
        suffix = mimetypes.guess_extension(content_type.split(";")[0].strip()) if content_type else None
        final_path = destination
        if suffix and destination.suffix.lower() != suffix.lower():
            final_path = destination.with_suffix(suffix)
        with final_path.open("wb") as handle:
            shutil.copyfileobj(response, handle)
    return final_path


def main() -> int:
    args = parse_args()
    prompt = load_prompt(args)
    config = load_config(args.config)
    channel_name, channel = resolve_channel(config, args.channel)
    run_dir = make_run_dir(args.run_dir)
    arguments = provider_arguments(args, prompt)
    model_id = resolve_model_id(channel, args.mode)
    log(f"run directory: {run_dir}")

    (run_dir / "final_prompt_en.txt").write_text(prompt + "\n", encoding="utf-8")
    (run_dir / "generation_request.json").write_text(
        json.dumps(
            {"mode": args.mode, "channel": channel_name, "provider": channel.get("provider"), "model_id": model_id, "arguments": arguments},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if args.dry_run:
        (run_dir / "generation_result.json").write_text(
            json.dumps({"dry_run": True, "channel": channel_name}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(str(run_dir))
        return 0

    log(f"using channel: {channel_name}")
    result = call_provider(channel, args.mode, arguments)
    urls = extract_image_urls(result)
    if not urls:
        (run_dir / "generation_result.json").write_text(
            json.dumps({"channel": channel_name, "result": result}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        raise SystemExit("No image URL found in generation result. Saved generation_result.json for inspection.")

    saved_paths: list[str] = []
    for index, url in enumerate(urls[: args.num_images], start=1):
        destination = output_path(run_dir, args.output_prefix, index, min(len(urls), args.num_images), args.output_format)
        saved_paths.append(str(download_image(url, destination)))
    log(f"saved {len(saved_paths)} image file(s)")

    (run_dir / "generation_result.json").write_text(
        json.dumps(
            {
                "channel": channel_name,
                "provider": channel.get("provider"),
                "mode": args.mode,
                "model_id": model_id,
                "image_urls": urls,
                "output_paths": saved_paths,
                "result": result,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print("\n".join(saved_paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
