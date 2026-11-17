#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Read-only Control UI report using the installed agent's gates and ordering."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def load_helper(name):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), SCRIPT_DIR / name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


active = load_helper("list-active-items.py")


def read_api(endpoint):
    # No shell, supplied command, write method, or unbounded network read.
    result = subprocess.run(
        ["glab", "api", endpoint], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=25,
    )
    return json.loads(result.stdout)


def report():
    from datetime import datetime, timezone

    active.api_json = read_api
    user = read_api("user")
    if type(user.get("id")) is not int or not isinstance(user.get("username"), str):
        raise ValueError("Incomplete GitLab identity")
    owner = active.configured_owner()
    projects = {}
    access = {}
    records = []
    for collection in ("issues", "merge_requests"):
        for candidate in active.paginated(f"{collection}?state=opened&scope=assigned_to_me"):
            if not active.project_is_active(candidate.get("project_id"), projects):
                continue
            kind = "merge_request" if collection == "merge_requests" else active.issue_kind(candidate)
            project, endpoint = active.object_endpoint(candidate, kind)
            if project not in access:
                access[project] = user["username"] == owner or active.owner_created_membership(
                    project, user["id"], user["username"], owner,
                )
            if not access[project]:
                continue
            current = read_api(endpoint)
            labels = current.get("labels")
            if (current.get("state") != "opened"
                    or not any(a.get("username") == user["username"] for a in current.get("assignees", []))
                    or not isinstance(labels, list) or any(not isinstance(s, str) for s in labels)):
                continue
            row = active.normalized(current, kind)
            row.update(
                created_at=current.get("created_at"),
                updated_at=current.get("updated_at"),
                project_path=project,
                time_spent=current.get("time_stats", {}).get("total_time_spent", 0),
                item_type=current.get("issue_type", kind),
            )
            if kind != "merge_request":
                related = active.paginated(endpoint + "/related_merge_requests")
                if any(not isinstance(mr, dict) or mr.get("state") not in
                       {"opened", "closed", "merged"} for mr in related):
                    raise ValueError("Incomplete related merge request state")
                # UI metadata only; discovery and its original ranks stay intact.
                row["has_open_merge_request"] = any(mr["state"] == "opened" for mr in related)
            records.append(row)

    records = active.order_items(records)
    todos = []
    # All pending to-dos are visible, not only owner mentions used by automation.
    for todo in active.paginated("todos?state=pending"):
        if todo.get("state") != "pending":
            continue
        target = todo.get("target") or {}
        author = todo.get("author") or {}
        todos.append({
            "id": todo["id"], "title": target.get("title") or todo.get("body") or "GitLab to-do",
            "web_url": todo.get("target_url"), "created_at": todo.get("created_at"),
            "updated_at": target.get("updated_at") or todo.get("updated_at"),
            "project_path": (todo.get("project") or {}).get("path_with_namespace"),
            "labels": target.get("labels", []), "item_type": todo.get("target_type", "To-do"),
            "time_spent": target.get("time_stats", {}).get("total_time_spent", 0),
            "author": author.get("username"), "action": todo.get("action_name"),
            "owner_addressed": author.get("username") == owner and todo.get("action_name") == "directly_addressed",
        })
    sources = []
    for name, description in (
        ("list-active-items.py", "Assigned work, owner membership checks, incident adoption and priority ordering."),
        ("list-directly-addressed-todos.py", "Pending direct mentions from the configured owner, in GitLab order."),
        ("work-queue-report.py", "This read-only report; reuses the discovery gates and ordering without adopting or updating items."),
    ):
        source_prefix = "skills/gitlab-agent/scripts" if "skills" in SCRIPT_DIR.parts else "gitlab-agent/scripts"
        sources.append({"name": name, "path": f"{source_prefix}/{name}",
                        "description": description, "source": (SCRIPT_DIR / name).read_text(encoding="utf-8")})
    return {"user": {"username": user["username"], "name": user.get("name")}, "owner": owner,
            "generated_at": datetime.now(timezone.utc).isoformat(), "items": records,
            "todos": todos, "scripts": sources}


def failure_code(error):
    if isinstance(error, subprocess.TimeoutExpired):
        return "gitlab-timeout"
    if isinstance(error, subprocess.CalledProcessError):
        details = error.stderr or ""
        if isinstance(details, bytes):
            details = details.decode("utf-8", errors="replace")
        statuses = set(re.findall(r"\bHTTP ([1-5][0-9]{2})\b", details))
        if len(statuses) == 1:
            status = statuses.pop()
            known = {"401": "gitlab-authentication", "403": "gitlab-permission",
                     "404": "gitlab-not-found", "429": "gitlab-rate-limit"}
            return known.get(status, "gitlab-unavailable" if status.startswith("5") else "gitlab-api")
        return "gitlab-api"
    if isinstance(error, FileNotFoundError):
        return "helper-unavailable"
    if isinstance(error, PermissionError):
        return "helper-permission"
    if isinstance(error, json.JSONDecodeError):
        return "api-json-invalid"
    if isinstance(error, (ValueError, KeyError, TypeError)):
        return "report-invalid"
    return "helper-io" if isinstance(error, OSError) else "helper-failed"


def main():
    try:
        print(json.dumps(report()))
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError) as error:
        # Emit only an allowlisted category, never commands, endpoints, output,
        # headers, credentials or an exception representation.
        print("WORK_QUEUE_ERROR=" + json.dumps({"error_code": failure_code(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
