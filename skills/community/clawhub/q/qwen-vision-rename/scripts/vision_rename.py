#!/usr/bin/env python3

"""
Vision rename CLI (OpenAI-compatible multimodal API)

Use cases:
- describe a single image
- batch-generate filename titles for a directory
- apply renames with rollback file
"""

import argparse
import base64
import datetime as dt
import hashlib
import ipaddress
import json
import mimetypes
import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
from urllib.parse import urlparse

import requests

try:
    from PIL import Image
except Exception:
    Image = None


DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "qwen-vl-max-latest"
DEFAULT_MEDIA_OUTBOUND_DIR = "~/.openclaw/media/outbound"
OPENCLAW_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
PUBLIC_MEDIA_BASE_URL_FILE = Path.home() / ".openclaw" / "media" / "public_base_url.txt"
DEFAULT_PROMPT = (
    "你是图片文件重命名助手。"
    "请识别图片类型和主题，并只输出严格 JSON：{\"type\":\"类型\",\"title\":\"主题\"}。"
    "type 示例：邀请函、海报、聊天截图、人物照、宠物照、风景照、商品图、证件照、菜单、其他。"
    "title 要具体，4到12个汉字，不要标点，不要扩展名，不要解释。"
    "不要输出 JSON 以外的任何内容。"
)
IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".heic",
    ".heif",
}
PLACEHOLDER_API_KEYS = {
    "",
    "your_api_key",
    "your-api-key",
    "sk-your_api_key",
    "none",
    "null",
}
_OPENCLAW_CONFIG_CACHE = None  # type: Dict[str, Any]


def load_openclaw_config() -> Dict[str, Any]:
    global _OPENCLAW_CONFIG_CACHE
    if _OPENCLAW_CONFIG_CACHE is not None:
        return _OPENCLAW_CONFIG_CACHE

    try:
        _OPENCLAW_CONFIG_CACHE = json.loads(OPENCLAW_CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        _OPENCLAW_CONFIG_CACHE = {}
    return _OPENCLAW_CONFIG_CACHE


def get_openclaw_skill_entry(skill_name: str) -> Dict[str, Any]:
    config = load_openclaw_config()
    entries = config.get("skills", {}).get("entries", {})
    entry = entries.get(skill_name, {})
    return entry if isinstance(entry, dict) else {}


def get_openclaw_skill_env(skill_name: str) -> Dict[str, str]:
    entry = get_openclaw_skill_entry(skill_name)
    env = entry.get("env", {})
    return env if isinstance(env, dict) else {}


def first_non_empty(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def is_placeholder_api_key(value: str) -> bool:
    lowered = value.strip().lower()
    return lowered in PLACEHOLDER_API_KEYS or "your_api_key" in lowered


def resolve_runtime_api_key() -> str:
    env_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
    if env_key and not is_placeholder_api_key(env_key):
        return env_key

    configured = get_openclaw_skill_entry("qwen-vision-rename").get("apiKey", "")
    if isinstance(configured, str) and configured.strip() and not is_placeholder_api_key(configured):
        return configured.strip()

    return ""


def resolve_runtime_base_url(cli_value: str) -> str:
    skill_env = get_openclaw_skill_env("qwen-vision-rename")
    return first_non_empty(
        cli_value,
        os.getenv("DASHSCOPE_BASE_URL", ""),
        os.getenv("OPENAI_BASE_URL", ""),
        skill_env.get("DASHSCOPE_BASE_URL", ""),
        DEFAULT_BASE_URL,
    )


def resolve_runtime_model(cli_value: str) -> str:
    skill_env = get_openclaw_skill_env("qwen-vision-rename")
    return first_non_empty(
        cli_value,
        os.getenv("DASHSCOPE_VISION_MODEL", ""),
        os.getenv("OPENCLAW_IMAGE_UNDERSTAND_MODEL", ""),
        skill_env.get("DASHSCOPE_VISION_MODEL", ""),
        DEFAULT_MODEL,
    )


def resolve_image_mode() -> str:
    skill_env = get_openclaw_skill_env("qwen-vision-rename")
    mode = first_non_empty(
        os.getenv("OPENCLAW_VISION_IMAGE_MODE", ""),
        skill_env.get("OPENCLAW_VISION_IMAGE_MODE", ""),
    ).lower()
    if mode in ("auto", "data", "url"):
        return mode
    return "auto"


def resolve_media_base_url() -> str:
    vision_env = get_openclaw_skill_env("qwen-vision-rename")
    image_env = get_openclaw_skill_env("qwen-image")
    file_value = ""
    try:
        if PUBLIC_MEDIA_BASE_URL_FILE.is_file():
            file_value = PUBLIC_MEDIA_BASE_URL_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        file_value = ""
    return first_non_empty(
        os.getenv("OPENCLAW_VISION_IMAGE_BASE_URL", ""),
        os.getenv("OPENCLAW_MEDIA_BASE_URL", ""),
        vision_env.get("OPENCLAW_VISION_IMAGE_BASE_URL", ""),
        vision_env.get("OPENCLAW_MEDIA_BASE_URL", ""),
        image_env.get("OPENCLAW_MEDIA_BASE_URL", ""),
        file_value,
    )


def resolve_media_outbound_dir() -> Path:
    vision_env = get_openclaw_skill_env("qwen-vision-rename")
    image_env = get_openclaw_skill_env("qwen-image")
    raw = first_non_empty(
        os.getenv("OPENCLAW_VISION_IMAGE_PUBLISH_DIR", ""),
        os.getenv("OPENCLAW_MEDIA_OUTBOUND_DIR", ""),
        vision_env.get("OPENCLAW_VISION_IMAGE_PUBLISH_DIR", ""),
        vision_env.get("OPENCLAW_MEDIA_OUTBOUND_DIR", ""),
        image_env.get("OPENCLAW_MEDIA_OUTBOUND_DIR", ""),
        DEFAULT_MEDIA_OUTBOUND_DIR,
    )
    return Path(raw).expanduser()


def has_public_media_base_url(value: str) -> bool:
    if not value:
        return False

    parsed = urlparse(value)
    host = parsed.hostname or ""
    if parsed.scheme not in ("http", "https") or not host:
        return False
    if host == "localhost":
        return False

    try:
        ip = ipaddress.ip_address(host)
        return not (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        )
    except ValueError:
        return True


def endpoint_requires_public_image_url(base_url: str) -> bool:
    host = urlparse(base_url).hostname or ""
    return host in {"api.chipltech.com", "openapi.chipltech.com"}


def publish_local_image(path: Path) -> str:
    media_base_url = resolve_media_base_url()
    if not has_public_media_base_url(media_base_url):
        return ""

    source_path = path
    prepared_path = prepare_image_for_remote_fetch(path)
    if prepared_path is not None:
        source_path = prepared_path

    publish_root = resolve_media_outbound_dir() / "vision-input"
    publish_root.mkdir(parents=True, exist_ok=True)

    stat = source_path.stat()
    mtime_ns = getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1000000000))
    digest_src = "{}:{}:{}".format(source_path.resolve(), stat.st_size, mtime_ns)
    digest = hashlib.sha1(digest_src.encode("utf-8")).hexdigest()[:10]
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    suffix = source_path.suffix.lower() or ".bin"
    target_name = "vision-{}-{}{}".format(stamp, digest, suffix)
    target_path = publish_root / target_name
    if not target_path.exists():
        shutil.copy2(str(source_path), str(target_path))

    return media_base_url.rstrip("/") + "/vision-input/" + target_name


def prepare_image_for_remote_fetch(path: Path) -> Path:
    if Image is None:
        return path

    try:
        with Image.open(str(path)) as img:
            img.load()
            width, height = img.size
            max_edge = max(width, height)
            file_size = path.stat().st_size
            if file_size <= 700 * 1024 and max_edge <= 1024:
                return path

            if img.mode not in ("RGB", "L"):
                converted = Image.new("RGB", img.size, (255, 255, 255))
                converted.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[-1])
                img = converted
            elif img.mode == "L":
                img = img.convert("RGB")
            else:
                img = img.copy()

            img.thumbnail((1024, 1024), Image.LANCZOS)
            cache_root = resolve_media_outbound_dir() / "vision-input-cache"
            cache_root.mkdir(parents=True, exist_ok=True)
            stat = path.stat()
            mtime_ns = getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1000000000))
            digest_src = "{}:{}:{}".format(path.resolve(), stat.st_size, mtime_ns)
            digest = hashlib.sha1(digest_src.encode("utf-8")).hexdigest()[:16]
            optimized_path = cache_root / ("optimized-{}.jpg".format(digest))
            if not optimized_path.exists():
                img.save(str(optimized_path), format="JPEG", quality=82, optimize=True)
            return optimized_path
    except Exception:
        return path


def load_dotenv_files(paths: List[Path]) -> None:
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
            if quoted:
                value = value[1:-1]
            elif " #" in value:
                value = value.split(" #", 1)[0].rstrip()

            if key not in os.environ or not os.environ.get(key, "").strip():
                os.environ[key] = value


def resolve_dotenv_paths() -> List[Path]:
    candidates = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent / ".env",
    ]
    dedup = []  # type: List[Path]
    seen = set()  # type: Set[str]
    for candidate in candidates:
        resolved = str(candidate.resolve())
        if resolved in seen:
            continue
        seen.add(resolved)
        dedup.append(candidate)
    return dedup


def is_http_or_data_url(value: str) -> bool:
    lowered = value.lower().strip()
    return lowered.startswith("http://") or lowered.startswith("https://") or lowered.startswith("data:image/")


def local_image_to_data_url(path_str: str) -> str:
    path = Path(path_str).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Image file not found: {path}")

    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = "image/png"

    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def normalize_image_input(value: str, base_url: str) -> str:
    val = value.strip()
    if is_http_or_data_url(val):
        return val

    path = Path(val).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Image file not found: {path}")

    prepared_path = prepare_image_for_remote_fetch(path)
    image_mode = resolve_image_mode()
    if image_mode == "url":
        published_url = publish_local_image(prepared_path)
        if published_url:
            return published_url
        media_base_url = resolve_media_base_url()
        if media_base_url and not has_public_media_base_url(media_base_url):
            raise RuntimeError(
                "Configured OPENCLAW_MEDIA_BASE_URL is not publicly reachable: {}. "
                "Use a public http(s) URL or switch back to qwen-vl-max-latest.".format(media_base_url)
            )
        raise RuntimeError(
            "Current vision endpoint requires local images to be reachable by public URL. "
            "Configure OPENCLAW_MEDIA_BASE_URL and OPENCLAW_MEDIA_OUTBOUND_DIR, or switch back to qwen-vl-max-latest."
        )

    return local_image_to_data_url(str(prepared_path))


def parse_openai_content(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []  # type: List[str]
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "text" and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts).strip()

    return ""


def call_vision_api(
    *,
    base_url: str,
    api_key: str,
    model: str,
    image: str,
    prompt: str,
    timeout: int,
) -> str:
    endpoint = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image}},
                ],
            }
        ],
        "temperature": 0,
    }

    resp = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )

    if resp.status_code != 200:
        body = resp.text
        try:
            data = resp.json()
            err = data.get("error", {}) if isinstance(data, dict) else {}
            message = err.get("message") or data.get("message") or body
            code = err.get("code") or data.get("code") or "UnknownError"
            raise RuntimeError(f"API error {resp.status_code} [{code}]: {message}")
        except ValueError:
            raise RuntimeError(f"API error {resp.status_code}: {body}")

    data = resp.json()
    if isinstance(data, dict) and not data.get("choices") and ("code" in data or "msg" in data or "message" in data):
        code = data.get("code", "UnknownError")
        message = data.get("msg") or data.get("message") or json.dumps(data, ensure_ascii=False)[:800]
        raise RuntimeError("API error [{}]: {}".format(code, message))

    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        raise RuntimeError(f"Unexpected response: {json.dumps(data, ensure_ascii=False)[:800]}")

    message = choices[0].get("message", {})
    text = parse_openai_content(message.get("content"))
    if not text:
        raise RuntimeError(f"No text content in response: {json.dumps(data, ensure_ascii=False)[:800]}")

    return text


def extract_title(raw_text: str, fallback: str) -> str:
    text = raw_text.strip()
    if not text:
        return fallback

    line = ""
    for row in text.splitlines():
        row = row.strip()
        if row:
            line = row
            break
    if not line:
        line = text

    # Remove common wrappers.
    line = line.strip().strip("`\"' ")
    line = re.sub(r"^(title|filename|name|image description|description)\s*[:：-]\s*", "", line, flags=re.I)

    # If the model returns markdown list item or prefix markers.
    line = re.sub(r"^[\-\*\d\.\)\s]+", "", line)

    if not line:
        return fallback

    return line


def extract_type_and_title(raw_text: str, fallback: str) -> Tuple[str, str]:
    text = raw_text.strip()
    if not text:
        return "", fallback

    candidates = [text]  # type: List[str]
    code_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.I | re.S)
    if code_block:
        candidates.insert(0, code_block.group(1))

    first_obj = re.search(r"\{.*?\}", text, flags=re.S)
    if first_obj:
        candidates.append(first_obj.group(0))

    for candidate in candidates:
        try:
            data = json.loads(candidate)
            if not isinstance(data, dict):
                continue
            image_type = str(data.get("type", "")).strip()
            title = str(data.get("title", "")).strip()
            if image_type or title:
                return image_type, title or fallback
        except Exception:
            continue

    line = extract_title(text, fallback)
    parts = re.split(r"\s*[-—_:：]\s*", line, maxsplit=1)
    if len(parts) == 2 and parts[0].strip() and parts[1].strip():
        return parts[0].strip(), parts[1].strip()

    return "", line


def sanitize_filename_stem(value: str, *, max_chars: int) -> str:
    stem = value
    stem = re.sub(r"[\\/:*?\"<>|\r\n\t]", " ", stem)
    stem = re.sub(r"\s+", " ", stem).strip(" ._-")
    if not stem:
        stem = "untitled"
    if max_chars > 0 and len(stem) > max_chars:
        stem = stem[:max_chars].rstrip(" ._-")
    if not stem:
        stem = "untitled"
    return stem


def compose_stem(image_type: str, title: str, fallback: str, max_stem_chars: int) -> str:
    type_clean = sanitize_filename_stem(image_type, max_chars=10) if image_type else ""
    title_clean = sanitize_filename_stem(title, max_chars=max_stem_chars) if title else ""

    if type_clean and title_clean:
        stem = f"{type_clean}-{title_clean}"
    elif title_clean:
        stem = title_clean
    elif type_clean:
        stem = type_clean
    else:
        stem = sanitize_filename_stem(fallback, max_chars=max_stem_chars)

    return sanitize_filename_stem(stem, max_chars=max_stem_chars)


def collect_images(directory: Path, recursive: bool) -> List[Path]:
    if recursive:
        items = [p for p in directory.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS]
    else:
        items = [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS]
    return sorted(items, key=lambda p: p.name.lower())


def resolve_target_directory(dir_arg: str) -> Path:
    if dir_arg.strip():
        root = Path(dir_arg).expanduser().resolve()
        if not root.is_dir():
            raise SystemExit(f"Directory not found: {root}")
        return root

    candidates = []  # type: List[Path]
    env_dir = os.getenv("OPENCLAW_RENAME_DEFAULT_DIR", "").strip()
    if env_dir:
        candidates.append(Path(env_dir).expanduser())

    home = Path.home()
    candidates.extend([home / "图片", home / "Pictures"])

    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()

    tried = ", ".join(str(path) for path in candidates) if candidates else "(none)"
    raise SystemExit(
        "Directory not provided and no default image directory found. "
        f"Tried: {tried}. Use --dir or set OPENCLAW_RENAME_DEFAULT_DIR."
    )


def unique_target_name(stem: str, suffix: str, used_names: Set[str]) -> str:
    candidate = f"{stem}{suffix}"
    if candidate.lower() not in used_names:
        used_names.add(candidate.lower())
        return candidate

    i = 2
    while True:
        candidate = f"{stem}-{i:02d}{suffix}"
        key = candidate.lower()
        if key not in used_names:
            used_names.add(key)
            return candidate
        i += 1


def build_plan(
    *,
    files: List[Path],
    model: str,
    base_url: str,
    api_key: str,
    prompt: str,
    timeout: int,
    max_stem_chars: int,
    fail_fast: bool,
) -> Dict[str, Any]:
    used_names = {p.name.lower() for p in files}
    items = []  # type: List[Dict[str, Any]]

    for file in files:
        source = str(file)
        suffix = file.suffix.lower() or ".jpg"
        try:
            image_ref = normalize_image_input(source, base_url)
            raw_text = call_vision_api(
                base_url=base_url,
                api_key=api_key,
                model=model,
                image=image_ref,
                prompt=prompt,
                timeout=timeout,
            )
            image_type, title = extract_type_and_title(raw_text, fallback=file.stem)
            stem = compose_stem(image_type, title, file.stem, max_stem_chars=max_stem_chars)
            target_name = unique_target_name(stem, suffix, used_names)
            target = str(file.with_name(target_name))
            action = "rename" if Path(target).name != file.name else "skip_same"
            items.append(
                {
                    "source": source,
                    "target": target,
                    "action": action,
                    "type": image_type,
                    "title": title,
                    "stem": stem,
                    "raw": raw_text,
                    "error": "",
                }
            )
        except Exception as exc:
            if fail_fast:
                raise
            items.append(
                {
                    "source": source,
                    "target": source,
                    "action": "skip_error",
                    "type": "",
                    "title": file.stem,
                    "stem": file.stem,
                    "raw": "",
                    "error": str(exc),
                }
            )

    rename_count = sum(1 for item in items if item["action"] == "rename")
    error_count = sum(1 for item in items if item["action"] == "skip_error")
    same_count = sum(1 for item in items if item["action"] == "skip_same")

    return {
        "created_at": dt.datetime.now().isoformat(),
        "model": model,
        "base_url": base_url,
        "prompt": prompt,
        "items": items,
        "summary": {
            "total": len(items),
            "rename": rename_count,
            "skip_same": same_count,
            "skip_error": error_count,
        },
    }


def apply_plan(plan: Dict[str, Any]) -> List[Dict[str, str]]:
    rollback = []  # type: List[Dict[str, str]]

    for item in plan.get("items", []):
        if item.get("action") != "rename":
            continue

        src = Path(item["source"]).expanduser()
        dst = Path(item["target"]).expanduser()

        if not src.exists():
            raise FileNotFoundError(f"Source missing: {src}")
        if dst.exists() and dst.resolve() != src.resolve():
            raise FileExistsError(f"Target already exists: {dst}")

        src.rename(dst)
        rollback.append({"from": str(dst), "to": str(src)})

    return rollback


def cmd_describe(args: argparse.Namespace) -> int:
    load_dotenv_files(resolve_dotenv_paths())

    api_key = resolve_runtime_api_key()
    if not api_key:
        raise SystemExit("Missing DASHSCOPE_API_KEY")

    base_url = resolve_runtime_base_url(args.base_url)
    model = resolve_runtime_model(args.model)

    text = call_vision_api(
        base_url=base_url,
        api_key=api_key,
        model=model,
        image=normalize_image_input(args.image, base_url),
        prompt=args.prompt,
        timeout=args.timeout,
    )

    image_type, title = extract_type_and_title(text, fallback="untitled")
    stem = compose_stem(image_type, title, "untitled", max_stem_chars=args.max_stem_chars)
    result = {"image": args.image, "type": image_type, "title": title, "stem": stem, "raw": text, "model": model}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_rename_dir(args: argparse.Namespace) -> int:
    load_dotenv_files(resolve_dotenv_paths())

    api_key = resolve_runtime_api_key()
    if not api_key:
        raise SystemExit("Missing DASHSCOPE_API_KEY")

    base_url = resolve_runtime_base_url(args.base_url)
    model = resolve_runtime_model(args.model)

    root = resolve_target_directory(args.dir)

    files = collect_images(root, recursive=args.recursive)
    if args.limit > 0:
        files = files[: args.limit]

    if not files:
        raise SystemExit("No image files found")

    plan = build_plan(
        files=files,
        model=model,
        base_url=base_url,
        api_key=api_key,
        prompt=args.prompt,
        timeout=args.timeout,
        max_stem_chars=args.max_stem_chars,
        fail_fast=args.fail_fast,
    )

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    plan_path = Path(args.plan_file).expanduser() if args.plan_file else (root / f"rename-plan-{stamp}.json")
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    rollback_path = ""
    applied = 0
    if args.apply:
        rollback = apply_plan(plan)
        applied = len(rollback)
        rb = {"created_at": dt.datetime.now().isoformat(), "items": rollback}
        rb_path = root / f"rename-rollback-{stamp}.json"
        rb_path.write_text(json.dumps(rb, ensure_ascii=False, indent=2), encoding="utf-8")
        rollback_path = str(rb_path)

    output = {
        "mode": "apply" if args.apply else "dry-run",
        "directory": str(root),
        "plan_file": str(plan_path),
        "rollback_file": rollback_path,
        "summary": plan.get("summary", {}),
        "applied": applied,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


def cmd_rollback(args: argparse.Namespace) -> int:
    path = Path(args.rollback_file).expanduser().resolve()
    if not path.is_file():
        raise SystemExit(f"Rollback file not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("items", [])
    restored = 0

    for item in reversed(items):
        src = Path(item["from"]).expanduser()
        dst = Path(item["to"]).expanduser()

        if not src.exists():
            continue
        if dst.exists() and dst.resolve() != src.resolve():
            raise FileExistsError(f"Rollback target already exists: {dst}")

        src.rename(dst)
        restored += 1

    print(json.dumps({"rollback_file": str(path), "restored": restored}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Vision describe and batch rename tool")
    parser.add_argument(
        "--base-url",
        default="",
        help="OpenAI-compatible base URL",
    )
    parser.add_argument(
        "--model",
        default="",
        help="Vision model id",
    )
    parser.add_argument("--timeout", type=int, default=120, help="HTTP timeout in seconds")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt for image understanding")
    parser.add_argument("--max-stem-chars", type=int, default=24, help="Max filename stem chars")

    sub = parser.add_subparsers(dest="mode")

    p_describe = sub.add_parser("describe", help="Describe one image and output suggested title")
    p_describe.add_argument("--image", required=True, help="Image path, url, or data URL")

    p_rename = sub.add_parser("rename-dir", help="Batch plan or apply renames for a directory")
    p_rename.add_argument("--dir", default="", help="Target directory (optional if default image dir exists)")
    p_rename.add_argument("--recursive", action="store_true", help="Recursively scan directory")
    p_rename.add_argument("--limit", type=int, default=0, help="Limit number of files (0 = all)")
    p_rename.add_argument("--fail-fast", action="store_true", help="Stop on first image API error")
    p_rename.add_argument("--apply", action="store_true", help="Apply rename operations")
    p_rename.add_argument("--plan-file", default="", help="Optional path for generated plan json")

    p_rollback = sub.add_parser("rollback", help="Rollback applied rename using rollback json")
    p_rollback.add_argument("--rollback-file", required=True, help="Path to rollback json")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not getattr(args, "mode", None):
        parser.error("a subcommand is required")

    if args.mode == "describe":
        return cmd_describe(args)
    if args.mode == "rename-dir":
        return cmd_rename_dir(args)
    if args.mode == "rollback":
        return cmd_rollback(args)

    raise SystemExit(f"Unknown mode: {args.mode}")


if __name__ == "__main__":
    raise SystemExit(main())
