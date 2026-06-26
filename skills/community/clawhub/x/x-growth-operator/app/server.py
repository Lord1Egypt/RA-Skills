from __future__ import annotations

import json
import mimetypes
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.drafting import build_draft
from core.execution import preflight_action, run_x_action
from core.storage import LocalStateStore
from scripts.common import utc_now_iso

APP_DIR = ROOT / "app"
STATIC_DIR = APP_DIR / "static"
DATA_DIR = ROOT / "data"
STORE = LocalStateStore(DATA_DIR)


def load_json_safe(name: str, default):
    payload = STORE.load_json(name, default=default)
    return payload if payload is not None else default


def load_execution_log(limit: int = 25) -> list[dict]:
    path = DATA_DIR / "execution_log.jsonl"
    if not path.exists():
        return []
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    events: list[dict] = []
    for raw in lines[-limit:]:
        try:
            events.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return list(reversed(events))


def load_generated_files() -> list[str]:
    if not DATA_DIR.exists():
        return []
    interesting = []
    for path in sorted(DATA_DIR.glob("*.json")):
        if path.name == ".gitkeep":
            continue
        interesting.append(path.name)
    if (DATA_DIR / "execution_log.jsonl").exists():
        interesting.append("execution_log.jsonl")
    return interesting


def build_dashboard_state() -> dict:
    scored = load_json_safe("opportunities_scored.json", {"items": []})
    plan = load_json_safe("action_plan.json", {"items": []})
    action = load_json_safe("action.json", {})
    return {
        "mission": load_json_safe("mission.json", {}),
        "memory": load_json_safe("memory.json", {}),
        "action_plan": plan,
        "current_action": action,
        "opportunities_scored": scored,
        "feedback_report": load_json_safe("feedback_report.json", {}),
        "execution_log": load_execution_log(),
        "generated_files": load_generated_files(),
    }


def load_action(name: str = "action.json") -> dict:
    payload = load_json_safe(name, {})
    return payload if isinstance(payload, dict) else {}


def draft_action(opportunity_id: str) -> dict:
    mission = STORE.load_mission()
    opportunities_payload = STORE.load_json("opportunities_scored.json", default={"items": []}) or {"items": []}
    opportunities = opportunities_payload.get("items", [])
    opportunity = next((item for item in opportunities if item.get("id") == opportunity_id), None)
    if not opportunity:
        raise ValueError(f"Opportunity not found: {opportunity_id}")

    draft, rationale = build_draft(mission, opportunity)
    action = {
        "id": f"action-{opportunity['id']}",
        "created_at": utc_now_iso(),
        "status": "proposed",
        "mission_name": mission.get("name", ""),
        "opportunity_id": opportunity["id"],
        "action_type": opportunity.get("recommended_action", "observe"),
        "target_url": opportunity.get("url", ""),
        "target_account": opportunity.get("source_account", ""),
        "risk_level": opportunity.get("risk_level", "medium"),
        "score": opportunity.get("score", 0),
        "draft_text": draft,
        "rationale": rationale,
        "requires_approval": True,
    }
    STORE.save_action(action)
    return action


def execute_action(mode: str) -> dict:
    mission = STORE.load_mission()
    action = load_action()
    if not action:
        raise ValueError("No current action to execute.")

    execution_output = None
    preflight_result = None
    if mode == "x-api":
        if action.get("action_type") in {"reply", "quote_post"}:
            preflight_result = preflight_action(action)
            if preflight_result.get("decision") == "block":
                raise ValueError(json.dumps(preflight_result, ensure_ascii=False))
        execution_output = run_x_action(action)

    result = {
        "executed_at": utc_now_iso(),
        "mode": mode,
        "mission_name": mission.get("name", ""),
        "action_id": action.get("id"),
        "action_type": action.get("action_type"),
        "target_url": action.get("target_url"),
        "target_account": action.get("target_account"),
        "draft_text": action.get("draft_text"),
        "status": "recorded" if mode == "record-only" else "executed" if mode == "x-api" else "dry_run_executed",
    }
    if execution_output:
        result["provider_result"] = json.loads(execution_output)
    if preflight_result:
        result["preflight"] = preflight_result

    STORE.append_execution_event(result)
    action["status"] = "executed"
    action["executed_at"] = result["executed_at"]
    action["execution_mode"] = mode
    STORE.save_action(action)
    return result


def read_json_body(handler: BaseHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length", "0"))
    if length <= 0:
        return {}
    raw = handler.rfile.read(length)
    if not raw:
        return {}
    payload = json.loads(raw.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")
    return payload


class DashboardHandler(BaseHTTPRequestHandler):
    server_version = "XGrowthDashboard/1.0"

    def do_GET(self) -> None:  # noqa: N802
        self.handle_request(include_body=True)

    def do_HEAD(self) -> None:  # noqa: N802
        self.handle_request(include_body=False)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            payload = read_json_body(self)
            if parsed.path == "/api/draft":
                action = draft_action(str(payload.get("opportunity_id", "")).strip())
                self.respond_json({"ok": True, "action": action, "state": build_dashboard_state()})
                return
            if parsed.path == "/api/preflight":
                action = load_action()
                if not action:
                    raise ValueError("No current action to preflight.")
                result = preflight_action(action)
                self.respond_json({"ok": result.get("ok", False), "preflight": result})
                return
            if parsed.path == "/api/execute":
                mode = str(payload.get("mode", "dry-run"))
                if mode not in {"dry-run", "record-only", "x-api"}:
                    raise ValueError(f"Unsupported execution mode: {mode}")
                result = execute_action(mode)
                self.respond_json({"ok": True, "execution": result, "state": build_dashboard_state()})
                return
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
        except ValueError as exc:
            self.respond_json({"ok": False, "error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
        except SystemExit as exc:
            self.respond_json({"ok": False, "error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
        except Exception as exc:  # noqa: BLE001
            self.respond_json({"ok": False, "error": str(exc)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return

    def handle_request(self, *, include_body: bool) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/favicon.ico":
            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()
            return
        if parsed.path == "/api/state":
            self.respond_json(build_dashboard_state(), include_body=include_body)
            return
        if parsed.path == "/api/files":
            self.respond_json({"files": load_generated_files()}, include_body=include_body)
            return

        file_path = STATIC_DIR / ("index.html" if parsed.path == "/" else parsed.path.lstrip("/"))
        if not file_path.exists() or not file_path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return

        payload = file_path.read_bytes()
        mime_type, _ = mimetypes.guess_type(file_path.name)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if include_body:
            self.wfile.write(payload)

    def respond_json(
        self,
        payload: dict,
        *,
        include_body: bool = True,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        if include_body:
            self.wfile.write(encoded)


def main() -> int:
    host = "127.0.0.1"
    port = 8787
    server = ThreadingHTTPServer((host, port), DashboardHandler)
    print(f"Dashboard running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
