from __future__ import annotations

import json
import os
import signal
import shlex
import subprocess
import sys
import tomllib
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


KNOWN_ACTIONS = {
    "bootstrap",
    "login",
    "crawl_seed",
    "crawl_homefeed",
    "collect_nightly",
    "report_weekly",
    "list_contactable",
    "job_status",
    "job_logs",
    "job_stop",
    "ack_event",
}

BACKGROUND_ACTIONS = {"crawl_seed", "crawl_homefeed", "collect_nightly"}

EXPECTED_ARTIFACTS = {
    "crawl_seed": ("accounts.csv", "contact_leads.csv", "run_report.json"),
    "crawl_homefeed": ("accounts.csv", "contact_leads.csv", "run_report.json"),
    "collect_nightly": (
        "daily-run-report.json",
        "weekly-growth-report.json",
        "contactable_creators.csv",
    ),
    "report_weekly": (
        "weekly-growth-report.json",
        "contactable_creators.csv",
    ),
}

CONFIG_DEFAULTS = (
    ("default_crawl_budget", "crawl_budget"),
    ("default_report_days", "days"),
    ("default_list_limit", "limit"),
)

CLI_ARTIFACT_DEFAULTS = {
    "crawl_seed": "output",
    "crawl_homefeed": "output",
    "collect_nightly": "reports",
    "report_weekly": "reports",
}

EXPECTED_PROJECT_NAME = "red-crawler"
DEFAULT_ACTION = "crawl_homefeed"
DEFAULT_HEARTBEAT_DIR = ".openclaw/red-crawler"
DEFAULT_LOG_DIR = "logs/jobs"
JOB_SCHEMA_VERSION = 1


def extract_config(context):
    if not isinstance(context, dict):
        return {}
    config = context.get("config", {})
    return config if isinstance(config, dict) else {}


def merge_config(input_data, context):
    if not isinstance(input_data, dict):
        return structured_error(
            "validation_error",
            "input must be a mapping.",
            "Pass a JSON object with action and parameters.",
        )
    config = extract_config(context)
    merged = dict(config)
    for key, value in input_data.items():
        if value is not None:
            merged[key] = value
    for default_key, target_key in CONFIG_DEFAULTS:
        if target_key not in merged and merged.get(default_key) is not None:
            merged[target_key] = merged[default_key]
    if not str(merged.get("action", "")).strip():
        merged["action"] = DEFAULT_ACTION
    return merged


def structured_error(error_type, message, suggested_fix):
    return {
        "status": "error",
        "error_type": error_type,
        "message": message,
        "suggested_fix": suggested_fix,
    }


def _display_command(argv):
    return shlex.join(str(part) for part in argv)


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _safe_slug(value):
    allowed = []
    for char in str(value):
        if char.isalnum() or char in {"-", "_"}:
            allowed.append(char)
        else:
            allowed.append("_")
    return "".join(allowed).strip("_")


def _read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp_path.replace(path)


def _get_runner_command(resolved):
    runner_command = resolved.get("runner_command")
    if runner_command is None:
        return ["red-crawler"]
    if isinstance(runner_command, str):
        parts = shlex.split(runner_command)
        return parts if parts else ["red-crawler"]
    if isinstance(runner_command, Sequence):
        return [str(part) for part in runner_command]
    return ["red-crawler"]


def _extend_flag(argv, flag, value):
    if value is not None:
        argv.extend([flag, str(value)])


def _extend_bool_flag(argv, flag, value):
    if value is True:
        argv.append(flag)


def _extend_browser_flags(argv, resolved):
    _extend_flag(argv, "--browser-mode", resolved.get("browser_mode"))
    _extend_flag(argv, "--browser-endpoint", resolved.get("browser_endpoint"))
    _extend_flag(argv, "--browser-auth", resolved.get("browser_auth"))
    _extend_flag(argv, "--proxy", resolved.get("proxy"))
    _extend_flag(argv, "--proxy-list", resolved.get("proxy_list"))
    _extend_flag(argv, "--rotation-mode", resolved.get("rotation_mode"))
    _extend_flag(argv, "--rotation-retries", resolved.get("rotation_retries"))
    if resolved.get("randomize_headers") is False:
        argv.append("--no-randomize-headers")


def build_login_command(resolved):
    argv = _get_runner_command(resolved) + ["login"]
    _extend_flag(argv, "--save-state", resolved.get("storage_state"))
    _extend_flag(argv, "--login-url", resolved.get("login_url"))
    return argv


def build_crawl_seed_command(resolved):
    argv = _get_runner_command(resolved) + ["crawl-seed"]
    _extend_flag(argv, "--seed-url", resolved.get("seed_url"))
    _extend_flag(argv, "--storage-state", resolved.get("storage_state"))
    _extend_flag(argv, "--max-accounts", resolved.get("max_accounts"))
    _extend_flag(argv, "--max-depth", resolved.get("max_depth"))
    _extend_bool_flag(
        argv,
        "--include-note-recommendations",
        resolved.get("include_note_recommendations"),
    )
    _extend_bool_flag(argv, "--safe-mode", resolved.get("safe_mode"))
    _extend_flag(argv, "--cache-dir", resolved.get("cache_dir"))
    _extend_flag(argv, "--cache-ttl-days", resolved.get("cache_ttl_days"))
    _extend_flag(argv, "--gender-filter", resolved.get("gender_filter"))
    _extend_browser_flags(argv, resolved)
    _extend_flag(argv, "--db-path", resolved.get("db_path"))
    _extend_flag(argv, "--output-dir", resolved.get("output_dir"))
    return argv


def build_crawl_homefeed_command(resolved):
    argv = _get_runner_command(resolved) + ["crawl-homefeed"]
    _extend_flag(argv, "--homefeed-url", resolved.get("homefeed_url"))
    _extend_flag(argv, "--storage-state", resolved.get("storage_state"))
    _extend_flag(argv, "--max-accounts", resolved.get("max_accounts"))
    _extend_flag(argv, "--search-scroll-rounds", resolved.get("search_scroll_rounds"))
    _extend_bool_flag(argv, "--safe-mode", resolved.get("safe_mode"))
    _extend_flag(argv, "--cache-dir", resolved.get("cache_dir"))
    _extend_flag(argv, "--cache-ttl-days", resolved.get("cache_ttl_days"))
    _extend_flag(argv, "--gender-filter", resolved.get("gender_filter"))
    _extend_browser_flags(argv, resolved)
    _extend_flag(argv, "--db-path", resolved.get("db_path"))
    _extend_flag(argv, "--output-dir", resolved.get("output_dir"))
    return argv


def build_collect_nightly_command(resolved):
    argv = _get_runner_command(resolved) + ["collect-nightly"]
    _extend_flag(argv, "--storage-state", resolved.get("storage_state"))
    _extend_flag(argv, "--db-path", resolved.get("db_path"))
    _extend_flag(argv, "--report-dir", resolved.get("report_dir"))
    _extend_flag(argv, "--cache-dir", resolved.get("cache_dir"))
    _extend_flag(argv, "--cache-ttl-days", resolved.get("cache_ttl_days"))
    _extend_flag(argv, "--crawl-budget", resolved.get("crawl_budget"))
    _extend_flag(argv, "--search-term-limit", resolved.get("search_term_limit"))
    _extend_flag(
        argv,
        "--startup-jitter-minutes",
        resolved.get("startup_jitter_minutes"),
    )
    _extend_flag(argv, "--slot-name", resolved.get("slot_name"))
    _extend_browser_flags(argv, resolved)
    return argv


def build_report_weekly_command(resolved):
    argv = _get_runner_command(resolved) + ["report-weekly"]
    _extend_flag(argv, "--db-path", resolved.get("db_path"))
    _extend_flag(argv, "--report-dir", resolved.get("report_dir"))
    _extend_flag(argv, "--days", resolved.get("days"))
    return argv


def build_list_contactable_command(resolved):
    argv = _get_runner_command(resolved) + ["list-contactable"]
    _extend_flag(argv, "--db-path", resolved.get("db_path"))
    _extend_flag(argv, "--lead-type", resolved.get("lead_type"))
    _extend_flag(argv, "--creator-segment", resolved.get("creator_segment"))
    _extend_flag(
        argv,
        "--min-relevance-score",
        resolved.get("min_relevance_score"),
    )
    _extend_flag(argv, "--limit", resolved.get("limit"))
    _extend_flag(argv, "--format", resolved.get("format", "csv"))
    return argv


def build_command(resolved):
    action = str(resolved.get("action", "")).strip().lower()
    if action == "bootstrap":
        raise ValueError("bootstrap uses multi-step execution")
    if action == "login":
        return build_login_command(resolved)
    if action == "crawl_seed":
        return build_crawl_seed_command(resolved)
    if action == "crawl_homefeed":
        return build_crawl_homefeed_command(resolved)
    if action == "collect_nightly":
        return build_collect_nightly_command(resolved)
    if action == "report_weekly":
        return build_report_weekly_command(resolved)
    if action == "list_contactable":
        return build_list_contactable_command(resolved)
    raise ValueError(f"Unsupported action: {resolved.get('action')}")


def run_command(argv, cwd):
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True)


def _tail_file(path, max_lines):
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    if max_lines is not None and max_lines > 0:
        lines = lines[-max_lines:]
    return "\n".join(lines)


def _start_background_job(command, command_display, normalized_action, resolved):
    job_id = resolved.get("job_id") or _make_job_id(normalized_action)
    now = _utc_now()
    logs = _log_dir(resolved)
    logs.mkdir(parents=True, exist_ok=True)
    stdout_path = logs / f"{_safe_slug(job_id)}.out.log"
    stderr_path = logs / f"{_safe_slug(job_id)}.err.log"
    job = {
        "schema_version": JOB_SCHEMA_VERSION,
        "job_id": job_id,
        "action": normalized_action,
        "status": "accepted",
        "command": command_display,
        "argv": [str(part) for part in command],
        "workspace_path": str(_workspace_root(resolved)),
        "stdout_log": str(stdout_path),
        "stderr_log": str(stderr_path),
        "created_at": now,
        "updated_at": now,
        "started_at": None,
        "finished_at": None,
        "returncode": None,
        "summary": f"{normalized_action} accepted as background job.",
        "artifacts": {},
        "missing_artifacts": [],
        "resolved": resolved,
    }
    path = _job_path(resolved, job_id)
    _write_json(path, job)
    _write_heartbeat(resolved)

    wrapper_command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--run-job",
        str(path),
    ]
    try:
        with stdout_path.open("a", encoding="utf-8") as stdout_handle, stderr_path.open(
            "a", encoding="utf-8"
        ) as stderr_handle:
            process = subprocess.Popen(
                wrapper_command,
                cwd=_workspace_root(resolved),
                stdout=stdout_handle,
                stderr=stderr_handle,
                start_new_session=True,
            )
    except OSError as exc:
        job["status"] = "failed"
        job["error_type"] = "execution_error"
        job["message"] = f"{normalized_action} background job failed to start: {exc}."
        job["summary"] = job["message"]
        job["finished_at"] = _utc_now()
        job["updated_at"] = job["finished_at"]
        _write_json(path, job)
        _append_event(resolved, job_id, "error", job["summary"])
        _write_heartbeat(resolved)
        return {
            "status": "error",
            "action": normalized_action,
            "error_type": "execution_error",
            "message": job["message"],
            "command": command_display,
            "stdout": "",
            "stderr": "",
            "suggested_fix": (
                "Verify the Python runtime can launch the background job wrapper, "
                "then rerun the action."
            ),
        }

    job["status"] = "running"
    job["wrapper_pid"] = process.pid
    job["updated_at"] = _utc_now()
    _write_json(path, job)
    _write_heartbeat(resolved)
    return {
        "status": "accepted",
        "action": normalized_action,
        "run_mode": "background",
        "job_id": job_id,
        "pid": process.pid,
        "command": command_display,
        "artifacts": {
            "job": str(path),
            "heartbeat": str(_heartbeat_path(resolved)),
            "stdout_log": str(stdout_path),
            "stderr_log": str(stderr_path),
        },
        "summary": f"{normalized_action} is running in the background.",
        "next_step": "Use action=job_status with this job_id, or let OpenClaw heartbeat read HEARTBEAT.md.",
        "stdout": "",
        "stderr": "",
    }


def _run_job_file(job_path):
    path = Path(job_path)
    job = _read_json(path)
    if not isinstance(job, dict):
        return 2

    resolved = dict(job.get("resolved") or {})
    action = str(job.get("action", "")).strip().lower()
    job_id = job.get("job_id")
    now = _utc_now()
    job.update(
        {
            "status": "running",
            "started_at": job.get("started_at") or now,
            "updated_at": now,
            "wrapper_pid": os.getpid(),
        }
    )
    _write_json(path, job)
    _write_heartbeat(resolved)

    stdout_path = Path(job["stdout_log"])
    stderr_path = Path(job["stderr_log"])
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with stdout_path.open("a", encoding="utf-8") as stdout_handle, stderr_path.open(
            "a", encoding="utf-8"
        ) as stderr_handle:
            process = subprocess.Popen(
                job["argv"],
                cwd=job["workspace_path"],
                stdout=stdout_handle,
                stderr=stderr_handle,
                text=True,
            )
            job["process_pid"] = process.pid
            job["updated_at"] = _utc_now()
            _write_json(path, job)
            _write_heartbeat(resolved)
            returncode = process.wait()
    except OSError as exc:
        finished_at = _utc_now()
        job.update(
            {
                "status": "failed",
                "returncode": None,
                "finished_at": finished_at,
                "updated_at": finished_at,
                "error_type": "execution_error",
                "message": f"{action} failed to start: {exc}.",
                "summary": f"{action} failed to start: {exc}.",
            }
        )
        _write_json(path, job)
        _append_event(resolved, job_id, "error", job["summary"])
        _write_heartbeat(resolved)
        return 1

    artifacts, missing_artifacts = _collect_artifacts(action, resolved)
    finished_at = _utc_now()
    job.update(
        {
            "returncode": returncode,
            "finished_at": finished_at,
            "updated_at": finished_at,
            "artifacts": artifacts,
            "missing_artifacts": missing_artifacts,
        }
    )
    if returncode != 0:
        job["status"] = "failed"
        job["error_type"] = "execution_error"
        job["message"] = f"{action} failed with exit code {returncode}."
        job["summary"] = job["message"]
        _append_event(resolved, job_id, "error", job["summary"])
    elif missing_artifacts:
        job["status"] = "failed"
        job["error_type"] = "artifact_error"
        job["message"] = (
            f"{action} completed but missing required artifacts: "
            f"{', '.join(missing_artifacts)}."
        )
        job["summary"] = job["message"]
        _append_event(resolved, job_id, "error", job["summary"])
    else:
        job["status"] = "succeeded"
        job["summary"] = f"{action} completed successfully."
        _append_event(resolved, job_id, "info", job["summary"])

    _write_json(path, job)
    _write_heartbeat(resolved)
    return 0 if job["status"] == "succeeded" else 1


def _workspace_root(resolved):
    return Path(resolved["workspace_path"])


def _is_red_crawler_workspace(workspace):
    pyproject = workspace / "pyproject.toml"
    if not pyproject.exists():
        return False

    try:
        with pyproject.open("rb") as handle:
            project_name = tomllib.load(handle).get("project", {}).get("name")
    except (OSError, tomllib.TOMLDecodeError):
        return False

    return project_name == EXPECTED_PROJECT_NAME


def _resolve_workspace_path_value(path_value, resolved):
    base = _workspace_root(resolved)
    path = Path(path_value)
    if path.is_absolute():
        return path
    return base / path


def _resolve_artifact_dir(path_value, resolved):
    base = _workspace_root(resolved)
    if path_value is None:
        default_dir = CLI_ARTIFACT_DEFAULTS.get(str(resolved.get("action", "")).strip().lower())
        if default_dir is None:
            return base
        return base / default_dir

    return _resolve_workspace_path_value(path_value, resolved)


def _heartbeat_root(resolved):
    return _resolve_workspace_path_value(
        resolved.get("heartbeat_dir") or DEFAULT_HEARTBEAT_DIR,
        resolved,
    )


def _job_dir(resolved):
    return _heartbeat_root(resolved) / "jobs"


def _event_dir(resolved):
    return _heartbeat_root(resolved) / "events"


def _ack_dir(resolved):
    return _heartbeat_root(resolved) / "acks"


def _log_dir(resolved):
    return _resolve_workspace_path_value(
        resolved.get("job_log_dir") or DEFAULT_LOG_DIR,
        resolved,
    )


def _job_path(resolved, job_id):
    return _job_dir(resolved) / f"{_safe_slug(job_id)}.json"


def _event_path(resolved, job_id):
    return _event_dir(resolved) / f"{_safe_slug(job_id)}.jsonl"


def _heartbeat_path(resolved):
    return _heartbeat_root(resolved) / "HEARTBEAT.md"


def _make_job_id(action):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{_safe_slug(action)}_{timestamp}_{uuid4().hex[:8]}"


def _job_paths_for_workspace(resolved):
    root = _job_dir(resolved)
    if not root.exists():
        return []
    return sorted(root.glob("*.json"))


def _load_job(resolved, job_id):
    path = _job_path(resolved, job_id)
    if not path.exists():
        return None
    return _read_json(path)


def _append_event(resolved, job_id, level, message):
    event = {
        "event_id": f"evt_{uuid4().hex}",
        "job_id": job_id,
        "level": level,
        "message": message,
        "created_at": _utc_now(),
    }
    path = _event_path(resolved, job_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return event


def _iter_events(resolved):
    root = _event_dir(resolved)
    if not root.exists():
        return []
    events = []
    for path in sorted(root.glob("*.jsonl")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)
    return events


def _pending_events(resolved):
    acks = _ack_dir(resolved)
    pending = []
    for event in _iter_events(resolved):
        event_id = event.get("event_id")
        if event_id and not (acks / f"{_safe_slug(event_id)}.ack").exists():
            pending.append(event)
    return pending


def _render_heartbeat(resolved):
    jobs = []
    for path in _job_paths_for_workspace(resolved):
        job = _read_json(path)
        if isinstance(job, dict):
            jobs.append(job)

    active_jobs = [
        job for job in jobs if job.get("status") in {"accepted", "running", "stopping"}
    ]
    pending_events = _pending_events(resolved)
    lines = [
        "# red-crawler heartbeat",
        "",
        "Active jobs:",
    ]
    if active_jobs:
        for job in active_jobs:
            summary = job.get("summary") or job.get("command") or ""
            lines.append(
                f"- {job.get('job_id')}: {job.get('status')}, "
                f"last update {job.get('updated_at')}; {summary}"
            )
    else:
        lines.append("- none")

    lines.extend(["", "Pending user updates:"])
    if pending_events:
        for event in pending_events:
            lines.extend(
                [
                    f"- event_id: {event.get('event_id')}",
                    f"  job_id: {event.get('job_id')}",
                    f"  level: {event.get('level')}",
                    f"  message: {event.get('message')}",
                ]
            )
    else:
        lines.append("- none")

    return "\n".join(lines) + "\n"


def _write_heartbeat(resolved):
    path = _heartbeat_path(resolved)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_render_heartbeat(resolved), encoding="utf-8")
    return path


def _artifact_root(action, resolved):
    if action in {"crawl_seed", "crawl_homefeed"}:
        return _resolve_artifact_dir(resolved.get("output_dir"), resolved)
    if action in {"collect_nightly", "report_weekly"}:
        return _resolve_artifact_dir(resolved.get("report_dir"), resolved)
    return None


def _collect_artifacts(action, resolved):
    expected = EXPECTED_ARTIFACTS.get(action, ())
    if not expected:
        return {}, []

    root = _artifact_root(action, resolved)
    artifacts = {}
    missing = []

    for name in expected:
        artifact_path = root / name
        if artifact_path.exists():
            artifacts[name] = str(artifact_path)
        else:
            missing.append(name)

    return artifacts, missing


def validate_request(resolved):
    action = str(resolved.get("action", "")).strip().lower()
    if action not in KNOWN_ACTIONS:
        return structured_error(
            "validation_error",
            f"Unsupported action: {resolved.get('action')}",
            (
                "Use one of: bootstrap, login, crawl_seed, crawl_homefeed, "
                "collect_nightly, report_weekly, list_contactable."
            ),
        )

    if action == "crawl_seed" and not resolved.get("seed_url"):
        return structured_error(
            "validation_error",
            "seed_url is required for crawl_seed.",
            "Provide a valid Xiaohongshu seed profile URL.",
        )

    if action in {"job_status", "job_logs", "job_stop"} and not resolved.get("job_id"):
        return structured_error(
            "validation_error",
            f"job_id is required for {action}.",
            "Pass the job_id returned by a background crawl action.",
        )
    if action == "ack_event" and not resolved.get("event_id"):
        return structured_error(
            "validation_error",
            "event_id is required for ack_event.",
            "Pass the event_id from HEARTBEAT.md after notifying the user.",
        )

    run_mode = str(resolved.get("run_mode", "sync")).strip().lower()
    if run_mode not in {"sync", "background"}:
        return structured_error(
            "validation_error",
            f"Unsupported run_mode: {resolved.get('run_mode')}",
            "Use run_mode: sync or run_mode: background.",
        )
    if run_mode == "background" and action not in BACKGROUND_ACTIONS:
        return structured_error(
            "validation_error",
            f"run_mode: background is not supported for {action}.",
            "Use background mode only with crawl_seed, crawl_homefeed, or collect_nightly.",
        )

    workspace_path = resolved.get("workspace_path")
    if not workspace_path:
        return structured_error(
            "configuration_error",
            "workspace_path is required.",
            "Provide workspace_path directly or set it in context.config.",
        )

    if action == "login" and not resolved.get("storage_state"):
        return structured_error(
            "configuration_error",
            f"storage_state is required for {action}.",
            "Run login first or provide a storage_state path.",
        )

    try:
        workspace = Path(workspace_path)
    except (TypeError, ValueError):
        return structured_error(
            "configuration_error",
            "workspace_path must be a path-like value.",
            "Provide workspace_path as a string or Path to the red-crawler working directory.",
        )
    if not workspace.exists() or not workspace.is_dir():
        return structured_error(
            "configuration_error",
            f"workspace_path must be an existing directory: {workspace}",
            "Create a working directory for state, database, reports, and outputs, then rerun the action.",
        )

    needs_local_checkout = (
        resolved.get("require_local_checkout") is True
        or resolved.get("sync_dependencies") is True
    )
    if needs_local_checkout and not _is_red_crawler_workspace(workspace):
        return structured_error(
            "configuration_error",
            (
                "workspace_path must be a red-crawler repository root with "
                f"pyproject.toml name = '{EXPECTED_PROJECT_NAME}': {workspace}"
            ),
            "Point workspace_path at a red-crawler checkout, or install the published CLI and disable local-checkout-only setup.",
        )

    if action in {"crawl_seed", "crawl_homefeed", "collect_nightly"} and resolved.get("storage_state"):
        state_path = _resolve_workspace_path_value(resolved["storage_state"], resolved)
        if not state_path.exists():
            return structured_error(
                "configuration_error",
                f"storage_state file does not exist: {state_path}",
                "Run login first, or remove storage_state to crawl without an authenticated session.",
            )

    return {"status": "ok", "action": action, "resolved": resolved}


def _bootstrap_commands(resolved):
    commands = []
    if resolved.get("sync_dependencies") is True:
        commands.append(["uv", "sync"])
    if resolved.get("install_browser") is True:
        commands.append(_get_runner_command(resolved) + ["install-browsers"])

    return commands


def _bootstrap_result(resolved):
    commands = _bootstrap_commands(resolved)
    command_displays = []

    for command in commands:
        command_display = _display_command(command)
        command_displays.append(command_display)
        try:
            completed = run_command(command, cwd=_workspace_root(resolved))
        except OSError as exc:
            return {
                "status": "error",
                "action": "bootstrap",
                "error_type": "execution_error",
                "message": f"bootstrap failed to start: {exc}.",
                "command": command_display,
                "stdout": "",
                "stderr": "",
                "suggested_fix": (
                    "Verify the required bootstrap command is installed and "
                    "available in the current environment, then rerun bootstrap."
                ),
            }

        if completed.returncode != 0:
            return {
                "status": "error",
                "action": "bootstrap",
                "error_type": "execution_error",
                "message": (
                    f"bootstrap step failed with exit code {completed.returncode}."
                ),
                "command": command_display,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "suggested_fix": (
                    "Inspect stderr, fix the failing bootstrap step, and rerun "
                    "bootstrap."
                ),
            }

    metrics = {
        "uv_sync_ran": resolved.get("sync_dependencies") is True,
        "playwright_install_ran": resolved.get("install_browser") is True,
    }
    return {
        "status": "success",
        "action": "bootstrap",
        "command": " && ".join(command_displays),
        "artifacts": {"workspace_path": str(_workspace_root(resolved))},
        "metrics": metrics,
        "next_step": "Run crawl_homefeed or crawl_seed; login is optional if you want an authenticated storage state.",
        "summary": "bootstrap completed successfully.",
        "stdout": "",
        "stderr": "",
    }


def _job_status_result(resolved):
    job_id = resolved["job_id"]
    job = _load_job(resolved, job_id)
    if not isinstance(job, dict):
        return structured_error(
            "not_found",
            f"job_id not found: {job_id}",
            "Check the job_id returned by the background action and the workspace_path.",
        )
    heartbeat = _write_heartbeat(resolved)
    return {
        "status": "success",
        "action": "job_status",
        "job_id": job_id,
        "job": job,
        "artifacts": {
            "job": str(_job_path(resolved, job_id)),
            "heartbeat": str(heartbeat),
            **dict(job.get("artifacts") or {}),
        },
        "summary": job.get("summary", ""),
        "stdout": _tail_file(Path(job.get("stdout_log", "")), resolved.get("tail_lines", 80)),
        "stderr": _tail_file(Path(job.get("stderr_log", "")), resolved.get("tail_lines", 80)),
    }


def _job_logs_result(resolved):
    job_id = resolved["job_id"]
    job = _load_job(resolved, job_id)
    if not isinstance(job, dict):
        return structured_error(
            "not_found",
            f"job_id not found: {job_id}",
            "Check the job_id returned by the background action and the workspace_path.",
        )
    tail_lines = resolved.get("tail_lines", 120)
    return {
        "status": "success",
        "action": "job_logs",
        "job_id": job_id,
        "summary": f"logs for {job_id}.",
        "artifacts": {
            "stdout_log": job.get("stdout_log", ""),
            "stderr_log": job.get("stderr_log", ""),
        },
        "stdout": _tail_file(Path(job.get("stdout_log", "")), tail_lines),
        "stderr": _tail_file(Path(job.get("stderr_log", "")), tail_lines),
    }


def _terminate_pid(pid):
    if not pid:
        return False
    try:
        os.kill(int(pid), signal.SIGTERM)
    except (OSError, ValueError):
        return False
    return True


def _job_stop_result(resolved):
    job_id = resolved["job_id"]
    job = _load_job(resolved, job_id)
    if not isinstance(job, dict):
        return structured_error(
            "not_found",
            f"job_id not found: {job_id}",
            "Check the job_id returned by the background action and the workspace_path.",
        )

    stopped_process = _terminate_pid(job.get("process_pid"))
    stopped_wrapper = _terminate_pid(job.get("wrapper_pid"))
    now = _utc_now()
    job["status"] = "stopping" if stopped_process or stopped_wrapper else job.get("status")
    job["updated_at"] = now
    if stopped_process or stopped_wrapper:
        job["summary"] = f"stop requested for {job_id}."
    else:
        job["summary"] = f"no running process was found for {job_id}."
    _write_json(_job_path(resolved, job_id), job)
    _write_heartbeat(resolved)
    return {
        "status": "success",
        "action": "job_stop",
        "job_id": job_id,
        "job": job,
        "summary": job["summary"],
        "artifacts": {
            "job": str(_job_path(resolved, job_id)),
            "heartbeat": str(_heartbeat_path(resolved)),
        },
        "stdout": "",
        "stderr": "",
    }


def _ack_event_result(resolved):
    event_id = resolved["event_id"]
    ack_path = _ack_dir(resolved) / f"{_safe_slug(event_id)}.ack"
    ack_path.parent.mkdir(parents=True, exist_ok=True)
    ack_path.write_text(_utc_now() + "\n", encoding="utf-8")
    heartbeat = _write_heartbeat(resolved)
    return {
        "status": "success",
        "action": "ack_event",
        "event_id": event_id,
        "summary": f"acknowledged event {event_id}.",
        "artifacts": {
            "ack": str(ack_path),
            "heartbeat": str(heartbeat),
        },
        "stdout": "",
        "stderr": "",
    }


async def handler(input, context):
    resolved = merge_config(input, context or {})
    if isinstance(resolved, dict) and resolved.get("status") == "error":
        return resolved
    validation = validate_request(resolved)
    if validation["status"] == "error":
        return validation

    normalized_action = validation["action"]
    resolved = dict(validation["resolved"])
    resolved["action"] = normalized_action
    if normalized_action == "bootstrap":
        return _bootstrap_result(resolved)
    if normalized_action == "job_status":
        return _job_status_result(resolved)
    if normalized_action == "job_logs":
        return _job_logs_result(resolved)
    if normalized_action == "job_stop":
        return _job_stop_result(resolved)
    if normalized_action == "ack_event":
        return _ack_event_result(resolved)
    command = build_command(resolved)
    command_display = _display_command(command)
    if str(resolved.get("run_mode", "sync")).strip().lower() == "background":
        return _start_background_job(command, command_display, normalized_action, resolved)
    try:
        completed = run_command(command, cwd=_workspace_root(resolved))
    except OSError as exc:
        return {
            "status": "error",
            "action": normalized_action,
            "error_type": "execution_error",
            "message": f"{normalized_action} failed to start: {exc}.",
            "command": command_display,
            "stdout": "",
            "stderr": "",
            "suggested_fix": (
                "Verify the runner command is installed and available from the "
                "current environment, then rerun the action."
            ),
        }

    if completed.returncode != 0:
        return {
            "status": "error",
            "action": normalized_action,
            "error_type": "execution_error",
            "message": (
                f"{normalized_action} failed with exit code {completed.returncode}."
            ),
            "command": command_display,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "suggested_fix": (
                "Inspect stderr, verify the red-crawler CLI arguments, and rerun "
                "after fixing the underlying issue."
            ),
        }

    artifacts, missing_artifacts = _collect_artifacts(normalized_action, resolved)
    if missing_artifacts:
        return {
            "status": "error",
            "action": normalized_action,
            "error_type": "artifact_error",
            "message": (
                f"{normalized_action} completed but missing required artifacts: "
                f"{', '.join(missing_artifacts)}."
            ),
            "command": command_display,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "suggested_fix": (
                "Verify the CLI completed in the expected output directory and "
                "check whether the underlying command wrote all required files."
            ),
        }

    return {
        "status": "success",
        "action": normalized_action,
        "command": command_display,
        "artifacts": artifacts,
        "summary": f"{normalized_action} completed successfully.",
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--run-job":
        raise SystemExit(_run_job_file(sys.argv[2]))
    raise SystemExit("usage: index.py --run-job JOB_JSON")
