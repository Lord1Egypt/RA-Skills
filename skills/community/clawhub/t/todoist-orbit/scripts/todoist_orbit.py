#!/usr/bin/env python3
import argparse
import asyncio
import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = "https://api.todoist.com/api/v1"
DEFAULT_TIMEOUT = 60


class TodoistError(Exception):
    pass


def non_empty_text(value: str, *, source: str) -> str:
    if not value:
        raise TodoistError(f"Comment content from {source} is empty")
    return value


def env_token() -> str:
    token = os.environ.get("TODOIST_API_KEY")
    if not token:
        raise TodoistError("TODOIST_API_KEY environment variable is not set")
    return token


def auth_headers(content_type: Optional[str] = "application/json") -> Dict[str, str]:
    headers = {"Authorization": f"Bearer {env_token()}"}
    if content_type:
        headers["Content-Type"] = content_type
    return headers


async def request_json(endpoint: str, *, method: str = "GET", data: Optional[dict] = None, params: Optional[dict] = None) -> Any:
    return await asyncio.to_thread(_request_json_sync, endpoint, method, data, params)


async def request_bytes(url: str, *, method: str = "GET", data: Optional[bytes] = None, headers: Optional[dict] = None) -> bytes:
    return await asyncio.to_thread(_request_bytes_sync, url, method, data, headers)


def _request_json_sync(endpoint: str, method: str, data: Optional[dict], params: Optional[dict]) -> Any:
    url = endpoint if endpoint.startswith("http") else f"{API_BASE}{endpoint}"
    if params:
        params = {k: v for k, v in params.items() if v is not None}
        if params:
            url = f"{url}?{urlencode(params, doseq=True)}"
    payload = None if data is None else json.dumps(data).encode("utf-8")
    req = Request(url, method=method, headers=auth_headers(), data=payload)
    try:
        with urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            body = resp.read()
    except HTTPError as e:
        raise _format_http_error(e)
    except URLError as e:
        raise TodoistError(f"Request failed: {e.reason}")
    return _decode_json_or_empty(body)


def _request_bytes_sync(url: str, method: str, data: Optional[bytes], headers: Optional[dict]) -> bytes:
    req = Request(url, method=method, headers=headers or auth_headers(None), data=data)
    try:
        with urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            return resp.read()
    except HTTPError as e:
        raise _format_http_error(e)
    except URLError as e:
        raise TodoistError(f"Request failed: {e.reason}")


def _decode_json_or_empty(body: bytes) -> Any:
    if not body:
        return {"ok": True}
    return json.loads(body.decode("utf-8"))


def _format_http_error(e: HTTPError) -> TodoistError:
    body = e.read().decode("utf-8", errors="replace")
    try:
        parsed = json.loads(body)
    except Exception:
        parsed = body
    return TodoistError(f"HTTP {e.code}: {parsed}")


def collection_items(payload: Any) -> list:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("results", "items", "projects", "sections", "labels"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def filter_by_name(items: list, needle: str, *, field: str = "name", exact: bool = False) -> list:
    query = needle.lower()
    matched = []
    for item in items:
        value = str(item.get(field, ""))
        hay = value.lower()
        if (hay == query) if exact else (query in hay):
            matched.append(item)
    return matched


async def list_tasks(args):
    params = {
        "filter": args.filter,
        "project_id": args.project_id,
        "section_id": args.section_id,
        "label": args.label,
        "ids": args.ids,
        "limit": args.limit,
    }
    tasks = await request_json("/tasks", params=params)
    if args.priority:
        tasks = [task for task in tasks if task.get("priority") == args.priority]
    if args.content_contains:
        needle = args.content_contains.lower()
        tasks = [task for task in tasks if needle in task.get("content", "").lower()]
    return tasks


async def get_task(args):
    return await request_json(f"/tasks/{args.task_id}")


async def add_task(args):
    payload = {
        "content": args.content,
        "description": args.description,
        "project_id": args.project_id,
        "section_id": args.section_id,
        "parent_id": args.parent_id,
        "order": args.order,
        "labels": args.labels,
        "priority": args.priority,
        "due_string": args.due,
        "deadline_date": args.deadline_date,
        "duration": {"amount": args.duration_amount, "unit": args.duration_unit} if args.duration_amount and args.duration_unit else None,
    }
    return await request_json("/tasks", method="POST", data={k: v for k, v in payload.items() if v is not None})


async def update_task(args):
    payload = {
        "content": args.content,
        "description": args.description,
        "project_id": args.project_id,
        "section_id": args.section_id,
        "parent_id": args.parent_id,
        "labels": args.labels,
        "priority": args.priority,
        "due_string": args.due,
        "deadline_date": args.deadline_date,
    }
    return await request_json(f"/tasks/{args.task_id}", method="POST", data={k: v for k, v in payload.items() if v is not None})


async def move_task(args):
    return await request_json(f"/tasks/{args.task_id}/move", method="POST", data={k: v for k, v in {
        "project_id": args.project_id,
        "section_id": args.section_id,
        "parent_id": args.parent_id,
    }.items() if v is not None})


async def close_task(args):
    return await request_json(f"/tasks/{args.task_id}/close", method="POST")


async def reopen_task(args):
    return await request_json(f"/tasks/{args.task_id}/reopen", method="POST")


async def delete_task(args):
    await request_json(f"/tasks/{args.task_id}", method="DELETE")
    return {"ok": True, "deleted": args.task_id}


async def list_projects(_args):
    return await request_json("/projects")


async def search_projects(args):
    projects = await request_json("/projects/search", params={"query": args.name})
    items = collection_items(projects)
    if args.exact:
        items = filter_by_name(items, args.name, exact=True)
    return items


async def get_project(args):
    return await request_json(f"/projects/{args.project_id}")


async def add_project(args):
    payload = {
        "name": args.name,
        "parent_id": args.parent_id,
        "color": args.color,
        "view_style": args.view_style,
        "is_favorite": args.favorite,
    }
    return await request_json("/projects", method="POST", data={k: v for k, v in payload.items() if v is not None})


async def update_project(args):
    payload = {
        "name": args.name,
        "color": args.color,
        "view_style": args.view_style,
        "is_favorite": args.favorite,
    }
    return await request_json(f"/projects/{args.project_id}", method="POST", data={k: v for k, v in payload.items() if v is not None})


async def archive_project(args):
    return await request_json(f"/projects/{args.project_id}/archive", method="POST")


async def unarchive_project(args):
    return await request_json(f"/projects/{args.project_id}/unarchive", method="POST")


async def delete_project(args):
    await request_json(f"/projects/{args.project_id}", method="DELETE")
    return {"ok": True, "deleted": args.project_id}


async def list_sections(args):
    return await request_json("/sections", params={"project_id": args.project_id})


async def get_section(args):
    return await request_json(f"/sections/{args.section_id}")


async def add_section(args):
    return await request_json("/sections", method="POST", data={"name": args.name, "project_id": args.project_id, **({"order": args.order} if args.order is not None else {})})


async def update_section(args):
    payload = {"name": args.name}
    if args.order is not None:
        payload["order"] = args.order
    return await request_json(f"/sections/{args.section_id}", method="POST", data=payload)


async def move_section(args):
    raise TodoistError(
        "sections move is not supported by the Todoist REST API. "
        "The CLI keeps this command for compatibility, but it cannot move sections."
    )


async def archive_section(args):
    return await request_json(f"/sections/{args.section_id}/archive", method="POST")


async def unarchive_section(args):
    return await request_json(f"/sections/{args.section_id}/unarchive", method="POST")


async def delete_section(args):
    await request_json(f"/sections/{args.section_id}", method="DELETE")
    return {"ok": True, "deleted": args.section_id}


async def list_labels(_args):
    return await request_json("/labels")


async def search_labels(args):
    labels = await request_json("/labels/search", params={"query": args.name})
    items = collection_items(labels)
    if args.exact:
        items = filter_by_name(items, args.name, exact=True)
    return items


async def get_label(args):
    return await request_json(f"/labels/{args.label_id}")


async def add_label(args):
    payload = {
        "name": args.name,
        "color": args.color,
        "order": args.order,
        "is_favorite": args.favorite,
    }
    return await request_json("/labels", method="POST", data={k: v for k, v in payload.items() if v is not None})


async def update_label(args):
    payload = {
        "name": args.name,
        "color": args.color,
        "order": args.order,
        "is_favorite": args.favorite,
    }
    return await request_json(f"/labels/{args.label_id}", method="POST", data={k: v for k, v in payload.items() if v is not None})


async def delete_label(args):
    await request_json(f"/labels/{args.label_id}", method="DELETE")
    return {"ok": True, "deleted": args.label_id}


async def list_comments(args):
    params = {"task_id": args.task_id, "project_id": args.project_id}
    return await request_json("/comments", params=params)


def comment_target_payload(args) -> dict:
    payload: Dict[str, Any] = {}
    if args.task_id:
        payload["task_id"] = args.task_id
    if args.project_id:
        payload["project_id"] = args.project_id
    return payload


def read_comment_content_from_file(path_str: str) -> str:
    path = Path(path_str)
    if not path.is_file():
        raise TodoistError(f"File not found: {path}")
    try:
        return non_empty_text(path.read_text(encoding="utf-8"), source=str(path))
    except UnicodeDecodeError as exc:
        raise TodoistError(f"Comment content file must be valid UTF-8: {path}") from exc


def read_comment_content_from_stdin() -> str:
    return non_empty_text(sys.stdin.read(), source="stdin")


async def add_comment(args):
    payload = {"content": non_empty_text(args.content, source="command line"), **comment_target_payload(args)}
    if args.attachment:
        payload["attachment"] = await upload_file(Path(args.attachment))
    return await request_json("/comments", method="POST", data=payload)


async def add_comment_from_file(args):
    payload = {"content": read_comment_content_from_file(args.file), **comment_target_payload(args)}
    if args.attachment:
        payload["attachment"] = await upload_file(Path(args.attachment))
    return await request_json("/comments", method="POST", data=payload)


async def add_comment_from_stdin(args):
    payload = {"content": read_comment_content_from_stdin(), **comment_target_payload(args)}
    if args.attachment:
        payload["attachment"] = await upload_file(Path(args.attachment))
    return await request_json("/comments", method="POST", data=payload)


async def upload_only(args):
    return await upload_file(Path(args.file))


async def upload_file(path: Path) -> dict:
    if not path.is_file():
        raise TodoistError(f"File not found: {path}")
    filename = path.name
    mime = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    data = path.read_bytes()
    boundary = f"todoist-orbit-{uuid.uuid4().hex}"
    body = build_multipart(boundary, filename, mime, data)
    raw = await request_bytes(
        f"{API_BASE}/uploads",
        method="POST",
        data=body,
        headers={
            "Authorization": f"Bearer {env_token()}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    return _decode_json_or_empty(raw)


def build_multipart(boundary: str, filename: str, mime: str, payload: bytes) -> bytes:
    parts = [
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode(),
        f"Content-Type: {mime}\r\n\r\n".encode(),
        payload,
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ]
    return b"".join(parts)


async def resolve(args):
    coros = {}
    if args.project:
        coros["projects"] = request_json("/projects")
    if args.section:
        coros["sections"] = request_json("/sections")
    if args.task_filter is not None:
        coros["tasks"] = request_json("/tasks", params={"filter": args.task_filter or None, "limit": args.limit})
    results = await asyncio.gather(*coros.values(), return_exceptions=True)
    out: Dict[str, Any] = {}
    for key, value in zip(coros.keys(), results):
        if isinstance(value, Exception):
            out[key] = {"error": str(value)}
        else:
            out[key] = value
    if args.project:
        matches = filter_by_name(collection_items(out.get("projects")), args.project, exact=True)
        out["project_match"] = matches[0] if matches else None
    if args.section:
        matches = filter_by_name(collection_items(out.get("sections")), args.section, exact=True)
        out["section_match"] = matches[0] if matches else None
    return out


def configure_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Async Todoist CLI using the REST API and stdlib HTTP")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("tasks", help="Task operations")
    ps = p.add_subparsers(dest="action", required=True)

    sp = ps.add_parser("list")
    sp.add_argument("--filter")
    sp.add_argument("--project-id")
    sp.add_argument("--section-id")
    sp.add_argument("--label")
    sp.add_argument("--ids", nargs="*")
    sp.add_argument("--priority", type=int, choices=[1, 2, 3, 4])
    sp.add_argument("--content-contains")
    sp.add_argument("--limit", type=int, default=50)
    sp.set_defaults(func=list_tasks)

    sp = ps.add_parser("get")
    sp.add_argument("task_id")
    sp.set_defaults(func=get_task)

    sp = ps.add_parser("add")
    sp.add_argument("content")
    sp.add_argument("--description")
    sp.add_argument("--project-id")
    sp.add_argument("--section-id")
    sp.add_argument("--parent-id")
    sp.add_argument("--order", type=int)
    sp.add_argument("--labels", nargs="*")
    sp.add_argument("--priority", type=int, choices=[1, 2, 3, 4])
    sp.add_argument("--due")
    sp.add_argument("--deadline-date")
    sp.add_argument("--duration-amount", type=int)
    sp.add_argument("--duration-unit", choices=["minute", "day"])
    sp.set_defaults(func=add_task)

    sp = ps.add_parser("update")
    sp.add_argument("task_id")
    sp.add_argument("--content")
    sp.add_argument("--description")
    sp.add_argument("--project-id")
    sp.add_argument("--section-id")
    sp.add_argument("--parent-id")
    sp.add_argument("--labels", nargs="*")
    sp.add_argument("--priority", type=int, choices=[1, 2, 3, 4])
    sp.add_argument("--due")
    sp.add_argument("--deadline-date")
    sp.set_defaults(func=update_task)

    sp = ps.add_parser("move")
    sp.add_argument("task_id")
    sp.add_argument("--project-id")
    sp.add_argument("--section-id")
    sp.add_argument("--parent-id")
    sp.set_defaults(func=move_task)

    sp = ps.add_parser("close")
    sp.add_argument("task_id")
    sp.set_defaults(func=close_task)

    sp = ps.add_parser("reopen")
    sp.add_argument("task_id")
    sp.set_defaults(func=reopen_task)

    sp = ps.add_parser("delete")
    sp.add_argument("task_id")
    sp.set_defaults(func=delete_task)

    p = sub.add_parser("projects", help="Project operations")
    ps = p.add_subparsers(dest="action", required=True)

    sp = ps.add_parser("list")
    sp.set_defaults(func=list_projects)

    sp = ps.add_parser(
        "search",
        help="Search projects via Todoist API /projects/search",
        description="Search projects via Todoist API /projects/search",
    )
    sp.add_argument("name")
    sp.add_argument("--exact", action="store_true")
    sp.set_defaults(func=search_projects)

    sp = ps.add_parser("get")
    sp.add_argument("project_id")
    sp.set_defaults(func=get_project)

    sp = ps.add_parser("add")
    sp.add_argument("name")
    sp.add_argument("--parent-id")
    sp.add_argument("--color")
    sp.add_argument("--view-style", choices=["list", "board", "calendar"])
    sp.add_argument("--favorite", action="store_true", default=None)
    sp.set_defaults(func=add_project)

    sp = ps.add_parser("update")
    sp.add_argument("project_id")
    sp.add_argument("--name")
    sp.add_argument("--color")
    sp.add_argument("--view-style", choices=["list", "board", "calendar"])
    sp.add_argument("--favorite", action="store_true", default=None)
    sp.set_defaults(func=update_project)

    sp = ps.add_parser("archive")
    sp.add_argument("project_id")
    sp.set_defaults(func=archive_project)

    sp = ps.add_parser("unarchive")
    sp.add_argument("project_id")
    sp.set_defaults(func=unarchive_project)

    sp = ps.add_parser("delete")
    sp.add_argument("project_id")
    sp.set_defaults(func=delete_project)

    p = sub.add_parser("sections", help="Section operations")
    ps = p.add_subparsers(dest="action", required=True)

    sp = ps.add_parser("list")
    sp.add_argument("--project-id")
    sp.set_defaults(func=list_sections)

    sp = ps.add_parser("get")
    sp.add_argument("section_id")
    sp.set_defaults(func=get_section)

    sp = ps.add_parser("add")
    sp.add_argument("project_id")
    sp.add_argument("name")
    sp.add_argument("--order", type=int)
    sp.set_defaults(func=add_section)

    sp = ps.add_parser("update")
    sp.add_argument("section_id")
    sp.add_argument("name")
    sp.add_argument("--order", type=int)
    sp.set_defaults(func=update_section)

    sp = ps.add_parser(
        "move",
        help="Not supported by Todoist REST; kept for compatibility",
        description=(
            "Todoist REST does not expose a section move operation. "
            "This command is retained for CLI compatibility and fails with a clear error."
        ),
    )
    sp.add_argument("section_id")
    sp.add_argument("project_id")
    sp.set_defaults(func=move_section)

    sp = ps.add_parser("archive")
    sp.add_argument("section_id")
    sp.set_defaults(func=archive_section)

    sp = ps.add_parser("unarchive")
    sp.add_argument("section_id")
    sp.set_defaults(func=unarchive_section)

    sp = ps.add_parser("delete")
    sp.add_argument("section_id")
    sp.set_defaults(func=delete_section)

    p = sub.add_parser("labels", help="Label operations")
    ps = p.add_subparsers(dest="action", required=True)

    sp = ps.add_parser("list")
    sp.set_defaults(func=list_labels)

    sp = ps.add_parser(
        "search",
        help="Search labels via Todoist API /labels/search",
        description="Search labels via Todoist API /labels/search",
    )
    sp.add_argument("name")
    sp.add_argument("--exact", action="store_true")
    sp.set_defaults(func=search_labels)

    sp = ps.add_parser("get")
    sp.add_argument("label_id")
    sp.set_defaults(func=get_label)

    sp = ps.add_parser("add")
    sp.add_argument("name")
    sp.add_argument("--color")
    sp.add_argument("--order", type=int)
    sp.add_argument("--favorite", action="store_true", default=None)
    sp.set_defaults(func=add_label)

    sp = ps.add_parser("update")
    sp.add_argument("label_id")
    sp.add_argument("--name")
    sp.add_argument("--color")
    sp.add_argument("--order", type=int)
    sp.add_argument("--favorite", action="store_true", default=None)
    sp.set_defaults(func=update_label)

    sp = ps.add_parser("delete")
    sp.add_argument("label_id")
    sp.set_defaults(func=delete_label)

    p = sub.add_parser(
        "comments",
        help="Comment operations",
        description=(
            "Use comments for long notes, logs, or structured text. "
            "Prefer add-file or add-stdin for multi-line content to avoid shell quoting issues."
        ),
    )
    ps = p.add_subparsers(dest="action", required=True)

    sp = ps.add_parser("list")
    sp.add_argument("--task-id")
    sp.add_argument("--project-id")
    sp.set_defaults(func=list_comments)

    sp = ps.add_parser("add", help="Add a short inline comment")
    target = sp.add_mutually_exclusive_group(required=True)
    target.add_argument("--task-id")
    target.add_argument("--project-id")
    sp.add_argument("content")
    sp.add_argument("--attachment")
    sp.set_defaults(func=add_comment)

    sp = ps.add_parser(
        "add-file",
        help="Add a comment from a UTF-8 text file",
        description="Read comment content from a UTF-8 file. Use this for long or structured notes.",
    )
    target = sp.add_mutually_exclusive_group(required=True)
    target.add_argument("--task-id")
    target.add_argument("--project-id")
    sp.add_argument("file", help="Path to a UTF-8 text file containing the comment body")
    sp.add_argument("--attachment")
    sp.set_defaults(func=add_comment_from_file)

    sp = ps.add_parser(
        "add-stdin",
        help="Add a comment by reading UTF-8 text from stdin",
        description="Read comment content from stdin. Use this for here-docs, pipes, or generated text.",
    )
    target = sp.add_mutually_exclusive_group(required=True)
    target.add_argument("--task-id")
    target.add_argument("--project-id")
    sp.add_argument("--attachment")
    sp.set_defaults(func=add_comment_from_stdin)

    p = sub.add_parser("uploads", help="Upload files for comment attachments")
    ps = p.add_subparsers(dest="action", required=True)
    sp = ps.add_parser("add")
    sp.add_argument("file")
    sp.set_defaults(func=upload_only)

    p = sub.add_parser("resolve", help="Resolve project/section names and optionally fetch tasks concurrently")
    p.add_argument("--project")
    p.add_argument("--section")
    p.add_argument("--task-filter", nargs="?", const="")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=resolve)

    return parser


async def main_async() -> int:
    parser = configure_parser()
    args = parser.parse_args()
    try:
        result = await args.func(args)
        print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
        return 0
    except TodoistError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


def main() -> int:
    return asyncio.run(main_async())


if __name__ == "__main__":
    raise SystemExit(main())
