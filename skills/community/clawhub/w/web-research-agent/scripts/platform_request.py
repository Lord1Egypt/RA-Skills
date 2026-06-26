#!/usr/bin/env python3
"""Authenticated OpenMarlin platform requests with routing hints."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from openclaw_skill_config import (
    DEFAULT_SERVER_URL,
    build_server_connection_error,
    get_skill_env,
    probe_server_openapi,
    require_server_url,
)
from openclaw_billing_state import record_balance_snapshot
from openclaw_platform_auth import DEFAULT_AGENT_ID, DEFAULT_PROFILE_ID, resolve_platform_api_key
from billing import build_recovery_commands, parse_insufficient_balance


JsonValue = Any


ERROR_HELP = {
    "missing_api_key": "Missing platform API key. Export OPENMARLIN_PLATFORM_API_KEY first.",
    "invalid_api_key": "The platform API key was rejected. Re-bootstrap a fresh key and retry.",
    "api_key_inactive": "The platform API key is no longer active. Bootstrap a replacement key.",
    "workspace_missing": "The API key resolved, but its workspace no longer exists on the server.",
    "account_missing": "The API key resolved, but its owning account no longer exists on the server.",
    "invalid_routing_labels": "Routing labels were invalid. Use repeated --label key=value flags or valid JSON in OPENMARLIN_DEFAULT_ROUTING_LABELS.",
    "provider_unavailable": "The selected provider is not currently connected.",
    "provider_label_mismatch": "The selected provider does not satisfy the requested routing hints.",
    "execution_provider_not_found": "The server could not find any eligible execution provider for this request. Retry with different labels, a different model, or an explicit --provider override.",
    "execution_provider_ambiguous": "More than one eligible execution provider matched and the server could not choose automatically. Retry with narrower labels or an explicit --provider override.",
    "execution_kind_not_available": "The selected provider does not support the requested execution kind.",
    "task_executor_not_found": "The server could not find any configured task executor for this long-running task kind.",
    "invalid_request": "The request payload did not match the server contract.",
}

TASK_TERMINAL_STATUSES = {"succeeded", "failed"}


def parse_args() -> argparse.Namespace:
    default_server_url, server_url_source = get_skill_env("OPENMARLIN_SERVER_URL")
    default_api_key, _api_key_source = get_skill_env("OPENMARLIN_PLATFORM_API_KEY")
    default_provider, provider_source = get_skill_env("OPENMARLIN_DEFAULT_PROVIDER_ID")
    common = argparse.ArgumentParser(add_help=False)
    common.set_defaults(_server_url_source=server_url_source, _provider_source=provider_source)
    common.add_argument(
        "--server-url",
        default=(default_server_url or "").strip(),
        help=f"Base URL for the OpenMarlin server. Defaults to OPENMARLIN_SERVER_URL, then OpenClaw skill config, then {DEFAULT_SERVER_URL}. Do not include /v1.",
    )
    common.add_argument(
        "--api-key",
        default=(default_api_key or "").strip(),
        help="Platform API key. Defaults to OPENMARLIN_PLATFORM_API_KEY, then OpenClaw auth-profiles.json.",
    )
    common.add_argument(
        "--provider",
        default=(default_provider or "").strip(),
        help="Optional explicit provider override for /v1/executions. Defaults to OPENMARLIN_DEFAULT_PROVIDER_ID, then OpenClaw skill config. /v1/tasks is now executor-routed and does not accept provider overrides.",
    )
    common.add_argument(
        "--label",
        action="append",
        default=[],
        help="Routing hint in key=value form. May be repeated.",
    )
    common.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON output when possible.",
    )
    common.add_argument(
        "--dry-run",
        action="store_true",
        help="Show resolved configuration and a lightweight connectivity check without executing the request.",
    )
    common.add_argument(
        "--profile-id",
        default=DEFAULT_PROFILE_ID,
        help=f"OpenClaw auth profile ID used when resolving a stored platform key. Default: {DEFAULT_PROFILE_ID}.",
    )
    common.add_argument(
        "--agent-id",
        default=DEFAULT_AGENT_ID,
        help=f"OpenClaw agent ID used when resolving a stored platform key. Default: {DEFAULT_AGENT_ID}.",
    )

    parser = argparse.ArgumentParser(
        description="Send authenticated OpenMarlin execution, task, and model-discovery requests with optional provider overrides and routing hints.",
        parents=[common],
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    executions = subparsers.add_parser(
        "executions",
        help="Send a /v1/executions request.",
        parents=[common],
    )
    executions.add_argument(
        "--body-json",
        help="Raw JSON object payload for /v1/executions.",
    )
    executions.add_argument(
        "--body-file",
        help="Path to a JSON file containing the /v1/executions payload.",
    )

    task_submit = subparsers.add_parser(
        "tasks-submit",
        help="Submit a /v1/tasks request for long-running work.",
        parents=[common],
    )
    task_submit.add_argument(
        "--body-json",
        help="Raw JSON object payload for /v1/tasks.",
    )
    task_submit.add_argument(
        "--body-file",
        help="Path to a JSON file containing the /v1/tasks payload.",
    )
    task_submit.add_argument(
        "--watch",
        action="store_true",
        help="After task submission is accepted, keep polling until it succeeds or fails.",
    )
    task_submit.add_argument(
        "--interval-seconds",
        type=float,
        default=2.0,
        help="Polling interval in seconds when --watch is set. Default: 2.0.",
    )
    task_submit.add_argument(
        "--timeout-seconds",
        type=float,
        default=1800.0,
        help="Maximum total wait time in seconds when --watch is set. Default: 1800.0.",
    )

    task_status = subparsers.add_parser(
        "tasks-status",
        help="Fetch the current state of a previously submitted task.",
        parents=[common],
    )
    task_status.add_argument("--task-id", required=True, help="Task ID returned by /v1/tasks.")

    task_watch = subparsers.add_parser(
        "tasks-watch",
        help="Poll a task until it succeeds or fails.",
        parents=[common],
    )
    task_watch.add_argument("--task-id", required=True, help="Task ID returned by /v1/tasks.")
    task_watch.add_argument(
        "--interval-seconds",
        type=float,
        default=2.0,
        help="Polling interval in seconds. Default: 2.0.",
    )
    task_watch.add_argument(
        "--timeout-seconds",
        type=float,
        default=1800.0,
        help="Maximum total wait time in seconds. Default: 1800.0.",
    )

    subparsers.add_parser(
        "models",
        help="List currently available execution models from /v1/models.",
        parents=[common],
    )

    return parser.parse_args()


def require_non_empty(value: str, message: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise SystemExit(message)
    return normalized


def normalize_execution_request(body: dict[str, Any]) -> None:
    if "model_provider" in body or "modelProvider" in body:
        raise SystemExit(
            "Family-level execution routing is not supported in this skill. "
            "Use no model for server-side automatic selection, or pass an exact full model ref in body.model."
        )

    raw_model = body.get("model")
    if raw_model is None:
        return
    if not isinstance(raw_model, str):
        raise SystemExit("If body.model is provided, it must be a string exact full model ref.")

    model = raw_model.strip()
    if not model:
        body.pop("model", None)
        return
    if "/" not in model:
        raise SystemExit(
            f"If body.model is provided, it must be an exact full ref, got {model!r}. "
            "Run `python3 scripts/platform_request.py models` and use the exact id as returned."
        )

    body["model"] = model


def normalize_task_request(body: dict[str, Any]) -> None:
    if "stream" in body:
        raise SystemExit("Long-running task submission does not support body.stream. Use /v1/tasks without streaming.")
    if "provider_id" in body or "providerId" in body:
        raise SystemExit("Long-running task submission no longer accepts provider overrides in the request body.")
    if "labels" in body:
        raise SystemExit("Long-running task submission no longer accepts routing labels in the request body.")
    if "model" in body or "model_provider" in body or "modelProvider" in body:
        raise SystemExit("Long-running task submission no longer accepts execution-model routing fields.")
    if body.get("kind") != "video":
        raise SystemExit('Long-running task submission currently requires body.kind = "video".')
    input_value = body.get("input")
    if not isinstance(input_value, dict):
        raise SystemExit("Long-running task submission requires body.input as a JSON object.")
    prompt = input_value.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise SystemExit("Long-running task submission requires body.input.prompt as a non-empty string.")
    metadata_value = body.get("metadata")
    if metadata_value is not None and not isinstance(metadata_value, dict):
        raise SystemExit("If body.metadata is provided for long-running task submission, it must be a JSON object.")

    allowed_keys = {"kind", "input", "metadata"}
    unknown_keys = sorted(key for key in body.keys() if key not in allowed_keys)
    if unknown_keys:
        raise SystemExit(
            "Long-running task submission only accepts body.kind, body.input, and optional body.metadata. "
            f"Unexpected keys: {', '.join(unknown_keys)}."
        )

    allowed_input_keys = {"prompt", "media_urls", "media_ids", "duration_ms", "aspect_ratio"}
    unknown_input_keys = sorted(key for key in input_value.keys() if key not in allowed_input_keys)
    if unknown_input_keys:
        raise SystemExit(
            "Long-running task video input only accepts prompt, media_urls, media_ids, duration_ms, and aspect_ratio. "
            f"Unexpected input keys: {', '.join(unknown_input_keys)}."
        )

    input_value["prompt"] = prompt.strip()


def resolve_api_key(raw_api_key: str, profile_id: str, agent_id: str) -> tuple[str | None, str | None, str | None]:
    if raw_api_key.strip():
        return raw_api_key.strip(), "env-or-flag", None

    key, _profile, auth_store_path = resolve_platform_api_key(profile_id=profile_id, agent_id=agent_id)
    if key:
        return key, f"auth-profiles:{auth_store_path}", None

    return None, None, (
        "Missing platform API key. Set OPENMARLIN_PLATFORM_API_KEY, pass --api-key, "
        "or bootstrap with --store so the key is saved into OpenClaw auth-profiles.json."
    )


def resolve_api_key_or_exit(raw_api_key: str, profile_id: str, agent_id: str) -> tuple[str, str]:
    key, source, error = resolve_api_key(raw_api_key, profile_id, agent_id)
    if error:
        raise SystemExit(error)
    assert key is not None and source is not None
    return key, source


def load_json_object(raw: str, *, source: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON in {source}: {error}") from error
    if not isinstance(parsed, dict):
        raise SystemExit(f"{source} must decode to a JSON object.")
    return parsed


def load_json_object_from_option(raw: str | None, path: str | None, *, source_name: str) -> dict[str, Any]:
    if bool(raw) == bool(path):
        raise SystemExit(f"Provide exactly one of {source_name}-json or {source_name}-file.")
    if raw:
        return load_json_object(raw, source=f"--{source_name}-json")
    with open(path, "r", encoding="utf-8") as handle:
        return load_json_object(handle.read(), source=f"--{source_name}-file")


def parse_label_pairs(values: list[str]) -> dict[str, str]:
    labels: dict[str, str] = {}
    for raw in values:
        key, separator, value = raw.partition("=")
        key = key.strip()
        value = value.strip()
        if separator != "=" or not key or not value:
            raise SystemExit(f"Invalid --label value: {raw!r}. Expected key=value.")
        labels[key] = value
    return labels


def resolve_labels(cli_labels: list[str]) -> dict[str, str] | None:
    merged: dict[str, str] = {}
    env_raw, _source = get_skill_env("OPENMARLIN_DEFAULT_ROUTING_LABELS")
    env_raw = (env_raw or "").strip()
    if env_raw:
        env_labels = load_json_object(env_raw, source="OPENMARLIN_DEFAULT_ROUTING_LABELS")
        for key, value in env_labels.items():
            if not isinstance(key, str) or not isinstance(value, str) or not key or not value.strip():
                raise SystemExit(
                    "OPENMARLIN_DEFAULT_ROUTING_LABELS must be a JSON object of non-empty string values."
                )
            merged[key] = value.strip()

    merged.update(parse_label_pairs(cli_labels))
    return merged or None


def request(
    *,
    url: str,
    method: str,
    headers: dict[str, str],
    payload: dict[str, Any],
) -> tuple[int, JsonValue, dict[str, str]]:
    body = json.dumps(payload).encode("utf-8")
    request_obj = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            **headers,
        },
    )
    try:
        with urllib.request.urlopen(request_obj) as response:
            content_type = response.headers.get("content-type", "")
            raw = response.read().decode("utf-8")
            payload_out: JsonValue
            if "application/json" in content_type and raw:
                payload_out = json.loads(raw)
            else:
                payload_out = raw
            return response.status, payload_out, dict(response.headers.items())
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8")
        try:
            payload_out = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload_out = raw
        return error.code, payload_out, dict(error.headers.items())
    except urllib.error.URLError as error:
        parsed = urllib.parse.urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else url
        raise SystemExit(build_server_connection_error(base_url, str(error.reason))) from error


def request_without_body(
    *,
    url: str,
    method: str,
    headers: dict[str, str],
) -> tuple[int, JsonValue, dict[str, str]]:
    request_obj = urllib.request.Request(
        url,
        method=method,
        headers={
            "Accept": "application/json",
            **headers,
        },
    )
    try:
        with urllib.request.urlopen(request_obj) as response:
            content_type = response.headers.get("content-type", "")
            raw = response.read().decode("utf-8")
            payload_out: JsonValue
            if "application/json" in content_type and raw:
                payload_out = json.loads(raw)
            else:
                payload_out = raw
            return response.status, payload_out, dict(response.headers.items())
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8")
        try:
            payload_out = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload_out = raw
        return error.code, payload_out, dict(error.headers.items())
    except urllib.error.URLError as error:
        parsed = urllib.parse.urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else url
        raise SystemExit(build_server_connection_error(base_url, str(error.reason))) from error


def parse_sse_events(raw: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    event_type: str | None = None
    data_lines: list[str] = []

    def flush_event() -> None:
        nonlocal event_type, data_lines
        if event_type is None and not data_lines:
            return
        data_raw = "\n".join(data_lines)
        data_payload: Any = data_raw
        if data_raw:
            try:
                data_payload = json.loads(data_raw)
            except json.JSONDecodeError:
                data_payload = data_raw
        event: dict[str, Any] = {"event": event_type or "message", "data": data_payload}
        events.append(event)
        event_type = None
        data_lines = []

    for line in raw.splitlines():
        if not line.strip():
            flush_event()
            continue
        if line.startswith(":"):
            continue
        field, separator, value = line.partition(":")
        value = value[1:] if separator and value.startswith(" ") else value
        if field == "event":
            event_type = value
        elif field == "data":
            data_lines.append(value)

    flush_event()
    return events


def explain_error(code: int, payload: JsonValue, provider: str | None, labels: dict[str, str] | None) -> str:
    if isinstance(payload, dict):
        recovery = parse_insufficient_balance(payload)
        if code == 402 and recovery:
            commands = build_recovery_commands(recovery)
            context_parts = []
            if provider:
                context_parts.append(f"provider={provider}")
            if labels:
                context_parts.append(f"labels={json.dumps(labels, sort_keys=True)}")
            context = f" Sent {', '.join(context_parts)}." if context_parts else ""
            return (
                f"HTTP 402 insufficient_balance: {recovery['message']} "
                f"Current={recovery['current_balance']['amount']} {recovery['current_balance']['unit']}, "
                f"required={recovery['required_balance']['amount']} {recovery['required_balance']['unit']}, "
                f"shortfall={recovery['shortfall']['amount']} {recovery['shortfall']['unit']}.{context} "
                f"Recovery: {commands[0]} then {commands[1]}"
            )
        error_code = payload.get("error")
        if isinstance(error_code, str):
            explanation = ERROR_HELP.get(error_code, "The server rejected the request.")
            context_parts = []
            if provider:
                context_parts.append(f"provider={provider}")
            if labels:
                context_parts.append(f"labels={json.dumps(labels, sort_keys=True)}")
            context = f" Sent {', '.join(context_parts)}." if context_parts else ""
            return f"HTTP {code} {error_code}: {explanation}{context}"
    return f"HTTP {code}: {payload}"


def iter_discovered_models(payload: JsonValue) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
    return []


def format_labels(labels: Any) -> str | None:
    if isinstance(labels, dict) and labels:
        normalized = {str(key): value for key, value in labels.items()}
        return json.dumps(normalized, sort_keys=True)
    return None


def format_string_list(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    return [item.strip() for item in values if isinstance(item, str) and item.strip()]


def task_status(payload: JsonValue) -> str | None:
    if isinstance(payload, dict):
        status = payload.get("status")
        if isinstance(status, str) and status.strip():
            return status.strip()
    return None


def task_summary_lines(payload: JsonValue) -> list[str]:
    if not isinstance(payload, dict):
        return []
    lines: list[str] = []
    for key, label in (
        ("task_id", "Task ID"),
        ("status", "Status"),
        ("provider_id", "Provider"),
        ("workspace_id", "Workspace"),
        ("created_at", "Created at"),
        ("updated_at", "Updated at"),
        ("started_at", "Started at"),
        ("completed_at", "Completed at"),
    ):
        value = payload.get(key)
        if value is not None:
            lines.append(f"{label}: {value}")
    if payload.get("error") is not None:
        lines.append(f"Error: {payload.get('error')}")
    output = payload.get("output")
    if output is not None:
        lines.append(f"Output: {json.dumps(output, sort_keys=True)}")
    metadata = payload.get("metadata")
    if metadata is not None:
        lines.append(f"Metadata: {json.dumps(metadata, sort_keys=True)}")
    return lines


def print_models_success(payload: JsonValue) -> None:
    models = iter_discovered_models(payload)
    if not models:
        print("Command: models")
        print("Exact models: 0")
        print("No exact models were returned. /v1/executions can still omit body.model and let the server choose automatically.")
        return

    print("Command: models")
    print(f"Exact models: {len(models)}")
    for entry in models:
        model_id = entry.get("id") if isinstance(entry.get("id"), str) and entry.get("id").strip() else "<unknown>"
        providers = entry.get("providers")
        if isinstance(providers, list) and providers:
            for provider_entry in providers:
                if not isinstance(provider_entry, dict):
                    continue
                provider_id = (
                    provider_entry.get("provider_id")
                    if isinstance(provider_entry.get("provider_id"), str) and provider_entry.get("provider_id").strip()
                    else "<unknown>"
                )
                provider_models = format_string_list(provider_entry.get("model_providers"))
                labels = format_labels(provider_entry.get("labels"))
                details: list[str] = []
                if provider_models and provider_models != [model_id]:
                    details.append(f"advertises={json.dumps(provider_models)}")
                if labels:
                    details.append(f"labels={labels}")
                suffix = f" {' '.join(details)}" if details else ""
                print(f"- {model_id} via {provider_id}{suffix}")
            continue


def print_success(command: str, provider: str | None, labels: dict[str, str] | None, payload: JsonValue) -> None:
    if command == "models":
        print_models_success(payload)
        return
    if command in {"tasks-submit", "tasks-status", "tasks-watch"}:
        print(f"Command: {command}")
        for line in task_summary_lines(payload):
            print(line)
        return

    print(f"Command: {command}")
    if provider:
        print(f"Provider override: {provider}")
    else:
        print("Provider override: <none; server-side automatic routing>")
    if labels:
        print(f"Routing labels: {json.dumps(labels, sort_keys=True)}")
    else:
        print("Routing labels: <none>")
    print("Response:")
    if isinstance(payload, str):
        print(payload)
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))


def print_dry_run(args: argparse.Namespace, server_url: str, provider: str | None, labels: dict[str, str] | None) -> int:
    api_key, api_key_source, api_key_error = resolve_api_key(args.api_key, args.profile_id, args.agent_id)
    reachable, detail = probe_server_openapi(server_url)
    payload: dict[str, Any] = {
        "ok": reachable and api_key_error is None,
        "dry_run": True,
        "command": args.command,
        "server_url": server_url,
        "server_url_source": args._server_url_source or "flag-or-arg",
        "api_key_source": api_key_source,
        "api_key_error": api_key_error,
        "provider_override": provider if args.command == "executions" else None,
        "provider_source": args._provider_source or ("flag-or-arg" if provider and args.command == "executions" else None),
        "labels": labels or {} if args.command == "executions" else {},
        "connectivity": detail,
    }
    if args.command == "executions":
        body = load_json_object_from_option(args.body_json, args.body_file, source_name="body")
        normalize_execution_request(body)
        payload["request_preview"] = {
            "kind": body.get("kind", "agent_run"),
            "model": body.get("model"),
            "stream": body.get("stream") is True,
            "has_instruction": isinstance(body.get("instruction"), str) and bool(body.get("instruction").strip()),
        }
    elif args.command == "tasks-submit":
        body = load_json_object_from_option(args.body_json, args.body_file, source_name="body")
        normalize_task_request(body)
        payload["request_preview"] = {
            "kind": body.get("kind"),
            "has_prompt": isinstance(body.get("input", {}).get("prompt"), str)
            and bool(body.get("input", {}).get("prompt").strip()),
        }
        payload["watch"] = args.watch
    elif args.command == "tasks-status":
        payload["task_id"] = args.task_id
        payload["operation"] = f"GET /v1/tasks/{args.task_id}"
    elif args.command == "tasks-watch":
        payload["task_id"] = args.task_id
        payload["operation"] = f"WATCH /v1/tasks/{args.task_id}"
    elif args.command == "models":
        payload["operation"] = "GET /v1/models"

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("Dry run only. No platform request was executed.")
        print(f"Command: {args.command}")
        print(f"Resolved server URL: {server_url}")
        print(f"Server URL source: {payload['server_url_source']}")
        print(f"Connectivity check: {detail}")
        if api_key_error:
            print(f"API key: missing ({api_key_error})")
        else:
            print(f"API key source: {api_key_source}")
        if args.command == "executions":
            print(f"Provider override: {provider or '<none; server-side automatic routing>'}")
            print(f"Routing labels: {json.dumps(labels or {}, sort_keys=True)}")
        if args.command == "executions":
            preview = payload["request_preview"]
            print(f"Execution kind: {preview.get('kind', 'agent_run')}")
            print(f"Model: {preview.get('model') or '<server auto-select>'}")
            print(f"Instruction present: {'yes' if preview.get('has_instruction') else 'no'}")
            print(f"Stream: {'yes' if preview.get('stream') else 'no'}")
        elif args.command == "tasks-submit":
            preview = payload["request_preview"]
            print(f"Task kind: {preview.get('kind') or '<missing>'}")
            print(f"Prompt present: {'yes' if preview.get('has_prompt') else 'no'}")
            print(f"Watch after submit: {'yes' if payload.get('watch') else 'no'}")
        elif args.command == "tasks-status":
            print(f"Task ID: {args.task_id}")
            print(f"Operation: GET /v1/tasks/{args.task_id}")
        elif args.command == "tasks-watch":
            print(f"Task ID: {args.task_id}")
            print(f"Poll interval: {args.interval_seconds:.1f}s")
            print(f"Timeout: {args.timeout_seconds:.1f}s")
        elif args.command == "models":
            print("Operation: GET /v1/models")
    return 0 if payload["ok"] else 1


def fetch_task(
    *,
    server_url: str,
    api_key: str,
    task_id: str,
) -> tuple[int, JsonValue, dict[str, str]]:
    return request_without_body(
        url=f"{server_url}/v1/tasks/{urllib.parse.quote(task_id)}",
        method="GET",
        headers={
            "Authorization": f"Bearer {api_key}",
        },
    )


def watch_task(
    *,
    server_url: str,
    api_key: str,
    task_id: str,
    interval_seconds: float,
    timeout_seconds: float,
) -> tuple[int, JsonValue, dict[str, str]]:
    deadline = time.monotonic() + timeout_seconds
    while True:
        status, payload, response_headers = fetch_task(server_url=server_url, api_key=api_key, task_id=task_id)
        current_status = task_status(payload)
        if status >= 400 or current_status in TASK_TERMINAL_STATUSES:
            return status, payload, response_headers
        if time.monotonic() >= deadline:
            raise SystemExit(f"Timed out after {timeout_seconds:.1f}s waiting for task {task_id}.")
        time.sleep(interval_seconds)


def main() -> int:
    args = parse_args()
    server_url = require_server_url(args.server_url)
    provider = args.provider.strip() or None
    labels = resolve_labels(args.label)
    if args.dry_run:
        return print_dry_run(args, server_url, provider, labels)
    api_key, api_key_source = resolve_api_key_or_exit(args.api_key, args.profile_id, args.agent_id)

    if args.command == "executions":
        body = load_json_object_from_option(args.body_json, args.body_file, source_name="body")
        normalize_execution_request(body)
        if provider:
            body["provider_id"] = provider
        if labels:
            body["labels"] = labels
        status, payload, response_headers = request(
            url=f"{server_url}/v1/executions",
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            payload=body,
        )
    elif args.command == "tasks-submit":
        body = load_json_object_from_option(args.body_json, args.body_file, source_name="body")
        normalize_task_request(body)
        status, payload, response_headers = request(
            url=f"{server_url}/v1/tasks",
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            payload=body,
        )
        if (
            status < 400
            and args.watch
            and isinstance(payload, dict)
            and isinstance(payload.get("task_id"), str)
            and payload["task_id"].strip()
        ):
            status, payload, response_headers = watch_task(
                server_url=server_url,
                api_key=api_key,
                task_id=payload["task_id"].strip(),
                interval_seconds=args.interval_seconds,
                timeout_seconds=args.timeout_seconds,
            )
    elif args.command == "tasks-status":
        status, payload, response_headers = fetch_task(
            server_url=server_url,
            api_key=api_key,
            task_id=args.task_id,
        )
    elif args.command == "tasks-watch":
        status, payload, response_headers = watch_task(
            server_url=server_url,
            api_key=api_key,
            task_id=args.task_id,
            interval_seconds=args.interval_seconds,
            timeout_seconds=args.timeout_seconds,
        )
    elif args.command == "models":
        status, payload, response_headers = request_without_body(
            url=f"{server_url}/v1/models",
            method="GET",
            headers={
                "Authorization": f"Bearer {api_key}",
            },
        )
    else:
        raise SystemExit(f"Unsupported command: {args.command}")

    stream_events = None
    if (
        args.command == "executions"
        and isinstance(payload, str)
        and "text/event-stream" in response_headers.get("content-type", "")
    ):
        stream_events = parse_sse_events(payload)

    if status >= 400:
        message = explain_error(status, payload, provider, labels)
        recovery = parse_insufficient_balance(payload) if isinstance(payload, dict) else None
        stored_balance = None
        if recovery and isinstance(recovery.get("workspace_id"), str) and recovery["workspace_id"].strip():
            stored_balance = record_balance_snapshot(
                workspace_id=recovery["workspace_id"],
                amount=recovery["current_balance"]["amount"],
                unit=recovery["current_balance"]["unit"],
                agent_id=args.agent_id,
                source="structured_402",
                estimated=False,
                message=recovery.get("message"),
                required_amount=recovery["required_balance"]["amount"],
                reference={"error_code": "insufficient_balance"},
            )
        if args.json:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "status": status,
                        "provider": provider,
                        "labels": labels or {},
                        "api_key_source": api_key_source,
                        "response": payload,
                        **({"stream_events": stream_events} if stream_events is not None else {}),
                        "message": message,
                        **({"recovery": recovery, "commands": build_recovery_commands(recovery)} if recovery else {}),
                        **({"stored_balance": stored_balance} if stored_balance else {}),
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(message, file=sys.stderr)
            if stored_balance:
                print(f"Saved billing snapshot to: {stored_balance['billing_state_path']}", file=sys.stderr)
        return 1

    if args.json:
        print(
            json.dumps(
                {
                    "ok": True,
                    "status": status,
                    "provider": provider,
                    "labels": labels or {},
                    "api_key_source": api_key_source,
                    "response_headers": response_headers,
                    "response": payload,
                    **({"stream_events": stream_events} if stream_events is not None else {}),
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        if stream_events is not None:
            print(f"Command: {args.command}")
            print(f"Provider override: {provider or '<none; server-side automatic routing>'}")
            print(f"Routing labels: {json.dumps(labels or {}, sort_keys=True)}")
            print("Execution stream:")
            for event in stream_events:
                print(f"- {event['event']}: {json.dumps(event['data'], sort_keys=True)}")
        else:
            print_success(args.command, provider, labels, payload)

    return 0


if __name__ == "__main__":
    sys.exit(main())
