#!/usr/bin/env python3
"""
Todoist API helper for Agent Skills.

Non-interactive by design:
- accepts all input via flags
- prints structured output to stdout
- prints diagnostics to stderr
- supports dry-runs and explicit confirmations for risky operations

Environment:
  TODOIST_API_TOKEN or TODOIST_TOKEN

Typical usage:
  python3 scripts/todoist_api.py get-projects --limit 10
  python3 scripts/todoist_api.py resolve-project --name "Inbox"
  python3 scripts/todoist_api.py ensure-section --project-name "Client Alpha" --name "Next Actions"
  python3 scripts/todoist_api.py bulk-close-tasks --filter "overdue & @errands" --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

VERSION = "2.0.0"
DEFAULT_BASE_URL = "https://api.todoist.com/api/v1"
USER_AGENT = f"todoist-api-skill/{VERSION}"

EXIT_USAGE = 2
EXIT_AUTH = 3
EXIT_NOT_FOUND = 4
EXIT_API = 5
EXIT_OTHER = 6


class ClientError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        payload: Any = None,
        exit_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.payload = payload
        self.exit_code = exit_code or self._default_exit_code(status)

    @staticmethod
    def _default_exit_code(status: int | None) -> int:
        if status in {401, 403}:
            return EXIT_AUTH
        if status == 404:
            return EXIT_NOT_FOUND
        if status is not None:
            return EXIT_API
        return EXIT_OTHER


def stderr(message: str) -> None:
    print(message, file=sys.stderr)


def emit_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(
        f"invalid boolean value: {value!r}. Use one of true/false/yes/no/1/0."
    )


def parse_json_text(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"invalid JSON: {exc}") from exc


def load_json_text(value: str | None, file_path: str | None) -> Any:
    if value and file_path:
        raise ClientError("Provide either --json or --json-file, not both.", exit_code=EXIT_USAGE)
    if file_path:
        try:
            return json.loads(Path(file_path).read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ClientError(f"JSON file not found: {file_path}", exit_code=EXIT_USAGE) from exc
        except json.JSONDecodeError as exc:
            raise ClientError(f"Invalid JSON in file {file_path}: {exc}", exit_code=EXIT_USAGE) from exc
    if value:
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ClientError(f"Invalid JSON supplied to --json: {exc}", exit_code=EXIT_USAGE) from exc
    return None


def parse_kv_pairs(pairs: list[str] | None) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise ClientError(
                f"Invalid key=value pair: {pair!r}. Use repeated --query key=value or --form key=value.",
                exit_code=EXIT_USAGE,
            )
        key, value = pair.split("=", 1)
        key = key.strip()
        if not key:
            raise ClientError(f"Invalid key=value pair: {pair!r}. Key must not be empty.", exit_code=EXIT_USAGE)
        parsed[key] = value
    return parsed


def get_token(args: argparse.Namespace, *, allow_missing: bool = False) -> str:
    token = args.token or os.getenv("TODOIST_API_TOKEN") or os.getenv("TODOIST_TOKEN")
    if token:
        return token
    if allow_missing:
        return "DRY_RUN_TOKEN"
    raise ClientError("Missing Todoist token. Pass --token or set TODOIST_API_TOKEN.", exit_code=EXIT_USAGE)


def with_base(base_url: str, path: str) -> str:
    base = base_url.rstrip("/")
    if not path.startswith("/"):
        path = "/" + path
    return f"{base}{path}"


def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    result = dict(headers)
    if "Authorization" in result:
        result["Authorization"] = "Bearer ***REDACTED***"
    return result


def preview_request(
    method: str,
    url: str,
    headers: dict[str, str],
    *,
    json_body: Any = None,
    form_body: dict[str, str] | None = None,
    query: dict[str, Any] | None = None,
) -> dict[str, Any]:
    preview: dict[str, Any] = {
        "method": method,
        "url": url,
        "headers": redact_headers(headers),
    }
    if query:
        preview["query"] = query
    if json_body is not None:
        preview["json_body"] = json_body
    if form_body is not None:
        preview["form_body"] = form_body
    return preview


def retry_delay_from_payload(payload: Any) -> float | None:
    if not isinstance(payload, dict):
        return None
    extra = payload.get("error_extra")
    if isinstance(extra, dict):
        retry_after = extra.get("retry_after")
        try:
            if retry_after is not None:
                return float(retry_after)
        except (TypeError, ValueError):
            return None
    return None


def api_request(
    *,
    method: str,
    base_url: str,
    path: str,
    token: str,
    timeout: int,
    retry: int,
    retry_backoff: float,
    verbose: bool,
    query: dict[str, Any] | None = None,
    json_body: Any = None,
    form_body: dict[str, str] | None = None,
) -> Any:
    if json_body is not None and form_body is not None:
        raise ClientError("Internal error: cannot send JSON and form data together.")
    url = with_base(base_url, path)
    if query:
        encoded_query = urllib.parse.urlencode(
            {k: v for k, v in query.items() if v is not None},
            doseq=True,
        )
        if encoded_query:
            url = f"{url}?{encoded_query}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }

    data: bytes | None = None
    if json_body is not None:
        data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif form_body is not None:
        data = urllib.parse.urlencode(form_body).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    for attempt in range(retry + 1):
        if verbose:
            stderr(f"{method} {url} (attempt {attempt + 1}/{retry + 1})")
        request = urllib.request.Request(url=url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read()
                if not raw:
                    return None
                content_type = response.headers.get("Content-Type", "")
                text = raw.decode("utf-8", errors="replace")
                if "application/json" in content_type or text.lstrip().startswith(("{", "[", "null")):
                    return json.loads(text)
                return {"text": text}
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            try:
                payload: Any = json.loads(body) if body else None
            except json.JSONDecodeError:
                payload = {"error": body} if body else None
            retry_after: float | None = None
            header_retry = exc.headers.get("Retry-After")
            if header_retry:
                try:
                    retry_after = float(header_retry)
                except ValueError:
                    retry_after = None
            retry_after = retry_after if retry_after is not None else retry_delay_from_payload(payload)
            should_retry = exc.code in {429, 500, 502, 503, 504} and attempt < retry
            if should_retry:
                delay = retry_after if retry_after is not None else min(retry_backoff * (2 ** attempt), 10.0)
                if verbose:
                    stderr(f"retrying after HTTP {exc.code} in {delay:.2f}s")
                time.sleep(max(delay, 0.0))
                continue
            message = f"HTTP {exc.code}"
            if isinstance(payload, dict) and payload.get("error"):
                message = str(payload["error"])
            raise ClientError(message, status=exc.code, payload=payload) from exc
        except urllib.error.URLError as exc:
            if attempt < retry:
                delay = min(retry_backoff * (2 ** attempt), 10.0)
                if verbose:
                    stderr(f"retrying after network error in {delay:.2f}s: {exc.reason}")
                time.sleep(delay)
                continue
            raise ClientError(f"Network error: {exc.reason}", exit_code=EXIT_OTHER) from exc


def paginate(
    *,
    args: argparse.Namespace,
    path: str,
    params: dict[str, Any] | None = None,
    results_key: str = "results",
) -> dict[str, Any] | Any:
    query = dict(params or {})
    page_size = max(1, min(args.limit, 200))
    if args.max_items is not None:
        page_size = min(page_size, max(1, args.max_items))

    def fetch_page(cursor: str | None, request_limit: int) -> Any:
        page_query = dict(query)
        page_query["limit"] = request_limit
        if cursor:
            page_query["cursor"] = cursor
        return api_request(
            method="GET",
            base_url=args.base_url,
            path=path,
            token=get_token(args),
            query=page_query,
            timeout=args.timeout,
            retry=args.retry,
            retry_backoff=args.retry_backoff,
            verbose=args.verbose,
        )

    if not args.all:
        page = fetch_page(args.cursor, page_size)
        if isinstance(page, dict) and results_key in page and args.max_items is not None:
            items = list(page.get(results_key) or [])
            if len(items) > args.max_items:
                items = items[: args.max_items]
            result = dict(page)
            result[results_key] = items
            result["truncated"] = bool(page.get("next_cursor")) or len(items) >= args.max_items
            return result
        return page

    all_items: list[Any] = []
    cursor = args.cursor
    truncated = False
    next_cursor: str | None = None

    while True:
        remaining = None if args.max_items is None else max(args.max_items - len(all_items), 0)
        if remaining == 0:
            truncated = True
            next_cursor = cursor
            break
        request_limit = page_size if remaining is None else max(1, min(page_size, remaining))
        page = fetch_page(cursor, request_limit)
        if not isinstance(page, dict) or results_key not in page:
            return page
        page_items = list(page.get(results_key) or [])
        all_items.extend(page_items)
        next_cursor = page.get("next_cursor")
        if args.max_items is not None and len(all_items) >= args.max_items:
            all_items = all_items[: args.max_items]
            truncated = bool(next_cursor)
            break
        if not next_cursor:
            break
        cursor = next_cursor

    return {results_key: all_items, "next_cursor": next_cursor, "truncated": truncated}


def clean_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


def require_any_of(args: argparse.Namespace, *names: str) -> None:
    if not any(getattr(args, name) is not None for name in names):
        wanted = ", ".join(f"--{name.replace('_', '-')}" for name in names)
        raise ClientError(f"At least one of {wanted} is required.", exit_code=EXIT_USAGE)


def require_exactly_one_of(args: argparse.Namespace, *names: str) -> None:
    supplied = [name for name in names if getattr(args, name) is not None]
    if len(supplied) != 1:
        wanted = ", ".join(f"--{name.replace('_', '-')}" for name in names)
        raise ClientError(f"Exactly one of {wanted} is required.", exit_code=EXIT_USAGE)


def require_confirm_or_dry_run(args: argparse.Namespace, what: str) -> None:
    if getattr(args, "dry_run", False) or getattr(args, "confirm", False):
        return
    raise ClientError(
        f"{what} is risky. Re-run with --dry-run to preview or --confirm to execute.",
        exit_code=EXIT_USAGE,
    )


def todoist_link(kind: str, object_id: str | int) -> str:
    if kind == "task":
        return f"todoist://task?id={object_id}"
    if kind == "project":
        return f"todoist://project?id={object_id}"
    return ""


def add_links(data: Any, *, kind: str | None = None) -> Any:
    if not kind:
        return data
    if isinstance(data, dict) and data.get("id") is not None:
        copy = dict(data)
        url = todoist_link(kind, copy["id"])
        if url:
            copy["todoist_url"] = url
        return copy
    return data


def make_envelope(
    action: str,
    *,
    args: argparse.Namespace | None = None,
    data: Any = None,
    warnings: list[str] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    envelope: dict[str, Any] = {
        "ok": True,
        "action": action,
        "dry_run": bool(getattr(args, "dry_run", False)) if args is not None else False,
    }
    if data is not None:
        envelope["data"] = data
        if isinstance(data, dict):
            if "results" in data and isinstance(data["results"], list):
                envelope["count"] = len(data["results"])
                if "next_cursor" in data:
                    envelope["next_cursor"] = data.get("next_cursor")
                if "truncated" in data:
                    envelope["truncated"] = bool(data.get("truncated"))
            elif "items" in data and isinstance(data["items"], list):
                envelope["count"] = len(data["items"])
                if "next_cursor" in data:
                    envelope["next_cursor"] = data.get("next_cursor")
                if "truncated" in data:
                    envelope["truncated"] = bool(data.get("truncated"))
        elif isinstance(data, list):
            envelope["count"] = len(data)
    if warnings:
        envelope["warnings"] = warnings
    envelope.update(extra)
    return envelope


def summary_line_for_item(item: Any) -> str:
    if not isinstance(item, dict):
        return json.dumps(item, ensure_ascii=False)
    for key in ("name", "content", "email", "status", "id"):
        if item.get(key):
            head = f"{key}={item[key]!r}"
            break
    else:
        head = json.dumps(item, ensure_ascii=False)
    if item.get("id") and "id=" not in head:
        head += f" id={item['id']!r}"
    return head


def render_summary(payload: dict[str, Any]) -> str:
    lines = [f"action: {payload.get('action')}", f"ok: {payload.get('ok')}"]
    for key in (
        "dry_run",
        "count",
        "matched_count",
        "changed_count",
        "skipped_count",
        "next_cursor",
        "truncated",
        "output_file",
    ):
        if key in payload:
            lines.append(f"{key}: {payload[key]}")
    data = payload.get("data")
    if isinstance(data, dict):
        if "preview" in payload and isinstance(payload["preview"], dict):
            lines.append("preview: request available in JSON output")
        elif "id" in data or "name" in data or "content" in data or "email" in data:
            lines.append(summary_line_for_item(data))
        elif "results" in data and isinstance(data["results"], list):
            for item in data["results"][:10]:
                lines.append(f"- {summary_line_for_item(item)}")
        elif "items" in data and isinstance(data["items"], list):
            for item in data["items"][:10]:
                lines.append(f"- {summary_line_for_item(item)}")
    if isinstance(data, list):
        for item in data[:10]:
            lines.append(f"- {summary_line_for_item(item)}")
    if payload.get("warnings"):
        lines.append("warnings:")
        for warning in payload["warnings"]:
            lines.append(f"- {warning}")
    return "\n".join(lines)


def write_output(payload: dict[str, Any], args: argparse.Namespace) -> None:
    if args.format == "summary":
        rendered = render_summary(payload)
    else:
        rendered = emit_json(payload)

    if args.output and args.output != "-":
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + ("" if rendered.endswith("\n") else "\n"), encoding="utf-8")
        notice = make_envelope(
            payload.get("action", "command"),
            args=args,
            output_file=str(output_path),
            format=args.format,
            count=payload.get("count"),
            matched_count=payload.get("matched_count"),
            changed_count=payload.get("changed_count"),
            truncated=payload.get("truncated"),
        )
        sys.stdout.write(emit_json(notice) + "\n")
        return

    sys.stdout.write(rendered)
    if not rendered.endswith("\n"):
        sys.stdout.write("\n")


def request_headers(token: str, *, json_body: bool = False, form_body: bool = False) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if json_body:
        headers["Content-Type"] = "application/json"
    if form_body:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    return headers


def list_from_results(payload: Any) -> list[Any]:
    if isinstance(payload, dict):
        if "results" in payload and isinstance(payload["results"], list):
            return payload["results"]
        if "items" in payload and isinstance(payload["items"], list):
            return payload["items"]
    if isinstance(payload, list):
        return payload
    raise ClientError("Expected a list-like response from Todoist.", exit_code=EXIT_OTHER)


def lower_name(item: dict[str, Any]) -> str:
    for key in ("name", "content"):
        value = item.get(key)
        if isinstance(value, str):
            return value.lower()
    return ""


def compact_candidates(items: Iterable[dict[str, Any]], *, kind: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in items:
        row = {"id": item.get("id")}
        if "name" in item:
            row["name"] = item.get("name")
        if "content" in item:
            row["content"] = item.get("content")
        if kind == "section" and item.get("project_id") is not None:
            row["project_id"] = item.get("project_id")
        out.append(row)
    return out


def resolve_single_name(
    *,
    items: list[dict[str, Any]],
    name: str,
    kind: str,
    strict: bool,
) -> dict[str, Any]:
    target = name.strip().lower()
    exact = [item for item in items if lower_name(item) == target]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise ClientError(
            f"Ambiguous {kind} name {name!r}: {len(exact)} exact matches.",
            payload={"candidates": compact_candidates(exact[:20], kind=kind)},
            exit_code=EXIT_API,
        )

    if strict:
        raise ClientError(
            f"No {kind} found with exact name {name!r}.",
            status=404,
            payload={"candidates": compact_candidates(items[:20], kind=kind)},
            exit_code=EXIT_NOT_FOUND,
        )

    starts = [item for item in items if lower_name(item).startswith(target)]
    if len(starts) == 1:
        return starts[0]
    contains = [item for item in items if target in lower_name(item)]
    if len(contains) == 1:
        return contains[0]

    candidates = starts or contains
    if not candidates:
        raise ClientError(
            f"No {kind} found matching {name!r}.",
            status=404,
            exit_code=EXIT_NOT_FOUND,
        )
    raise ClientError(
        f"Ambiguous {kind} name {name!r}: {len(candidates)} candidates.",
        payload={"candidates": compact_candidates(candidates[:20], kind=kind)},
        exit_code=EXIT_API,
    )


def get_all_projects(args: argparse.Namespace, *, include_archived: bool = False) -> list[dict[str, Any]]:
    active_args = argparse.Namespace(**vars(args))
    active_args.all = True
    active_args.cursor = None
    active = paginate(args=active_args, path="/projects")
    items = list_from_results(active)
    if include_archived:
        archived = paginate(args=active_args, path="/projects/archived")
        items.extend(list_from_results(archived))
    return items


def get_all_sections(
    args: argparse.Namespace,
    *,
    project_id: str | None = None,
    include_archived: bool = False,
) -> list[dict[str, Any]]:
    work_args = argparse.Namespace(**vars(args))
    work_args.all = True
    work_args.cursor = None
    active = paginate(args=work_args, path="/sections", params={"project_id": project_id})
    items = list_from_results(active)
    if include_archived:
        archived = paginate(args=work_args, path="/sections/archived", params={"project_id": project_id})
        items.extend(list_from_results(archived))
    return items


def get_all_labels(args: argparse.Namespace, *, include_shared: bool = False) -> list[dict[str, Any]]:
    work_args = argparse.Namespace(**vars(args))
    work_args.all = True
    work_args.cursor = None
    labels = list_from_results(paginate(args=work_args, path="/labels"))
    if include_shared:
        shared_payload = api_request(
            method="GET",
            base_url=args.base_url,
            path="/labels/shared",
            token=get_token(args),
            timeout=args.timeout,
            retry=args.retry,
            retry_backoff=args.retry_backoff,
            verbose=args.verbose,
        )
        if isinstance(shared_payload, dict) and "results" in shared_payload:
            labels.extend(list(shared_payload.get("results") or []))
        elif isinstance(shared_payload, list):
            labels.extend(shared_payload)
    return labels


def resolve_project_id(args: argparse.Namespace, *, project_id: str | None, project_name: str | None, strict: bool) -> str | None:
    if project_id:
        return project_id
    if project_name:
        project = resolve_single_name(
            items=get_all_projects(args, include_archived=True),
            name=project_name,
            kind="project",
            strict=strict,
        )
        return str(project["id"])
    return None


def resolve_section_id(
    args: argparse.Namespace,
    *,
    section_id: str | None,
    section_name: str | None,
    project_id: str | None,
    project_name: str | None,
    strict: bool,
) -> str | None:
    if section_id:
        return section_id
    if section_name:
        project_resolved = resolve_project_id(args, project_id=project_id, project_name=project_name, strict=strict)
        sections = get_all_sections(args, project_id=project_resolved, include_archived=True)
        section = resolve_single_name(items=sections, name=section_name, kind="section", strict=strict)
        return str(section["id"])
    return None


def resolve_label_id(args: argparse.Namespace, *, label_id: str | None, label_name: str | None, strict: bool) -> str | None:
    if label_id:
        return label_id
    if label_name:
        label = resolve_single_name(
            items=get_all_labels(args, include_shared=True),
            name=label_name,
            kind="label",
            strict=strict,
        )
        return str(label["id"])
    return None


def get_tasks_by_filter_all(args: argparse.Namespace, query: str, lang: str | None) -> list[dict[str, Any]]:
    work_args = argparse.Namespace(**vars(args))
    work_args.all = True
    work_args.cursor = None
    response = paginate(args=work_args, path="/tasks/filter", params={"query": query, "lang": lang})
    return list_from_results(response)


def do_get_projects(args: argparse.Namespace) -> dict[str, Any]:
    return make_envelope("get-projects", args=args, data=paginate(args=args, path="/projects"))


def do_get_archived_projects(args: argparse.Namespace) -> dict[str, Any]:
    return make_envelope("get-archived-projects", args=args, data=paginate(args=args, path="/projects/archived"))


def do_search_projects(args: argparse.Namespace) -> dict[str, Any]:
    data = paginate(args=args, path="/projects/search", params={"query": args.query})
    return make_envelope("search-projects", args=args, data=data)


def do_get_project(args: argparse.Namespace) -> dict[str, Any]:
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path=f"/projects/{args.project_id}",
        token=get_token(args),
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("get-project", args=args, data=add_links(data, kind="project"))


def do_get_project_collaborators(args: argparse.Namespace) -> dict[str, Any]:
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path=f"/projects/{args.project_id}/collaborators",
        token=get_token(args),
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("get-project-collaborators", args=args, data=data)


def do_get_project_full(args: argparse.Namespace) -> dict[str, Any]:
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path=f"/projects/{args.project_id}/full",
        token=get_token(args),
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("get-project-full", args=args, data=data)


def do_create_project(args: argparse.Namespace) -> dict[str, Any]:
    body = clean_dict(
        {
            "name": args.name,
            "description": args.description,
            "parent_id": args.parent_id,
            "color": args.color,
            "is_favorite": args.is_favorite,
            "view_style": args.view_style,
            "workspace_id": args.workspace_id,
        }
    )
    token = get_token(args, allow_missing=args.dry_run)
    if args.dry_run:
        url = with_base(args.base_url, "/projects")
        return make_envelope(
            "create-project",
            args=args,
            preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body),
        )
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path="/projects",
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("create-project", args=args, data=add_links(data, kind="project"))


def do_update_project(args: argparse.Namespace) -> dict[str, Any]:
    require_any_of(args, "name", "description", "color", "is_favorite", "view_style", "child_order")
    body = clean_dict(
        {
            "name": args.name,
            "description": args.description,
            "color": args.color,
            "is_favorite": args.is_favorite,
            "view_style": args.view_style,
            "child_order": args.child_order,
        }
    )
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/projects/{args.project_id}"
    if args.dry_run:
        url = with_base(args.base_url, path)
        return make_envelope(
            "update-project",
            args=args,
            preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body),
        )
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("update-project", args=args, data=add_links(data, kind="project"))


def do_delete_project(args: argparse.Namespace) -> dict[str, Any]:
    require_confirm_or_dry_run(args, "Deleting a project")
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/projects/{args.project_id}"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope(
            "delete-project",
            args=args,
            preview=preview_request("DELETE", url, request_headers(token)),
        )
    api_request(
        method="DELETE",
        base_url=args.base_url,
        path=path,
        token=token,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("delete-project", args=args, data={"status": "ok", "id": args.project_id})


def do_archive_project(args: argparse.Namespace) -> dict[str, Any]:
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/projects/{args.project_id}/archive"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("archive-project", args=args, preview=preview_request("POST", url, request_headers(token)))
    api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("archive-project", args=args, data={"status": "ok", "id": args.project_id})


def do_unarchive_project(args: argparse.Namespace) -> dict[str, Any]:
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/projects/{args.project_id}/unarchive"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("unarchive-project", args=args, preview=preview_request("POST", url, request_headers(token)))
    api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("unarchive-project", args=args, data={"status": "ok", "id": args.project_id})


def do_resolve_project(args: argparse.Namespace) -> dict[str, Any]:
    project = resolve_single_name(
        items=get_all_projects(args, include_archived=args.include_archived),
        name=args.name,
        kind="project",
        strict=args.strict,
    )
    return make_envelope("resolve-project", args=args, data=add_links(project, kind="project"))


def do_ensure_project(args: argparse.Namespace) -> dict[str, Any]:
    existing = None
    try:
        existing = resolve_single_name(
            items=get_all_projects(args, include_archived=False),
            name=args.name,
            kind="project",
            strict=True,
        )
    except ClientError as exc:
        if exc.exit_code != EXIT_NOT_FOUND:
            raise
    warnings: list[str] = []
    if existing is not None:
        if not args.update_existing:
            return make_envelope(
                "ensure-project",
                args=args,
                data=add_links(existing, kind="project"),
                created=False,
                updated=False,
                resolved={"project_id": existing.get("id")},
            )
        body = clean_dict(
            {
                "name": args.name,
                "description": args.description,
                "color": args.color,
                "is_favorite": args.is_favorite,
                "view_style": args.view_style,
            }
        )
        if len(body) == 1 and "name" in body:
            warnings.append("Project already existed with the same name; no fields requested for update.")
            return make_envelope(
                "ensure-project",
                args=args,
                data=add_links(existing, kind="project"),
                created=False,
                updated=False,
                resolved={"project_id": existing.get("id")},
                warnings=warnings,
            )
        token = get_token(args, allow_missing=args.dry_run)
        path = f"/projects/{existing['id']}"
        url = with_base(args.base_url, path)
        if args.dry_run:
            return make_envelope(
                "ensure-project",
                args=args,
                created=False,
                updated=True,
                resolved={"project_id": existing.get("id")},
                preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body),
            )
        updated = api_request(
            method="POST",
            base_url=args.base_url,
            path=path,
            token=token,
            json_body=body,
            timeout=args.timeout,
            retry=args.retry,
            retry_backoff=args.retry_backoff,
            verbose=args.verbose,
        )
        return make_envelope(
            "ensure-project",
            args=args,
            data=add_links(updated, kind="project"),
            created=False,
            updated=True,
            resolved={"project_id": existing.get("id")},
        )

    create_args = argparse.Namespace(**vars(args))
    return_value = do_create_project(create_args)
    return_value["action"] = "ensure-project"
    return_value["created"] = True
    return_value["updated"] = False
    if isinstance(return_value.get("data"), dict):
        return_value["resolved"] = {"project_id": return_value["data"].get("id")}
    return return_value


def do_get_sections(args: argparse.Namespace) -> dict[str, Any]:
    data = paginate(args=args, path="/sections", params={"project_id": args.project_id})
    return make_envelope("get-sections", args=args, data=data)


def do_get_archived_sections(args: argparse.Namespace) -> dict[str, Any]:
    data = paginate(args=args, path="/sections/archived", params={"project_id": args.project_id})
    return make_envelope("get-archived-sections", args=args, data=data)


def do_search_sections(args: argparse.Namespace) -> dict[str, Any]:
    data = paginate(args=args, path="/sections/search", params={"query": args.query, "project_id": args.project_id})
    return make_envelope("search-sections", args=args, data=data)


def do_get_section(args: argparse.Namespace) -> dict[str, Any]:
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path=f"/sections/{args.section_id}",
        token=get_token(args),
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("get-section", args=args, data=data)


def do_create_section(args: argparse.Namespace) -> dict[str, Any]:
    body = clean_dict({"name": args.name, "project_id": args.project_id, "order": args.order})
    token = get_token(args, allow_missing=args.dry_run)
    path = "/sections"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("create-section", args=args, preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body))
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("create-section", args=args, data=data)


def do_update_section(args: argparse.Namespace) -> dict[str, Any]:
    require_any_of(args, "name", "section_order", "is_collapsed")
    body = clean_dict({"name": args.name, "section_order": args.section_order, "is_collapsed": args.is_collapsed})
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/sections/{args.section_id}"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("update-section", args=args, preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body))
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("update-section", args=args, data=data)


def do_delete_section(args: argparse.Namespace) -> dict[str, Any]:
    require_confirm_or_dry_run(args, "Deleting a section")
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/sections/{args.section_id}"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("delete-section", args=args, preview=preview_request("DELETE", url, request_headers(token)))
    api_request(
        method="DELETE",
        base_url=args.base_url,
        path=path,
        token=token,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("delete-section", args=args, data={"status": "ok", "id": args.section_id})


def do_archive_section(args: argparse.Namespace) -> dict[str, Any]:
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/sections/{args.section_id}/archive"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("archive-section", args=args, preview=preview_request("POST", url, request_headers(token)))
    api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("archive-section", args=args, data={"status": "ok", "id": args.section_id})


def do_unarchive_section(args: argparse.Namespace) -> dict[str, Any]:
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/sections/{args.section_id}/unarchive"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("unarchive-section", args=args, preview=preview_request("POST", url, request_headers(token)))
    api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("unarchive-section", args=args, data={"status": "ok", "id": args.section_id})


def do_resolve_section(args: argparse.Namespace) -> dict[str, Any]:
    project_id = resolve_project_id(
        args,
        project_id=args.project_id,
        project_name=args.project_name,
        strict=args.strict,
    )
    section = resolve_single_name(
        items=get_all_sections(args, project_id=project_id, include_archived=args.include_archived),
        name=args.name,
        kind="section",
        strict=args.strict,
    )
    return make_envelope("resolve-section", args=args, data=section)


def do_ensure_section(args: argparse.Namespace) -> dict[str, Any]:
    project_id = resolve_project_id(args, project_id=args.project_id, project_name=args.project_name, strict=args.strict)
    if not project_id:
        raise ClientError("ensure-section requires --project-id or --project-name.", exit_code=EXIT_USAGE)

    existing = None
    try:
        existing = resolve_single_name(
            items=get_all_sections(args, project_id=project_id, include_archived=False),
            name=args.name,
            kind="section",
            strict=True,
        )
    except ClientError as exc:
        if exc.exit_code != EXIT_NOT_FOUND:
            raise

    if existing is not None:
        if not args.update_existing:
            return make_envelope(
                "ensure-section",
                args=args,
                data=existing,
                created=False,
                updated=False,
                resolved={"project_id": project_id, "section_id": existing.get("id")},
            )
        body = clean_dict({"name": args.name, "section_order": args.section_order, "is_collapsed": args.is_collapsed})
        if not body:
            return make_envelope(
                "ensure-section",
                args=args,
                data=existing,
                created=False,
                updated=False,
                resolved={"project_id": project_id, "section_id": existing.get("id")},
            )
        token = get_token(args, allow_missing=args.dry_run)
        path = f"/sections/{existing['id']}"
        url = with_base(args.base_url, path)
        if args.dry_run:
            return make_envelope(
                "ensure-section",
                args=args,
                created=False,
                updated=True,
                resolved={"project_id": project_id, "section_id": existing.get("id")},
                preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body),
            )
        updated = api_request(
            method="POST",
            base_url=args.base_url,
            path=path,
            token=token,
            json_body=body,
            timeout=args.timeout,
            retry=args.retry,
            retry_backoff=args.retry_backoff,
            verbose=args.verbose,
        )
        return make_envelope(
            "ensure-section",
            args=args,
            data=updated,
            created=False,
            updated=True,
            resolved={"project_id": project_id, "section_id": existing.get("id")},
        )

    create_args = argparse.Namespace(**vars(args))
    create_args.project_id = project_id
    result = do_create_section(create_args)
    result["action"] = "ensure-section"
    result["created"] = True
    result["updated"] = False
    if isinstance(result.get("data"), dict):
        result["resolved"] = {"project_id": project_id, "section_id": result["data"].get("id")}
    return result


def do_get_labels(args: argparse.Namespace) -> dict[str, Any]:
    data = paginate(args=args, path="/labels")
    return make_envelope("get-labels", args=args, data=data)


def do_get_shared_labels(args: argparse.Namespace) -> dict[str, Any]:
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path="/labels/shared",
        token=get_token(args),
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("get-shared-labels", args=args, data=data)


def do_search_labels(args: argparse.Namespace) -> dict[str, Any]:
    data = paginate(args=args, path="/labels/search", params={"query": args.query})
    return make_envelope("search-labels", args=args, data=data)


def do_get_label(args: argparse.Namespace) -> dict[str, Any]:
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path=f"/labels/{args.label_id}",
        token=get_token(args),
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("get-label", args=args, data=data)


def do_create_label(args: argparse.Namespace) -> dict[str, Any]:
    body = clean_dict({"name": args.name, "order": args.order, "color": args.color, "is_favorite": args.is_favorite})
    token = get_token(args, allow_missing=args.dry_run)
    path = "/labels"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("create-label", args=args, preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body))
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("create-label", args=args, data=data)


def do_update_label(args: argparse.Namespace) -> dict[str, Any]:
    require_any_of(args, "name", "order", "color", "is_favorite")
    body = clean_dict({"name": args.name, "order": args.order, "color": args.color, "is_favorite": args.is_favorite})
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/labels/{args.label_id}"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("update-label", args=args, preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body))
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("update-label", args=args, data=data)


def do_delete_label(args: argparse.Namespace) -> dict[str, Any]:
    require_confirm_or_dry_run(args, "Deleting a label")
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/labels/{args.label_id}"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("delete-label", args=args, preview=preview_request("DELETE", url, request_headers(token)))
    api_request(
        method="DELETE",
        base_url=args.base_url,
        path=path,
        token=token,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("delete-label", args=args, data={"status": "ok", "id": args.label_id})


def do_resolve_label(args: argparse.Namespace) -> dict[str, Any]:
    label = resolve_single_name(
        items=get_all_labels(args, include_shared=args.include_shared),
        name=args.name,
        kind="label",
        strict=args.strict,
    )
    return make_envelope("resolve-label", args=args, data=label)


def do_ensure_label(args: argparse.Namespace) -> dict[str, Any]:
    existing = None
    try:
        existing = resolve_single_name(
            items=get_all_labels(args, include_shared=False),
            name=args.name,
            kind="label",
            strict=True,
        )
    except ClientError as exc:
        if exc.exit_code != EXIT_NOT_FOUND:
            raise

    if existing is not None:
        if not args.update_existing:
            return make_envelope(
                "ensure-label",
                args=args,
                data=existing,
                created=False,
                updated=False,
                resolved={"label_id": existing.get("id")},
            )
        body = clean_dict({"name": args.name, "order": args.order, "color": args.color, "is_favorite": args.is_favorite})
        token = get_token(args, allow_missing=args.dry_run)
        path = f"/labels/{existing['id']}"
        url = with_base(args.base_url, path)
        if args.dry_run:
            return make_envelope(
                "ensure-label",
                args=args,
                created=False,
                updated=True,
                resolved={"label_id": existing.get("id")},
                preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body),
            )
        updated = api_request(
            method="POST",
            base_url=args.base_url,
            path=path,
            token=token,
            json_body=body,
            timeout=args.timeout,
            retry=args.retry,
            retry_backoff=args.retry_backoff,
            verbose=args.verbose,
        )
        return make_envelope(
            "ensure-label",
            args=args,
            data=updated,
            created=False,
            updated=True,
            resolved={"label_id": existing.get("id")},
        )

    result = do_create_label(args)
    result["action"] = "ensure-label"
    result["created"] = True
    result["updated"] = False
    if isinstance(result.get("data"), dict):
        result["resolved"] = {"label_id": result["data"].get("id")}
    return result


def build_task_body(args: argparse.Namespace) -> dict[str, Any]:
    body = clean_dict(
        {
            "content": getattr(args, "content", None),
            "description": getattr(args, "description", None),
            "project_id": getattr(args, "project_id", None),
            "section_id": getattr(args, "section_id", None),
            "parent_id": getattr(args, "parent_id", None),
            "order": getattr(args, "order", None),
            "labels": getattr(args, "labels", None),
            "priority": getattr(args, "priority", None),
            "assignee_id": getattr(args, "assignee_id", None),
            "due_string": getattr(args, "due_string", None),
            "due_date": getattr(args, "due_date", None),
            "due_datetime": getattr(args, "due_datetime", None),
            "due_lang": getattr(args, "due_lang", None),
            "duration": getattr(args, "duration", None),
            "duration_unit": getattr(args, "duration_unit", None),
            "deadline_date": getattr(args, "deadline_date", None),
            "child_order": getattr(args, "child_order", None),
            "is_collapsed": getattr(args, "is_collapsed", None),
        }
    )
    return body


def do_get_tasks(args: argparse.Namespace) -> dict[str, Any]:
    params = {
        "project_id": args.project_id,
        "section_id": args.section_id,
        "parent_id": args.parent_id,
        "label": args.label,
        "ids": args.ids,
    }
    data = paginate(args=args, path="/tasks", params=params)
    if isinstance(data, dict) and isinstance(data.get("results"), list):
        data = dict(data)
        data["results"] = [add_links(item, kind="task") for item in data["results"]]
    return make_envelope("get-tasks", args=args, data=data)


def do_get_tasks_by_filter(args: argparse.Namespace) -> dict[str, Any]:
    data = paginate(args=args, path="/tasks/filter", params={"query": args.query, "lang": args.lang})
    if isinstance(data, dict) and isinstance(data.get("results"), list):
        data = dict(data)
        data["results"] = [add_links(item, kind="task") for item in data["results"]]
    return make_envelope("get-tasks-by-filter", args=args, data=data)


def do_get_task(args: argparse.Namespace) -> dict[str, Any]:
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path=f"/tasks/{args.task_id}",
        token=get_token(args),
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("get-task", args=args, data=add_links(data, kind="task"))


def do_quick_add_task(args: argparse.Namespace) -> dict[str, Any]:
    body = clean_dict(
        {
            "text": args.text,
            "note": args.note,
            "reminder": args.reminder,
            "auto_reminder": args.auto_reminder,
            "meta": args.meta,
        }
    )
    token = get_token(args, allow_missing=args.dry_run)
    path = "/tasks/quick"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("quick-add-task", args=args, preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body))
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("quick-add-task", args=args, data=add_links(data, kind="task"))


def do_create_task(args: argparse.Namespace) -> dict[str, Any]:
    body = build_task_body(args)
    token = get_token(args, allow_missing=args.dry_run)
    path = "/tasks"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("create-task", args=args, preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body))
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("create-task", args=args, data=add_links(data, kind="task"))


def do_update_task(args: argparse.Namespace) -> dict[str, Any]:
    require_any_of(
        args,
        "content",
        "description",
        "labels",
        "priority",
        "due_string",
        "due_date",
        "due_datetime",
        "due_lang",
        "assignee_id",
        "duration",
        "duration_unit",
        "deadline_date",
        "child_order",
        "is_collapsed",
    )
    body = build_task_body(args)
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/tasks/{args.task_id}"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("update-task", args=args, preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body))
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("update-task", args=args, data=add_links(data, kind="task"))


def do_move_task(args: argparse.Namespace) -> dict[str, Any]:
    require_any_of(args, "project_id", "section_id")
    body = clean_dict({"project_id": args.project_id, "section_id": args.section_id})
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/tasks/{args.task_id}/move"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("move-task", args=args, preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body))
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("move-task", args=args, data=add_links(data, kind="task"))


def do_close_task(args: argparse.Namespace) -> dict[str, Any]:
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/tasks/{args.task_id}/close"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("close-task", args=args, preview=preview_request("POST", url, request_headers(token)))
    api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("close-task", args=args, data={"status": "ok", "id": args.task_id, "todoist_url": todoist_link("task", args.task_id)})


def do_reopen_task(args: argparse.Namespace) -> dict[str, Any]:
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/tasks/{args.task_id}/reopen"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("reopen-task", args=args, preview=preview_request("POST", url, request_headers(token)))
    api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("reopen-task", args=args, data={"status": "ok", "id": args.task_id, "todoist_url": todoist_link("task", args.task_id)})


def do_delete_task(args: argparse.Namespace) -> dict[str, Any]:
    require_confirm_or_dry_run(args, "Deleting a task")
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/tasks/{args.task_id}"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("delete-task", args=args, preview=preview_request("DELETE", url, request_headers(token)))
    api_request(
        method="DELETE",
        base_url=args.base_url,
        path=path,
        token=token,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("delete-task", args=args, data={"status": "ok", "id": args.task_id})


def do_get_completed_tasks(args: argparse.Namespace) -> dict[str, Any]:
    path = "/tasks/completed/by_completion_date" if args.by == "completion" else "/tasks/completed/by_due_date"
    params = {
        "since": args.since,
        "until": args.until,
        "workspace_id": args.workspace_id,
        "project_id": args.project_id,
        "section_id": args.section_id,
        "parent_id": args.parent_id,
        "filter_query": args.filter_query,
        "filter_lang": args.filter_lang,
    }
    data = paginate(args=args, path=path, params=params, results_key="items")
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        data = dict(data)
        data["items"] = [add_links(item, kind="task") for item in data["items"]]
    return make_envelope("get-completed-tasks", args=args, data=data, by=args.by)


def do_get_completed_stats(args: argparse.Namespace) -> dict[str, Any]:
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path="/tasks/completed/stats",
        token=get_token(args),
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("get-completed-stats", args=args, data=data)


def do_create_comment(args: argparse.Namespace) -> dict[str, Any]:
    require_exactly_one_of(args, "task_id", "project_id")
    body = clean_dict(
        {
            "content": args.content,
            "task_id": args.task_id,
            "project_id": args.project_id,
            "uids_to_notify": args.uids_to_notify,
        }
    )
    token = get_token(args, allow_missing=args.dry_run)
    path = "/comments"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("create-comment", args=args, preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body))
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("create-comment", args=args, data=data)


def do_get_comments(args: argparse.Namespace) -> dict[str, Any]:
    require_exactly_one_of(args, "task_id", "project_id")
    params = {"task_id": args.task_id, "project_id": args.project_id}
    data = paginate(args=args, path="/comments", params=params)
    return make_envelope("get-comments", args=args, data=data)


def do_get_comment(args: argparse.Namespace) -> dict[str, Any]:
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path=f"/comments/{args.comment_id}",
        token=get_token(args),
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("get-comment", args=args, data=data)


def do_update_comment(args: argparse.Namespace) -> dict[str, Any]:
    body = {"content": args.content}
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/comments/{args.comment_id}"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("update-comment", args=args, preview=preview_request("POST", url, request_headers(token, json_body=True), json_body=body))
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("update-comment", args=args, data=data)


def do_delete_comment(args: argparse.Namespace) -> dict[str, Any]:
    require_confirm_or_dry_run(args, "Deleting a comment")
    token = get_token(args, allow_missing=args.dry_run)
    path = f"/comments/{args.comment_id}"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("delete-comment", args=args, preview=preview_request("DELETE", url, request_headers(token)))
    api_request(
        method="DELETE",
        base_url=args.base_url,
        path=path,
        token=token,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("delete-comment", args=args, data={"status": "ok", "id": args.comment_id})


def do_get_activities(args: argparse.Namespace) -> dict[str, Any]:
    params = clean_dict(
        {
            "object_type": args.object_type,
            "object_id": args.object_id,
            "parent_project_id": args.parent_project_id,
            "parent_item_id": args.parent_item_id,
            "initiator_id": args.initiator_id,
            "event_type": args.event_type,
        }
    )
    data = paginate(args=args, path="/activities", params=params)
    return make_envelope("get-activities", args=args, data=data)


def do_ids_map(args: argparse.Namespace) -> dict[str, Any]:
    ids = args.ids or ",".join(args.id or [])
    if not ids:
        raise ClientError("ids-map requires --ids or repeated --id.", exit_code=EXIT_USAGE)
    path = f"/ids_mapping/{args.object_name}/{ids}"
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path=path,
        token=get_token(args),
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("ids-map", args=args, data=data, object_name=args.object_name)


def do_get_backups(args: argparse.Namespace) -> dict[str, Any]:
    params = clean_dict({"mfa_token": args.mfa_token})
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path="/backups",
        token=get_token(args),
        query=params,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("get-backups", args=args, data=data)


def do_get_or_create_email(args: argparse.Namespace) -> dict[str, Any]:
    body = {"obj_type": args.obj_type, "obj_id": args.obj_id}
    token = get_token(args, allow_missing=args.dry_run)
    path = "/emails"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("get-or-create-email", args=args, preview=preview_request("PUT", url, request_headers(token, json_body=True), json_body=body))
    data = api_request(
        method="PUT",
        base_url=args.base_url,
        path=path,
        token=token,
        json_body=body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("get-or-create-email", args=args, data=data)


def do_disable_email(args: argparse.Namespace) -> dict[str, Any]:
    token = get_token(args, allow_missing=args.dry_run)
    path = "/emails"
    url = with_base(args.base_url, path)
    query = {"obj_type": args.obj_type, "obj_id": args.obj_id}
    if args.dry_run:
        query_str = urllib.parse.urlencode(query)
        return make_envelope(
            "disable-email",
            args=args,
            preview=preview_request("DELETE", f"{url}?{query_str}", request_headers(token), query=query),
        )
    data = api_request(
        method="DELETE",
        base_url=args.base_url,
        path=path,
        token=token,
        query=query,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("disable-email", args=args, data=data)


def do_template_export_url(args: argparse.Namespace) -> dict[str, Any]:
    params = {"project_id": args.project_id, "use_relative_dates": str(args.use_relative_dates).lower()}
    data = api_request(
        method="GET",
        base_url=args.base_url,
        path="/templates/url",
        token=get_token(args),
        query=params,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("template-export-url", args=args, data=data)


def do_sync(args: argparse.Namespace) -> dict[str, Any]:
    commands = load_json_text(args.commands, args.commands_file)
    resource_types = load_json_text(args.resource_types, args.resource_types_file)
    if commands is not None and not isinstance(commands, list):
        raise ClientError("--commands / --commands-file must decode to a JSON array.", exit_code=EXIT_USAGE)
    if resource_types is not None and not isinstance(resource_types, list):
        raise ClientError("--resource-types / --resource-types-file must decode to a JSON array.", exit_code=EXIT_USAGE)

    sync_token = args.sync_token
    if sync_token is None and resource_types is not None:
        sync_token = "*"

    form_body: dict[str, str] = {}
    if sync_token is not None:
        form_body["sync_token"] = sync_token
    if resource_types is not None:
        form_body["resource_types"] = json.dumps(resource_types, ensure_ascii=False, separators=(",", ":"))
    if commands is not None:
        form_body["commands"] = json.dumps(commands, ensure_ascii=False, separators=(",", ":"))

    token = get_token(args, allow_missing=args.dry_run)
    path = "/sync"
    url = with_base(args.base_url, path)
    if args.dry_run:
        return make_envelope("sync", args=args, preview=preview_request("POST", url, request_headers(token, form_body=True), form_body=form_body))
    data = api_request(
        method="POST",
        base_url=args.base_url,
        path=path,
        token=token,
        form_body=form_body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("sync", args=args, data=data)


def do_raw(args: argparse.Namespace) -> dict[str, Any]:
    method = args.method.upper()
    if method == "GET" and (args.json or args.json_file):
        raise ClientError("GET requests do not accept --json / --json-file. Use --query instead.", exit_code=EXIT_USAGE)
    if method != "GET" and args.all:
        raise ClientError("--all is only supported for GET requests.", exit_code=EXIT_USAGE)
    if method == "DELETE":
        require_confirm_or_dry_run(args, "DELETE request")

    token = get_token(args, allow_missing=args.dry_run)
    path = args.path
    query = parse_kv_pairs(args.query)
    json_body = load_json_text(args.json, args.json_file)

    if method == "GET":
        if args.limit is not None:
            query["limit"] = args.limit
        if args.cursor is not None:
            query["cursor"] = args.cursor
        if args.all and not args.dry_run:
            base_params = {k: v for k, v in query.items() if k not in {"limit", "cursor"}}
            results_key = args.results_key
            accumulated: list[Any] = []
            cursor = args.cursor
            next_cursor: str | None = None
            truncated = False
            while True:
                page_params = dict(base_params)
                page_params["limit"] = min(args.limit, 200)
                if args.max_items is not None:
                    remaining = args.max_items - len(accumulated)
                    if remaining <= 0:
                        truncated = True
                        break
                    page_params["limit"] = max(1, min(page_params["limit"], remaining))
                if cursor:
                    page_params["cursor"] = cursor
                page = api_request(
                    method="GET",
                    base_url=args.base_url,
                    path=path,
                    token=token,
                    query=page_params,
                    timeout=args.timeout,
                    retry=args.retry,
                    retry_backoff=args.retry_backoff,
                    verbose=args.verbose,
                )
                if not isinstance(page, dict):
                    return make_envelope("raw", args=args, data=page, method=method, path=path)
                key = results_key
                if key == "auto":
                    if "results" in page and isinstance(page["results"], list):
                        key = "results"
                    elif "items" in page and isinstance(page["items"], list):
                        key = "items"
                    else:
                        return make_envelope("raw", args=args, data=page, method=method, path=path)
                if key not in page or not isinstance(page.get(key), list):
                    return make_envelope("raw", args=args, data=page, method=method, path=path)
                accumulated.extend(list(page.get(key) or []))
                next_cursor = page.get("next_cursor")
                if args.max_items is not None and len(accumulated) >= args.max_items:
                    accumulated = accumulated[: args.max_items]
                    truncated = bool(next_cursor)
                    break
                if not next_cursor:
                    break
                cursor = next_cursor
            data = {key: accumulated, "next_cursor": next_cursor, "truncated": truncated}
            return make_envelope("raw", args=args, data=data, method=method, path=path)

    url = with_base(args.base_url, path)
    query_str = urllib.parse.urlencode(query, doseq=True)
    if query_str:
        url = f"{url}?{query_str}"
    headers = request_headers(token, json_body=json_body is not None)

    if args.dry_run:
        return make_envelope("raw", args=args, preview=preview_request(method, url, headers, json_body=json_body, query=query))
    data = api_request(
        method=method,
        base_url=args.base_url,
        path=path,
        token=token,
        query=query,
        json_body=json_body,
        timeout=args.timeout,
        retry=args.retry,
        retry_backoff=args.retry_backoff,
        verbose=args.verbose,
    )
    return make_envelope("raw", args=args, data=data, method=method, path=path)


def do_bulk_close_tasks(args: argparse.Namespace) -> dict[str, Any]:
    require_confirm_or_dry_run(args, "Bulk close")
    tasks = get_tasks_by_filter_all(args, args.filter, args.lang)
    matched_count = len(tasks)
    actions = []
    for task in tasks:
        actions.append(
            {
                "task_id": task.get("id"),
                "content": task.get("content"),
                "todoist_url": todoist_link("task", task.get("id")),
            }
        )

    if args.dry_run:
        return make_envelope(
            "bulk-close-tasks",
            args=args,
            matched_count=matched_count,
            changed_count=len(actions),
            skipped_count=0,
            data=actions,
            resolved={"filter": args.filter},
        )

    changed: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    token = get_token(args)
    for task in tasks:
        task_id = task.get("id")
        try:
            api_request(
                method="POST",
                base_url=args.base_url,
                path=f"/tasks/{task_id}/close",
                token=token,
                timeout=args.timeout,
                retry=args.retry,
                retry_backoff=args.retry_backoff,
                verbose=args.verbose,
            )
            changed.append({"task_id": task_id, "content": task.get("content"), "todoist_url": todoist_link("task", task_id)})
        except ClientError as exc:
            errors.append({"task_id": task_id, "error": str(exc), "status": exc.status})
    return make_envelope(
        "bulk-close-tasks",
        args=args,
        data=changed,
        matched_count=matched_count,
        changed_count=len(changed),
        skipped_count=0,
        errors=errors,
        resolved={"filter": args.filter},
    )


def do_bulk_move_tasks(args: argparse.Namespace) -> dict[str, Any]:
    require_confirm_or_dry_run(args, "Bulk move")
    require_any_of(args, "target_project_id", "target_project_name", "target_section_id", "target_section_name")
    target_project_id = resolve_project_id(
        args,
        project_id=args.target_project_id,
        project_name=args.target_project_name,
        strict=args.strict,
    )
    target_section_id = resolve_section_id(
        args,
        section_id=args.target_section_id,
        section_name=args.target_section_name,
        project_id=target_project_id,
        project_name=None,
        strict=args.strict,
    )

    tasks = get_tasks_by_filter_all(args, args.filter, args.lang)
    matched_count = len(tasks)
    changes: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    for task in tasks:
        same_project = target_project_id is None or str(task.get("project_id")) == str(target_project_id)
        same_section = target_section_id is None or str(task.get("section_id")) == str(target_section_id)
        if same_project and same_section:
            skipped.append(
                {"task_id": task.get("id"), "content": task.get("content"), "reason": "already at target"}
            )
            continue
        change = {
            "task_id": task.get("id"),
            "content": task.get("content"),
            "from_project_id": task.get("project_id"),
            "from_section_id": task.get("section_id"),
            "to_project_id": target_project_id,
            "to_section_id": target_section_id,
            "todoist_url": todoist_link("task", task.get("id")),
        }
        changes.append(change)

    resolved = {"filter": args.filter, "project_id": target_project_id, "section_id": target_section_id}
    if args.dry_run:
        return make_envelope(
            "bulk-move-tasks",
            args=args,
            data=changes,
            matched_count=matched_count,
            changed_count=len(changes),
            skipped_count=len(skipped),
            skipped=skipped,
            resolved=resolved,
        )

    changed: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    token = get_token(args)
    for change in changes:
        body = clean_dict({"project_id": target_project_id, "section_id": target_section_id})
        try:
            api_request(
                method="POST",
                base_url=args.base_url,
                path=f"/tasks/{change['task_id']}/move",
                token=token,
                json_body=body,
                timeout=args.timeout,
                retry=args.retry,
                retry_backoff=args.retry_backoff,
                verbose=args.verbose,
            )
            changed.append(change)
        except ClientError as exc:
            errors.append({"task_id": change["task_id"], "error": str(exc), "status": exc.status})

    return make_envelope(
        "bulk-move-tasks",
        args=args,
        data=changed,
        matched_count=matched_count,
        changed_count=len(changed),
        skipped_count=len(skipped),
        skipped=skipped,
        errors=errors,
        resolved=resolved,
    )


def do_bulk_comment_tasks(args: argparse.Namespace) -> dict[str, Any]:
    require_confirm_or_dry_run(args, "Bulk comment")
    tasks = get_tasks_by_filter_all(args, args.filter, args.lang)
    matched_count = len(tasks)
    previews = [
        {
            "task_id": task.get("id"),
            "content": task.get("content"),
            "comment": args.content,
            "todoist_url": todoist_link("task", task.get("id")),
        }
        for task in tasks
    ]
    if args.dry_run:
        return make_envelope(
            "bulk-comment-tasks",
            args=args,
            data=previews,
            matched_count=matched_count,
            changed_count=len(previews),
            skipped_count=0,
            resolved={"filter": args.filter},
        )

    changed: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    token = get_token(args)
    for task in tasks:
        body = clean_dict({"task_id": task.get("id"), "content": args.content, "uids_to_notify": args.uids_to_notify})
        try:
            created = api_request(
                method="POST",
                base_url=args.base_url,
                path="/comments",
                token=token,
                json_body=body,
                timeout=args.timeout,
                retry=args.retry,
                retry_backoff=args.retry_backoff,
                verbose=args.verbose,
            )
            changed.append({"task_id": task.get("id"), "comment_id": getattr(created, "get", lambda *_: None)("id"), "content": task.get("content")})
        except ClientError as exc:
            errors.append({"task_id": task.get("id"), "error": str(exc), "status": exc.status})

    return make_envelope(
        "bulk-comment-tasks",
        args=args,
        data=changed,
        matched_count=matched_count,
        changed_count=len(changed),
        skipped_count=0,
        errors=errors,
        resolved={"filter": args.filter},
    )


def do_report_completed(args: argparse.Namespace) -> dict[str, Any]:
    project_id = resolve_project_id(args, project_id=args.project_id, project_name=args.project_name, strict=args.strict)
    section_id = resolve_section_id(
        args,
        section_id=args.section_id,
        section_name=args.section_name,
        project_id=project_id,
        project_name=None,
        strict=args.strict,
    )
    work_args = argparse.Namespace(**vars(args))
    work_args.project_id = project_id
    work_args.section_id = section_id
    work_args.parent_id = args.parent_id
    work_args.filter_query = args.filter_query
    work_args.filter_lang = args.filter_lang
    raw = do_get_completed_tasks(work_args)
    data = raw.get("data")
    items = list_from_results(data)
    by_project: dict[str, int] = {}
    by_section: dict[str, int] = {}
    for item in items:
        if item.get("project_id") is not None:
            key = str(item["project_id"])
            by_project[key] = by_project.get(key, 0) + 1
        if item.get("section_id") is not None:
            key = str(item["section_id"])
            by_section[key] = by_section.get(key, 0) + 1

    report = {
        "summary": {
            "total_completed": len(items),
            "window": {"since": args.since, "until": args.until, "by": args.by},
            "project_id": project_id,
            "section_id": section_id,
        },
        "by_project_id": by_project,
        "by_section_id": by_section,
        "items": items,
    }
    return make_envelope(
        "report-completed",
        args=args,
        data=report,
        count=len(items),
        resolved={"project_id": project_id, "section_id": section_id},
    )


def add_common_pagination_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--limit", type=int, default=50, help="Page size (default: 50, max: 200).")
    parser.add_argument("--cursor", help="Cursor for a follow-up request.")
    parser.add_argument("--all", action="store_true", help="Fetch pages until next_cursor is null or --max-items is reached.")
    parser.add_argument("--max-items", type=int, help="Hard cap on returned items across all pages.")


def add_write_safety_flags(parser: argparse.ArgumentParser, *, destructive: bool = False) -> None:
    parser.add_argument("--dry-run", action="store_true", help="Preview the request or planned changes without sending writes.")
    if destructive:
        parser.add_argument("--confirm", action="store_true", help="Execute a risky or bulk write after previewing it.")


def add_task_fields(parser: argparse.ArgumentParser, *, require_content: bool = False) -> None:
    parser.add_argument("--content", required=require_content, help="Task content.")
    parser.add_argument("--description", help="Task description.")
    parser.add_argument("--project-id", help="Project ID.")
    parser.add_argument("--section-id", help="Section ID.")
    parser.add_argument("--parent-id", help="Parent task ID.")
    parser.add_argument("--order", type=int, help="Task order within its collection.")
    parser.add_argument("--labels", nargs="+", help="Label names to apply.")
    parser.add_argument("--priority", type=int, choices=[1, 2, 3, 4], help="Task priority 1-4.")
    parser.add_argument("--assignee-id", type=int, help="Assignee user ID for shared projects.")
    parser.add_argument("--due-string", help="Natural-language due date string.")
    parser.add_argument("--due-date", help="Due date string.")
    parser.add_argument("--due-datetime", help="Due datetime string.")
    parser.add_argument("--due-lang", help="Language for due string parsing.")
    parser.add_argument("--duration", type=int, help="Duration amount.")
    parser.add_argument("--duration-unit", choices=["minute", "day"], help="Duration unit.")
    parser.add_argument("--deadline-date", help="Deadline date in YYYY-MM-DD format.")
    parser.add_argument("--child-order", type=int, help="Updated child order.")
    parser.add_argument("--is-collapsed", type=parse_bool, help="Updated collapsed state.")


def make_global_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todoist_api.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            f"""\
            Todoist API helper for Agent Skills (v{VERSION})

            Reads and writes Todoist API v1 with structured output.
            Prefer exact IDs for low-level commands. Use resolve-*, ensure-*, bulk-*,
            and report-* when an agent needs a safer workflow surface.

            Exit codes:
              0 success
              {EXIT_USAGE} invalid CLI usage
              {EXIT_AUTH} auth/permission failure
              {EXIT_NOT_FOUND} not found
              {EXIT_API} API validation or ambiguous resolution
              {EXIT_OTHER} network or unexpected failure
            """
        ),
    )
    parser.add_argument("--token", help="Todoist API token. Defaults to TODOIST_API_TOKEN.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"API base URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds (default: 30).")
    parser.add_argument("--retry", type=int, default=2, help="Retries for 429/5xx/network failures (default: 2).")
    parser.add_argument("--retry-backoff", type=float, default=1.0, help="Initial retry backoff in seconds (default: 1.0).")
    parser.add_argument("--format", choices=["json", "summary"], default="json", help="Stdout format (default: json).")
    parser.add_argument("--output", default="-", help="Write full output to FILE instead of stdout. Use - for stdout.")
    parser.add_argument("--verbose", action="store_true", help="Print request diagnostics to stderr.")
    return parser


def build_parser() -> argparse.ArgumentParser:
    parser = make_global_parser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Projects
    p = subparsers.add_parser("get-projects", help="List active projects.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_get_projects)

    p = subparsers.add_parser("get-archived-projects", help="List archived projects.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_get_archived_projects)

    p = subparsers.add_parser("search-projects", help="Search active projects by name.")
    p.add_argument("--query", required=True, help="Project search query.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_search_projects)

    p = subparsers.add_parser("get-project", help="Get one project by ID.")
    p.add_argument("--project-id", required=True, help="Project ID.")
    p.set_defaults(func=do_get_project)

    p = subparsers.add_parser("get-project-collaborators", help="Get collaborators for a shared project.")
    p.add_argument("--project-id", required=True, help="Project ID.")
    p.set_defaults(func=do_get_project_collaborators)

    p = subparsers.add_parser("get-project-full", help="Get the project-full payload for one project.")
    p.add_argument("--project-id", required=True, help="Project ID.")
    p.set_defaults(func=do_get_project_full)

    p = subparsers.add_parser("create-project", help="Create a project.")
    p.add_argument("--name", required=True, help="Project name.")
    p.add_argument("--description", help="Project description.")
    p.add_argument("--parent-id", help="Parent project ID.")
    p.add_argument("--color", help="Project colour.")
    p.add_argument("--is-favorite", type=parse_bool, help="Favourite state.")
    p.add_argument("--view-style", help="Project view style.")
    p.add_argument("--workspace-id", type=int, help="Workspace ID.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_create_project)

    p = subparsers.add_parser("update-project", help="Update a project.")
    p.add_argument("--project-id", required=True, help="Project ID.")
    p.add_argument("--name", help="Updated project name.")
    p.add_argument("--description", help="Updated project description.")
    p.add_argument("--color", help="Updated colour.")
    p.add_argument("--is-favorite", type=parse_bool, help="Updated favourite state.")
    p.add_argument("--view-style", help="Updated view style.")
    p.add_argument("--child-order", type=int, help="Updated child order.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_update_project)

    p = subparsers.add_parser("delete-project", help="Delete a project.")
    p.add_argument("--project-id", required=True, help="Project ID.")
    add_write_safety_flags(p, destructive=True)
    p.set_defaults(func=do_delete_project)

    p = subparsers.add_parser("archive-project", help="Archive a project.")
    p.add_argument("--project-id", required=True, help="Project ID.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_archive_project)

    p = subparsers.add_parser("unarchive-project", help="Unarchive a project.")
    p.add_argument("--project-id", required=True, help="Project ID.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_unarchive_project)

    p = subparsers.add_parser("resolve-project", help="Resolve a project name to one exact project object.")
    p.add_argument("--name", required=True, help="Project name to resolve.")
    p.add_argument("--strict", action="store_true", help="Require exact case-insensitive name match.")
    p.add_argument("--include-archived", action="store_true", help="Include archived projects when resolving.")
    p.set_defaults(func=do_resolve_project)

    p = subparsers.add_parser("ensure-project", help="Return an existing project or create it.")
    p.add_argument("--name", required=True, help="Exact project name to ensure.")
    p.add_argument("--description", help="Project description for create or update.")
    p.add_argument("--color", help="Project colour for create or update.")
    p.add_argument("--is-favorite", type=parse_bool, help="Favourite state for create or update.")
    p.add_argument("--view-style", help="View style for create or update.")
    p.add_argument("--update-existing", action="store_true", help="Update matching project when it already exists.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_ensure_project)

    # Sections
    p = subparsers.add_parser("get-sections", help="List active sections.")
    p.add_argument("--project-id", help="Limit sections to one project.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_get_sections)

    p = subparsers.add_parser("get-archived-sections", help="List archived sections.")
    p.add_argument("--project-id", help="Limit sections to one project.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_get_archived_sections)

    p = subparsers.add_parser("search-sections", help="Search active sections by name.")
    p.add_argument("--query", required=True, help="Section search query.")
    p.add_argument("--project-id", help="Limit search to one project.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_search_sections)

    p = subparsers.add_parser("get-section", help="Get one section by ID.")
    p.add_argument("--section-id", required=True, help="Section ID.")
    p.set_defaults(func=do_get_section)

    p = subparsers.add_parser("create-section", help="Create a section.")
    p.add_argument("--project-id", required=True, help="Parent project ID.")
    p.add_argument("--name", required=True, help="Section name.")
    p.add_argument("--order", type=int, help="Section order.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_create_section)

    p = subparsers.add_parser("update-section", help="Update a section.")
    p.add_argument("--section-id", required=True, help="Section ID.")
    p.add_argument("--name", help="Updated section name.")
    p.add_argument("--section-order", type=int, help="Updated section order.")
    p.add_argument("--is-collapsed", type=parse_bool, help="Updated collapsed state.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_update_section)

    p = subparsers.add_parser("delete-section", help="Delete a section.")
    p.add_argument("--section-id", required=True, help="Section ID.")
    add_write_safety_flags(p, destructive=True)
    p.set_defaults(func=do_delete_section)

    p = subparsers.add_parser("archive-section", help="Archive a section.")
    p.add_argument("--section-id", required=True, help="Section ID.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_archive_section)

    p = subparsers.add_parser("unarchive-section", help="Unarchive a section.")
    p.add_argument("--section-id", required=True, help="Section ID.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_unarchive_section)

    p = subparsers.add_parser("resolve-section", help="Resolve a section name to one exact section object.")
    p.add_argument("--name", required=True, help="Section name to resolve.")
    p.add_argument("--project-id", help="Project ID scope.")
    p.add_argument("--project-name", help="Project name scope.")
    p.add_argument("--strict", action="store_true", help="Require exact case-insensitive name match.")
    p.add_argument("--include-archived", action="store_true", help="Include archived sections.")
    p.set_defaults(func=do_resolve_section)

    p = subparsers.add_parser("ensure-section", help="Return an existing section or create it.")
    p.add_argument("--project-id", help="Parent project ID.")
    p.add_argument("--project-name", help="Parent project name.")
    p.add_argument("--name", required=True, help="Section name to ensure.")
    p.add_argument("--section-order", type=int, help="Section order for update.")
    p.add_argument("--is-collapsed", type=parse_bool, help="Collapsed state for update.")
    p.add_argument("--strict", action="store_true", help="Require exact name matches during resolution.")
    p.add_argument("--update-existing", action="store_true", help="Update matching section when it already exists.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_ensure_section)

    # Labels
    p = subparsers.add_parser("get-labels", help="List personal labels.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_get_labels)

    p = subparsers.add_parser("get-shared-labels", help="List shared labels.")
    p.set_defaults(func=do_get_shared_labels)

    p = subparsers.add_parser("search-labels", help="Search personal labels by name.")
    p.add_argument("--query", required=True, help="Label search query.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_search_labels)

    p = subparsers.add_parser("get-label", help="Get one label by ID.")
    p.add_argument("--label-id", required=True, help="Label ID.")
    p.set_defaults(func=do_get_label)

    p = subparsers.add_parser("create-label", help="Create a label.")
    p.add_argument("--name", required=True, help="Label name.")
    p.add_argument("--order", type=int, help="Label order.")
    p.add_argument("--color", help="Label colour.")
    p.add_argument("--is-favorite", type=parse_bool, help="Favourite state.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_create_label)

    p = subparsers.add_parser("update-label", help="Update a label.")
    p.add_argument("--label-id", required=True, help="Label ID.")
    p.add_argument("--name", help="Updated label name.")
    p.add_argument("--order", type=int, help="Updated order.")
    p.add_argument("--color", help="Updated colour.")
    p.add_argument("--is-favorite", type=parse_bool, help="Updated favourite state.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_update_label)

    p = subparsers.add_parser("delete-label", help="Delete a personal label.")
    p.add_argument("--label-id", required=True, help="Label ID.")
    add_write_safety_flags(p, destructive=True)
    p.set_defaults(func=do_delete_label)

    p = subparsers.add_parser("resolve-label", help="Resolve a label name to one label object.")
    p.add_argument("--name", required=True, help="Label name to resolve.")
    p.add_argument("--strict", action="store_true", help="Require exact case-insensitive name match.")
    p.add_argument("--include-shared", action="store_true", help="Include shared labels.")
    p.set_defaults(func=do_resolve_label)

    p = subparsers.add_parser("ensure-label", help="Return an existing label or create it.")
    p.add_argument("--name", required=True, help="Label name to ensure.")
    p.add_argument("--order", type=int, help="Label order for create or update.")
    p.add_argument("--color", help="Label colour for create or update.")
    p.add_argument("--is-favorite", type=parse_bool, help="Favourite state for create or update.")
    p.add_argument("--update-existing", action="store_true", help="Update matching label when it already exists.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_ensure_label)

    # Tasks
    p = subparsers.add_parser("get-tasks", help="List active tasks.")
    p.add_argument("--project-id", help="Project ID.")
    p.add_argument("--section-id", help="Section ID.")
    p.add_argument("--parent-id", help="Parent task ID.")
    p.add_argument("--label", help="Filter by label name.")
    p.add_argument("--ids", help="Comma-separated task IDs.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_get_tasks)

    p = subparsers.add_parser("get-tasks-by-filter", help="List active tasks matching a Todoist filter.")
    p.add_argument("--query", required=True, help="Todoist filter query.")
    p.add_argument("--lang", help="Filter language tag, e.g. en, de.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_get_tasks_by_filter)

    p = subparsers.add_parser("get-task", help="Get one task by ID.")
    p.add_argument("--task-id", required=True, help="Task ID.")
    p.set_defaults(func=do_get_task)

    p = subparsers.add_parser("quick-add-task", help="Create a task using Todoist quick add text.")
    p.add_argument("--text", required=True, help="Quick add text.")
    p.add_argument("--note", help="Optional task description/note.")
    p.add_argument("--reminder", help="Reminder text.")
    p.add_argument("--auto-reminder", type=parse_bool, help="Whether Todoist should create an automatic reminder.")
    p.add_argument("--meta", type=parse_bool, help="Whether to return parsing metadata.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_quick_add_task)

    p = subparsers.add_parser("create-task", help="Create a task.")
    add_task_fields(p, require_content=True)
    add_write_safety_flags(p)
    p.set_defaults(func=do_create_task)

    p = subparsers.add_parser("update-task", help="Update a task.")
    p.add_argument("--task-id", required=True, help="Task ID.")
    add_task_fields(p, require_content=False)
    add_write_safety_flags(p)
    p.set_defaults(func=do_update_task)

    p = subparsers.add_parser("move-task", help="Move a task to a project and/or section.")
    p.add_argument("--task-id", required=True, help="Task ID.")
    p.add_argument("--project-id", help="Target project ID.")
    p.add_argument("--section-id", help="Target section ID.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_move_task)

    p = subparsers.add_parser("close-task", help="Complete a task.")
    p.add_argument("--task-id", required=True, help="Task ID.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_close_task)

    p = subparsers.add_parser("reopen-task", help="Reopen a completed task.")
    p.add_argument("--task-id", required=True, help="Task ID.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_reopen_task)

    p = subparsers.add_parser("delete-task", help="Delete a task.")
    p.add_argument("--task-id", required=True, help="Task ID.")
    add_write_safety_flags(p, destructive=True)
    p.set_defaults(func=do_delete_task)

    p = subparsers.add_parser("get-completed-tasks", help="List completed tasks in a time window.")
    p.add_argument("--by", choices=["completion", "due"], default="completion", help="Use completion date or due date window.")
    p.add_argument("--since", required=True, help="Start RFC3339 datetime.")
    p.add_argument("--until", required=True, help="End RFC3339 datetime.")
    p.add_argument("--workspace-id", type=int, help="Workspace ID.")
    p.add_argument("--project-id", help="Project ID.")
    p.add_argument("--section-id", help="Section ID.")
    p.add_argument("--parent-id", help="Parent task ID.")
    p.add_argument("--filter-query", help="Todoist supported filter query.")
    p.add_argument("--filter-lang", help="Filter language.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_get_completed_tasks)

    p = subparsers.add_parser("get-completed-stats", help="Get Todoist completed-task productivity stats.")
    p.set_defaults(func=do_get_completed_stats)

    # Comments
    p = subparsers.add_parser("get-comments", help="List comments for a task or project.")
    p.add_argument("--task-id", help="Task ID.")
    p.add_argument("--project-id", help="Project ID.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_get_comments)

    p = subparsers.add_parser("get-comment", help="Get one comment by ID.")
    p.add_argument("--comment-id", required=True, help="Comment ID.")
    p.set_defaults(func=do_get_comment)

    p = subparsers.add_parser("create-comment", help="Create a comment on a task or project.")
    p.add_argument("--task-id", help="Task ID.")
    p.add_argument("--project-id", help="Project ID.")
    p.add_argument("--content", required=True, help="Comment text.")
    p.add_argument("--uids-to-notify", nargs="+", help="User IDs to notify.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_create_comment)

    p = subparsers.add_parser("update-comment", help="Update a comment.")
    p.add_argument("--comment-id", required=True, help="Comment ID.")
    p.add_argument("--content", required=True, help="Updated comment text.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_update_comment)

    p = subparsers.add_parser("delete-comment", help="Delete a comment.")
    p.add_argument("--comment-id", required=True, help="Comment ID.")
    add_write_safety_flags(p, destructive=True)
    p.set_defaults(func=do_delete_comment)

    # Activity / utility / templates / email
    p = subparsers.add_parser("get-activities", help="List activity events.")
    p.add_argument("--object-type", choices=["project", "item", "note"], help="Object type filter.")
    p.add_argument("--object-id", help="Object ID filter.")
    p.add_argument("--parent-project-id", help="Project scope filter.")
    p.add_argument("--parent-item-id", help="Parent task scope filter.")
    p.add_argument("--initiator-id", help="Initiator user ID.")
    p.add_argument("--event-type", help="Event type filter.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_get_activities)

    p = subparsers.add_parser("ids-map", help="Translate old and new Todoist IDs.")
    p.add_argument("--object-name", required=True, choices=["sections", "tasks", "comments", "reminders", "location_reminders", "projects"], help="Todoist object type.")
    p.add_argument("--ids", help="Comma-separated IDs.")
    p.add_argument("--id", action="append", help="Repeat to supply individual IDs.")
    p.set_defaults(func=do_ids_map)

    p = subparsers.add_parser("get-backups", help="List backup archives.")
    p.add_argument("--mfa-token", help="MFA token if required by Todoist for this endpoint.")
    p.set_defaults(func=do_get_backups)

    p = subparsers.add_parser("get-or-create-email", help="Get or create an email address for a task or project.")
    p.add_argument("--obj-type", required=True, choices=["project", "project_comments", "task"], help="Todoist email object type.")
    p.add_argument("--obj-id", required=True, help="Task or project ID.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_get_or_create_email)

    p = subparsers.add_parser("disable-email", help="Disable an existing task or project email address.")
    p.add_argument("--obj-type", required=True, choices=["project", "project_comments", "task"], help="Todoist email object type.")
    p.add_argument("--obj-id", required=True, help="Task or project ID.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_disable_email)

    p = subparsers.add_parser("template-export-url", help="Get a shareable project template URL.")
    p.add_argument("--project-id", required=True, help="Project ID.")
    p.add_argument("--use-relative-dates", type=parse_bool, default=True, help="Whether to keep relative dates (default: true).")
    p.set_defaults(func=do_template_export_url)

    # Higher-level agent commands
    p = subparsers.add_parser("bulk-close-tasks", help="Resolve a Todoist filter and close all matched tasks.")
    p.add_argument("--filter", required=True, help="Todoist filter query.")
    p.add_argument("--lang", help="Filter language.")
    p.add_argument("--confirm", action="store_true", help="Execute after previewing.")
    p.add_argument("--dry-run", action="store_true", help="Preview matched tasks.")
    p.add_argument("--max-items", type=int, help="Safety cap on matched tasks.")
    p.add_argument("--limit", type=int, default=50, help="Page size for task lookup.")
    p.add_argument("--cursor", help=argparse.SUPPRESS)
    p.add_argument("--all", action="store_true", default=True, help=argparse.SUPPRESS)
    p.set_defaults(func=do_bulk_close_tasks)

    p = subparsers.add_parser("bulk-move-tasks", help="Resolve a filter and move all matched tasks.")
    p.add_argument("--filter", required=True, help="Todoist filter query.")
    p.add_argument("--lang", help="Filter language.")
    p.add_argument("--target-project-id", help="Target project ID.")
    p.add_argument("--target-project-name", help="Target project name.")
    p.add_argument("--target-section-id", help="Target section ID.")
    p.add_argument("--target-section-name", help="Target section name.")
    p.add_argument("--strict", action="store_true", help="Require exact matches during name resolution.")
    p.add_argument("--confirm", action="store_true", help="Execute after previewing.")
    p.add_argument("--dry-run", action="store_true", help="Preview matched tasks and planned moves.")
    p.add_argument("--max-items", type=int, help="Safety cap on matched tasks.")
    p.add_argument("--limit", type=int, default=50, help="Page size for task lookup.")
    p.add_argument("--cursor", help=argparse.SUPPRESS)
    p.add_argument("--all", action="store_true", default=True, help=argparse.SUPPRESS)
    p.set_defaults(func=do_bulk_move_tasks)

    p = subparsers.add_parser("bulk-comment-tasks", help="Resolve a filter and add the same comment to each matched task.")
    p.add_argument("--filter", required=True, help="Todoist filter query.")
    p.add_argument("--lang", help="Filter language.")
    p.add_argument("--content", required=True, help="Comment text to add to each matched task.")
    p.add_argument("--uids-to-notify", nargs="+", help="User IDs to notify.")
    p.add_argument("--confirm", action="store_true", help="Execute after previewing.")
    p.add_argument("--dry-run", action="store_true", help="Preview matched tasks and planned comments.")
    p.add_argument("--max-items", type=int, help="Safety cap on matched tasks.")
    p.add_argument("--limit", type=int, default=50, help="Page size for task lookup.")
    p.add_argument("--cursor", help=argparse.SUPPRESS)
    p.add_argument("--all", action="store_true", default=True, help=argparse.SUPPRESS)
    p.set_defaults(func=do_bulk_comment_tasks)

    p = subparsers.add_parser("report-completed", help="Return completed tasks plus simple counts by project and section.")
    p.add_argument("--by", choices=["completion", "due"], default="completion", help="Use completion date or due date window.")
    p.add_argument("--since", required=True, help="Start RFC3339 datetime.")
    p.add_argument("--until", required=True, help="End RFC3339 datetime.")
    p.add_argument("--project-id", help="Project ID scope.")
    p.add_argument("--project-name", help="Project name scope.")
    p.add_argument("--section-id", help="Section ID scope.")
    p.add_argument("--section-name", help="Section name scope.")
    p.add_argument("--parent-id", help="Parent task scope.")
    p.add_argument("--filter-query", help="Todoist supported filter query.")
    p.add_argument("--filter-lang", help="Filter language.")
    p.add_argument("--strict", action="store_true", help="Require exact matches during name resolution.")
    add_common_pagination_flags(p)
    p.set_defaults(func=do_report_completed)

    # Escape hatches
    p = subparsers.add_parser("sync", help="Call Todoist /sync with form-encoded fields.")
    p.add_argument("--sync-token", help="Sync token. Use * for a full sync.")
    p.add_argument("--resource-types", help='JSON array such as ["all"] or ["projects","items"].')
    p.add_argument("--resource-types-file", help="Path to a JSON file containing resource types.")
    p.add_argument("--commands", help="JSON array of sync commands.")
    p.add_argument("--commands-file", help="Path to a JSON file containing sync commands.")
    add_write_safety_flags(p)
    p.set_defaults(func=do_sync)

    p = subparsers.add_parser("raw", help="Call an arbitrary Todoist endpoint.")
    p.add_argument("--method", required=True, choices=["GET", "POST", "PUT", "DELETE", "PATCH"], help="HTTP method.")
    p.add_argument("--path", required=True, help="Todoist API path, e.g. /projects/123/full.")
    p.add_argument("--query", action="append", help="Repeat key=value query parameters.")
    p.add_argument("--json", help="Inline JSON request body.")
    p.add_argument("--json-file", help="Path to a JSON request body.")
    p.add_argument("--results-key", choices=["auto", "results", "items"], default="auto", help="Pagination list key for GET --all (default: auto).")
    add_common_pagination_flags(p)
    add_write_safety_flags(p, destructive=True)
    p.set_defaults(func=do_raw)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        payload = args.func(args)
        write_output(payload, args)
        return 0
    except ClientError as exc:
        error_payload: dict[str, Any] = {"ok": False, "error": str(exc)}
        if exc.status is not None:
            error_payload["status"] = exc.status
        if exc.payload is not None:
            error_payload["details"] = exc.payload
        stderr(emit_json(error_payload))
        return exc.exit_code
    except KeyboardInterrupt:
        stderr(emit_json({"ok": False, "error": "Interrupted"}))
        return EXIT_OTHER
    except Exception as exc:  # pragma: no cover - defensive fallback for agent scripts
        stderr(emit_json({"ok": False, "error": f"Unexpected error: {exc}"}))
        return EXIT_OTHER


if __name__ == "__main__":
    raise SystemExit(main())
