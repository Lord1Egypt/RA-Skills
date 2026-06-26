#!/usr/bin/env python3
"""
Qwen Image CLI

Supports:
- text2img: prompt -> image(s)
- img2img: input image(s) + prompt -> image(s)
"""

import argparse
import base64
import datetime as dt
import io
import json
import mimetypes
import os
import re
import shutil
import sys
from pathlib import Path

import requests

try:
    from PIL import Image
except Exception:
    Image = None


ENDPOINTS = {
    "sg": "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
    "bj": "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
}


class ApiError(RuntimeError):
    def __init__(self, status_code: int, code: str, message: str, response_text: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.response_text = response_text
        super().__init__(f"API error {status_code} [{code}]: {message}")


def load_dotenv_files(paths: list[Path]) -> None:
    key_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    for path in paths:
        if not path.is_file():
            continue

        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if not key_pattern.match(key):
                continue

            quoted = len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"')
            if not quoted and " #" in value:
                value = value.split(" #", 1)[0].rstrip()
            elif quoted:
                value = value[1:-1]

            # Keep explicit shell environment highest priority, but allow
            # .env to fill variables that are present with empty values.
            if key not in os.environ or not os.environ.get(key, "").strip():
                os.environ[key] = value


def resolve_dotenv_paths() -> list[Path]:
    candidates = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent / ".env",
    ]
    dedup = []
    seen = set()
    for candidate in candidates:
        resolved = str(candidate.resolve())
        if resolved in seen:
            continue
        seen.add(resolved)
        dedup.append(candidate)
    return dedup


def encode_local_image(path_str: str) -> str:
    path = Path(path_str).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Image file not found: {path}")

    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = "image/png"

    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def normalize_image_input(value: str) -> str:
    val = value.strip()
    lower = val.lower()
    if lower.startswith("http://") or lower.startswith("https://") or lower.startswith("data:image/"):
        return val
    return encode_local_image(val)


def call_qwen_api(
    endpoint: str,
    api_key: str,
    model: str,
    content: list,
    n: int,
    size: str,
    negative_prompt: str,
    prompt_extend: bool,
    watermark: bool,
) -> tuple[dict, list[str]]:
    payload = {
        "model": model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": content,
                }
            ]
        },
        "parameters": {
            "n": n,
            "negative_prompt": negative_prompt,
            "prompt_extend": prompt_extend,
            "watermark": watermark,
        },
    }

    if size:
        payload["parameters"]["size"] = size

    response = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=600,
    )

    if response.status_code != 200:
        code = "UnknownError"
        message = response.text
        try:
            err = response.json()
            code = err.get("code", code)
            message = err.get("message", message)
        except ValueError:
            pass
        raise ApiError(
            status_code=response.status_code,
            code=code,
            message=message,
            response_text=response.text,
        )

    data = response.json()
    choices = data.get("output", {}).get("choices", [])
    if not choices:
        raise RuntimeError(f"Unexpected response: {json.dumps(data, ensure_ascii=False)[:1000]}")

    items = choices[0].get("message", {}).get("content", [])
    urls = [item["image"] for item in items if isinstance(item, dict) and "image" in item]
    if not urls:
        raise RuntimeError(f"No image URL in response: {json.dumps(data, ensure_ascii=False)[:1000]}")

    return data, urls


def download_images(urls: list[str], out_dir: Path) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    files = []

    for idx, url in enumerate(urls, start=1):
        path = out_dir / f"qwen-{timestamp}-{idx:02d}.png"
        resp = requests.get(url, timeout=300)
        resp.raise_for_status()
        path.write_bytes(resp.content)
        files.append(str(path))

    return files


def publish_images(
    files: list[str],
    urls: list[str],
    publish_dir: Path,
    public_base_url: str | None,
) -> tuple[list[str], list[str]]:
    """
    Publish images into a stable outbound directory and optionally map to public URLs.

    - If local files exist, copy them into publish_dir.
    - If no local files exist, fetch from remote URLs and save into publish_dir.
    """
    publish_dir.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    published_files: list[str] = []

    if files:
        for idx, src in enumerate(files, start=1):
            src_path = Path(src).expanduser().resolve()
            suffix = src_path.suffix or ".png"
            dst = publish_dir / f"qwen-{timestamp}-{idx:02d}{suffix}"
            shutil.copy2(src_path, dst)
            published_files.append(str(dst))
    else:
        for idx, url in enumerate(urls, start=1):
            dst = publish_dir / f"qwen-{timestamp}-{idx:02d}.png"
            resp = requests.get(url, timeout=300)
            resp.raise_for_status()
            dst.write_bytes(resp.content)
            published_files.append(str(dst))

    published_urls: list[str] = []
    if public_base_url:
        base = public_base_url.strip().rstrip("/")
        if base:
            for item in published_files:
                rel = Path(item).resolve().relative_to(publish_dir.resolve()).as_posix()
                published_urls.append(f"{base}/{rel}")

    return published_files, published_urls


def create_view_pages(
    published_files: list[str],
    publish_dir: Path,
    public_base_url: str | None,
) -> tuple[list[str], list[str]]:
    """
    Create lightweight HTML viewer pages for generated images.

    Why:
    - Some assistant models rewrite direct image URLs into markdown image syntax.
    - Control UI flattens remote markdown images into plain alt text ("image").
    - Returning an HTML viewer URL in text is more stable for visible/clickable links.
    """
    view_files: list[str] = []
    view_urls: list[str] = []
    base = (public_base_url or "").strip().rstrip("/")
    publish_dir_resolved = publish_dir.resolve()

    for item in published_files:
        image_path = Path(item).expanduser().resolve()
        image_name = image_path.name
        view_name = f"{image_path.stem}.view.html"
        view_path = publish_dir_resolved / view_name
        html = (
            "<!doctype html>\n"
            "<html lang=\"zh-CN\">\n"
            "<head>\n"
            "  <meta charset=\"utf-8\" />\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
            "  <title>Qwen Image Preview</title>\n"
            "  <style>\n"
            "    body { margin: 0; background: #111; color: #ddd; font-family: sans-serif; }\n"
            "    .wrap { max-width: 980px; margin: 0 auto; padding: 16px; }\n"
            "    img { width: 100%; height: auto; border-radius: 8px; display: block; }\n"
            "    .meta { margin-top: 10px; font-size: 12px; color: #aaa; word-break: break-all; }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "  <div class=\"wrap\">\n"
            f"    <img src=\"{image_name}\" alt=\"qwen-generated-image\" />\n"
            f"    <div class=\"meta\">{image_name}</div>\n"
            "  </div>\n"
            "</body>\n"
            "</html>\n"
        )
        view_path.write_text(html, encoding="utf-8")
        view_files.append(str(view_path))
        if base:
            view_urls.append(f"{base}/{view_name}")

    return view_files, view_urls


def build_preview_data_url_from_bytes(
    image_bytes: bytes,
    max_chars: int = 4000,
    max_side: int = 192,
    quality: int = 40,
) -> str | None:
    """Build a small data:image URL for inline rendering in Control UI."""
    if Image is None:
        return None

    side_candidates = [max_side, 384, 320, 256, 224, 192, 160, 128, 96, 72]
    quality_candidates = [quality, 60, 50, 40, 35, 30]

    try:
        with Image.open(io.BytesIO(image_bytes)) as src:
            src = src.convert("RGB")
            best_data_url = None
            for side in side_candidates:
                if side < 64:
                    continue
                for q in quality_candidates:
                    img = src.copy()
                    img.thumbnail((side, side))
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=q, optimize=True)
                    payload = base64.b64encode(buf.getvalue()).decode("ascii")
                    data_url = f"data:image/jpeg;base64,{payload}"
                    best_data_url = data_url
                    if len(data_url) <= max_chars:
                        return data_url
            return best_data_url if best_data_url and len(best_data_url) <= max_chars else None
    except Exception:
        return None


def fetch_url_bytes(url: str) -> bytes:
    resp = requests.get(url, timeout=180)
    resp.raise_for_status()
    return resp.content


def to_preferred_media_ref(path_or_url: str, base_dir: Path | None = None) -> str:
    value = path_or_url.strip()
    lowered = value.lower()
    if lowered.startswith("http://") or lowered.startswith("https://"):
        return value

    root = (base_dir or Path.cwd()).expanduser().resolve()
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (root / path)
    try:
        path = path.resolve()
    except Exception:
        path = path.absolute()

    try:
        rel = path.relative_to(root).as_posix()
        return f"./{rel}" if not rel.startswith(".") else rel
    except Exception:
        return str(path)


def choose_reply_media_refs(
    urls: list[str],
    files: list[str],
    base_dir: Path | None = None,
    preferred_urls: list[str] | None = None,
) -> list[str]:
    if preferred_urls:
        return [item.strip() for item in preferred_urls if item and item.strip()]

    # Prefer downloaded local files so media loading does not depend on temporary URLs.
    if files:
        return [to_preferred_media_ref(item, base_dir=base_dir) for item in files]
    return [to_preferred_media_ref(item, base_dir=base_dir) for item in urls]


def choose_channel_media_refs(urls: list[str], files: list[str]) -> list[str]:
    """
    Prefer absolute local file paths for outbound media delivery.

    Why:
    - Private HTTP URLs can be blocked by SSRF protection in media fetch path.
    - Local absolute paths work with OpenClaw media pipeline when local roots allow them.
    """
    if files:
        refs: list[str] = []
        for item in files:
            path = Path(item).expanduser()
            try:
                refs.append(str(path.resolve()))
            except Exception:
                refs.append(str(path.absolute()))
        return refs
    return [item.strip() for item in urls if item and item.strip()]


def validate_preview_options(max_side: int, quality: int, max_chars: int) -> None:
    if max_side < 64:
        raise SystemExit("--preview-max-side must be >= 64")
    if quality < 20 or quality > 95:
        raise SystemExit("--preview-quality must be in [20, 95]")
    if max_chars < 1000:
        raise SystemExit("--preview-max-chars must be >= 1000")


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--model", default="qwen-image-2.0-pro", help="e.g. qwen-image-2.0 or qwen-image-2.0-pro")
    parser.add_argument("--n", type=int, default=1, help="number of output images, range [1,6]")
    parser.add_argument("--size", default="", help='optional size like "1024*1024"')
    parser.add_argument("--negative-prompt", default=" ", help="negative prompt")
    parser.add_argument("--no-prompt-extend", action="store_true", help="disable prompt extension")
    parser.add_argument("--watermark", action="store_true", help="enable output watermark")
    parser.add_argument("--out-dir", default="./tmp/qwen-image", help="directory to save downloaded images")
    parser.add_argument(
        "--publish-dir",
        default=os.getenv("OPENCLAW_MEDIA_OUTBOUND_DIR", "~/.openclaw/media/outbound"),
        help="directory to publish final images for outbound media delivery",
    )
    parser.add_argument(
        "--public-base-url",
        default=os.getenv("OPENCLAW_MEDIA_BASE_URL", ""),
        help="public base URL mapped to --publish-dir, e.g. https://example.com/gen",
    )
    parser.add_argument(
        "--no-publish-outbound",
        action="store_true",
        help="skip publishing images into --publish-dir",
    )
    parser.add_argument("--no-download", action="store_true", help="do not download generated images")
    parser.add_argument(
        "--preview-inline",
        action="store_true",
        help="include a small preview_data_url (data:image/jpeg;base64,...) for inline UI rendering",
    )
    parser.add_argument("--preview-max-side", type=int, default=192, help="max side length for preview image")
    parser.add_argument("--preview-quality", type=int, default=40, help="jpeg quality for preview image")
    parser.add_argument(
        "--preview-max-chars",
        type=int,
        default=4000,
        help="max characters for preview_data_url to avoid chat truncation",
    )
    parser.add_argument(
        "--emit-openclaw-reply",
        action="store_true",
        help="print final 2-line OpenClaw reply (Chinese text + markdown image URL)",
    )
    parser.add_argument(
        "--reply-file",
        default="",
        help="optional file path to store final OpenClaw reply text when --emit-openclaw-reply is set",
    )
    parser.add_argument(
        "--reply-format",
        choices=["media", "markdown", "payload", "link"],
        default="markdown",
        help="OpenClaw reply format when --emit-openclaw-reply is enabled",
    )
    parser.add_argument(
        "--emit-media-ref",
        action="store_true",
        help="print MEDIA_REF:<path-or-url> for skill parsing without emitting MEDIA: in tool output",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Qwen image text2img / img2img CLI")
    parser.add_argument("--region", choices=["sg", "bj"], default=os.getenv("DASHSCOPE_REGION", "sg"))
    parser.add_argument("--endpoint", default=os.getenv("DASHSCOPE_ENDPOINT", ""))

    subparsers = parser.add_subparsers(dest="mode", required=True)

    t2i = subparsers.add_parser("text2img", help="generate images from text")
    t2i.add_argument("--prompt", required=True, help="generation prompt")
    add_common_args(t2i)

    i2i = subparsers.add_parser("img2img", help="edit/fuse images with text prompt")
    i2i.add_argument("--images", nargs="+", required=True, help="1~3 image inputs: path/url/base64")
    i2i.add_argument("--prompt", required=True, help="editing prompt")
    add_common_args(i2i)

    return parser


def main() -> int:
    load_dotenv_files(resolve_dotenv_paths())

    parser = build_parser()
    args = parser.parse_args()

    api_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("Missing DASHSCOPE_API_KEY")

    endpoint = args.endpoint or ENDPOINTS[args.region]
    endpoint_from_env = bool(os.getenv("DASHSCOPE_ENDPOINT", "").strip())
    endpoint_explicit = bool(args.endpoint or endpoint_from_env)

    if args.n < 1 or args.n > 6:
        raise SystemExit("--n must be in [1, 6]")

    if args.mode == "text2img":
        content = [{"text": args.prompt}]
    else:
        if len(args.images) < 1 or len(args.images) > 3:
            raise SystemExit("img2img requires 1~3 images")
        content = [{"image": normalize_image_input(item)} for item in args.images]
        content.append({"text": args.prompt})

    attempted_endpoints = [endpoint]
    # If endpoint is not explicitly pinned, auto-fallback once for region/key mismatch.
    if not endpoint_explicit:
        alt = ENDPOINTS["bj"] if endpoint == ENDPOINTS["sg"] else ENDPOINTS["sg"]
        attempted_endpoints.append(alt)

    last_error = None
    data = None
    urls = None
    used_endpoint = endpoint

    for idx, ep in enumerate(attempted_endpoints):
        try:
            data, urls = call_qwen_api(
                endpoint=ep,
                api_key=api_key,
                model=args.model,
                content=content,
                n=args.n,
                size=args.size,
                negative_prompt=args.negative_prompt,
                prompt_extend=not args.no_prompt_extend,
                watermark=args.watermark,
            )
            used_endpoint = ep
            if idx > 0:
                print(
                    "Notice: initial endpoint auth failed; switched region endpoint automatically.",
                    file=sys.stderr,
                )
            break
        except ApiError as err:
            last_error = err
            can_retry = (
                idx == 0
                and len(attempted_endpoints) > 1
                and err.status_code == 401
                and err.code == "InvalidApiKey"
            )
            if can_retry:
                continue
            if err.status_code == 401 and err.code == "InvalidApiKey":
                raise SystemExit(
                    "Authentication failed: InvalidApiKey.\n"
                    "Check DASHSCOPE_API_KEY and endpoint/region match.\n"
                    "Try one of these:\n"
                    "1) export DASHSCOPE_REGION=bj   (mainland endpoint)\n"
                    "2) export DASHSCOPE_REGION=sg   (international endpoint)\n"
                    "3) unset DASHSCOPE_API_KEY and rely on .env value\n"
                    "4) regenerate key from Model Studio and update .env"
                ) from err
            raise

    if data is None or urls is None:
        if last_error is not None:
            raise last_error
        raise SystemExit("Unknown error: no API response")

    out_dir = Path(args.out_dir).expanduser()
    files = []
    if not args.no_download:
        files = download_images(urls, out_dir)

    published_files: list[str] = []
    published_urls: list[str] = []
    published_view_files: list[str] = []
    published_view_urls: list[str] = []
    if not args.no_publish_outbound:
        published_files, published_urls = publish_images(
            files=files,
            urls=urls,
            publish_dir=Path(args.publish_dir).expanduser(),
            public_base_url=args.public_base_url.strip() or None,
        )
        published_view_files, published_view_urls = create_view_pages(
            published_files=published_files,
            publish_dir=Path(args.publish_dir).expanduser(),
            public_base_url=args.public_base_url.strip() or None,
        )

    preview_data_url = None
    if args.preview_inline:
        validate_preview_options(
            max_side=args.preview_max_side,
            quality=args.preview_quality,
            max_chars=args.preview_max_chars,
        )

        try:
            if files:
                image_bytes = Path(files[0]).read_bytes()
            else:
                image_bytes = fetch_url_bytes(urls[0])
            preview_data_url = build_preview_data_url_from_bytes(
                image_bytes=image_bytes,
                max_chars=args.preview_max_chars,
                max_side=args.preview_max_side,
                quality=args.preview_quality,
            )
        except Exception:
            preview_data_url = None

    result = {
        "request_id": data.get("request_id"),
        "model": args.model,
        "endpoint": used_endpoint,
        "urls": urls,
        "files": files,
        "published_files": published_files,
        "published_urls": published_urls,
        "published_view_files": published_view_files,
        "published_view_urls": published_view_urls,
        "preview_data_url": preview_data_url,
    }

    (out_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    media_refs = choose_reply_media_refs(
        urls=urls,
        files=published_files or files,
        base_dir=Path.cwd(),
        preferred_urls=published_urls,
    )
    channel_media_refs = choose_channel_media_refs(
        urls=urls,
        files=published_files or files,
    )

    if args.emit_media_ref:
        primary_ref = channel_media_refs[0] if channel_media_refs else urls[0]
        # Skill-level handshake line: parse this and emit MEDIA only in final assistant reply.
        print(f"MEDIA_REF:{primary_ref}")

    if args.emit_openclaw_reply:
        if args.reply_format == "payload":
            primary_media = channel_media_refs[0] if channel_media_refs else urls[0]
            primary_text_link = (
                published_view_urls[0]
                if published_view_urls
                else primary_media
            )
            payload_text = "\n".join(["已为你生成图片。", f"链接（页面）：{primary_text_link}"])

            payload = {
                "text": payload_text,
                "mediaUrl": primary_media,
            }
            if len(channel_media_refs) > 1:
                payload["mediaUrls"] = channel_media_refs
            reply_text = json.dumps(payload, ensure_ascii=False)
        elif args.reply_format == "link":
            primary_text_link = (
                published_view_urls[0]
                if published_view_urls
                else (
                    to_preferred_media_ref(published_view_files[0], base_dir=Path.cwd())
                    if published_view_files
                    else (media_refs[0] if media_refs else urls[0])
                )
            )
            # Text-only mode: avoid MEDIA directives so Control UI will not append "image/图片".
            reply_text = "\n".join(["已为你生成图片。", f"链接（页面）：{primary_text_link}"])
        elif args.reply_format == "media":
            media_lines = (
                [f"MEDIA:{ref}" for ref in channel_media_refs]
                if channel_media_refs
                else [f"MEDIA:{urls[0]}"]
            )
            # Media-first mode for chat channels (e.g. Feishu): send attachment directly.
            reply_text = "\n".join(media_lines)
        else:
            if media_refs and (media_refs[0].startswith("http://") or media_refs[0].startswith("https://")):
                reply_text = f"![生成图片]({media_refs[0]})"
            else:
                # Control UI chat markdown image may fallback to data:image URLs.
                inline_data_url = preview_data_url
                if inline_data_url is None:
                    validate_preview_options(
                        max_side=args.preview_max_side,
                        quality=args.preview_quality,
                        max_chars=args.preview_max_chars,
                    )
                    try:
                        if files:
                            image_bytes = Path(files[0]).read_bytes()
                        else:
                            image_bytes = fetch_url_bytes(urls[0])
                        inline_data_url = build_preview_data_url_from_bytes(
                            image_bytes=image_bytes,
                            max_chars=args.preview_max_chars,
                            max_side=args.preview_max_side,
                            quality=args.preview_quality,
                        )
                    except Exception:
                        inline_data_url = None

                if inline_data_url:
                    # Keep a single markdown image line to minimize model rewrites.
                    reply_text = f"![生成图片]({inline_data_url})"
                else:
                    media_lines = [f"MEDIA:{ref}" for ref in media_refs] if media_refs else [f"MEDIA:{urls[0]}"]
                    reply_text = "\n".join(["已为你生成图片。", *media_lines])

        reply_path = Path(args.reply_file).expanduser() if args.reply_file else (out_dir / "reply.txt")
        reply_path.parent.mkdir(parents=True, exist_ok=True)
        reply_path.write_text(reply_text, encoding="utf-8")
        print(f"REPLY_FILE:{reply_path}")
    elif not args.emit_media_ref:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
