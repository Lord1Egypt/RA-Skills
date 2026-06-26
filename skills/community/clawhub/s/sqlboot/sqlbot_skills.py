#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import sys
import time
from dataclasses import dataclass, field
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any, Iterable, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin
from urllib.request import HTTPCookieProcessor, OpenerDirector, Request, build_opener

API_PREFIX = "/api/v1"
DEFAULT_ENV_FILE = ".env"
DEFAULT_STATE_FILE = ".sqlbot-skill-state.json"


class SQLBotSkillError(RuntimeError):
    """Base error for this script."""


class ConfigError(SQLBotSkillError):
    """Raised when required configuration is missing or invalid."""


class APIError(SQLBotSkillError):
    """Raised when SQLBot returns an HTTP or business error."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        payload: Any = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


class BrowserError(SQLBotSkillError):
    """Raised when dashboard export in a browser fails."""


@dataclass(frozen=True)
class Workspace:
    id: int
    name: str

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> "Workspace":
        return cls(id=int(payload["id"]), name=str(payload["name"]))

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name}


@dataclass(frozen=True)
class Datasource:
    id: int
    name: str
    description: str | None = None
    type: str | None = None
    type_name: str | None = None
    num: int | None = None
    status: int | None = None
    oid: int | None = None

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> "Datasource":
        return cls(
            id=int(payload["id"]),
            name=str(payload["name"]),
            description=_coalesce(payload.get("description")),
            type=_coalesce(payload.get("type")),
            type_name=_coalesce(payload.get("type_name")),
            num=int(payload["num"]) if payload.get("num") is not None else None,
            status=int(payload["status"]) if payload.get("status") is not None else None,
            oid=int(payload["oid"]) if payload.get("oid") is not None else None,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "type_name": self.type_name,
            "num": self.num,
            "status": self.status,
            "oid": self.oid,
        }


@dataclass
class DashboardNode:
    id: str | None = None
    name: str | None = None
    pid: str | None = None
    node_type: str | None = None
    leaf: bool = False
    type: str | None = None
    create_time: int | None = None
    update_time: int | None = None
    children: list["DashboardNode"] = field(default_factory=list)

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> "DashboardNode":
        return cls(
            id=payload.get("id"),
            name=payload.get("name"),
            pid=payload.get("pid"),
            node_type=payload.get("node_type"),
            leaf=bool(payload.get("leaf", False)),
            type=payload.get("type"),
            create_time=payload.get("create_time"),
            update_time=payload.get("update_time"),
            children=[cls.from_api(item) for item in payload.get("children", [])],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "pid": self.pid,
            "node_type": self.node_type,
            "leaf": self.leaf,
            "type": self.type,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "children": [item.to_dict() for item in self.children],
        }

    def walk(self) -> list["DashboardNode"]:
        flattened = [self]
        for child in self.children:
            flattened.extend(child.walk())
        return flattened


@dataclass(frozen=True)
class SkillSettings:
    base_url: str
    access_key: str
    secret_key: str
    browser_path: str | None
    state_file: str
    timeout: float
    api_key_ttl_seconds: int
    env_file: str | None

    @classmethod
    def load(
        cls,
        *,
        env_file: str | None = None,
        base_url: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
        browser_path: str | None = None,
        state_file: str | None = None,
        timeout: float | None = None,
        api_key_ttl_seconds: int | None = None,
    ) -> "SkillSettings":
        env_values = load_env_file(env_file)
        resolved_base_url = _coalesce(base_url, env_values.get("SQLBOT_BASE_URL"))
        resolved_access_key = _coalesce(access_key, env_values.get("SQLBOT_API_KEY_ACCESS_KEY"))
        resolved_secret_key = _coalesce(secret_key, env_values.get("SQLBOT_API_KEY_SECRET_KEY"))
        resolved_browser_path = _coalesce(browser_path, env_values.get("SQLBOT_BROWSER_PATH"))
        resolved_state_path = _resolve_state_path(state_file, env_values.get("SQLBOT_STATE_FILE"))
        resolved_timeout = _parse_float(
            timeout,
            env_values.get("SQLBOT_TIMEOUT"),
            default=30.0,
            label="SQLBot timeout",
        )
        resolved_ttl = _parse_int(
            api_key_ttl_seconds,
            env_values.get("SQLBOT_API_KEY_TTL_SECONDS"),
            default=300,
            label="SQLBot API key TTL",
        )

        if not resolved_base_url:
            raise ConfigError("Missing SQLBOT_BASE_URL in .env or command arguments.")
        if not resolved_access_key:
            raise ConfigError("Missing SQLBOT_API_KEY_ACCESS_KEY in .env or command arguments.")
        if not resolved_secret_key:
            raise ConfigError("Missing SQLBOT_API_KEY_SECRET_KEY in .env or command arguments.")

        resolved_path = _resolve_env_path(env_file)
        return cls(
            base_url=resolved_base_url,
            access_key=resolved_access_key,
            secret_key=resolved_secret_key,
            browser_path=resolved_browser_path,
            state_file=str(resolved_state_path),
            timeout=resolved_timeout,
            api_key_ttl_seconds=resolved_ttl,
            env_file=str(resolved_path) if resolved_path else None,
        )


@dataclass(frozen=True)
class SkillState:
    current_workspace: Workspace | None = None
    current_datasource: Datasource | None = None

    @classmethod
    def load(cls, path: str | Path) -> "SkillState":
        state_path = Path(path)
        if not state_path.exists():
            return cls()
        decoded = json.loads(state_path.read_text(encoding="utf-8"))
        workspace_payload = decoded.get("current_workspace")
        datasource_payload = decoded.get("current_datasource")
        return cls(
            current_workspace=Workspace.from_api(workspace_payload) if isinstance(workspace_payload, dict) else None,
            current_datasource=Datasource.from_api(datasource_payload) if isinstance(datasource_payload, dict) else None,
        )

    def save(self, path: str | Path) -> None:
        state_path = Path(path)
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            json.dumps(
                {
                    "current_workspace": self.current_workspace.to_dict() if self.current_workspace else None,
                    "current_datasource": self.current_datasource.to_dict() if self.current_datasource else None,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


class OpenerLike(Protocol):
    def open(self, request: Request, timeout: float | None = None):  # pragma: no cover - protocol
        ...


def load_env_file(env_file: str | None = None) -> dict[str, str]:
    path = _resolve_env_path(env_file)
    if path is None:
        return {}
    if not path.exists():
        if env_file:
            raise ConfigError(f".env file not found: {path}")
        return {}

    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            stripped = stripped[len("export ") :].strip()
        if "=" not in stripped:
            continue
        key, raw_value = stripped.split("=", 1)
        key = key.strip()
        value = raw_value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key] = value
    return values


def normalize_api_base_url(base_url: str) -> str:
    if not isinstance(base_url, str):
        raise ConfigError("SQLBot base URL is required.")
    cleaned = base_url.strip().rstrip("/")
    if not cleaned:
        raise ConfigError("SQLBot base URL is required.")
    if cleaned.endswith(API_PREFIX):
        return cleaned
    return f"{cleaned}{API_PREFIX}"


def derive_app_url(base_url: str) -> str:
    normalized = normalize_api_base_url(base_url)
    return normalized[: -len(API_PREFIX)] or normalized


def build_api_key_header(
    *,
    access_key: str,
    secret_key: str,
    ttl_seconds: int = 300,
    now: int | None = None,
) -> str:
    if not access_key:
        raise ConfigError("SQLBot API key access_key is required.")
    if not secret_key:
        raise ConfigError("SQLBot API key secret_key is required.")
    if ttl_seconds <= 0:
        raise ConfigError("SQLBot API key ttl_seconds must be greater than 0.")

    issued_at = int(time.time() if now is None else now)
    payload = {
        "access_key": access_key,
        "iat": issued_at,
        "exp": issued_at + int(ttl_seconds),
    }
    token = _encode_jwt(payload, secret_key)
    return f"sk {token}"


def _encode_jwt(payload: dict[str, Any], secret_key: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_segment = _base64url_json(header)
    payload_segment = _base64url_json(payload)
    signing_input = f"{header_segment}.{payload_segment}".encode("utf-8")
    signature = hmac.new(secret_key.encode("utf-8"), signing_input, hashlib.sha256).digest()
    signature_segment = _base64url_encode(signature)
    return f"{header_segment}.{payload_segment}.{signature_segment}"


def _base64url_json(value: dict[str, Any]) -> str:
    raw = json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return _base64url_encode(raw)


def _base64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _resolve_env_path(env_file: str | None) -> Path | None:
    if env_file:
        return Path(env_file).expanduser()
    skill_path = Path(__file__).resolve().with_name(DEFAULT_ENV_FILE)
    if skill_path.exists():
        return skill_path
    cwd_path = Path.cwd() / DEFAULT_ENV_FILE
    if cwd_path.exists():
        return cwd_path
    return None


def _resolve_state_path(state_file: str | None, env_state_file: str | None = None) -> Path:
    if state_file:
        return Path(state_file).expanduser()
    if env_state_file:
        return Path(env_state_file).expanduser()
    return Path(__file__).resolve().with_name(DEFAULT_STATE_FILE)


def _coalesce(*values: str | None) -> str | None:
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return None


def _parse_float(
    direct_value: float | None,
    env_value: str | None,
    *,
    default: float,
    label: str,
) -> float:
    if direct_value is not None:
        return float(direct_value)
    text = _coalesce(env_value)
    if text is None:
        return default
    try:
        return float(text)
    except ValueError as exc:
        raise ConfigError(f"{label} must be a number.") from exc


def _parse_int(
    direct_value: int | None,
    env_value: str | None,
    *,
    default: int,
    label: str,
) -> int:
    if direct_value is not None:
        return int(direct_value)
    text = _coalesce(env_value)
    if text is None:
        return default
    try:
        return int(text)
    except ValueError as exc:
        raise ConfigError(f"{label} must be an integer.") from exc


class SQLBotClient:
    def __init__(
        self,
        *,
        base_url: str,
        access_key: str,
        secret_key: str,
        api_key_ttl_seconds: int = 300,
        timeout: float = 30.0,
        opener: OpenerDirector | OpenerLike | None = None,
    ) -> None:
        self.api_base_url = normalize_api_base_url(base_url)
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_key_ttl_seconds = int(api_key_ttl_seconds)
        self.timeout = timeout
        self.opener = opener or build_opener(HTTPCookieProcessor(CookieJar()))

    def build_auth_headers(self) -> dict[str, str]:
        return {
            "X-SQLBOT-ASK-TOKEN": build_api_key_header(
                access_key=self.access_key,
                secret_key=self.secret_key,
                ttl_seconds=self.api_key_ttl_seconds,
            )
        }

    def list_workspaces(self) -> list[Workspace]:
        payload = self._request("GET", "/user/ws")
        return [Workspace.from_api(item) for item in payload]

    def resolve_workspace(self, workspace: int | str | Workspace) -> Workspace:
        if isinstance(workspace, Workspace):
            return workspace

        workspaces = self.list_workspaces()
        text_ref = str(workspace).strip()
        if not text_ref:
            raise ConfigError("Workspace reference cannot be empty.")

        if text_ref.isdigit():
            workspace_id = int(text_ref)
            for item in workspaces:
                if item.id == workspace_id:
                    return item

        for item in workspaces:
            if item.name == text_ref:
                return item

        lowered = text_ref.casefold()
        for item in workspaces:
            if item.name.casefold() == lowered:
                return item

        raise APIError(f"Workspace not found: {workspace}")

    def switch_workspace(self, workspace: int | str | Workspace) -> Workspace:
        resolved = self.resolve_workspace(workspace)
        self._request("PUT", f"/user/ws/{resolved.id}")
        return resolved

    def list_datasources(
        self,
        *,
        workspace: int | str | Workspace | None = None,
    ) -> list[Datasource]:
        if workspace is not None:
            self.switch_workspace(workspace)
        payload = self._request("GET", "/datasource/list")
        return [Datasource.from_api(item) for item in payload]

    def resolve_datasource(
        self,
        datasource: int | str | Datasource,
        *,
        workspace: int | str | Workspace | None = None,
    ) -> Datasource:
        if isinstance(datasource, Datasource):
            return datasource

        datasources = self.list_datasources(workspace=workspace)
        text_ref = str(datasource).strip()
        if not text_ref:
            raise ConfigError("Datasource reference cannot be empty.")

        if text_ref.isdigit():
            datasource_id = int(text_ref)
            for item in datasources:
                if item.id == datasource_id:
                    return item

        for item in datasources:
            if item.name == text_ref:
                return item

        lowered = text_ref.casefold()
        for item in datasources:
            if item.name.casefold() == lowered:
                return item

        raise APIError(f"Datasource not found: {datasource}")

    def list_dashboards(
        self,
        *,
        workspace: int | str | Workspace | None = None,
        node_type: str | None = None,
    ) -> list[DashboardNode]:
        if workspace is not None:
            self.switch_workspace(workspace)

        payload: dict[str, Any] = {}
        if node_type:
            payload["node_type"] = node_type
        result = self._request("POST", "/dashboard/list_resource", payload=payload)
        return [DashboardNode.from_api(item) for item in result]

    def get_dashboard(
        self,
        dashboard_id: str,
        *,
        workspace: int | str | Workspace | None = None,
    ) -> dict[str, Any]:
        if workspace is not None:
            self.switch_workspace(workspace)
        if not dashboard_id:
            raise ConfigError("Dashboard ID is required.")
        result = self._request("POST", "/dashboard/load_resource", payload={"id": dashboard_id})
        if not isinstance(result, dict):
            raise APIError("Unexpected dashboard detail response.", payload=result)
        return result

    def start_chat(
        self,
        datasource: int | str | Datasource,
        *,
        question: str | None = None,
    ) -> dict[str, Any]:
        resolved = self.resolve_datasource(datasource)
        payload: dict[str, Any] = {"datasource": resolved.id}
        if question:
            payload["question"] = question
        result = self._request("POST", "/chat/start", payload=payload)
        if not isinstance(result, dict):
            raise APIError("Unexpected chat start response.", payload=result)
        return result

    def get_chat_record_data(self, record_id: int) -> Any:
        return self._request("GET", f"/chat/record/{record_id}/data")

    def ask_data(
        self,
        question: str,
        *,
        datasource: int | str | Datasource | None = None,
        chat_id: int | None = None,
    ) -> dict[str, Any]:
        if not question.strip():
            raise ConfigError("Question cannot be empty.")

        resolved_datasource: Datasource | None = None
        created_chat = False
        if datasource is not None:
            resolved_datasource = self.resolve_datasource(datasource)

        if chat_id is None:
            if resolved_datasource is None:
                raise ConfigError("Datasource is required when starting a new chat.")
            chat = self.start_chat(resolved_datasource)
            chat_id = int(chat["id"])
            created_chat = True

        payload: dict[str, Any] = {"chat_id": chat_id, "question": question}
        if resolved_datasource is not None:
            payload["datasource_id"] = resolved_datasource.id

        events = self._stream_request("POST", "/chat/question", payload=payload)
        result: dict[str, Any] = {
            "chat_id": chat_id,
            "created_chat": created_chat,
            "question": question,
            "datasource": resolved_datasource.to_dict() if resolved_datasource else None,
            "events": events,
        }

        record_id: int | None = None
        sql_answer_parts: list[str] = []
        chart_answer_parts: list[str] = []
        data_loaded = False

        for event in events:
            event_type = event.get("type")
            if event_type == "id":
                record_id = int(event["id"])
                result["record_id"] = record_id
            elif event_type == "brief":
                result["brief"] = event.get("brief")
            elif event_type == "question":
                result["question"] = event.get("question", question)
            elif event_type == "sql-result":
                sql_answer_parts.append(str(event.get("reasoning_content", "")))
            elif event_type == "sql":
                result["sql"] = event.get("content")
            elif event_type == "chart-result":
                chart_answer_parts.append(str(event.get("reasoning_content", "")))
            elif event_type == "chart":
                result["chart"] = event.get("content")
            elif event_type == "datasource" and result["datasource"] is None:
                result["datasource"] = {"id": event.get("id")}
            elif event_type == "error":
                result["error"] = event.get("content")
            elif event_type == "finish":
                result["finished"] = True
            elif event_type == "sql-data" and record_id is not None and not data_loaded:
                result["data"] = self.get_chat_record_data(record_id)
                data_loaded = True

        if sql_answer_parts:
            result["sql_answer"] = "".join(sql_answer_parts)
        if chart_answer_parts:
            result["chart_answer"] = "".join(chart_answer_parts)
        return result

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        url = urljoin(f"{self.api_base_url}/", path.lstrip("/"))
        body: bytes | None = None
        headers = {"Accept": "application/json"}
        headers.update(self.build_auth_headers())
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = Request(url=url, data=body, method=method.upper(), headers=headers)
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                raw = response.read()
        except HTTPError as exc:
            body_text = exc.read().decode("utf-8", errors="replace")
            decoded = self._decode_body(body_text)
            detail = self._extract_error_message(decoded) or body_text or str(exc)
            raise APIError(detail, status_code=exc.code, payload=decoded) from exc
        except URLError as exc:  # pragma: no cover
            raise APIError(f"Failed to reach SQLBot: {exc.reason}") from exc

        if not raw:
            return None

        decoded = self._decode_body(raw.decode("utf-8"))
        if isinstance(decoded, dict) and "code" in decoded:
            if decoded["code"] not in (0, 200):
                message = self._extract_error_message(decoded) or "SQLBot returned an error."
                raise APIError(message, payload=decoded)
            return decoded.get("data")
        return decoded

    def _stream_request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        url = urljoin(f"{self.api_base_url}/", path.lstrip("/"))
        body: bytes | None = None
        headers = {"Accept": "text/event-stream"}
        headers.update(self.build_auth_headers())
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = Request(url=url, data=body, method=method.upper(), headers=headers)
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                raw = response.read()
        except HTTPError as exc:
            body_text = exc.read().decode("utf-8", errors="replace")
            decoded = self._decode_body(body_text)
            detail = self._extract_error_message(decoded) or body_text or str(exc)
            raise APIError(detail, status_code=exc.code, payload=decoded) from exc
        except URLError as exc:  # pragma: no cover
            raise APIError(f"Failed to reach SQLBot: {exc.reason}") from exc

        return self._parse_sse_events(raw.decode("utf-8", errors="replace"))

    @staticmethod
    def _decode_body(body: str) -> Any:
        if not body.strip():
            return None
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return body

    @staticmethod
    def _extract_error_message(payload: Any) -> str | None:
        if isinstance(payload, dict):
            for key in ("detail", "message", "msg"):
                value = payload.get(key)
                if isinstance(value, str) and value:
                    return value
        if isinstance(payload, str) and payload:
            return payload
        return None

    def _parse_sse_events(self, body: str) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        for chunk in body.split("\n\n"):
            stripped = chunk.strip()
            if not stripped:
                continue
            data_lines = [line[len("data:") :].lstrip() for line in stripped.splitlines() if line.startswith("data:")]
            if not data_lines:
                continue
            decoded = self._decode_body("\n".join(data_lines))
            if isinstance(decoded, dict) and "code" in decoded and decoded["code"] not in (0, 200):
                message = self._extract_error_message(decoded) or "SQLBot returned an error."
                raise APIError(message, payload=decoded)
            if isinstance(decoded, dict):
                events.append(decoded)
        return events


class DashboardExporter:
    _CACHE_MAX_EXPIRES_MS = 253402300799000

    def __init__(
        self,
        client: SQLBotClient,
        *,
        browser_path: str | None = None,
        ready_selector: str = "#sq-preview-content .canvas-container",
        wait_for_ms: int = 2000,
        timeout_ms: int = 45000,
        viewport_width: int = 1600,
        viewport_height: int = 900,
    ) -> None:
        self.client = client
        self.app_url = derive_app_url(client.api_base_url)
        self.browser_path = browser_path
        self.ready_selector = ready_selector
        self.wait_for_ms = wait_for_ms
        self.timeout_ms = timeout_ms
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

    def build_preview_url(self, dashboard_id: str) -> str:
        return f"{self.app_url.rstrip('/')}/#/dashboard-preview?resourceId={quote(dashboard_id)}"

    def export_dashboard(
        self,
        dashboard_id: str,
        output_path: str | Path,
        *,
        export_format: str,
        workspace: int | str | Workspace | None = None,
    ) -> dict[str, Any]:
        resolved_workspace: Workspace | None = None
        if workspace is not None:
            resolved_workspace = self.client.switch_workspace(workspace)

        dashboard = self.client.get_dashboard(dashboard_id)
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        preview_url = self.build_preview_url(dashboard_id)
        self._run_playwright_export(
            preview_url=preview_url,
            output_path=destination,
            export_format=export_format.lower(),
            local_storage=self._build_local_storage(resolved_workspace),
        )
        return {
            "dashboard_id": dashboard_id,
            "dashboard_name": dashboard.get("name"),
            "workspace_id": resolved_workspace.id if resolved_workspace else dashboard.get("workspace_id"),
            "format": export_format.lower(),
            "output_path": str(destination),
            "preview_url": preview_url,
        }

    def _build_local_storage(self, workspace: Workspace | None) -> dict[str, str]:
        storage = {"user.token": "api-key-auth", "user.language": "zh-CN"}
        if workspace is not None:
            storage["user.oid"] = str(workspace.id)
        return storage

    def _run_playwright_export(
        self,
        *,
        preview_url: str,
        output_path: Path,
        export_format: str,
        local_storage: dict[str, str],
    ) -> None:
        try:
            from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright
        except ModuleNotFoundError as exc:  # pragma: no cover
            raise BrowserError(
                "Dashboard export requires Playwright. Install with "
                "`pip install -e .[browser]` and then run `playwright install chromium`."
            ) from exc

        if export_format not in {"png", "pdf"}:
            raise BrowserError("Unsupported export format. Use `png` or `pdf`.")

        launch_options: dict[str, Any] = {"headless": True}
        if self.browser_path:
            launch_options["executable_path"] = self.browser_path

        init_script = self._build_local_storage_init_script(local_storage)

        try:  # pragma: no cover
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(**launch_options)
                context = browser.new_context(
                    viewport={"width": self.viewport_width, "height": self.viewport_height},
                    screen={"width": self.viewport_width, "height": self.viewport_height},
                )
                context.set_extra_http_headers(self.client.build_auth_headers())
                context.add_init_script(init_script)
                page = context.new_page()
                page.goto(preview_url, wait_until="domcontentloaded")
                page.wait_for_selector(self.ready_selector, state="visible", timeout=self.timeout_ms)
                page.wait_for_timeout(self.wait_for_ms)
                export_size = self._prepare_export_layout(page)
                if export_format == "png":
                    page.screenshot(path=str(output_path), full_page=True)
                else:
                    page.pdf(
                        path=str(output_path),
                        print_background=True,
                        prefer_css_page_size=True,
                        width=f"{export_size['width']}px",
                        height=f"{export_size['height']}px",
                        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                    )
                context.close()
                browser.close()
        except PlaywrightTimeoutError as exc:
            raise BrowserError(f"Timed out waiting for dashboard preview to render at {preview_url}.") from exc

    def _build_local_storage_init_script(self, local_storage: dict[str, str]) -> str:
        return (
            "const storage = "
            + json.dumps(local_storage, ensure_ascii=False)
            + ";"
            + f"const maxExpires = {self._CACHE_MAX_EXPIRES_MS};"
            + "Object.entries(storage).forEach(([key, value]) => {"
            + "const cacheItem = { c: Date.now(), e: maxExpires, v: JSON.stringify(value) };"
            + "window.localStorage.setItem(key, JSON.stringify(cacheItem));"
            + "});"
        )

    def _prepare_export_layout(self, page: Any) -> dict[str, int]:
        export_size = page.evaluate(
            """(selector) => {
                const clamp = (value, fallback) => {
                  const number = Number(value)
                  if (!Number.isFinite(number) || number <= 0) return fallback
                  return Math.ceil(number)
                }
                const content = document.querySelector('#sq-preview-content')
                const canvas = document.querySelector(selector)
                const target = canvas || content || document.body
                const rect = target.getBoundingClientRect()
                const width = Math.max(
                  clamp(rect.width, 1),
                  clamp(target.scrollWidth, 1),
                  clamp(document.documentElement.scrollWidth, 1),
                  clamp(document.body.scrollWidth, 1)
                )
                const height = Math.max(
                  clamp(rect.height, 1),
                  clamp(target.scrollHeight, 1),
                  clamp(document.documentElement.scrollHeight, 1),
                  clamp(document.body.scrollHeight, 1)
                )

                ;[document.documentElement, document.body, content, canvas]
                  .filter(Boolean)
                  .forEach((element) => {
                    element.style.width = `${width}px`
                    element.style.minWidth = `${width}px`
                    element.style.maxWidth = `${width}px`
                    element.style.height = `${height}px`
                    element.style.minHeight = `${height}px`
                    element.style.maxHeight = `${height}px`
                    element.style.overflow = 'visible'
                  })

                const styleId = 'sqlbot-export-style'
                let styleTag = document.getElementById(styleId)
                if (!styleTag) {
                  styleTag = document.createElement('style')
                  styleTag.id = styleId
                  document.head.appendChild(styleTag)
                }
                styleTag.textContent = `
                  @page { size: ${width}px ${height}px; margin: 0; }
                  html, body { margin: 0; padding: 0; overflow: visible !important; }
                  #sq-preview-content, ${selector} {
                    overflow: visible !important;
                  }
                `

                return { width, height }
            }""",
            self.ready_selector,
        )
        page.set_viewport_size(export_size)
        page.wait_for_timeout(300)
        return {"width": int(export_size["width"]), "height": int(export_size["height"])}


class WorkspaceDashboardSkill:
    def __init__(
        self,
        *,
        base_url: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
        browser_path: str | None = None,
        state_file: str | None = None,
        timeout: float | None = None,
        api_key_ttl_seconds: int | None = None,
        env_file: str | None = None,
    ) -> None:
        settings = SkillSettings.load(
            env_file=env_file,
            base_url=base_url,
            access_key=access_key,
            secret_key=secret_key,
            browser_path=browser_path,
            state_file=state_file,
            timeout=timeout,
            api_key_ttl_seconds=api_key_ttl_seconds,
        )
        self.settings = settings
        self.state_path = Path(settings.state_file)
        self.client = SQLBotClient(
            base_url=settings.base_url,
            access_key=settings.access_key,
            secret_key=settings.secret_key,
            api_key_ttl_seconds=settings.api_key_ttl_seconds,
            timeout=settings.timeout,
        )
        self.exporter = DashboardExporter(self.client, browser_path=settings.browser_path)

    def list_workspaces(self) -> list[Workspace]:
        return self.client.list_workspaces()

    def switch_workspace(self, workspace: int | str | Workspace) -> Workspace:
        resolved = self.client.switch_workspace(workspace)
        self._save_state(SkillState(current_workspace=resolved))
        return resolved

    def list_datasources(
        self,
        *,
        workspace: int | str | Workspace | None = None,
    ) -> list[Datasource]:
        self._switch_workspace_if_requested(workspace)
        return self.client.list_datasources()

    def switch_datasource(
        self,
        datasource: int | str | Datasource,
        *,
        workspace: int | str | Workspace | None = None,
    ) -> Datasource:
        current_state = self._load_state()
        resolved_workspace = self._switch_workspace_if_requested(workspace)
        resolved_datasource = self.client.resolve_datasource(datasource)
        self._save_state(
            SkillState(
                current_workspace=resolved_workspace or current_state.current_workspace,
                current_datasource=resolved_datasource,
            )
        )
        return resolved_datasource

    def current_datasource(self) -> Datasource | None:
        return self._load_state().current_datasource

    def list_dashboards(
        self,
        *,
        workspace: int | str | Workspace | None = None,
        node_type: str | None = None,
    ) -> list[DashboardNode]:
        self._switch_workspace_if_requested(workspace)
        return self.client.list_dashboards(node_type=node_type)

    def view_dashboard(
        self,
        dashboard_id: str,
        *,
        workspace: int | str | Workspace | None = None,
    ) -> dict[str, Any]:
        self._switch_workspace_if_requested(workspace)
        return self.client.get_dashboard(dashboard_id)

    def export_dashboard(
        self,
        dashboard_id: str,
        output_path: str | Path,
        *,
        export_format: str,
        workspace: int | str | Workspace | None = None,
    ) -> dict[str, Any]:
        self._switch_workspace_if_requested(workspace)
        return self.exporter.export_dashboard(
            dashboard_id,
            output_path,
            export_format=export_format,
            workspace=None,
        )

    def ask_data(
        self,
        question: str,
        *,
        workspace: int | str | Workspace | None = None,
        datasource: int | str | Datasource | None = None,
        chat_id: int | None = None,
        include_events: bool = True,
    ) -> dict[str, Any]:
        current_state = self._load_state()
        resolved_workspace = self._switch_workspace_if_requested(workspace)
        selected_datasource = datasource
        if selected_datasource is None and chat_id is None:
            state_workspace = current_state.current_workspace
            if current_state.current_datasource and (
                resolved_workspace is None
                or (state_workspace is not None and state_workspace.id == resolved_workspace.id)
            ):
                selected_datasource = current_state.current_datasource
        result = self.client.ask_data(question, datasource=selected_datasource, chat_id=chat_id)
        next_datasource = None
        if selected_datasource is not None:
            next_datasource = self.client.resolve_datasource(selected_datasource)
        elif isinstance(result.get("datasource"), dict) and result["datasource"].get("id"):
            datasource_id = result["datasource"]["id"]
            datasource_list = self.client.list_datasources()
            next_datasource = next((item for item in datasource_list if item.id == int(datasource_id)), None)
        if not include_events:
            result.pop("events", None)
        self._save_state(
            SkillState(
                current_workspace=resolved_workspace or current_state.current_workspace,
                current_datasource=next_datasource or current_state.current_datasource,
            )
        )
        return result

    def _load_state(self) -> SkillState:
        return SkillState.load(self.state_path)

    def _save_state(self, state: SkillState) -> None:
        state.save(self.state_path)

    def _switch_workspace_if_requested(
        self,
        workspace: int | str | Workspace | None,
    ) -> Workspace | None:
        if workspace is None:
            return None
        current_state = self._load_state()
        resolved = self.client.switch_workspace(workspace)
        preserved_datasource = current_state.current_datasource
        if (
            current_state.current_workspace is None
            or current_state.current_workspace.id != resolved.id
        ):
            preserved_datasource = None
        self._save_state(
            SkillState(
                current_workspace=resolved,
                current_datasource=preserved_datasource,
            )
        )
        return resolved


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sqlbot_skills.py",
        description="Workspace and dashboard skills for SQLBot.",
    )
    parser.add_argument(
        "--env-file",
        default=None,
        help="Path to .env file. Defaults to ./.env.",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="SQLBot base URL or API base URL. Defaults to SQLBOT_BASE_URL from .env.",
    )
    parser.add_argument(
        "--access-key",
        default=None,
        help="SQLBot API key access_key. Defaults to SQLBOT_API_KEY_ACCESS_KEY from .env.",
    )
    parser.add_argument(
        "--secret-key",
        default=None,
        help="SQLBot API key secret_key. Defaults to SQLBOT_API_KEY_SECRET_KEY from .env.",
    )
    parser.add_argument(
        "--browser-path",
        default=None,
        help="Optional Chromium/Chrome executable path. Defaults to SQLBOT_BROWSER_PATH from .env.",
    )
    parser.add_argument(
        "--state-file",
        default=None,
        help="Path to local datasource state file. Defaults to SQLBOT_STATE_FILE or skill-local state file.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        help="HTTP timeout in seconds. Defaults to SQLBOT_TIMEOUT from .env.",
    )
    parser.add_argument(
        "--api-key-ttl-seconds",
        type=int,
        default=None,
        help="Signed API key token TTL. Defaults to SQLBOT_API_KEY_TTL_SECONDS from .env.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    workspace_parser = subparsers.add_parser("workspace", help="Workspace operations.")
    workspace_subparsers = workspace_parser.add_subparsers(dest="workspace_command", required=True)
    workspace_subparsers.add_parser("list", help="List accessible workspaces.")
    workspace_switch = workspace_subparsers.add_parser("switch", help="Switch current workspace.")
    workspace_switch.add_argument("workspace", help="Workspace id or exact name.")

    datasource_parser = subparsers.add_parser("datasource", help="Datasource operations.")
    datasource_subparsers = datasource_parser.add_subparsers(dest="datasource_command", required=True)
    datasource_list = datasource_subparsers.add_parser("list", help="List datasources.")
    datasource_list.add_argument("--workspace", help="Workspace id or exact name.")
    datasource_switch = datasource_subparsers.add_parser("switch", help="Switch current datasource locally.")
    datasource_switch.add_argument("datasource", help="Datasource id or exact name.")
    datasource_switch.add_argument("--workspace", help="Workspace id or exact name.")
    datasource_subparsers.add_parser("current", help="Show current datasource saved in the skill state.")

    dashboard_parser = subparsers.add_parser("dashboard", help="Dashboard operations.")
    dashboard_subparsers = dashboard_parser.add_subparsers(dest="dashboard_command", required=True)

    dashboard_list = dashboard_subparsers.add_parser("list", help="List dashboards.")
    dashboard_list.add_argument("--workspace", help="Workspace id or exact name.")
    dashboard_list.add_argument("--node-type", choices=["folder", "leaf"], help="Optional node type filter.")
    dashboard_list.add_argument("--flat", action="store_true", help="Flatten the dashboard tree before printing.")

    dashboard_show = dashboard_subparsers.add_parser("show", help="Show dashboard detail.")
    dashboard_show.add_argument("dashboard_id", help="Dashboard id.")
    dashboard_show.add_argument("--workspace", help="Workspace id or exact name.")

    dashboard_export = dashboard_subparsers.add_parser("export", help="Export dashboard as screenshot or PDF.")
    dashboard_export.add_argument("dashboard_id", help="Dashboard id.")
    dashboard_export.add_argument("--workspace", help="Workspace id or exact name.")
    dashboard_export.add_argument("--format", choices=["png", "pdf"], required=True, help="Export format.")
    dashboard_export.add_argument("--output", help="Output file path. Defaults to ./<dashboard_id>.<format>.")

    ask_parser = subparsers.add_parser("ask", help="Ask a natural-language question against a datasource.")
    ask_parser.add_argument("question", nargs="+", help="Natural-language question.")
    ask_parser.add_argument("--workspace", help="Workspace id or exact name.")
    ask_parser.add_argument("--datasource", help="Datasource id or exact name. Defaults to the current switched datasource.")
    ask_parser.add_argument("--chat-id", type=int, help="Existing chat id to continue. Defaults to creating a new chat.")
    ask_parser.add_argument(
        "--include-events",
        action="store_true",
        help="Include raw SSE events in the output payload.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        skill = WorkspaceDashboardSkill(
            env_file=args.env_file,
            base_url=args.base_url,
            access_key=args.access_key,
            secret_key=args.secret_key,
            browser_path=args.browser_path,
            state_file=args.state_file,
            timeout=args.timeout,
            api_key_ttl_seconds=args.api_key_ttl_seconds,
        )
        if args.command == "workspace":
            return _run_workspace(skill, args)
        if args.command == "datasource":
            return _run_datasource(skill, args)
        if args.command == "dashboard":
            return _run_dashboard(skill, args)
        if args.command == "ask":
            return _run_ask(skill, args)
        parser.error("Unknown command.")
        return 2
    except SQLBotSkillError as exc:
        print(str(exc), file=sys.stderr)
        return 1


def _run_workspace(skill: WorkspaceDashboardSkill, args: argparse.Namespace) -> int:
    if args.workspace_command == "list":
        _print_json([item.to_dict() for item in skill.list_workspaces()])
        return 0
    if args.workspace_command == "switch":
        workspace = skill.switch_workspace(args.workspace)
        _print_json({"switched": True, "workspace": workspace.to_dict()})
        return 0
    raise AssertionError("Unhandled workspace command.")


def _run_dashboard(skill: WorkspaceDashboardSkill, args: argparse.Namespace) -> int:
    if args.dashboard_command == "list":
        dashboards = skill.list_dashboards(workspace=args.workspace, node_type=args.node_type)
        payload = [item.to_dict() for item in (_flatten_nodes(dashboards) if args.flat else dashboards)]
        _print_json(payload)
        return 0
    if args.dashboard_command == "show":
        _print_json(skill.view_dashboard(args.dashboard_id, workspace=args.workspace))
        return 0
    if args.dashboard_command == "export":
        output = args.output or f"./{args.dashboard_id}.{args.format}"
        payload = skill.export_dashboard(
            args.dashboard_id,
            output,
            export_format=args.format,
            workspace=args.workspace,
        )
        _print_json(payload)
        return 0
    raise AssertionError("Unhandled dashboard command.")


def _run_datasource(skill: WorkspaceDashboardSkill, args: argparse.Namespace) -> int:
    if args.datasource_command == "list":
        _print_json([item.to_dict() for item in skill.list_datasources(workspace=args.workspace)])
        return 0
    if args.datasource_command == "switch":
        datasource = skill.switch_datasource(args.datasource, workspace=args.workspace)
        _print_json({"switched": True, "datasource": datasource.to_dict()})
        return 0
    if args.datasource_command == "current":
        datasource = skill.current_datasource()
        _print_json(datasource.to_dict() if datasource else None)
        return 0
    raise AssertionError("Unhandled datasource command.")


def _run_ask(skill: WorkspaceDashboardSkill, args: argparse.Namespace) -> int:
    payload = skill.ask_data(
        " ".join(args.question),
        workspace=args.workspace,
        datasource=args.datasource,
        chat_id=args.chat_id,
        include_events=args.include_events,
    )
    _print_json(payload)
    return 0


def _flatten_nodes(nodes: Iterable[DashboardNode]) -> list[DashboardNode]:
    flattened: list[DashboardNode] = []
    for node in nodes:
        flattened.extend(node.walk())
    return flattened


def _print_json(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
