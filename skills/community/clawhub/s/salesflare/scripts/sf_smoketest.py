#!/usr/bin/env python3
"""Smoke-test Salesflare OpenAPI operations with safe defaults.

Default mode is read-only. With --allow-write, the smoke test uses a lifecycle
flow for supported entities:

  Phase 1 — POST controlled fixtures
  Phase 2 — GET list endpoints and collect IDs
  Phase 3 — GET specific/by-ID endpoints
  Phase 4 — PUT only records created by Phase 1
  Phase 5 — DELETE only records created by Phase 1 (requires --allow-delete)

Writes outside the lifecycle fixture set are skipped. IDs are never invented:
by-ID reads use either records created in this run or IDs discovered from list
responses. PUT/DELETE never targets pre-existing CRM data.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

DEFAULT_OPENAPI_URL = "https://api.salesflare.com/openapi.json"
DEFAULT_BASE_URL = "https://api.salesflare.com"

# Phase constants (used as sort key)
_PHASE_CREATE   = 0
_PHASE_GET_LIST = 1
_PHASE_GET_ID   = 2
_PHASE_UPDATE   = 3
_PHASE_DELETE   = 4

_CUSTOMFIELD_ITEM_CLASSES = ("accounts", "contacts", "opportunities")

_LIFECYCLE_ENTITIES: dict[str, dict[str, Any]] = {
    "account": {
        "sample_key": "account_id",
        "post_path": "/accounts",
        "put_path": "/accounts/{account_id}",
        "delete_path": "/accounts/{account_id}",
        "requires": [],
        "delete_order": 60,
    },
    "contact": {
        "sample_key": "contact_id",
        "post_path": "/contacts",
        "put_path": "/contacts/{contact_id}",
        "delete_path": "/contacts/{contact_id}",
        "requires": ["account_id"],
        "delete_order": 50,
    },
    "opportunity": {
        "sample_key": "opportunity_id",
        "post_path": "/opportunities",
        "put_path": "/opportunities/{id}",
        "delete_path": "/opportunities/{id}",
        "requires": ["account_id"],
        "delete_order": 40,
    },
    "task": {
        "sample_key": "task_id",
        "post_path": "/tasks",
        "put_path": "/tasks/{id}",
        "delete_path": "/tasks/{id}",
        "requires": ["account_id"],
        "delete_order": 30,
    },
    "meeting": {
        "sample_key": "meeting_id",
        "post_path": "/meetings",
        "put_path": "/meetings/{meeting_id}",
        "delete_path": "/meetings/{meeting_id}",
        "requires": ["contact_id"],
        "delete_order": 25,
    },
    "message": {
        "sample_key": "message_id",
        "post_path": "/messages",
        "put_path": "/messages/{message_id}",
        "delete_path": "/messages/{message_id}",
        "requires": ["account_id"],
        "delete_order": 20,
    },
    "tag": {
        "sample_key": "tag_id",
        "post_path": "/tags",
        "put_path": "/tags/{tag_id}",
        "delete_path": "/tags/{tag_id}",
        "requires": [],
        "delete_order": 10,
    },
}

_LIFECYCLE_BY_POST = {spec["post_path"]: name for name, spec in _LIFECYCLE_ENTITIES.items()}
_LIFECYCLE_BY_PUT = {spec["put_path"]: name for name, spec in _LIFECYCLE_ENTITIES.items()}
_LIFECYCLE_BY_DELETE = {spec["delete_path"]: name for name, spec in _LIFECYCLE_ENTITIES.items()}
_LIFECYCLE_CREATE_ORDER = ("account", "contact", "opportunity", "task", "meeting", "message", "tag")

_EXTRA_POST_PATHS = {
    "/accounts/{account_id}/contacts",
    "/accounts/{account_id}/users",
    "/message/{message_id}/feedback",
    "/messages/{message_id}/feedback",
}
_EXTRA_PUT_PATHS = {
    "/accounts/{account_id}/contacts",
    "/accounts/{account_id}/users",
}


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def load_spec(src: str) -> dict[str, Any]:
    if src.startswith("http://") or src.startswith("https://"):
        with urllib.request.urlopen(src, timeout=45) as r:
            return json.loads(r.read().decode("utf-8"))
    return json.loads(Path(src).read_text(encoding="utf-8"))


def call_json(
    method: str,
    url: str,
    api_key: str,
    body: Any | None,
    timeout: int = 45,
    retries: int = 2,
) -> tuple[int, Any]:
    payload = None if body is None else json.dumps(body).encode("utf-8")
    attempt = 0
    while True:
        req = urllib.request.Request(url, data=payload, method=method)
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Accept", "application/json")
        if payload is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read().decode("utf-8", errors="replace")
                try:
                    return int(r.getcode() or 200), json.loads(raw) if raw else {}
                except Exception:
                    return int(r.getcode() or 200), {"raw": raw[:2000]}
        except urllib.error.HTTPError as e:
            code = int(e.code)
            raw = e.read().decode("utf-8", errors="replace")
            if code == 429 and attempt < retries:
                time.sleep(1.5 * (2 ** attempt))
                attempt += 1
                continue
            try:
                return code, json.loads(raw) if raw else {}
            except Exception:
                return code, {"raw": raw[:2000]}
        except Exception as exc:
            if attempt < retries:
                time.sleep(1.5 * (2 ** attempt))
                attempt += 1
                continue
            return 0, {"error": str(exc)}


# ---------------------------------------------------------------------------
# Data extraction helpers
# ---------------------------------------------------------------------------

def _as_list(data: Any) -> list[Any]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in ("data", "items", "results"):
            if isinstance(data.get(k), list):
                return data[k]
    return []


def _first_top_level_id(data: Any) -> int | None:
    for item in _as_list(data):
        if isinstance(item, dict) and isinstance(item.get("id"), int):
            if item.get("id") not in (None, 0):
                return int(item["id"])
    return None


def _extract_id(data: Any) -> int | None:
    if isinstance(data, dict):
        value = data.get("id")
        if isinstance(value, int) and value:
            return value
        for key in ("data", "item", "result"):
            nested = _extract_id(data.get(key))
            if nested:
                return nested
    if isinstance(data, list):
        return _first_top_level_id(data)
    return None


# ---------------------------------------------------------------------------
# Path filling
# ---------------------------------------------------------------------------

def _required_id_key(path: str) -> str | None:
    """Return the samples key whose presence is required to run this path.

    Returns None for paths with no path params, or for paths whose params
    are non-ID placeholders that can be filled safely.
    """
    params = re.findall(r"\{([^}]+)\}", path)
    if not params:
        return None

    named_param_map = {
        "account_id":    "account_id",
        "contact_id":    "contact_id",
        "tag_id":        "tag_id",
        "stage_id":      "stage_id",
        "meeting_id":    "meeting_id",
        "message_id":    "message_id",
        "call_id":       "call_id",
        "datasource_id": "datasource_id",
    }

    for p in params:
        if p in named_param_map:
            return named_param_map[p]

    if path.startswith("/customfields/"):
        if "id" in params:
            return "customfield_id"
        if "customFieldApiField" in params:
            return "customFieldApiField"

    # Bare {id}: context from path prefix
    if "id" in params:
        if path.startswith("/opportunities/"):
            return "opportunity_id"
        if path.startswith("/tasks/"):
            return "task_id"
        if path.startswith("/users/"):
            return "user_id"
        if path.startswith("/groups/"):
            return "group_id"
        if path.startswith("/workflows/"):
            return "workflow_id"
        if path.startswith("/datasources/email/"):
            return "datasource_id"

    # Non-ID params only, such as itemClass — no ID gate needed.
    return None


def fill_path(path: str, samples: dict[str, int | str]) -> str:
    mapping: dict[str, Any] = {
        "account_id":         samples.get("account_id", 0),
        "contact_id":         samples.get("contact_id", 0),
        "stage_id":           samples.get("stage_id", 0),
        "tag_id":             samples.get("tag_id", 0),
        "meeting_id":         samples.get("meeting_id", samples.get("call_id", 0)),
        "message_id":         samples.get("message_id", 0),
        "call_id":            samples.get("call_id", 0),
        "conference_id":      0,
        "record_id":          0,
        "itemClass":          samples.get("customfield_itemClass", "accounts"),
        "customFieldApiField": samples.get("customFieldApiField", ""),
        "id":                 0,
    }

    # Contextualise bare {id}
    if "{id}" in path:
        if path.startswith("/opportunities/"):
            mapping["id"] = samples.get("opportunity_id", 0)
        elif path.startswith("/tasks/"):
            mapping["id"] = samples.get("task_id", 0)
        elif path.startswith("/users/"):
            mapping["id"] = samples.get("user_id", 0)
        elif path.startswith("/groups/"):
            mapping["id"] = samples.get("group_id", 0)
        elif path.startswith("/workflows/"):
            mapping["id"] = samples.get("workflow_id", 0)
        elif path.startswith("/datasources/email/"):
            mapping["id"] = samples.get("datasource_id", 0)
        elif path.startswith("/customfields/"):
            mapping["id"] = samples.get("customfield_id", 0)
            mapping["itemClass"] = samples.get("customfield_itemClass", "accounts")

    if path.startswith("/customfields/") and "{customFieldApiField}" in path:
        mapping["itemClass"] = samples.get(
            "customfield_options_itemClass",
            samples.get("customfield_itemClass", "accounts"),
        )

    def repl(match: re.Match[str]) -> str:
        k = match.group(1)
        return str(mapping.get(k, 0))

    return re.sub(r"\{([^}]+)\}", repl, path)


def lifecycle_create_body(kind: str, samples: dict[str, Any], marker: str) -> Any:
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    end_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 1800))
    if kind == "account":
        return {"name": f"OpenClaw Smoke Account {marker}"}
    if kind == "contact":
        return {
            "email": f"openclaw-smoke-{marker}@example.com",
            "firstname": "OpenClaw",
            "lastname": f"Smoke {marker}",
            "account": samples["account_id"],
        }
    if kind == "opportunity":
        return {
            "account": samples["account_id"],
            "name": f"OpenClaw Smoke Opportunity {marker}",
            "value": 1,
        }
    if kind == "task":
        return {
            "description": f"OpenClaw smoke task {marker}",
            "account": samples["account_id"],
        }
    if kind == "meeting":
        return [
            {
                "date": now_iso,
                "end_date": end_iso,
                "subject": f"OpenClaw smoke meeting {marker}",
                "notes": f"OpenClaw smoke meeting {marker}",
                "participants": [samples["contact_id"]],
                "type": "meeting-live",
            }
        ]
    if kind == "message":
        return {
            "account": samples["account_id"],
            "body": f"OpenClaw smoke internal note {marker}",
        }
    if kind == "tag":
        return {"name": f"openclaw-smoke-{marker}"}
    return {}


def lifecycle_update_body(kind: str, samples: dict[str, Any], marker: str) -> Any:
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    end_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 1800))
    if kind == "account":
        return {"name": f"OpenClaw Smoke Account {marker} Updated"}
    if kind == "contact":
        return {"firstname": "OpenClaw", "lastname": f"Smoke {marker} Updated"}
    if kind == "opportunity":
        return {"name": f"OpenClaw Smoke Opportunity {marker} Updated", "value": 2}
    if kind == "task":
        return {"description": f"OpenClaw smoke task {marker} updated"}
    if kind == "meeting":
        return {
            "date": now_iso,
            "end_date": end_iso,
            "subject": f"OpenClaw smoke meeting {marker} updated",
            "notes": f"OpenClaw smoke meeting {marker} updated",
            "participants": [samples["contact_id"]],
            "type": "meeting-live",
        }
    if kind == "message":
        return {
            "account": samples["account_id"],
            "body": f"OpenClaw smoke internal note {marker} updated",
        }
    if kind == "tag":
        return {"name": f"openclaw-smoke-{marker}-updated"}
    return {}


def missing_requirements(kind: str, samples: dict[str, Any]) -> list[str]:
    spec = _LIFECYCLE_ENTITIES[kind]
    return [key for key in spec["requires"] if key not in samples]


def extra_write_body(path: str, samples: dict[str, Any]) -> tuple[Any | None, list[str]]:
    if path == "/accounts/{account_id}/contacts":
        missing = [key for key in ("account_id", "contact_id") if key not in samples]
        if missing:
            return None, missing
        return [{"id": samples["contact_id"]}], []
    if path == "/accounts/{account_id}/users":
        missing = [key for key in ("account_id", "user_id") if key not in samples]
        if missing:
            return None, missing
        return [{"id": samples["user_id"]}], []
    if path in {"/message/{message_id}/feedback", "/messages/{message_id}/feedback"}:
        if "message_id" not in samples:
            return None, ["message_id"]
        return {"feedback": "helpful"}, []
    return None, ["unsupported"]


def collect_samples_from_get(
    samples: dict[str, int | str],
    path: str,
    resolved_path: str,
    data: Any,
) -> None:
    list_path_map = {
        "/accounts": "account_id",
        "/contacts": "contact_id",
        "/opportunities": "opportunity_id",
        "/tasks": "task_id",
        "/workflows": "workflow_id",
        "/users": "user_id",
        "/tags": "tag_id",
        "/stages": "stage_id",
        "/meetings": "meeting_id",
        "/messages": "message_id",
        "/calls": "call_id",
        "/datasources/email": "datasource_id",
        "/groups": "group_id",
    }
    key = list_path_map.get(path)
    if key and key not in samples:
        value = _first_top_level_id(data)
        if isinstance(value, int):
            samples[key] = value

    if path == "/customfields/{itemClass}":
        item_class = resolved_path.rstrip("/").split("/")[-1]
        collect_customfield_samples(samples, item_class, data)


def collect_customfield_samples(
    samples: dict[str, int | str],
    item_class: str,
    data: Any,
) -> None:
    if not isinstance(data, list):
        return
    for fld in data:
        if not isinstance(fld, dict):
            continue
        field_id = fld.get("id")
        api_field = fld.get("api_field")
        if isinstance(field_id, int) and field_id and "customfield_id" not in samples:
            samples["customfield_id"] = field_id
            samples["customfield_itemClass"] = item_class
        if (
            fld.get("type") == "select"
            and isinstance(api_field, str)
            and api_field
            and "customFieldApiField" not in samples
        ):
            samples["customFieldApiField"] = api_field
            samples["customfield_options_itemClass"] = item_class


def append_default_query(path: str, method: str, op: dict[str, Any]) -> list[tuple[str, str]]:
    q: list[tuple[str, str]] = []

    list_with_limit_prefixes = (
        "/accounts",
        "/contacts",
        "/opportunities",
        "/tasks",
        "/users",
        "/workflows",
        "/tags",
        "/messages",
        "/meetings",
        "/calls",
    )
    if method == "GET" and "{" not in path and path.startswith(list_with_limit_prefixes):
        q.append(("limit", "1"))

    for p in op.get("parameters") or []:
        if p.get("in") != "query" or not p.get("required"):
            continue
        name = p.get("name")
        if name == "limit":
            q.append(("limit", "1"))
        elif name == "offset":
            q.append(("offset", "0"))
        elif name and name != "q":
            q.append((name, "1"))

    if method == "GET" and path == "/persons":
        q = [("search", "a")]

    return q


# ---------------------------------------------------------------------------
# Phase bucketing
# ---------------------------------------------------------------------------

def _phase_for(method: str, path: str) -> int:
    if method == "POST":
        return _PHASE_CREATE
    if method == "GET":
        return _PHASE_GET_LIST if is_list_get_path(path) else _PHASE_GET_ID
    if method in {"PUT", "PATCH"}:
        return _PHASE_UPDATE
    if method == "DELETE":
        return _PHASE_DELETE
    return _PHASE_GET_ID


def is_list_get_path(path: str) -> bool:
    if "{" not in path:
        return True
    return path in {
        "/customfields/{itemClass}",
        "/filterfields/{entity}",
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=DEFAULT_OPENAPI_URL)
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--api-key", default=os.environ.get("SALESFLARE_API_KEY"))
    _skill_dir = Path(__file__).parent.parent
    ap.add_argument("--out-json", default=str(_skill_dir / "references" / "test-results.json"))
    ap.add_argument("--out-md", default=str(_skill_dir / "references" / "test-results.md"))
    ap.add_argument(
        "--allow-write",
        action="store_true",
        help="Allow write operations (POST/PUT/PATCH). Disabled by default.",
    )
    ap.add_argument(
        "--allow-delete",
        action="store_true",
        help="Allow DELETE operations. Requires --allow-write.",
    )
    args = ap.parse_args()

    if not args.api_key:
        raise SystemExit("Missing API key")
    if args.allow_delete and not args.allow_write:
        raise SystemExit("--allow-delete requires --allow-write")

    spec = load_spec(args.source)
    paths = spec.get("paths", {})

    marker = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    samples: dict[str, int | str] = {}
    created: dict[str, int] = {}
    results: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Bucket all spec operations by lifecycle phase; sort for determinism.
    # ------------------------------------------------------------------
    ops: list[tuple[int, str, str, dict[str, Any]]] = []  # (phase, path, method, op)
    for path, methods in paths.items():
        if not isinstance(methods, dict):
            continue
        for method, op in methods.items():
            m = method.upper()
            if m not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
                continue
            ops.append((_phase_for(m, path), path, m, op))

    ops.sort(key=lambda x: (x[0], x[1], x[2]))

    # ------------------------------------------------------------------
    # Phase 1: POST lifecycle fixtures first.
    # ------------------------------------------------------------------
    post_entries = [entry for entry in ops if entry[0] == _PHASE_CREATE]
    post_entries_by_path = {entry[1]: entry for entry in post_entries}

    for kind in _LIFECYCLE_CREATE_ORDER:
        spec_entry = _LIFECYCLE_ENTITIES[kind]
        path = spec_entry["post_path"]
        entry = post_entries_by_path.get(path)
        if not entry:
            continue
        _, path, m, op = entry
        if not args.allow_write:
            results.append(_skip(m, path, op, "Skipped: POST disabled by default (use --allow-write)"))
            continue
        missing = missing_requirements(kind, samples)
        if missing:
            results.append(_skip(m, path, op, f"Skipped: missing lifecycle dependency {', '.join(missing)}"))
            continue
        body = lifecycle_create_body(kind, samples, marker)
        status, data = call_json(m, args.base_url.rstrip("/") + path, args.api_key, body)
        result = _result(_PHASE_CREATE, m, path, path, op, status, data)
        created_id = _extract_id(data)
        if 200 <= status < 300 and isinstance(created_id, int):
            sample_key = _LIFECYCLE_ENTITIES[kind]["sample_key"]
            created[kind] = created_id
            samples[sample_key] = created_id
            result["note"] = f"created {kind}"
        elif 200 <= status < 300:
            result["outcome"] = "client_error"
            result["note"] = f"created {kind} but response did not include an id"
        results.append(result)
        time.sleep(0.1)

    handled_post_paths = {
        _LIFECYCLE_ENTITIES[kind]["post_path"]
        for kind in _LIFECYCLE_CREATE_ORDER
        if _LIFECYCLE_ENTITIES[kind]["post_path"] in post_entries_by_path
    }

    for _, path, m, op in post_entries:
        if path in handled_post_paths:
            continue
        kind = _LIFECYCLE_BY_POST.get(path)
        if path in _EXTRA_POST_PATHS:
            if not args.allow_write:
                results.append(_skip(m, path, op, "Skipped: POST disabled by default (use --allow-write)"))
                continue
            body, missing = extra_write_body(path, samples)
            if missing:
                results.append(_skip(m, path, op, f"Skipped: missing lifecycle dependency {', '.join(missing)}"))
                continue
            filled_path = fill_path(path, samples)
            status, data = call_json(m, args.base_url.rstrip("/") + filled_path, args.api_key, body)
            results.append(_result(_PHASE_CREATE, m, path, filled_path, op, status, data))
            time.sleep(0.1)
            continue
        if not kind:
            results.append(
                _skip(m, path, op, "Skipped: POST is not part of lifecycle smoke and cannot be safely cleaned up")
            )
            continue

    # ------------------------------------------------------------------
    # Phase 2: GET list endpoints and collect IDs.
    # ------------------------------------------------------------------
    for _, path, m, op in [entry for entry in ops if entry[0] == _PHASE_GET_LIST]:
        filled_paths = [fill_path(path, samples)]
        if path == "/customfields/{itemClass}":
            filled_paths = [f"/customfields/{item_class}" for item_class in _CUSTOMFIELD_ITEM_CLASSES]
        elif path.startswith("/filterfields/"):
            filled_paths = ["/filterfields/contact"]

        for filled_path in filled_paths:
            query_pairs = append_default_query(filled_path, m, op)
            url = args.base_url.rstrip("/") + filled_path
            if query_pairs:
                url += "?" + urllib.parse.urlencode(query_pairs, doseq=True)
            status, data = call_json(m, url, args.api_key, None)
            collect_samples_from_get(samples, path, filled_path, data)
            results.append(_result(_PHASE_GET_LIST, m, path, filled_path, op, status, data))
            time.sleep(0.1)

    # ------------------------------------------------------------------
    # Phase 3: GET specific endpoints using created or discovered IDs.
    # ------------------------------------------------------------------
    for _, path, m, op in [entry for entry in ops if entry[0] == _PHASE_GET_ID]:
        if m == "GET" and path == "/tags/{tag_id}":
            results.append(_skip(m, path, op, "Skipped: unsupported in this skill (server-side 500)"))
            continue
        required_key = _required_id_key(path)
        if required_key and required_key not in samples:
            results.append(_skip(m, path, op, f"Skipped: no {required_key} discovered from lifecycle/list probes"))
            continue
        filled_path = fill_path(path, samples)
        query_pairs = append_default_query(filled_path, m, op)
        url = args.base_url.rstrip("/") + filled_path
        if query_pairs:
            url += "?" + urllib.parse.urlencode(query_pairs, doseq=True)
        status, data = call_json(m, url, args.api_key, None)
        results.append(_result(_PHASE_GET_ID, m, path, filled_path, op, status, data))
        time.sleep(0.1)

    # ------------------------------------------------------------------
    # Phase 4: PUT only entities created by this run.
    # ------------------------------------------------------------------
    for _, path, m, op in [entry for entry in ops if entry[0] == _PHASE_UPDATE]:
        kind = _LIFECYCLE_BY_PUT.get(path)
        if not kind:
            if path in _EXTRA_PUT_PATHS:
                if not args.allow_write:
                    results.append(_skip(m, path, op, "Skipped: PUT disabled by default (use --allow-write)"))
                    continue
                body, missing = extra_write_body(path, samples)
                if missing:
                    results.append(_skip(m, path, op, f"Skipped: missing lifecycle dependency {', '.join(missing)}"))
                    continue
                filled_path = fill_path(path, samples)
                status, data = call_json(m, args.base_url.rstrip("/") + filled_path, args.api_key, body)
                results.append(_result(_PHASE_UPDATE, m, path, filled_path, op, status, data))
                time.sleep(0.1)
                continue
            results.append(_skip(m, path, op, "Skipped: PUT/PATCH only runs on lifecycle-created records"))
            continue
        if not args.allow_write:
            results.append(_skip(m, path, op, "Skipped: PUT disabled by default (use --allow-write)"))
            continue
        if kind not in created:
            results.append(_skip(m, path, op, f"Skipped: no {kind} was created in this run"))
            continue
        filled_path = fill_path(path, samples)
        body = lifecycle_update_body(kind, samples, marker)
        status, data = call_json(m, args.base_url.rstrip("/") + filled_path, args.api_key, body)
        results.append(_result(_PHASE_UPDATE, m, path, filled_path, op, status, data))
        time.sleep(0.1)

    # ------------------------------------------------------------------
    # Phase 5: DELETE only entities created by this run, in dependency order.
    # ------------------------------------------------------------------
    delete_entries = [entry for entry in ops if entry[0] == _PHASE_DELETE]
    lifecycle_delete_entries = [
        entry for entry in delete_entries if _LIFECYCLE_BY_DELETE.get(entry[1]) in created
    ]
    lifecycle_delete_entries.sort(
        key=lambda entry: _LIFECYCLE_ENTITIES[_LIFECYCLE_BY_DELETE[entry[1]]]["delete_order"]
    )
    handled_delete_paths = {entry[1] for entry in lifecycle_delete_entries}

    for _, path, m, op in lifecycle_delete_entries:
        kind = _LIFECYCLE_BY_DELETE[path]
        if not args.allow_write:
            results.append(_skip(m, path, op, "Skipped: DELETE requires --allow-write and --allow-delete"))
            continue
        if not args.allow_delete:
            results.append(_skip(m, path, op, "Skipped: DELETE disabled by default (use --allow-delete with --allow-write)"))
            continue
        filled_path = fill_path(path, samples)
        status, data = call_json(m, args.base_url.rstrip("/") + filled_path, args.api_key, None)
        result = _result(_PHASE_DELETE, m, path, filled_path, op, status, data)
        if 200 <= status < 300:
            result["note"] = f"deleted {kind}"
        results.append(result)
        time.sleep(0.1)

    for _, path, m, op in delete_entries:
        if path in handled_delete_paths:
            continue
        kind = _LIFECYCLE_BY_DELETE.get(path)
        if kind:
            results.append(_skip(m, path, op, f"Skipped: no {kind} was created in this run"))
        else:
            results.append(_skip(m, path, op, "Skipped: DELETE only runs on lifecycle-created records"))

    # ------------------------------------------------------------------
    # Aggregate
    # ------------------------------------------------------------------
    by_outcome: dict[str, int] = defaultdict(int)
    by_status: dict[str, int] = defaultdict(int)
    for r in results:
        by_outcome[r["outcome"]] += 1
        if r.get("status") is not None:
            by_status[str(r["status"])] += 1

    payload = {
        "source": args.source,
        "base_url": args.base_url,
        "sample_ids": samples,
        "summary": {
            "total": len(results),
            "by_outcome": dict(sorted(by_outcome.items())),
            "by_status": dict(
                sorted(by_status.items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else 9999)
            ),
        },
        "results": results,
    }

    Path(args.out_json).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # Markdown report
    phase_labels = {
        _PHASE_CREATE: "POST fixtures",
        _PHASE_GET_LIST: "GET list",
        _PHASE_GET_ID:   "GET by-id",
        _PHASE_UPDATE:   "PUT fixtures",
        _PHASE_DELETE:   "DELETE",
    }
    lines = [
        "# Salesflare API smoke test results",
        "",
        f"- Source: `{args.source}`",
        f"- Base URL: `{args.base_url}`",
        f"- Total operations tested: **{len(results)}**",
        "",
        "## Summary",
        "",
    ]
    for k, v in payload["summary"]["by_outcome"].items():
        lines.append(f"- {k}: {v}")
    lines += [
        "",
        "### Status distribution",
        "",
    ]
    for k, v in payload["summary"]["by_status"].items():
        lines.append(f"- {k}: {v}")
    lines += [
        "",
        "## Operation matrix",
        "",
        "| Phase | Method | Path | Status | Outcome | Note |",
        "|---|---|---|---:|---|---|",
    ]
    for r in results:
        note = (r.get("note") or "").replace("|", "\\|").replace("\n", " ")
        st = "" if r.get("status") is None else str(r.get("status"))
        ph = phase_labels.get(r.get("phase", -1), "")
        lines.append(f"| {ph} | {r['method']} | `{r['path']}` | {st} | {r['outcome']} | {note[:120]} |")

    Path(args.out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(payload["summary"], indent=2))
    print(f"Wrote: {args.out_json}")
    print(f"Wrote: {args.out_md}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _result(
    phase: int,
    method: str,
    path: str,
    resolved_path: str,
    op: dict[str, Any],
    status: int,
    data: Any,
) -> dict[str, Any]:
    if status == 0:
        outcome = "network_error"
    elif 200 <= status < 300:
        outcome = "ok"
    elif 400 <= status < 500:
        outcome = "client_error"
    else:
        outcome = "server_error"

    note = ""
    if isinstance(data, dict):
        for k in ("error", "message", "details", "raw"):
            if k in data and data[k]:
                note = str(data[k])[:180]
                break
    elif isinstance(data, list):
        note = f"list[{len(data)}]"

    return {
        "phase": phase,
        "method": method,
        "path": path,
        "resolved_path": resolved_path,
        "operationId": op.get("operationId"),
        "summary": op.get("summary"),
        "status": status,
        "outcome": outcome,
        "note": note,
    }


def _skip(method: str, path: str, op: dict[str, Any], note: str) -> dict[str, Any]:
    return {
        "phase": _phase_for(method, path),
        "method": method,
        "path": path,
        "operationId": op.get("operationId"),
        "summary": op.get("summary"),
        "status": None,
        "outcome": "skipped",
        "note": note,
    }


if __name__ == "__main__":
    main()
