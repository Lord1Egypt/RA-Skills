#!/usr/bin/env python3
"""
Minimal local server for browsing and editing workflow JSON files.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


SKILL_ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = Path(__file__).resolve().parent / "static"
TEMPLATE_PATH = SKILL_ROOT / "assets" / "workflow-template.json"
SAFE_ID = re.compile(r"^[^\W_][\w-]*$", re.UNICODE)
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from workflow_engine import (  # noqa: E402
    capture_workflow,
    find_matches,
    load_workflows,
    normalize_tools,
    render_execution_brief,
    slugify,
)


@dataclass
class AppConfig:
    workflows_dir: Path
    host: str
    port: int


def ensure_workflows_dir(path: Path) -> Path:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise OSError(
            f"Cannot create or access workflow directory: {path}. "
            "Use a writable path such as './.openclaw/workflows' or '/tmp/workflows'."
        ) from exc
    return path


def load_template() -> dict:
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def workflow_path(workflows_dir: Path, workflow_id: str) -> Path:
    if not SAFE_ID.fullmatch(workflow_id):
        raise ValueError("Workflow id must start with a letter/number and may contain letters, numbers, underscores, or hyphens.")
    return workflows_dir / f"{workflow_id}.json"


def read_workflow(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def list_workflows(workflows_dir: Path) -> list[dict]:
    items: list[dict] = []
    for path in sorted(workflows_dir.glob("*.json")):
        try:
            workflow = read_workflow(path)
        except (json.JSONDecodeError, OSError):
            continue
        stat = path.stat()
        items.append(
            {
                "id": workflow.get("id", path.stem),
                "name": workflow.get("name", path.stem),
                "summary": workflow.get("summary", ""),
                "keywords": workflow.get("match", {}).get("keywords", []),
                "updated_at": int(stat.st_mtime),
            }
        )
    items.sort(key=lambda item: (item["name"] or item["id"]).lower())
    return items


def validate_workflow(payload: object) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Workflow payload must be a JSON object.")
    name = payload.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Workflow name is required.")
    workflow_id = payload.get("id") or slugify(name)
    if not isinstance(workflow_id, str) or not SAFE_ID.fullmatch(workflow_id):
        raise ValueError("Workflow id must start with a letter/number and may contain letters, numbers, underscores, or hyphens.")
    payload["id"] = workflow_id
    if "version" not in payload:
        payload["version"] = 1
    return payload


class WorkflowHandler(BaseHTTPRequestHandler):
    server_version = "WorkStyleMemoryUI/0.1"

    @property
    def config(self) -> AppConfig:
        return self.server.config  # type: ignore[attr-defined]

    def log_message(self, fmt: str, *args: object) -> None:
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path == "/api/meta":
            return self.respond_json(
                {
                    "workflows_dir": str(self.config.workflows_dir),
                    "count": len(list_workflows(self.config.workflows_dir)),
                }
            )
        if path == "/api/template":
            return self.respond_json(load_template())
        if path == "/api/workflows":
            return self.respond_json(list_workflows(self.config.workflows_dir))
        if path.startswith("/api/workflows/"):
            workflow_id = path.rsplit("/", 1)[-1]
            return self.handle_get_workflow(workflow_id)
        return self.serve_static(path)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path == "/api/workflows":
            return self.handle_save_workflow()
        if path == "/api/match":
            return self.handle_match_workflows()
        if path == "/api/capture-draft":
            return self.handle_capture_draft()
        if path == "/api/render-brief":
            return self.handle_render_brief()
        self.respond_error(HTTPStatus.NOT_FOUND, "Unknown endpoint.")

    def do_DELETE(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path.startswith("/api/workflows/"):
            workflow_id = path.rsplit("/", 1)[-1]
            return self.handle_delete_workflow(workflow_id)
        self.respond_error(HTTPStatus.NOT_FOUND, "Unknown endpoint.")

    def handle_get_workflow(self, workflow_id: str) -> None:
        try:
            path = workflow_path(self.config.workflows_dir, workflow_id)
        except ValueError as exc:
            return self.respond_error(HTTPStatus.BAD_REQUEST, str(exc))
        if not path.exists():
            return self.respond_error(HTTPStatus.NOT_FOUND, "Workflow not found.")
        try:
            payload = read_workflow(path)
        except json.JSONDecodeError:
            return self.respond_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Workflow JSON is invalid.")
        self.respond_json(payload)

    def handle_save_workflow(self) -> None:
        body = self.read_json_body()
        if body is None:
            return
        original_id = body.pop("_original_id", None)
        try:
            workflow = validate_workflow(body)
            destination = workflow_path(self.config.workflows_dir, workflow["id"])
        except ValueError as exc:
            return self.respond_error(HTTPStatus.BAD_REQUEST, str(exc))

        if original_id and original_id != workflow["id"]:
            try:
                old_path = workflow_path(self.config.workflows_dir, original_id)
            except ValueError as exc:
                return self.respond_error(HTTPStatus.BAD_REQUEST, str(exc))
            if old_path.exists():
                old_path.unlink()

        destination.write_text(json.dumps(workflow, indent=2) + "\n", encoding="utf-8")
        self.respond_json({"ok": True, "id": workflow["id"]})

    def handle_delete_workflow(self, workflow_id: str) -> None:
        try:
            path = workflow_path(self.config.workflows_dir, workflow_id)
        except ValueError as exc:
            return self.respond_error(HTTPStatus.BAD_REQUEST, str(exc))
        if not path.exists():
            return self.respond_error(HTTPStatus.NOT_FOUND, "Workflow not found.")
        try:
            path.unlink()
        except OSError:
            return self.respond_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Failed to delete workflow.")
        self.respond_json({"ok": True, "id": workflow_id})

    def handle_match_workflows(self) -> None:
        body = self.read_json_body()
        if body is None:
            return
        task = str(body.get("task", "")).strip()
        tools = body.get("tools", [])
        limit = int(body.get("limit", 3))
        tool_list = normalize_tools(tools if isinstance(tools, list) else str(tools).split(","))
        workflows = load_workflows(self.config.workflows_dir)
        matches = find_matches(task, workflows, tools=tool_list, limit=limit)
        suggestion = None
        if matches and matches[0]["score"] >= 0.55:
            top = matches[0]
            suggestion = {
                "workflow_id": top["workflow_id"],
                "name": top["name"],
                "message": f'This looks similar to your "{top["name"]}" workflow. Want to reuse that SOP?',
                "score": top["score"],
            }
        self.respond_json(
            {
                "task": task,
                "tools": tool_list,
                "matches": matches,
                "suggestion": suggestion,
            }
        )

    def handle_capture_draft(self) -> None:
        body = self.read_json_body()
        if body is None:
            return
        task = str(body.get("task", "")).strip()
        steps = body.get("steps", "")
        tools = body.get("tools", [])
        tool_list = normalize_tools(tools if isinstance(tools, list) else str(tools).split(","))
        workflow = capture_workflow(task, raw_steps=steps, tools=tool_list)
        self.respond_json(workflow)

    def handle_render_brief(self) -> None:
        body = self.read_json_body()
        if body is None:
            return
        task = str(body.get("task", "")).strip()
        workflow_id = body.get("workflow_id")
        workflow_payload = body.get("workflow")

        if isinstance(workflow_payload, dict):
            workflow = workflow_payload
        elif isinstance(workflow_id, str) and workflow_id:
            try:
                workflow = read_workflow(workflow_path(self.config.workflows_dir, workflow_id))
            except (ValueError, OSError, json.JSONDecodeError):
                return self.respond_error(HTTPStatus.NOT_FOUND, "Workflow not found.")
        else:
            return self.respond_error(HTTPStatus.BAD_REQUEST, "workflow_id or workflow payload is required.")

        brief = render_execution_brief(workflow, task=task)
        self.respond_json({"brief": brief})

    def read_json_body(self) -> dict | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self.respond_error(HTTPStatus.BAD_REQUEST, "Invalid Content-Length.")
        try:
            payload = self.rfile.read(length).decode("utf-8")
            return json.loads(payload or "{}")
        except json.JSONDecodeError:
            self.respond_error(HTTPStatus.BAD_REQUEST, "Request body must be valid JSON.")
            return None

    def serve_static(self, path: str) -> None:
        if path == "/":
            path = "/index.html"
        candidate = (STATIC_DIR / path.lstrip("/")).resolve()
        if not str(candidate).startswith(str(STATIC_DIR.resolve())) or not candidate.is_file():
            return self.respond_error(HTTPStatus.NOT_FOUND, "File not found.")
        content_type, _ = mimetypes.guess_type(candidate.name)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.end_headers()
        self.wfile.write(candidate.read_bytes())

    def respond_json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def respond_error(self, status: HTTPStatus, message: str) -> None:
        self.respond_json({"ok": False, "error": message}, status=status)


def default_workflows_dir() -> Path:
    cwd = Path.cwd() / ".openclaw" / "workflows"
    if cwd.exists():
        return cwd
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "work-style-memory" / "workflows"
    return cwd


def parse_args() -> AppConfig:
    parser = argparse.ArgumentParser(description="Run the Work Style Memory local UI.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind")
    parser.add_argument(
        "--dir",
        default=str(default_workflows_dir()),
        help="Directory containing workflow JSON files",
    )
    args = parser.parse_args()
    return AppConfig(
        workflows_dir=ensure_workflows_dir(Path(args.dir).expanduser().resolve()),
        host=args.host,
        port=args.port,
    )


def main() -> None:
    try:
        config = parse_args()
    except OSError as exc:
        print(exc)
        raise SystemExit(1)
    server = ThreadingHTTPServer((config.host, config.port), WorkflowHandler)
    server.config = config  # type: ignore[attr-defined]
    print(f"Work Style Memory UI running at http://{config.host}:{config.port}")
    print(f"Workflow directory: {config.workflows_dir}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
