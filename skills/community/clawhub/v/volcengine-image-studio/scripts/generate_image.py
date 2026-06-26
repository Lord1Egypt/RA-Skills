#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import pathlib
import sys
import time
import subprocess
import urllib.error
import urllib.request


def parse_sse(raw: str):
    events = []
    current = {}
    for line in raw.splitlines():
        if not line.strip():
            if current:
                events.append(current)
                current = {}
            continue
        if line.startswith("event:"):
            current["event"] = line.split(":", 1)[1].strip()
        elif line.startswith("data:"):
            payload = line.split(":", 1)[1].strip()
            try:
                current.setdefault("data", []).append(json.loads(payload))
            except json.JSONDecodeError:
                current.setdefault("data", []).append(payload)
    if current:
        events.append(current)
    return events


def getenv(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


def ensure_dir(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def safe_stem(text: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in text.strip())
    cleaned = "-".join(filter(None, cleaned.split("-")))
    return (cleaned[:48] or "image")


def build_url(base: str) -> str:
    base = base.strip().rstrip("/")
    if not base:
        raise SystemExit("Missing VOLCENGINE_ENDPOINT / ARK_BASE_URL / OPENAI_BASE_URL")
    if base.endswith("/images/generations"):
        return base
    if base.endswith("/api/v3"):
        return base + "/images/generations"
    if base.endswith("/v1"):
        return base + "/images/generations"
    return base + "/v1/images/generations"


def parse_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def local_file_to_data_url(path_str: str) -> str:
    path = pathlib.Path(path_str).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Local image not found: {path}")
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def normalize_image_value(value: str) -> str:
    if value.startswith("http://") or value.startswith("https://") or value.startswith("data:"):
        return value
    return local_file_to_data_url(value)


def collect_images(image_args, image_file: str):
    values = []
    for item in image_args or []:
        if item:
            values.extend([part.strip() for part in item.split(",") if part.strip()])
    if image_file:
        path = pathlib.Path(image_file).expanduser()
        if not path.exists():
            raise SystemExit(f"Image list file not found: {path}")
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                values.append(line)
    return [normalize_image_value(v) for v in values]


def download_to_dir(url: str, out_dir: pathlib.Path, filename: str):
    ensure_dir(out_dir)
    out = out_dir / filename
    with urllib.request.urlopen(url, timeout=180) as r:
        out.write_bytes(r.read())
    return out


def build_batch_dir(base_dir: pathlib.Path, stem: str, stamp: int) -> pathlib.Path:
    folder = base_dir / f"{stamp}-{stem}"
    ensure_dir(folder)
    return folder


def reveal_in_finder(path: pathlib.Path) -> None:
    try:
        subprocess.run(["open", str(path)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate images via Volcengine/ARK-compatible image API")
    parser.add_argument("prompt")
    parser.add_argument("--model", default=getenv("VOLCENGINE_MODEL", "ARK_MODEL", "OPENAI_IMAGE_MODEL"))
    parser.add_argument("--endpoint", default=getenv("VOLCENGINE_ENDPOINT", "ARK_BASE_URL", "OPENAI_BASE_URL"))
    parser.add_argument("--api-key", default=getenv("VOLCENGINE_API_KEY", "ARK_API_KEY", "OPENAI_API_KEY"))
    parser.add_argument("--size", default=os.getenv("VOLCENGINE_IMAGE_SIZE", "1024x1024"))
    parser.add_argument("--n", type=int, default=int(os.getenv("VOLCENGINE_IMAGE_COUNT", "1")))
    parser.add_argument("--quality", default=os.getenv("VOLCENGINE_IMAGE_QUALITY", "standard"))
    parser.add_argument("--response-format", default=os.getenv("VOLCENGINE_RESPONSE_FORMAT", "url"))
    parser.add_argument("--sequential-image-generation", default=os.getenv("VOLCENGINE_SEQUENTIAL_IMAGE_GENERATION", "disabled"))
    parser.add_argument("--sequential-max-images", type=int, default=int(os.getenv("VOLCENGINE_SEQUENTIAL_MAX_IMAGES", "0")))
    parser.add_argument("--watermark", default=os.getenv("VOLCENGINE_WATERMARK", "true"))
    parser.add_argument("--stream", default=os.getenv("VOLCENGINE_STREAM", "false"))
    parser.add_argument("--image", action="append", default=[], help="Reference image URL, data URL, or local path. Repeat flag or pass comma-separated values.")
    parser.add_argument("--image-file", default=os.getenv("VOLCENGINE_IMAGE_FILE", ""), help="Text file with one reference image URL/path per line.")
    parser.add_argument("--output-dir", default=os.getenv("VOLCENGINE_OUTPUT_DIR", "generated-images"))
    parser.add_argument("--download-dir", default=os.getenv("VOLCENGINE_DOWNLOAD_DIR", str(pathlib.Path.home() / "Desktop")), help="Directory for auto-downloaded result images.")
    parser.add_argument("--download-results", default=os.getenv("VOLCENGINE_DOWNLOAD_RESULTS", "true"), help="Whether to auto-download URL results.")
    parser.add_argument("--download-folder-per-run", default=os.getenv("VOLCENGINE_DOWNLOAD_FOLDER_PER_RUN", "auto"), help="auto|true|false. When auto, multi-image runs create a new folder.")
    parser.add_argument("--open-download-folder", default=os.getenv("VOLCENGINE_OPEN_DOWNLOAD_FOLDER", "auto"), help="auto|true|false. When auto, open Finder for batch download folders.")
    parser.add_argument("--timeout", type=int, default=int(os.getenv("VOLCENGINE_TIMEOUT", "120")))
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("Missing API key. Set VOLCENGINE_API_KEY (or ARK_API_KEY / OPENAI_API_KEY).")
    if not args.model:
        raise SystemExit("Missing model. Set VOLCENGINE_MODEL (or ARK_MODEL / OPENAI_IMAGE_MODEL).")

    url = build_url(args.endpoint)
    output_dir = pathlib.Path(args.output_dir).expanduser().resolve()
    ensure_dir(output_dir)
    download_dir = pathlib.Path(args.download_dir).expanduser().resolve()
    images = collect_images(args.image, args.image_file)

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "n": args.n,
        "quality": args.quality,
        "response_format": args.response_format,
        "sequential_image_generation": args.sequential_image_generation,
        "stream": parse_bool(args.stream),
        "watermark": parse_bool(args.watermark),
    }
    if images:
        payload["image"] = images[0] if len(images) == 1 else images
    if args.sequential_max_images > 0:
        payload["sequential_image_generation_options"] = {"max_images": args.sequential_max_images}

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {args.api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            raw = resp.read().decode("utf-8")
            status = resp.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"ok": False, "status": e.code, "error": body, "request": payload}, ensure_ascii=False, indent=2))
        return 1
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e), "request": payload}, ensure_ascii=False, indent=2))
        return 1

    try:
        data = json.loads(raw)
        items = data.get("data") or []
    except json.JSONDecodeError:
        if args.stream and "event:" in raw and "data:" in raw:
            events = parse_sse(raw)
            items = []
            for evt in events:
                for datum in evt.get("data", []):
                    if isinstance(datum, dict):
                        items.append(datum)
            data = {"events": events}
        else:
            print(json.dumps({"ok": False, "status": status, "error": "Non-JSON response", "body": raw[:1000], "request": payload}, ensure_ascii=False, indent=2))
            return 1

    saved = []
    stamp = int(time.time())
    stem = safe_stem(args.prompt)
    auto_download = parse_bool(args.download_results)
    folder_mode = str(args.download_folder_per_run).strip().lower()
    use_folder = folder_mode == "true" or (folder_mode == "auto" and len(items) > 1)
    effective_download_dir = build_batch_dir(download_dir, stem, stamp) if (auto_download and use_folder) else download_dir

    for idx, item in enumerate(items, start=1):
        if item.get("b64_json"):
            out = output_dir / f"{stamp}-{stem}-{idx}.png"
            out.write_bytes(base64.b64decode(item["b64_json"]))
            saved.append({"type": "file", "path": str(out)})
        elif item.get("url"):
            entry = {"type": "url", "url": item["url"]}
            if auto_download:
                ext = pathlib.Path(item["url"].split("?", 1)[0]).suffix or ".png"
                filename = f"{stamp}-{stem}-{idx}{ext}"
                try:
                    downloaded = download_to_dir(item["url"], effective_download_dir, filename)
                    entry["downloaded_path"] = str(downloaded)
                except Exception as e:
                    entry["download_error"] = str(e)
            saved.append(entry)

    open_mode = str(args.open_download_folder).strip().lower()
    should_open = auto_download and (
        open_mode == "true" or (open_mode == "auto" and use_folder)
    )
    if should_open:
        reveal_in_finder(effective_download_dir)

    result = {
        "ok": True,
        "request": {
            "url": url,
            "model": args.model,
            "size": args.size,
            "n": args.n,
            "quality": args.quality,
            "reference_images": len(images),
            "sequential_image_generation": args.sequential_image_generation,
            "sequential_max_images": args.sequential_max_images,
            "download_results": auto_download,
            "download_dir": str(download_dir),
            "effective_download_dir": str(effective_download_dir) if auto_download else None,
            "download_folder_per_run": folder_mode,
            "open_download_folder": open_mode,
        },
        "saved": saved,
        "raw": data if not saved else None,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
