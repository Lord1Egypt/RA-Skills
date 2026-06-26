#!/usr/bin/env python3
"""Queenshow detail page OpenAPI client.

Standard-library only. The script prints JSON to stdout.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import sys
import time
import uuid
from pathlib import Path
from typing import Any
from urllib import request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

SENSITIVE_KEYS = {"apiKey", "api_key", "authorization", "plainKey", "secret", "token"}


def json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def redact_sensitive(data: Any) -> Any:
    if isinstance(data, dict):
        redacted: dict[str, Any] = {}
        for key, value in data.items():
            if key == "keyPrefix":
                redacted[key] = value
            elif key in SENSITIVE_KEYS:
                redacted[key] = redact_key(value)
            else:
                redacted[key] = redact_sensitive(value)
        return redacted
    if isinstance(data, list):
        return [redact_sensitive(item) for item in data]
    if isinstance(data, str) and data.startswith("qs_live_"):
        return redact_key(data)
    return data


def redact_key(value: Any) -> Any:
    if not isinstance(value, str):
        return "<redacted>"
    if len(value) <= 14:
        return "<redacted>"
    return value[:14] + "...<redacted>"


def openapi_url(base_url: str, path: str, query: dict[str, Any] | None = None) -> str:
    url = base_url.rstrip("/") + path
    if query:
        clean = {k: v for k, v in query.items() if v not in (None, "")}
        if clean:
            url += "?" + urlencode(clean)
    return url


def unwrap_response(raw: bytes) -> Any:
    payload = json.loads(raw.decode("utf-8"))
    if isinstance(payload, dict) and "errorNo" in payload:
        if payload.get("errorNo") != 200:
            raise RuntimeError(payload.get("errorDesc") or "Queenshow API request failed")
        return payload.get("result")
    return payload


def request_json(
    base_url: str,
    api_key: str,
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
) -> Any:
    data = None
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    req = request.Request(openapi_url(base_url, path, query), data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=60) as resp:
            return unwrap_response(resp.read())
    except HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}") from exc
    except URLError as exc:
        raise RuntimeError(str(exc.reason)) from exc


def request_multipart(
    base_url: str,
    api_key: str,
    path: str,
    files: list[Path],
    fields: dict[str, str],
) -> Any:
    boundary = "----queenshow-" + uuid.uuid4().hex
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )
    for file_path in files:
        mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                (
                    f'Content-Disposition: form-data; name="files"; '
                    f'filename="{file_path.name}"\r\n'
                ).encode(),
                f"Content-Type: {mime}\r\n\r\n".encode(),
                file_path.read_bytes(),
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode())
    req = request.Request(
        openapi_url(base_url, path),
        data=b"".join(chunks),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=300) as resp:
            return unwrap_response(resp.read())
    except HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}") from exc
    except URLError as exc:
        raise RuntimeError(str(exc.reason)) from exc


def build_product(args: argparse.Namespace) -> dict[str, Any]:
    skus = json.loads(args.skus) if args.skus else []
    watermark = json.loads(args.watermark) if args.watermark else {"enabled": False}
    return {
        "mainImages": args.main_image,
        "intro": args.intro or "",
        "brandLogo": args.brand_logo or "",
        "watermark": watermark,
        "skus": skus,
        "detailStyle": args.detail_style or "",
    }


def load_json_payload(inline: str, file_name: str) -> Any:
    if inline and file_name:
        raise RuntimeError("Use either inline JSON or a JSON file, not both")
    if file_name:
        return json.loads(Path(file_name).read_text(encoding="utf-8"))
    if inline:
        return json.loads(inline)
    return None


def create_page(args: argparse.Namespace) -> Any:
    return request_json(
        args.base_url,
        args.api_key,
        "POST",
        "/openapi/detail-pages",
        {
            "title": args.title,
            "desc": args.desc or "",
            "thumbnail": args.thumbnail or "",
            "viewportId": args.viewport_id,
            "product": build_product(args),
        },
    )


def poll_status(args: argparse.Namespace, detail_page_id: str, until: set[str]) -> Any:
    deadline = time.time() + args.timeout
    while True:
        result = request_json(
            args.base_url,
            args.api_key,
            "GET",
            f"/openapi/detail-pages/{detail_page_id}/status",
        )
        status = result.get("status")
        if status in until:
            return result
        if status == "failed":
            return result
        if time.time() >= deadline:
            raise TimeoutError(f"Timed out waiting for {until}; last status={status}")
        time.sleep(args.interval)


def latest_outline_task(status_result: dict[str, Any]) -> dict[str, Any]:
    outline_tasks = [
        task
        for task in status_result.get("tasks", [])
        if task.get("type") == "product_outline_generate"
    ]
    if not outline_tasks:
        raise RuntimeError("No outline task found")
    return outline_tasks[-1]


def command_upload(args: argparse.Namespace) -> Any:
    files = [Path(item) for item in args.files]
    for file_path in files:
        if not file_path.is_file():
            raise RuntimeError(f"File not found: {file_path}")
    return request_multipart(
        args.base_url,
        args.api_key,
        "/openapi/materials/upload",
        files,
        {"fileType": args.file_type} if args.file_type else {},
    )


def command_materials(args: argparse.Namespace) -> Any:
    return request_json(
        args.base_url,
        args.api_key,
        "GET",
        "/openapi/materials",
        query={"fileType": args.file_type, "limit": args.limit},
    )


def command_create(args: argparse.Namespace) -> Any:
    return create_page(args)


def command_pages(args: argparse.Namespace) -> Any:
    return request_json(
        args.base_url,
        args.api_key,
        "GET",
        "/openapi/detail-pages",
        query={"limit": args.limit},
    )


def command_status(args: argparse.Namespace) -> Any:
    return request_json(
        args.base_url,
        args.api_key,
        "GET",
        f"/openapi/detail-pages/{args.detail_page_id}/status",
    )


def command_apply_outline(args: argparse.Namespace) -> Any:
    body: dict[str, Any] = {
        "taskId": args.task_id or "",
        "viewportId": args.viewport_id,
    }
    if args.sections_json:
        body["sections"] = json.loads(args.sections_json)
    return request_json(
        args.base_url,
        args.api_key,
        "POST",
        f"/openapi/detail-pages/{args.detail_page_id}/outline/apply",
        body,
    )


def command_get(args: argparse.Namespace) -> Any:
    return request_json(
        args.base_url,
        args.api_key,
        "GET",
        f"/openapi/detail-pages/{args.detail_page_id}",
    )


def command_update(args: argparse.Namespace) -> Any:
    body: dict[str, Any] = {}
    if args.title is not None:
        body["title"] = args.title
    if args.desc is not None:
        body["desc"] = args.desc
    if args.thumbnail is not None:
        body["thumbnail"] = args.thumbnail
    product = load_json_payload(args.product_json, args.product_file)
    if product is not None:
        body["product"] = product
    document = load_json_payload(args.document_json, args.document_file)
    if document is not None:
        body["document"] = document
    document_field_update = args.document_desc is not None or args.document_title is not None
    if document_field_update:
        if document is not None:
            raise RuntimeError(
                "Use either --document-desc/--document-title or --document-json/--document-file, not both"
            )
        current = request_json(
            args.base_url,
            args.api_key,
            "GET",
            f"/openapi/detail-pages/{args.detail_page_id}",
        )
        current_doc = (current.get("detailPage") or {}).get("document")
        if not isinstance(current_doc, dict):
            raise RuntimeError("Current detail page document is missing or invalid")
        if args.document_desc is not None:
            current_doc["desc"] = args.document_desc
            body.setdefault("desc", args.document_desc)
        if args.document_title is not None:
            current_doc["title"] = args.document_title
            body.setdefault("title", args.document_title)
        body["document"] = current_doc
    if not body:
        raise RuntimeError("No update fields provided")
    return request_json(
        args.base_url,
        args.api_key,
        "POST",
        f"/openapi/detail-pages/{args.detail_page_id}/update",
        body,
    )


def command_task(args: argparse.Namespace) -> Any:
    return request_json(args.base_url, args.api_key, "GET", f"/openapi/tasks/{args.task_id}")


def command_usage(args: argparse.Namespace) -> Any:
    return request_json(args.base_url, args.api_key, "GET", "/openapi/usage")


def command_run(args: argparse.Namespace) -> Any:
    created = create_page(args)
    detail_page_id = created["detailPageId"]
    outline_status = poll_status(args, detail_page_id, {"outline_ready"})
    if outline_status.get("status") == "failed":
        return {"created": created, "status": outline_status}
    outline_task = latest_outline_task(outline_status)
    applied = request_json(
        args.base_url,
        args.api_key,
        "POST",
        f"/openapi/detail-pages/{detail_page_id}/outline/apply",
        {"taskId": outline_task.get("taskId", ""), "viewportId": args.viewport_id},
    )
    final_status = poll_status(args, detail_page_id, {"completed"})
    final_page = request_json(args.base_url, args.api_key, "GET", f"/openapi/detail-pages/{detail_page_id}")
    return {
        "created": created,
        "outlineStatus": outline_status,
        "applied": applied,
        "finalStatus": final_status,
        "finalPage": final_page,
    }


def document_nodes(document: dict[str, Any]) -> list[dict[str, Any]]:
    nodes = document.get("nodes")
    if isinstance(nodes, dict):
        return [node for node in nodes.values() if isinstance(node, dict)]
    if isinstance(nodes, list):
        return [node for node in nodes if isinstance(node, dict)]
    return []


def image_url(node: dict[str, Any]) -> str:
    value = node.get("value") if isinstance(node.get("value"), dict) else {}
    for key in ("url", "src", "imageUrl", "generatedUrl"):
        url = value.get(key)
        if isinstance(url, str) and url:
            return url
    return ""


def is_image_node(node: dict[str, Any]) -> bool:
    return node.get("compKey") == "Image" or str(node.get("id", "")).startswith("node_image_")


def is_section_node(node: dict[str, Any]) -> bool:
    return node.get("compKey") == "Section" or str(node.get("id", "")).startswith("section_outline_")


def summarize_task(task: dict[str, Any]) -> dict[str, Any]:
    progress = task.get("progress") if isinstance(task.get("progress"), dict) else {}
    billing = task.get("billing") if isinstance(task.get("billing"), dict) else {}
    return {
        "taskId": task.get("taskId"),
        "type": task.get("type"),
        "title": task.get("title"),
        "status": task.get("status"),
        "percent": progress.get("percent"),
        "stage": progress.get("stage"),
        "billingStatus": billing.get("status"),
        "amount": billing.get("amount"),
    }


def summarize_status(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "detailPageId": result.get("detailPageId"),
        "status": result.get("status"),
        "spent": result.get("spent"),
        "updated": result.get("updated"),
        "tasks": [summarize_task(task) for task in result.get("tasks", []) if isinstance(task, dict)],
    }


def summarize_detail_page(result: dict[str, Any]) -> dict[str, Any]:
    detail_page = result.get("detailPage") if isinstance(result.get("detailPage"), dict) else {}
    document = detail_page.get("document") if isinstance(detail_page.get("document"), dict) else {}
    nodes = document_nodes(document)
    image_nodes = [node for node in nodes if is_image_node(node)]
    section_nodes = [node for node in nodes if is_section_node(node)]
    images = []
    for node in image_nodes:
        value = node.get("value") if isinstance(node.get("value"), dict) else {}
        url = image_url(node)
        images.append(
            {
                "id": node.get("id"),
                "generationStatus": value.get("generationStatus"),
                "hasUrl": bool(url),
                "url": url,
            }
        )
    return {
        "detailPageId": result.get("detailPageId"),
        "status": result.get("status"),
        "spent": result.get("spent"),
        "updated": result.get("updated"),
        "title": detail_page.get("title"),
        "document": {
            "id": document.get("id"),
            "title": document.get("title"),
            "desc": document.get("desc"),
            "nodeCount": len(nodes),
            "sectionNodes": len(section_nodes),
            "imageNodes": len(image_nodes),
            "imagesWithUrl": sum(1 for node in image_nodes if image_url(node)),
            "images": images,
        },
        "tasks": [summarize_task(task) for task in result.get("tasks", []) if isinstance(task, dict)],
    }


def summarize_collection(result: dict[str, Any], key: str) -> dict[str, Any]:
    items = result.get(key)
    if not isinstance(items, list):
        return result
    return {
        "count": len(items),
        key: items,
    }


def summarize_usage(result: dict[str, Any]) -> dict[str, Any]:
    key = result.get("key") if isinstance(result.get("key"), dict) else {}
    return {
        "usage": result.get("usage"),
        "key": {
            "_id": key.get("_id"),
            "name": key.get("name"),
            "keyPrefix": key.get("keyPrefix"),
            "priceLimit": key.get("priceLimit"),
            "status": key.get("status"),
            "lastUsedAt": key.get("lastUsedAt"),
        },
    }


def summarize_result(command: str, result: Any) -> Any:
    if not isinstance(result, dict):
        return result
    if command == "status":
        return summarize_status(result)
    if command == "get":
        return summarize_detail_page(result)
    if command == "usage":
        return summarize_usage(result)
    if command == "materials":
        return summarize_collection(result, "materials")
    if command == "pages":
        return summarize_collection(result, "detailPages")
    if command == "run":
        final_status = result.get("finalStatus")
        final_page = result.get("finalPage")
        return {
            "created": result.get("created"),
            "outlineStatus": summarize_status(final_status) if isinstance(final_status, dict) else final_status,
            "applied": result.get("applied"),
            "finalPage": summarize_detail_page(final_page) if isinstance(final_page, dict) else final_page,
        }
    return result


def add_product_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--title", required=True)
    parser.add_argument("--desc", default="")
    parser.add_argument("--thumbnail", default="")
    parser.add_argument("--viewport-id", default="mobile-750-long")
    parser.add_argument("--main-image", action="append", required=True)
    parser.add_argument("--intro", default="")
    parser.add_argument("--brand-logo", default="")
    parser.add_argument("--watermark", default="")
    parser.add_argument("--skus", default="")
    parser.add_argument("--detail-style", default="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Queenshow detail page OpenAPI client")
    parser.add_argument("--base-url", required=True, help="Example: https://host/api/promotion")
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--summary", action="store_true", help="Print a compact verification-friendly summary")
    parser.add_argument("--show-sensitive", action="store_true", help="Do not redact sensitive fields in output")
    sub = parser.add_subparsers(dest="command", required=True)

    upload = sub.add_parser("upload")
    upload.add_argument("--file-type", choices=["image", "video"], default="")
    upload.add_argument("files", nargs="+")
    upload.set_defaults(func=command_upload)

    materials = sub.add_parser("materials")
    materials.add_argument("--file-type", choices=["image", "video"], default="")
    materials.add_argument("--limit", type=int, default=50)
    materials.set_defaults(func=command_materials)

    create = sub.add_parser("create")
    add_product_args(create)
    create.set_defaults(func=command_create)

    pages = sub.add_parser("pages")
    pages.add_argument("--limit", type=int, default=50)
    pages.set_defaults(func=command_pages)

    status = sub.add_parser("status")
    status.add_argument("detail_page_id")
    status.set_defaults(func=command_status)

    apply_outline = sub.add_parser("apply-outline")
    apply_outline.add_argument("detail_page_id")
    apply_outline.add_argument("--task-id", default="")
    apply_outline.add_argument("--viewport-id", default="mobile-750-long")
    apply_outline.add_argument("--sections-json", default="")
    apply_outline.set_defaults(func=command_apply_outline)

    get = sub.add_parser("get")
    get.add_argument("detail_page_id")
    get.set_defaults(func=command_get)

    update = sub.add_parser("update")
    update.add_argument("detail_page_id")
    update.add_argument("--title")
    update.add_argument("--desc")
    update.add_argument("--thumbnail")
    update.add_argument("--product-json", default="")
    update.add_argument("--product-file", default="")
    update.add_argument("--document-json", default="")
    update.add_argument("--document-file", default="")
    update.add_argument("--document-desc", help="Fetch the current document, set document.desc, and update it")
    update.add_argument("--document-title", help="Fetch the current document, set document.title, and update it")
    update.set_defaults(func=command_update)

    task = sub.add_parser("task")
    task.add_argument("task_id")
    task.set_defaults(func=command_task)

    usage = sub.add_parser("usage")
    usage.set_defaults(func=command_usage)

    run = sub.add_parser("run")
    add_product_args(run)
    run.add_argument("--interval", type=int, default=10)
    run.add_argument("--timeout", type=int, default=900)
    run.set_defaults(func=command_run)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.func(args)
        if args.summary:
            result = summarize_result(args.command, result)
        if not args.show_sensitive:
            result = redact_sensitive(result)
        print(json_dumps(result))
        return 0
    except Exception as exc:  # noqa: BLE001
        print(json_dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
