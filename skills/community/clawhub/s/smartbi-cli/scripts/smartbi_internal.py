#!/usr/bin/env python3
"""Safely inspect or mutate SmartBI Baize Agent workflows and tool providers.

These endpoints are internal SmartBI contracts, not stable public SDK APIs.
Authentication headers are read only from environment variables. Agent update
uses a two-phase SHA-256 precondition and always writes a local backup first.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


SENSITIVE_KEYS = {"authorization", "cookie", "password", "secret", "token", "credential"}
AGENT_EDITABLE_FIELDS = ("name", "alias", "desc", "define", "setting")


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if key.lower() in SENSITIVE_KEYS else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def headers_from_environment(items: list[str]) -> dict[str, str]:
    headers = {"Accept": "application/json"}
    for item in items:
        if "=" not in item:
            raise ValueError("--header-env must be HTTP_HEADER=ENV_VAR")
        header, environment_name = item.split("=", 1)
        if not header or not environment_name or any(c in header for c in "\r\n"):
            raise ValueError("invalid header or environment variable name")
        value = os.environ.get(environment_name)
        if value is None:
            raise ValueError(f"environment variable {environment_name!r} is not set")
        if any(c in value for c in "\r\n"):
            raise ValueError(f"environment variable {environment_name!r} contains a newline")
        headers[header] = value
    return headers


class Client:
    def __init__(self, base_url: str, header_env: list[str], timeout: float):
        base = base_url.rstrip("/")
        if base.endswith("/smartbi"):
            base = base[: -len("/smartbi")]
        self.prefix = base + "/smartbi/smartbix/api/dataagent"
        self.headers = headers_from_environment(header_env)
        self.timeout = timeout

    def request(self, method: str, path: str, body: Any = None, *, content_type: str = "application/json") -> Any:
        headers = dict(self.headers)
        data = None
        if body is not None:
            headers["Content-Type"] = content_type
            if content_type.startswith("application/json"):
                data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            elif isinstance(body, str):
                data = body.encode("utf-8")
            else:
                data = bytes(body)
        request = urllib.request.Request(self.prefix + path, data=data, headers=headers, method=method)
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = raw
        if isinstance(payload, dict) and str(payload.get("code")) == "0" and "result" in payload:
            return payload["result"]
        return payload


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_agent(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("agent response must be an object")
    if isinstance(raw.get("define"), (dict, list)):
        raw = dict(raw)
        raw["define"] = json.dumps(raw["define"], ensure_ascii=False, separators=(",", ":"))
    return raw


def agent_digest(agent: dict[str, Any]) -> str:
    return canonical_hash({key: agent.get(key) for key in ("id",) + AGENT_EDITABLE_FIELDS})


def graph_summary(agent: dict[str, Any]) -> dict[str, Any]:
    define = agent.get("define")
    graph: dict[str, Any] = {}
    if isinstance(define, str):
        try:
            parsed = json.loads(define)
            if isinstance(parsed, dict):
                graph = parsed
        except json.JSONDecodeError:
            pass
    return {
        "id": agent.get("id"),
        "name": agent.get("name"),
        "alias": agent.get("alias"),
        "sha256": agent_digest(agent),
        "node_count": len(graph.get("nodes") or []),
        "link_count": len(graph.get("links") or graph.get("edges") or []),
    }


def get_agent(client: Client, agent_id: str) -> dict[str, Any]:
    quoted = urllib.parse.quote(agent_id, safe="")
    return normalize_agent(client.request("GET", f"/graph/{quoted}"))


def command_agent_get(args: argparse.Namespace, client: Client) -> int:
    agent = get_agent(client, args.agent_id)
    write_json(args.output, redact(agent))
    print(json.dumps({"ok": True, "output": str(args.output), **graph_summary(agent)}, ensure_ascii=False, indent=2))
    return 0


def command_agent_update(args: argparse.Namespace, client: Client) -> int:
    live = get_agent(client, args.agent_id)
    current_hash = agent_digest(live)
    patch = normalize_agent(load_json(args.file))
    if patch.get("id") not in (None, args.agent_id):
        raise ValueError("payload id does not match --agent-id")

    candidate = dict(live)
    changed_fields: list[str] = []
    for key in AGENT_EDITABLE_FIELDS:
        if key in patch and patch[key] != live.get(key):
            candidate[key] = patch[key]
            changed_fields.append(key)
    candidate["id"] = args.agent_id
    candidate = normalize_agent(candidate)

    result = {
        "ok": True,
        "mode": "apply" if args.apply else "dry-run",
        "agent_id": args.agent_id,
        "current_sha256": current_hash,
        "candidate_sha256": agent_digest(candidate),
        "changed_fields": changed_fields,
        "current": graph_summary(live),
        "candidate": graph_summary(candidate),
    }
    if not args.apply:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if not args.expect_sha256:
        raise ValueError("--apply requires --expect-sha256 from a prior dry-run")
    if args.expect_sha256 != current_hash:
        raise ValueError("live agent changed after dry-run; export again instead of overwriting")
    if not changed_fields:
        raise ValueError("candidate has no editable changes")

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = args.backup_dir / f"agent-{args.agent_id}-before-{stamp}.json"
    write_json(backup, redact(live))
    update_result = client.request("POST", "/graph/update", candidate)
    if update_result is not True:
        raise RuntimeError(f"agent update returned {update_result!r}")
    verified = get_agent(client, args.agent_id)
    for key in AGENT_EDITABLE_FIELDS:
        if verified.get(key) != candidate.get(key):
            raise RuntimeError(f"read-back mismatch in field {key!r}")
    result.update({"backup": str(backup), "verified": graph_summary(verified)})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def command_agent_create(args: argparse.Namespace, client: Client) -> int:
    payload = normalize_agent(load_json(args.file))
    missing = [key for key in ("name", "alias", "define") if not payload.get(key)]
    if missing:
        raise ValueError(f"agent payload missing required fields: {', '.join(missing)}")
    preview = {"mode": "apply" if args.apply else "dry-run", "parent_id": args.parent_id, **graph_summary(payload)}
    if not args.apply:
        print(json.dumps({"ok": True, **preview}, ensure_ascii=False, indent=2))
        return 0
    parent = urllib.parse.quote(args.parent_id, safe="")
    created_id = client.request("POST", f"/graph/create/{parent}", payload)
    if not isinstance(created_id, str) or not created_id:
        raise RuntimeError(f"agent create returned {created_id!r}")
    verified = get_agent(client, created_id)
    print(json.dumps({"ok": True, **preview, "created_id": created_id, "verified": graph_summary(verified)}, ensure_ascii=False, indent=2))
    return 0


def command_provider_list(args: argparse.Namespace, client: Client) -> int:
    payload = client.request("POST", "/tools/list", {})
    safe = redact(payload)
    if args.output:
        write_json(args.output, safe)
    count = len(payload) if isinstance(payload, list) else None
    print(json.dumps({"ok": True, "provider_count": count, "output": str(args.output) if args.output else None}, ensure_ascii=False, indent=2))
    return 0


def command_provider_get(args: argparse.Namespace, client: Client) -> int:
    query = urllib.parse.urlencode({"name": args.name})
    payload = client.request("GET", "/tools/getByName?" + query)
    if args.output:
        write_json(args.output, redact(payload))
    summary = {
        "ok": True,
        "id": payload.get("id") if isinstance(payload, dict) else None,
        "name": payload.get("name") if isinstance(payload, dict) else None,
        "type": payload.get("type") if isinstance(payload, dict) else None,
        "tool_count": len(payload.get("tools") or []) if isinstance(payload, dict) else None,
        "output": str(args.output) if args.output else None,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def command_provider_parse(args: argparse.Namespace, client: Client) -> int:
    definition = args.openapi_file.read_text(encoding="utf-8")
    query = urllib.parse.urlencode({"type": "OPENAPI"})
    payload = client.request("POST", "/tools/parse?" + query, definition, content_type="text/plain; charset=utf-8")
    if args.output:
        write_json(args.output, redact(payload))
    print(json.dumps({"ok": True, "name": payload.get("name") if isinstance(payload, dict) else None, "tool_count": len(payload.get("tools") or []) if isinstance(payload, dict) else None, "output": str(args.output) if args.output else None}, ensure_ascii=False, indent=2))
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="for example http://smartbi.example:9070")
    parser.add_argument("--header-env", action="append", default=[], metavar="HTTP_HEADER=ENV_VAR")
    parser.add_argument("--timeout", type=float, default=30.0)
    subparsers = parser.add_subparsers(dest="action", required=True)

    agent_get = subparsers.add_parser("agent-get")
    agent_get.add_argument("--agent-id", required=True)
    agent_get.add_argument("--output", required=True, type=Path)
    agent_get.set_defaults(func=command_agent_get)

    agent_update = subparsers.add_parser("agent-update")
    agent_update.add_argument("--agent-id", required=True)
    agent_update.add_argument("--file", required=True, type=Path)
    agent_update.add_argument("--backup-dir", required=True, type=Path)
    agent_update.add_argument("--expect-sha256")
    agent_update.add_argument("--apply", action="store_true")
    agent_update.set_defaults(func=command_agent_update)

    agent_create = subparsers.add_parser("agent-create")
    agent_create.add_argument("--parent-id", required=True)
    agent_create.add_argument("--file", required=True, type=Path)
    agent_create.add_argument("--apply", action="store_true")
    agent_create.set_defaults(func=command_agent_create)

    provider_list = subparsers.add_parser("provider-list")
    provider_list.add_argument("--output", type=Path)
    provider_list.set_defaults(func=command_provider_list)

    provider_get = subparsers.add_parser("provider-get")
    provider_get.add_argument("--name", required=True)
    provider_get.add_argument("--output", type=Path)
    provider_get.set_defaults(func=command_provider_get)

    provider_parse = subparsers.add_parser("provider-parse")
    provider_parse.add_argument("--openapi-file", required=True, type=Path)
    provider_parse.add_argument("--output", type=Path)
    provider_parse.set_defaults(func=command_provider_parse)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        client = Client(args.base_url, args.header_env, args.timeout)
        return int(args.func(args, client))
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError, urllib.error.URLError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
