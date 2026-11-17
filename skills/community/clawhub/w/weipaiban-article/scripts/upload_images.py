#!/usr/bin/env python3
"""把本地图片或远程 URL 上传到微排版素材库，返回 CDN 永久链接。

本地文件走 `POST {WEIPAIBAN_API_BASE}/api/v1/assets/upload`（multipart `file`）。
http(s) URL 走 `POST {WEIPAIBAN_API_BASE}/api/v1/assets/fetch`（JSON `{ "url" }`）。
两端均按文件内容 SHA1 去重：相同图片重复上传返回已有记录，重试安全。

鉴权：`Authorization: Bearer <sk-...>`，token 取自 `WEIPAIBAN_API_KEY`。
不要求 admin。密钥只发往 https://weipaiban.cn（含子域）或本机
localhost / 127.0.0.1 / ::1。

用法示例：

    python3 upload_images.py --file ./a.png --url https://example.com/b.jpg

    python3 upload_images.py --dir ./images --out /tmp/weipaiban-upload-result.json

预览（不发送请求）：

    python3 upload_images.py --dry-run --file ./a.png --dir ./images
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import ssl
import sys
import time
import uuid
import urllib.error
import urllib.request
from pathlib import Path

from api_base import (
    build_ssl_context,
    invalid_api_key_message,
    missing_api_key_message,
    validate_api_base,
)

REQUEST_TIMEOUT = 30
RATE_LIMIT_SLEEP = 2
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}


def env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return value if value not in (None, "") else default


def is_http_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def guess_content_type(path: Path) -> str:
    content_type, _ = mimetypes.guess_type(path.name)
    return content_type or "application/octet-stream"


def encode_multipart_file(path: Path) -> tuple[bytes, str]:
    boundary = uuid.uuid4().hex
    filename = path.name.replace("\\", "\\\\").replace('"', '\\"')
    content_type = guess_content_type(path)
    data = path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n"
        "\r\n"
    ).encode("utf-8") + data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    return body, f"multipart/form-data; boundary={boundary}"


def parse_asset_response(payload: object) -> dict:
    if not isinstance(payload, dict):
        return {"status": "failed", "error": "响应非 JSON 对象"}

    error = payload.get("error")
    if error:
        if isinstance(error, dict):
            message = error.get("message") or json.dumps(error, ensure_ascii=False)
        else:
            message = str(error)
        return {"status": "failed", "error": message}

    data = payload.get("data")
    if not isinstance(data, dict) or not data.get("src"):
        return {"status": "failed", "error": "响应缺少 data.src"}

    return {
        "status": "uploaded",
        "id": data.get("id"),
        "src": data.get("src"),
        "width": data.get("width"),
        "height": data.get("height"),
        "title": data.get("title"),
        "size": data.get("size"),
    }


def collect_dir_files(directory: Path, recursive: bool) -> list[Path]:
    iterator = directory.rglob("*") if recursive else directory.iterdir()
    files = [
        path
        for path in iterator
        if path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in IMAGE_SUFFIXES
    ]
    files.sort()
    return files


def failed_item(source: str, mode: str, error: str) -> dict:
    return {"source": source, "mode": mode, "status": "failed", "error": error}


def collect_jobs(args: argparse.Namespace) -> tuple[list[dict], list[dict]]:
    jobs: list[dict] = []
    failed: list[dict] = []
    seen: set[str] = set()

    def add_job(source: str, mode: str, path: Path | None = None) -> None:
        if source in seen:
            return
        seen.add(source)
        job = {"source": source, "mode": mode}
        if path is not None:
            job["path"] = path
        jobs.append(job)

    def add_failed(source: str, mode: str, error: str) -> None:
        if source in seen:
            return
        seen.add(source)
        failed.append(failed_item(source, mode, error))

    for file_arg in args.file or []:
        path = Path(file_arg).expanduser()
        resolved = path.resolve()
        if not resolved.is_file():
            add_failed(str(path), "upload", f"本地文件不存在：{file_arg}")
            continue
        add_job(str(resolved), "upload", resolved)

    for dir_arg in args.dir or []:
        directory = Path(dir_arg).expanduser().resolve()
        if not directory.is_dir():
            add_failed(str(directory), "upload", f"目录不存在：{dir_arg}")
            continue
        files = collect_dir_files(directory, args.recursive)
        if not files:
            add_failed(str(directory), "upload", "目录中没有可上传的图片")
            continue
        for path in files:
            add_job(str(path), "upload", path)

    for url in args.url or []:
        if url.startswith("data:"):
            add_failed(url, "fetch", "不支持 data: URL")
            continue
        if not is_http_url(url):
            add_failed(url, "fetch", "URL 必须是 http(s)")
            continue
        add_job(url, "fetch")

    return jobs, failed


def post_json(url: str, payload: dict, api_key: str, context: ssl.SSLContext) -> tuple[int, object]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, method="POST")
    request.add_header("Content-Type", "application/json")
    request.add_header("Accept", "application/json, text/plain, */*")
    request.add_header("Authorization", f"Bearer {api_key}")
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT, context=context) as resp:
        raw = resp.read().decode("utf-8")
        status = resp.status
    return status, json.loads(raw) if raw else {}


def post_multipart(
    url: str, path: Path, api_key: str, context: ssl.SSLContext
) -> tuple[int, object]:
    body, content_type = encode_multipart_file(path)
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", content_type)
    request.add_header("Accept", "application/json, text/plain, */*")
    request.add_header("Authorization", f"Bearer {api_key}")
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT, context=context) as resp:
        raw = resp.read().decode("utf-8")
        status = resp.status
    return status, json.loads(raw) if raw else {}


def request_once(job: dict, api_base: str, api_key: str, context: ssl.SSLContext) -> tuple[int, object]:
    if job["mode"] == "upload":
        url = f"{api_base}/api/v1/assets/upload"
        return post_multipart(url, job["path"], api_key, context)
    url = f"{api_base}/api/v1/assets/fetch"
    return post_json(url, {"url": job["source"]}, api_key, context)


def read_http_error(error: urllib.error.HTTPError) -> tuple[int, object, str]:
    body_text = error.read().decode("utf-8", errors="replace")
    try:
        payload = json.loads(body_text) if body_text else {}
    except json.JSONDecodeError:
        payload = {"error": {"message": body_text or error.reason, "code": error.code}}
    return error.code, payload, body_text


def upload_job(
    job: dict, api_base: str, api_key: str, context: ssl.SSLContext
) -> dict:
    last_error: str | None = None
    for attempt in (1, 2):
        try:
            _status, payload = request_once(job, api_base, api_key, context)
            result = parse_asset_response(payload)
            result["source"] = job["source"]
            result["mode"] = job["mode"]
            return result
        except urllib.error.HTTPError as error:
            status, payload, body_text = read_http_error(error)
            if status == 429 and attempt == 1:
                time.sleep(RATE_LIMIT_SLEEP)
                continue
            result = parse_asset_response(payload)
            if result.get("status") != "failed":
                result = {
                    "status": "failed",
                    "error": f"HTTP {status} {error.reason}: {body_text}",
                }
            result["source"] = job["source"]
            result["mode"] = job["mode"]
            result["httpStatus"] = status
            return result
        except urllib.error.URLError as error:
            last_error = str(error.reason)
        except json.JSONDecodeError as error:
            last_error = f"响应非 JSON：{error}"
        except OSError as error:
            last_error = str(error)
        if attempt == 1:
            time.sleep(RATE_LIMIT_SLEEP)

    return {
        "source": job["source"],
        "mode": job["mode"],
        "status": "failed",
        "error": last_error or "上传失败",
    }


def build_output(api_base: str, items: list[dict]) -> dict:
    uploaded = sum(1 for item in items if item.get("status") == "uploaded")
    failed = sum(1 for item in items if item.get("status") == "failed")
    planned = sum(1 for item in items if item.get("status") == "planned")
    return {
        "ok": failed == 0 and planned == 0 and uploaded == len(items) and len(items) > 0,
        "apiBase": api_base,
        "counts": {
            "total": len(items),
            "uploaded": uploaded,
            "failed": failed,
            "planned": planned,
        },
        "items": items,
    }


def print_auth_hint(status: int) -> None:
    if status == 401:
        print(invalid_api_key_message(), file=sys.stderr)
    elif status == 403:
        print(
            "提示：该用户未订阅且不是 developer。",
            file=sys.stderr,
        )
    elif status == 402:
        print(
            "提示：402 素材容量已满，请清理素材或升级套餐。",
            file=sys.stderr,
        )
    elif status == 429:
        print("提示：429 触发限流，请稍后重试。", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="上传图片到微排版素材库")
    parser.add_argument("--file", action="append", default=[], help="本地图片路径，可重复")
    parser.add_argument("--url", action="append", default=[], help="远程图片 URL，可重复")
    parser.add_argument("--dir", action="append", default=[], help="本地图片目录，可重复")
    parser.add_argument("--recursive", action="store_true", help="递归扫描 --dir")
    parser.add_argument("--out", help="把结果 JSON 写到该文件")
    parser.add_argument("--api-base", help="覆盖 WEIPAIBAN_API_BASE")
    parser.add_argument("--dry-run", action="store_true", help="只列出将要上传的条目，不发送请求")
    args = parser.parse_args()

    if not (args.file or args.url or args.dir):
        print("错误：至少提供 --file、--url 或 --dir", file=sys.stderr)
        return 2

    jobs, failed = collect_jobs(args)
    if not jobs and not failed:
        print("错误：没有可处理的图片", file=sys.stderr)
        return 2

    try:
        api_base = validate_api_base(
            args.api_base or env("WEIPAIBAN_API_BASE", "https://weipaiban.cn") or ""
        )
    except ValueError as error:
        print(f"错误：{error}", file=sys.stderr)
        return 2

    if args.dry_run:
        items = failed + [
            {
                "source": job["source"],
                "mode": job["mode"],
                "status": "planned",
            }
            for job in jobs
        ]
        output = build_output(api_base, items)
        output["ok"] = not failed
        text = json.dumps(output, ensure_ascii=False, indent=2)
        print(text)
        if args.out:
            Path(args.out).write_text(text + "\n", encoding="utf-8")
        return 1 if failed else 0

    api_key = env("WEIPAIBAN_API_KEY")
    if not api_key:
        print(missing_api_key_message(), file=sys.stderr)
        return 2

    context = build_ssl_context()
    items: list[dict] = list(failed)
    abort_error: str | None = None

    for job in jobs:
        if abort_error:
            items.append(
                {
                    "source": job["source"],
                    "mode": job["mode"],
                    "status": "failed",
                    "error": abort_error,
                }
            )
            continue

        result = upload_job(job, api_base, api_key, context)
        items.append(result)
        status = result.get("httpStatus")
        if status in (401, 402, 403):
            print_auth_hint(status)
            abort_error = result.get("error") or f"HTTP {status}，停止后续上传"
        elif status == 429:
            print_auth_hint(status)

    output = build_output(api_base, items)
    text = json.dumps(output, ensure_ascii=False, indent=2)
    print(text)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")

    if not items:
        return 2
    if any(item.get("status") == "failed" for item in items):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
