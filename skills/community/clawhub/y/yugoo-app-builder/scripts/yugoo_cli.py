#!/usr/bin/env python3
"""
Yugoo Platform CLI Client

Stateless command-line interface for the Yugoo (语构) chat API.
Designed for AI agent integrations (skills) — all output is JSON lines on stdout.

Usage:
    python yugoo_cli.py [--token <jwt>] [--base-url URL] [--insecure] <command> [options]

IMPORTANT: Global options (--token, --base-url, --insecure, --timeout) must appear
BEFORE the subcommand. Placing them after the subcommand will cause an error.

Environment variables:
    YUGOO_BASE_URL       - Platform base URL (alternative to --base-url)
    CREO4U_SKILL_API_KEY - API key for authentication (alternative to --token)
"""

import argparse
import hashlib
import json
import os
import sys
import time
from typing import Any, Dict, Iterator, List, NoReturn, Optional

try:
    import requests
except ImportError:
    print(
        "Error: 'requests' package not installed. Run: pip install requests",
        file=sys.stderr,
    )
    sys.exit(1)

DEFAULT_BASE_URL = "https://creo4u.com/autoagent/api"
VERSION = "1.0.0"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": f"yugoo-cli/{VERSION}",
    }


def _sse_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "User-Agent": f"yugoo-cli/{VERSION}",
    }


def _emit(obj: Any) -> None:
    """Write a single JSON line to stdout."""
    print(json.dumps(obj, ensure_ascii=False, default=str), flush=True)


def _log(msg: str) -> None:
    """Write a message to stderr."""
    print(msg, file=sys.stderr, flush=True)


def _die(msg: str, code: int = 1) -> NoReturn:
    """Print error to stderr and exit."""
    print(json.dumps({"error": msg}, ensure_ascii=False), file=sys.stderr)
    sys.exit(code)


def _raise_for_api_error(resp: "requests.Response") -> Any:
    """Check HTTP status and return parsed JSON body. Raises on error."""
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        try:
            body = resp.json()
        except Exception:
            body = {"raw": resp.text}
        error_info = {
            "error": body.get("detail", body) if isinstance(body, dict) else body,
            "status_code": resp.status_code,
        }
        _log(json.dumps(error_info, ensure_ascii=False, default=str))
        sys.exit(1)
    return resp.json()


def _get(cfg: dict, path: str, params: Optional[dict] = None) -> Any:
    """HTTP GET helper."""
    url = f"{cfg['base_url']}{path}"
    try:
        resp = requests.get(url, headers=_headers(cfg["token"]), params=params, timeout=cfg["timeout"], verify=cfg["verify"])
    except requests.exceptions.ConnectionError:
        _die(f"Connection failed: {url}")
    except requests.exceptions.Timeout:
        _die(f"Request timeout: {url}")
    return _raise_for_api_error(resp)


def _get_text(cfg: dict, path: str) -> str:
    """HTTP GET helper that returns plain text."""
    url = f"{cfg['base_url']}{path}"
    try:
        resp = requests.get(url, headers=_headers(cfg["token"]), timeout=cfg["timeout"], verify=cfg["verify"])
    except requests.exceptions.ConnectionError:
        _die(f"Connection failed: {url}")
    except requests.exceptions.Timeout:
        _die(f"Request timeout: {url}")
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        try:
            body = resp.json()
        except Exception:
            body = {"raw": resp.text}
        _log(json.dumps({"error": body, "status_code": resp.status_code}, ensure_ascii=False, default=str))
        sys.exit(1)
    return resp.text


def _post(cfg: dict, path: str, body: Optional[dict] = None) -> Any:
    """HTTP POST helper."""
    url = f"{cfg['base_url']}{path}"
    try:
        resp = requests.post(url, headers=_headers(cfg["token"]), json=body or {}, timeout=cfg["timeout"], verify=cfg["verify"])
    except requests.exceptions.ConnectionError:
        _die(f"Connection failed: {url}")
    except requests.exceptions.Timeout:
        _die(f"Request timeout: {url}")
    return _raise_for_api_error(resp)


def _delete(cfg: dict, path: str) -> Any:
    """HTTP DELETE helper."""
    url = f"{cfg['base_url']}{path}"
    try:
        resp = requests.delete(url, headers=_headers(cfg["token"]), timeout=cfg["timeout"], verify=cfg["verify"])
    except requests.exceptions.ConnectionError:
        _die(f"Connection failed: {url}")
    except requests.exceptions.Timeout:
        _die(f"Request timeout: {url}")
    return _raise_for_api_error(resp)


def _patch(cfg: dict, path: str, body: Optional[dict] = None) -> Any:
    """HTTP PATCH helper."""
    url = f"{cfg['base_url']}{path}"
    try:
        resp = requests.patch(url, headers=_headers(cfg["token"]), json=body or {}, timeout=cfg["timeout"], verify=cfg["verify"])
    except requests.exceptions.ConnectionError:
        _die(f"Connection failed: {url}")
    except requests.exceptions.Timeout:
        _die(f"Request timeout: {url}")
    return _raise_for_api_error(resp)


# ---------------------------------------------------------------------------
# SSE Streaming
# ---------------------------------------------------------------------------


def stream_sse(
    cfg: dict,
    path: str,
    last_event_id: Optional[str] = None,
    snapshot_interval: Optional[int] = None,
) -> Iterator[Dict[str, Any]]:
    """
    Connect to SSE endpoint and yield parsed events.

    Each yielded dict has:
      {"event": str, "sequence": str|None, "data": dict|str}

    Terminal events: "completed", "error"
    """
    url = f"{cfg['base_url']}{path}"
    headers = _sse_headers(cfg["token"])
    if last_event_id is not None:
        headers["Last-Event-ID"] = str(last_event_id)

    params = {}
    if snapshot_interval is not None:
        params["snapshot_interval"] = snapshot_interval

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params or None,
            stream=True,
            timeout=(cfg["timeout"], None),  # connect timeout, no read timeout
            verify=cfg["verify"],
        )
    except requests.exceptions.ConnectionError:
        _die(f"SSE connection failed: {url}")
    except requests.exceptions.Timeout:
        _die(f"SSE connection timeout: {url}")

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        try:
            body = resp.json()
        except Exception:
            body = {"raw": resp.text}
        _log(json.dumps({"error": body, "status_code": resp.status_code}, ensure_ascii=False, default=str))
        sys.exit(1)

    # Parse SSE frames
    # SSE field prefixes
    SSE_DATA_PREFIX = "data" + ":"  # "" - constructed to avoid rendering issues
    SSE_ID_PREFIX = "id:"
    SSE_EVENT_PREFIX = "event:"

    current_id = None
    current_event = None
    current_data_buf = ""

    for line in resp.iter_lines(decode_unicode=True):
        if line is None:
            continue

        if line == "":
            # Empty line = end of SSE frame
            if current_event or current_data_buf:
                parsed_payload: Any = {}
                if current_data_buf:
                    try:
                        parsed_payload = json.loads(current_data_buf)
                    except json.JSONDecodeError:
                        parsed_payload = current_data_buf

                event_obj = {
                    "event": current_event or "message",
                    "sequence": current_id,
                    "data": parsed_payload,
                }
                yield event_obj

                # Check for terminal events
                if current_event in ("completed", "error"):
                    return

            current_id = None
            current_event = None
            current_data_buf = ""

        elif line.startswith(SSE_ID_PREFIX):
            current_id = line[len(SSE_ID_PREFIX):].strip()
        elif line.startswith(SSE_EVENT_PREFIX):
            current_event = line[len(SSE_EVENT_PREFIX):].strip()
        elif line.startswith(SSE_DATA_PREFIX):
            data_part = line[len(SSE_DATA_PREFIX):].strip()
            if current_data_buf:
                current_data_buf += data_part
            else:
                current_data_buf = data_part


# ---------------------------------------------------------------------------
# Snapshot Result Extraction
# ---------------------------------------------------------------------------


def extract_result(snapshot_data: dict, message_id: Optional[str] = None) -> dict:
    """
    Extract structured development results from a CopilotInterface snapshot.

    Walks through runs[message_id].messages to find assistant responses
    with files_generated, files_modified, summary, and extracts task status
    from OperationLogPanel.
    """
    # Unwrap Result envelope, then unwrap Snapshot.data to get CopilotInterface
    outer = snapshot_data.get("data", snapshot_data) if isinstance(snapshot_data, dict) else snapshot_data
    inner = outer.get("data", outer) if isinstance(outer, dict) else outer
    runs = inner.get("runs", {}) if isinstance(inner, dict) else {}

    if not runs:
        return {"error": "No runs found in snapshot"}

    # Determine which run(s) to extract from
    if message_id and message_id in runs:
        target_runs = {message_id: runs[message_id]}
    else:
        # Use the latest run (last key)
        last_key = list(runs.keys())[-1]
        target_runs = {last_key: runs[last_key]}

    results: List[dict] = []
    for mid, run in target_runs.items():
        files_generated: List[str] = []
        files_modified: List[str] = []
        summaries: List[str] = []
        assistant_msgs: List[str] = []

        for msg in run.get("messages", []):
            if msg.get("role") != "assistant":
                continue
            content = msg.get("content")
            if content:
                assistant_msgs.append(content)
            if msg.get("files_generated"):
                files_generated.extend(msg["files_generated"])
            if msg.get("files_modified"):
                files_modified.extend(msg["files_modified"])
            if msg.get("summary"):
                summaries.append(msg["summary"])

        # Extract tasks from OperationLogPanel
        tasks: List[dict] = []
        panels = run.get("panels", {})
        op_log = panels.get("OperationLogPanel", {})
        for phase in op_log.get("phases", []):
            payload = phase.get("payload", {})
            for task in payload.get("tasks", []):
                task_info = {
                    "task_id": task.get("task_id", ""),
                    "title": task.get("title", ""),
                    "status": task.get("status", ""),
                    "type": task.get("type", ""),
                }
                task_info["sub_tasks"] = []
                for st in task.get("sub_tasks", []):
                    task_info["sub_tasks"].append({
                        "sub_task_id": st.get("sub_task_id", ""),
                        "file_name": st.get("file_name", st.get("task_name", "")),
                        "status": st.get("status", ""),
                    })
                for f in task.get("files", []):
                    task_info["sub_tasks"].append({
                        "sub_task_id": f.get("file_id", ""),
                        "file_name": f.get("file_path", f.get("file_name", "")),
                        "status": f.get("status", ""),
                    })
                if not task_info["sub_tasks"]:
                    del task_info["sub_tasks"]
                tasks.append(task_info)

            # AutoCopilot phases have goal instead of tasks
            goal = payload.get("goal")
            if goal:
                tasks.append({
                    "task_id": goal.get("plan_id", ""),
                    "title": goal.get("goal", ""),
                    "status": goal.get("status", ""),
                    "type": "auto_copilot_goal",
                })

        result = {
            "conversation_id": outer.get("conversation_id", "") if isinstance(outer, dict) else "",
            "message_id": mid,
            "status": run.get("state", "unknown"),
            "summary": summaries[-1] if summaries else None,
            "files_generated": sorted(set(files_generated)),
            "files_modified": sorted(set(files_modified)),
            "assistant_messages": assistant_msgs,
            "tasks": tasks,
            "error": run.get("error"),
            "token_usage": run.get("metadata", {}).get("token_usage"),
            "credit_usage": run.get("metadata", {}).get("credit_usage"),
            "started_at": run.get("started_at"),
            "completed_at": run.get("completed_at"),
        }
        results.append(result)

    if len(results) == 1:
        return results[0]
    return {"results": results}


# ---------------------------------------------------------------------------
# Polling Mode
# ---------------------------------------------------------------------------


def poll_until_complete(
    cfg: dict,
    conversation_id: str,
    message_id: str,
    interval: float = 15.0,
    max_iterations: int = 40,
) -> Iterator[Dict[str, Any]]:
    """
    Poll the snapshot endpoint until the run for message_id reaches terminal state.
    Yields structured poll events.

    Args:
        interval: Polling interval in seconds (default: 15s)
        max_iterations: Max polling iterations (default: 40 = 10 minutes)
    """
    path = f"/chat/v3/conversations/{conversation_id}/messages"
    iteration = 0

    # Terminal states that indicate the run is finished
    TERMINAL_STATES = {"completed", "failed", "cancelled", "interrupted"}

    while True:
        iteration += 1
        snapshot = _get(cfg, path)
        # Unwrap Result envelope, then unwrap Snapshot.data to get CopilotInterface
        outer = snapshot.get("data", snapshot) if isinstance(snapshot, dict) else {}
        data = outer.get("data", outer) if isinstance(outer, dict) else {}
        runs = data.get("runs", {}) if isinstance(data, dict) else {}
        run = runs.get(message_id, {}) if isinstance(runs, dict) else {}
        state = run.get("state", "pending") if isinstance(run, dict) else "pending"

        # Check panels for task completion status
        panels = run.get("panels", {})
        op_log = panels.get("OperationLogPanel", {})
        phases = op_log.get("phases", [])

        # Determine if all phases/tasks are actually done
        has_executing_phase = False
        has_pending_phase = False

        for phase in phases:
            payload = phase.get("payload", {})
            phase_status = payload.get("status", "")
            if phase_status == "executing":
                has_executing_phase = True
            if phase_status == "pending":
                has_pending_phase = True

        # Check goal status if present (auto_copilot)
        has_executing_goal = False
        for phase in phases:
            payload = phase.get("payload", {})
            goal = payload.get("goal")
            if goal and goal.get("status") == "executing":
                has_executing_goal = True

        # Only consider complete if state is terminal AND no executing phases/goals
        if state in TERMINAL_STATES:
            if has_executing_phase or has_executing_goal:
                # State says complete but tasks still running - keep polling
                _emit({"event": "poll", "iteration": iteration, "state": "executing"})
            else:
                yield {"event": "poll_completed", "iteration": iteration, "state": state, "snapshot": snapshot}
                return
        elif has_executing_phase or has_executing_goal:
            # Still executing
            _emit({"event": "poll", "iteration": iteration, "state": "executing"})
        else:
            _emit({"event": "poll", "iteration": iteration, "state": state})

        if max_iterations > 0 and iteration >= max_iterations:
            yield {"event": "poll_timeout", "iteration": iteration, "state": state, "snapshot": snapshot}
            return

        time.sleep(interval)


# ---------------------------------------------------------------------------
# Command Handlers
# ---------------------------------------------------------------------------


def cmd_create(args: argparse.Namespace, cfg: dict) -> None:
    """Create a new conversation."""
    body = {"name": args.name}
    result = _post(cfg, "/chat/v3/conversations", body)
    _emit(result)


def _file_md5(filepath: str) -> str:
    """Calculate MD5 hash of a file."""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_upload(args: argparse.Namespace, cfg: dict) -> None:
    """Upload a local file as a chat attachment."""
    filepath = args.file
    if not os.path.isfile(filepath):
        _die(f"File not found: {filepath}")

    filename = os.path.basename(filepath)
    file_size = os.path.getsize(filepath)
    _log(f"Calculating MD5 for {filename} ({file_size} bytes)...")
    file_md5 = _file_md5(filepath)

    # Step 1: Get upload credentials
    _log("Getting upload credentials...")
    creds = _get(cfg, "/chat/v3/attachments/upload-url", params={
        "fileMd5": file_md5,
        "filename": filename,
    })

    oss_path = creds.get("ossPath") or creds.get("oss_path", "")
    upload_host = creds.get("host", "")
    if upload_host.startswith("//"):
        upload_host = "https:" + upload_host

    # Step 2: Upload file to OSS
    _log(f"Uploading to OSS: {oss_path}...")
    with open(filepath, "rb") as f:
        upload_data = {
            "key": oss_path,
            "OSSAccessKeyId": creds.get("access_id", ""),
            "policy": creds.get("policy", ""),
            "signature": creds.get("signature", ""),
            "success_action_status": "200",
        }
        upload_files = {"file": (filename, f)}
        try:
            resp = requests.post(
                upload_host, data=upload_data, files=upload_files,
                timeout=300,
            )
        except requests.exceptions.ConnectionError:
            _die(f"OSS upload connection failed: {upload_host}")
        except requests.exceptions.Timeout:
            _die("OSS upload timed out")

    if resp.status_code not in (200, 204):
        _die(f"OSS upload failed with status {resp.status_code}: {resp.text}")

    _log("Upload complete.")
    _emit({
        "oss_path": oss_path,
        "filename": filename,
        "file_md5": file_md5,
        "size_bytes": file_size,
    })


def cmd_models(args: argparse.Namespace, cfg: dict) -> None:
    """List available presets and models for --model-choice."""
    result = _get(cfg, "/models")
    # Normalize Result envelope to its payload when present
    if isinstance(result, dict) and "data" in result and isinstance(result["data"], dict):
        result = result["data"]
    _emit(result)


def cmd_chat(args: argparse.Namespace, cfg: dict) -> None:
    """Send a message and optionally watch the response stream."""
    # Resolve content: --file takes priority, then --content, then error
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                content = fh.read()
        except FileNotFoundError:
            _die(f"File not found: {args.file}")
        except OSError as exc:
            _die(f"Cannot read file {args.file}: {exc}")
    elif args.content:
        content = args.content
        if content == "-":
            content = sys.stdin.read()
    else:
        _die("Either --content (-m) or --file (-f) is required")

    body: Dict[str, Any] = {"content": content}
    if args.conversation_id:
        body["conversation_id"] = args.conversation_id
    if args.agent_name:
        body["agent_name"] = args.agent_name
    if args.model_choice:
        body["model_choice"] = args.model_choice
    if args.context:
        try:
            body["context"] = json.loads(args.context)
        except json.JSONDecodeError:
            _die("--context must be valid JSON")

    # Merge attachments into context
    if args.attachment:
        ctx = body.get("context") or {}
        ctx["attachments"] = args.attachment
        body["context"] = ctx

    # Step 1: Send message
    result = _post(cfg, "/chat/v3/messages", body)

    # Check for business-level errors (API returns 200 but with error in body)
    if isinstance(result, dict):
        if result.get("code") == -1 or result.get("success") is False:
            error_msg = result.get("message", "Unknown error")
            _die(error_msg)

    data = result.get("data", result) if isinstance(result, dict) else result
    message_id = data.get("message_id", "")
    conversation_id = data.get("conversation_id", "")

    # Emit accepted event
    _emit({
        "event": "message_accepted",
        "message_id": message_id,
        "conversation_id": conversation_id,
    })

    # Step 2: Optionally watch
    if args.watch:
        # Polling mode with fixed 5s interval
        _log("Polling every 15.0s...")
        for event in poll_until_complete(cfg, conversation_id, message_id, interval=15.0):
            _emit(event)


def cmd_poll(args: argparse.Namespace, cfg: dict) -> None:
    """Resume polling for a message that is still in progress."""
    conversation_id = args.conversation_id
    message_id = args.message_id

    _log("Resuming poll every 15.0s...")
    for event in poll_until_complete(cfg, conversation_id, message_id, interval=15.0):
        _emit(event)


def cmd_stream(args: argparse.Namespace, cfg: dict) -> None:
    """Watch SSE stream for a specific message."""
    path = f"/chat/v3/conversations/{args.conversation_id}/messages/{args.message_id}/stream"
    for event in stream_sse(
        cfg,
        path,
        last_event_id=args.last_event_id,
        snapshot_interval=args.snapshot_interval,
    ):
        _emit(event)


def cmd_messages(args: argparse.Namespace, cfg: dict) -> None:
    """Get the full snapshot for a conversation."""
    path = f"/chat/v3/conversations/{args.conversation_id}/messages"
    result = _get(cfg, path)
    _emit(result)


def cmd_result(args: argparse.Namespace, cfg: dict) -> None:
    """Extract structured development results from snapshot."""
    path = f"/chat/v3/conversations/{args.conversation_id}/messages"
    snapshot = _get(cfg, path)
    extracted = extract_result(snapshot, message_id=args.message_id)
    _emit(extracted)


def cmd_stop(args: argparse.Namespace, cfg: dict) -> None:
    """Stop message generation."""
    path = f"/chat/v3/conversations/{args.conversation_id}/messages/{args.message_id}/stop"
    result = _post(cfg, path)
    _emit(result)


def cmd_start_runtime(args: argparse.Namespace, cfg: dict) -> None:
    """Start or restart conversation runtime."""
    path = f"/chat/v3/conversations/{args.conversation_id}/start"
    result = _post(cfg, path)
    _emit(result)


def cmd_list(args: argparse.Namespace, cfg: dict) -> None:
    """List conversations."""
    params: Dict[str, Any] = {
        "limit": args.limit,
        "offset": args.offset,
    }
    if args.keyword:
        params["keyword"] = args.keyword
    if args.sort_by:
        params["sort_by"] = args.sort_by
    if args.sort_order:
        params["sort_order"] = args.sort_order
    if args.is_published is not None:
        params["is_published"] = args.is_published

    result = _get(cfg, "/chat/v3/conversations", params=params)
    _emit(result)


def cmd_get(args: argparse.Namespace, cfg: dict) -> None:
    """Get conversation details."""
    path = f"/chat/v3/conversations/{args.conversation_id}"
    result = _get(cfg, path)
    _emit(result)


def cmd_delete(args: argparse.Namespace, cfg: dict) -> None:
    """Terminate a conversation."""
    path = f"/chat/v3/conversations/{args.conversation_id}"
    result = _delete(cfg, path)
    _emit(result)


def cmd_health(args: argparse.Namespace, cfg: dict) -> None:
    """Check sandbox services health."""
    path = f"/chat/v3/conversations/{args.conversation_id}/health"
    result = _get(cfg, path)
    _emit(result)


def cmd_urls(args: argparse.Namespace, cfg: dict) -> None:
    """Get sandbox, preview, and backend URLs."""
    cid = args.conversation_id
    urls: Dict[str, Optional[str]] = {}

    for name, endpoint in [
        ("sandbox_url", f"/chat/v3/conversations/{cid}/sandbox"),
        ("preview_url", f"/chat/v3/conversations/{cid}/preview"),
        ("backend_url", f"/chat/v3/conversations/{cid}/backend"),
    ]:
        try:
            urls[name] = _get_text(cfg, endpoint)
        except SystemExit:
            urls[name] = None

    _emit(urls)


def cmd_download(args: argparse.Namespace, cfg: dict) -> None:
    """Download workspace."""
    path = f"/chat/v3/conversations/{args.conversation_id}/download"
    result = _get(cfg, path)
    _emit(result)


def cmd_versions(args: argparse.Namespace, cfg: dict) -> None:
    """List versions."""
    path = f"/chat/v3/conversations/{args.conversation_id}/versions"
    params = {}
    if args.sort_order:
        params["sort_order"] = args.sort_order
    result = _get(cfg, path, params=params or None)
    _emit(result)


def cmd_current_version(args: argparse.Namespace, cfg: dict) -> None:
    """Get current version info."""
    path = f"/chat/v3/conversations/{args.conversation_id}/versions/current"
    result = _get(cfg, path)
    _emit(result)


def cmd_restore_version(args: argparse.Namespace, cfg: dict) -> None:
    """Restore to a specific version."""
    path = f"/chat/v3/conversations/{args.conversation_id}/versions/{args.version}/restore"
    result = _post(cfg, path)
    _emit(result)


def cmd_copy(args: argparse.Namespace, cfg: dict) -> None:
    """Copy a conversation."""
    path = f"/chat/v3/conversations/{args.conversation_id}/copy"
    body: Dict[str, Any] = {}
    if args.new_name:
        body["new_name"] = args.new_name
    result = _post(cfg, path, body)
    _emit(result)

    # Optionally poll status
    if args.wait:
        data = result.get("data", result) if isinstance(result, dict) else result
        new_conversation_id = data.get("conversation_id", "")
        if new_conversation_id:
            _log("Polling copy status...")
            poll_copy_status(cfg, new_conversation_id)


def poll_copy_status(cfg: dict, conversation_id: str, interval: float = 5.0, max_iterations: int = 120) -> None:
    """Poll copy status until completion.
    
    Copy operation completes when workspace files are ready.
    Status transitions: copying -> active (ready)
    """
    path = f"/chat/v3/conversations/{conversation_id}"
    
    TERMINAL_STATUSES = {"active", "failed"}
    
    for iteration in range(1, max_iterations + 1):
        result = _get(cfg, path)
        data = result.get("data", result) if isinstance(result, dict) else result
        status = data.get("status", "unknown")

        _emit({"iteration": iteration, "status": status, "conversation_id": conversation_id})

        if status in TERMINAL_STATUSES:
            if status == "failed":
                _log(f"Copy failed: {data.get('error', 'Unknown error')}")
                sys.exit(1)
            _log("Copy completed successfully!")
            return
        
        _log(f"Copy in progress... (iteration {iteration})")
        time.sleep(interval)
    
    _die("Copy status polling timeout")


def cmd_publish(args: argparse.Namespace, cfg: dict) -> None:
    """Trigger deployment to production."""
    path = "/publish/"
    body: Dict[str, Any] = {
        "session_id": args.conversation_id,
        "republish": True,
    }
    if args.env:
        body["env"] = args.env

    result = _post(cfg, path, body)

    # Check for business-level errors
    if isinstance(result, dict):
        if result.get("code") == -1 or result.get("success") is False:
            error_msg = result.get("message", "Unknown error")
            _die(error_msg)

    data = result.get("data", result) if isinstance(result, dict) else result
    release_id = data.get("publish_id", data.get("id", ""))
    _emit(result)

    # Optionally poll status
    if args.wait:
        _log("Polling publish status...")
        poll_publish_status(cfg, args.conversation_id, release_id)


def cmd_unpublish(args: argparse.Namespace, cfg: dict) -> None:
    """Unpublish (take down) a deployed application."""
    url = f"{cfg['base_url']}/publish/"
    params = {"session_id": args.conversation_id}
    try:
        resp = requests.delete(url, headers=_headers(cfg["token"]), params=params, timeout=cfg["timeout"], verify=cfg["verify"])
    except requests.exceptions.ConnectionError:
        _die(f"Connection failed: {url}")
    except requests.exceptions.Timeout:
        _die(f"Request timeout: {url}")
    result = _raise_for_api_error(resp)
    _emit(result)


def cmd_publish_status(args: argparse.Namespace, cfg: dict) -> None:
    """Check the status of a deployment."""
    path = f"/publish/session/{args.conversation_id}/status"
    result = _get(cfg, path)
    _emit(result)


def poll_publish_status(cfg: dict, conversation_id: str, release_id: str, interval: float = 15.0, max_iterations: int = 40) -> None:
    """Poll publish status until completion."""
    path = f"/publish/session/{conversation_id}/status"

    TERMINAL_STATES = {"published", "published", "failed", "COMPLETED", "completed", "failed"}

    for iteration in range(1, max_iterations + 1):
        result = _get(cfg, path)
        data = result.get("data", result) if isinstance(result, dict) else result
        status = data.get("status", data.get("state", "UNKNOWN"))

        _emit({"iteration": iteration, "status": status})

        if status in TERMINAL_STATES:
            if status == "failed" or status == "FAILED":
                _log(f"Publish failed: {data.get('message', data.get('error', 'Unknown error'))}")
                sys.exit(1)
            _log("Publish completed successfully!")
            return

        time.sleep(interval)

    _die("Publish status polling timeout")


def cmd_rename(args: argparse.Namespace, cfg: dict) -> None:
    """Rename a conversation."""
    path = f"/chat/v3/conversations/{args.conversation_id}/name"
    body = {"name": args.name}
    result = _patch(cfg, path, body)
    _emit(result)


def cmd_market_list(args: argparse.Namespace, cfg: dict) -> None:
    """List app market items."""
    params: Dict[str, Any] = {
        "limit": args.limit,
        "offset": args.offset,
    }
    if args.keyword:
        params["keyword"] = args.keyword
    if args.category_id is not None:
        params["category_id"] = args.category_id
    if args.sort_by:
        params["sort_by"] = args.sort_by
    result = _get(cfg, "/app-market/items", params=params)
    _emit(result)


def cmd_clone_market(args: argparse.Namespace, cfg: dict) -> None:
    """Clone an app from the market."""
    path = f"/app-market/items/{args.item_id}/clone"
    result = _post(cfg, path)
    _emit(result)


def cmd_delete_version(args: argparse.Namespace, cfg: dict) -> None:
    """Delete a WIP version."""
    path = f"/chat/v3/conversations/{args.conversation_id}/versions/{args.version}"
    result = _delete(cfg, path)
    _emit(result)


def cmd_finalize_version(args: argparse.Namespace, cfg: dict) -> None:
    """Finalize current WIP version."""
    path = f"/chat/v3/conversations/{args.conversation_id}/versions/finalize"
    result = _post(cfg, path)
    _emit(result)


def cmd_update_version_desc(args: argparse.Namespace, cfg: dict) -> None:
    """Update version description."""
    path = f"/chat/v3/conversations/{args.conversation_id}/versions/{args.version}/description"
    body = {"description": args.description}
    result = _patch(cfg, path, body)
    _emit(result)


def cmd_spending(args: argparse.Namespace, cfg: dict) -> None:
    """Get message-level spending for a conversation."""
    path = f"/credit/spending/sessions/{args.conversation_id}/messages"
    params: Dict[str, Any] = {
        "limit": args.limit,
        "offset": args.offset,
    }
    if args.message_id:
        params["message_id"] = args.message_id
    result = _get(cfg, path, params=params)
    _emit(result)


# ---------------------------------------------------------------------------
# CLI Parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="yugoo",
        description="Yugoo Platform CLI — stateless chat API client for agent integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Global options (--token, --base-url, --insecure, --timeout) must appear\n"
            "BEFORE the subcommand. Example:\n"
            "  yugoo --token TOKEN --insecure create --name \"My App\"   (correct)\n"
            "  yugoo create --token TOKEN --name \"My App\"              (WRONG)\n\n"
            "Environment variables:\n"
            "  YUGOO_BASE_URL   API base URL (default: %(default_url)s)\n"
            "  CREO4U_SKILL_API_KEY API key for authentication"
        ) % {"default_url": DEFAULT_BASE_URL},
    )
    parser.add_argument(
        "--token",
        default=None,
        help="JWT Bearer token (default: CREO4U_SKILL_API_KEY env var)",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("YUGOO_BASE_URL", DEFAULT_BASE_URL),
        help=f"API base URL (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.environ.get("AUTOAGENT_TIMEOUT", "30")),
        help="HTTP request timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--insecure", "-k",
        action="store_true",
        default=os.environ.get("AUTOAGENT_INSECURE", "").lower() in ("1", "true", "yes"),
        help="Disable SSL certificate verification",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # -- create --
    p = sub.add_parser("create", help="Create a new conversation")
    p.add_argument("--name", default="New Conversation", help="Conversation name (default: New Conversation)")

    # -- models --
    p = sub.add_parser("models", help="List available model presets and concrete model ids for --model-choice")

    # -- upload --
    p = sub.add_parser("upload", help="Upload a local file as a chat attachment")
    p.add_argument("--file", required=True, help="Local file path to upload")

    # -- chat --
    p = sub.add_parser("chat", help="Send a message and optionally watch the response stream")
    p.add_argument("-c", "--conversation-id", default=None, help="Conversation ID (omit to auto-create)")
    p.add_argument("-m", "--content", required=False, default=None, help="Message content (use '-' to read from stdin)")
    p.add_argument("-f", "--file", default=None, help="Read message content from a local file path")
    p.add_argument("-w", "--watch", action="store_true", help="Watch for completion via polling (5s interval)")
    p.add_argument("--agent-name", default=None, help="Specific agent to handle the message")
    p.add_argument("--context", default=None, help="JSON string for additional context")
    p.add_argument("--attachment", action="append", default=None, help="OSS path of uploaded attachment (repeatable)")
    p.add_argument(
        "--model-choice",
        default=None,
        help=(
            "Model choice: preset id ('auto' | 'economy' | 'advance' | 'expert') "
            "or a concrete model id from 'models' command. Default is smart routing. "
            "Only affects the Task agent."
        ),
    )

    # -- poll --
    p = sub.add_parser("poll", help="Resume polling for a message still in progress")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")
    p.add_argument("--message-id", required=True, help="Message ID")

    # -- stream --
    p = sub.add_parser("stream", help="Watch SSE stream for a specific message")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")
    p.add_argument("--message-id", required=True, help="Message ID")
    p.add_argument("--last-event-id", default=None, help="Resume from this event ID")
    p.add_argument("--snapshot-interval", type=int, default=None, help="Request snapshot every N events")

    # -- messages --
    p = sub.add_parser("messages", help="Get full conversation snapshot")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")

    # -- result --
    p = sub.add_parser("result", help="Extract structured development results from snapshot")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")
    p.add_argument("--message-id", default=None, help="Specific message run to extract (default: latest)")

    # -- stop --
    p = sub.add_parser("stop", help="Stop message generation")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")
    p.add_argument("--message-id", required=True, help="Message ID")

    # -- start-runtime --
    p = sub.add_parser("start-runtime", help="Start or restart conversation runtime")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")

    # -- list --
    p = sub.add_parser("list", help="List conversations")
    p.add_argument("--limit", type=int, default=50, help="Max results (default: 50)")
    p.add_argument("--offset", type=int, default=0, help="Pagination offset (default: 0)")
    p.add_argument("--keyword", default=None, help="Search keyword")
    p.add_argument("--sort-by", default="updated_at", help="Sort field (default: updated_at)")
    p.add_argument("--sort-order", default="desc", choices=["asc", "desc"], help="Sort direction (default: desc)")
    p.add_argument("--is-published", type=bool, default=None, help="Filter by publish status")

    # -- get --
    p = sub.add_parser("get", help="Get conversation details")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")

    # -- delete --
    p = sub.add_parser("delete", help="Terminate a conversation")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")

    # -- health --
    p = sub.add_parser("health", help="Check sandbox services health")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")

    # -- urls --
    p = sub.add_parser("urls", help="Get sandbox, preview, and backend URLs")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")

    # -- download --
    p = sub.add_parser("download", help="Download workspace")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")

    # -- versions --
    p = sub.add_parser("versions", help="List versions")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")
    p.add_argument("--sort-order", default="desc", choices=["asc", "desc"], help="Sort direction (default: desc)")

    # -- current-version --
    p = sub.add_parser("current-version", help="Get current version info")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")

    # -- restore-version --
    p = sub.add_parser("restore-version", help="Restore to a specific version")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")
    p.add_argument("--version", type=int, required=True, help="Version number to restore")

    # -- copy --
    p = sub.add_parser("copy", help="Copy a conversation")
    p.add_argument("-c", "--conversation-id", required=True, help="Source conversation ID")
    p.add_argument("--new-name", default=None, help="Name for the copied conversation")
    p.add_argument("-w", "--wait", action="store_true", help="Auto-poll copy status until workspace is ready")

    # -- rename --
    p = sub.add_parser("rename", help="Rename a conversation")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")
    p.add_argument("--name", required=True, help="New conversation name")

    # -- publish --
    p = sub.add_parser("publish", help="Trigger deployment to production")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID to publish")
    p.add_argument("-w", "--wait", action="store_true", help="Auto-poll publish status until published or failed")
    p.add_argument("--env", default=None, help="Target environment (default: PRODUCE)")

    # -- unpublish --
    p = sub.add_parser("unpublish", help="Unpublish (take down) a deployed application")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID to unpublish")

    # -- publish-status --
    p = sub.add_parser("publish-status", help="Check the status of a deployment")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")

    # -- market-list --
    p = sub.add_parser("market-list", help="List app market items")
    p.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    p.add_argument("--offset", type=int, default=0, help="Pagination offset (default: 0)")
    p.add_argument("--keyword", default=None, help="Search keyword")
    p.add_argument("--category-id", type=int, default=None, help="Filter by category ID")
    p.add_argument("--sort-by", default=None, help="Sort field (e.g. view_count, clone_count, created_at)")

    # -- clone-market --
    p = sub.add_parser("clone-market", help="Clone an app from the market")
    p.add_argument("--item-id", required=True, help="Market item ID to clone")

    # -- delete-version --
    p = sub.add_parser("delete-version", help="Delete a WIP version")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")
    p.add_argument("--version", type=int, required=True, help="Version number to delete")

    # -- finalize-version --
    p = sub.add_parser("finalize-version", help="Finalize current WIP version")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")

    # -- update-version-desc --
    p = sub.add_parser("update-version-desc", help="Update version description")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")
    p.add_argument("--version", type=int, required=True, help="Version number")
    p.add_argument("--description", required=True, help="New description for the version")

    # -- spending --
    p = sub.add_parser("spending", help="Get message-level spending for a conversation")
    p.add_argument("-c", "--conversation-id", required=True, help="Conversation ID")
    p.add_argument("--message-id", default=None, help="Filter by specific message ID")
    p.add_argument("--limit", type=int, default=50, help="Max results (default: 50)")
    p.add_argument("--offset", type=int, default=0, help="Pagination offset (default: 0)")

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# Command dispatch table
COMMANDS = {
    "create": cmd_create,
    "models": cmd_models,
    "upload": cmd_upload,
    "chat": cmd_chat,
    "poll": cmd_poll,
    "stream": cmd_stream,
    "messages": cmd_messages,
    "result": cmd_result,
    "stop": cmd_stop,
    "start-runtime": cmd_start_runtime,
    "list": cmd_list,
    "get": cmd_get,
    "delete": cmd_delete,
    "health": cmd_health,
    "urls": cmd_urls,
    "download": cmd_download,
    "versions": cmd_versions,
    "current-version": cmd_current_version,
    "restore-version": cmd_restore_version,
    "copy": cmd_copy,
    "rename": cmd_rename,
    "publish": cmd_publish,
    "unpublish": cmd_unpublish,
    "publish-status": cmd_publish_status,
    "market-list": cmd_market_list,
    "clone-market": cmd_clone_market,
    "delete-version": cmd_delete_version,
    "finalize-version": cmd_finalize_version,
    "update-version-desc": cmd_update_version_desc,
    "spending": cmd_spending,
}


def main():
    """Parse CLI arguments and dispatch to the appropriate handler."""
    parser = build_parser()
    args = parser.parse_args()

    # Resolve token: --token arg > CREO4U_SKILL_API_KEY env var > prompt user
    token = args.token
    if not token:
        token = os.environ.get("CREO4U_SKILL_API_KEY")

    if not token:
        # Prompt user for API key
        print("Warning: CREO4U_SKILL_API_KEY environment variable not set.", file=sys.stderr)
        token = input("Please enter your API key: ").strip()
        if not token:
            _die("API key is required")

    # Resolve configuration
    cfg = {
        "token": token,
        "base_url": args.base_url.rstrip("/"),
        "timeout": args.timeout,
        "verify": not args.insecure,
    }

    # Dispatch
    handler = COMMANDS.get(args.command)
    if handler is None:
        _die(f"Unknown command: {args.command}")

    try:
        handler(args, cfg)
    except KeyboardInterrupt:
        sys.exit(0)
    except SystemExit:
        raise
    except Exception as exc:
        _die(str(exc))


if __name__ == "__main__":
    main()
