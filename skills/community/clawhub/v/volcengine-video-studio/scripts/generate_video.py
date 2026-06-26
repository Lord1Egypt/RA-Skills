#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional


def getenv(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def ensure_dir(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def safe_stem(text: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in text.strip())
    cleaned = "-".join(filter(None, cleaned.split("-")))
    return (cleaned[:48] or "video")


def build_submit_url(base: str) -> str:
    base = base.strip().rstrip("/")
    if not base:
        raise SystemExit("Missing VOLCENGINE_ENDPOINT / ARK_BASE_URL / OPENAI_BASE_URL")
    if base.endswith("/contents/generations/tasks"):
        return base
    if base.endswith("/api/v3"):
        return base + "/contents/generations/tasks"
    return base + "/api/v3/contents/generations/tasks"


def build_task_url(base: str, task_id: str) -> str:
    return build_submit_url(base) + "/" + urllib.parse.quote(task_id)


def local_file_to_data_url(path_str: str) -> str:
    path = pathlib.Path(path_str).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Local file not found: {path}")
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def normalize_media_value(value: str) -> str:
    if value.startswith("http://") or value.startswith("https://") or value.startswith("data:"):
        return value
    return local_file_to_data_url(value)


def add_text_content(items: List[Dict[str, Any]], text: str) -> None:
    if text.strip():
        items.append({"type": "text", "text": text.strip()})


def add_image_content(items: List[Dict[str, Any]], value: str) -> None:
    url = normalize_media_value(value)
    items.append({"type": "image_url", "image_url": {"url": url}})


def add_video_content(items: List[Dict[str, Any]], value: str) -> None:
    url = normalize_media_value(value)
    items.append({"type": "video_url", "video_url": {"url": url}})


def extract_status(payload: Dict[str, Any]) -> Optional[str]:
    for key in ("status", "state"):
        if key in payload and payload[key]:
            return str(payload[key])
    data = payload.get("data")
    if isinstance(data, dict):
        return extract_status(data)
    if isinstance(data, list) and data and isinstance(data[0], dict):
        return extract_status(data[0])
    return None


def extract_task_id(payload: Dict[str, Any]) -> Optional[str]:
    for key in ("task_id", "id", "taskId"):
        if key in payload and payload[key]:
            return str(payload[key])
    data = payload.get("data")
    if isinstance(data, dict):
        return extract_task_id(data)
    if isinstance(data, list) and data and isinstance(data[0], dict):
        return extract_task_id(data[0])
    return None


def walk_urls(node: Any, found: List[str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            lowered = str(key).lower()
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                if any(token in lowered for token in ["video", "file", "url", "output", "media", "cover"]):
                    found.append(value)
            else:
                walk_urls(value, found)
    elif isinstance(node, list):
        for item in node:
            walk_urls(item, found)


def download_file(url: str, out_dir: pathlib.Path, filename: str) -> pathlib.Path:
    ensure_dir(out_dir)
    out = out_dir / filename
    with urllib.request.urlopen(url, timeout=600) as resp:
        out.write_bytes(resp.read())
    return out


def request_json(req: urllib.request.Request, timeout: int) -> Dict[str, Any]:
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit and optionally wait for a Volcengine/ARK video generation task")
    parser.add_argument("prompt", nargs="?", default="", help="Main text prompt. Ignored when --content-json is provided.")
    parser.add_argument(
        "--model",
        default=getenv(
            "VOLCENGINE_VIDEO_MODEL",
            default="doubao-seedance-1-0-pro-fast-251015",
        ),
        help="Video model id. Recommended: doubao-seedance-1-0-pro-fast-251015 (default) or doubao-seedance-1-5-pro-251215.",
    )
    parser.add_argument("--endpoint", default=getenv("VOLCENGINE_VIDEO_ENDPOINT", "VOLCENGINE_ENDPOINT", "ARK_BASE_URL", "OPENAI_BASE_URL"))
    parser.add_argument("--api-key", default=getenv("VOLCENGINE_API_KEY", "ARK_API_KEY", "OPENAI_API_KEY"))
    parser.add_argument("--image", action="append", default=[], help="Reference image URL, data URL, or local path. Repeat flag for multiple images.")
    parser.add_argument("--video", action="append", default=[], help="Reference video URL, data URL, or local path (for draft/sample video workflows).")
    parser.add_argument("--content-json", default="", help="Raw JSON array/object for the API content field. Overrides prompt/image/video assembly.")
    parser.add_argument("--ratio", default=os.getenv("VOLCENGINE_VIDEO_RATIO", ""), help="Examples: 16:9, 9:16, 1:1, adaptive")
    parser.add_argument("--duration", type=int, default=int(os.getenv("VOLCENGINE_VIDEO_DURATION", "0")), help="Seconds, usually 2-12. If 0, omit.")
    parser.add_argument("--frames", type=int, default=int(os.getenv("VOLCENGINE_VIDEO_FRAMES", "0")), help="Alternative to duration.")
    parser.add_argument("--seed", type=int, default=int(os.getenv("VOLCENGINE_VIDEO_SEED", "0")), help="If 0, omit.")
    parser.add_argument("--resolution", default=os.getenv("VOLCENGINE_VIDEO_RESOLUTION", ""))
    parser.add_argument("--camera-fixed", default=os.getenv("VOLCENGINE_VIDEO_CAMERA_FIXED", "false"))
    parser.add_argument("--watermark", default=os.getenv("VOLCENGINE_VIDEO_WATERMARK", "false"))
    parser.add_argument("--callback-url", default=os.getenv("VOLCENGINE_VIDEO_CALLBACK_URL", ""))
    parser.add_argument("--task-id", default="", help="Skip submission and inspect an existing task id.")
    parser.add_argument("--wait", default=os.getenv("VOLCENGINE_VIDEO_WAIT", "true"), help="Whether to poll until completion.")
    parser.add_argument("--poll-interval", type=int, default=int(os.getenv("VOLCENGINE_VIDEO_POLL_INTERVAL", "8")))
    parser.add_argument("--timeout", type=int, default=int(os.getenv("VOLCENGINE_TIMEOUT", "900")))
    parser.add_argument("--download-results", default=os.getenv("VOLCENGINE_VIDEO_DOWNLOAD_RESULTS", "true"))
    parser.add_argument("--download-dir", default=os.getenv("VOLCENGINE_VIDEO_DOWNLOAD_DIR", str(pathlib.Path.home() / "Desktop" / "volcengine-videos")))
    parser.add_argument("--print-request", action="store_true", help="Print the assembled request body before submission.")
    return parser.parse_args()


def assemble_content(args: argparse.Namespace) -> Any:
    if args.content_json:
        parsed = json.loads(args.content_json)
        return parsed
    items: List[Dict[str, Any]] = []
    add_text_content(items, args.prompt)
    for image in args.image:
        add_image_content(items, image)
    for video in args.video:
        add_video_content(items, video)
    if not items:
        raise SystemExit("Provide a prompt and/or --image/--video, or pass --content-json.")
    return items


def assemble_payload(args: argparse.Namespace) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": args.model,
        "content": assemble_content(args),
    }
    if args.ratio:
        payload["ratio"] = args.ratio
    if args.duration > 0:
        payload["duration"] = args.duration
    if args.frames > 0:
        payload["frames"] = args.frames
    if args.seed > 0:
        payload["seed"] = args.seed
    if args.resolution:
        payload["resolution"] = args.resolution
    payload["camera_fixed"] = parse_bool(args.camera_fixed)
    payload["watermark"] = parse_bool(args.watermark)
    if args.callback_url:
        payload["callback_url"] = args.callback_url
    return payload


def make_headers(api_key: str) -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


def submit_task(args: argparse.Namespace, payload: Dict[str, Any]) -> Dict[str, Any]:
    req = urllib.request.Request(
        build_submit_url(args.endpoint),
        data=json.dumps(payload).encode("utf-8"),
        headers=make_headers(args.api_key),
        method="POST",
    )
    return request_json(req, min(args.timeout, 120))


def fetch_task(args: argparse.Namespace, task_id: str) -> Dict[str, Any]:
    req = urllib.request.Request(
        build_task_url(args.endpoint, task_id),
        headers=make_headers(args.api_key),
        method="GET",
    )
    return request_json(req, min(args.timeout, 120))


def finalize_result(args: argparse.Namespace, task_payload: Dict[str, Any], prompt_hint: str) -> Dict[str, Any]:
    urls: List[str] = []
    walk_urls(task_payload, urls)
    deduped_urls: List[str] = []
    seen = set()
    for url in urls:
        if url not in seen:
            seen.add(url)
            deduped_urls.append(url)

    downloads: List[str] = []
    if parse_bool(args.download_results) and deduped_urls:
        download_dir = pathlib.Path(args.download_dir).expanduser().resolve()
        stamp = int(time.time())
        stem = safe_stem(prompt_hint or extract_task_id(task_payload) or "video")
        run_dir = download_dir / f"{stamp}-{stem}"
        for idx, url in enumerate(deduped_urls, start=1):
            ext = pathlib.Path(url.split("?", 1)[0]).suffix or ".mp4"
            filename = f"{stamp}-{stem}-{idx}{ext}"
            downloads.append(str(download_file(url, run_dir, filename)))

    return {
        "ok": True,
        "task_id": extract_task_id(task_payload),
        "status": extract_status(task_payload),
        "videos": deduped_urls,
        "downloaded_files": downloads,
        "raw": task_payload,
    }


def main() -> int:
    args = parse_args()
    if not args.api_key:
        raise SystemExit("Missing API key. Set VOLCENGINE_API_KEY (or ARK_API_KEY / OPENAI_API_KEY).")
    if not args.endpoint:
        raise SystemExit("Missing endpoint. Set VOLCENGINE_VIDEO_ENDPOINT / VOLCENGINE_ENDPOINT / ARK_BASE_URL.")
    if not args.task_id and not args.model:
        raise SystemExit("Missing model. Set VOLCENGINE_VIDEO_MODEL / VOLCENGINE_MODEL / ARK_MODEL.")

    prompt_hint = args.prompt
    try:
        if args.task_id:
            latest = fetch_task(args, args.task_id)
        else:
            payload = assemble_payload(args)
            if args.print_request:
                print(json.dumps({"request": payload}, ensure_ascii=False, indent=2), file=sys.stderr)
            submit_response = submit_task(args, payload)
            task_id = extract_task_id(submit_response)
            if not task_id:
                print(json.dumps({"ok": False, "error": "No task id returned", "raw": submit_response}, ensure_ascii=False, indent=2))
                return 1
            latest = submit_response
            latest.setdefault("task_id", task_id)

        if not parse_bool(args.wait):
            print(json.dumps({"ok": True, "task_id": extract_task_id(latest), "status": extract_status(latest), "raw": latest}, ensure_ascii=False, indent=2))
            return 0

        task_id = extract_task_id(latest)
        if not task_id:
            print(json.dumps({"ok": False, "error": "No task id available for polling", "raw": latest}, ensure_ascii=False, indent=2))
            return 1

        deadline = time.time() + args.timeout
        terminal_ok = {"succeeded", "success", "completed", "done", "finished"}
        terminal_fail = {"failed", "error", "cancelled", "canceled", "deleted", "timeout"}
        while True:
            latest = fetch_task(args, task_id)
            status = (extract_status(latest) or "").strip().lower()
            if status in terminal_ok:
                print(json.dumps(finalize_result(args, latest, prompt_hint), ensure_ascii=False, indent=2))
                return 0
            if status in terminal_fail:
                print(json.dumps({"ok": False, "task_id": task_id, "status": extract_status(latest), "raw": latest}, ensure_ascii=False, indent=2))
                return 1
            if time.time() >= deadline:
                print(json.dumps({"ok": False, "task_id": task_id, "status": extract_status(latest), "error": f"Polling timed out after {args.timeout}s", "raw": latest}, ensure_ascii=False, indent=2))
                return 1
            time.sleep(max(1, args.poll_interval))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"ok": False, "status": e.code, "error": body}, ensure_ascii=False, indent=2))
        return 1
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"Invalid JSON: {e}"}, ensure_ascii=False, indent=2))
        return 1
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
