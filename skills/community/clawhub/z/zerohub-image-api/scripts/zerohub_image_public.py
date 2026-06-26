#!/usr/bin/env python3
"""zeroHub image API helper.

Features:
- balance: query user balance with user-provided ZEROHUB_API_KEY
- generate: submit image generation task and poll until done
- download: download returned zeroHub image URLs to a user-selected directory

Security:
- Never hard-code or print API keys.
- Only sends ZEROHUB_API_KEY to the configured zeroHub API origin.
- Downloads are restricted to allowed zeroHub hosts by default.
- Blocks localhost/private/link-local IP targets.
- Enforces a maximum download size.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import mimetypes
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_BASE_URL = "https://zerohub.zhyy.ltd"
BASE_URL = os.environ.get("ZEROHUB_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
DEFAULT_MODEL = os.environ.get("ZEROHUB_MODEL", "gpt-image-2")
DEFAULT_MAX_DOWNLOAD_BYTES = int(os.environ.get("ZEROHUB_MAX_DOWNLOAD_BYTES", str(25 * 1024 * 1024)))
DEFAULT_ALLOWED_HOSTS = {"zerohub.zhyy.ltd"}


def _json_dump(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _api_key(required: bool = True) -> Optional[str]:
    key = os.environ.get("ZEROHUB_API_KEY")
    if required and not key:
        print("ERROR: ZEROHUB_API_KEY is required", file=sys.stderr)
        sys.exit(2)
    return key


def _host_of(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return (parsed.hostname or "").lower().rstrip(".")


def _base_origin() -> str:
    parsed = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != "https" or not parsed.hostname:
        print("ERROR: ZEROHUB_BASE_URL must be an https URL with a hostname", file=sys.stderr)
        sys.exit(2)
    return f"{parsed.scheme}://{parsed.netloc}"


def _allowed_hosts(extra_hosts: Optional[List[str]] = None) -> set[str]:
    hosts = set(DEFAULT_ALLOWED_HOSTS)
    base_host = _host_of(BASE_URL)
    if base_host:
        hosts.add(base_host)
    for h in extra_hosts or []:
        clean = h.strip().lower().rstrip(".")
        if clean:
            hosts.add(clean)
    return hosts


def _validate_hostname(host: str, allowed_hosts: set[str]) -> None:
    if not host:
        raise ValueError("URL has no hostname")
    # Keep policy simple and reviewable: exact host or subdomain of an allowed host.
    if not any(host == allowed or host.endswith("." + allowed) for allowed in allowed_hosts):
        raise ValueError(f"host not allowed: {host}")


def _is_blocked_ip(ip_text: str) -> bool:
    ip = ipaddress.ip_address(ip_text)
    return any([
        ip.is_private,
        ip.is_loopback,
        ip.is_link_local,
        ip.is_multicast,
        ip.is_reserved,
        ip.is_unspecified,
    ])


def _validate_resolved_ips(host: str) -> None:
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as e:
        raise ValueError(f"cannot resolve host {host}: {e}") from e
    seen: set[str] = set()
    for info in infos:
        ip_text = info[4][0]
        if ip_text in seen:
            continue
        seen.add(ip_text)
        if _is_blocked_ip(ip_text):
            raise ValueError(f"blocked private or local network target: {host} -> {ip_text}")


def _validate_url_for_network(url: str, *, allowed_hosts: set[str], allow_http: bool = False) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ({"https", "http"} if allow_http else {"https"}):
        raise ValueError("only https URLs are allowed" if not allow_http else "only http/https URLs are allowed")
    host = (parsed.hostname or "").lower().rstrip(".")
    _validate_hostname(host, allowed_hosts)
    _validate_resolved_ips(host)
    return urllib.parse.urlunparse(parsed)


def _request(method: str, path: str, *, data: Optional[Dict[str, Any]] = None, timeout: int = 60) -> Dict[str, Any]:
    key = _api_key(True)
    origin = _base_origin()
    url = path if path.startswith(("http://", "https://")) else f"{origin}{path}"
    # API requests must go to the configured zeroHub origin only. This prevents accidental
    # credential transmission to arbitrary URLs if a path is attacker-controlled.
    parsed_url = urllib.parse.urlparse(url)
    parsed_origin = urllib.parse.urlparse(origin)
    if parsed_url.scheme != "https" or parsed_url.hostname != parsed_origin.hostname:
        return {"error": "API request host is not allowed", "url": url}
    body = None
    headers = {"Authorization": f"Bearer {key}", "Accept": "application/json"}
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                parsed = {"raw": raw}
            if isinstance(parsed, dict):
                parsed.setdefault("_http_status", resp.status)
            return parsed
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        if isinstance(parsed, dict):
            parsed["_http_status"] = e.code
        return parsed


def _absolute_url(url: str) -> str:
    text = str(url or "").strip()
    if text.startswith(("http://", "https://")):
        return text
    if text.startswith("//"):
        return "https:" + text
    if text.startswith("/"):
        return f"{_base_origin()}{text}"
    return urllib.parse.urljoin(_base_origin() + "/", text)


def _safe_filename(value: str, *, fallback: str) -> str:
    name = Path(urllib.parse.urlparse(value).path).name or fallback
    name = urllib.parse.unquote(name)
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip(".-")
    return name or fallback


def _guess_ext(content_type: str, url: str) -> str:
    path_ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if path_ext in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        return path_ext
    ctype = (content_type or "").split(";", 1)[0].strip().lower()
    return mimetypes.guess_extension(ctype) or ".png"


def _read_limited(resp: Any, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = resp.read(1024 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise ValueError(f"download exceeds maximum size of {max_bytes} bytes")
        chunks.append(chunk)
    return b"".join(chunks)


def download_one(
    url: str,
    output_dir: Path,
    *,
    prefix: str,
    index: int,
    timeout: int = 120,
    max_bytes: int = DEFAULT_MAX_DOWNLOAD_BYTES,
    allowed_hosts: Optional[List[str]] = None,
    allow_http: bool = False,
) -> Dict[str, Any]:
    abs_url = _absolute_url(url)
    try:
        safe_url = _validate_url_for_network(
            abs_url,
            allowed_hosts=_allowed_hosts(allowed_hosts),
            allow_http=allow_http,
        )
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "url": abs_url, "error": str(e)}

    output_dir.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(safe_url, headers={"User-Agent": "zerohub-image-api/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            content_length = resp.headers.get("Content-Length")
            if content_length and int(content_length) > max_bytes:
                raise ValueError(f"download exceeds maximum size of {max_bytes} bytes")
            data = _read_limited(resp, max_bytes)
            ext = _guess_ext(content_type, safe_url)
            fallback = f"{prefix}-{index}{ext}"
            base_name = _safe_filename(safe_url, fallback=fallback)
            if not Path(base_name).suffix:
                base_name += ext
            filename = _safe_filename(f"{prefix}-{index}-{base_name}", fallback=fallback)
            path = (output_dir / filename).resolve()
            try:
                path.relative_to(output_dir.resolve())
            except ValueError:
                raise RuntimeError("resolved output path escapes output_dir")
            path.write_bytes(data)
            return {
                "ok": True,
                "url": safe_url,
                "path": str(path),
                "filename": filename,
                "content_type": content_type,
                "size": len(data),
            }
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "url": safe_url, "error": str(e)}


def download_urls(
    urls: List[str],
    output_dir: Path,
    *,
    prefix: str,
    timeout: int,
    max_bytes: int,
    allowed_hosts: Optional[List[str]] = None,
    allow_http: bool = False,
) -> List[Dict[str, Any]]:
    return [
        download_one(
            url,
            output_dir,
            prefix=prefix,
            index=i,
            timeout=timeout,
            max_bytes=max_bytes,
            allowed_hosts=allowed_hosts,
            allow_http=allow_http,
        )
        for i, url in enumerate(urls, start=1)
    ]


def balance(_: argparse.Namespace) -> None:
    _json_dump(_request("GET", "/v1/user/balance", timeout=30))


def _extract_task_id(resp: Dict[str, Any]) -> Optional[str]:
    if isinstance(resp.get("task_id"), str):
        return resp["task_id"]
    text = json.dumps(resp, ensure_ascii=False)
    m = re.search(r"task_[A-Za-z0-9_-]+", text)
    return m.group(0) if m else None


def _collect_images(payload: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    images = payload.get("images") if isinstance(payload.get("images"), list) else []
    previews = payload.get("preview_images") if isinstance(payload.get("preview_images"), list) else []
    return [str(x) for x in images], [str(x) for x in previews]


def generate(args: argparse.Namespace) -> None:
    payload: Dict[str, Any] = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "quality": args.quality,
    }
    if args.images:
        payload["images"] = args.images

    submit = _request("POST", "/v1/images/generations", data=payload, timeout=args.submit_timeout)
    task_id = _extract_task_id(submit)
    result: Dict[str, Any] = {
        "submitted": submit,
        "task_id": task_id,
        "status": None,
        "images": [],
        "preview_images": [],
        "downloaded_files": [],
    }
    if not task_id:
        result["status"] = "submit_error"
        _json_dump(result)
        sys.exit(1)

    deadline = time.time() + args.max_wait
    poll_count = 0
    last: Dict[str, Any] = {}
    while time.time() <= deadline:
        poll_count += 1
        time.sleep(args.interval if poll_count > 1 else args.first_delay)
        last = _request("GET", f"/v1/images/query/{task_id}", timeout=args.query_timeout)
        status = last.get("status")
        if args.progress:
            print(json.dumps({"poll": poll_count, "task_id": task_id, "status": status}, ensure_ascii=False), file=sys.stderr)
        if status in {"success", "failed"}:
            break

    images, previews = _collect_images(last)
    result.update({
        "status": last.get("status", "timeout"),
        "poll_count": poll_count,
        "query": last,
        "images": [_absolute_url(x) for x in images],
        "preview_images": [_absolute_url(x) for x in previews],
    })

    if args.download and result["status"] == "success":
        if not args.output_dir:
            result["download_error"] = "--output-dir is required when --download is used"
            _json_dump(result)
            sys.exit(2)
        urls = images + ([] if args.no_preview_download else previews)
        result["downloaded_files"] = download_urls(
            urls,
            Path(args.output_dir).expanduser(),
            prefix=_safe_filename(task_id, fallback="zerohub-task"),
            timeout=args.download_timeout,
            max_bytes=args.max_download_bytes,
            allowed_hosts=args.allowed_host,
            allow_http=args.allow_http,
        )

    _json_dump(result)
    if result["status"] != "success":
        sys.exit(1)


def download_cmd(args: argparse.Namespace) -> None:
    if not args.urls:
        print("ERROR: at least one URL is required", file=sys.stderr)
        sys.exit(2)
    downloaded = download_urls(
        args.urls,
        Path(args.output_dir).expanduser(),
        prefix=_safe_filename(args.prefix, fallback="zerohub-image"),
        timeout=args.download_timeout,
        max_bytes=args.max_download_bytes,
        allowed_hosts=args.allowed_host,
        allow_http=args.allow_http,
    )
    _json_dump({"downloaded_files": downloaded})
    if not all(x.get("ok") for x in downloaded):
        sys.exit(1)


def add_download_safety_args(sp: argparse.ArgumentParser) -> None:
    sp.add_argument("--download-timeout", type=int, default=120)
    sp.add_argument("--max-download-bytes", type=int, default=DEFAULT_MAX_DOWNLOAD_BYTES)
    sp.add_argument(
        "--allowed-host",
        action="append",
        default=[],
        help="additional allowed download host; zeroHub hosts are allowed by default",
    )
    sp.add_argument("--allow-http", action="store_true", help="allow http downloads; https-only by default")


def main() -> None:
    p = argparse.ArgumentParser(description="zeroHub image API helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("balance", help="query balance")
    sp.set_defaults(func=balance)

    sp = sub.add_parser("generate", help="submit and poll image generation")
    sp.add_argument("--prompt", required=True)
    sp.add_argument("--model", default=DEFAULT_MODEL)
    sp.add_argument("--size", default="1:1")
    sp.add_argument("--quality", default="low", choices=["auto", "low", "medium", "high"])
    sp.add_argument("--images", nargs="*", default=[])
    sp.add_argument("--max-wait", type=int, default=180)
    sp.add_argument("--interval", type=int, default=5)
    sp.add_argument("--first-delay", type=int, default=3)
    sp.add_argument("--submit-timeout", type=int, default=60)
    sp.add_argument("--query-timeout", type=int, default=30)
    sp.add_argument("--progress", action="store_true", help="print poll progress to stderr")
    sp.add_argument("--download", action="store_true", help="download generated images to --output-dir")
    sp.add_argument("--output-dir", help="user-selected local directory for downloaded images")
    sp.add_argument("--no-preview-download", action="store_true", help="download images only, not preview_images")
    add_download_safety_args(sp)
    sp.set_defaults(func=generate)

    sp = sub.add_parser("download", help="download existing zeroHub image URLs")
    sp.add_argument("--output-dir", required=True, help="user-selected local directory")
    sp.add_argument("--prefix", default="zerohub-image")
    add_download_safety_args(sp)
    sp.add_argument("urls", nargs="+")
    sp.set_defaults(func=download_cmd)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
